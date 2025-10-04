"""
Assignment Orchestrator - Python Implementation

This module provides a comprehensive Python implementation
that coordinates the complete workflow for managing GitHub Classroom assignments.

Main workflow steps:
1. Template synchronization with classroom 
2. Student repository discovery
3. Secret management across repositories
4. Optional student assistance 
5. Optional collaborator cycling

Author: Classroom Pilot Team
"""

import os
import sys
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, TaskID
from rich.table import Table

from ..config.global_config import GlobalConfig, get_global_config, load_global_config
from ..secrets.github_secrets import GitHubSecretsManager
from ..utils.github_classroom_api import GitHubClassroomAPI
from ..utils.logger import get_logger

# Module-level logger for backward compatibility with tests
logger = get_logger("assignments.orchestrator")


class WorkflowStep(Enum):
    """Available workflow steps."""
    SYNC = "sync"
    DISCOVER = "discover"
    SECRETS = "secrets"
    ASSIST = "assist"
    CYCLE = "cycle"


@dataclass
class StepResult:
    """Result of executing a workflow step."""
    step: WorkflowStep
    success: bool
    message: str
    duration: float
    data: Optional[Dict] = None


@dataclass
class WorkflowConfig:
    """Configuration for workflow execution."""
    enabled_steps: Set[WorkflowStep]
    dry_run: bool = False
    verbose: bool = False
    force_yes: bool = False
    step_override: Optional[WorkflowStep] = None
    skip_steps: Set[WorkflowStep] = None

    def __post_init__(self):
        if self.skip_steps is None:
            self.skip_steps = set()


class AssignmentOrchestrator:
    """
    Main workflow coordinator for GitHub Classroom assignments.

    Orchestrates template sync, discovery, secrets, and assistance steps
    using the Python implementations we've already created.
    """

    def __init__(self, config_file: Optional[Path] = None):
        """Initialize the orchestrator with configuration."""
        self.logger = get_logger(__name__)
        self.console = Console()

        # Load global configuration
        if config_file:
            try:
                load_global_config(str(config_file))
            except FileNotFoundError:
                self.logger.warning(
                    f"Configuration file not found: {config_file}")
        self.global_config = get_global_config()
        self.config_file = config_file or Path.cwd() / "assignment.conf"

        # Initialize components only if config is loaded
        if self.global_config:
            self.classroom_api = GitHubClassroomAPI(self.global_config)
            self.secrets_manager = GitHubSecretsManager(self.global_config)
        else:
            self.classroom_api = None
            self.secrets_manager = None

        # Workflow state
        self.results: List[StepResult] = []
        self.start_time: Optional[float] = None
        self.discovered_repos: List[str] = []

    def validate_configuration(self) -> bool:
        """Validate that required configuration is present."""
        try:
            # Check if global config is loaded
            if not self.global_config:
                self.logger.error("Global configuration not loaded")
                return False

            # Check required fields
            required_fields = [
                'classroom_url',
                'template_repo_url',
                'github_organization',
                'assignment_name'
            ]

            for field in required_fields:
                if not getattr(self.global_config, field, None):
                    self.logger.error(
                        f"Required configuration field missing: {field}")
                    return False

            self.logger.info("Configuration validation passed")
            return True

        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False

    def show_configuration_summary(self) -> None:
        """Display configuration summary."""
        table = Table(title="Assignment Configuration")
        table.add_column("Setting", style="bold blue")
        table.add_column("Value", style="green")

        table.add_row(
            "Assignment", self.global_config.assignment_name or "Not set")
        table.add_row("Organization",
                      self.global_config.github_organization or "Not set")
        table.add_row("Template Repository",
                      self.global_config.template_repo_url or "Not set")
        table.add_row("Classroom URL",
                      self.global_config.classroom_url or "Not set")
        table.add_row("Assignment File",
                      self.global_config.assignment_file or "assignment.conf")

        # Show enabled workflow steps
        enabled_steps = []
        if getattr(self.global_config, 'step_sync_template', True):
            enabled_steps.append("✓ Sync Template")
        if getattr(self.global_config, 'step_discover_repos', True):
            enabled_steps.append("✓ Discover Repos")
        if getattr(self.global_config, 'step_manage_secrets', True):
            enabled_steps.append("✓ Manage Secrets")
        if getattr(self.global_config, 'step_assist_students', False):
            enabled_steps.append("✓ Assist Students")
        if getattr(self.global_config, 'step_cycle_collaborators', False):
            enabled_steps.append("✓ Cycle Collaborators")

        table.add_row("Workflow Steps", "\n".join(enabled_steps))

        self.console.print(table)

    def confirm_execution(self, workflow_config: WorkflowConfig) -> bool:
        """Confirm workflow execution with user."""
        if workflow_config.force_yes or workflow_config.dry_run:
            return True

        return typer.confirm("Do you want to proceed with this workflow?")

    def step_sync_template(self, dry_run: bool = False) -> StepResult:
        """
        Step 1: Synchronize template with classroom.

        Note: This step requires template push functionality that will be
        implemented in the push manager component.
        For now, we'll provide a placeholder that logs the action.
        """
        start_time = time.time()

        if not getattr(self.global_config, 'step_sync_template', True):
            return StepResult(
                step=WorkflowStep.SYNC,
                success=True,
                message="Skipped (disabled in config)",
                duration=0.0
            )

        try:
            if dry_run:
                self.logger.info(
                    "DRY RUN: Would synchronize template with classroom")
                self.logger.info(
                    f"Template repo: {self.global_config.template_repo_url}")
                message = "DRY RUN: Template sync simulated"
            else:
                # Template push functionality is available via push manager
                self.logger.warning(
                    "Template sync requires push manager integration")
                self.logger.info(
                    "Use 'classroom-pilot repos push' for template synchronization")
                message = "Template sync available via push manager"

            duration = time.time() - start_time
            return StepResult(
                step=WorkflowStep.SYNC,
                success=True,
                message=message,
                duration=duration
            )

        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"Template sync failed: {e}")
            return StepResult(
                step=WorkflowStep.SYNC,
                success=False,
                message=f"Template sync failed: {e}",
                duration=duration
            )

    def step_discover_repos(self, dry_run: bool = False) -> StepResult:
        """Step 2: Discover student repositories using GitHub Classroom API."""
        start_time = time.time()

        if not getattr(self.global_config, 'step_discover_repos', True):
            return StepResult(
                step=WorkflowStep.DISCOVER,
                success=True,
                message="Skipped (disabled in config)",
                duration=0.0
            )

        try:
            if dry_run:
                self.logger.info(
                    "DRY RUN: Would discover student repositories")
                self.logger.info(
                    f"Organization: {self.global_config.github_organization}")
                self.logger.info(
                    f"Assignment: {self.global_config.assignment_name}")
                repos = ["https://github.com/example/student-repo-1",
                         "https://github.com/example/student-repo-2"]
                message = f"DRY RUN: Would discover {len(repos)} repositories"
            else:
                # Use our existing GitHub Classroom API integration
                self.logger.info("Discovering student repositories...")
                repos = self.classroom_api.discover_student_repositories()
                self.discovered_repos = repos

                # Save to output files for legacy compatibility
                output_dir = Path(
                    getattr(self.global_config, 'output_dir', 'scripts'))
                output_dir.mkdir(exist_ok=True)

                batch_file = output_dir / \
                    getattr(self.global_config, 'student_repos_file',
                            'student-repos-batch.txt')
                students_only_file = output_dir / \
                    getattr(self.global_config, 'students_only_file',
                            'student-repos-students-only.txt')

                # Write all repositories
                with open(batch_file, 'w') as f:
                    for repo in repos:
                        f.write(f"{repo}\n")

                # Write students-only (exclude instructor-tests)
                student_repos = [
                    repo for repo in repos if 'instructor-tests' not in repo]
                with open(students_only_file, 'w') as f:
                    for repo in student_repos:
                        f.write(f"{repo}\n")

                self.logger.info(f"Total repositories: {len(repos)}")
                self.logger.info(f"Student repositories: {len(student_repos)}")
                self.logger.info(f"Batch file: {batch_file}")
                self.logger.info(f"Students-only file: {students_only_file}")

                message = f"Discovered {len(repos)} repositories ({len(student_repos)} student repos)"

            duration = time.time() - start_time
            return StepResult(
                step=WorkflowStep.DISCOVER,
                success=True,
                message=message,
                duration=duration,
                data={"repositories": repos if not dry_run else None,
                      "count": len(repos) if not dry_run else 2}
            )

        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"Repository discovery failed: {e}")
            return StepResult(
                step=WorkflowStep.DISCOVER,
                success=False,
                message=f"Repository discovery failed: {e}",
                duration=duration
            )

    def step_manage_secrets(self, dry_run: bool = False) -> StepResult:
        """Step 3: Manage secrets across repositories using our GitHub secrets manager."""
        start_time = time.time()

        if not getattr(self.global_config, 'step_manage_secrets', True):
            return StepResult(
                step=WorkflowStep.SECRETS,
                success=True,
                message="Skipped (disabled in config)",
                duration=0.0
            )

        try:
            # Check if we have repositories to work with
            if not dry_run and not self.discovered_repos:
                # Try to load from file if discovery wasn't run
                output_dir = Path(
                    getattr(self.global_config, 'output_dir', 'scripts'))
                batch_file = output_dir / \
                    getattr(self.global_config, 'student_repos_file',
                            'student-repos-batch.txt')

                if batch_file.exists():
                    with open(batch_file, 'r') as f:
                        self.discovered_repos = [
                            line.strip() for line in f if line.strip().startswith('https://')]
                else:
                    return StepResult(
                        step=WorkflowStep.SECRETS,
                        success=False,
                        message="No repositories found. Run discovery step first.",
                        duration=time.time() - start_time
                    )

            # Use our existing GitHub secrets manager
            if dry_run:
                self.logger.info(
                    "DRY RUN: Would manage secrets for student repositories")
                message = "DRY RUN: Secret management simulated"
                success_count = len(
                    self.discovered_repos) if self.discovered_repos else 2
                failed_count = 0
            else:
                self.logger.info(
                    f"Managing secrets for {len(self.discovered_repos)} repositories...")
                success_count, failed_count = self.secrets_manager.distribute_secrets_to_repositories(
                    self.discovered_repos,
                    dry_run=False
                )
                message = f"Secrets distributed: {success_count} success, {failed_count} failed"

            duration = time.time() - start_time
            return StepResult(
                step=WorkflowStep.SECRETS,
                success=failed_count == 0,
                message=message,
                duration=duration,
                data={"success_count": success_count,
                      "failed_count": failed_count}
            )

        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"Secret management failed: {e}")
            return StepResult(
                step=WorkflowStep.SECRETS,
                success=False,
                message=f"Secret management failed: {e}",
                duration=duration
            )

    def step_assist_students(self, dry_run: bool = False) -> StepResult:
        """
        Step 4: Student assistance.

        Note: This step requires student update helper functionality that will be
        implemented in the student helper component.
        """
        start_time = time.time()

        if not getattr(self.global_config, 'step_assist_students', False):
            return StepResult(
                step=WorkflowStep.ASSIST,
                success=True,
                message="Skipped (disabled in config)",
                duration=0.0
            )

        try:
            if dry_run:
                self.logger.info("DRY RUN: Would run student assistance tools")
                message = "DRY RUN: Student assistance simulated"
            else:
                # Student assistance functionality is available via student helper
                self.logger.warning(
                    "Student assistance requires direct student helper usage")
                self.logger.info(
                    "Use 'classroom-pilot assignments student-help' for assistance tools")
                message = "Student assistance available via student helper"

            duration = time.time() - start_time
            return StepResult(
                step=WorkflowStep.ASSIST,
                success=True,
                message=message,
                duration=duration
            )

        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"Student assistance failed: {e}")
            return StepResult(
                step=WorkflowStep.ASSIST,
                success=False,
                message=f"Student assistance failed: {e}",
                duration=duration
            )

    def step_cycle_collaborators(self, dry_run: bool = False) -> StepResult:
        """
        Step 5: Cycle collaborator access.

        Note: This step requires collaborator cycling functionality that will be
        implemented in the cycle collaborator component.
        """
        start_time = time.time()

        if not getattr(self.global_config, 'step_cycle_collaborators', False):
            return StepResult(
                step=WorkflowStep.CYCLE,
                success=True,
                message="Skipped (disabled in config)",
                duration=0.0
            )

        try:
            if dry_run:
                self.logger.info("DRY RUN: Would cycle collaborator access")
                message = "DRY RUN: Collaborator cycling simulated"
            else:
                # Collaborator cycling functionality is available via cycle collaborator
                self.logger.warning(
                    "Collaborator cycling requires direct cycle collaborator usage")
                self.logger.info(
                    "Use 'classroom-pilot repos cycle-collaborator' for access management")
                message = "Collaborator cycling available via cycle collaborator"

            duration = time.time() - start_time
            return StepResult(
                step=WorkflowStep.CYCLE,
                success=True,
                message=message,
                duration=duration
            )

        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"Collaborator cycling failed: {e}")
            return StepResult(
                step=WorkflowStep.CYCLE,
                success=False,
                message=f"Collaborator cycling failed: {e}",
                duration=duration
            )

    def execute_single_step(self, step: WorkflowStep, dry_run: bool = False) -> StepResult:
        """Execute a single workflow step."""
        self.logger.info(f"Executing single step: {step.value}")

        step_methods = {
            WorkflowStep.SYNC: self.step_sync_template,
            WorkflowStep.DISCOVER: self.step_discover_repos,
            WorkflowStep.SECRETS: self.step_manage_secrets,
            WorkflowStep.ASSIST: self.step_assist_students,
            WorkflowStep.CYCLE: self.step_cycle_collaborators,
        }

        if step not in step_methods:
            raise ValueError(f"Unknown step: {step}")

        return step_methods[step](dry_run)

    def execute_workflow(self, workflow_config: WorkflowConfig) -> List[StepResult]:
        """Execute the complete workflow or a specific step."""
        self.start_time = time.time()
        self.results = []

        self.logger.info("Starting assignment workflow execution")

        # Show workflow header
        if workflow_config.dry_run:
            self.console.print(
                Panel("🧪 DRY RUN MODE - No actual changes will be made", style="yellow"))

        try:
            # Execute single step if specified
            if workflow_config.step_override:
                result = self.execute_single_step(
                    workflow_config.step_override, workflow_config.dry_run)
                self.results.append(result)
                return self.results

            # Execute full workflow
            steps_to_run = [
                (WorkflowStep.SYNC, self.step_sync_template),
                (WorkflowStep.DISCOVER, self.step_discover_repos),
                (WorkflowStep.SECRETS, self.step_manage_secrets),
                (WorkflowStep.ASSIST, self.step_assist_students),
                (WorkflowStep.CYCLE, self.step_cycle_collaborators),
            ]

            repos_discovered = False

            with Progress() as progress:
                task = progress.add_task(
                    "Workflow Progress", total=len(steps_to_run))

                for step_enum, step_method in steps_to_run:
                    # Skip if not in enabled steps or is in skip list
                    if (workflow_config.enabled_steps and
                            step_enum not in workflow_config.enabled_steps):
                        continue
                    if step_enum in workflow_config.skip_steps:
                        continue

                    progress.update(
                        task, description=f"Executing {step_enum.value}...")
                    result = step_method(workflow_config.dry_run)
                    self.results.append(result)

                    # Track if repositories were discovered for dependent steps
                    if step_enum == WorkflowStep.DISCOVER and result.success:
                        repos_discovered = True

                    # Skip repository-dependent steps if no repos were discovered
                    if not repos_discovered and step_enum in [WorkflowStep.SECRETS, WorkflowStep.ASSIST, WorkflowStep.CYCLE]:
                        if not workflow_config.dry_run:
                            self.logger.warning(
                                f"Skipping {step_enum.value} (no repositories discovered)")
                            continue

                    progress.advance(task)

            return self.results

        except Exception as e:
            self.logger.error(f"Workflow execution failed: {e}")
            raise

    def generate_workflow_report(self) -> Dict:
        """Generate a comprehensive workflow report."""
        if not self.start_time:
            return {}

        total_duration = time.time() - self.start_time

        # Count successes and failures
        successful_steps = [r for r in self.results if r.success]
        failed_steps = [r for r in self.results if not r.success]

        # Create summary table
        table = Table(title="Workflow Execution Report")
        table.add_column("Step", style="bold")
        table.add_column("Status", style="bold")
        table.add_column("Duration", style="cyan")
        table.add_column("Message", style="dim")

        for result in self.results:
            status = "✅ SUCCESS" if result.success else "❌ FAILED"
            status_style = "green" if result.success else "red"
            table.add_row(
                result.step.value.title(),
                f"[{status_style}]{status}[/{status_style}]",
                f"{result.duration:.2f}s",
                result.message
            )

        self.console.print(table)

        # Summary
        self.console.print(
            f"\n[bold green]Total Steps:[/] {len(self.results)}")
        self.console.print(
            f"[bold green]Successful:[/] {len(successful_steps)}")
        self.console.print(f"[bold red]Failed:[/] {len(failed_steps)}")
        self.console.print(
            f"[bold blue]Total Duration:[/] {total_duration:.2f}s")

        return {
            "total_steps": len(self.results),
            "successful_steps": len(successful_steps),
            "failed_steps": len(failed_steps),
            "total_duration": total_duration,
            "results": [
                {
                    "step": r.step.value,
                    "success": r.success,
                    "message": r.message,
                    "duration": r.duration,
                    "data": r.data
                }
                for r in self.results
            ]
        }

    # Legacy methods for backward compatibility with existing tests
    def run_complete_workflow(self):
        """Legacy method - use execute_workflow instead."""
        logger.info("Running complete workflow")
        workflow_config = WorkflowConfig(
            enabled_steps=set(WorkflowStep),
            dry_run=False,
            verbose=False,
            force_yes=True
        )
        return self.execute_workflow(workflow_config)

    def sync_template(self):
        """Legacy method - use step_sync_template instead."""
        logger.info("Syncing template repository")
        return self.step_sync_template(dry_run=False)

    def discover_repositories(self):
        """Legacy method - use step_discover_repos instead."""
        logger.info("Discovering student repositories")
        return self.step_discover_repos(dry_run=False)

    def manage_secrets(self):
        """Legacy method - use step_manage_secrets instead."""
        logger.info("Managing secrets")
        return self.step_manage_secrets(dry_run=False)

    def assist_students(self):
        """Legacy method - use step_assist_students instead."""
        logger.info("Assisting students")
        return self.step_assist_students(dry_run=False)

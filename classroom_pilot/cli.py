"""
Enhanced CLI interface for Classroom Pilot with modular package structure.

This module provides a comprehensive command-line interface organized by functional areas:
- assignments: Setup, orchestration, and management
- repos: Repository operations and collaborator management  
- secrets: Token and secret management
- automation: Cron jobs and batch processing
"""

import typer
from pathlib import Path

from .utils import setup_logging, get_logger
from .assignments.setup import AssignmentSetup
from .bash_wrapper import BashWrapper
from .config import ConfigLoader

# Initialize logger
logger = get_logger("cli")

# Create the main Typer application
app = typer.Typer(
    help="Classroom Pilot - Comprehensive automation suite for managing GitHub Classroom assignments.",
    no_args_is_help=True
)

# Create subcommand groups
assignments_app = typer.Typer(
    help="Assignment setup, orchestration, and management commands")
repos_app = typer.Typer(
    help="Repository operations and collaborator management commands")
secrets_app = typer.Typer(help="Secret and token management commands")
automation_app = typer.Typer(
    help="Automation, scheduling, and batch processing commands")

# Add subcommand groups to main app
app.add_typer(assignments_app, name="assignments")
app.add_typer(repos_app, name="repos")
app.add_typer(secrets_app, name="secrets")
app.add_typer(automation_app, name="automation")


# Assignment Commands
@assignments_app.command("setup")
def assignment_setup():
    """Setup a new assignment configuration (Interactive Python wizard)."""
    setup_logging()
    logger.info("Starting assignment setup wizard")

    setup = AssignmentSetup()
    setup.run_wizard()


@assignments_app.command("orchestrate")
def assignment_orchestrate(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """Run the complete assignment workflow (sync, discover, secrets, assist)."""
    setup_logging(verbose)
    logger.info("Starting assignment orchestration")

    # Use bash wrapper for now - TODO: migrate to pure Python
    config = ConfigLoader(Path(config_file)).load()
    wrapper = BashWrapper(config, dry_run=dry_run, verbose=verbose)

    success = wrapper.assignment_orchestrator(workflow_type="run")
    if not success:
        logger.error("Assignment orchestration failed")
        raise typer.Exit(code=1)


@assignments_app.command("manage")
def assignment_manage():
    """High-level assignment lifecycle management."""
    setup_logging()
    logger.info("Assignment management interface")

    # TODO: Implement assignment management
    typer.echo("🚧 Assignment management commands coming soon!")


# Repository Commands
@repos_app.command("fetch")
def repos_fetch(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """Discover and fetch student repositories from GitHub Classroom."""
    setup_logging(verbose)
    logger.info("Fetching student repositories")

    # Use bash wrapper for now - TODO: migrate to pure Python
    config = ConfigLoader(Path(config_file)).load()
    wrapper = BashWrapper(config, dry_run=dry_run, verbose=verbose)

    success = wrapper.fetch_student_repos()
    if not success:
        logger.error("Repository fetch failed")
        raise typer.Exit(code=1)


@repos_app.command("update")
def repos_update(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """Update assignment configuration and student repositories."""
    setup_logging(verbose)
    logger.info("Updating repositories")

    # Use bash wrapper for now - TODO: migrate to pure Python
    config = ConfigLoader(Path(config_file)).load()
    wrapper = BashWrapper(config, dry_run=dry_run, verbose=verbose)

    success = wrapper.update_assignment()
    if not success:
        logger.error("Repository update failed")
        raise typer.Exit(code=1)


@repos_app.command("push")
def repos_push(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """Sync template repository to GitHub Classroom."""
    setup_logging(verbose)
    logger.info("Pushing to classroom repository")

    # Use bash wrapper for now - TODO: migrate to pure Python
    config = ConfigLoader(Path(config_file)).load()
    wrapper = BashWrapper(config, dry_run=dry_run, verbose=verbose)

    success = wrapper.push_to_classroom()
    if not success:
        logger.error("Repository push failed")
        raise typer.Exit(code=1)


@repos_app.command("cycle-collaborator")
def repos_cycle_collaborator(
    assignment_prefix: str = typer.Option(
        None, "--assignment-prefix", help="Assignment prefix"),
    username: str = typer.Option(None, "--username", help="Username"),
    organization: str = typer.Option(
        None, "--organization", help="Organization"),
    list_collaborators: bool = typer.Option(
        False, "--list", help="List collaborators"),
    force: bool = typer.Option(False, "--force", help="Force cycling"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """Cycle repository collaborator permissions."""
    setup_logging(verbose)
    logger.info("Cycling collaborator permissions")

    # Use bash wrapper for now - TODO: migrate to pure Python
    config = ConfigLoader(Path(config_file)).load()
    wrapper = BashWrapper(config, dry_run=dry_run, verbose=verbose)

    success = wrapper.cycle_collaborator(
        assignment_prefix=assignment_prefix,
        username=username,
        organization=organization,
        list_mode=list_collaborators,
        force_cycle=force
    )
    if not success:
        logger.error("Collaborator cycling failed")
        raise typer.Exit(code=1)


# Secret Commands
@secrets_app.command("add")
def secrets_add(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """Add or update secrets in student repositories."""
    setup_logging(verbose)
    logger.info("Adding secrets to student repositories")

    # Use bash wrapper for now - TODO: migrate to pure Python
    config = ConfigLoader(Path(config_file)).load()
    wrapper = BashWrapper(config, dry_run=dry_run, verbose=verbose)

    success = wrapper.add_secrets_to_students()
    if not success:
        logger.error("Secret management failed")
        raise typer.Exit(code=1)


@secrets_app.command("manage")
def secrets_manage():
    """Advanced secret and token management."""
    setup_logging()
    logger.info("Secret management interface")

    # TODO: Implement secret management
    typer.echo("🚧 Advanced secret management commands coming soon!")


# Automation Commands
@automation_app.command("cron")
def automation_cron(
    action: str = typer.Option(
        "status", "--action", "-a", help="Action to perform (status, install, remove)"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """Manage cron automation jobs."""
    setup_logging(verbose)
    logger.info(f"Managing cron jobs: {action}")

    # Use bash wrapper for now - TODO: migrate to pure Python
    config = ConfigLoader(Path(config_file)).load()
    wrapper = BashWrapper(config, dry_run=dry_run, verbose=verbose)

    success = wrapper.manage_cron(action)
    if not success:
        logger.error("Cron management failed")
        raise typer.Exit(code=1)


@automation_app.command("sync")
def automation_sync(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """Execute scheduled synchronization tasks."""
    setup_logging(verbose)
    logger.info("Running scheduled sync")

    # Use bash wrapper for now - TODO: migrate to pure Python
    config = ConfigLoader(Path(config_file)).load()
    wrapper = BashWrapper(config, dry_run=dry_run, verbose=verbose)

    success = wrapper.cron_sync()
    if not success:
        logger.error("Scheduled sync failed")
        raise typer.Exit(code=1)


@automation_app.command("batch")
def automation_batch():
    """Run batch processing operations."""
    setup_logging()
    logger.info("Batch processing interface")

    # TODO: Implement batch processing
    typer.echo("🚧 Batch processing commands coming soon!")


# Legacy compatibility commands (top-level)
@app.command("setup")
def legacy_setup():
    """Setup a new assignment configuration (Interactive Python wizard) - Legacy command."""
    typer.echo("🔄 Redirecting to: classroom-pilot assignments setup")
    assignment_setup()


@app.command("run")
def legacy_run(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """Run the complete classroom workflow - Legacy command."""
    typer.echo("🔄 Redirecting to: classroom-pilot assignments orchestrate")
    assignment_orchestrate(
        dry_run=dry_run, verbose=verbose, config_file=config_file)


# Utility commands
@app.command("version")
def version():
    """Show version information."""
    typer.echo("Classroom Pilot v3.0.0-alpha.1")
    typer.echo("Modular Python CLI for GitHub Classroom automation")
    typer.echo("https://github.com/hugo-valle/classroom-pilot")


def main():
    """Main entry point for the CLI application."""
    app()


if __name__ == "__main__":
    main()

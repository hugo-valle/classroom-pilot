"""
Enhanced CLI Interface for Classroom Pilot GitHub Assignment Management.

This module provides:
- Comprehensive command-line interface organized by functional areas
- Modular command structure with intuitive subcommand organization
- Rich console output with progress tracking and error handling
- Legacy command support for backward compatibility
- Integration with all core Classroom Pilot functionality including assignments,
  repositories, secrets, and automation workflows
"""

import typer
from pathlib import Path
from typing import Optional, List

from .utils import setup_logging, get_logger
from .assignments.setup import AssignmentSetup
from .config import ConfigLoader
from .config.global_config import load_global_config, get_global_config

# Initialize logger
logger = get_logger("cli")


def version_callback(value: bool):
    """Callback to handle --version flag."""
    if value:
        from . import __version__
        typer.echo(f"Classroom Pilot {__version__}")
        typer.echo("Modular Python CLI for GitHub Classroom automation")
        typer.echo("https://github.com/hugo-valle/classroom-pilot")
        raise typer.Exit()


# Create the main Typer application
app = typer.Typer(
    help="Classroom Pilot - Comprehensive automation suite for managing GitHub Classroom assignments.",
    no_args_is_help=True
)


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,
        help="Show the application version and exit."
    ),
    config_file: str = typer.Option(
        "assignment.conf",
        "--config",
        help="Configuration file to load (default: assignment.conf)"
    ),
    assignment_root: str = typer.Option(
        None,
        "--assignment-root",
        help="Root directory containing assignment.conf file"
    )
):
    """
    Classroom Pilot - Comprehensive automation suite for managing GitHub Classroom assignments.

    This tool automatically loads configuration from assignment.conf file and makes
    all configuration variables globally available to all commands.
    """
    # Set up logging first
    setup_logging()

    # Try to load global configuration (don't fail if not found, some commands create it)
    try:
        assignment_root_path = Path(
            assignment_root) if assignment_root else None
        load_global_config(config_file, assignment_root_path)
        logger.info("✅ Global configuration loaded and ready")
    except FileNotFoundError:
        # Config file not found - this is OK for commands like 'assignments setup'
        logger.debug(
            f"Configuration file {config_file} not found - will be created by setup command")
    except Exception as e:
        logger.warning(f"Failed to load configuration: {e}")
        logger.info("Some commands may not work properly without configuration")


# Create subcommand groups
assignments_app = typer.Typer(
    help="Assignment setup, orchestration, and management commands")
repos_app = typer.Typer(
    help="Repository operations and collaborator management commands")
secrets_app = typer.Typer(help="Secret and token management commands")
automation_app = typer.Typer(
    help="Automation, scheduling, and batch processing commands")


# Universal options callback for assignments commands
@assignments_app.callback()
def assignments_callback(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"
    )
):
    """Assignment setup, orchestration, and management commands."""
    if verbose:
        setup_logging(verbose=True)
    # Store options in context for child commands to access
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['dry_run'] = dry_run


# Universal options callback for repos commands
@repos_app.callback()
def repos_callback(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"
    )
):
    """Repository operations and collaborator management commands."""
    if verbose:
        setup_logging(verbose=True)
    # Store options in context for child commands to access
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['dry_run'] = dry_run


# Universal options callback for secrets commands
@secrets_app.callback()
def secrets_callback(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"
    )
):
    """Secret and token management commands."""
    if verbose:
        setup_logging(verbose=True)
    # Store options in context for child commands to access
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['dry_run'] = dry_run


# Universal options callback for automation commands
@automation_app.callback()
def automation_callback(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"
    )
):
    """Automation, scheduling, and batch processing commands."""
    if verbose:
        setup_logging(verbose=True)
    # Store options in context for child commands to access
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['dry_run'] = dry_run


# Add subcommand groups to main app
app.add_typer(assignments_app, name="assignments")
app.add_typer(repos_app, name="repos")
app.add_typer(secrets_app, name="secrets")
app.add_typer(automation_app, name="automation")


# Assignment Commands
@assignments_app.command("setup")
def assignment_setup(
    ctx: typer.Context,
    url: str = typer.Option(
        None,
        "--url",
        help="GitHub Classroom URL for simplified setup (auto-extracts organization and assignment info)"
    ),
    simplified: bool = typer.Option(
        False,
        "--simplified",
        help="Use simplified setup wizard with minimal prompts"
    )
):
    """
    Launch interactive wizard to configure a new assignment.

    This command initializes an interactive setup wizard that guides users through
    the complete process of configuring a new GitHub Classroom assignment. The wizard
    collects all required configuration parameters and generates the assignment.conf
    file needed for subsequent operations.

    Two setup modes are available:

    1. Standard Setup (default):
       - Full interactive wizard with all configuration options
       - Step-by-step guidance through all settings
       - Comprehensive validation and error checking

    2. Simplified Setup (--simplified or --url):
       - Auto-extracts organization and assignment info from GitHub Classroom URL
       - Uses GitHub API to fetch assignment details automatically
       - Minimal user prompts for essential missing information
       - Ideal for quick setup with existing classroom assignments

    The setup process includes:
    - Assignment metadata configuration (name, description, organization)
    - GitHub repository settings and template configuration  
    - Student repository discovery parameters
    - Interactive validation and confirmation of all collected data
    - Secrets and token management setup
    - Automation and workflow preferences

    Supports universal options: --verbose, --dry-run

    Raises:
        SystemExit: If setup process is interrupted or fails.

    Examples:
        $ classroom-pilot assignments setup
        # Full interactive wizard

        $ classroom-pilot assignments setup --simplified
        # Simplified wizard with GitHub Classroom URL prompt

        $ classroom-pilot assignments setup --url "https://classroom.github.com/classrooms/123/assignments/hw1"
        # Auto-extract from URL with minimal prompts

        $ classroom-pilot assignments setup --verbose --dry-run
        # Shows what setup would do with detailed logging
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    if verbose:
        logger.debug("Verbose mode enabled for assignment setup")

    if dry_run:
        logger.info("DRY RUN: Would start assignment setup wizard")
        logger.info("DRY RUN: Would create assignment.conf file")
        if simplified or url:
            logger.info("DRY RUN: Would use simplified setup with GitHub API")
        return

    # Determine which setup flow to use
    if url or simplified:
        logger.info("Starting simplified assignment setup wizard")
        setup = AssignmentSetup()
        setup.run_simplified_wizard(classroom_url=url)
    else:
        logger.info("Starting standard assignment setup wizard")
        setup = AssignmentSetup()
        setup.run_wizard()


@assignments_app.command("validate-config")
def assignment_validate_config(
    config_file: str = typer.Option(
        "assignment.conf", "--config-file", "-c", help="Configuration file path to validate"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    )
):
    """
    Validate assignment configuration file.

    This command validates the structure and content of an assignment configuration 
    file, checking for required fields, valid URLs, proper formatting, and other
    configuration requirements.

    The validation includes:
    - Required field presence checks
    - GitHub URL format validation
    - Organization name validation  
    - Assignment name validation
    - File path validation

    Example:
        $ classroom-pilot assignments validate-config
        $ classroom-pilot assignments validate-config --config-file custom.conf
    """
    setup_logging(verbose=verbose)
    logger.info(f"Validating configuration file: {config_file}")

    try:
        from .config import ConfigLoader, ConfigValidator

        # Load configuration
        config_path = Path(config_file)
        if not config_path.exists():
            typer.echo(
                f"❌ Configuration file not found: {config_file}", err=True)
            raise typer.Exit(code=1)

        loader = ConfigLoader(config_path)
        config = loader.load()

        if verbose:
            typer.echo(f"📋 Loaded configuration from: {config_file}")
            typer.echo(f"📊 Configuration contains {len(config)} entries")

        # Validate configuration
        validator = ConfigValidator()
        is_valid, errors = validator.validate_full_config(config)

        if is_valid:
            typer.echo(f"✅ Configuration file is valid: {config_file}")
            if verbose:
                typer.echo("📝 Configuration details:")
                for key, value in config.items():
                    typer.echo(f"  {key}: {value}")
        else:
            typer.echo(
                f"❌ Configuration validation failed: {config_file}", err=True)
            typer.echo("📋 Validation errors:")
            for error in errors:
                typer.echo(f"  • {error}", err=True)
            raise typer.Exit(code=1)

    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        typer.echo(f"❌ Error validating configuration: {e}", err=True)
        raise typer.Exit(code=1)


@assignments_app.command("orchestrate")
def assignment_orchestrate(
    ctx: typer.Context,
    force_yes: bool = typer.Option(
        False, "--yes", "-y", help="Automatically confirm all prompts"),
    step: str = typer.Option(
        None, "--step", help="Execute only a specific step (sync, discover, secrets, assist, cycle)"),
    skip_steps: str = typer.Option(
        None, "--skip", help="Skip specific steps (comma-separated: sync,discover,secrets,assist,cycle)"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Execute complete assignment workflow with comprehensive orchestration.

    This command runs the full assignment management workflow including repository
    synchronization, student repository discovery, secrets deployment, and 
    assistance operations. It provides the primary automation interface for
    managing GitHub Classroom assignments end-to-end.

    The orchestration workflow includes:
    - Template repository synchronization to GitHub Classroom
    - Student repository discovery and validation
    - Secrets and token deployment to student repositories
    - Optional student assistance operations
    - Optional collaborator access cycling
    - Progress tracking and comprehensive error handling

    Args:
        force_yes (bool): Skip confirmation prompts and proceed automatically.
        step (str): Execute only the specified workflow step.
        skip_steps (str): Comma-separated list of steps to skip.
        config_file (str): Path to assignment configuration file.
                          Defaults to "assignment.conf" in current directory.

    Raises:
        typer.Exit: With code 1 if orchestration fails or encounters errors.

    Example:
        $ classroom-pilot assignments --dry-run --verbose orchestrate
        $ classroom-pilot assignments orchestrate --step discover
        $ classroom-pilot assignments orchestrate --skip sync,assist
        $ classroom-pilot assignments orchestrate --config my-assignment.conf
    """
    # Get universal options from context
    dry_run = ctx.obj.get('dry_run', False)
    verbose = ctx.obj.get('verbose', False)

    setup_logging(verbose)
    logger.info("Starting assignment orchestration")

    try:
        # Import the Python orchestrator
        from .assignments.orchestrator import AssignmentOrchestrator, WorkflowConfig, WorkflowStep

        # Initialize orchestrator with configuration
        config_path = Path(config_file) if config_file else None
        orchestrator = AssignmentOrchestrator(config_path)

        # Validate configuration
        if not orchestrator.validate_configuration():
            logger.error("Configuration validation failed")
            raise typer.Exit(code=1)

        # Show configuration summary
        orchestrator.show_configuration_summary()

        # Parse workflow configuration
        enabled_steps = set(WorkflowStep)
        skip_step_set = set()
        step_override = None

        # Handle step override
        if step:
            try:
                step_override = WorkflowStep(step.lower())
                logger.info(f"Executing single step: {step_override.value}")
            except ValueError:
                valid_steps = [s.value for s in WorkflowStep]
                logger.error(
                    f"Invalid step '{step}'. Valid steps: {', '.join(valid_steps)}")
                raise typer.Exit(code=1)

        # Handle skip steps
        if skip_steps:
            for skip_step in skip_steps.split(','):
                try:
                    skip_step_set.add(WorkflowStep(skip_step.strip().lower()))
                except ValueError:
                    valid_steps = [s.value for s in WorkflowStep]
                    logger.error(
                        f"Invalid skip step '{skip_step}'. Valid steps: {', '.join(valid_steps)}")
                    raise typer.Exit(code=1)

        # Create workflow configuration
        workflow_config = WorkflowConfig(
            enabled_steps=enabled_steps,
            dry_run=dry_run,
            verbose=verbose,
            force_yes=force_yes,
            step_override=step_override,
            skip_steps=skip_step_set
        )

        # Confirm execution (skip confirmation in dry-run mode)
        if not dry_run and not orchestrator.confirm_execution(workflow_config):
            logger.info("Orchestration cancelled by user")
            raise typer.Exit(code=0)

        # Execute workflow
        results = orchestrator.execute_workflow(workflow_config)

        # Generate and display report
        report = orchestrator.generate_workflow_report()

        # Check for failures
        failed_steps = [r for r in results if not r.success]
        if failed_steps:
            logger.error(
                f"Orchestration completed with {len(failed_steps)} failed steps")
            raise typer.Exit(code=1)

        logger.info("✅ Assignment orchestration completed successfully")

    except ImportError as e:
        logger.error(f"Failed to import orchestrator components: {e}")
        logger.error("Make sure all required dependencies are installed")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Assignment orchestration failed: {e}")
        raise typer.Exit(code=1)


@assignments_app.command("help-student")
def help_student(
    ctx: typer.Context,
    repo_url: str = typer.Argument(..., help="Student repository URL to help"),
    one_student: bool = typer.Option(
        False, "--one-student", help="Use template directly (bypass classroom repository)"),
    auto_confirm: bool = typer.Option(
        False, "--yes", "-y", help="Automatically confirm all prompts"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Help a specific student with repository updates.

    This command assists instructors in helping students who are having difficulty
    updating their repositories with template changes. It can clone the student's
    repository, apply updates, and handle merge conflicts automatically.

    The command supports two modes:
    - Default mode: Uses classroom repository for updates
    - One-student mode: Uses template repository directly (--one-student)

    Args:
        repo_url: URL of the student repository to help
        one_student: Use template repository directly instead of classroom
        auto_confirm: Skip confirmation prompts
        config_file: Path to configuration file

    Supports universal options: --verbose, --dry-run

    Example:
        $ classroom-pilot assignments help-student https://github.com/org/assignment-student123
        $ classroom-pilot assignments help-student --one-student https://github.com/org/assignment-student123
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    setup_logging(verbose)
    logger.info("Starting student assistance")

    try:
        from .assignments.student_helper import StudentUpdateHelper, OperationResult

        # Initialize helper
        config_path = Path(config_file) if config_file else None
        helper = StudentUpdateHelper(config_path, auto_confirm=auto_confirm)

        # Validate configuration
        if not helper.validate_configuration():
            logger.error("Configuration validation failed")
            raise typer.Exit(code=1)

        if dry_run:
            logger.info("DRY RUN: Would help student with repository updates")
            logger.info(f"Repository: {repo_url}")
            logger.info(
                f"Mode: {'Template direct' if one_student else 'Classroom'}")
            return

        # Help the student
        result = helper.help_single_student(
            repo_url, use_template_direct=one_student)

        # Display result
        if result.result == OperationResult.SUCCESS:
            logger.info(f"✅ Successfully helped student: {result.message}")
        elif result.result == OperationResult.UP_TO_DATE:
            logger.info(f"ℹ️ Student already up to date: {result.message}")
        else:
            logger.error(f"❌ Failed to help student: {result.message}")
            raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import student helper: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Student assistance failed: {e}")
        raise typer.Exit(code=1)


@assignments_app.command("help-students")
def help_students(
    repo_file: str = typer.Argument(...,
                                    help="File containing student repository URLs"),
    auto_confirm: bool = typer.Option(
        False, "--yes", "-y", help="Automatically confirm all prompts"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Help multiple students with repository updates (batch processing).

    This command processes a file containing student repository URLs and helps
    each student with updates. It provides a summary of successful updates,
    students who were already up to date, and any errors encountered.

    The repository file should contain one URL per line:
        https://github.com/org/assignment-student1
        https://github.com/org/assignment-student2
        # Comments are ignored
        https://github.com/org/assignment-student3

    Args:
        repo_file: Path to file containing student repository URLs
        auto_confirm: Skip all confirmation prompts
        verbose: Enable detailed logging
        config_file: Path to configuration file

    Example:
        $ classroom-pilot assignments help-students student-repos.txt
        $ classroom-pilot assignments help-students student-repos.txt --yes
    """
    setup_logging(verbose)
    logger.info("Starting batch student assistance")

    try:
        from .assignments.student_helper import StudentUpdateHelper

        # Initialize helper
        config_path = Path(config_file) if config_file else None
        helper = StudentUpdateHelper(config_path, auto_confirm=auto_confirm)

        # Validate configuration
        if not helper.validate_configuration():
            logger.error("Configuration validation failed")
            raise typer.Exit(code=1)

        # Process students
        repo_file_path = Path(repo_file)
        summary = helper.batch_help_students(repo_file_path)

        # Display summary
        helper.display_batch_summary(summary)

        if summary.errors > 0:
            logger.warning(f"Completed with {summary.errors} errors")
            raise typer.Exit(code=1)
        else:
            logger.info("✅ Batch student assistance completed successfully")

    except ImportError as e:
        logger.error(f"Failed to import student helper: {e}")
        raise typer.Exit(code=1)
    except FileNotFoundError as e:
        logger.error(f"Repository file not found: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Batch student assistance failed: {e}")
        raise typer.Exit(code=1)


@assignments_app.command("check-student")
def check_student(
    repo_url: str = typer.Argument(...,
                                   help="Student repository URL to check"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Check the status of a student repository.

    This command checks whether a student repository needs updates by comparing
    commits with the template and classroom repositories. It provides detailed
    status information including accessibility and update requirements.

    Args:
        repo_url: URL of the student repository to check
        verbose: Enable detailed logging
        config_file: Path to configuration file

    Example:
        $ classroom-pilot assignments check-student https://github.com/org/assignment-student123
    """
    setup_logging(verbose)
    logger.info("Checking student repository status")

    try:
        from .assignments.student_helper import StudentUpdateHelper

        # Initialize helper
        config_path = Path(config_file) if config_file else None
        helper = StudentUpdateHelper(config_path)

        # Validate configuration
        if not helper.validate_configuration():
            logger.error("Configuration validation failed")
            raise typer.Exit(code=1)

        # Check student status
        status = helper.check_student_status(repo_url)

        # Display status
        helper.display_student_status(status)

        # Exit with appropriate code
        if not status.accessible:
            raise typer.Exit(code=1)
        elif status.needs_update:
            logger.info("ℹ️ Student needs updates")
            raise typer.Exit(code=2)
        else:
            logger.info("✅ Student is up to date")

    except ImportError as e:
        logger.error(f"Failed to import student helper: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Student status check failed: {e}")
        raise typer.Exit(code=1)


@assignments_app.command("student-instructions")
def student_instructions(
    repo_url: str = typer.Argument(..., help="Student repository URL"),
    output_file: Optional[str] = typer.Option(
        None, "--output", "-o", help="Save instructions to file"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Generate update instructions for a student.

    This command generates detailed instructions that can be sent to a student
    to help them update their repository manually. The instructions include
    multiple methods and troubleshooting tips.

    Args:
        repo_url: URL of the student repository
        output_file: Optional file to save instructions to
        config_file: Path to configuration file

    Example:
        $ classroom-pilot assignments student-instructions https://github.com/org/assignment-student123
        $ classroom-pilot assignments student-instructions https://github.com/org/assignment-student123 -o instructions.txt
    """
    logger.info("Generating student instructions")

    try:
        from .assignments.student_helper import StudentUpdateHelper

        # Initialize helper
        config_path = Path(config_file) if config_file else None
        helper = StudentUpdateHelper(config_path)

        # Generate instructions
        instructions = helper.generate_student_instructions(repo_url)

        # Output instructions
        if output_file:
            with open(output_file, 'w') as f:
                f.write(instructions)
            logger.info(f"Instructions saved to: {output_file}")
        else:
            print(instructions)

    except ImportError as e:
        logger.error(f"Failed to import student helper: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Failed to generate instructions: {e}")
        raise typer.Exit(code=1)


@assignments_app.command("check-classroom")
def check_classroom(
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Check if the classroom repository is ready for student updates.

    This command verifies that the classroom repository is accessible and
    compares its state with the template repository to ensure it's ready
    for student assistance operations.

    Args:
        verbose: Enable detailed logging
        config_file: Path to configuration file

    Example:
        $ classroom-pilot assignments check-classroom
    """
    setup_logging(verbose)
    logger.info("Checking classroom repository status")

    try:
        from .assignments.student_helper import StudentUpdateHelper

        # Initialize helper
        config_path = Path(config_file) if config_file else None
        helper = StudentUpdateHelper(config_path)

        # Validate configuration
        if not helper.validate_configuration():
            logger.error("Configuration validation failed")
            raise typer.Exit(code=1)

        # Check classroom status
        is_ready = helper.check_classroom_ready()

        if is_ready:
            logger.info("✅ Classroom repository is ready")
        else:
            logger.error("❌ Classroom repository is not ready")
            raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import student helper: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Classroom status check failed: {e}")
        raise typer.Exit(code=1)


@assignments_app.command("manage")
def assignment_manage(ctx: typer.Context):
    """
    Provides a high-level interface for managing the assignment lifecycle.

    This function provides access to assignment management functionality with
    support for universal options. Assignment management commands will be
    implemented in future versions.

    Supports universal options: --verbose, --dry-run

    Example:
        $ classroom-pilot assignments manage
        $ classroom-pilot assignments manage --verbose --dry-run
    """
    # Access universal options from parent context
    verbose = ctx.parent.params.get('verbose', False)
    dry_run = ctx.parent.params.get('dry_run', False)

    if verbose:
        setup_logging(level="DEBUG")
        logger.debug("Verbose mode enabled for assignment management")
    else:
        setup_logging()

    if dry_run:
        logger.info("DRY RUN: Would start assignment management interface")
        typer.echo("🚧 DRY RUN: Assignment management commands coming soon!")
        return

    logger.info("Assignment management interface")
    # TODO: Implement assignment management
    typer.echo("🚧 Assignment management commands coming soon!")


@assignments_app.command("cycle-collaborator")
def cycle_single_collaborator(
    ctx: typer.Context,
    repo_url: str = typer.Argument(
        ..., help="Repository URL to cycle collaborator permissions for"),
    username: str = typer.Argument(...,
                                   help="Username to cycle permissions for"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force cycling even when access appears correct"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Cycle collaborator permissions for a single repository.

    This command fixes repository access issues by cycling collaborator permissions.
    It intelligently detects when cycling is needed and only performs the operation
    when necessary, unless force mode is enabled.

    Args:
        repo_url: URL of the repository to cycle permissions for
        username: Username to cycle permissions for
        force: Force cycling even when access appears correct
        config_file: Path to configuration file

    Supports universal options: --verbose, --dry-run

    Example:
        $ classroom-pilot assignments cycle-collaborator https://github.com/org/repo student123
        $ classroom-pilot assignments cycle-collaborator --force https://github.com/org/repo student123 --verbose --dry-run
    """
    # Access universal options from parent context
    verbose = ctx.parent.params.get('verbose', False)
    dry_run = ctx.parent.params.get('dry_run', False)

    if verbose:
        setup_logging(level="DEBUG")
        logger.debug(
            f"Verbose mode enabled for cycling collaborator {username} on {repo_url}")
    else:
        setup_logging()

    logger.info("Cycling single repository collaborator permissions")

    if dry_run:
        logger.info(
            f"DRY RUN: Would cycle collaborator {username} on {repo_url}")
        logger.info(f"DRY RUN: Force mode: {force}")
        logger.info(f"DRY RUN: Config file: {config_file}")
        return

    try:
        from .assignments.cycle_collaborator import CycleCollaboratorManager

        # Initialize manager
        config_path = Path(config_file) if config_file else None
        manager = CycleCollaboratorManager(config_path, auto_confirm=True)

        # Validate configuration
        if not manager.validate_configuration():
            logger.error("Configuration validation failed")
            raise typer.Exit(code=1)

        # Cycle permissions
        result = manager.cycle_single_repository(repo_url, username, force)

        # Display result
        manager.display_cycle_result(result)

        # Exit with appropriate code
        if result.result.value == "success":
            logger.info("✅ Collaborator cycling completed successfully")
        elif result.result.value == "skipped":
            logger.info("ℹ️ Collaborator cycling skipped - no action needed")
        else:
            logger.error("❌ Collaborator cycling failed")
            raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import cycle collaborator manager: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Collaborator cycling failed: {e}")
        raise typer.Exit(code=1)


@assignments_app.command("cycle-collaborators")
def cycle_multiple_collaborators(
    ctx: typer.Context,
    batch_file: str = typer.Argument(...,
                                     help="File containing repository URLs or usernames"),
    repo_url_mode: bool = typer.Option(
        False, "--repo-urls", help="Treat batch file as repository URLs (extract usernames)"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force cycling even when access appears correct"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Cycle collaborator permissions for multiple repositories (batch processing).

    This command processes a file containing either repository URLs or usernames
    and cycles collaborator permissions for each entry. It provides intelligent
    detection of access issues and only cycles when necessary.

    The batch file format depends on the mode:
    - Username mode (default): One username per line
    - Repository URL mode (--repo-urls): One repository URL per line

    Args:
        batch_file: Path to file containing repository URLs or usernames
        repo_url_mode: Treat file as repository URLs instead of usernames
        force: Force cycling even when access appears correct
        dry_run: Preview actions without making changes
        verbose: Enable detailed logging
        Supports universal options: --verbose, --dry-run

    Example:
        $ classroom-pilot assignments cycle-collaborators student-repos.txt --repo-urls
        $ classroom-pilot assignments cycle-collaborators usernames.txt --force
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    setup_logging(verbose)
    logger.info("Cycling multiple repository collaborator permissions")

    try:
        from .assignments.cycle_collaborator import CycleCollaboratorManager

        # Initialize manager
        config_path = Path(config_file) if config_file else None
        manager = CycleCollaboratorManager(config_path, auto_confirm=True)

        # Validate configuration
        if not manager.validate_configuration():
            logger.error("Configuration validation failed")
            raise typer.Exit(code=1)

        batch_file_path = Path(batch_file)
        if not batch_file_path.exists():
            logger.error(f"Batch file not found: {batch_file}")
            raise typer.Exit(code=1)

        if dry_run:
            logger.info(
                "DRY RUN: Would cycle collaborator permissions for batch")
            logger.info(f"Batch file: {batch_file}")
            logger.info(f"Repository URL mode: {repo_url_mode}")
            logger.info(f"Force mode: {force}")
            return

        # Process batch file
        summary = manager.batch_cycle_from_file(
            batch_file_path, repo_url_mode, force)

        # Display summary
        manager.display_batch_summary(summary)

        # Exit with appropriate code
        if summary.failed_operations > 0:
            logger.warning(
                f"Completed with {summary.failed_operations} failures")
            raise typer.Exit(code=1)
        else:
            logger.info("✅ Batch collaborator cycling completed successfully")

    except ImportError as e:
        logger.error(f"Failed to import cycle collaborator manager: {e}")
        raise typer.Exit(code=1)
    except FileNotFoundError as e:
        logger.error(f"Batch file not found: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Batch collaborator cycling failed: {e}")
        raise typer.Exit(code=1)


@assignments_app.command("check-repository-access")
def check_repository_access(
    repo_url: str = typer.Argument(...,
                                   help="Repository URL to check access for"),
    username: str = typer.Argument(..., help="Username to check access for"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Check repository access status for a specific user.

    This command checks whether a user has proper access to a repository,
    including collaborator status and pending invitations. It provides
    detailed status information to help diagnose access issues.

    Args:
        repo_url: URL of the repository to check
        username: Username to check access for
        verbose: Enable detailed logging
        config_file: Path to configuration file

    Example:
        $ classroom-pilot assignments check-repository-access https://github.com/org/repo student123
    """
    setup_logging(verbose)
    logger.info("Checking repository access status")

    try:
        from .assignments.cycle_collaborator import CycleCollaboratorManager

        # Initialize manager
        config_path = Path(config_file) if config_file else None
        manager = CycleCollaboratorManager(config_path)

        # Validate configuration
        if not manager.validate_configuration():
            logger.error("Configuration validation failed")
            raise typer.Exit(code=1)

        # Check repository status
        status = manager.check_repository_status(repo_url, username)

        # Display status
        manager.display_repository_status(status)

        # Exit with appropriate code based on status
        if not status.accessible:
            logger.error("❌ Repository is not accessible")
            raise typer.Exit(code=1)
        elif status.needs_cycling:
            logger.warning(
                "⚠️ Repository access issues detected - cycling recommended")
            raise typer.Exit(code=2)
        else:
            logger.info("✅ Repository access is working correctly")

    except ImportError as e:
        logger.error(f"Failed to import cycle collaborator manager: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Repository access check failed: {e}")
        raise typer.Exit(code=1)


@assignments_app.command("push-to-classroom")
def push_to_classroom(
    ctx: typer.Context,
    force: bool = typer.Option(
        False, "--force", "-f", help="Force push without confirmation"),
    interactive: bool = typer.Option(
        True, "--interactive/--non-interactive", help="Enable interactive mode for confirmations"),
    branch: str = typer.Option(
        "main", "--branch", "-b", help="Branch to push to classroom repository"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Push template repository changes to the classroom repository.

    This command synchronizes your local template repository with the
    GitHub Classroom repository, ensuring students receive the latest
    assignment updates and fixes.

    The command performs:
    - Repository validation and status checks
    - Git remote configuration for classroom repository
    - Change analysis and conflict detection
    - Interactive confirmation (unless --force is used)
    - Push execution with appropriate force handling
    - Verification of successful synchronization

    Examples:
        # Interactive push with confirmation
        classroom-pilot assignments push-to-classroom

        # Force push without confirmation
        classroom-pilot assignments push-to-classroom --force

        # Push specific branch
        classroom-pilot assignments push-to-classroom --branch develop

        # Non-interactive mode for automation
        classroom-pilot assignments push-to-classroom --non-interactive --force
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    try:
        from .assignments.push_manager import ClassroomPushManager, PushResult

        # Set up logging
        setup_logging(verbose)
        logger.info("🚀 Starting classroom repository push workflow")

        if dry_run:
            logger.info("🔍 DRY RUN MODE - No changes will be made")

        # Initialize manager
        config_path = Path(config_file) if config_file else None
        manager = ClassroomPushManager(assignment_root=Path.cwd())
        manager.branch = branch

        if dry_run:
            # In dry run mode, only show what would be done
            logger.info("📋 Push workflow steps that would be executed:")
            logger.info("  1. Validate repository structure and configuration")
            logger.info("  2. Check for uncommitted changes")
            logger.info("  3. Setup classroom remote repository")
            logger.info("  4. Fetch latest classroom repository state")
            logger.info("  5. Analyze changes between local and classroom")
            logger.info("  6. Display changes summary and get confirmation")
            logger.info("  7. Push changes to classroom repository")
            logger.info("  8. Verify push completed successfully")
            logger.info("  9. Provide next steps guidance")
            logger.info(
                "✅ Dry run completed - use without --dry-run to execute")
            return

        # Execute the push workflow
        result, message = manager.execute_push_workflow(
            force=(force and not interactive),
            interactive=interactive
        )

        # Handle results
        if result == PushResult.SUCCESS:
            logger.info(f"✅ {message}")
        elif result == PushResult.UP_TO_DATE:
            logger.info(f"ℹ️ {message}")
        elif result == PushResult.CANCELLED:
            logger.info(f"❌ {message}")
        elif result == PushResult.PERMISSION_ERROR:
            logger.error(f"🔒 {message}")
            logger.error("Check your GitHub permissions and authentication")
            raise typer.Exit(code=1)
        elif result == PushResult.NETWORK_ERROR:
            logger.error(f"🌐 {message}")
            logger.error("Check your network connection and try again")
            raise typer.Exit(code=1)
        elif result == PushResult.REPOSITORY_ERROR:
            logger.error(f"📁 {message}")
            logger.error("Fix repository issues and try again")
            raise typer.Exit(code=1)
        else:
            logger.error(f"❌ Push failed: {message}")
            raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import push manager: {e}")
        raise typer.Exit(code=1)
    except KeyboardInterrupt:
        logger.info("❌ Push cancelled by user")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Push workflow failed: {e}")
        if verbose:
            import traceback
            logger.error(traceback.format_exc())
        raise typer.Exit(code=1)


# Repository Commands
@repos_app.command("fetch")
def repos_fetch(
    ctx: typer.Context,
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Discover and fetch student repositories from GitHub Classroom.

    This command loads the assignment configuration, then uses a Bash wrapper to fetch
    student repositories as specified in the configuration file. It supports dry-run and
    verbose modes for safer and more informative execution.

    Args:
        config_file (str): Path to the configuration file (default: "assignment.conf").

    Supports universal options: --verbose, --dry-run

    Raises:
        typer.Exit: If the repository fetch operation fails.

    Example:
        $ classroom-pilot repos fetch
        $ classroom-pilot repos fetch --config custom.conf --verbose --dry-run
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    if verbose:
        logger.debug(
            f"Verbose mode enabled for repo fetch with config: {config_file}")

    logger.info("Fetching student repositories")

    if dry_run:
        logger.info(
            f"DRY RUN: Would fetch student repositories using config: {config_file}")
        return

    # Use Python implementation
    try:
        from .repos.fetch import RepositoryFetcher

        config_path = Path(config_file) if config_file else None
        fetcher = RepositoryFetcher(config_path)

        success = fetcher.fetch_all_repositories(verbose=verbose)
        if not success:
            logger.error("Repository fetch failed")
            raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import repos fetcher: {e}")
        raise typer.Exit(code=1)


@repos_app.command("update")
def repos_update(
    ctx: typer.Context,
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Update assignment configuration and student repositories.

    This function updates the assignment configuration and all associated student repositories.
    It supports a dry-run mode to preview actions without making changes, and a verbose mode for detailed output.
    The configuration file path can be specified.

    Args:
        config_file (str): Path to the configuration file.

    Supports universal options: --verbose, --dry-run

    Raises:
        typer.Exit: If the repository update fails.

    Example:
        $ classroom-pilot repos update
        $ classroom-pilot repos update --config custom.conf --verbose --dry-run
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    if verbose:
        logger.debug(
            f"Verbose mode enabled for repo update with config: {config_file}")

    logger.info("Updating repositories")

    if dry_run:
        logger.info(
            f"DRY RUN: Would update repositories using config: {config_file}")
        return
        return

    # Use Python implementation
    try:
        from .assignments.student_helper import StudentUpdateHelper

        config_path = Path(config_file) if config_file else None
        helper = StudentUpdateHelper(config_path)

        success, message = helper.execute_update_workflow(
            auto_confirm=True, verbose=verbose)
        if not success:
            logger.error(f"Repository update failed: {message}")
            raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import student update helper: {e}")
        raise typer.Exit(code=1)


@repos_app.command("push")
def repos_push(
    ctx: typer.Context,
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Syncs the template repository to the GitHub Classroom repository.

    This command pushes the current state of the template repository to the configured
    GitHub Classroom repository, using the provided configuration file. It supports dry-run
    mode to preview actions without executing them, and verbose mode for detailed output.

    Args:
        config_file (str): Path to the configuration file (default: "assignment.conf").

    Supports universal options: --verbose, --dry-run

    Raises:
        typer.Exit: If the repository push fails, exits with a non-zero status code.

    Example:
        $ classroom-pilot repos push
        $ classroom-pilot repos push --config custom.conf --verbose --dry-run
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    if verbose:
        logger.debug(
            f"Verbose mode enabled for repo push with config: {config_file}")

    logger.info("Pushing to classroom repository")

    if dry_run:
        logger.info(
            f"DRY RUN: Would push to classroom repository using config: {config_file}")
        return

    # Use Python implementation
    try:
        from .assignments.push_manager import ClassroomPushManager, PushResult

        manager = ClassroomPushManager(assignment_root=Path.cwd())

        result, message = manager.execute_push_workflow(
            force=False, interactive=False)

        if result == PushResult.SUCCESS:
            logger.info(f"✅ {message}")
        elif result == PushResult.UP_TO_DATE:
            logger.info(f"ℹ️ {message}")
        else:
            logger.error(f"Repository push failed: {message}")
            raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import push manager: {e}")
        raise typer.Exit(code=1)


@repos_app.command("cycle-collaborator")
def repos_cycle_collaborator(
    ctx: typer.Context,
    assignment_prefix: str = typer.Option(
        None, "--assignment-prefix", help="Assignment prefix"),
    username: str = typer.Option(None, "--username", help="Username"),
    organization: str = typer.Option(
        None, "--organization", help="Organization"),
    list_collaborators: bool = typer.Option(
        False, "--list", help="List collaborators"),
    force: bool = typer.Option(False, "--force", help="Force cycling"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Cycle repository collaborator permissions for assignments.

    This command manages collaborator permissions on repositories matching a given assignment prefix,
    optionally for a specific user and organization. It can list current collaborators, force cycling
    of permissions, and supports dry-run and verbose modes.

    Args:
        assignment_prefix (str, optional): Prefix for assignment repositories to target.
        username (str, optional): Username of the collaborator to cycle.
        organization (str, optional): Name of the GitHub organization.
        list_collaborators (bool, optional): If True, list current collaborators instead of cycling.
        force (bool, optional): If True, force cycling of collaborator permissions.
        config_file (str, optional): Path to the configuration file (default: "assignment.conf").

    Supports universal options: --verbose, --dry-run

    Raises:
        typer.Exit: Exits with code 1 if cycling collaborator permissions fails.

    Example:
        $ classroom-pilot repos cycle-collaborator --assignment-prefix hw1 --username student123 --organization myorg
        $ classroom-pilot repos cycle-collaborator --list --verbose --dry-run
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    if verbose:
        logger.debug(
            f"Verbose mode enabled for cycling collaborator permissions")

    logger.info("Cycling collaborator permissions")

    if dry_run:
        logger.info("DRY RUN: Would cycle collaborator permissions")
        if assignment_prefix and username and organization:
            repo_url = f"https://github.com/{organization}/{assignment_prefix}-{username}"
            logger.info(f"DRY RUN: Would target repository: {repo_url}")
        logger.info(f"DRY RUN: List mode: {list_collaborators}")
        logger.info(f"DRY RUN: Force mode: {force}")
        return

    # Use Python implementation
    try:
        from .assignments.cycle_collaborator import CycleCollaboratorManager

        config_path = Path(config_file) if config_file else None
        manager = CycleCollaboratorManager(config_path)

        # Build repository URL from parameters if provided
        repo_url = None
        if assignment_prefix and username and organization:
            repo_url = f"https://github.com/{organization}/{assignment_prefix}-{username}"

        if list_collaborators:
            # List mode
            if repo_url:
                collaborators = manager.list_repository_collaborators(repo_url)
                for collab in collaborators:
                    logger.info(f"  {collab['login']}: {collab['permission']}")
            else:
                logger.error(
                    "Repository URL required for listing collaborators")
                raise typer.Exit(code=1)
        else:
            # Cycle mode
            if repo_url:
                success, message = manager.cycle_single_repository(
                    repo_url, force=force)
                if not success:
                    logger.error(f"Collaborator cycling failed: {message}")
                    raise typer.Exit(code=1)
            else:
                logger.error(
                    "Repository URL required for cycling collaborators")
                raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import cycle collaborator manager: {e}")
        raise typer.Exit(code=1)


# Secret Commands
@secrets_app.command("add")
def secrets_add(
    ctx: typer.Context,
    assignment_root: str = typer.Option(
        None, "--assignment-root", "-r", help="Path to assignment template repository root directory"),
    repo_urls: str = typer.Option(
        None, "--repos", help="Comma-separated list of repository URLs to process")
):
    """
    Add or update secrets in student repositories using global configuration.

    This function manages the process of adding or updating secrets in student repositories
    based on the global configuration loaded from assignment.conf. It supports dry-run and
    verbose modes for testing and debugging purposes.

    The command uses the globally loaded configuration, which contains all necessary
    settings including SECRETS_CONFIG, GITHUB_ORGANIZATION, and INSTRUCTOR_TOKEN_FILE.

    Args:
        assignment_root (str, optional): Path to assignment template repository root. 
                                       If not provided, uses current directory.
        repo_urls (str, optional): Comma-separated list of repository URLs. If not provided,
                                  auto-discovery will be attempted (when implemented).

    Supports universal options: --verbose, --dry-run

    Raises:
        typer.Exit: Exits with code 1 if secret management fails.

    Example:
        $ classroom-pilot secrets add
        $ classroom-pilot secrets add --repos "url1,url2" --verbose --dry-run
    """
    from .secrets.github_secrets import GitHubSecretsManager

    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    if verbose:
        logger.debug("Verbose mode enabled for secrets add")

    logger.info(
        "Adding secrets to student repositories using global configuration")

    if dry_run:
        logger.info("DRY RUN: Would add secrets to student repositories")
        if repo_urls:
            target_repos = [url.strip()
                            for url in repo_urls.split(',') if url.strip()]
            logger.info(
                f"DRY RUN: Would process {len(target_repos)} specified repositories")
        if assignment_root:
            logger.info(
                f"DRY RUN: Would use assignment root: {assignment_root}")
        return

    # Check if global configuration is loaded
    global_config = get_global_config()
    if not global_config:
        logger.error("Global configuration not loaded")
        logger.error(
            "Please ensure you're running from a directory with assignment.conf")
        logger.error(
            "Or use --assignment-root to specify the assignment directory")
        raise typer.Exit(code=1)

    # Validate secrets configuration
    if not global_config.secrets_config:
        logger.error("No secrets configuration found in assignment.conf")
        logger.error(
            "Please configure SECRETS_CONFIG in your assignment.conf file")
        raise typer.Exit(code=1)

    # Parse repository URLs if provided
    target_repos = None
    if repo_urls:
        target_repos = [url.strip()
                        for url in repo_urls.split(',') if url.strip()]
        logger.info(f"Processing {len(target_repos)} specified repositories")

    # Create secrets manager with global configuration
    try:
        secrets_manager = GitHubSecretsManager(dry_run=dry_run)

        # Add secrets using global configuration
        success = secrets_manager.add_secrets_from_global_config(
            repo_urls=target_repos)

        if not success:
            logger.error("Secret management failed")
            raise typer.Exit(code=1)

        logger.info("✅ Secret management completed successfully")

    except Exception as e:
        logger.error(f"Failed to initialize secrets manager: {e}")
        raise typer.Exit(code=1)


@secrets_app.command("manage")
def secrets_manage(ctx: typer.Context):
    """
    Provides an interface for advanced secret and token management.

    This function provides access to advanced secret management functionality with
    support for universal options. Advanced secret management commands will be
    implemented in future versions.

    Supports universal options: --verbose, --dry-run

    Example:
        $ classroom-pilot secrets manage
        $ classroom-pilot secrets manage --verbose --dry-run
    """
    # Access universal options from parent context
    verbose = ctx.parent.params.get('verbose', False)
    dry_run = ctx.parent.params.get('dry_run', False)

    if verbose:
        setup_logging(level="DEBUG")
        logger.debug("Verbose mode enabled for secrets management")
    else:
        setup_logging()

    if dry_run:
        logger.info("DRY RUN: Would start secret management interface")
        typer.echo("🚧 DRY RUN: Advanced secret management commands coming soon!")
        return

    logger.info("Secret management interface")
    # TODO: Implement secret management
    typer.echo("🚧 Advanced secret management commands coming soon!")


# Automation Commands
@automation_app.command("cron-install")
def automation_cron_install(
    ctx: typer.Context,
    steps: List[str] = typer.Argument(
        ..., help="Workflow steps to schedule (sync, secrets, cycle, discover, assist)"),
    schedule: Optional[str] = typer.Option(
        None, "--schedule", "-s", help="Cron schedule (e.g., '0 */4 * * *'). Uses default if not provided"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Install cron job for automated workflow steps.

    Install cron jobs to automate GitHub Classroom workflow operations like
    template synchronization, secret management, and repository access cycling.

    Supports universal options: --verbose, --dry-run

    Examples:
        classroom-pilot automation cron-install sync
        classroom-pilot automation cron-install secrets --schedule "0 2 * * *" --verbose
        classroom-pilot automation cron-install sync secrets cycle --dry-run
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    if verbose:
        logger.debug(f"Verbose mode enabled for cron installation: {steps}")

    if dry_run:
        logger.info(
            f"DRY RUN: Would install cron job for steps: {', '.join(steps)}")
        if schedule:
            logger.info(f"DRY RUN: Schedule: {schedule}")
        logger.info(f"DRY RUN: Config file: {config_file}")
        return

    try:
        from .automation import CronManager

        # Load configuration
        cron_manager = CronManager()

        logger.info(f"Installing cron job for steps: {', '.join(steps)}")

        result, message = cron_manager.install_cron_job(steps, schedule)

        if result.value == "success":
            typer.echo(f"✅ {message}", color=typer.colors.GREEN)
        elif result.value == "already_exists":
            typer.echo(f"⚠️  {message}", color=typer.colors.YELLOW)
        else:
            typer.echo(f"❌ {message}", color=typer.colors.RED)
            raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Cron job installation failed: {e}")
        raise typer.Exit(code=1)


@automation_app.command("cron-remove")
def automation_cron_remove(
    ctx: typer.Context,
    steps: Optional[List[str]] = typer.Argument(
        None, help="Workflow steps to remove (sync, secrets, cycle, discover, assist) or 'all'"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Remove cron jobs for automated workflow steps.

    Remove specific cron jobs or all assignment-related cron jobs from
    the user's crontab.

    Examples:
        classroom-pilot automation cron-remove sync
        classroom-pilot automation cron-remove all
        classroom-pilot automation cron-remove secrets cycle
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    setup_logging(verbose)

    try:
        from .automation import CronManager

        # Load configuration
        cron_manager = CronManager()

        # Default to removing all if no steps specified
        if not steps:
            steps = "all"
        elif len(steps) == 1 and steps[0] == "all":
            steps = "all"

        if dry_run:
            if steps == "all":
                typer.echo("[DRY RUN] Would remove all assignment cron jobs")
            else:
                typer.echo(
                    f"[DRY RUN] Would remove cron job for steps: {', '.join(steps)}")
            return

        logger.info(
            f"Removing cron job for steps: {steps if isinstance(steps, str) else ', '.join(steps)}")

        result, message = cron_manager.remove_cron_job(steps)

        if result.value == "success":
            typer.echo(f"✅ {message}", color=typer.colors.GREEN)
        elif result.value == "not_found":
            typer.echo(f"⚠️  {message}", color=typer.colors.YELLOW)
        else:
            typer.echo(f"❌ {message}", color=typer.colors.RED)
            raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Cron job removal failed: {e}")
        raise typer.Exit(code=1)


@automation_app.command("cron-status")
def automation_cron_status(
    ctx: typer.Context,
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Show status of installed cron jobs.

    Display information about currently installed assignment-related cron jobs,
    including schedules, commands, and recent log activity.

    Supports universal options: --verbose, --dry-run

    Example:
        classroom-pilot automation cron-status
        classroom-pilot automation --verbose --dry-run cron-status
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    if verbose:
        logger.debug("Verbose mode enabled for cron status check")

    logger.info("Checking cron job status...")

    if dry_run:
        logger.info("DRY RUN: Would check cron job status")
        logger.info(f"DRY RUN: Config file: {config_file}")
        return

    try:
        from .automation import CronManager

        # Load configuration
        cron_manager = CronManager()
        status = cron_manager.get_cron_status()

        if not status.has_jobs:
            typer.echo("⚠️  No assignment cron jobs are installed",
                       color=typer.colors.YELLOW)
            typer.echo("\nTo install a cron job, run:")
            typer.echo("  classroom-pilot automation cron-install [steps]")
        else:
            typer.echo(
                f"✅ Assignment cron jobs are installed: {status.total_jobs} job(s)", color=typer.colors.GREEN)
            typer.echo()

            for job in status.installed_jobs:
                typer.echo(
                    f"📅 Steps: {', '.join(job.steps) if hasattr(job, 'steps') else job.steps_key}")
                typer.echo(f"   Schedule: {job.schedule}")
                if hasattr(job, 'command'):
                    typer.echo(f"   Command: {job.command}")
                typer.echo()

            if status.log_file_exists and status.last_log_activity:
                typer.echo("📋 Recent log activity:")
                # Show last few lines, truncated if too long
                log_lines = status.last_log_activity.splitlines()
                for line in log_lines[-3:]:  # Show last 3 lines
                    typer.echo(f"   {line}")
            elif status.log_file_exists:
                typer.echo("📋 Log file exists but no recent activity")
            else:
                typer.echo(
                    "⚠️  No log file found - cron jobs may not have run yet")

    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Failed to get cron job status: {e}")
        raise typer.Exit(code=1)


@automation_app.command("cron-logs")
def automation_cron_logs(
    lines: int = typer.Option(
        30, "--lines", "-n", help="Number of recent log lines to show"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Show recent workflow log entries.

    Display recent log entries from automated workflow executions to help
    with debugging and monitoring cron job activity.

    Example:
        classroom-pilot automation cron-logs --lines 50
    """
    setup_logging(verbose)

    try:
        from .automation import CronManager

        # Load configuration
        cron_manager = CronManager()

        logger.info(f"Showing recent workflow logs ({lines} lines)...")

        success, output = cron_manager.show_logs(lines)

        if success:
            typer.echo(output)
        else:
            # Check if it's a "file not found" case (normal condition)
            if "Log file not found" in output or "not found" in output.lower():
                typer.echo("📋 No logs available yet",
                           color=typer.colors.YELLOW)
                typer.echo(
                    "\nCron jobs may not have run yet, or logging may not be configured.")
                typer.echo(
                    "Once cron jobs start running, their output will appear here.")
            else:
                # Other errors should still be reported
                typer.echo(f"❌ {output}", color=typer.colors.RED)
                raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Failed to show logs: {e}")
        raise typer.Exit(code=1)


@automation_app.command("cron-schedules")
def automation_cron_schedules():
    """
    List default schedules for workflow steps.

    Show the default cron schedules used for different workflow steps
    and provide examples of cron schedule formats.

    Example:
        classroom-pilot automation cron-schedules
    """
    try:
        from .automation import CronManager

        cron_manager = CronManager()
        output = cron_manager.list_default_schedules()
        typer.echo(output)

    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Failed to list schedules: {e}")
        raise typer.Exit(code=1)


@automation_app.command("cron-sync")
def automation_cron_sync(
    ctx: typer.Context,
    steps: List[str] = typer.Argument(
        None, help="Workflow steps to execute (sync, discover, secrets, assist, cycle)"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path"),
    stop_on_failure: bool = typer.Option(
        False, "--stop-on-failure", help="Stop execution on first step failure"),
    show_log: bool = typer.Option(
        False, "--show-log", help="Show log tail after execution")
):
    """
    Execute automated workflow cron job with specified steps.

    This command runs workflow steps designed for scheduled execution,
    providing comprehensive logging and error handling suitable for
    cron job automation.

    The command performs:
    - Environment validation and step verification
    - Sequential execution of specified workflow steps
    - Comprehensive logging with automatic log rotation
    - Error handling and result reporting
    - Optional log display for immediate feedback

    Available workflow steps:
    - sync: Synchronize template with classroom repository
    - discover: Discover and update student repositories
    - secrets: Manage repository secrets
    - assist: Provide automated student assistance
    - cycle: Cycle collaborator permissions

    Examples:
        # Execute sync step only (default)
        classroom-pilot automation cron-sync

        # Execute multiple steps
        classroom-pilot automation cron-sync sync secrets cycle

        # Dry run to see what would be executed
        classroom-pilot automation cron-sync --dry-run sync secrets

        # Stop on first failure and show logs
        classroom-pilot automation cron-sync --stop-on-failure --show-log sync secrets

        # Verbose execution for debugging
        classroom-pilot automation cron-sync --verbose sync
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    try:
        from .automation.cron_sync import CronSyncManager, CronSyncResult

        # Set up logging
        setup_logging(verbose)
        logger.info("🔄 Starting automated workflow cron job")

        if dry_run:
            logger.info("🔍 DRY RUN MODE - No workflow steps will be executed")

        # Initialize manager
        manager = CronSyncManager(assignment_root=Path.cwd())

        # Default to sync if no steps provided
        if not steps:
            steps = ["sync"]

        if dry_run:
            # Show what would be executed
            logger.info("📋 Workflow steps that would be executed:")
            for i, step in enumerate(steps, 1):
                logger.info(f"  {i}. {step}")
            logger.info(f"📂 Log file: {manager.log_file}")
            logger.info(
                "✅ Dry run completed - use without --dry-run to execute")
            return

        # Execute cron sync workflow
        result = manager.execute_cron_sync(
            steps=steps,
            verbose=verbose,
            stop_on_failure=stop_on_failure
        )

        # Report results
        if result.overall_result == CronSyncResult.SUCCESS:
            logger.info(
                f"✅ All workflow steps completed successfully in {result.total_execution_time:.2f}s")
        elif result.overall_result == CronSyncResult.PARTIAL_FAILURE:
            logger.warning(
                f"⚠️ Some workflow steps failed: {result.error_summary}")
            logger.info(f"📂 Check log file: {result.log_file_path}")
        elif result.overall_result == CronSyncResult.COMPLETE_FAILURE:
            logger.error(
                f"❌ All workflow steps failed: {result.error_summary}")
            logger.error(f"📂 Check log file: {result.log_file_path}")
        elif result.overall_result == CronSyncResult.ENVIRONMENT_ERROR:
            logger.error(f"🏗️ Environment error: {result.error_summary}")
        elif result.overall_result == CronSyncResult.CONFIGURATION_ERROR:
            logger.error(f"⚙️ Configuration error: {result.error_summary}")

        # Show execution summary
        if result.steps_executed:
            logger.info("📊 Step execution summary:")
            for step_result in result.steps_executed:
                status = "✅" if step_result.success else "❌"
                logger.info(
                    f"  {status} {step_result.step.value}: {step_result.message}")

        # Show log tail if requested
        if show_log:
            logger.info("📋 Recent log entries:")
            log_lines = manager.get_log_tail(20)
            for line in log_lines[-10:]:  # Show last 10 lines
                logger.info(f"  {line}")

        # Set exit code based on result
        if result.overall_result in [CronSyncResult.COMPLETE_FAILURE,
                                     CronSyncResult.ENVIRONMENT_ERROR,
                                     CronSyncResult.CONFIGURATION_ERROR]:
            raise typer.Exit(code=1)
        elif result.overall_result == CronSyncResult.PARTIAL_FAILURE:
            raise typer.Exit(code=2)  # Partial failure exit code

    except ImportError as e:
        logger.error(f"Failed to import cron sync manager: {e}")
        raise typer.Exit(code=1)
    except KeyboardInterrupt:
        logger.info("❌ Cron sync cancelled by user")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Cron sync workflow failed: {e}")
        if verbose:
            import traceback
            logger.error(traceback.format_exc())
        raise typer.Exit(code=1)


@automation_app.command("cron")
def automation_cron(
    ctx: typer.Context,
    action: str = typer.Option(
        "status", "--action", "-a", help="Action to perform (status, install, remove)"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Manage cron automation jobs via CLI (legacy command).

    This is a legacy command that provides basic cron job management.
    Use the specific cron-* commands for better functionality:
    - cron-install: Install cron jobs
    - cron-remove: Remove cron jobs  
    - cron-status: Show status
    - cron-logs: Show logs

    Args:
        action (str): Action to perform on cron jobs. Options are "status", "install", or "remove".
        dry_run (bool): If True, shows what would be done without executing any changes.
        verbose (bool): If True, enables verbose logging output.
        config_file (str): Path to the configuration file to use.
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    setup_logging(verbose)

    typer.echo("⚠️  This is a legacy command. Consider using specific commands:",
               color=typer.colors.YELLOW)
    typer.echo("   classroom-pilot automation cron-install [steps]")
    typer.echo("   classroom-pilot automation cron-remove [steps]")
    typer.echo("   classroom-pilot automation cron-status")
    typer.echo("   classroom-pilot automation cron-logs")
    typer.echo()

    # For now, delegate to Python cron manager implementation
    logger.info(f"Managing cron jobs: {action}")

    try:
        from .automation.cron_manager import CronManager

        manager = CronManager()

        if dry_run:
            logger.info(f"DRY RUN: Would execute cron {action}")
            return

        if action == "status":
            status = manager.get_cron_status()
            # Format the status for display
            output = f"Cron Jobs Installed: {status.total_jobs}\n"
            if status.has_jobs:
                output += f"Jobs: {[job.steps_key for job in status.installed_jobs]}\n"
            output += f"Log File Exists: {status.log_file_exists}\n"
            if status.last_log_activity:
                output += f"Last Activity: {status.last_log_activity[:100]}...\n"
            typer.echo(output)
        elif action == "install":
            success, message = manager.install_cron_job(
                ["sync"], "0 */4 * * *")
            if not success:
                logger.error(f"Cron installation failed: {message}")
                raise typer.Exit(code=1)
        elif action == "remove":
            success, message = manager.remove_cron_job("sync")
            if not success:
                logger.error(f"Cron removal failed: {message}")
                raise typer.Exit(code=1)
        else:
            logger.error(f"Unknown cron action: {action}")
            raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import cron manager: {e}")
        raise typer.Exit(code=1)


@automation_app.command("sync")
def automation_sync(
    ctx: typer.Context,
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """
    Execute scheduled synchronization tasks using configuration from a file.

    This function sets up logging based on the verbosity flag, loads the configuration
    from the specified file, and invokes a Bash wrapper to perform the scheduled sync.
    It supports a dry-run mode to preview actions without executing them.

    Args:
        config_file (str): Path to the configuration file.

    Supports universal options: --verbose, --dry-run

    Raises:
        typer.Exit: Exits with code 1 if the scheduled sync fails.

    Example:
        $ classroom-pilot automation sync
        $ classroom-pilot automation --dry-run --verbose sync
    """
    # Access universal options from context
    verbose = ctx.obj.get('verbose', False)
    dry_run = ctx.obj.get('dry_run', False)

    if verbose:
        logger.debug("Verbose mode enabled for scheduled sync")

    logger.info("Running scheduled sync")

    if dry_run:
        logger.info("DRY RUN: Would run scheduled sync")
        logger.info(f"DRY RUN: Config file: {config_file}")
        return

    # Use Python implementation
    try:
        from .automation.cron_sync import CronSyncManager, CronSyncResult

        manager = CronSyncManager(assignment_root=Path.cwd())

        result = manager.execute_cron_sync(["sync"], verbose=verbose)

        if result.overall_result == CronSyncResult.SUCCESS:
            logger.info("✅ Scheduled sync completed successfully")
        else:
            logger.error(f"Scheduled sync failed: {result.error_summary}")
            raise typer.Exit(code=1)

    except ImportError as e:
        logger.error(f"Failed to import cron sync manager: {e}")
        raise typer.Exit(code=1)


@automation_app.command("batch")
def automation_batch():
    """
    Run batch processing operations for the CLI.

    This function sets up logging and provides a placeholder for future batch processing commands.
    Currently, it notifies the user that batch processing commands are coming soon.

    Returns:
        None
    """
    setup_logging()
    logger.info("Batch processing interface")

    # TODO: Implement batch processing
    typer.echo("🚧 Batch processing commands coming soon!")


def main():
    """Main entry point for the CLI application."""
    app()


if __name__ == "__main__":
    main()

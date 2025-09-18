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
    """
    Launch interactive wizard to configure a new assignment.

    This command initializes an interactive setup wizard that guides users through
    the complete process of configuring a new GitHub Classroom assignment. The wizard
    collects all required configuration parameters and generates the assignment.conf
    file needed for subsequent operations.

    The setup process includes:
    - Assignment metadata configuration (name, description, organization)
    - GitHub repository settings and template configuration  
    - Student repository discovery parameters
    - Secrets and token management setup
    - Automation and workflow preferences

    Raises:
        SystemExit: If setup process is interrupted or fails.

    Example:
        $ classroom-pilot assignments setup
        # Interactive wizard begins
    """
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
    - Repository access verification and assistance operations
    - Progress tracking and comprehensive error handling

    Args:
        dry_run (bool): Preview operations without executing changes.
                       Useful for validating configuration and workflow steps.
        verbose (bool): Enable detailed logging and progress information.
                       Provides comprehensive feedback during execution.
        config_file (str): Path to assignment configuration file.
                          Defaults to "assignment.conf" in current directory.

    Raises:
        typer.Exit: With code 1 if orchestration fails or encounters errors.

    Example:
        $ classroom-pilot assignments orchestrate --dry-run --verbose
        $ classroom-pilot assignments orchestrate --config my-assignment.conf
    """
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
    """
    Provides a high-level interface for managing the assignment lifecycle.

    This function sets up logging and displays a placeholder message indicating
    that assignment management commands will be implemented in the future.
    """
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
    """
    Discover and fetch student repositories from GitHub Classroom.

    This command loads the assignment configuration, then uses a Bash wrapper to fetch
    student repositories as specified in the configuration file. It supports dry-run and
    verbose modes for safer and more informative execution.

    Args:
        dry_run (bool): If True, show what would be done without executing any actions.
        verbose (bool): If True, enable verbose output for debugging and detailed logs.
        config_file (str): Path to the configuration file (default: "assignment.conf").

    Raises:
        typer.Exit: If the repository fetch operation fails.
    """
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
    """
    Update assignment configuration and student repositories.

    This function updates the assignment configuration and all associated student repositories.
    It supports a dry-run mode to preview actions without making changes, and a verbose mode for detailed output.
    The configuration file path can be specified.

    Args:
        dry_run (bool): If True, show what would be done without executing.
        verbose (bool): If True, enable verbose output.
        config_file (str): Path to the configuration file.

    Raises:
        typer.Exit: If the repository update fails.
    """
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
    """
    Syncs the template repository to the GitHub Classroom repository.

    This command pushes the current state of the template repository to the configured
    GitHub Classroom repository, using the provided configuration file. It supports dry-run
    mode to preview actions without executing them, and verbose mode for detailed output.

    Args:
        dry_run (bool): If True, shows what would be done without executing any actions.
        verbose (bool): If True, enables verbose logging output.
        config_file (str): Path to the configuration file (default: "assignment.conf").

    Raises:
        typer.Exit: If the repository push fails, exits with a non-zero status code.
    """
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
        dry_run (bool, optional): If True, show actions without executing them.
        verbose (bool, optional): If True, enable verbose logging output.
        config_file (str, optional): Path to the configuration file (default: "assignment.conf").

    Raises:
        typer.Exit: Exits with code 1 if cycling collaborator permissions fails.
    """
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
    """
    Add or update secrets in student repositories.

    This function manages the process of adding or updating secrets in student repositories
    based on the provided configuration file. It supports dry-run and verbose modes for
    testing and debugging purposes.

    Args:
        dry_run (bool): If True, displays the actions that would be performed without executing them.
        verbose (bool): If True, enables verbose logging output.
        config_file (str): Path to the configuration file specifying repository and secret details.

    Raises:
        typer.Exit: Exits with code 1 if secret management fails.
    """
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
    """
    Provides an interface for advanced secret and token management.

    This function sets up logging and displays a placeholder message indicating that
    advanced secret management commands will be implemented in the future.
    """
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
    """
    Manage cron automation jobs via CLI.

    This function provides a command-line interface for managing cron jobs related to automation tasks.
    It supports actions such as checking the status, installing, or removing cron jobs, with options for dry-run
    and verbose output. The function loads configuration from a specified file and delegates the actual cron
    management to a Bash wrapper.

    Args:
        action (str): Action to perform on cron jobs. Options are "status", "install", or "remove".
        dry_run (bool): If True, shows what would be done without executing any changes.
        verbose (bool): If True, enables verbose logging output.
        config_file (str): Path to the configuration file to use.

    Raises:
        typer.Exit: Exits with code 1 if cron management fails.
    """
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
    """
    Execute scheduled synchronization tasks using configuration from a file.

    This function sets up logging based on the verbosity flag, loads the configuration
    from the specified file, and invokes a Bash wrapper to perform the scheduled sync.
    It supports a dry-run mode to preview actions without executing them.

    Args:
        dry_run (bool): If True, show what would be done without executing.
        verbose (bool): If True, enable verbose output.
        config_file (str): Path to the configuration file.

    Raises:
        typer.Exit: Exits with code 1 if the scheduled sync fails.
    """
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


# Utility commands
@app.command("version")
def version():
    """
    Display the current version and basic information about Classroom Pilot.

    This function prints the version number, a brief description, and the project's GitHub URL to the console.
    """
    typer.echo("Classroom Pilot v3.1.0a1")
    typer.echo("Modular Python CLI for GitHub Classroom automation")
    typer.echo("https://github.com/hugo-valle/classroom-pilot")


# ================================
# LEGACY COMMANDS (DEPRECATED)
# ================================
# These commands are provided for backwards compatibility only.
# Use the new modular commands instead: assignments, repos, secrets, automation

@app.command("setup", deprecated=True)
def legacy_setup():
    """🔄 [LEGACY] Setup assignment configuration → Use: classroom-pilot assignments setup"""
    typer.echo("⚠️  LEGACY COMMAND: This command is deprecated.")
    typer.echo("🔄 Redirecting to: classroom-pilot assignments setup")
    typer.echo("💡 Use 'classroom-pilot assignments setup' instead")
    typer.echo("")
    assignment_setup()


@app.command("run", deprecated=True)
def legacy_run(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"),
    config_file: str = typer.Option(
        "assignment.conf", "--config", "-c", help="Configuration file path")
):
    """🔄 [LEGACY] Run classroom workflow → Use: classroom-pilot assignments orchestrate"""
    typer.echo("⚠️  LEGACY COMMAND: This command is deprecated.")
    typer.echo("🔄 Redirecting to: classroom-pilot assignments orchestrate")
    typer.echo("💡 Use 'classroom-pilot assignments orchestrate' instead")
    typer.echo("")
    assignment_orchestrate(
        dry_run=dry_run, verbose=verbose, config_file=config_file)


def main():
    """Main entry point for the CLI application."""
    app()


if __name__ == "__main__":
    main()

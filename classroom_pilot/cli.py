"""
CLI interface for Classroom Pilot using Typer framework.

This module provides the main command-line interface that mirrors the bash script 
functionality from assignment-orchestrator.sh with commands for run, sync, discover, 
secrets, and assist operations.
"""

from pathlib import Path
from typing import Annotated, Optional

import typer

from .config import Configuration
from .bash_wrapper import BashWrapper
from .utils import setup_logging, logger

# Create the main Typer application
app = typer.Typer(
    name="classroom-pilot",
    help="Classroom Pilot - Comprehensive automation suite for managing assignments",
    add_completion=False,
    rich_markup_mode="rich",
)

# Global options
DryRunOption = Annotated[bool, typer.Option(
    "--dry-run", "-n", help="Show what would be done without executing")]
VerboseOption = Annotated[bool, typer.Option(
    "--verbose", "-v", help="Enable verbose output")]
ConfigOption = Annotated[Optional[Path], typer.Option(
    "--config-file", "-c", help="Path to configuration file")]
YesOption = Annotated[bool, typer.Option(
    "--yes", "-y", help="Automatically answer yes to prompts")]


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    dry_run: DryRunOption = False,
    verbose: VerboseOption = False,
    config_file: ConfigOption = None,
    yes: YesOption = False,
) -> None:
    """
    Global callback to set up logging and store global options.

    This callback runs before any command. Configuration loading is deferred
    to individual commands to avoid loading config for --help and version.
    """
    # Always set up logging
    setup_logging(verbose)

    # Store global options in context for commands to use
    ctx.obj = {
        'dry_run': dry_run,
        'verbose': verbose,
        'config_file': config_file,
        'yes': yes
    }

    # Handle case where no subcommand is invoked (e.g., just --help)
    if ctx.invoked_subcommand is None:
        # Don't load config during resilient parsing (--help) or when no command specified
        return


def _load_config_and_wrapper(ctx: typer.Context) -> BashWrapper:
    """
    Helper function to load configuration and create BashWrapper.

    This is called by individual commands that need configuration.
    """
    # Skip if we're in resilient parsing mode (e.g., during --help)
    if ctx.resilient_parsing:
        return None

    # Get global options from context
    options = ctx.obj

    try:
        # Load configuration
        config = Configuration.load(options['config_file'])

        # Create bash wrapper with global options
        wrapper = BashWrapper(
            config,
            dry_run=options['dry_run'],
            verbose=options['verbose'],
            auto_yes=options['yes']
        )

        return wrapper

    except Exception as e:
        logger.error(f"❌ Error loading configuration: {e}")
        raise typer.Exit(code=1)


@app.command()
def run(ctx: typer.Context) -> None:
    """
    Run the complete classroom workflow (sync, discover, secrets, assist).

    This command executes the full assignment orchestration workflow:
    1. Sync templates to classroom
    2. Discover student repositories  
    3. Update secrets in student repos
    4. Assist students with common issues
    """
    # Load configuration and create wrapper
    wrapper = _load_config_and_wrapper(ctx)

    try:
        logger.info("🚀 Starting complete classroom workflow")

        # Execute the full workflow using assignment-orchestrator.sh
        success = wrapper.assignment_orchestrator(workflow_type="run")

        if success:
            logger.info("✅ Classroom workflow completed successfully")
            raise typer.Exit(code=0)
        else:
            logger.error("❌ Classroom workflow failed")
            raise typer.Exit(code=1)

    except typer.Exit:
        raise  # Re-raise typer.Exit without catching it
    except Exception as e:
        logger.error(f"❌ Error running workflow: {e}")
        raise typer.Exit(code=1)


@app.command()
def sync(ctx: typer.Context) -> None:
    """
    Sync template repository to GitHub Classroom.

    Pushes the current template repository content to the GitHub Classroom
    assignment repository, updating the assignment template.
    """
    # Load configuration and create wrapper
    wrapper = _load_config_and_wrapper(ctx)

    try:
        logger.info("🔄 Starting template sync to classroom")

        success = wrapper.push_to_classroom()

        if success:
            logger.info("✅ Template sync completed successfully")
            raise typer.Exit(code=0)
        else:
            logger.error("❌ Template sync failed")
            raise typer.Exit(code=1)

    except typer.Exit:
        raise  # Re-raise typer.Exit without catching it
    except Exception as e:
        logger.error(f"❌ Error syncing template: {e}")
        raise typer.Exit(code=1)


@app.command()
def discover(ctx: typer.Context) -> None:
    """
    Discover and fetch student repositories from GitHub Classroom.

    Fetches all student repositories for the assignment, filtering out
    instructor repositories and organizing them for batch operations.
    """
    # Load configuration and create wrapper
    wrapper = _load_config_and_wrapper(ctx)

    try:
        logger.info("🔍 Starting student repository discovery")

        success = wrapper.fetch_student_repos()

        if success:
            logger.info(
                "✅ Student repository discovery completed successfully")
            raise typer.Exit(code=0)
        else:
            logger.error("❌ Student repository discovery failed")
            raise typer.Exit(code=1)

    except typer.Exit:
        raise  # Re-raise typer.Exit without catching it
    except Exception as e:
        logger.error(f"❌ Error discovering repositories: {e}")
        raise typer.Exit(code=1)


@app.command()
def secrets(ctx: typer.Context) -> None:
    """
    Add or update secrets in student repositories.

    Adds the configured secrets to all discovered student repositories,
    enabling automated workflows and secure operations.
    """
    # Load configuration and create wrapper
    wrapper = _load_config_and_wrapper(ctx)

    try:
        logger.info("🔐 Starting secrets management")

        success = wrapper.add_secrets_to_students()

        if success:
            logger.info("✅ Secrets management completed successfully")
            raise typer.Exit(code=0)
        else:
            logger.error("❌ Secrets management failed")
            raise typer.Exit(code=1)

    except typer.Exit:
        raise  # Re-raise typer.Exit without catching it
    except Exception as e:
        logger.error(f"❌ Error managing secrets: {e}")
        raise typer.Exit(code=1)


@app.command()
def assist(ctx: typer.Context) -> None:
    """
    Assist students with common repository issues.

    Provides automated assistance for common student workflow issues,
    including repository setup, permissions, and configuration problems.
    """
    # Load configuration and create wrapper
    wrapper = _load_config_and_wrapper(ctx)

    try:
        logger.info("🆘 Starting student assistance")

        success = wrapper.student_update_helper()

        if success:
            logger.info("✅ Student assistance completed successfully")
            raise typer.Exit(code=0)
        else:
            logger.error("❌ Student assistance failed")
            raise typer.Exit(code=1)

    except typer.Exit:
        raise  # Re-raise typer.Exit without catching it
    except Exception as e:
        logger.error(f"❌ Error providing assistance: {e}")
        raise typer.Exit(code=1)


@app.command()
def setup(ctx: typer.Context) -> None:
    """
    Setup a new assignment configuration.

    Initialize assignment configuration files and prepare the environment
    for managing a GitHub Classroom assignment.
    """
    # Load configuration and create wrapper
    wrapper = _load_config_and_wrapper(ctx)

    try:
        logger.info("⚙️ Starting assignment setup")

        success = wrapper.setup_assignment()

        if success:
            logger.info("✅ Assignment setup completed successfully")
            raise typer.Exit(code=0)
        else:
            logger.error("❌ Assignment setup failed")
            raise typer.Exit(code=1)

    except typer.Exit:
        raise  # Re-raise typer.Exit without catching it
    except Exception as e:
        logger.error(f"❌ Error setting up assignment: {e}")
        raise typer.Exit(code=1)


@app.command()
def update(ctx: typer.Context) -> None:
    """
    Update assignment configuration and repositories.

    Update existing assignment configuration and synchronize changes
    across all related repositories and settings.
    """
    # Load configuration and create wrapper
    wrapper = _load_config_and_wrapper(ctx)

    try:
        logger.info("🔄 Starting assignment update")

        success = wrapper.update_assignment()

        if success:
            logger.info("✅ Assignment update completed successfully")
            raise typer.Exit(code=0)
        else:
            logger.error("❌ Assignment update failed")
            raise typer.Exit(code=1)

    except typer.Exit:
        raise  # Re-raise typer.Exit without catching it
    except Exception as e:
        logger.error(f"❌ Error updating assignment: {e}")
        raise typer.Exit(code=1)


@app.command()
def cron(
    ctx: typer.Context,
    action: Annotated[str, typer.Argument(
        help="Cron action: status, enable, disable, list, etc.")] = "status"
) -> None:
    """
    Manage cron automation jobs.

    Control automated scheduling for classroom operations including
    status checking, enabling/disabling jobs, and managing schedules.

    Examples:
        classroom-pilot cron status
        classroom-pilot cron enable
        classroom-pilot cron disable
    """
    # Load configuration and create wrapper
    wrapper = _load_config_and_wrapper(ctx)

    try:
        logger.info(f"⏰ Managing cron automation: {action}")

        success = wrapper.manage_cron(action)

        if success:
            logger.info("✅ Cron management completed successfully")
            raise typer.Exit(code=0)
        else:
            logger.error("❌ Cron management failed")
            raise typer.Exit(code=1)

    except typer.Exit:
        raise  # Re-raise typer.Exit without catching it
    except Exception as e:
        logger.error(f"❌ Error managing cron: {e}")
        raise typer.Exit(code=1)


@app.command()
def cron_sync(ctx: typer.Context) -> None:
    """
    Execute scheduled synchronization tasks.

    Run the automated synchronization workflow typically executed
    by cron jobs for keeping repositories and configurations in sync.
    """
    # Load configuration and create wrapper
    wrapper = _load_config_and_wrapper(ctx)

    try:
        logger.info("🔄 Starting cron synchronization")

        success = wrapper.cron_sync()

        if success:
            logger.info("✅ Cron synchronization completed successfully")
            raise typer.Exit(code=0)
        else:
            logger.error("❌ Cron synchronization failed")
            raise typer.Exit(code=1)

    except typer.Exit:
        raise  # Re-raise typer.Exit without catching it
    except Exception as e:
        logger.error(f"❌ Error running cron sync: {e}")
        raise typer.Exit(code=1)


@app.command()
def cycle(
    ctx: typer.Context,
    assignment_prefix: Annotated[Optional[str], typer.Argument(
        help="Assignment prefix for repository filtering")] = None,
    username: Annotated[Optional[str], typer.Argument(
        help="Single username for individual user mode")] = None,
    organization: Annotated[Optional[str], typer.Argument(
        help="GitHub organization name")] = None,
    batch_file: Annotated[Optional[Path], typer.Option(
        "--batch", "-b", help="Path to batch file containing multiple operations")] = None,
    config_file_cycle: Annotated[Optional[Path], typer.Option(
        "--config", help="Path to configuration file for cycle operations")] = None,
    list_mode: Annotated[bool, typer.Option(
        "--list", "-l", help="Only list current collaborators without making changes")] = False,
    force_cycle: Annotated[bool, typer.Option(
        "--force", "-f", help="Force permission cycling even if already at target level")] = False,
    repo_url_mode: Annotated[bool, typer.Option(
        "--repo-urls", "-r", help="Operate on repository URLs instead of assignment prefix")] = False,
) -> None:
    """
    Cycle repository collaborator permissions.

    Manage collaborator permissions on GitHub repositories, either for a single user
    or in batch mode. Supports listing current collaborators, forcing permission changes,
    and operating on repository URLs directly.

    Examples:
        classroom-pilot cycle --list lab01
        classroom-pilot cycle --force homework01 student123 cs101
        classroom-pilot cycle --batch operations.txt --repo-urls
    """
    # Load configuration and create wrapper
    wrapper = _load_config_and_wrapper(ctx)

    try:
        logger.info("🔄 Starting collaborator permission cycling")

        success = wrapper.cycle_collaborator(
            assignment_prefix=assignment_prefix,
            username=username,
            organization=organization,
            batch_file=str(batch_file) if batch_file else None,
            config_file=str(config_file_cycle) if config_file_cycle else None,
            list_mode=list_mode,
            force_cycle=force_cycle,
            repo_url_mode=repo_url_mode
        )

        if success:
            logger.info(
                "✅ Collaborator permission cycling completed successfully")
            raise typer.Exit(code=0)
        else:
            logger.error("❌ Collaborator permission cycling failed")
            raise typer.Exit(code=1)

    except typer.Exit:
        raise  # Re-raise typer.Exit without catching it
    except Exception as e:
        logger.error(f"❌ Error cycling collaborator permissions: {e}")
        raise typer.Exit(code=1)


@app.command()
def version() -> None:
    """Show version information."""
    from . import __version__
    typer.echo(f"GitHub Classroom Tools v{__version__}")


def main() -> None:
    """Main entry point for the CLI application."""
    app()


if __name__ == "__main__":
    main()

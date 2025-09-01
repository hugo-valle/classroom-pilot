"""
CLI interface for Classroom Pilot using Typer framework.

This module provides the main command-line interface that mirrors the bash script 
functionality from assignment-orchestrator.sh with commands for run, sync, discover, 
secrets, and assist operations.
"""

from pathlib import Path
from typing import Optional

import typer

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

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
def version() -> None:
    """Show version information."""
    from . import __version__
    typer.echo(f"GitHub Classroom Tools v{__version__}")


def main() -> None:
    """Main entry point for the CLI application."""
    app()


if __name__ == "__main__":
    main()

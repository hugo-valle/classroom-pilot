"""
Simple CLI interface for Classroom Pilot using basic Typer patterns.

This module provides a simplified command-line interface that avoids
complex type annotations that cause compatibility issues in CI environments.
"""

from pathlib import Path
import typer

from .config import Configuration
from .bash_wrapper import BashWrapper
from .utils import setup_logging, logger

# Create the main Typer application with no configuration at all
app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
)


@app.callback()
def main_callback(
    ctx: typer.Context,
    dry_run: bool = False,
    verbose: bool = False,
    config_file: str = None,
    yes: bool = False,
):
    """Classroom Pilot - Comprehensive automation suite for managing assignments."""
    # Store global options in context
    ctx.ensure_object(dict)
    ctx.obj['dry_run'] = dry_run
    ctx.obj['verbose'] = verbose
    ctx.obj['config_file'] = config_file
    ctx.obj['yes'] = yes

    # Setup logging based on verbose flag
    setup_logging(verbose)


@app.command()
def run(ctx: typer.Context):
    """Run the complete classroom workflow (sync, discover, secrets, assist)."""
    # Load configuration
    config = Configuration.load(ctx.obj.get('config_file'))

    wrapper = BashWrapper(
        config,
        dry_run=ctx.obj.get('dry_run', False),
        verbose=ctx.obj.get('verbose', False),
        auto_yes=ctx.obj.get('yes', False)
    )
    success = wrapper.assignment_orchestrator(workflow_type="run")

    if success:
        logger.info("✅ Workflow completed successfully")
    else:
        logger.error("❌ Workflow failed")
        raise typer.Exit(code=1)


@app.command()
def sync(ctx: typer.Context):
    """Sync template repository to GitHub Classroom."""
    # Load configuration
    config = Configuration.load(ctx.obj.get('config_file'))

    wrapper = BashWrapper(
        config,
        dry_run=ctx.obj.get('dry_run', False),
        verbose=ctx.obj.get('verbose', False),
        auto_yes=ctx.obj.get('yes', False)
    )
    success = wrapper.push_to_classroom()

    if success:
        logger.info("✅ Sync completed successfully")
    else:
        logger.error("❌ Sync failed")
        raise typer.Exit(code=1)


@app.command()
def discover(ctx: typer.Context):
    """Discover and fetch student repositories from GitHub Classroom."""
    # Load configuration
    config = Configuration.load(ctx.obj.get('config_file'))

    wrapper = BashWrapper(
        config,
        dry_run=ctx.obj.get('dry_run', False),
        verbose=ctx.obj.get('verbose', False),
        auto_yes=ctx.obj.get('yes', False)
    )
    success = wrapper.fetch_student_repos()

    if success:
        logger.info("✅ Discovery completed successfully")
    else:
        logger.error("❌ Discovery failed")
        raise typer.Exit(code=1)


@app.command()
def secrets(ctx: typer.Context):
    """Add or update secrets in student repositories."""
    # Load configuration
    config = Configuration.load(ctx.obj.get('config_file'))

    wrapper = BashWrapper(
        config,
        dry_run=ctx.obj.get('dry_run', False),
        verbose=ctx.obj.get('verbose', False),
        auto_yes=ctx.obj.get('yes', False)
    )
    success = wrapper.add_secrets_to_students()

    if success:
        logger.info("✅ Secrets management completed successfully")
    else:
        logger.error("❌ Secrets management failed")
        raise typer.Exit(code=1)


@app.command()
def assist(ctx: typer.Context):
    """Assist students with common repository issues."""
    # Load configuration
    config = Configuration.load(ctx.obj.get('config_file'))

    wrapper = BashWrapper(
        config,
        dry_run=ctx.obj.get('dry_run', False),
        verbose=ctx.obj.get('verbose', False),
        auto_yes=ctx.obj.get('yes', False)
    )
    success = wrapper.student_update_helper()

    if success:
        logger.info("✅ Student assistance completed successfully")
    else:
        logger.error("❌ Student assistance failed")
        raise typer.Exit(code=1)


@app.command()
def setup(ctx: typer.Context):
    """Setup a new assignment configuration."""
    # Load configuration
    config = Configuration.load(ctx.obj.get('config_file'))

    wrapper = BashWrapper(
        config,
        dry_run=ctx.obj.get('dry_run', False),
        verbose=ctx.obj.get('verbose', False),
        auto_yes=ctx.obj.get('yes', False)
    )
    success = wrapper.setup_assignment()

    if success:
        logger.info("✅ Setup completed successfully")
    else:
        logger.error("❌ Setup failed")
        raise typer.Exit(code=1)


@app.command()
def update(ctx: typer.Context):
    """Update assignment configuration and repositories."""
    # Load configuration
    config = Configuration.load(ctx.obj.get('config_file'))

    wrapper = BashWrapper(
        config,
        dry_run=ctx.obj.get('dry_run', False),
        verbose=ctx.obj.get('verbose', False),
        auto_yes=ctx.obj.get('yes', False)
    )
    success = wrapper.update_assignment()

    if success:
        logger.info("✅ Update completed successfully")
    else:
        logger.error("❌ Update failed")
        raise typer.Exit(code=1)


@app.command()
def cron(ctx: typer.Context):
    """Manage cron automation jobs."""
    import sys

    # Check if an action was provided as a trailing argument
    # This is a workaround to avoid typer.Argument() for CI compatibility
    action = "status"  # default
    if len(sys.argv) > 1:
        # Look for cron command and check if there's an argument after it
        try:
            cron_idx = sys.argv.index("cron")
            if cron_idx + 1 < len(sys.argv) and not sys.argv[cron_idx + 1].startswith("-"):
                action = sys.argv[cron_idx + 1]
        except (ValueError, IndexError):
            pass

    # Load configuration
    config = Configuration.load(ctx.obj.get('config_file'))

    wrapper = BashWrapper(
        config,
        dry_run=ctx.obj.get('dry_run', False),
        verbose=ctx.obj.get('verbose', False),
        auto_yes=ctx.obj.get('yes', False)
    )
    success = wrapper.manage_cron(action)

    if success:
        logger.info("✅ Cron management completed successfully")
    else:
        logger.error("❌ Cron management failed")
        raise typer.Exit(code=1)


@app.command(name="cron-sync")
def cron_sync(ctx: typer.Context):
    """Execute scheduled synchronization tasks."""
    # Load configuration
    config = Configuration.load(ctx.obj.get('config_file'))

    wrapper = BashWrapper(
        config,
        dry_run=ctx.obj.get('dry_run', False),
        verbose=ctx.obj.get('verbose', False),
        auto_yes=ctx.obj.get('yes', False)
    )
    success = wrapper.cron_sync()

    if success:
        logger.info("✅ Cron sync completed successfully")
    else:
        logger.error("❌ Cron sync failed")
        raise typer.Exit(code=1)


@app.command()
def cycle(
    ctx: typer.Context,
    assignment_prefix: str = None,
    username: str = None,
    organization: str = None,
    list: bool = False,
    force: bool = False,
    repo_urls: bool = False,
):
    """Cycle repository collaborator permissions."""
    # Load configuration
    config = Configuration.load(ctx.obj.get('config_file'))

    wrapper = BashWrapper(
        config,
        dry_run=ctx.obj.get('dry_run', False),
        verbose=ctx.obj.get('verbose', False),
        auto_yes=ctx.obj.get('yes', False)
    )
    success = wrapper.cycle_collaborator(
        assignment_prefix=assignment_prefix,
        username=username,
        organization=organization,
        list_mode=list,
        force_cycle=force,
        repo_url_mode=repo_urls
    )

    if success:
        logger.info("✅ Collaborator cycling completed successfully")
    else:
        logger.error("❌ Collaborator cycling failed")
        raise typer.Exit(code=1)


@app.command()
def version():
    """Show version information."""
    typer.echo("Classroom Pilot v1.0.0")
    typer.echo("Python CLI for GitHub Classroom automation")


if __name__ == "__main__":
    app()

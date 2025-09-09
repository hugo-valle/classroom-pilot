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
def main_callback():
    """Classroom Pilot - Comprehensive automation suite for managing assignments."""
    pass


@app.command()
def run():
    """Run the complete classroom workflow (sync, discover, secrets, assist)."""
    wrapper = BashWrapper()
    return wrapper.run_workflow()


@app.command()
def sync():
    """Sync template repository to GitHub Classroom."""
    wrapper = BashWrapper()
    return wrapper.sync_template()


@app.command()
def discover():
    """Discover and fetch student repositories from GitHub Classroom."""
    wrapper = BashWrapper()
    return wrapper.discover_repositories()


@app.command()
def secrets():
    """Add or update secrets in student repositories."""
    wrapper = BashWrapper()
    return wrapper.add_secrets()


@app.command()
def assist():
    """Assist students with common repository issues."""
    wrapper = BashWrapper()
    return wrapper.assist_students()


@app.command()
def version():
    """Show version information."""
    typer.echo("Classroom Pilot v1.0.0")
    typer.echo("Python CLI for GitHub Classroom automation")


if __name__ == "__main__":
    app()

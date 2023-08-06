"""This module provides the RP Tracker CLI."""
# rptodo/cli.py

from pathlib import Path
from typing import Optional

import typer

from trk import (__app_name__, __version__, ERRORS, config, database, controller, output)

app = typer.Typer()


"""
Every time the to-do application runs, it needs to access the Todoer class 
and connect the CLI with the database. To satisfy this requirement, you’ll 
implement a function called get_todoer()

"""

def get_tracker() -> controller.Tracker:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "trk init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return controller.Tracker(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "trk init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="to-do database location?",
    ),
) -> None:
    """Initialize the to-do database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def start(description: str = typer.Argument(...),   
    start_time: str =  typer.Option(None, "--manual", "-m", help = "Add a manual start time instead of current time."),
    project: str = typer.Option("", "--project", "-p", help = "Add a project tag"),
    task: str = typer.Option("", "--task", "-t", help = "Add a project tag"),
    client: str = typer.Option("","--client", "-c", help = "Add a client tag"),
    billable: str = typer.Option("n", "--bill", "-b", help = "Classify as billable"),    
    tags: str = typer.Option("", "--tags", "-l", help = "Add tags")) -> None:
    ''' Start recording a task'''

    tracker = get_tracker()
    
    str_time, error = tracker.start(description,start_time, project, task, client, billable, tags)

    if error is None:

        output.start_end_message("start", description, str_time, task, project, client, billable)

       

    else:
        message = typer.style(error, fg = typer.colors.BRIGHT_RED )
        typer.echo(message)


@app.command()
def stop(end_time: str =  typer.Option(None, "--manual", "-m", help = "Add a manual end time instead of current time.")):
    """End recording a task"""
    tracker = get_tracker()
    description, str_start, str_end, str_minutes,  task, project, client, billable,  error = tracker.stop(end_time)

    output.start_end_message("end", description, str_start, task, project, client, billable, str_end, str_minutes)
    
    
       
    



























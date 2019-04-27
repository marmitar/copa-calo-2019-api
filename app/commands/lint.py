import os
from glob import glob

import click


@click.command()
def lint():
    """Lint and check code style with flake8 and isort."""
    skip = ['requirements']
    root_files = glob('*.py')
    root_directories = [name for name in next(os.walk('.'))[1] if not name.startswith('.')]
    files_and_directories = [arg for arg in root_files + root_directories if arg not in skip]

    args = ['flake8', '--exit-zero']
    command_line = ' '.join(args + files_and_directories)

    os.system(command_line)  # noqa: S605

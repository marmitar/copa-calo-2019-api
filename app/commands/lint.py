import os
from glob import glob

import click


@click.command()
@click.option('-f', '--fix-imports', default=False, is_flag=True,
              help='Fix imports using isort, before linting')
def lint(fix_imports):
    """Lint and check code style with flake8 and isort."""
    skip = ['requirements']
    root_files = glob('*.py')
    root_directories = [name for name in next(os.walk('.'))[1] if not name.startswith('.')]
    files_and_directories = [arg for arg in root_files + root_directories if arg not in skip]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_args = list(args) + files_and_directories
        command_line = ' '.join(command_args)
        click.echo('{}: {}'.format(description, command_line))
        return_value = os.system(command_line)  # noqa: S605
        if return_value != 0:
            exit(return_value)

    execute_tool('Checking code style', 'flake8', '--exit-zero')

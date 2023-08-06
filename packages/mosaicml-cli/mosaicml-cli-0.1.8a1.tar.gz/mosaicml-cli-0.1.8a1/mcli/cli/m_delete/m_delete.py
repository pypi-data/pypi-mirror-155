""" m delete Entrypoint """
import argparse
import textwrap
from typing import List, Optional

from mcli.cli.m_delete.delete import delete_environment_variable, delete_platform, delete_run, delete_secret
from mcli.utils.utils_pod_state import PodState


def delete(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def add_common_args(parser: argparse.ArgumentParser):
    parser.add_argument('-y',
                        '--force',
                        dest='force',
                        action='store_true',
                        help='Skip confirmation dialog before deleting. Please be careful!')


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers()
    parser.set_defaults(func=delete, parser=parser)

    # TODO: Delete Projects

    platform_parser = subparsers.add_parser(
        'platform',
        aliases=['platforms'],
        help='Delete one or more platforms',
    )
    platform_parser.add_argument(
        'platform_names',
        nargs='*',
        metavar='PLATFORM',
        help='The name of the platform(s) to delete. Also supports glob-style pattern matching')
    platform_parser.add_argument('-a', '--all', dest='delete_all', action='store_true', help='Delete all platforms')
    platform_parser.set_defaults(func=delete_platform)
    add_common_args(platform_parser)

    environment_parser = subparsers.add_parser(
        'env',
        aliases=['envs'],
        help='Delete an Environment Variable',
    )
    environment_parser.add_argument(
        'variable_names',
        nargs='*',
        metavar='ENV',
        help='The name(s) of the environment variable(s) to delete. Also supports glob-style pattern matching')
    environment_parser.add_argument('-a',
                                    '--all',
                                    dest='delete_all',
                                    action='store_true',
                                    help='Delete all environment variables')
    environment_parser.set_defaults(func=delete_environment_variable)
    add_common_args(environment_parser)

    secrets_parser = subparsers.add_parser(
        'secret',
        aliases=['secrets'],
        help='Delete a Secret',
    )
    secrets_parser.add_argument(
        'secret_names',
        nargs='*',
        metavar='SECRET',
        help='The name(s) of the secret(s) to delete. Also supports glob-style pattern matching.')
    secrets_parser.add_argument('-a', '--all', dest='delete_all', action='store_true', help='Delete all secrets')
    secrets_parser.set_defaults(func=delete_secret)
    add_common_args(secrets_parser)

    # pylint: disable-next=invalid-name
    RUN_EXAMPLES = textwrap.dedent("""

    Examples:

    # Delete a specific run
    mcli delete run my-run-1

    # Delete all runs on platform rXzX
    mcli delete runs --platform rXzX

    # Delete all failed runs
    mcli delete runs --status failed

    # Delete all runs (Please be careful!)
    mcli delete runs --all

    """)
    run_parser = subparsers.add_parser(
        'run',
        aliases=['runs'],
        help='Delete a run or set of runs',
        description='Delete a run or set of runs that match some conditions',
        epilog=RUN_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    run_parser.add_argument('name_filter',
                            nargs='*',
                            metavar='RUN',
                            default=None,
                            help='The name(s) of the run(s) to delete')
    run_parser.add_argument('-p',
                            '--platform',
                            nargs='+',
                            dest='platform_filter',
                            metavar='PLATFORM',
                            default=None,
                            help='Delete runs on the specified platform(s). If no other arguments are provided, all '
                            'runs on the specified platform(s) will be deleted')

    def _to_status(text: str) -> str:
        return text.title().replace('_', '').lower()

    status_options = [_to_status(state.value) for state in PodState]
    run_parser.add_argument('-s',
                            '--status',
                            dest='status_filter',
                            nargs='+',
                            default=None,
                            metavar='STATUS',
                            choices=status_options,
                            type=_to_status,
                            help=f'Delete runs with the specified statuses (choices: {", ".join(status_options)})')
    run_parser.add_argument('-a', '--all', dest='delete_all', action='store_true', help='Delete all runs')
    run_parser.set_defaults(func=delete_run)
    add_common_args(run_parser)

    return parser


def add_delete_argparser(subparser: argparse._SubParsersAction,
                         parents: Optional[List[argparse.ArgumentParser]] = None) -> argparse.ArgumentParser:
    del parents
    delete_parser: argparse.ArgumentParser = subparser.add_parser(
        'delete',
        aliases=['del'],
        help='Configure your local project',
    )
    delete_parser = configure_argparser(parser=delete_parser)
    return delete_parser

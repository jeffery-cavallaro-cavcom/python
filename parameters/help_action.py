"""
Parameter Set Extended Help

This argparse action class extends the standard help information with a list
of recognized environment variables and configuration file parameters.
"""

from argparse import Action, ArgumentParser, SUPPRESS
import sys
from typing import Any, ClassVar, Iterable

from parameters.parameter import Parameter

class HelpAction(Action):
    """ Extended Help Action """
    HELP : ClassVar[str] = 'show this help message and exit'

    def __init__(
        self,
        option_strings : list[str],
        *_args : list[Any],
        const : Iterable[Parameter],
        **_kwargs : dict[str, Any]
    ):
        """
        Initialize the help action

        Arguments:
            option_strings:
                Option strings that will invoke this action.
            args:
                Positional arguments for the Action base class (unused).
                are ignored.
            const:
                List of parameters from which the environment variable and
                configuration file parameter information is gleaned.
            kwargs:
                Keyword arguments for Action base class (unused).
        """
        super().__init__(
            option_strings,
            SUPPRESS,
            const=const,
            nargs=0,
            default=SUPPRESS,
            help=self.HELP
        )

    def __call__(
        self,
        parser : ArgumentParser,
        *_args : list[Any],
        **_kwargs : dict[str, Any]
    ) -> None:
        """
        Display help information

        Arguments:
            parser:
                Parent parser instance.
            args:
                Other positional arguments (unused).
            kwargs:
                Other keyword arguments (unused).
        """
        env_help = []
        config_help = []

        parameters : Iterable[Parameter] = self.const

        for parameter in parameters:
            help_text = parameter.help_text or ''

            if parameter.env:
                env_name = parameter.env.get_name(
                    parameter.name, parameter.group
                )
                env_help.append(f"  {env_name:<21s} {help_text:<s}")

            if parameter.config:
                config_name = parameter.get_full_name()
                config_help.append(f"  {config_name:<21s} {help_text:<s}")

        parser.print_help()

        if env_help:
            print('\nenvironment variables:')
            print('\n'.join(env_help))

        if config_help:
            print('\nconfiguration parameters:')
            print('\n'.join(config_help))

        sys.exit(0)

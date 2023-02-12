"""
Application Parameter Set
"""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, SUPPRESS
from configparser import ConfigParser, ExtendedInterpolation
from typing import Any

from parameters.help_action import HelpAction
from parameters.parameter import Parameter

class ParameterSet:
    """ Application Parameter Set Definition """
    parameters : dict[str, Parameter]
    groups : dict[str, Any]
    arguments : ArgumentParser
    config : ConfigParser

    def __init__(
        self,
        **kwargs : dict[str, Any]
    ):
        """
        Create a new parameter set

        Arguments:
            kwargs:
                Keyword arguments for ArgumentParser().
        """
        self.parameters = {}
        self.groups = {}

        self.arguments = self.make_argument_parser(**kwargs)
        self.setup_help()

        self.config = self.make_config_parser()

    @staticmethod
    def make_argument_parser(
        **kwargs : dict[str, Any]
    ) -> ArgumentParser:
        """
        Construct the argument parser

        Arguments:
            kwargs:
                Keyword arguments for ArgumentParser().  The add_help argument
                is forced to False since an extended help action will be added.
                If a help formatter is not specified then the one that adds
                default information is specified.

        Returns:
            The constructed command line argument parser.
        """
        kwargs = kwargs.copy()
        kwargs['add_help'] = False

        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = ArgumentDefaultsHelpFormatter

        return ArgumentParser(**kwargs)


    def setup_help(self) -> None:
        """ Setup extended help """
        self.arguments.register('action', 'help', HelpAction)

        self.arguments.add_argument(
            '-h', '--help',
            action='help',
            const=self.parameters,
            dest=SUPPRESS,
            default=SUPPRESS
        )

    @staticmethod
    def make_config_parser() -> ConfigParser:
        """
        Construct the configuration file parser

        Returns:
            The constructed configuration file parser.  Extended interpolation
            is selected.  The name/value delimiter is set to '=' and the
            comment line character to '#'.  In line comments are allowed.
            Empty lines in values is disabled.
        """
        return ConfigParser(
            delimiters='=',
            comment_prefixes='#',
            inline_comment_prefixes='#',
            empty_lines_in_values=False,
            interpolation=ExtendedInterpolation
        )

if __name__ == '__main__':
    parms = ParameterSet(description='Test Parameters')
    parms.arguments.parse_args(args=['-h'])

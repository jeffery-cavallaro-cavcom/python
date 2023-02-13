"""
Application Parameter Set

A ParameterSet class instance manages all of the parameter values for an
application.  These values can originate from command line options and
arguments, environment variables, INI-style configuration file entries, and
compiled default values, in that order of precedence.  Once collected, the
final set of values is returned via a dictionary that is indexed by parameter
name.
"""

from argparse import ArgumentParser, Namespace, SUPPRESS
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
from sys import getdefaultencoding
from typing import Any, Iterable, Optional, Union

from parameters.help_action import HelpAction
from parameters.option import Option
from parameters.parameter import Parameter

from utility.expand_path import expand_path

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

    def add_help_group(
        self,
        name : str,
        **kwargs : dict[str, Any]
    ) -> None:
        """
        Add an argument help group

        Arguments:
            name:
                Name of the help group.  This name is referenced by the
                parameter argument definitions that wish to join the group.
                Group members are displayed together in the help usage
                information.
            kwargs:
                Keyword arguments for argparse.add_argument_group().
        """
        self.groups[name] = self.arguments.add_argument_group(**kwargs)

    def add_mutex_group(
        self,
        name : str,
        **kwargs : dict[str, Any]
    ) -> None:
        """
        Add an argument mutex group

        Arguments:
            name:
                Name of the mutex group.  This name is referenced by the
                parameter argument definitions that wish to join the group.
                Group members may not appear together on a command line.
            kwargs:
                Keyword arguments for argparse.add_mutually_exclusive_group().
        """
        self.groups[name] = self.arguments.add_mutually_exclusive_group(
            **kwargs
        )

    def add_parameters(
        self,
        parameters : Union[Parameter, Iterable[Parameter]]
    ):
        """
        Add parameters to the parameter set

        Arguments:
            parameters:
                One or more parameters to add to the parameter set.
        """
        if isinstance(parameters, Parameter):
            parameters = [parameters]

        for parameter in parameters or []:
            name = parameter.get_full_name()

            parent = None
            if isinstance(parameter.arg, Option):
                parent = parameter.arg.help_or_mutex
            parent = parent or self.arguments

            parameter.add_argument(parent)

            self.parameters[name] = parameter

    def collect_values(
        self,
        args : Optional[list[str]] = None,
        source : Optional[Union[Path, Parameter, str]] = None
    ) -> dict[str, Any]:
        """
        Parse and collect parameter values

        Arguments:
            args:
                Command line arguments.  Defaults to None (use sys.argv).
            source:
                Configuration source.  If a Path then the configuration
                information is read from the specified file.  If a Parameter
                then the target configuration file name is specified by another
                parameter value.  If a string then the contents are used as the
                configuration information.

        Returns:
            A dictionary of the found parameter values indexed by full
            parameter name
        """
        values = {}

        arguments = self.arguments.parse_args(args)
        self.read_source(source, arguments)

        for name, parameter in self.parameters.items():
            values[name] = parameter.get_value(arguments, self.config)

        return values

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

    def read_source(
        self,
        source : Union[Path, Parameter, str],
        arguments : Namespace
    ) -> None:
        """
        Read and parse configuration data from source

        Arguments:
            source:
                Configuration source (see above).
            arguments:
                Parsed command line argument values.  Used when the
                configuration file name is specified by another parameter.
        """
        if isinstance(source, Parameter):
            filename = source.get_value(arguments, self.config)
            if filename:
                self.read_source_file(filename)
        elif isinstance(source, Path):
            self.read_source_file(source)
        elif isinstance(source, str):
            self.config.read_string(source)

    def read_source_file(self, path : Path) -> None:
        """
        Read and parse a configuration file

        Arguments:
            path:
                Input file to read.
        """
        filename = expand_path(path)
        with open(filename, encoding=getdefaultencoding()) as source:
            self.config.read_file(source)

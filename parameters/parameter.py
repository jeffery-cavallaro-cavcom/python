"""
Application Parameters

Parameter values can come from the command line, environment variables,
INI-style configuration files, and compiled defaults, in that order of
precedence.  The Parameter class describes a single parameter and how to obtain
its value from these various sources.

Each parameter is assigned a base name and an optional group name.  These
parts are used to identify the parameter value in the various sources as
follows:

    [group_]name        The key for the final resolved value in the resulting
                        parameter values set.

    [--][group_]name    If there is a corresponding command line option, then
                        the long option name.  If there is a corresponding
                        command line positional argument, then the positionl
                        argument name.

    [GROUP_]NAME        If there is a corresponding environment variable then
                        the environment variable name.

    [group]             If there is a corresponding configuration option then
    name = value        the group name is the section name and the base name is
                        the option name.  If no group name is specified then
                        the current default section at the time the value is
                        fetched is assumed.
"""

from argparse import ArgumentParser, Namespace
from argparse import _ArgumentGroup, _MutuallyExclusiveGroup
from configparser import ConfigParser
from typing import Any, Callable, Optional, Union

from parameters.argument import Argument
from parameters.env_variable import EnvVariable

class Parameter:
    """ Application Parameter Definition """
    # pylint: disable=too-many-instance-attributes

    name : str
    group : str
    arg : Argument
    env : EnvVariable
    config : bool
    converter : Callable[[str], Any]
    default : Any
    help_text : str

    def __init__(
        # pylint: disable=too-many-arguments
        self,
        name : str,
        group : Optional[str] = None,
        arg : Optional[Argument] = None,
        env : Optional[EnvVariable] = None,
        config : Optional[Union[bool, 'Parameter']] = False,
        converter : Optional[Callable[[str], Any]] = None,
        default : Optional[Any] = None,
        help_text : Optional[str] = None
    ):
        """
        Define a parameter

        Arguments:
            name:
                The parameter base name.  This name may be prefixed with a
                group name (see below).
            group:
                The prefix that is prepended to the base name, separated by a
                single '_'.  If this parameter has a corresponding configuration
                option and the group value is None then the current default
                section at the time the value is fetched is assumed.
            arg:
                If specified then this parameter has a corresponding command
                line positional argument or option.
            env:
                If specified then this parameter has a corresponding
                environment variable.
            config:
                If truthy then this parameter has a corresponding configuration
                file value.  If a parameter is specified then that parameter's
                value serves as an alternate section name.  Defaults to False
                (no configuration file value).
            converter:
                Value converter.  Any found parameter string value will be
                passed to this method for type conversion.  In the case of
                command line values this is accomplished via the 'type' keyword
                argument.  Defaults to None (return the original string value).
            default:
                The compile-time default value.  The default value is the
                accepted value if no corresponding value is found in the other
                sources.  A default value in a present argument description
                overrides this value.  Defaults to None.
            help (str, optional):
                Help text for usage messages.  If None is specified then any
                command line argument help text is used.  If no argument help
                text is specified then this text is used.  Default information,
                if present, is appended to the message text.  Defaults to None
                (no help).
        """
        self.name = name
        self.group = group
        self.arg = arg
        self.env = env
        self.config = config if isinstance(config, Parameter) else bool(config)
        self.converter = converter

        if self.arg:
            arg_default = self.arg.kwargs.pop('default', None)
            arg_help = self.arg.kwargs.get('help', None)
        else:
            arg_default = None
            arg_help = None

        self.default = default if arg_default is None else arg_default

        help_text = arg_help or help_text
        if help_text and self.default is not None:
            help_text = f"{help_text} (def: {str(self.default)})"

        if self.arg:
            self.arg.kwargs['help'] = help_text
        self.help_text = help_text

    def get_full_name(self) -> str:
        """
        Construct parameter full name

        Returns:
            The parameter name possibly prefixed with the group name and a
            '_' separator.
        """
        parts = []

        if self.group:
            parts.append(self.group)
        parts.append(self.name)

        return '_'.join(parts)

    def add_argument(
        self,
        parent : Union[ArgumentParser, _ArgumentGroup, _MutuallyExclusiveGroup]
    ) -> None:
        """
        Add parameter argument to parent

        Arguments:
            parent:
                Argument parser, help group, or mutex group to which the
                command line argument is added.
        """
        if self.arg:
            self.arg.add_argument(
                self.name,
                self.group,
                parent,
                converter=self.converter
            )

    def get_value(
        self,
        values : Namespace,
        config : ConfigParser
    ) -> Any:
        """
        Get parameter value according to source precedence

        Arguments:
            parser:
                Parsed command line argument values.
            config:
                Parsed configuration file context.

        Returns:
            Value from the command line, an environment variable, a
            configuration file, or the compiled default, in that order of
            precendence.  Note that if there is not group then configuration
            values are taken from the current default section.
        """
        if self.arg:
            value = self.arg.get_value(self.name, self.group, values)
            if value is not None:
                return value

        if self.env:
            value = self.env.get_value(
                self.name, self.group, converter=self.converter
            )
            if value is not None:
                return value

        if self.config:
            if isinstance(self.config, Parameter):
                group = self.config.get_value(values, config)
            elif self.group:
                group = self.group
            else:
                group = config.default_section

            value = config.get(group, self.name, fallback=None)

            if value is not None and self.converter:
                value = self.converter(value)

            if value is not None:
                return value

        return self.default

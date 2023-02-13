"""
Command Line Option

An Option class instance is used to enable a parameter as a command line
option.  Option names can be long or short, each with an optional prefix.  The
long name defaults to the parameter name and the long name prefix defaults to
the parameter group name.

Arguments are defined using the same keyword argument values as those used by
ArgumentParser.add_argument().  The following keyword argument values have
special meaning if specified:

    dest        Values are normally fetched from the argument parser namespace
                using the (prefixed) long name; however, this can be overridden
                by specifying a 'dest' keyword argument.

    type        Argument values are normally converted using the parameter
                converter; however, this can be overridden by specifying a
                'type' keyword argument.

Note that if the 'default' keyword argument is specified then it essentially
overrides any parameter default value (since argument values have the highest
priority).
"""

from argparse import ArgumentParser, _ArgumentGroup, _MutuallyExclusiveGroup
from typing import Any, Callable, Optional, Union

from parameters.argument import Argument

class Option(Argument):
    """ Command Line Option """
    short_name : str
    short_prefix : str
    help_or_mutex : str
    kwargs : dict[str, Any]

    def __init__(
        self,
        short_name : Optional[str] = None,
        short_prefix : Optional[str] = None,
        help_or_mutex : Optional[str] = None,
        **kwargs : dict[str, Any]
    ):
        """
        Define a Command Line Option

        Arguments:
            short_name:
                Short option name.  Defaults to None (no short name).
            short_prefix:
                Short option name prefix.  This is useful when option sets are
                reused, possibly resulting in conflicting option names.
                Defaults to None (no short name prefix).
            help_or_mutex:
                Name of help or mutex group that is registered with the parent
                parameter set.
            kwargs:
                Keyword arguments for base classes.
        """
        super().__init__(**kwargs)
        self.short_name = short_name
        self.short_prefix = short_prefix
        self.help_or_mutex = help_or_mutex

    def add_argument(
        self,
        name : str,
        group : str,
        parent : Union[ArgumentParser, _ArgumentGroup, _MutuallyExclusiveGroup],
        converter : Optional[Callable[[str], Any]] = None
    ) -> None:
        """
        Add an argument

        Arguments:
            name:
                Parameter name.  This name is normally used as the long
                argument name.
            group:
                Group name.  This name is optionally prefixed to the long
                argument name (with a '_' separator) to obtain the full long
                name.  A None value disables the prefix.
            parent:
                Argument parser, help group, or mutex group to which the
                argument is added.
            converter:
                A method that converts the original argument string value to
                its desired type.  If the 'action' keyword argument is not
                specified or is 'store' and the 'type' keyword argument is not
                specified then this converter is used as the 'type' keyword
                argument value.  Defaults to None (return the original string
                value).
        """
        long_name = self.get_long_name(name, group)
        short_name = self.get_short_name()

        names = []
        if short_name:
            names.append('-' + short_name)
        names.append('--' + long_name)

        type_converter = self.kwargs.get('type', None)
        store_action = self.kwargs.get('action', None)
        if type_converter is None and store_action in [None, 'store']:
            self.kwargs['type'] = converter

        parent.add_argument(*names, **self.kwargs)

    def get_short_name(self) -> str:
        """
        Construct the short argument name

        Returns:
            Constructed short name with optional prefix.  None if there is no
            defined short name.
        """
        short_name = self.short_name
        short_prefix = self.short_prefix
        if short_name and short_prefix:
            short_name = short_prefix + short_name

        return short_name

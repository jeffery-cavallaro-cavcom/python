"""
Command Line Arguments

An Argument class instance is used to enable a parameter as a command line
argument.  The Argument class is used to define a positional argument value and
serves as the base class for the Option class, which is used to define an
option value.

Each argument is assigned a long name with an optional prefix.  The long name
defaults to the parameter name and the long name prefix defaults to the
parameter group name.

Arguments are defined using the same keyword argument values as those used by
ArgumentParser.add_argument().  The following keyword argument values have
special meaning if specified:

    type        Argument values are normally converted using the parameter
                converter; however, this can be overridden by specifying a
                'type' keyword argument.

Note that if the 'default' keyword argument is specified then it essentially
overrides any parameter default value (since argument values have the highest
priority).
"""

from argparse import ArgumentParser, Namespace
from typing import Any, Callable, Optional

class Argument:
    """ Command Line Option/Argument Definition """
    long_name : str
    use_prefix : bool
    kwargs : dict[str, Any]

    def __init__(
        self,
        long_name : Optional[str] = None,
        use_prefix : Optional[bool] = True,
        **kwargs : dict[str, Any]
    ):
        """
        Define a positional argument

        Arguments:
            long_name:
                Normally, the parameter name is used as the argument name.
                This argument provides an alternate name to use instead.  Note
                that this alternate name is still subject to a possible group
                name prefix (see below).  Defaults to None (use the parameter
                name),
            use_prefix:
                Specifies whether the argument name should be prefixed with
                the parameter group name.  Defaults to True (use the group
                name prefix).
            kwargs:
                Keyword arguments for ArgumentParser.add_argument().  A
                shallow copy is saved.
        """
        self.long_name = long_name or None
        self.use_prefix = bool(use_prefix)
        self.kwargs = kwargs.copy()

    def add_argument(
        self,
        name : str,
        group : str,
        parent : ArgumentParser,
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
                Argument parser to which the argument is added.
            converter:
                A method that converts the original argument string value to
                its desired type.  If the 'action' keyword argument is not
                specified or is 'store' and the 'type' keyword argument is not
                specified then this converter is used as the 'type' keyword
                argument value.  Defaults to None (return the original string
                value).
        """
        long_name = self.get_long_name(name, group)

        type_converter = self.kwargs.get('type', None)
        store_action = self.kwargs.get('action', None)
        if type_converter is None and store_action in [None, 'store']:
            self.kwargs['type'] = converter

        parent.add_argument(long_name, **self.kwargs)

    def get_long_name(self, name : str, group : str) -> str:
        """
        Construct the long argument name

        Arguments:
            name:
                Parameter name to use as the base long name.
            group:
                Parameter group to use as the long name prefix.  May be None
                to disable the prefix.

        Returns:
            Constructed long argument name.  The long name is normally the
            specified parameter name, but this can be overridden with the
            long_name value.  If a group name is specified and the use_prefix
            value is True then the long name is prefixed with the group name.
        """
        parts = []

        if self.use_prefix and group:
            parts.append(group)
        parts.append(self.long_name or name)

        return '_'.join(parts)

    def get_value(
        self,
        name : str,
        group : str,
        values : Namespace
    ) -> Any:
        """
        Get argument value

        Arguments:
            name:
                Parameter name.
            group:
                Group name.  May be None.
            values:
                Parsed argument values, accessed by constructed long name or
                'dest' argument override.

        Returns:
            Parsed (and possible converted) argument value from the specified
            argument parser namespace.
        """
        override_name = self.kwargs.get('dest', None)
        long_name = override_name or self.get_long_name(name, group)

        return getattr(values, long_name, None)

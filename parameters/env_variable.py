"""
Environment Variables

An EnvVariable class instance allows a parameter value to be supplied by an
environment variable.  The uppercase version of the parameter name is normally
used as the environment name.  This name can be prefixed with the parameter
group name (with a '_' separator).
"""

from os import environ
from typing import Any, Callable, Optional

class EnvVariable:
    """ Environment Variable Definition """
    name : str
    use_prefix : bool

    def __init__(
        self,
        name : Optional[str] = None,
        use_prefix : Optional[bool] = True
    ):
        """
        Define an environment variable

        Arguments;
            name:
                Normally, the uppercase version of the parameter name is used
                as the environment variable name.  This argument provides an
                optional name to use instead.  Note that this name is still
                subject to a possible group prefix (see below).  Defaults to
                None (use the parameter name).
            use_prefix:
                Specifies whether the environment variable name should be
                prefixed with the parameter group name.  Defaults to True (use
                the group prefix).
        """
        self.name = name
        self.use_prefix = bool(use_prefix)

    def get_name(
        self,
        name : str,
        group : str,
    ) -> str:
        """
        Construct the environment variable name

        Arguments:
            name:
                Parameter name to use as the base environment variable name.
            group:
                Parameter group to use as the environment variable name prefix.
                May be None to disable the prefix.

        Returns:
            Constructed environment variable name.  The name is normally the
            uppercase version of the specified parameter name, but this can be
            overridden with the name value.  If a group name is specified and
            the use_prefix value is True then the environment variable name is
            prefixed with the group name.
        """
        parts = []

        if self.use_prefix and group:
            parts.append(group)
        parts.append(self.name or name)

        return '_'.join(parts).upper()

    def get_value(
        self,
        name : str,
        group : str,
        converter : Optional[Callable[[str], Any]] = None
    ) -> Any:
        """
        Get environment variable value

        Arguments:
            name:
                Parameter name.
            group:
                Group name.  May be None.
            converter:
                Value converter.  Any found environment variable string value
                will be passed to this method.  Defaults to None (return the
                string value).

        Returns:
            Parsed (and possible converted) environment variable value.
        """
        env_name = self.get_name(name, group)
        value = environ.get(env_name, None)

        if value is not None and converter:
            value = converter(value)

        return value

"""
Convert Delimited String to List

This callable converts a string consisting of tokens separated by delimiters to
a corresponding list of tokens.  The default delimiter is a comma.  Leading and
trailing whitespace can be optionally stripped from each token.
"""

from typing import Any, Callable, Optional

class Str2List:
    """ Convert String to List """
    # pylint: disable=too-few-public-methods

    delimiter : str
    strip : bool
    allow_blank : bool
    converter : Callable[[str], Any]

    def __init__(
        self,
        delimiter : Optional[str] = None,
        strip : Optional[bool] = True,
        allow_blank: Optional[bool] = False,
        converter : Callable[[str], Any] = None
    ):
        """
        Initialize converter

        Arguments:
            delimiter:
                Token delimiter (for split()).  Defaults to None (comma).
            strip:
                If True then leading and trailing whitespace is stripped from
                each resulting token.
            allow_blank:
                If True then blank tokens between delimiters are preserved.
                This also causes a blank string to result in one blank token.
            converter:
                A converter that is applied to each token.  Defaults to None
                (return original string values).
        """
        self.delimiter = delimiter or ','
        self.strip = bool(strip)
        self.allow_blank = bool(allow_blank)
        self.converter = converter

    def __call__(self, value : str) -> list[Any]:
        """
        Parse delimited string

        Arguments:
            value:
                String to parse.  A value of None results in an empty token
                list.

        Returns:
            List of (converted) token values.  A None value always results in
            an empty list.
        """
        if value is None:
            return []

        parts = value.split(self.delimiter)

        if self.strip:
            parts = [part.strip() for part in parts]

        if not self.allow_blank:
            parts = [part for part in parts if part]

        if self.converter:
            parts = [self.converter(part) for part in parts]

        return parts

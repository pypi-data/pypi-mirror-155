import re
from typing import Pattern, Type, Union

from pydantic.errors import StrRegexError
from pydantic.main import BaseModel
from pydantic.types import StrBytes
from .errors import StrBytesError


class RegexBaseModel(BaseModel):
    __regex__: Union[Pattern, str]

    @classmethod
    def parse_regex(
        cls: Type["RegexBaseModel"],
        s: StrBytes,
        *,
        encoding: str = 'utf8',
    ) -> "RegexBaseModel":
        if isinstance(cls.__regex__, str):
            cls.__regex__ = re.compile(cls.__regex__)

        if isinstance(s, bytes):
            s = s.decode(encoding)
        elif not isinstance(s, str):
            raise StrBytesError()

        match = cls.__regex__.match(s)

        if match is None:
            raise StrRegexError(pattern=cls.__regex__.pattern)

        obj = match.groupdict()

        return cls.parse_obj(obj)

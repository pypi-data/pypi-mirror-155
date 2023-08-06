from pydantic.errors import PydanticTypeError


class StrBytesError(PydanticTypeError):
    msg_template = 'str or byte type expected'

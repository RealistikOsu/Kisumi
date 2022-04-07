from .parser import (
    Header,
    Body,
    RequestStruct,
)

class LoginRequestStruct(RequestStruct):
    """A structure holding unparsed login information."""

    body: Body(into_str= True)
    token: Header("osu-token")
    user_agent: Header("user-agent")

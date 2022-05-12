from pydantic import BaseModel

class LoginRequestModel(BaseModel):
    """A validated model for login data."""

    username: str
    password_md5: str
    osu_version: str
    utc_timezone: int
    display_city: bool
    allow_dms: bool
    osu_path_md5: str
    adapters: str
    adapters_md5: str
    uninstall_md5: str
    serial_md5: str

    @staticmethod
    def from_req_body(body: str) -> "LoginRequestModel":
        """Parses the login data from the login request body."""

        (
            username,
            password_md5,
            data,
            _,
        ) = body.split("\n")
        
        (
            osu_ver,
            timezone,
            display_city,
            client_hashes,
            allow_dms,
        ) = data.split("|")
        (
            osu_path_md5,
            adapters,
            adapter_md5,
            uninstall_md5,
            serial_md5,
            _,
        ) = client_hashes.split(":")

        return LoginRequestModel(
            username= username,
            password_md5= password_md5,
            osu_version= osu_ver,
            utc_timezone= timezone,
            display_city= display_city,
            allow_dms= allow_dms,
            osu_path_md5= osu_path_md5,
            adapters= adapters,
            adapters_md5= adapter_md5,
            uninstall_md5= uninstall_md5,
            serial_md5= serial_md5,
        )

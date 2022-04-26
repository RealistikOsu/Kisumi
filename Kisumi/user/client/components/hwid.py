from dataclasses import dataclass

@dataclass
class StableHWID:
    """A class containing the HWID information and hashes for an osu!stable client. This
    data is received upon login."""

    client_md5: str
    adapter: str
    adapter_md5: str
    uninstaller_md5: str
    serial_md5: str

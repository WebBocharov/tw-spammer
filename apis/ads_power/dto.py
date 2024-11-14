from dataclasses import dataclass


@dataclass
class BrowserProfileInfoDTO:
    name: str
    browser_id: str
    serial_number: str

    @property
    def info(self):
        return f"{self.serial_number}. {self.name} {self.browser_id}"


@dataclass
class BrowserProfileConnectionDTO:
    active: bool
    ws_connection: str
    msg: str = ""
    full_object: dict | str | bytes = None
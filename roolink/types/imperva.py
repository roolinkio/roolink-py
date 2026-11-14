from dataclasses import dataclass
from typing import Any


@dataclass
class ImpervaPayloadRequest:
    script: str
    # Absolute, or relative to page_url.
    script_url: str
    page_url: str
    # The User-Agent your requests to the site send, because the payload is
    # built from a collected browser with it.
    user_agent: str
    # The Accept-Language header your requests send, such as "en-US,en;q=0.9".
    language: str
    # The site's base64 GPC challenge without the JSON quotes it arrives in.
    # Leave it None when the site has none.
    pow: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "script": self.script,
            "scriptUrl": self.script_url,
            "pageUrl": self.page_url,
            "userAgent": self.user_agent,
            "language": self.language,
        }
        if self.pow:
            result["pow"] = self.pow
        return result


@dataclass
class ImpervaUTMVCRequest:
    script: str
    # The site's document.cookie, which the API requires even when it is empty.
    cookies: str
    user_agent: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "script": self.script,
            "cookies": self.cookies,
            "userAgent": self.user_agent,
        }


@dataclass
class ImpervaUTMVCResponse:
    """Holds the ___utmvc cookie that the API built.

    Only cookie or set_cookie is sent to the site. The fields after them
    describe how the value was built.
    """

    name: str
    value: str
    # name=value, for a Cookie header.
    cookie: str
    # cookie with its expiry and path, for a cookie jar.
    set_cookie: str
    fingerprint: str
    digest: str
    signature: str
    salt: str
    key: str
    version: str
    window_key_count: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ImpervaUTMVCResponse":
        return cls(
            name=data["name"],
            value=data["value"],
            cookie=data["cookie"],
            set_cookie=data["setCookie"],
            fingerprint=data["fingerprint"],
            digest=data["digest"],
            signature=data["signature"],
            salt=data["salt"],
            key=data["key"],
            version=data["version"],
            window_key_count=data["windowKeyCount"],
        )

from dataclasses import dataclass
from typing import Any

ScriptData = dict[str, Any]


@dataclass
class WebSensorRequest:
    user_agent: str
    url: str
    flags: str | None = None
    abck: str | None = None
    bm_sz: str | None = None
    sec_cpt: bool | None = None
    index: int | None = None
    stepper: bool | None = None
    keyboard: bool | None = None
    count: bool | None = None
    language: str | None = None
    custom_sensor: bool | None = None
    script_data: ScriptData | None = None
    script_url: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "userAgent": self.user_agent,
            "url": self.url,
        }
        if self.flags:
            result["flags"] = self.flags
        if self.abck:
            result["_abck"] = self.abck
        if self.bm_sz:
            result["bm_sz"] = self.bm_sz
        if self.sec_cpt is not None:
            result["sec_cpt"] = self.sec_cpt
        if self.index is not None:
            result["index"] = self.index
        if self.stepper is not None:
            result["stepper"] = self.stepper
        if self.keyboard is not None:
            result["keyboard"] = self.keyboard
        if self.count is not None:
            result["count"] = self.count
        if self.language:
            result["language"] = self.language
        if self.custom_sensor is not None:
            result["customSensor"] = self.custom_sensor
        if self.script_data:
            result["scriptData"] = self.script_data
        if self.script_url:
            result["scriptUrl"] = self.script_url
        return result


@dataclass
class WebSensorResponse:
    sensor: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WebSensorResponse":
        return cls(sensor=data["sensor"])


@dataclass
class PixelRequest:
    user_agent: str
    bazadebezolkohpepadr: int
    hash: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "userAgent": self.user_agent,
            "bazadebezolkohpepadr": self.bazadebezolkohpepadr,
            "hash": self.hash,
        }


@dataclass
class PixelResponse:
    sensor: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PixelResponse":
        return cls(sensor=data["sensor"])


@dataclass
class SecCptRequest:
    token: str
    timestamp: int
    nonce: str
    difficulty: int
    count: int
    cookie: str
    sec_cp_challenge: str | None = None
    provider: str | None = None
    branding_url_content: str | None = None
    chlg_duration: int | None = None
    timeout: int | None = None
    cpu: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "token": self.token,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "difficulty": self.difficulty,
            "count": self.count,
            "cookie": self.cookie,
        }
        if self.sec_cp_challenge:
            result["sec-cp-challenge"] = self.sec_cp_challenge
        if self.provider:
            result["provider"] = self.provider
        if self.branding_url_content:
            result["branding_url_content"] = self.branding_url_content
        if self.chlg_duration is not None:
            result["chlg_duration"] = self.chlg_duration
        if self.timeout is not None:
            result["timeout"] = self.timeout
        if self.cpu is not None:
            result["cpu"] = self.cpu
        return result


@dataclass
class SecCptResponse:
    token: str
    answers: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SecCptResponse":
        return cls(token=data["token"], answers=data["answers"])


@dataclass
class SBSDRequest:
    vid: str
    user_agent: str
    bm_o: str
    url: str
    legacy: bool | None = None
    script_hash: str | None = None
    script_url: str | None = None
    language: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "vid": self.vid,
            "userAgent": self.user_agent,
            "bm_o": self.bm_o,
            "url": self.url,
        }
        if self.legacy is not None:
            result["legacy"] = self.legacy
        if self.script_hash:
            result["script_hash"] = self.script_hash
        if self.script_url:
            result["script_url"] = self.script_url
        if self.language:
            result["language"] = self.language
        return result


@dataclass
class SBSDResponse:
    body: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SBSDResponse":
        return cls(body=data["body"])

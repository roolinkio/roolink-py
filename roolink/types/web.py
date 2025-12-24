from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict

# Type alias for parsed Akamai script configuration data
ScriptData = Dict[str, Any]


@dataclass
class WebSensorRequest:
    """Request to generate an Akamai web sensor."""

    user_agent: str
    url: str
    flags: Optional[str] = None
    abck: Optional[str] = None
    bm_sz: Optional[str] = None
    sec_cpt: Optional[bool] = None
    index: Optional[int] = None
    stepper: Optional[bool] = None
    keyboard: Optional[bool] = None
    count: Optional[bool] = None
    language: Optional[str] = None
    custom_sensor: Optional[bool] = None
    script_data: Optional[ScriptData] = None
    script_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with correct JSON field names."""
        result = {
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
    """Response from web sensor generation."""

    sensor: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebSensorResponse":
        return cls(sensor=data["sensor"])


@dataclass
class PixelRequest:
    """Request to generate pixel data."""

    user_agent: str
    bazadebezolkohpepadr: int
    hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "userAgent": self.user_agent,
            "bazadebezolkohpepadr": self.bazadebezolkohpepadr,
            "hash": self.hash,
        }


@dataclass
class PixelResponse:
    """Response from pixel generation."""

    sensor: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PixelResponse":
        return cls(sensor=data["sensor"])


@dataclass
class SecCptRequest:
    """Request to solve a sec-cpt challenge."""

    token: str
    timestamp: int
    nonce: str
    difficulty: int
    cookie: str
    sec_cp_challenge: Optional[str] = None
    provider: Optional[str] = None
    branding_url_content: Optional[str] = None
    chlg_duration: Optional[int] = None
    timeout: Optional[int] = None
    cpu: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "token": self.token,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "difficulty": self.difficulty,
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
    """Response from sec-cpt challenge."""

    token: str
    answers: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SecCptResponse":
        return cls(token=data["token"], answers=data["answers"])


@dataclass
class SBSDRequest:
    """Request to solve SBSD challenge."""

    vid: str
    user_agent: str
    bm_o: str
    url: str
    legacy: Optional[bool] = None
    script_hash: Optional[str] = None
    script_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
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
        return result


@dataclass
class SBSDResponse:
    """Response from SBSD challenge."""

    body: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SBSDResponse":
        return cls(body=data["body"])


@dataclass
class ParseResponse:
    """Response from script parsing."""

    script_data: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ParseResponse":
        return cls(script_data=data["scriptData"])

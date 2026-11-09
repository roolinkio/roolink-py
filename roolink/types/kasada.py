import base64
import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class KasadaPayloadRequest:
    script: str
    ips_url: str
    language: str
    referer: str
    user_agent: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "script": self.script,
            "ipsUrl": self.ips_url,
            "language": self.language,
            "referer": self.referer,
            "userAgent": self.user_agent,
        }


@dataclass
class KasadaPayloadResponse:
    headers: Dict[str, str]
    # The /tl request body, decoded from the base64 the API sends.
    payload: bytes

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KasadaPayloadResponse":
        return cls(
            headers=data["headers"],
            payload=base64.b64decode(data["payload"]),
        )


@dataclass
class KasadaCDRequest:
    st: int
    ct: str
    domain: str
    fc: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "st": self.st,
            "ct": self.ct,
            "domain": self.domain,
        }
        if self.fc:
            result["fc"] = self.fc
        return result


@dataclass
class KasadaCDResponse:
    # The x-kpsdk-cd header value, which is itself JSON, so send it unchanged.
    payload: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KasadaCDResponse":
        return cls(payload=data["payload"])


@dataclass
class KasadaBotIDRequest:
    script: str

    def to_dict(self) -> Dict[str, Any]:
        return {"script": self.script}


@dataclass
class KasadaBotIDResponse:
    b: float
    v: float
    e: str
    s: str
    d: float
    vr: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KasadaBotIDResponse":
        return cls(
            b=data["b"],
            v=data["v"],
            e=data["e"],
            s=data["s"],
            d=data["d"],
            vr=data["vr"],
        )

    def to_header(self) -> str:
        """Returns the x-is-human header value, compact JSON in the API's field order as a browser sends it."""
        return json.dumps(asdict(self), separators=(",", ":"))

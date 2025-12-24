from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict


@dataclass
class BMPSensorRequest:
    """Request to generate an Akamai BMP sensor."""

    app: str
    proxy: str
    language: Optional[str] = None
    android: Optional[bool] = None
    ipad: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Cookie:
    """Cookie returned from BMP sensor generation."""

    name: str
    value: str
    domain: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Cookie":
        return cls(
            name=data["name"],
            value=data["value"],
            domain=data["domain"],
        )


@dataclass
class BMPSensorResponse:
    """Response from BMP sensor generation."""

    sensor: str
    platform: str
    device_id: str
    app_version: str
    screen_height: int
    screen_width: int
    language: str

    # iOS specific fields
    ios: Optional[str] = None
    kernel_os_release: Optional[str] = None
    kernel_os_version: Optional[str] = None
    machine_id: Optional[str] = None
    cookies: Optional[List[Cookie]] = None

    # Android specific fields
    android: Optional[str] = None
    device_model: Optional[str] = None
    device_manufacturer: Optional[str] = None
    sdk_version: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BMPSensorResponse":
        cookies = None
        if "cookies" in data and data["cookies"]:
            cookies = [Cookie.from_dict(c) for c in data["cookies"]]

        return cls(
            sensor=data["sensor"],
            platform=data["platform"],
            device_id=data["deviceId"],
            app_version=data["appVersion"],
            screen_height=data["screenHeight"],
            screen_width=data["screenWidth"],
            language=data["language"],
            ios=data.get("ios"),
            kernel_os_release=data.get("kernelOsRelease"),
            kernel_os_version=data.get("kernelOsVersion"),
            machine_id=data.get("machineId"),
            cookies=cookies,
            android=data.get("android"),
            device_model=data.get("deviceModel"),
            device_manufacturer=data.get("deviceManufacturer"),
            sdk_version=data.get("sdkVersion"),
        )

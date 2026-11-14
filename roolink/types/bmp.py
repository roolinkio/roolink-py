from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class BMPSensorRequest:
    app: str
    proxy: str
    language: str | None = None
    device_id: str | None = None
    android: bool | None = None
    ipad: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        result = {k: v for k, v in asdict(self).items() if v is not None}
        if "device_id" in result:
            result["deviceId"] = result.pop("device_id")
        return result


@dataclass
class Cookie:
    name: str
    value: str
    domain: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Cookie":
        return cls(
            name=data["name"],
            value=data["value"],
            domain=data["domain"],
        )


@dataclass
class BMPSensorResponse:
    sensor: str
    platform: str
    device_id: str
    app_version: str
    screen_height: int
    screen_width: int
    language: str

    ios: str | None = None
    kernel_os_release: str | None = None
    kernel_os_version: str | None = None
    machine_id: str | None = None
    cookies: list[Cookie] | None = None

    android: str | None = None
    device_model: str | None = None
    device_manufacturer: str | None = None
    sdk_version: str | None = None
    app_version_code: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BMPSensorResponse":
        cookies = None
        if data.get("cookies"):
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
            app_version_code=data.get("appVersionCode"),
        )

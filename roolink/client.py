import gzip
import json
from types import TracebackType
from typing import Any

import httpx

from . import __version__
from .types.bmp import BMPSensorRequest, BMPSensorResponse
from .types.imperva import (
    ImpervaPayloadRequest,
    ImpervaUTMVCRequest,
    ImpervaUTMVCResponse,
)
from .types.kasada import (
    KasadaBotIDRequest,
    KasadaBotIDResponse,
    KasadaCDRequest,
    KasadaCDResponse,
    KasadaPayloadRequest,
    KasadaPayloadResponse,
)
from .types.web import (
    PixelRequest,
    PixelResponse,
    SBSDRequest,
    SBSDResponse,
    SecCptRequest,
    SecCptResponse,
    WebSensorRequest,
    WebSensorResponse,
)

BMP_BASE_URL = "https://bmp.roolink.io"
WEB_BASE_URL = "https://web.roolink.io"
KASADA_BASE_URL = "https://ksd.roolink.io"
IMPERVA_BASE_URL = "https://imperva.roolink.io"
DEFAULT_TIMEOUT = 30.0
USER_AGENT = f"roolink-py/{__version__}"


class RoolinkError(Exception):
    """Raised when the API answers with an error status.

    The message holds the status and the response body.
    """


class RoolinkClient:
    def __init__(self, api_key: str, compress: bool = True) -> None:
        """Creates a client that sends api_key with every request.

        When compress is True, parse_script gzips its request body. The client
        keeps connections open until close is called or a with block ends.
        """
        self.api_key = api_key
        self.compress = compress
        self.timeout = DEFAULT_TIMEOUT

        self.client = httpx.Client(
            http2=True,
            timeout=self.timeout,
        )

    def _request(
        self, url: str, body: str, content_type: str, compress: bool = False
    ) -> dict[str, Any]:
        return json.loads(
            self._send(url, body, content_type, compress=compress)
        )

    def _send(
        self, url: str, body: str, content_type: str, compress: bool = False
    ) -> str:
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": content_type,
            "User-Agent": USER_AGENT,
        }
        if compress:
            headers["Content-Encoding"] = "gzip"

        response = self.client.post(
            url,
            content=gzip.compress(body.encode()) if compress else body,
            headers=headers,
        )

        if response.status_code >= 400:
            raise RoolinkError(
                f"API error (status {response.status_code}): {response.text}"
            )

        return response.text

    def close(self) -> None:
        """Closes the client's connections. Calling it again does nothing."""
        self.client.close()

    def __enter__(self) -> "RoolinkClient":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def generate_bmp_sensor(self, req: BMPSensorRequest) -> BMPSensorResponse:
        url = f"{BMP_BASE_URL}/api/v1/sensor"
        data = self._request(url, json.dumps(req.to_dict()), "application/json")
        return BMPSensorResponse.from_dict(data)

    def generate_web_sensor(self, req: WebSensorRequest) -> WebSensorResponse:
        url = f"{WEB_BASE_URL}/api/v1/sensor"
        data = self._request(url, json.dumps(req.to_dict()), "application/json")
        return WebSensorResponse.from_dict(data)

    def generate_pixel(self, req: PixelRequest) -> PixelResponse:
        """Returns the sensor, which /pixel sends as text/plain, not JSON."""
        url = f"{WEB_BASE_URL}/api/v1/pixel"
        text = self._send(url, json.dumps(req.to_dict()), "application/json")
        return PixelResponse(sensor=text)

    def solve_sec_cpt(self, req: SecCptRequest) -> SecCptResponse:
        url = f"{WEB_BASE_URL}/api/v1/sec-cpt"
        data = self._request(url, json.dumps(req.to_dict()), "application/json")
        return SecCptResponse.from_dict(data)

    def solve_sbsd(self, req: SBSDRequest) -> SBSDResponse:
        url = f"{WEB_BASE_URL}/api/v1/sbsd"
        data = self._request(url, json.dumps(req.to_dict()), "application/json")
        return SBSDResponse.from_dict(data)

    def parse_script(self, script_content: str) -> dict[str, Any]:
        url = f"{WEB_BASE_URL}/api/v1/parse"
        return self._request(
            url, script_content, "text/plain", compress=self.compress
        )

    def generate_kasada_payload(
        self, req: KasadaPayloadRequest
    ) -> KasadaPayloadResponse:
        url = f"{KASADA_BASE_URL}/api/v1/payload"
        data = self._request(url, json.dumps(req.to_dict()), "application/json")
        return KasadaPayloadResponse.from_dict(data)

    def generate_kasada_cd(self, req: KasadaCDRequest) -> KasadaCDResponse:
        url = f"{KASADA_BASE_URL}/api/v1/cd"
        data = self._request(url, json.dumps(req.to_dict()), "application/json")
        return KasadaCDResponse.from_dict(data)

    def generate_kasada_bot_id(
        self, req: KasadaBotIDRequest
    ) -> KasadaBotIDResponse:
        url = f"{KASADA_BASE_URL}/api/v1/botid"
        data = self._request(url, json.dumps(req.to_dict()), "application/json")
        return KasadaBotIDResponse.from_dict(data)

    def generate_imperva_payload(self, req: ImpervaPayloadRequest) -> str:
        """Returns the Reese84 submission as the text the API sent.

        Post it to the challenge endpoint unchanged.
        """
        url = f"{IMPERVA_BASE_URL}/api/v1/payload"
        return self._send(url, json.dumps(req.to_dict()), "application/json")

    def generate_imperva_utmvc(
        self, req: ImpervaUTMVCRequest
    ) -> ImpervaUTMVCResponse:
        url = f"{IMPERVA_BASE_URL}/api/v1/utmvc"
        data = self._request(url, json.dumps(req.to_dict()), "application/json")
        return ImpervaUTMVCResponse.from_dict(data)

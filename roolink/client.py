import gzip
import json
from typing import Any, Dict

import httpx

from .types.bmp import BMPSensorRequest, BMPSensorResponse
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
DEFAULT_TIMEOUT = 30.0


class RoolinkClient:
    """Client for interacting with Roolink services."""

    def __init__(self, api_key: str, compress: bool = True):
        """
        Initialize the Roolink client.

        Args:
            api_key: Your Roolink API key
            compress: Whether parse_script gzips the script it sends
        """
        self.api_key = api_key
        self.compress = compress
        self.timeout = DEFAULT_TIMEOUT

        self.client = httpx.Client(
            http2=True,
            timeout=self.timeout,
        )

    def _request(
        self,
        method: str,
        url: str,
        body: str,
        content_type: str,
        compress: bool = False,
    ) -> Dict[str, Any]:
        """Make an HTTP request and decode the JSON response."""
        return json.loads(
            self._send(method, url, body, content_type, compress=compress)
        )

    def _send(
        self,
        method: str,
        url: str,
        body: str,
        content_type: str,
        compress: bool = False,
    ) -> str:
        """Make an HTTP request, gzipping the body if compress is set, and return the response body as text."""
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": content_type,
        }
        if compress:
            headers["Content-Encoding"] = "gzip"

        response = self.client.request(
            method=method,
            url=url,
            content=gzip.compress(body.encode()) if compress else body,
            headers=headers,
        )

        if response.status_code >= 400:
            raise Exception(
                f"API error (status {response.status_code}): {response.text}"
            )

        return response.text

    def __del__(self):
        """Clean up the HTTP client."""
        if hasattr(self, "client"):
            self.client.close()

    # BMP API Methods
    def generate_bmp_sensor(self, req: BMPSensorRequest) -> BMPSensorResponse:
        """Generate an Akamai BMP sensor for mobile apps."""
        url = f"{BMP_BASE_URL}/api/v1/sensor"
        data = self._request(
            "POST", url, json.dumps(req.to_dict()), "application/json"
        )
        return BMPSensorResponse.from_dict(data)

    # Web API Methods
    def generate_web_sensor(self, req: WebSensorRequest) -> WebSensorResponse:
        """Generate an Akamai web sensor."""
        url = f"{WEB_BASE_URL}/api/v1/sensor"
        data = self._request(
            "POST", url, json.dumps(req.to_dict()), "application/json"
        )
        return WebSensorResponse.from_dict(data)

    def generate_pixel(self, req: PixelRequest) -> PixelResponse:
        """Generate pixel sensor data."""
        url = f"{WEB_BASE_URL}/api/v1/pixel"
        text = self._send(
            "POST", url, json.dumps(req.to_dict()), "application/json"
        )
        return PixelResponse(sensor=text)

    def solve_sec_cpt(self, req: SecCptRequest) -> SecCptResponse:
        """Solve a sec-cpt crypto challenge."""
        url = f"{WEB_BASE_URL}/api/v1/sec-cpt"
        data = self._request(
            "POST", url, json.dumps(req.to_dict()), "application/json"
        )
        return SecCptResponse.from_dict(data)

    def solve_sbsd(self, req: SBSDRequest) -> SBSDResponse:
        """Solve an SBSD challenge."""
        url = f"{WEB_BASE_URL}/api/v1/sbsd"
        data = self._request(
            "POST", url, json.dumps(req.to_dict()), "application/json"
        )
        return SBSDResponse.from_dict(data)

    def parse_script(self, script_content: str) -> Dict[str, Any]:
        """Parse an Akamai script and return script data."""
        url = f"{WEB_BASE_URL}/api/v1/parse"
        return self._request(
            "POST", url, script_content, "text/plain", compress=self.compress
        )

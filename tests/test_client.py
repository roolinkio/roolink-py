import gzip
import json

import httpx

from roolink import BMPSensorRequest, PixelRequest, RoolinkClient, SecCptRequest


def mock_client(handler, **kwargs):
    client = RoolinkClient("roo_test", **kwargs)
    client.client = httpx.Client(transport=httpx.MockTransport(handler))
    return client


def test_pixel_returns_text_body():
    body = "ap=true&bt=0&fonts=1&fh=abc"

    def handler(request):
        return httpx.Response(
            200, text=body, headers={"Content-Type": "text/plain"}
        )

    resp = mock_client(handler).generate_pixel(
        PixelRequest(user_agent="ua", bazadebezolkohpepadr=1, hash="h")
    )
    assert resp.sensor == body


def test_bmp_sends_device_id_as_device_id_key():
    sent = {}

    def handler(request):
        sent.update(json.loads(request.content))
        return httpx.Response(400, text="stop")

    try:
        mock_client(handler).generate_bmp_sensor(
            BMPSensorRequest(app="app", proxy="http://p", device_id="dev-1")
        )
    except Exception:
        pass
    assert sent.get("deviceId") == "dev-1"
    assert "device_id" not in sent


def test_sec_cpt_sends_count():
    req = SecCptRequest(
        token="t", timestamp=1, nonce="n", difficulty=1, count=5, cookie="c"
    )
    assert req.to_dict()["count"] == 5


def test_compression():
    script = "var _ac=function(){};"
    sent = []

    def handler(request):
        sent.append(request)
        return httpx.Response(200, json={})

    mock_client(handler).parse_script(script)
    mock_client(handler, compress=False).parse_script(script)
    compressed, uncompressed = sent

    assert compressed.headers["Content-Encoding"] == "gzip"
    assert gzip.decompress(compressed.content).decode() == script
    assert "Content-Encoding" not in uncompressed.headers
    assert uncompressed.content.decode() == script

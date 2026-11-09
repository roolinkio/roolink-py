import gzip
import json

import httpx

import roolink
from roolink import (
    BMPSensorRequest,
    KasadaBotIDRequest,
    KasadaBotIDResponse,
    KasadaCDRequest,
    KasadaCDResponse,
    KasadaPayloadRequest,
    KasadaPayloadResponse,
    PixelRequest,
    RoolinkClient,
    SecCptRequest,
)


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


def test_user_agent_names_sdk_and_version():
    sent = []

    def handler(request):
        sent.append(request)
        return httpx.Response(200, json={})

    mock_client(handler).parse_script("var _ac=function(){};")
    assert sent[0].headers["User-Agent"] == f"roolink-py/{roolink.__version__}"


def kasada_client(reply):
    """Returns a client whose API answers every request with reply, and the list of requests it sent."""
    sent = []

    def handler(request):
        sent.append(request)
        return httpx.Response(
            200, text=reply, headers={"Content-Type": "application/json"}
        )

    return mock_client(handler), sent


def assert_kasada_request(sent, path, body):
    (request,) = sent
    assert request.method == "POST"
    assert str(request.url) == f"https://ksd.roolink.io{path}"
    assert request.headers["x-api-key"] == "roo_test"
    assert request.headers["Content-Type"] == "application/json"
    assert json.loads(request.content) == body


def test_kasada_payload():
    client, sent = kasada_client(
        '{"headers":{"x-kpsdk-ct":"ct","x-kpsdk-v":"j-1.1.0"},"payload":"APv/EA=="}\n'
    )

    resp = client.generate_kasada_payload(
        KasadaPayloadRequest(
            script="(function(){})();",
            ips_url="https://www.example.com/a/b/ips.js?x-kpsdk-v=j-1.1.0",
            language="en-US",
            referer="https://www.example.com/",
            user_agent="Mozilla/5.0",
        )
    )
    assert_kasada_request(
        sent,
        "/api/v1/payload",
        {
            "script": "(function(){})();",
            "ipsUrl": "https://www.example.com/a/b/ips.js?x-kpsdk-v=j-1.1.0",
            "language": "en-US",
            "referer": "https://www.example.com/",
            "userAgent": "Mozilla/5.0",
        },
    )
    assert resp == KasadaPayloadResponse(
        headers={"x-kpsdk-ct": "ct", "x-kpsdk-v": "j-1.1.0"},
        payload=b"\x00\xfb\xff\x10",
    )


def test_kasada_cd():
    cd = '{"workTime":1788893087900,"id":"0123456789abcdef0123456789abcdef","answers":[3,7],"duration":2,"d":120,"st":1788893087778,"rst":1788893087898}'
    session = {
        "st": 1788893087778,
        "ct": "0aGzYc9d3d1b8f6f4e0e2d7c1b9a5f3e",
        "domain": "www.example.com",
    }

    for fc, body in [
        ("eyJ4IjoxfQ==", {**session, "fc": "eyJ4IjoxfQ=="}),
        (None, session),
    ]:
        client, sent = kasada_client(json.dumps({"payload": cd}))
        resp = client.generate_kasada_cd(KasadaCDRequest(**session, fc=fc))
        assert_kasada_request(sent, "/api/v1/cd", body)
        assert resp == KasadaCDResponse(payload=cd)


def test_kasada_bot_id():
    header = '{"b":0,"v":0.08084381062192014,"e":"eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..uydqejFMULzuEHyK.Eh2s.aM1k","s":"q+/0Zm9v","d":2,"vr":"3"}'
    client, sent = kasada_client(header + "\n")

    resp = client.generate_kasada_bot_id(
        KasadaBotIDRequest(script="(function(){})();")
    )
    assert_kasada_request(
        sent, "/api/v1/botid", {"script": "(function(){})();"}
    )
    assert resp == KasadaBotIDResponse(
        b=0,
        v=0.08084381062192014,
        e="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..uydqejFMULzuEHyK.Eh2s.aM1k",
        s="q+/0Zm9v",
        d=2,
        vr="3",
    )
    # The x-is-human header is the response serialized back to JSON, which must match what the API sent.
    assert resp.to_header() == header

import dataclasses
import gzip
import json

import httpx
import pytest

import roolink
from roolink import (
    BMPSensorRequest,
    ImpervaPayloadRequest,
    ImpervaUTMVCRequest,
    ImpervaUTMVCResponse,
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


def json_client(reply, status=200):
    """Returns a client whose API answers every request with reply and status, and the list of requests it sent."""
    sent = []

    def handler(request):
        sent.append(request)
        return httpx.Response(
            status, text=reply, headers={"Content-Type": "application/json"}
        )

    return mock_client(handler), sent


def assert_json_request(sent, url, body):
    (request,) = sent
    assert request.method == "POST"
    assert str(request.url) == url
    assert request.headers["x-api-key"] == "roo_test"
    assert request.headers["Content-Type"] == "application/json"
    assert json.loads(request.content) == body


def test_kasada_payload():
    client, sent = json_client(
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
    assert_json_request(
        sent,
        "https://ksd.roolink.io/api/v1/payload",
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
        client, sent = json_client(json.dumps({"payload": cd}))
        resp = client.generate_kasada_cd(KasadaCDRequest(**session, fc=fc))
        assert_json_request(sent, "https://ksd.roolink.io/api/v1/cd", body)
        assert resp == KasadaCDResponse(payload=cd)


def test_kasada_bot_id():
    header = '{"b":0,"v":0.08084381062192014,"e":"eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..uydqejFMULzuEHyK.Eh2s.aM1k","s":"q+/0Zm9v","d":2,"vr":"3"}'
    client, sent = json_client(header + "\n")

    resp = client.generate_kasada_bot_id(
        KasadaBotIDRequest(script="(function(){})();")
    )
    assert_json_request(
        sent,
        "https://ksd.roolink.io/api/v1/botid",
        {"script": "(function(){})();"},
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


IMPERVA_PAYLOAD = ImpervaPayloadRequest(
    script="(function(){})();",
    script_url="/Hedge-the-Stage-Thy-Seed/script.js",
    page_url="https://www.example.com/",
    user_agent="Mozilla/5.0",
    language="en-US,en;q=0.9",
)


def test_imperva_payload():
    # Callers post the submission to Imperva unchanged, so the client must return the text the API sent.
    submission = '{"solution":{"interrogation":{"p":"AAEC/w==","st":1788893087,"sr":3420118839,"cr":2045817226,"og":2},"version":"stable"},"old_token":null,"error":null,"errors":[],"performance":{"1030820235":41,"4203433130":12,"total":43}}'
    body = {
        "script": "(function(){})();",
        "scriptUrl": "/Hedge-the-Stage-Thy-Seed/script.js",
        "pageUrl": "https://www.example.com/",
        "userAgent": "Mozilla/5.0",
        "language": "en-US,en;q=0.9",
    }

    for pow, sent_body in [
        (
            "eyJjIjoiYWJjIiwiZCI6NH0=",
            {**body, "pow": "eyJjIjoiYWJjIiwiZCI6NH0="},
        ),
        (None, body),
    ]:
        client, sent = json_client(submission)
        resp = client.generate_imperva_payload(
            dataclasses.replace(IMPERVA_PAYLOAD, pow=pow)
        )
        assert_json_request(
            sent, "https://imperva.roolink.io/api/v1/payload", sent_body
        )
        assert resp == submission


def test_imperva_payload_error():
    # An error body is JSON as well, and posting it to Imperva as a submission would fail without saying why.
    client, _ = json_client(
        '{"code":"device_not_found","error":"no collected browser has this User-Agent"}',
        status=422,
    )

    with pytest.raises(Exception, match="device_not_found"):
        client.generate_imperva_payload(IMPERVA_PAYLOAD)


def test_imperva_utmvc():
    cookie = {
        "name": "___utmvc",
        "value": "jxKgPCxkaWdlc3Q9NzI2MSxzPTlkYTQ5YmE0OWY1ZmE5OTJhM2E2NjNhMWEzYTdhOQ==",
        "cookie": "___utmvc=jxKgPCxkaWdlc3Q9NzI2MSxzPTlkYTQ5YmE0OWY1ZmE5OTJhM2E2NjNhMWEzYTdhOQ==",
        "setCookie": "___utmvc=jxKgPCxkaWdlc3Q9NzI2MSxzPTlkYTQ5YmE0OWY1ZmE5OTJhM2E2NjNhMWEzYTdhOQ==; expires=Mon, 09 Nov 2026 19:04:40 GMT; path=/",
        "fingerprint": "navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.",
        "digest": "7261",
        "signature": "9da49ba49f5fa992a3a663a1a3a7a9",
        "salt": "fresh-salt-plus",
        "key": "fresh",
        "version": "version-one",
        "windowKeyCount": 289,
    }

    # The API requires cookies, so an empty document.cookie must still be sent.
    for cookies in ["incap_ses_1234_567890=abc; visid_incap_567890=def", ""]:
        client, sent = json_client(json.dumps(cookie) + "\n")
        resp = client.generate_imperva_utmvc(
            ImpervaUTMVCRequest(
                script="(function(){})();",
                cookies=cookies,
                user_agent="Mozilla/5.0",
            )
        )
        assert_json_request(
            sent,
            "https://imperva.roolink.io/api/v1/utmvc",
            {
                "script": "(function(){})();",
                "cookies": cookies,
                "userAgent": "Mozilla/5.0",
            },
        )
        assert resp == ImpervaUTMVCResponse(
            name="___utmvc",
            value="jxKgPCxkaWdlc3Q9NzI2MSxzPTlkYTQ5YmE0OWY1ZmE5OTJhM2E2NjNhMWEzYTdhOQ==",
            cookie="___utmvc=jxKgPCxkaWdlc3Q9NzI2MSxzPTlkYTQ5YmE0OWY1ZmE5OTJhM2E2NjNhMWEzYTdhOQ==",
            set_cookie="___utmvc=jxKgPCxkaWdlc3Q9NzI2MSxzPTlkYTQ5YmE0OWY1ZmE5OTJhM2E2NjNhMWEzYTdhOQ==; expires=Mon, 09 Nov 2026 19:04:40 GMT; path=/",
            fingerprint="navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.",
            digest="7261",
            signature="9da49ba49f5fa992a3a663a1a3a7a9",
            salt="fresh-salt-plus",
            key="fresh",
            version="version-one",
            window_key_count=289,
        )

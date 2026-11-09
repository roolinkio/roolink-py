# Roolink Python SDK

Python client (`roolink`) for the Roolink Akamai Web (`web.roolink.io`), Akamai BMP (`bmp.roolink.io`), Kasada (`ksd.roolink.io`) and Imperva (`imperva.roolink.io`) APIs.

Documentation: https://docs.roolink.io

## Install

```sh
pip install roolink
```

## Usage

```python
from roolink import RoolinkClient, WebSensorRequest

client = RoolinkClient("your-api-key")

script_data = client.parse_script(script_text)
sensor = client.generate_web_sensor(
    WebSensorRequest(
        user_agent=user_agent,
        url="https://example.com/",
        abck=abck_cookie,
        bm_sz=bm_sz_cookie,
        script_data=script_data,
    )
)
```

## Methods

| Method | Endpoint |
| --- | --- |
| `parse_script(script_text)` | `POST https://web.roolink.io/api/v1/parse` (gzip-compressed by default; pass `compress=False` to `RoolinkClient` to disable) |
| `generate_web_sensor(WebSensorRequest)` | `POST https://web.roolink.io/api/v1/sensor` |
| `generate_pixel(PixelRequest)` | `POST https://web.roolink.io/api/v1/pixel` |
| `solve_sec_cpt(SecCptRequest)` | `POST https://web.roolink.io/api/v1/sec-cpt` |
| `solve_sbsd(SBSDRequest)` | `POST https://web.roolink.io/api/v1/sbsd` |
| `generate_bmp_sensor(BMPSensorRequest)` | `POST https://bmp.roolink.io/api/v1/sensor` (`android=False` for iOS, `android=True` for Android) |
| `generate_kasada_payload(KasadaPayloadRequest)` | `POST https://ksd.roolink.io/api/v1/payload` |
| `generate_kasada_cd(KasadaCDRequest)` | `POST https://ksd.roolink.io/api/v1/cd` |
| `generate_kasada_bot_id(KasadaBotIDRequest)` | `POST https://ksd.roolink.io/api/v1/botid` |
| `generate_imperva_payload(ImpervaPayloadRequest)` | `POST https://imperva.roolink.io/api/v1/payload` |
| `generate_imperva_utmvc(ImpervaUTMVCRequest)` | `POST https://imperva.roolink.io/api/v1/utmvc` |

## Kasada

`generate_kasada_payload` decodes the payload from base64, so `payload` is the `/tl` request body as `bytes`. Each protected request needs a new `generate_kasada_cd`, whose `payload` is the `x-kpsdk-cd` header value. For Vercel BotID, the `x-is-human` header is the response's `to_header()`.

```python
from roolink import KasadaBotIDRequest, KasadaCDRequest, KasadaPayloadRequest

answer = client.generate_kasada_payload(
    KasadaPayloadRequest(
        script=ips_script,
        ips_url=ips_url,
        language="en-US",
        referer="https://www.example.com/",
        user_agent=user_agent,
    )
)
# Post answer.payload to /tl with answer.headers, and keep its x-kpsdk-ct and x-kpsdk-st response headers.

cd = client.generate_kasada_cd(
    KasadaCDRequest(st=st, ct=ct, domain="www.example.com")
).payload

is_human = client.generate_kasada_bot_id(
    KasadaBotIDRequest(script=bot_id_script)
).to_header()
```

## Imperva

`generate_imperva_payload` returns the Reese84 submission as the JSON text the API sent, which the site expects unchanged. Pass `pow` only when the site's GPC request returns a challenge. `generate_imperva_utmvc` takes every cookie the site has set as one `document.cookie` string, including the `incap_ses_*` cookies, and returns the `___utmvc` cookie.

```python
from roolink import ImpervaPayloadRequest, ImpervaUTMVCRequest

submission = client.generate_imperva_payload(
    ImpervaPayloadRequest(
        script=sensor_script,
        script_url=script_url,
        page_url="https://www.example.com/",
        user_agent=user_agent,
        language="en-US,en;q=0.9",
        pow=pow_challenge or None,
    )
)
# Post submission to script_url with d=<host> in the query, and store the token in the reply as the reese84 cookie.

cookie = client.generate_imperva_utmvc(
    ImpervaUTMVCRequest(
        script=incapsula_script,
        cookies=document_cookie,
        user_agent=user_agent,
    )
).cookie
```

## License

MIT — see [LICENSE](LICENSE).

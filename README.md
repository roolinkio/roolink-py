# Roolink Python SDK

Python client (`roolink`) for the Roolink Akamai Web (`web.roolink.io`) and Akamai BMP (`bmp.roolink.io`) APIs.

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

## License

MIT — see [LICENSE](LICENSE).

<div align="center">

# 🔗 Roolink Python SDK

### Enterprise-grade Akamai sensor generation for Python

[![PyPI](https://img.shields.io/badge/PyPI-1.0.0-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/roolink/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

**[📚 Documentation](https://docs.roolink.io/)** • **[💬 Discord](https://discord.gg/rooapi)**

---

</div>

## 🚀 Overview

Production-ready APIs for generating Akamai sensor data across web and mobile platforms. This SDK handles authentication, requests, and response parsing with full type hints.

### 🎯 Supported Services

| Service | Features |
|---------|----------|
| **🌐 Web API** | Sensor generation, pixel challenges, SBSD, sec-cpt solving |
| **📱 BMP API** | iOS & Android mobile app sensor generation |

---

## 📦 Installation

```bash
pip install roolink
```

## ⚡ Quick Start

```python
from roolink import RoolinkClient

client = RoolinkClient('your-api-key')
sensor = client.generate_web_sensor(req)
```

---

## 🌐 Web API

```python
# Sensor Generation
client.generate_web_sensor(req)

# Pixel Challenges
client.generate_pixel(req)

# Sec-Cpt Challenges
client.solve_sec_cpt(req)

# SBSD Challenges
client.solve_sbsd(req)

# Script Parsing
client.parse_script(script_content)
```

---

## 📱 BMP API

```python
# iOS Sensors (android=False)
client.generate_bmp_sensor(BMPSensorRequest(
    android=False,
))

# Android Sensors (android=True)
client.generate_bmp_sensor(BMPSensorRequest(
    android=True,
))
```

---

## 🆘 Error Handling

```python
try:
    result = client.generate_web_sensor(req)
except Exception as e:
    # handle error
    pass
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with 💜**

</div>

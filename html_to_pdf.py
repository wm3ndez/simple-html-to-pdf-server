import base64
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import logging

logger = logging.getLogger(__name__)


def _encode_html(html: str) -> str:
    return base64.b64encode(html.encode("utf-8")).decode()


def to_pdf(html: str) -> bytes:
    html_b64 = _encode_html(html)
    chrome_options = build_chrome_options()
    executable_path = os.environ.get("CHROMEDRIVER_PATH") or "/usr/bin/chromedriver"

    try:
        driver = webdriver.Chrome(
            executable_path=executable_path, chrome_options=chrome_options
        )
    except Exception as e:
        logger.error(e)
        print(e)
        return b""

    try:
        driver.get(f"data:text/html;base64,{html_b64}")
        pdf = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
    except Exception as e:
        logger.error(e)
        print(e)
        return b""
    finally:
        driver.close()

    return base64.b64decode(pdf["data"])


def build_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-profile")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu-rasterization")
    chrome_options.add_argument("--disable-software-rasterizer")

    chrome_options.binary_location = (
        os.environ.get("CHROME_BINARY") or "/opt/google/chrome/chrome"
    )

    return chrome_options

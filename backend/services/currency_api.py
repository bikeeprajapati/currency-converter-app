import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://v6.exchangerate-api.com/v6"


def get_conversion_rate(base: str, target: str) -> float:
    API_KEY = os.getenv("CURRENCY_API_KEY")

    if not API_KEY:
        raise RuntimeError("CURRENCY_API_KEY is not set")

    # ExchangeRate-API uses this format: /v6/{api_key}/pair/{from}/{to}
    url = f"{BASE_URL}/{API_KEY}/pair/{base}/{target}"
    
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(
            f"Currency API HTTP {response.status_code}: {response.text}"
        )

    data = response.json()

    if data.get("result") != "success":
        raise RuntimeError(f"API Error: {data}")

    return data["conversion_rate"]
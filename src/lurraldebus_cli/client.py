import requests
from .municipalities import MUNICIPALITIES

BASE_URL = "https://lurraldebus.eus"
TIMEOUT = 15
MAX_RETRIES = 2


class LurraldebusClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "lurraldebus-cli/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })

    def get_municipalities(self):
        return dict(MUNICIPALITIES)

    def get_stops(self, municipio_id):
        url = f"{BASE_URL}/real/ajax_get_paradas_municipio_info.json"
        for attempt in range(MAX_RETRIES + 1):
            try:
                resp = self.session.post(
                    url,
                    data={"municipioId": municipio_id},
                    timeout=TIMEOUT,
                )
                resp.raise_for_status()
                data = resp.json()
                if data.get("status") == 200:
                    return data["data"]
                return []
            except requests.RequestException:
                if attempt == MAX_RETRIES:
                    raise

    def get_arrivals_html(self, municipio_id, parada_id):
        url = f"{BASE_URL}/real/result"
        payload = {
            "_method": "POST",
            "data[Real][municipioId]": municipio_id,
            "data[Real][paradaId]": parada_id,
        }
        for attempt in range(MAX_RETRIES + 1):
            try:
                resp = self.session.post(
                    url,
                    data=payload,
                    timeout=TIMEOUT,
                )
                resp.raise_for_status()
                return resp.text
            except requests.RequestException:
                if attempt == MAX_RETRIES:
                    raise

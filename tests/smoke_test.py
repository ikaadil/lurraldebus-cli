import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lurraldebus_cli.client import LurraldebusClient
from lurraldebus_cli.matching import parse_arrivals, match_municipality, match_stop


def test_list_municipalities():
    client = LurraldebusClient()
    municipalities = client.get_municipalities()
    assert len(municipalities) > 50, f"Expected >50 municipalities, got {len(municipalities)}"
    assert "20069" in municipalities, "Donostia/San Sebastian should be present"
    print(f"[PASS] Listed {len(municipalities)} municipalities")


def test_list_stops():
    client = LurraldebusClient()
    stops = client.get_stops("20069")
    assert len(stops) > 10, f"Expected >10 stops for Donostia, got {len(stops)}"
    stop_names = [s["name"] for s in stops]
    assert any("Gipuzkoa" in n for n in stop_names), "Should find Gipuzkoa plaza stop"
    print(f"[PASS] Listed {len(stops)} stops for Donostia/San Sebastian")


def test_live_arrivals():
    client = LurraldebusClient()
    html = client.get_arrivals_html("20069", "109")
    assert "line-number" in html or "live-line-time" in html, "HTML should contain arrival data"
    arrivals = parse_arrivals(html)
    if arrivals:
        print(f"[PASS] Got {len(arrivals)} live arrivals for Gipuzkoa plaza 10")
        for a in arrivals[:3]:
            print(f"  {a['line_number']} -> {a['direction']} ({a['time']})")
    else:
        print("[PASS] No arrivals currently (valid empty-board response)")


def test_municipality_matching():
    matches = match_municipality("Donostia / San Sebastian")
    assert len(matches) == 1
    assert matches[0][0] == "20069"
    print("[PASS] Municipality matching works")


def test_stop_matching():
    stops = [{"value": "109", "name": "109 - Donostia - Gipuzkoa plaza 10"}]
    matches = match_stop("109", stops)
    assert len(matches) == 1
    assert matches[0][0] == "109"
    print("[PASS] Stop matching works")


if __name__ == "__main__":
    print("Running smoke tests against live lurraldebus.eus API...\n")
    test_list_municipalities()
    test_list_stops()
    test_live_arrivals()
    test_municipality_matching()
    test_stop_matching()
    print("\nAll smoke tests passed!")

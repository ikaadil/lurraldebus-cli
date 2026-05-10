from .municipalities import MUNICIPALITIES
import re


def parse_arrivals(html):
    table_start = html.find("<table")
    table_end = html.find("</table>")
    if table_start == -1 or table_end == -1:
        return []
    table = html[table_start:table_end]
    rows = re.findall(r"<tr>(.*?)</tr>", table, re.DOTALL)
    arrivals = []
    for i, row in enumerate(rows):
        if i == 0:
            continue
        line_number = _extract(row, r'class="line-number"[^>]*>\s*([^<]+)')
        line_name = _extract(row, r'class="line-name"[^>]*>\s*([^<]+)')
        occupancy = _extract_occupancy(row)
        direction = _extract_direction(row)
        time = _extract(row, r'class="live-line-time"[^>]*>\s*<p>\s*<span>\s*([^<]+)')
        if line_number or time:
            arrivals.append({
                "line_number": line_number.strip() if line_number else "?",
                "line_name": line_name.strip() if line_name else "",
                "occupancy": occupancy.strip() if occupancy else "-",
                "direction": direction.strip() if direction else "?",
                "time": time.strip() if time else "?",
            })
    return arrivals


def _extract(row, pattern):
    m = re.search(pattern, row, re.DOTALL)
    return m.group(1) if m else ""


def _extract_occupancy(row):
    pattern = r'ocupacion[^>]*>[^<]*</img>\s*<span[^>]*>\s*([^<]+)'
    m = re.search(pattern, row, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    pattern2 = r'ocupacion\.png[^/]*/>\s*<span[^>]*>\s*([^<]+)'
    m2 = re.search(pattern2, row, re.DOTALL | re.IGNORECASE)
    return m2.group(1).strip() if m2 else "-"


def _extract_direction(row):
    tds = re.findall(r'<td class="line-direction">(.*?)</td>', row, re.DOTALL)
    for td in tds:
        text = re.sub(r'<[^>]+>', '', td).strip()
        if text:
            return text
    return "?"


def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())


def match_municipality(name, municipalities=None):
    if municipalities is None:
        municipalities = MUNICIPALITIES
    name_norm = normalize(name)
    exact = []
    for mid, mname in municipalities.items():
        if normalize(mname) == name_norm:
            exact.append((mid, mname))
    if exact:
        return exact
    partial = []
    for mid, mname in municipalities.items():
        if name_norm in normalize(mname):
            partial.append((mid, mname))
    return partial


def match_stop(name, stops):
    name_norm = normalize(name)
    exact = []
    for stop in stops:
        stop_name = stop.get("name", "")
        stop_id = stop.get("value", "")
        if normalize(stop_name) == name_norm:
            exact.append((stop_id, stop_name))
    if exact:
        return exact
    partial = []
    for stop in stops:
        stop_name = stop.get("name", "")
        stop_id = stop.get("value", "")
        if name_norm in normalize(stop_name):
            partial.append((stop_id, stop_name))
    return partial

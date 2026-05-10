import json
import re


def normalize_occupation(value):
    if not value or value in ("-", "ocupacion-", "ocupacion -"):
        return "-"
    m = re.search(r"ocupacion\s*(.+)", value, re.IGNORECASE)
    if m:
        inner = m.group(1).strip()
        return inner if inner and inner != "-" else "-"
    return value.strip() if value.strip() and value.strip() != "-" else "-"


def format_arrivals_table(arrivals, stop_name=""):
    if not arrivals:
        return "No live arrivals found" + (f" for {stop_name}" if stop_name else "")

    header = f"{'Line':<6} {'Route':<52} {'Occupation':<14} {'Direction':<26} {'Min':<8}"
    separator = "-" * len(header)
    lines = [separator, header, separator]

    for a in arrivals:
        line = a.get("line_number", "?")
        route = a.get("line_name", "") or "-"
        direction = a.get("direction", "?")
        time = a.get("time", "?")
        occupation_text = a.get("occupation_text", "ocupacion -")
        occupation_display = normalize_occupation(occupation_text)

        minutes = time
        if "min" not in minutes.lower():
            minutes = minutes + " min" if minutes and minutes != "?" else "-"
        if minutes == "0 min":
            minutes = "0 min"

        route = route[:50] + ".." if len(route) > 52 else route
        direction = direction[:24] + ".." if len(direction) > 26 else direction

        lines.append(f"{line:<6} {route:<52} {occupation_display:<14} {direction:<26} {minutes:<8}")

    lines.append(separator)
    return "\n".join(lines)


def format_arrivals_json(arrivals, stop_name="", stop_id="", municipio_id=""):
    output = {
        "municipality_id": municipio_id,
        "stop_id": stop_id,
        "stop_name": stop_name,
        "arrivals": [],
    }
    for a in arrivals:
        time_str = a.get("time", "?")
        minutes = time_str
        if "min" in minutes.lower():
            minutes = minutes.lower().replace("min", "").strip()
        if minutes == "":
            minutes = "0"
        output["arrivals"].append({
            "line": a.get("line_number", "?"),
            "route": a.get("line_name", ""),
            "direction": a.get("direction", ""),
            "minutes": minutes,
            "occupancy": a.get("occupancy", "-"),
            "occupation_text": a.get("occupation_text", "ocupacion -"),
        })
    return json.dumps(output, indent=2, ensure_ascii=False)


def format_municipalities_table(municipalities):
    lines = []
    for mid, name in sorted(municipalities.items(), key=lambda x: x[1]):
        lines.append(f"  {name}")
    return "\n".join(lines)


def format_municipalities_json(municipalities):
    data = [{"id": mid, "name": name} for mid, name in sorted(municipalities.items(), key=lambda x: x[1])]
    return json.dumps(data, indent=2, ensure_ascii=False)


def format_stops_table(stops):
    lines = []
    for stop in stops:
        lines.append(f"  {stop['name']}")
    return "\n".join(lines)


def format_stops_json(stops):
    data = [{"id": s.get("value", ""), "name": s.get("name", "")} for s in stops]
    return json.dumps(data, indent=2, ensure_ascii=False)

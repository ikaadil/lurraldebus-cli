import json


def format_arrivals_table(arrivals, stop_name=""):
    if not arrivals:
        return "No live arrivals found" + (f" for {stop_name}" if stop_name else "")

    header = f"{'Line':<8} {'Destination':<35} {'Minutes':<10} {'Occupancy':<10}"
    separator = "-" * len(header)
    lines = [separator, header, separator]

    for a in arrivals:
        line = a.get("line_number", "?")
        direction = a.get("direction", "?")
        time = a.get("time", "?")
        occupancy = a.get("occupancy", "-")

        minutes = time
        if "min" in minutes.lower():
            minutes = minutes.lower().replace("min", "").strip()
        if minutes == "":
            minutes = "0"

        direction = direction[:33] + ".." if len(direction) > 35 else direction

        lines.append(f"{line:<8} {direction:<35} {minutes:<10} {occupancy:<10}")

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

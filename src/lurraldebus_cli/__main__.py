import argparse
import sys

from .client import LurraldebusClient
from .matching import match_municipality, match_stop, parse_arrivals
from .formatting import (
    format_arrivals_table,
    format_arrivals_json,
    format_municipalities_table,
    format_municipalities_json,
    format_stops_table,
    format_stops_json,
)


def main():
    parser = argparse.ArgumentParser(
        prog="lurraldebus-cli",
        description="Fetch live bus arrivals from Lurraldebus (Gipuzkoa, Basque Country)",
    )
    parser.add_argument(
        "--municipality", "-m",
        help="Municipality name (e.g. 'Donostia / San Sebastian')",
    )
    parser.add_argument(
        "--stop", "-s",
        help="Bus stop name or number (e.g. 'Gipuzkoa plaza' or '109')",
    )
    parser.add_argument(
        "--list-municipalities",
        action="store_true",
        help="List all available municipalities",
    )
    parser.add_argument(
        "--list-stops",
        action="store_true",
        help="List bus stops for the given municipality (requires --municipality)",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        dest="json_output",
        help="Output as JSON",
    )

    args = parser.parse_args()
    client = LurraldebusClient()

    if args.list_municipalities:
        municipalities = client.get_municipalities()
        if args.json_output:
            print(format_municipalities_json(municipalities))
        else:
            print("Available municipalities:\n")
            print(format_municipalities_table(municipalities))
        return

    if args.list_stops:
        if not args.municipality:
            print("Error: --list-stops requires --municipality", file=sys.stderr)
            sys.exit(1)
        matches = match_municipality(args.municipality)
        if not matches:
            print(f"No municipality matching '{args.municipality}' found.", file=sys.stderr)
            sys.exit(1)
        if len(matches) > 1:
            print(f"Multiple municipalities match '{args.municipality}':", file=sys.stderr)
            for mid, mname in matches:
                print(f"  {mname} (ID: {mid})", file=sys.stderr)
            sys.exit(1)
        mid, mname = matches[0]
        try:
            stops = client.get_stops(mid)
        except Exception as e:
            print(f"Error fetching stops: {e}", file=sys.stderr)
            sys.exit(1)
        if not stops:
            print(f"No stops found for {mname}", file=sys.stderr)
            sys.exit(1)
        if args.json_output:
            print(format_stops_json(stops))
        else:
            print(f"Bus stops in {mname}:\n")
            print(format_stops_table(stops))
        return

    if args.municipality and args.stop:
        matches = match_municipality(args.municipality)
        if not matches:
            print(f"No municipality matching '{args.municipality}' found.", file=sys.stderr)
            sys.exit(1)
        if len(matches) > 1:
            print(f"Multiple municipalities match '{args.municipality}':", file=sys.stderr)
            for mid, mname in matches:
                print(f"  {mname} (ID: {mid})", file=sys.stderr)
            sys.exit(1)
        mid, mname = matches[0]

        try:
            stops = client.get_stops(mid)
        except Exception as e:
            print(f"Error fetching stops: {e}", file=sys.stderr)
            sys.exit(1)

        stop_matches = match_stop(args.stop, stops)
        if not stop_matches:
            print(f"No stop matching '{args.stop}' found in {mname}.", file=sys.stderr)
            print("Try --list-stops --municipality to see available stops.", file=sys.stderr)
            sys.exit(1)
        if len(stop_matches) > 1:
            print(f"Multiple stops match '{args.stop}':", file=sys.stderr)
            for sid, sname in stop_matches:
                print(f"  {sname} (ID: {sid})", file=sys.stderr)
            sys.exit(1)

        sid, sname = stop_matches[0]

        try:
            html = client.get_arrivals_html(mid, sid)
        except Exception as e:
            print(f"Error fetching arrivals: {e}", file=sys.stderr)
            sys.exit(1)

        arrivals = parse_arrivals(html)

        if args.json_output:
            print(format_arrivals_json(arrivals, sname, sid, mid))
        else:
            print(f"\n  Live arrivals: {sname}\n")
            print(format_arrivals_table(arrivals, sname))
        return

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()

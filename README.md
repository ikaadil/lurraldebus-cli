# lurraldebus-cli

A command-line tool that fetches live bus arrival data from the [Lurraldebus](https://lurraldebus.eus) website (Gipuzkoa, Basque Country, Spain).

## What it does

This CLI replicates the "Live Arrivals" (Llegadas en tiempo real) feature of the Lurraldebus website. Given a municipality and a bus stop, it prints the same live arrival billboard you'd see on the website.

## Installation

```bash
pip install -r requirements.txt
```

Requires Python 3.8+ and the `requests` library.

## Usage

### List all municipalities

```bash
python -m lurraldebus_cli --list-municipalities
```

### List bus stops for a municipality

```bash
python -m lurraldebus_cli --list-stops --municipality "Donostia / San Sebastian"
```

### Fetch live arrivals

```bash
python -m lurraldebus_cli --municipality "Donostia / San Sebastian" --stop "Gipuzkoa plaza 10"
```

You can also use stop numbers:

```bash
python -m lurraldebus_cli --municipality "Donostia / San Sebastian" --stop "109"
```

### Output as JSON

Add `--json` (or `-j`) to any command for structured JSON output:

```bash
python -m lurraldebus_cli --municipality "Irun" --stop "1503" --json
```

### Short options

```
-m, --municipality   Municipality name
-s, --stop           Bus stop name or number
-j, --json           Output as JSON
    --list-municipalities  List all municipalities
    --list-stops           List stops for a municipality
```

## Example output

```
  Live arrivals: 109 - Donostia - Gipuzkoa plaza 10

------------------------------------------------------------------
Line     Destination                         Minutes    Occupancy
------------------------------------------------------------------
E21      Hondarribia                         00         16
E27      Hondarri(N-1)                       06         -
E01      Donostia/San Sebastian              10         38
E05      Donostia/San Sebastian              15         0
E02      Donostia/San Sebastian              22         43
E27      Donostia (N-I)                      30         39
E27      Donostia (N-I)                      47         25
------------------------------------------------------------------
```

## Matching behavior

- Municipality and stop matching is **case-insensitive** and **partial**.
- If multiple matches are found, the CLI lists all matches and exits with an error code.
- If no matches are found, it prints a clear message and exits with an error code.

## Running tests

```bash
python -m pytest tests/test_matching.py -v
```

To run a smoke test against the live API:

```bash
python tests/smoke_test.py
```

## Known limitations

- The live arrivals data comes from HTML parsing (no JSON API available for the billboard). If the website layout changes significantly, the parser may break.
- Occupancy data may show `-` when not available.
- Some municipalities (e.g., Vitoria-Gasteiz, Bilbao) have limited stop data because they are outside the core Gipuzkoa service area.
- Arrival times are in minutes and may be "00 min" (arriving now) or slightly delayed.

## Troubleshooting

- **Connection errors**: Check your internet connection. The tool requires access to `https://lurraldebus.eus`.
- **No arrivals found**: This is normal outside service hours or for stops with no active service. Try a major stop like Gipuzkoa Plaza in Donostia.
- **Multiple matches**: Use a more specific name or the stop number (from `--list-stops`) to disambiguate.

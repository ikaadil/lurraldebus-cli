import unittest
from lurraldebus_cli.matching import (
    parse_arrivals,
    normalize,
    match_municipality,
    match_stop,
)
from lurraldebus_cli.formatting import (
    format_arrivals_table,
    format_arrivals_json,
    format_municipalities_table,
    format_stops_table,
)


SAMPLE_HTML_TABLE = """<table>
<tr>
<td><b>Linea</b></td><td></td><td><b>Okupazioa</b></td><td><b>Norantza</b></td><td></td>
</tr>
<tr>
<td class="live-line-left"><p class="line-number">E21</p></td>
<td><p class="line-name">Donostiako Aireportua&gt;Hondarribia&gt;Donostia/San Sebastian</p></td>
<td><p class="line-direction"><img src="/img/ocupacion.png" title="ocupacion" alt="ocupacion" style="margin-right:10px;width: 18px;"/><span style="position: relative; top: -4px;">16</span></p></td>
<td class="line-direction">Donostia/San Sebastian</td>
<td class="live-line-time"><p><span>00 min</span></p></td>
</tr>
<tr>
<td class="live-line-left"><p class="line-number">E27</p></td>
<td><p class="line-name">Donos&gt;Pasai An&gt;Errente&gt;Oiart&gt;Hondarri&gt;Irun&gt;Hondarri(N-1)</p></td>
<td><p class="line-direction"><img src="/img/ocupacion.png" title="ocupacion" alt="ocupacion" style="margin-right:10px;width: 18px;"/><span style="position: relative; top: -4px;"> - </span></p></td>
<td class="line-direction">Hondarri(N-1)</td>
<td class="live-line-time"><p><span>10 min</span></p></td>
</tr>
<tr>
<td class="live-line-left"><p class="line-number">E01</p></td>
<td><p class="line-name">Pasaia Donibane&gt;Lezo&gt;Errenteria&gt;Donostia/San Sebastian</p></td>
<td><p class="line-direction"><img src="/img/ocupacion.png" title="ocupacion" alt="ocupacion" style="margin-right:10px;width: 18px;"/><span style="position: relative; top: -4px;">38</span></p></td>
<td class="line-direction">Donostia/San Sebastian</td>
<td class="live-line-time"><p><span>14 min</span></p></td>
</tr>
</table>"""


class TestNormalize(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(normalize("  Hello   World  "), "hello world")

    def test_case_insensitive(self):
        self.assertEqual(normalize("DONOSTIA"), "donostia")

    def test_accents_preserved(self):
        result = normalize("Donostia / San Sebastián")
        self.assertIn("sebastián", result)


class TestMatchMunicipality(unittest.TestCase):
    def test_exact_match(self):
        matches = match_municipality("Donostia / San Sebastian")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "20069")

    def test_case_insensitive(self):
        matches = match_municipality("donostia / san sebastian")
        self.assertEqual(len(matches), 1)

    def test_partial_match(self):
        matches = match_municipality("Donostia")
        self.assertTrue(len(matches) >= 1)
        self.assertTrue(any("20069" == m[0] for m in matches))

    def test_no_match(self):
        matches = match_municipality("Madrid")
        self.assertEqual(len(matches), 0)

    def test_irun(self):
        matches = match_municipality("Irun")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "20045")


class TestMatchStop(unittest.TestCase):
    def setUp(self):
        self.stops = [
            {"value": "109", "name": "109 - Donostia - Gipuzkoa plaza 10"},
            {"value": "110", "name": "110 - Donostia - Gipuzkoa plaza"},
            {"value": "130", "name": "130 - Donostia - Donostiako autobus geltokia"},
        ]

    def test_exact_number_match(self):
        matches = match_stop("109", self.stops)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "109")

    def test_partial_name_match(self):
        matches = match_stop("Gipuzkoa plaza", self.stops)
        self.assertEqual(len(matches), 2)

    def test_no_match(self):
        matches = match_stop("nonexistent", self.stops)
        self.assertEqual(len(matches), 0)


class TestParseArrivals(unittest.TestCase):
    def test_parse_sample(self):
        arrivals = parse_arrivals(SAMPLE_HTML_TABLE)
        self.assertEqual(len(arrivals), 3)

    def test_first_arrival(self):
        arrivals = parse_arrivals(SAMPLE_HTML_TABLE)
        self.assertEqual(arrivals[0]["line_number"], "E21")
        self.assertEqual(arrivals[0]["direction"], "Donostia/San Sebastian")
        self.assertEqual(arrivals[0]["time"], "00 min")
        self.assertEqual(arrivals[0]["occupancy"], "16")

    def test_second_arrival(self):
        arrivals = parse_arrivals(SAMPLE_HTML_TABLE)
        self.assertEqual(arrivals[1]["line_number"], "E27")
        self.assertEqual(arrivals[1]["direction"], "Hondarri(N-1)")
        self.assertEqual(arrivals[1]["time"], "10 min")
        self.assertEqual(arrivals[1]["occupancy"], "-")

    def test_third_arrival(self):
        arrivals = parse_arrivals(SAMPLE_HTML_TABLE)
        self.assertEqual(arrivals[2]["line_number"], "E01")
        self.assertEqual(arrivals[2]["occupancy"], "38")

    def test_empty_html(self):
        arrivals = parse_arrivals("<html></html>")
        self.assertEqual(arrivals, [])

    def test_no_table(self):
        arrivals = parse_arrivals("<div>no table here</div>")
        self.assertEqual(arrivals, [])


class TestFormatting(unittest.TestCase):
    def test_arrivals_table_no_results(self):
        result = format_arrivals_table([])
        self.assertIn("No live arrivals found", result)

    def test_arrivals_table_with_data(self):
        arrivals = [{"line_number": "E21", "direction": "Test", "time": "05 min", "occupancy": "10"}]
        result = format_arrivals_table(arrivals)
        self.assertIn("E21", result)
        self.assertIn("Test", result)

    def test_arrivals_json(self):
        arrivals = [{"line_number": "E21", "line_name": "Route", "direction": "Dest", "time": "05 min", "occupancy": "10"}]
        import json
        result = format_arrivals_json(arrivals, "Test Stop", "109", "20069")
        parsed = json.loads(result)
        self.assertEqual(parsed["stop_name"], "Test Stop")
        self.assertEqual(len(parsed["arrivals"]), 1)
        self.assertEqual(parsed["arrivals"][0]["line"], "E21")

    def test_municipalities_table(self):
        m = {"20069": "Donostia / San Sebastian", "20045": "Irun"}
        result = format_municipalities_table(m)
        self.assertIn("Donostia", result)
        self.assertIn("Irun", result)

    def test_stops_table(self):
        stops = [{"name": "Stop A", "value": "1"}, {"name": "Stop B", "value": "2"}]
        result = format_stops_table(stops)
        self.assertIn("Stop A", result)
        self.assertIn("Stop B", result)


if __name__ == "__main__":
    unittest.main()

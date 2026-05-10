# Lurraldebus API Discovery

## Overview

The Lurraldebus website (https://lurraldebus.eus) is a CakePHP application that provides live bus arrival information for the Gipuzkoa region (Basque Country, Spain). The "Live Arrivals" feature at `/real/result` uses two backend endpoints: one JSON API for fetching bus stops by municipality, and one HTML-rendering endpoint for the live arrivals billboard.

## Website Flow

1. User opens `https://lurraldebus.eus/real/result`
2. The page contains a form with a municipality `<select>` dropdown pre-populated with all municipalities
3. When a municipality is selected, JavaScript fires an AJAX POST to fetch bus stops
4. The stops dropdown is populated from the JSON response
5. When the user selects a stop and clicks "See result", the form POSTs to `/real/result`
6. The server returns an HTML page with a `<table>` containing live arrival data

---

## Endpoint 1: Fetch Bus Stops by Municipality

**URL:** `https://lurraldebus.eus/real/ajax_get_paradas_municipio_info.json`

**Method:** `POST`

**Content-Type:** `application/x-www-form-urlencoded`

**Required Headers:** None special (standard browser headers suffice)

**Required Cookies/Tokens:** None

**Request Body:**

```
municipioId=<MUNICIPALITY_ID>
```

**Example curl:**

```bash
curl -s -X POST 'https://lurraldebus.eus/real/ajax_get_paradas_municipio_info.json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'municipioId=20069'
```

**Example Response:**

```json
{
  "status": 200,
  "data": [
    {
      "name": "1 - Donostia - Mirakruz kalea 26",
      "value": "1",
      "UTM_X": 583220,
      "UTM_Y": 4797109
    },
    {
      "name": "109 - Donostia - Gipuzkoa plaza 10",
      "value": "109",
      "UTM_X": 582557,
      "UTM_Y": 4796998
    }
  ]
}
```

**Response Fields:**

- `status`: HTTP-like status code (200 = success)
- `data[]`: Array of stop objects
  - `name`: Human-readable stop name (format: `"<stop_number> - <municipality> - <street/description>"`)
  - `value`: Stop ID (used as `paradaId` in the arrivals request)
  - `UTM_X`, `UTM_Y`: UTM coordinates (used for map display only)

---

## Endpoint 2: Fetch Live Arrivals (Billboard)

**URL:** `https://lurraldebus.eus/real/result`

**Method:** `POST`

**Content-Type:** `application/x-www-form-urlencoded`

**Required Headers:** None special

**Required Cookies/Tokens:** None

**Request Body:**

```
_method=POST&data[Real][municipioId]=<MUNICIPALITY_ID>&data[Real][paradaId]=<STOP_ID>
```

**Example curl:**

```bash
curl -s -X POST 'https://lurraldebus.eus/real/result' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d '_method=POST&data%5BReal%5D%5BmunicipioId%5D=20069&data%5BReal%5D%5BparadaId%5D=109'
```

**Response:** HTML page. The live arrivals are in a `<table>` with this structure:

```html
<table>
  <tr>
    <td><b>Linea</b></td>
    <td></td>
    <td><b>Okupazioa</b></td>
    <td><b>Norantza</b></td>
    <td></td>
  </tr>
  <tr>
    <td class="live-line-left">
      <p class="line-number">E21</p>
    </td>
    <td>
      <p class="line-name">Donostiako Aireportua>Hondarribia>Donostia/San Sebastian</p>
    </td>
    <td>
      <p class="line-direction">
        <img src="/img/ocupacion.png" .../>
        <span>16</span>
      </p>
    </td>
    <td class="line-direction">Donostia/San Sebastian</td>
    <td class="live-line-time">
      <p><span>00 min</span></p>
    </td>
  </tr>
  <!-- more rows... -->
</table>
```

**Parsed fields from HTML table:**

| Column | CSS Class / Selector | Meaning |
|--------|---------------------|---------|
| Line number | `.line-number` | Bus line identifier (e.g., "E21", "E05") |
| Line name/route | `.line-name` | Route description with stops separated by `>` |
| Occupancy | `.line-direction span` (after img) | Current bus occupancy (number or "-") |
| Direction | `td.line-direction` | Destination/terminus |
| Arrival time | `.live-line-time span` | Minutes until arrival (e.g., "00 min", "10 min") |

---

## Municipality ID Mapping

Municipality IDs are embedded in the HTML `<select>` dropdown on the initial page load. They follow a provincial pattern:

- `20xxx` = Gipuzkoa municipalities
- `48xxx` = Bizkaia municipalities  
- `01xxx` = Araba/Alava municipalities

### Complete Municipality List

| ID | Name |
|----|------|
| 20001 | Abaltzisketa |
| 20002 | Aduna |
| 20003 | Aizarnazabal |
| 20004 | Albiztur |
| 20005 | Alegia |
| 20006 | Alkiza |
| 20007 | Altzo |
| 20008 | Amezketa |
| 20009 | Andoain |
| 20010 | Anoeta |
| 20011 | Antzuola |
| 20012 | Arama |
| 20013 | Aretxabaleta |
| 20014 | Asteasu |
| 20015 | Ataun |
| 20016 | Aia |
| 20017 | Azkoitia |
| 20018 | Azpeitia |
| 20019 | Beasain |
| 20020 | Beizama |
| 20021 | Belauntza |
| 20022 | Berastegi |
| 20025 | Zegama |
| 20026 | Zerain |
| 20027 | Zestoa |
| 20028 | Zizurkil |
| 20029 | Deba |
| 20030 | Eibar |
| 20031 | Elduain |
| 20032 | Elgoibar |
| 20033 | Elgeta |
| 20034 | Eskoriatza |
| 20035 | Ezkio-Itsaso |
| 20036 | Hondarribia |
| 20037 | Gaintza |
| 20038 | Gabiria |
| 20039 | Getaria |
| 20040 | Hernani |
| 20041 | Hernialde |
| 20042 | Ibarra |
| 20043 | Idiazabal |
| 20044 | Ikaztegieta |
| 20045 | Irun |
| 20046 | Irura |
| 20047 | Itsasondo |
| 20048 | Larraul |
| 20049 | Lazkao |
| 20050 | Leaburu |
| 20051 | Legazpi |
| 20052 | Legorreta |
| 20053 | Lezo |
| 20054 | Lizartza |
| 20055 | Arrasate/Mondragon |
| 20056 | Mutriku |
| 20057 | Mutiloa |
| 20058 | Olaberria |
| 20059 | Onati |
| 20060 | Orexa |
| 20061 | Orio |
| 20062 | Ormaiztegi |
| 20063 | Oiartzun |
| 20064 | Pasaia |
| 20065 | Soraluze |
| 20066 | Errezil |
| 20067 | Errenteria |
| 20068 | Leintz-Gatzaga |
| 20069 | Donostia / San Sebastian |
| 20070 | Segura |
| 20071 | Tolosa |
| 20072 | Urnieta |
| 20073 | Usurbil |
| 20074 | Bergara |
| 20075 | Villabona |
| 20076 | Ordizia |
| 20077 | Urretxu |
| 20078 | Zaldibia |
| 20079 | Zarautz |
| 20080 | Zumarraga |
| 20081 | Zumaia |
| 20901 | Mendaro |
| 20902 | Lasarte-Oria |
| 20903 | Astigarraga |
| 20904 | Baliarrain |
| 20905 | Orendain |
| 20906 | Altzaga |
| 20907 | Gaztelu |
| 48001 | Abadino |
| 48003 | Amorebieta-Etxano |
| 48018 | Berriatua |
| 48020 | Bilbao |
| 48027 | Durango |
| 48032 | Elorrio |
| 48034 | Ermua |
| 48057 | Lekeitio |
| 48058 | Mallabia |
| 48073 | Ondarroa |
| 48091 | Atxondo |
| 48095 | Zaldibar |
| 01059 | Vitoria-Gasteiz |

Additional IDs with sub-stops:
- `20036N01` = Donostiako Aireportua / Aeropuerto de San Sebastian
- `48903N01` = Bilboko Aireportua / Aeropuerto de Bilbao
- `01008` = Arratzua-ubarrundia (with sub-stops `01008N01`-`01008N05`)

---

## Notes

- No authentication, CSRF tokens, or session cookies are required for any endpoint.
- The site is built with CakePHP (evident from `_method` hidden inputs and `data[Model][field]` naming convention).
- There is no JSON API for the live arrivals billboard — it only returns HTML that must be parsed.
- The `/real/result.json` endpoint exists but returns an internal error.
- Bus occupancy data may show `-` when not available.
- Arrival times are shown in minutes (e.g., "00 min" = arriving now).

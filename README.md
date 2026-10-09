# Starting behind, slowing down

FIT3179 Data Visualisation 2 · Divieleisch Ranjan · 35213949

How Australian children arrive at school (Australian Early Development Census 2009–2024) and how their
movement, screen time, sleep and diet change as they grow (ABS National Nutrition and Physical Activity Survey 2023).

## Structure

| Path | What it is |
|---|---|
| `index.html` | The web page |
| `js/*.vg.json` | One Vega-Lite specification per chart (13) |
| `data/*.csv` | Cleaned data, one file per chart group |
| `data/aus_lga.topojson` | Council boundaries (objects: `lga`, `states`; key: `properties.LGA_CODE24`) |
| `data/hex_grid.geojson` | ~100 km hexagons used by the bin map (key: `properties.hex_id`) |
| `raw/` | The original AEDC and ABS spreadsheets |
| `scripts/build_data.py` | Converts the spreadsheets in `raw/` into the files in `data/` |

To rebuild the data, run `python3 scripts/build_data.py` from the repo root with the original spreadsheets in `raw/`
(needs `openpyxl` and `pyproj`). It prints check values for each file.

## Charts

1. Choropleth map with city zoom panels and an area menu: % vulnerable by council, 2024
2. Proportional symbol map with year slider: number of vulnerable children, 2009–2024
3. Hexagon bin map: change in % vulnerable 2021 → 2024, ~100 km hexagons
4. Box plot with council dots: spread within each state, 2024
5. Heatmap: % on track on all five domains, state × year
6. Small multiples (line charts): % vulnerable in each area of development, 2009–2024
7. Dumbbell chart: most vs least disadvantaged areas, by state, 2024
8. Isotype (pictogram grids): children meeting all 24-hour movement guidelines, by age
8b. Arrow chart with sex toggle: % meeting each guideline, ages 5–8 to 15–17
9. Butterfly chart with sex toggle: daily activity vs screen time, by age
10. Bubble grid: screen devices in the bedroom, by age
10b. Diverging stacked bar: sleep quality, by age
11. Bullet charts with error bars: saturated fat and free sugars vs recommended limits

## Data files

| File | Source | Charts |
|---|---|---|
| `aedc_lga.csv` | AEDC by council, 2009–2024 (with `hex_id`) | 2, 3, 4 |
| `aedc_lga_domains.csv` | AEDC by council, 2024, each area of development | 1 |
| `aedc_states.csv` | AEDC state summary indicators | 5 |
| `aedc_domains_national.csv` | AEDC national % vulnerable per area | 6 |
| `aedc_seifa.csv` | AEDC by socio-economic quintile | 7 |
| `nnpas_guidelines.csv` | ABS NNPAS tables 2.3–2.4 | 8, 8b |
| `nnpas_activity_screens.csv` | ABS NNPAS table 5.1 | 9 |
| `nnpas_bedroom_devices.csv`, `nnpas_sleep_quality.csv` | ABS NNPAS table 12.3 | 10, 10b |
| `nnpas_nutrients.csv` | ABS NNPAS food and nutrients tables 2.1–2.2 | 11 |

## Sources (CC BY 4.0)

- Australian Early Development Census, Australian Government Department of Education — aedc.gov.au
- National Nutrition and Physical Activity Survey 2023, Australian Bureau of Statistics — abs.gov.au
- Local Government Areas 2024, ABS ASGS Edition 3 (simplified with mapshaper)
- Guideline limits: NHMRC Nutrient Reference Values for Australia and New Zealand; WHO Guideline: Sugars intake for adults and children (2015)

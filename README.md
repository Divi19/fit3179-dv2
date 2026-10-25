# Starting behind, slowing down

FIT3179 Data Visualisation 2 · Divieleisch Ranjan · 35213949

How Australian children arrive at school (Australian Early Development Census 2009–2024) and how their
movement, screen time, sleep and diet change as they grow (ABS National Nutrition and Physical Activity Survey 2023).

## Structure

| Path | What it is |
|---|---|
| `index.html` | The web page |
| `js/*.vg.json` | One Vega-Lite specification per chart (15), plus the two class of 24 figures |
| `img/` | The school photo (Unsplash, recoloured as a duotone) |
| `data/*.csv` | Cleaned data, one file per chart group |
| `data/aus_lga.topojson` | Council boundaries (objects: `lga`, `states`; key: `properties.LGA_CODE24`) |
| `data/hex_grid.geojson` | ~100 km hexagons used by the bin map (key: `properties.hex_id`) |
| `raw/` | The original AEDC and ABS spreadsheets |
| `scripts/build_data.py` | Converts the spreadsheets in `raw/` into the files in `data/` |

To rebuild the data, run `python3 scripts/build_data.py` from the repo root with the original spreadsheets in `raw/`
(needs `openpyxl` and `pyproj`). It prints check values for each file.

## Page design

The page follows one school day as the children grow. It opens on a dawn sky where eight children walk to school and one carries a rust backpack (1 in 8), followed by a class of 24 figure. Part A (the census) runs through warm daylight bands joined by hill and rooftop edges, with chapter 2 as a night band in the middle. Part B (the survey) opens on a plain sunset gradient, and its charts are recoloured to sit straight on the night bands. Chapter 4 splits in two: movement on navy, then a lighter dusk band, "Screens at bedtime", for the bedroom devices and sleep charts. The page closes on a night sky with a single lit phone screen. The banner scenes are kept deliberately sparse to avoid chartjunk; they and the band edges are inline SVG drawn for the page.

Headings use Gloock and everything else, charts included, uses Source Sans 3. Rust (`#d0571b`, glowing `#ff8a4c` on dark) marks the census and worse outcomes; blue (`#0a74c4`, glowing `#4fa8ec` on dark) marks the survey and better outcomes; gold (`#f2b84b`) carries the closing line of each section on dark. A sticky ruler at the top shows the age in view: age 5 in Part A, ages 2 to 17 in Part B.

## Charts

Class of 24. Pictogram: the 2024 intake as one class of 24 (and again as 24 teenagers in the summary)
0. 100% stacked bar with year toggle: vulnerable, at risk and on track in each area of development, 2009 vs 2024
1. Choropleth map with city zoom panels and an area menu: % vulnerable by council, 2024
2. Proportional symbol map with year slider, play button, city zoom and a linked national bar chart: number of vulnerable children, 2009–2024
3. Hexagon bin map: change in % vulnerable 2021 → 2024, ~100 km hexagons
4. Box plot with council dots and named councils: spread within each state, 2024
5. Heatmap coloured by change since the previous collection (significance in tooltips): % on track in all five areas, state × year
6. Small multiples (line charts): % vulnerable in each area of development, 2009–2024
7. Dumbbell chart with stacked 2009 and 2024 lanes and a year switch: most vs least disadvantaged areas, by state, 2009 and 2024
Bridge. Donut rings (small multiples) with legend highlight: how a 24-hour day is split, by age
8. Isotype (pictogram grids): children meeting all 24-hour movement guidelines, by age
8b. Arrow chart with sex toggle: % meeting each guideline, ages 5–8 to 15–17
9. Butterfly chart with sex toggle: daily activity vs screen time, by age
10. Bubble grid: screen devices in the bedroom, by age
10b. Diverging stacked bar: sleep quality, by age
11. Bullet charts with error bars: saturated fat and free sugars vs recommended limits

## Data files

| File | Source | Charts |
|---|---|---|
| `aedc_categories_national.csv` | AEDC national on track / at risk / vulnerable, 2009 and 2024 | 0 |
| `aedc_lga.csv` | AEDC by council, 2009–2024 (with `hex_id`) | 2, 3, 4 |
| `aedc_lga_domains.csv` | AEDC by council, 2024, each area of development | 1 |
| `aedc_states.csv` | AEDC state summary indicators, significance flags and an Australia row | 2, 5 |
| `aedc_domains_national.csv` | AEDC national % vulnerable per area | 6 |
| `aedc_seifa.csv` | AEDC by socio-economic quintile, 2009, 2021 and 2024 | 7 |
| `nnpas_day.csv` | ABS NNPAS tables 4.1 and 5.1 | Day rings |
| `nnpas_guidelines.csv` | ABS NNPAS tables 2.3–2.4 | 8, 8b |
| `nnpas_activity_screens.csv` | ABS NNPAS tables 5.1–5.2 (with RSEs) | 9 |
| `nnpas_bedroom_devices.csv`, `nnpas_sleep_quality.csv` | ABS NNPAS tables 12.3–12.4 (with margins of error) | 10, 10b |
| `nnpas_nutrients.csv` | ABS NNPAS food and nutrients tables 2.1–2.2 | 11 |

## Images

- Children walking to school: note thanun, Unsplash License
- Child with a tablet at night: Helena Lopes, Unsplash License

## Sources (CC BY 4.0)

- Australian Early Development Census, Australian Government Department of Education, aedc.gov.au
- National Nutrition and Physical Activity Survey 2023, Australian Bureau of Statistics, abs.gov.au
- Local Government Areas 2024, ABS ASGS Edition 3 (simplified with mapshaper)
- Guideline limits: NHMRC Nutrient Reference Values for Australia and New Zealand; WHO Guideline: Sugars intake for adults and children (2015)

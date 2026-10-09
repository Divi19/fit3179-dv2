# Starting behind, slowing down

FIT3179 Data Visualisation 2 · Divieleisch Ranjan · 35213949

How Australian children arrive at school (Australian Early Development Census 2009–2024) and how their
movement, screen time, sleep and diet change as they grow (ABS National Nutrition and Physical Activity Survey 2023).

## Structure

| Path | What it is |
|---|---|
| `index.html` | The web page |
| `js/*.vg.json` | One Vega-Lite specification per chart (11) |
| `data/*.csv` | Cleaned data, one file per chart group |
| `data/aus_lga.topojson` | Council boundaries (objects: `lga`, `states`; key: `properties.LGA_CODE24`) |
| `scripts/build_data.py` | Converts the original AEDC and ABS spreadsheets into the CSVs |

## Charts

1. Choropleth map: % vulnerable on 1+ domains by council, 2024
2. Proportional symbol map with year slider: number of vulnerable children, 2009–2024
3. Bin map: change in % vulnerable 2021 → 2024, 2° grid squares
4. Box plot with council dots: spread within each state, 2024
5. Heatmap: % on track on all five domains, state × year
6. Slope chart: % vulnerable by domain, 2021 → 2024
7. Dumbbell chart: most vs least disadvantaged areas, by state, 2024
8. Waffle chart (small multiples): children meeting the activity guideline, by age
9. Butterfly chart: daily activity minutes, boys vs girls, by age
10. Connected scatterplot: screens before bed vs sleep, by age
11. Bullet chart: % of energy from free sugars vs WHO limit

## Sources (CC BY 4.0)

- Australian Early Development Census, Australian Government Department of Education — aedc.gov.au
- National Nutrition and Physical Activity Survey 2023, Australian Bureau of Statistics — abs.gov.au
- Local Government Areas 2024, ABS ASGS Edition 3 (simplified with mapshaper)

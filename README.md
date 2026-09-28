# CodeAlpha Task 3 — Global Development Data Visualization

A portfolio-ready data visualization project built for the CodeAlpha Data Analytics internship.

## Project goal

Use real country-year data to communicate how **wealth, population, and life expectancy** changed across the world between 1952 and 2007.

## Questions answered

1. How did average life expectancy change across continents?
2. Which continents experienced the largest GDP-per-capita growth?
3. How is GDP per capita related to life expectancy in 2007?
4. How did population size change by continent?

## Visual deliverables

- `outputs/dashboard.html` — interactive Plotly dashboard with hover, zoom, legend filters, and an animated GDP/life-expectancy view.
- `outputs/01_life_expectancy_by_continent.png` — trend small multiples.
- `outputs/02_gdp_growth_by_continent.png` — GDP-per-capita growth.
- `outputs/03_gdp_vs_life_expectancy_2007.png` — bubble scatterplot.
- `outputs/04_population_by_continent.png` — population trend.

## Dataset

Source: [Plotly Gapminder dataset](https://github.com/plotly/datasets/blob/master/gapminderDataFiveYear.csv), originally compiled from Gapminder World. The dataset contains 1,704 observations across 142 countries and six variables: country, continent, year, life expectancy, population, GDP per capita.

The downloaded source file is retained at `data/gapminder.csv` for reproducibility.

## How to run

```bash
pip install -r requirements.txt
python src/create_visualizations.py
```

Then open `outputs/dashboard.html` in a browser.

## Key findings

- Life expectancy increased across all continents from 1952 to 2007, with the strongest absolute levels in Europe and Oceania.
- Asia and Africa show substantial long-run gains, although Africa remains lower in 2007 than the other continents in this dataset.
- The 2007 bubble chart shows a clear positive relationship between GDP per capita and life expectancy, with important within-continent variation.
- Asia became the dominant population center by a wide margin, while all continents grew over the period.

## Limitations

- GDP per capita is reported in 2005 US dollars and is not adjusted here for purchasing-power parity.
- Country averages can hide substantial inequality within countries and continents.
- Correlation in the scatterplot does not establish causation.
- Gapminder data ends in 2007, so the dashboard is intentionally historical rather than a current-status dashboard.

## Suggested GitHub repository name

`CodeAlpha_DataVisualization`

## Permanent website

Live dashboard: https://gdevviz-eoq9fzj8.manus.space

The deployable website source is in [`website/`](website/). The main interactive dashboard is [`website/index.html`](website/index.html).


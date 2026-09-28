from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

DATA_URL = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
DATA_PATH = DATA_DIR / "gapminder.csv"

sns.set_theme(style="whitegrid", context="talk")
PALETTE = {
    "Africa": "#E76F51",
    "Americas": "#2A9D8F",
    "Asia": "#457B9D",
    "Europe": "#8E6C8A",
    "Oceania": "#F4A261",
}


def load_data():
    if not DATA_PATH.exists():
        df = pd.read_csv(DATA_URL)
        df.to_csv(DATA_PATH, index=False)
    else:
        df = pd.read_csv(DATA_PATH)
    df["year"] = df["year"].astype(int)
    return df


def savefig(name):
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / name, dpi=180, bbox_inches="tight")
    plt.close()


def make_static_charts(df):
    # 1. Life expectancy trend
    continent_avg = df.groupby(["year", "continent"], as_index=False)["lifeExp"].mean()
    fig, ax = plt.subplots(figsize=(12, 7))
    for continent, part in continent_avg.groupby("continent"):
        ax.plot(part["year"], part["lifeExp"], marker="o", linewidth=3,
                label=continent, color=PALETTE[continent])
    ax.set_title("Life expectancy rose across every continent", loc="left", weight="bold", pad=18)
    ax.set_xlabel("Year")
    ax.set_ylabel("Average life expectancy (years)")
    ax.legend(title="Continent", frameon=True)
    ax.text(0, -0.16, "Source: Gapminder World via Plotly | Country averages are weighted equally.",
            transform=ax.transAxes, fontsize=10, color="#666666")
    savefig("01_life_expectancy_by_continent.png")

    # 2. GDP growth (log scale makes cross-continent comparison clearer)
    gdp_avg = df.groupby(["year", "continent"], as_index=False)["gdpPercap"].mean()
    fig, ax = plt.subplots(figsize=(12, 7))
    for continent, part in gdp_avg.groupby("continent"):
        ax.plot(part["year"], part["gdpPercap"], marker="o", linewidth=3,
                label=continent, color=PALETTE[continent])
    ax.set_yscale("log")
    ax.set_title("GDP per capita expanded unevenly across continents", loc="left", weight="bold", pad=18)
    ax.set_xlabel("Year")
    ax.set_ylabel("Average GDP per capita (2005 USD, log scale)")
    ax.legend(title="Continent", frameon=True)
    ax.text(0, -0.16, "Log scale highlights relative growth while preserving all continents on one view.",
            transform=ax.transAxes, fontsize=10, color="#666666")
    savefig("02_gdp_growth_by_continent.png")

    # 3. 2007 relationship scatter
    latest = df[df["year"] == 2007].copy()
    fig, ax = plt.subplots(figsize=(12, 7))
    for continent, part in latest.groupby("continent"):
        ax.scatter(part["gdpPercap"], part["lifeExp"], s=part["pop"] / 2.5e5,
                   alpha=0.7, edgecolor="white", linewidth=0.7, label=continent,
                   color=PALETTE[continent])
    x = latest["gdpPercap"].to_numpy()
    y = latest["lifeExp"].to_numpy()
    slope, intercept = np.polyfit(np.log10(x), y, 1)
    xs = np.geomspace(x.min(), x.max(), 100)
    ax.plot(xs, slope * np.log10(xs) + intercept, color="#222222", linestyle="--", linewidth=2,
            label="Log-linear trend")
    corr = latest[["gdpPercap", "lifeExp"]].corr().iloc[0, 1]
    ax.set_xscale("log")
    ax.set_title(f"Higher GDP per capita aligned with longer lives in 2007 (r = {corr:.2f})",
                 loc="left", weight="bold", pad=18)
    ax.set_xlabel("GDP per capita (2005 USD, log scale)")
    ax.set_ylabel("Life expectancy (years)")
    ax.legend(title="Continent", frameon=True)
    ax.text(0, -0.16, "Bubble size represents population. Association is descriptive, not causal.",
            transform=ax.transAxes, fontsize=10, color="#666666")
    savefig("03_gdp_vs_life_expectancy_2007.png")

    # 4. Population trend
    pop_sum = df.groupby(["year", "continent"], as_index=False)["pop"].sum()
    fig, ax = plt.subplots(figsize=(12, 7))
    for continent, part in pop_sum.groupby("continent"):
        ax.plot(part["year"], part["pop"] / 1e9, marker="o", linewidth=3,
                label=continent, color=PALETTE[continent])
    ax.set_title("Asia remained the population center of gravity", loc="left", weight="bold", pad=18)
    ax.set_xlabel("Year")
    ax.set_ylabel("Population (billions)")
    ax.legend(title="Continent", frameon=True)
    ax.text(0, -0.16, "Population is the sum of country populations in each continent-year.",
            transform=ax.transAxes, fontsize=10, color="#666666")
    savefig("04_population_by_continent.png")


def make_dashboard(df):
    latest = df[df["year"] == 2007].copy()
    continent_avg = df.groupby(["year", "continent"], as_index=False).agg(
        lifeExp=("lifeExp", "mean"), gdpPercap=("gdpPercap", "mean"), pop=("pop", "sum")
    )

    fig1 = px.line(continent_avg, x="year", y="lifeExp", color="continent", markers=True,
                   color_discrete_map=PALETTE, title="Average life expectancy by continent")
    fig1.update_layout(template="plotly_white", height=430, legend_title="Continent",
                       yaxis_title="Years", xaxis_title="")

    fig2 = px.line(continent_avg, x="year", y="gdpPercap", color="continent", markers=True,
                   color_discrete_map=PALETTE, title="Average GDP per capita by continent")
    fig2.update_layout(template="plotly_white", height=430, yaxis_type="log",
                       legend_title="Continent", yaxis_title="2005 USD (log scale)", xaxis_title="")

    fig3 = px.scatter(latest, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                      hover_name="country", log_x=True, color_discrete_map=PALETTE,
                      animation_frame="year", size_max=55,
                      title="GDP per capita and life expectancy — 2007")
    fig3.update_layout(template="plotly_white", height=500, legend_title="Continent",
                       xaxis_title="GDP per capita (2005 USD, log scale)", yaxis_title="Life expectancy (years)")

    fig4 = px.area(continent_avg, x="year", y="pop", color="continent",
                   color_discrete_map=PALETTE, title="Population by continent")
    fig4.update_layout(template="plotly_white", height=430, legend_title="Continent",
                       yaxis_title="Population", xaxis_title="")

    cards = {
        "countries": int(df["country"].nunique()),
        "observations": int(len(df)),
        "year_range": f"{df['year'].min()}–{df['year'].max()}",
        "latest_life": f"{latest['lifeExp'].mean():.1f} years",
    }
    divs = [fig.to_html(full_html=False, include_plotlyjs=(i == 0)) for i, fig in enumerate([fig1, fig2, fig3, fig4])]
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Global Development Data Story</title>
<style>
body{{margin:0;background:#f5f7fb;color:#172033;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif}}
.wrap{{max-width:1400px;margin:auto;padding:34px 28px 56px}} .hero{{background:#172033;color:#fff;border-radius:22px;padding:36px 42px;margin-bottom:22px}}
h1{{font-size:clamp(30px,5vw,52px);margin:0 0 10px;letter-spacing:-1px}} .hero p{{max-width:780px;color:#d9e2f2;font-size:17px;line-height:1.55}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:20px 0 26px}} .card{{background:#fff;border-radius:16px;padding:18px 20px;box-shadow:0 5px 20px #17203312}} .label{{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#6d7890}} .value{{font-size:28px;font-weight:750;margin-top:5px}}
.chart{{background:#fff;border-radius:16px;margin:18px 0;padding:10px;box-shadow:0 5px 20px #17203312}} .footer{{color:#6d7890;font-size:13px;margin-top:28px}}
@media(max-width:900px){{.grid{{grid-template-columns:repeat(2,1fr)}}}} @media(max-width:600px){{.grid{{grid-template-columns:1fr}} .hero{{padding:26px}}}}
</style></head><body><main class="wrap">
<section class="hero"><div class="label" style="color:#9fc5ff">CODEALPHA · TASK 3</div><h1>Global Development Data Story</h1><p>How wealth, population, and life expectancy changed across the world from 1952 to 2007. Use the chart controls to filter continents, zoom, and inspect countries.</p></section>
<section class="grid"><div class="card"><div class="label">Countries</div><div class="value">{cards['countries']}</div></div><div class="card"><div class="label">Observations</div><div class="value">{cards['observations']:,}</div></div><div class="card"><div class="label">Time span</div><div class="value">{cards['year_range']}</div></div><div class="card"><div class="label">Avg life expectancy in 2007</div><div class="value">{cards['latest_life']}</div></div></section>
<div class="chart">{divs[0]}</div><div class="chart">{divs[1]}</div><div class="chart">{divs[2]}</div><div class="chart">{divs[3]}</div>
<p class="footer"><strong>Source:</strong> Gapminder World via Plotly datasets. GDP per capita is in 2005 US dollars. Visualizations are descriptive and do not establish causality.</p>
</main></body></html>'''
    (OUTPUT_DIR / "dashboard.html").write_text(html, encoding="utf-8")


def main():
    df = load_data()
    make_static_charts(df)
    make_dashboard(df)
    print(f"Generated visualizations in {OUTPUT_DIR}")
    print(f"Rows: {len(df):,} | Countries: {df['country'].nunique()} | Years: {df['year'].min()}–{df['year'].max()}")


if __name__ == "__main__":
    main()

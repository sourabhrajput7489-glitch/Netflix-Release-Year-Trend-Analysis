
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import darsh as da

st.set_page_config(
    page_title="Netflix Release Year Trend Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Netflix Release Year Trend Analysis")
st.caption("Task 4 | Time Series Analysis • Growth Tracking • Historical Insights")

@st.cache_data
def load_data():
    path = Path(__file__).resolve().parent / "data" / "Cleaned_Netflix.csv"
    data = pd.read_csv(path)

    data["release_year"] = pd.to_numeric(
        data["release_year"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["release_year", "show_id", "type"]
    ).copy()

    data["release_year"] = data["release_year"].astype(int)

    data = data.drop_duplicates(subset=["show_id"])

    return data


df = load_data()

st.sidebar.header("Dashboard Filters")

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())

year_range = st.sidebar.slider(
    "Select Release Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(max(min_year, 1990), max_year)
)

content_type = st.sidebar.selectbox(
    "Select Content Type",
    ["All", "Movie", "TV Show"]
)

top_n = st.sidebar.slider(
    "Top Release Years",
    min_value=5,
    max_value=20,
    value=10
)

filtered_df = df[
    df["release_year"].between(year_range[0], year_range[1])
].copy()

if content_type != "All":
    filtered_df = filtered_df[
        filtered_df["type"] == content_type
    ]

if filtered_df.empty:
    st.warning("No records found for selected filters.")
    st.stop()

yearly_count = (
    filtered_df.groupby("release_year")["show_id"]
    .nunique()
    .sort_index()
)

yearly_type = (
    filtered_df.groupby(["release_year", "type"])["show_id"]
    .nunique()
    .reset_index(name="total_titles")
)

yearly_comparison = (
    yearly_type.pivot(
        index="release_year",
        columns="type",
        values="total_titles"
    )
    .fillna(0)
    .reindex(
        range(year_range[0], year_range[1] + 1),
        fill_value=0
    )
)

yearly_comparison.index.name = "release_year"

yearly_full = yearly_count.reindex(
    range(year_range[0], year_range[1] + 1),
    fill_value=0
)

growth_df = yearly_full.reset_index()
growth_df.columns = ["release_year", "total_titles"]

growth_df["growth_percent"] = (
    growth_df["total_titles"]
    .pct_change(fill_method=None)
    .mul(100)
)

growth_df.loc[
    growth_df["total_titles"].shift(1).eq(0),
    "growth_percent"
] = float("nan")

total_titles = filtered_df["show_id"].nunique()

movies = filtered_df.loc[
    filtered_df["type"] == "Movie", "show_id"
].nunique()

tv_shows = filtered_df.loc[
    filtered_df["type"] == "TV Show", "show_id"
].nunique()

peak_year = int(yearly_count.idxmax())
peak_titles = int(yearly_count.max())

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Titles", f"{total_titles:,}")
c2.metric("Movies", f"{movies:,}")
c3.metric("TV Shows", f"{tv_shows:,}")
c4.metric("Peak Release Year", peak_year)

st.info(
    f"Peak Year: {peak_year} | "
    f"Titles Released: {peak_titles:,}"
)

st.divider()

st.subheader("📈 Netflix Yearly Release Trend")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    yearly_full.index,
    yearly_full.values,
    color="#E50914",
    marker="o",
    markersize=3,
    linewidth=2
)

ax.set_title("Netflix Content by Release Year")
ax.set_xlabel("Release Year")
ax.set_ylabel("Number of Titles")
ax.grid(alpha=0.3)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()

st.subheader("🎬 Movies vs TV Shows Yearly Comparison")

fig, ax = plt.subplots(figsize=(12, 5))

for column in yearly_comparison.columns:
    ax.plot(
        yearly_comparison.index,
        yearly_comparison[column],
        marker="o",
        markersize=3,
        label=column
    )

ax.set_xlabel("Release Year")
ax.set_ylabel("Total Titles")
ax.set_title("Movies and TV Shows Release Trends")
ax.legend()
ax.grid(alpha=0.3)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()

st.subheader("📊 Year-over-Year Growth Analysis")

growth_chart = growth_df.dropna(
    subset=["growth_percent"]
)

if not growth_chart.empty:
    colors = [
        "green" if value >= 0 else "red"
        for value in growth_chart["growth_percent"]
    ]

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.bar(
        growth_chart["release_year"],
        growth_chart["growth_percent"],
        color=colors
    )

    ax.axhline(0, color="black", linewidth=1)
    ax.set_xlabel("Release Year")
    ax.set_ylabel("Growth (%)")
    ax.set_title("Year-over-Year Growth and Decline")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("Not enough consecutive yearly data to calculate growth.")

st.caption(
    "Growth is undefined when the previous year's title count is zero."
)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("🏆 Top Release Years")

    ranking = (
        yearly_count.sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    ranking.columns = ["Release Year", "Total Titles"]
    ranking.index += 1

    st.dataframe(
        ranking,
        use_container_width=True,
        height=360
    )

with right:
    st.subheader("🥧 Movies vs TV Shows")

    type_count = (
        filtered_df.groupby("type")["show_id"]
        .nunique()
    )

    fig, ax = plt.subplots(figsize=(6, 5))

    ax.pie(
        type_count.values,
        labels=type_count.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Content Type Distribution")

    st.pyplot(fig)
    plt.close(fig)

st.divider()

st.subheader("🌐 Darsh 3D Release Year Analysis")

st.write(
    "3D Scatter: release_year vs type_code vs total_titles"
)

df_3d = yearly_type.copy()

df_3d["type_code"] = df_3d["type"].map({
    "Movie": 0,
    "TV Show": 1
})

try:
    chart = da.scatter_3d(
        df_3d,
        x="release_year",
        y="type_code",
        z="total_titles"
    )

    if chart is not None and hasattr(chart, "to_plotly_json"):
        st.plotly_chart(
            chart,
            use_container_width=True
        )

    elif chart is not None and hasattr(chart, "to_html"):
        import streamlit.components.v1 as components

        components.html(
            chart.to_html(
                full_html=False,
                include_plotlyjs=True
            ),
            height=650
        )

    else:
        st.warning(
            "Darsh did not return an embeddable figure."
        )
        st.dataframe(df_3d, hide_index=True)

except Exception as error:
    st.error(f"Darsh 3D chart error: {error}")

with st.expander("Content Type Codes"):
    st.write("0 = Movie")
    st.write("1 = TV Show")

st.divider()

st.subheader("💡 Business Insights")

st.success(
    f"{peak_year} has the highest number of releases "
    f"with {peak_titles:,} titles in the selected data."
)

if movies > tv_shows:
    st.write("Movies dominate the selected release-year data.")
elif tv_shows > movies:
    st.write("TV Shows dominate the selected release-year data.")
else:
    st.write("Movies and TV Shows have equal counts.")

valid_growth = growth_df.dropna(
    subset=["growth_percent"]
)

if not valid_growth.empty:
    best_growth = valid_growth.loc[
        valid_growth["growth_percent"].idxmax()
    ]

    st.info(
        f"Highest yearly growth: "
        f"{int(best_growth['release_year'])} "
        f"({best_growth['growth_percent']:.2f}%)."
    )

    declining_years = valid_growth[
        valid_growth["growth_percent"] < 0
    ]

    st.write(
        f"Years with negative growth: "
        f"{len(declining_years)}"
    )

st.caption(
    "Release year refers to the original release of each title. "
    "These trends do not directly measure Netflix platform additions "
    "or Netflix-produced originals."
)

st.divider()

st.subheader("📥 Download Analysis Reports")

download1, download2 = st.columns(2)

with download1:
    st.download_button(
        "Download Yearly Content Analysis",
        data=yearly_type.to_csv(index=False),
        file_name="Yearly_Content_Analysis.csv",
        mime="text/csv"
    )

with download2:
    st.download_button(
        "Download Yearly Growth Analysis",
        data=growth_df.to_csv(index=False),
        file_name="Yearly_Growth_Analysis.csv",
        mime="text/csv"
    )

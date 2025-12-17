import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="3D In-Vitro Lead Qualification Dashboard",
    layout="wide"
)

st.title("3D In-Vitro Lead Qualification Dashboard")
st.write(
    "This dashboard ranks life-science professionals based on their "
    "probability of working with 3D in-vitro models."
)

df = pd.read_csv("data.csv")
df.columns = df.columns.str.strip().str.lower()

def calculate_score(row):
    score = 0

    if any(x in row["title"] for x in ["Director", "Head", "VP"]):
        score += 30

    if row["published_dili_paper"] == "Yes":
        score += 40

    funding_scores = {
        "Series A": 15,
        "Series B": 20,
        "Series C": 20,
        "IPO": 25
    }
    score += funding_scores.get(row["funding_stage"], 0)

    if row["uses_invitro"] == "Yes":
        score += 15

    if row["open_to_nams"] == "Yes":
        score += 10

    hubs = ["Boston", "Cambridge", "Basel", "Bay Area", "UK Golden Triangle"]
    if any(hub in row["hq_location"] for hub in hubs):
        score += 10

    return min(score, 100)

df["probability_score"] = df.apply(calculate_score, axis=1)
df = df.sort_values("probability_score", ascending=False).reset_index(drop=True)
df["rank"] = df.index + 1

st.sidebar.header("Filters")
min_score = st.sidebar.slider("Minimum Probability Score", 0, 100, 0)

filtered_df = df[df["probability_score"] >= min_score]

st.dataframe(
    filtered_df[
        [
            "rank",
            "probability_score",
            "name",
            "title",
            "company",
            "person_location",
            "hq_location",
            "funding_stage"
        ]
    ],
    use_container_width=True
)


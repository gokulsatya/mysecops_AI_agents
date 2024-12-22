import streamlit as st
import json
import pandas as pd

# Load data from JSON files
def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Convert JSON data to Pandas DataFrame
def json_to_dataframe(json_data):
    return pd.DataFrame(json_data)

# Visualize threat scores
def visualize_threat_scores(df):
    st.subheader("Threat Score Distribution")
    score_counts = df["threat_score"].value_counts()
    st.bar_chart(score_counts)

# Display full table of results
def display_full_table(df):
    st.subheader("Full TTP Mappings and Threat Scores")
    st.dataframe(df)

# Add filtering options
def add_filters(df):
    st.sidebar.header("Filters")
    threat_level = st.sidebar.multiselect("Select Threat Score", df["threat_score"].unique())
    if threat_level:
        return df[df["threat_score"].isin(threat_level)]
    return df

# Main dashboard logic
def main():
    st.title("SECOPS AI Agents Dashboard")

    # Load enriched data
    data = load_data("data/ttp_mappings_with_scores.json")
    df = json_to_dataframe(data)

    # Add filters
    filtered_df = add_filters(df)

    # Display visualizations
    visualize_threat_scores(filtered_df)

    # Display full table
    display_full_table(filtered_df)

if __name__ == "__main__":
    main()

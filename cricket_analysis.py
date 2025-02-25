import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load both CSV files (ODI and T20)
df_odi_batter = pd.read_csv("batsman data odi.csv")
df_t20_batter = pd.read_csv("batsman data t20i.csv")
df_odi_bowler = pd.read_csv("bowler data odi.csv")
df_t20_bowler = pd.read_csv("bowler data t20i.csv")
df_odi_wicketkeeper = pd.read_csv("wicketkeeper data odi.csv")
df_t20_wicketkeeper = pd.read_csv("wicketkeeper data t20i.csv")

# Data Cleaning
def clean_data(df, numeric_columns):
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=numeric_columns)

# Clean data for batters, bowlers, and wicketkeepers
batter_numeric_columns = ["Matches", "Played", "Runs", "Batting Average", "Balls Faced", "Strike Rate"]
bowler_numeric_columns = ["Matches", "Played", "Overs", "Maiden Overs", "Runs", "Wickets", "Bowling Average", "Economy Rate", "Strike Rate"]
wicketkeeper_numeric_columns = ["Matches", "Played", "Dismissals", "Catches", "Stumpings"]

df_odi_batter = clean_data(df_odi_batter, batter_numeric_columns)
df_t20_batter = clean_data(df_t20_batter, batter_numeric_columns)
df_odi_bowler = clean_data(df_odi_bowler, bowler_numeric_columns)
df_t20_bowler = clean_data(df_t20_bowler, bowler_numeric_columns)
df_odi_wicketkeeper = clean_data(df_odi_wicketkeeper, wicketkeeper_numeric_columns)
df_t20_wicketkeeper = clean_data(df_t20_wicketkeeper, wicketkeeper_numeric_columns)

# Streamlit UI
st.title("Cricket Player Statistics")

# Dropdowns for format and player type
format_option = st.selectbox("Select Format:", ['ODI', 'T20'])
player_type = st.selectbox("Select Player Type:", ['Batters', 'Bowlers', 'Wicket Keepers'])

# Criteria dropdowns based on player type
if player_type == 'Batters':
    criteria = st.selectbox("Batters Criteria:", ['Runs', 'Batting Average', 'Strike Rate'])
elif player_type == 'Bowlers':
    criteria = st.selectbox("Bowlers Criteria:", ['Wickets', 'Bowling Average', 'Economy Rate'])
else:
    criteria = st.selectbox("Wicket Keepers Criteria:", ['Dismissals', 'Catches', 'Stumpings'])

min_matches = st.number_input("Minimum Matches Played:", min_value=0, value=0)

# Function to display top players based on selected criteria
def display_top_players(criteria, player_type, min_matches=0):
    if player_type == 'Batters':
        df_cleaned = df_odi_batter if format_option == 'ODI' else df_t20_batter
        if criteria == 'Runs':
            top_players = df_cleaned[df_cleaned["Matches"] >= min_matches].nlargest(10, "Runs")[["Player Name", "Country", "Runs", "Batting Average", "Strike Rate"]]
        elif criteria == 'Batting Average':
            top_players = df_cleaned[df_cleaned["Matches"] >= min_matches].nlargest(10, "Batting Average")[["Player Name", "Country", "Batting Average", "Matches"]]
        elif criteria == 'Strike Rate':
            top_players = df_cleaned[df_cleaned["Matches"] >= min_matches].nlargest(10, "Strike Rate")[["Player Name", "Country", "Strike Rate", "Runs"]]
        
        st.write(f"**Top 10 Batters by {criteria}:**")
        st.dataframe(top_players)
    
    elif player_type == 'Bowlers':
        df_cleaned = df_odi_bowler if format_option == 'ODI' else df_t20_bowler
        if criteria == 'Wickets':
            top_players = df_cleaned[df_cleaned["Matches"] >= min_matches].nlargest(10, "Wickets")[["Player Name", "Country", "Wickets", "Best Figure", "Bowling Average"]]
        elif criteria == 'Bowling Average':
            top_players = df_cleaned[df_cleaned["Matches"] >= min_matches].nlargest(10, "Bowling Average")[["Player Name", "Country", "Bowling Average", "Matches"]]
        elif criteria == 'Economy Rate':
            top_players = df_cleaned[df_cleaned["Matches"] >= min_matches].nsmallest(10, "Economy Rate")[["Player Name", "Country", "Economy Rate", "Wickets"]]
        
        st.write(f"**Top 10 Bowlers by {criteria}:**")
        st.dataframe(top_players)

    elif player_type == 'Wicket Keepers':
        df_cleaned = df_odi_wicketkeeper if format_option == 'ODI' else df_t20_wicketkeeper
        if criteria == 'Dismissals':
            top_players = df_cleaned[df_cleaned["Matches"] >= min_matches].nlargest(10, "Dismissals")[["Player Name", "Country", "Dismissals", "Catches", "Stumpings"]]
        elif criteria == 'Catches':
            top_players = df_cleaned[df_cleaned["Matches"] >= min_matches].nlargest(10, "Catches")[["Player Name", "Country", "Catches", "Dismissals", "Stumpings"]]
        elif criteria == 'Stumpings':
            top_players = df_cleaned[df_cleaned["Matches"] >= min_matches].nlargest(10, "Stumpings")[["Player Name", "Country", "Stumpings", "Dismissals", "Catches"]]
        
        st.write(f"**Top 10 Wicket Keepers by {criteria}:**")
        st.dataframe(top_players)

# Function to plot graphs based on selected criteria
def plot_graph(criteria, player_type):
    plt.figure(figsize=(10, 6))
    
    if player_type == 'Batters':
        df_cleaned = df_odi_batter if format_option == 'ODI' else df_t20_batter
        if criteria == 'Runs':
            top_run_scorers = df_cleaned.nlargest(10, "Runs")[["Player Name", "Runs"]]
            sns.barplot(x="Runs", y="Player Name", data=top_run_scorers, palette="Blues_d")
            plt.title("Top 10 Batters by Runs")
            plt.xlabel("Runs")
            plt.ylabel("Player Name")
        elif criteria == 'Strike Rate vs Runs':
            sns.scatterplot(x="Runs", y="Strike Rate", data=df_cleaned, hue="Country", palette="Set1")
            plt.title("Strike Rate vs Runs")
            plt.xlabel("Runs")
            plt.ylabel("Strike Rate")
        elif criteria == 'Distribution of Batting Averages':
            sns.boxplot(data=df_cleaned["Batting Average"], palette="Set2")
            plt.title("Distribution of Batting Averages")
    
    elif player_type == 'Bowlers':
        df_cleaned = df_odi_bowler if format_option == 'ODI' else df_t20_bowler
        if criteria == 'Wickets':
            top_wicket_takers = df_cleaned.nlargest(10, "Wickets")[["Player Name", "Wickets"]]
            sns.barplot(x="Wickets", y="Player Name", data=top_wicket_takers, palette="Greens_d")
            plt.title("Top 10 Bowlers by Wickets")
            plt.xlabel("Wickets")
            plt.ylabel("Player Name")
        elif criteria == 'Economy Rate vs Wickets':
            sns.scatterplot(x="Wickets", y="Economy Rate", data=df_cleaned, hue="Country", palette="Set2")
            plt.title("Economy Rate vs Wickets")
            plt.xlabel("Wickets")
            plt.ylabel("Economy Rate")
    
    elif player_type == 'Wicket Keepers':
        df_cleaned = df_odi_wicketkeeper if format_option == 'ODI' else df_t20_wicketkeeper
        if criteria == 'Dismissals':
            top_wicketkeepers = df_cleaned.nlargest(10, "Dismissals")[["Player Name", "Dismissals"]]
            sns.barplot(x="Dismissals", y="Player Name", data=top_wicketkeepers, palette="Oranges_d")
            plt.title("Top 10 Wicket Keepers by Dismissals")
            plt.xlabel("Dismissals")
            plt.ylabel("Player Name")
        elif criteria == 'Catches vs Stumpings':
            sns.scatterplot(x="Catches", y="Stumpings", data=df_cleaned, hue="Country", palette="Set3")
            plt.title("Catches vs Stumpings")
            plt.xlabel("Catches")
            plt.ylabel("Stumpings")

    plt.tight_layout()  # Adjust layout to fit everything
    st.pyplot(plt)  # Display the plot in Streamlit

# Display top players and plot graph based on button clicks
if st.button("Display Top Players"):
    display_top_players(criteria, player_type, min_matches)

if st.button("Plot Graph"):
    plot_graph(criteria, player_type)
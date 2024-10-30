import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from PIL import Image
import os

# Set up the page with a consistent color theme and page-wide layout
st.set_page_config(page_title="Crop Health Dashboard", layout="wide")
st.sidebar.header("Control Options 🌱")  # Sidebar for selections and filters

# CSS for font adjustments
st.markdown("""
    <style>
        h1 {text-align: center; color: #2E8B57; font-size: 36px;}
        h2 {color: #2E8B57; font-size: 24px;}
    </style>
""", unsafe_allow_html=True)
st.markdown("<h1>🌿 Crop Health Dashboard 🌿</h1>", unsafe_allow_html=True)

# Paths to data files
index_data_path = 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/OneDrive_2024-10-24_CeresImaging/Ceres Imaging/Index/Zonal_stats/MeanST_NDVIxMCARI2.xlsx'
management_data_path = 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/Management/Management/2024_TAPS_management_1.xlsx'
image_paths = {
    "NDVI": {
        "2024-06-17": 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/OneDrive_2024-10-24_CeresImaging/Ceres Imaging/Index/Heatmaps/NDVI_2024-06-17.png',
        "2024-07-09": 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/OneDrive_2024-10-24_CeresImaging/Ceres Imaging/Index/Heatmaps/NDVI_2024-07-09.png',
        "2024-07-25": 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/OneDrive_2024-10-24_CeresImaging/Ceres Imaging/Index/Heatmaps/NDVI_2024-07-25.png',
        "2024-08-15": 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/OneDrive_2024-10-24_CeresImaging/Ceres Imaging/Index/Heatmaps/NDVI_2024-08-15.png',
        "2024-08-30": 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/OneDrive_2024-10-24_CeresImaging/Ceres Imaging/Index/Heatmaps/NDVI_2024-08-30.png',
    },
    "MCARI2": {
        "2024-06-17": 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/OneDrive_2024-10-24_CeresImaging/Ceres Imaging/Index/Heatmaps/MCARI2_2024-06-17.png',
        "2024-07-09": 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/OneDrive_2024-10-24_CeresImaging/Ceres Imaging/Index/Heatmaps/MCARI2_2024-07-09.png',
        "2024-07-25": 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/OneDrive_2024-10-24_CeresImaging/Ceres Imaging/Index/Heatmaps/MCARI2_2024-07-25.png',
        "2024-08-15": 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/OneDrive_2024-10-24_CeresImaging/Ceres Imaging/Index/Heatmaps/MCARI2_2024-08-15.png',
        "2024-08-30": 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/OneDrive_2024-10-24_CeresImaging/Ceres Imaging/Index/Heatmaps/MCARI2_2024-08-30.png',
    }
}

# Sidebar options for selection
st.sidebar.write("### Select Options")
analysis_type = st.sidebar.radio("Analysis Type", ["Team-Based", "Plot-Based"])
index_type = st.sidebar.radio("Index Type", ["NDVI", "MCARI2"], help="Select the index to analyze crop health.")

# Data Loading with expanders
with st.sidebar.expander("Data Loading Options"):
    ndvi_df = pd.read_excel(index_data_path, sheet_name="Mean_NDVI")
    mcari2_df = pd.read_excel(index_data_path, sheet_name="Mean_MCARI2")
    nitrogen_df = pd.read_excel(management_data_path, sheet_name="Nitrogen fertilizer")
    irrigation_df = pd.read_excel(management_data_path, sheet_name="Irrigation amounts")
    planting_date_df = pd.read_excel(management_data_path, sheet_name="Planting Date")

# Display tabs for Zonal Statistics and Heatmap Visualization
tab1, tab2 = st.tabs(["Zonal Statistics 📊", "Heatmap Visualization 🌍"])

# Zonal Statistics Tab
with tab1:
    st.markdown("<h2>Zonal Statistics Analysis</h2>", unsafe_allow_html=True)
    st.markdown("""
        <p style='color: #555; font-size: 14px;'>
        Explore trends and health indicators for crops across different teams and plots over time.
        <br>**Note:** Data values used here for analysis are averaged from plots within the same team (for Team-Based) 
        or shown individually (for Plot-Based).</p>
    """, unsafe_allow_html=True)

    # Index DataFrame Selection
    data_df = ndvi_df if index_type == "NDVI" else mcari2_df

    # Team-Based Analysis
    if analysis_type == "Team-Based":
        teams = data_df["Team_ID"].unique()
        selected_teams = st.sidebar.multiselect("Select Team(s)", options=teams, default=teams[0])

        # Sidebar controls for threshold
        threshold = st.sidebar.number_input(f"{index_type} Threshold", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key="threshold")
        
        # Management data overlay options
        plot_options = st.sidebar.multiselect("Select Management Data to Overlay", ["Nitrogen fertilizer", "Irrigation amounts"])

        # Columns for better layout structure
        col1, col2 = st.columns([1, 2])
        with col1:
            if selected_teams:
                # Team and Plot Summary
                st.write("### Team and Plot Summary")
                team_data_summary = data_df[data_df["Team_ID"].isin(selected_teams)]
                st.write(team_data_summary[["Team_ID", "PLOT_ID"]].drop_duplicates().sort_values("Team_ID"))

                # Summary Table
                summary_table = pd.DataFrame()
                for team_id in selected_teams:
                    team_data = team_data_summary[team_data_summary["Team_ID"] == team_id]
                    team_means = team_data.drop(columns=["Team_ID"]).groupby("PLOT_ID").mean()
                    daily_mean = team_means.mean(axis=0).rename(team_id)
                    summary_table = pd.concat([summary_table, daily_mean], axis=1)

                summary_table = summary_table.T
                summary_table.index.name = "Team_ID"
                summary_table.columns = pd.to_datetime(summary_table.columns).strftime('%Y-%m-%d')
                st.write(f"### {index_type} Summary Table")
                st.write(summary_table)
        
        with col2:
            # Time Series Plot with Management Data Overlays
            time_series_data = summary_table.reset_index().melt(id_vars="Team_ID", var_name="Date", value_name="Mean Value")
            time_series_data["Date"] = pd.to_datetime(time_series_data["Date"])

            fig = px.line(time_series_data, x="Date", y="Mean Value", color="Team_ID", title=f"{index_type} Mean Values Over Time")
            fig.update_traces(mode="lines+markers", hoverinfo="text")
            fig.update_layout(transition_duration=500)

            # Add threshold line and management overlays
            fig.add_shape(type="line", x0=time_series_data["Date"].min(), y0=threshold, x1=time_series_data["Date"].max(), y1=threshold,
                          line=dict(color="Red", width=2, dash="dash"))

            # Overlay Nitrogen and Irrigation data for each team separately
            if "Nitrogen fertilizer" in plot_options or "Irrigation amounts" in plot_options:
                nitrogen_data = nitrogen_df[nitrogen_df["Team_ID"].isin(selected_teams)].copy()
                irrigation_data = irrigation_df[irrigation_df["Team_ID"].isin(selected_teams)].copy()
                nitrogen_data = nitrogen_data.melt(id_vars=["Team_ID"], var_name="Date", value_name="Nitrogen (lbs/acre)")
                irrigation_data = irrigation_data.melt(id_vars=["Team_ID"], var_name="Date", value_name="Irrigation (inches)")

                for team_id in selected_teams:
                    team_nitrogen = nitrogen_data[nitrogen_data["Team_ID"] == team_id]
                    team_irrigation = irrigation_data[irrigation_data["Team_ID"] == team_id]

                    if "Nitrogen fertilizer" in plot_options:
                        fig.add_trace(go.Bar(x=team_nitrogen["Date"], y=team_nitrogen["Nitrogen (lbs/acre)"],
                                             name=f"Nitrogen (Team {team_id})", yaxis="y2", opacity=0.6))
                    if "Irrigation amounts" in plot_options:
                        fig.add_trace(go.Bar(x=team_irrigation["Date"], y=team_irrigation["Irrigation (inches)"],
                                             name=f"Irrigation (Team {team_id})", yaxis="y2", opacity=0.6))

            fig.update_layout(yaxis2=dict(title="Management Data", overlaying="y", side="right"))
            st.plotly_chart(fig)
            
        # Plot-Based Analysis
    elif analysis_type == "Plot-Based":
        plots = data_df["PLOT_ID"].unique()
        selected_plots = st.sidebar.multiselect("Select Plot(s)", options=plots, default=plots[0])

        if selected_plots:
            plot_data = data_df[data_df["PLOT_ID"].isin(selected_plots)]
            plot_data_long = plot_data.melt(id_vars=["Team_ID", "PLOT_ID"], var_name="Date", value_name="Mean Value")
            plot_data_long["Date"] = pd.to_datetime(plot_data_long["Date"]).dt.date
            filtered_data = plot_data_long[plot_data_long["PLOT_ID"].isin(selected_plots)]
            fig = px.line(filtered_data, x="Date", y="Mean Value", color="PLOT_ID", title=f"{index_type} Mean Values for Selected Plot(s)")
            fig.update_layout(transition_duration=500)
            st.plotly_chart(fig)

# Heatmap Visualization Tab
with tab2:
    st.markdown("<h2>Heatmap Visualization</h2>", unsafe_allow_html=True)

    date = st.sidebar.selectbox("Select Date", ["2024-06-17", "2024-07-09", "2024-07-25", "2024-08-15", "2024-08-30"])
    st.markdown(f"<h3>{index_type} Heatmap on {date}</h3>", unsafe_allow_html=True)
    if index_type == "NDVI":
        st.markdown("""
            **NDVI (Normalized Difference Vegetation Index)**: A key indicator of crop health where higher values
            indicate healthier vegetation. It ranges from -1 to 1 and uses near-infrared and red bands to calculate vegetation vigor.
        """)
    elif index_type == "MCARI2":
        st.markdown("""
            **MCARI2 (Modified Chlorophyll Absorption in Reflectance Index 2)**: Used to assess chlorophyll content and photosynthetic capacity of plants, indicating crop health.
        """)

    image_path = image_paths[index_type][date]
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption=f"{index_type} on {date}", use_column_width=True)
    else:
        st.error(f"Image for {index_type} on {date} not found.")

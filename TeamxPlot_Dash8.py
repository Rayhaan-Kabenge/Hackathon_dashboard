import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.express as px


# Title for the Dashboard
st.title('Time Series Analysis Dashboard')

# Paths to data files
index_data_path = 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/OneDrive_2024-10-24_CeresImaging/Ceres Imaging/Index/Zonal_stats/MeanST_NDVIxMCARI2.xlsx'
management_data_path = 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Unzipped data/Management/Management/2024_TAPS_management_1.xlsx'

# Load the index data from both sheets
ndvi_df = pd.read_excel(index_data_path, sheet_name="Mean_NDVI")
mcari2_df = pd.read_excel(index_data_path, sheet_name="Mean_MCARI2")

# Load management data
nitrogen_df = pd.read_excel(management_data_path, sheet_name="Nitrogen fertilizer")
irrigation_df = pd.read_excel(management_data_path, sheet_name="Irrigation amounts")
planting_date_df = pd.read_excel(management_data_path, sheet_name="Planting Date")

# Create Tabs for the Time Series Analysis
selected_tab = st.radio("Select Analysis Type:", ["Team-Based", "Plot-Based"], index=0)

if selected_tab == "Team-Based":
    st.markdown("**Team-Based Analysis:** Select one or more teams to see a summary of the plots and calculated mean values.")

    # Select the index type
    index_type = st.radio("Select Index", options=["NDVI", "MCARI2"])

    # Choose the appropriate DataFrame
    data_df = ndvi_df if index_type == "NDVI" else mcari2_df

    # Extract unique teams
    teams = data_df["Team_ID"].unique()
    selected_teams = st.multiselect("Select Team(s)", options=teams, default=teams[0])

    if selected_teams:
        # Filter data for the selected teams
        selected_team_data = data_df[data_df["Team_ID"].isin(selected_teams)]

        # Display table with plots under each team
        plot_summary_table = selected_team_data[["Team_ID", "PLOT_ID"]].drop_duplicates().sort_values("Team_ID")
        st.write("### Plots Available per Selected Team(s)")
        st.write(plot_summary_table.style.format({'PLOT_ID': '{:g}'}))  # Remove comma formatting for Plot_ID

        # Create an empty DataFrame to store mean values for each team and date
        summary_table = pd.DataFrame()

        # Loop over each team to calculate the mean for each date
        for team_id in selected_teams:
            team_data = selected_team_data[selected_team_data["Team_ID"] == team_id]
            team_means = team_data.drop(columns=["Team_ID"]).groupby("PLOT_ID").mean()
            daily_mean = team_means.mean(axis=0).rename(team_id)  # Daily mean across plots
            summary_table = pd.concat([summary_table, daily_mean], axis=1)

        # Transpose and set headers for easier reading
        summary_table = summary_table.T
        summary_table.index.name = "Team_ID"

        # Format column headers as dates without time component
        summary_table.columns = pd.to_datetime(summary_table.columns).strftime('%Y-%m-%d')

        # Display the summary table
        st.write(f"### Summary of {index_type} Values for Selected Team(s)")
        st.write(summary_table)

        # Reshape the data for time series plotting
        time_series_data = summary_table.reset_index().melt(id_vars="Team_ID", 
                                                            var_name="Date", 
                                                            value_name="Mean Value")
        time_series_data["Date"] = pd.to_datetime(time_series_data["Date"])

        # Load and prepare Nitrogen and Irrigation data
        nitrogen_data = nitrogen_df[nitrogen_df["Team_ID"].isin(selected_teams)].copy()
        irrigation_data = irrigation_df[irrigation_df["Team_ID"].isin(selected_teams)].copy()

        # Adjust nitrogen data for "Variable" application date
        variable_nitrogen = nitrogen_data[nitrogen_data["Variable"].notna()]
        for team_id in variable_nitrogen["Team_ID"].unique():
            planting_date = planting_date_df.loc[planting_date_df["Team_ID"] == team_id, "Date"].values[0]
            nitrogen_data.loc[(nitrogen_data["Team_ID"] == team_id) & (nitrogen_data["Variable"].notna()), "Variable"] = planting_date

        nitrogen_data = nitrogen_data.melt(id_vars=["Team_ID"], 
                                           value_vars=[col for col in nitrogen_data.columns if col not in ["Team_ID", "Variable"]],
                                           var_name="Date", 
                                           value_name="Nitrogen (lbs/acre)")
        irrigation_data = irrigation_data.melt(id_vars=["Team_ID"], 
                                               var_name="Date", 
                                               value_name="Irrigation (inches)")

        # Convert dates to datetime
        nitrogen_data["Date"] = pd.to_datetime(nitrogen_data["Date"], errors='coerce')
        irrigation_data["Date"] = pd.to_datetime(irrigation_data["Date"], errors='coerce')

        # Plot selection
        plot_options = st.multiselect("Select Management Data to Plot", options=["Nitrogen fertilizer", "Irrigation amounts"])

        # Create a larger dual-axis plot for time series and management data with improved visibility
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.update_layout(width=1200, height=600)

        # Add the index mean line plot
        for team_id in selected_teams:
            team_data = time_series_data[time_series_data["Team_ID"] == team_id]
            fig.add_trace(
                go.Scatter(x=team_data["Date"], y=team_data["Mean Value"], mode="lines+markers", name=f"{index_type} Mean (Team {team_id})"),
                secondary_y=False
            )

        # Add nitrogen and irrigation as grouped bar graphs for each team if selected
        if "Nitrogen fertilizer" in plot_options:
            for team_id in selected_teams:
                team_nitrogen = nitrogen_data[nitrogen_data["Team_ID"] == team_id]
                fig.add_trace(
                    go.Bar(x=team_nitrogen["Date"], y=team_nitrogen["Nitrogen (lbs/acre)"], name=f"Nitrogen (Team {team_id})", opacity=0.6),
                    secondary_y=True
                )

        if "Irrigation amounts" in plot_options:
            for team_id in selected_teams:
                team_irrigation = irrigation_data[irrigation_data["Team_ID"] == team_id]
                fig.add_trace(
                    go.Bar(x=team_irrigation["Date"], y=team_irrigation["Irrigation (inches)"], name=f"Irrigation (Team {team_id})", opacity=0.6),
                    secondary_y=True
                )

        # Set y-axis titles and formatting
        fig.update_yaxes(title_text=f"{index_type} Mean", secondary_y=False)
        fig.update_yaxes(title_text="Nitrogen (lbs/acre) / Irrigation (inches)", secondary_y=True)

        # Set layout details
        fig.update_layout(
            title_text=f"Time Series of {index_type} Mean Values with Management Data for Selected Team(s)",
            barmode="group",  # Group the bars by team
            xaxis_title="Date",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        # Display the interactive plot
        st.plotly_chart(fig)

        # Show the contour plot if both Nitrogen and Irrigation are selected
        if "Nitrogen fertilizer" in plot_options and "Irrigation amounts" in plot_options:
            # Calculate cumulative Nitrogen and Irrigation per team
            cumulative_nitrogen = nitrogen_data.groupby("Team_ID")["Nitrogen (lbs/acre)"].sum()
            cumulative_irrigation = irrigation_data.groupby("Team_ID")["Irrigation (inches)"].sum()
            
            # Use cumulative values and mean NDVI per team for contour plot
            contour_data = pd.DataFrame({
                "Cumulative Nitrogen": cumulative_nitrogen,
                "Cumulative Irrigation": cumulative_irrigation,
                "Mean NDVI": summary_table.mean(axis=1)  # Using the mean NDVI across dates per team
            }).reset_index()

            # Create contour plot
            fig_contour = go.Figure(data=go.Contour(
                x=contour_data["Cumulative Nitrogen"],
                y=contour_data["Cumulative Irrigation"],
                z=contour_data["Mean NDVI"],
                colorscale="Viridis",
                colorbar_title="NDVI"
            ))

            fig_contour.update_layout(
                title="Contour Plot of NDVI vs Cumulative Nitrogen and Irrigation",
                xaxis_title="Cumulative Nitrogen (lbs/acre)",
                yaxis_title="Cumulative Irrigation (inches)",
                width=800,
                height=600
            )

            # Display the contour plot
            st.plotly_chart(fig_contour)

    else:
        st.write("Please select at least one team to display the summary and time series.")

elif selected_tab == "Plot-Based":
    st.markdown("**Plot-Based Analysis:** The information displayed in this tab is on an individual plot basis, providing detailed trends for each of the plots assigned to a given team.")

    # User selects the index type
    index_type = st.radio("Select Index", options=["NDVI", "MCARI2"])

    # Select the correct DataFrame based on index type
    data_df = ndvi_df if index_type == "NDVI" else mcari2_df

    # Extract available plot IDs
    available_plots = data_df["PLOT_ID"].unique()
    
    # Multi-select for plots
    selected_plots = st.multiselect("Select Plot(s)", options=available_plots, default=available_plots[0])

    if selected_plots:
        # Filter data for the selected plots
        plot_data = data_df[data_df["PLOT_ID"].isin(selected_plots)]

        # Reshape data to long format for plotting
        plot_data_long = plot_data.melt(id_vars=["Team_ID", "PLOT_ID"], 
                                        var_name="Date", 
                                        value_name="Mean Value")
        
        # Convert date column to datetime format for proper sorting
        plot_data_long["Date"] = pd.to_datetime(plot_data_long["Date"]).dt.date  # Remove time component

        # Filter only selected plots for display
        filtered_data = plot_data_long[plot_data_long["PLOT_ID"].isin(selected_plots)]

        # Create interactive plot
        fig = px.line(filtered_data, x="Date", y="Mean Value", color="PLOT_ID",
                      title=f"{index_type} Mean Values for Selected Plot(s)",
                      labels={"Mean Value": f"{index_type} Mean"})
        
        # Display the interactive plot
        st.plotly_chart(fig)
    else:
        st.write("Please select at least one plot to display the time series.")

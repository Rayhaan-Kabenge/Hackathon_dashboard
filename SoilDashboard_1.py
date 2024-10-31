# Import necessary libraries
import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
import plotly.express as px

# Set page configuration (must be the first Streamlit command)
st.title("Soil Status Dashboard")

# Custom CSS for overall dashboard styling
# Custom CSS for overall dashboard styling
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;  /* Main page background color set to black */
        font-family: 'Arial', sans-serif;
    }
    h1.dashboard-title {
        font-size: 60px;
        font-family: 'Renato', sans-serif;  /* Title font set to Renato */
        color: #FFFFFF;  /* White color for title to contrast with black background */
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    h1, h2, h3 {
        text-align: center;
        color: #FFFFFF;  /* White color for other headers */
    }
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
    }
    .metric {
        background-color: #333333;  /* Darker shade for metric cards */
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.5);
        color: #FFFFFF;  /* White text for metric cards */
    }
    .sidebar .sidebar-content {
        background-color: #1a1a1a;  /* Dark sidebar background */
        color: #FFFFFF;  /* White text for sidebar */
    }
    footer {
        text-align: center;
        margin-top: 20px;
        font-size: 16px;
        color: #FFFFFF;  /* White text for footer */
    }
    </style>
""", unsafe_allow_html=True)

# Set up title with updated font style
#st.markdown("<h1 class='dashboard-title'>🌿 Crop Health Dashboard 🌿</h1>", unsafe_allow_html=True)


# Add the main title with custom styling
st.markdown('<h1 class="dashboard-title">Soil Status Dashboard ⛰️</h1>', unsafe_allow_html=True)

# Sidebar configuration for marker customization
st.sidebar.header("Marker Customization")
marker_shapes = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up']
marker_shape = st.sidebar.selectbox("Select Marker Shape:", options=marker_shapes, index=0)
marker_size = st.sidebar.slider("Select Marker Size:", 4, 12, 6)

# Color Palette for Unique Line Colors
extended_color_palette = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2",
    "#7f7f7f", "#bcbd22", "#17becf", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5", "#aec7e8", "#393b79",
    "#637939", "#8c6d31", "#843c39", "#7b4173", "#5254a3", "#6b6ecf", "#b5cf6b",
    "#d6616b", "#ce6dbd", "#6baed6", "#fd8d3c", "#c7e9c0", "#9e9ac8", "#fdd0a2",
    "#e7cb94", "#9ecae1", "#a1d99b", "#dadaeb", "#fdae6b", "#c49c94", "#2ca25f",
    "#de2d26", "#3182bd", "#31a354", "#fd8d3c", "#756bb1", "#c6dbef", "#e6550d",
    "#9ecae1", "#bcbddc", "#74c476", "#99d8c9", "#6baed6", "#c7e9b4", "#756bb1",
    "#d6616b", "#c6dbef", "#e6550d", "#9ecae1", "#d9d9d9", "#8c6d31", "#843c39",
    "#7b4173", "#5254a3", "#bcbddc", "#fd8d3c", "#6baed6", "#8ca252", "#bdc9e1",
    "#ce6dbd", "#6baed6", "#fd8d3c", "#c7e9c0", "#9e9ac8", "#fdd0a2", "#e7cb94",
    "#a1d99b", "#dadaeb", "#fdae6b", "#c49c94", "#31a354", "#3182bd", "#31a354",
    "#fd8d3c", "#756bb1", "#c6dbef", "#e6550d", "#bcbddc", "#74c476", "#99d8c9",
    "#c7e9b4", "#6baed6", "#fd8d3c", "#9ecae1", "#d9d9d9", "#843c39", "#7b4173"
]

def get_unique_color(index):
    return extended_color_palette[index % len(extended_color_palette)]

# Function to customize marker, line, and general axes styling
# Function to customize marker, line, and general axes styling
def customize_axes(fig, x_label, y_label, title):
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        xaxis=dict(gridcolor="lightgrey", tickfont=dict(color='black', size=14)),
        yaxis=dict(gridcolor="lightgrey", tickfont=dict(color='black', size=14)),
        title_font=dict(size=20, color="black"),
        hovermode="x unified",
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        legend=dict(
            bgcolor="black",     # Set legend background to black
            font=dict(color="white")  # Set legend font color to white for readability
        )
    )
    fig.update_traces(
        marker=dict(size=marker_size, symbol=marker_shape, line=dict(width=1, color="black")),
    )
    return fig


# Load the dataset for moisture change analysis
file_path = 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Dashboard/Official_code/SoilDash/data/24 KSU TAPS Neutron Tube Readings_VWC.csv'
df = pd.read_csv(file_path)
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
depth_columns = [col for col in df.columns if col.startswith('V-')]

# Load TRT Plot Summary Data for Team Overview Tab
input_file_path = 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Dashboard/Official_code/SoilDash/data/TRT_Plot_Summary.xlsx'
trt_summary_df = pd.read_excel(input_file_path)
trt_summary_df.rename(columns={'TRT_ID': 'Team #', 'Plot_ID': 'Plot #', 'Block_ID': 'Block #'}, inplace=True)

# Create Tabs for Separation of Analysis Types
tab1, tab2, tab3, tab4 = st.tabs([
    "Tubes Readings", 
    "Acquaspy data (Moisture and EC)", 
    "Team and Plot Overview", 
    "Soil Moisture Prediction"
])

# Tab 1: Tubes Readings
# Tab 1: Tubes Readings
# Tab 1: Tubes Readings
# Tubes Readings Tab with Graph and Summary Table
# Tab 1: Tubes Readings
with tab1:
    st.header("Moisture Changes Over Time")

    # Filters for the Graph
    with st.sidebar.expander("Graph Filters", expanded=True):
        selected_blocks_graph = st.multiselect("Select Block(s) for Graph:", df['Block #'].unique(), key="select_blocks_graph")
        
        plot_selection_per_block = {}
        for block in selected_blocks_graph:
            plots_in_block = df[df['Block #'] == block]['Plot #'].unique()
            selected_plots = st.multiselect(f"Select Plot(s) for Block {block}:", plots_in_block, default=plots_in_block, key=f"select_plots_block_{block}")
            plot_selection_per_block[block] = selected_plots

        start_date, end_date = st.date_input(
            "Select Date Range:",
            [df['Date'].min(), df['Date'].max()],
            key="date_range_graph"
        )

        selected_depths_graph = st.multiselect("Select Depth(s) for Graph:", depth_columns, default=depth_columns, key="depths_graph")

    # Filter data based on selected blocks, plots, and depths
    filtered_df_graph = df[df['Block #'].isin(selected_blocks_graph) & df['Plot #'].isin(sum(plot_selection_per_block.values(), []))]
    filtered_df_graph = filtered_df_graph[(filtered_df_graph['Date'] >= pd.to_datetime(start_date)) & (filtered_df_graph['Date'] <= pd.to_datetime(end_date))]

    # Plotting the Graph
    st.subheader("Soil Moisture Trend Across Selected Plots and Blocks")

    x_axis_label = st.text_input("X-axis Label", "Date", key="x_axis_label_graph")
    y_axis_label = st.text_input("Y-axis Label", "Volumetric Water Content", key="y_axis_label_graph")
    chart_title = st.text_input("Chart Title", "Soil Moisture Trend Across Blocks and Plots", key="chart_title_graph")

    fig = go.Figure()
    color_index = 0  # Initialize color index for unique color assignment
    for block, plots in plot_selection_per_block.items():
        for plot in plots:
            plot_data = filtered_df_graph[(filtered_df_graph['Block #'] == block) & (filtered_df_graph['Plot #'] == plot)]
            for depth in selected_depths_graph:
                if depth in plot_data.columns:
                    fig.add_trace(go.Scatter(
                        x=plot_data['Date'],
                        y=plot_data[depth],
                        mode='lines+markers',
                        name=f'Block {block}, Plot {plot}, Depth {depth}',
                        line=dict(color=get_unique_color(color_index))  # Apply unique color here
                    ))
                    color_index += 1  # Increment to the next color for each trace

    fig = customize_axes(fig, x_axis_label, y_axis_label, chart_title)
    st.plotly_chart(fig, use_container_width=True)

    # Filters for the Summary Table
    st.subheader("Summary of Soil Moisture Extremes by Block and Depth")
    with st.sidebar.expander("Summary Table Filters", expanded=True):
        selected_blocks_summary = st.multiselect("Select Block(s) for Summary:", df['Block #'].unique(), key="select_blocks_summary")
        selected_depths_summary = st.multiselect("Select Depth(s) for Summary:", depth_columns, default=depth_columns, key="depths_summary")

    # Filter data for the summary table based on selected blocks and depths
    summary_data = []
    for block in selected_blocks_summary:
        block_data = df[df['Block #'] == block]
        for depth in selected_depths_summary:
            if depth in block_data.columns:
                max_moisture = block_data[depth].max()
                min_moisture = block_data[depth].min()
                max_plot = block_data.loc[block_data[depth].idxmax(), 'Plot #']
                min_plot = block_data.loc[block_data[depth].idxmin(), 'Plot #']
                
                summary_data.append({
                    "Block": block,
                    "Depth": depth,
                    "Max Moisture": max_moisture,
                    "Max Moisture Plot": max_plot,
                    "Min Moisture": min_moisture,
                    "Min Moisture Plot": min_plot
                })

    # Display the summary table
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        st.write("Summary Table Showing Extremes for Selected Blocks and Depths")
        st.dataframe(summary_df)
    else:
        st.write("No data available for the selected filters in the summary table.")



# Tab 2: Acquaspy data (Moisture and EC)
with tab2:
    st.header("Weekly Moisture and EC Plots")

    averaged_weekly_path = 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Dashboard/Official_code/SoilDash/data/Averaged_weekly.xlsx'
    sheets = pd.read_excel(averaged_weekly_path, sheet_name=None)

    selected_teams = st.multiselect("Select Team(s):", options=sheets.keys(), default=list(sheets.keys())[:1], key="teams_tab2")
    selected_measurements = st.multiselect("Select Measurement Type(s):", options=["Moisture", "Electrolytic Conductivity"], key="measurements_tab2")

    moisture_vars = ['MS', 'M4"', 'M8"', 'M12"', 'M16"', 'M20"', 'M24"', 'M28"', 'M32"', 'M36"', 'M40"', 'M44"', 'M48"']
    ec_vars = ['EC4"', 'EC8"', 'EC12"', 'EC16"', 'EC20"', 'EC24"', 'EC28"', 'EC32"', 'EC36"', 'EC40"', 'EC44"', 'EC48"']
    moisture_selected, ec_selected = [], []

    if "Moisture" in selected_measurements:
        moisture_selected = st.multiselect("Select Moisture Parameters:", options=moisture_vars, default=["MS"], key="moisture_params_tab2")
    if "Electrolytic Conductivity" in selected_measurements:
        ec_selected = st.multiselect("Select EC Parameters:", options=ec_vars, default=["EC4\""], key="ec_params_tab2")

    fig = go.Figure()
    for team in selected_teams:
        data = sheets[team]
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])

        for idx, parameter in enumerate(moisture_selected + ec_selected):
            if parameter in data.columns:
                fig.add_trace(go.Scatter(
                    x=data['Timestamp'],
                    y=data[parameter],
                    mode='lines+markers',
                    name=f'{parameter} - {team}',
                    line=dict(color=extended_color_palette[idx % len(extended_color_palette)])
                ))

    x_axis_label_tab2 = st.text_input("X-axis Label for Acquaspy Data", "Timestamp", key="x_axis_label_tab2")
    y_axis_label_tab2 = st.text_input("Y-axis Label for Acquaspy Data", "Measurement Values", key="y_axis_label_tab2")
    chart_title_tab2 = st.text_input("Chart Title for Acquaspy Data", "Weekly Averages of Selected Moisture and EC Parameters Across Teams", key="chart_title_tab2")

    fig = customize_axes(fig, x_axis_label_tab2, y_axis_label_tab2, chart_title_tab2)
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Team and Plot Overview with Box Plot
with tab3:
    st.header("Team and Plot Overview")

    # Team and Plot Selection
    selected_team = st.selectbox("Select Team #:", trt_summary_df['Team #'].unique(), key="select_team_tab3")
    team_data = trt_summary_df[trt_summary_df['Team #'] == selected_team]
    st.write(f"### Plots and Blocks for Team {selected_team}")
    st.dataframe(team_data[['Team #', 'Plot #', 'Block #']])

    # Plot and Depth Selection
    selected_plots = st.multiselect("Select Plot(s):", options=team_data['Plot #'].unique(), default=team_data['Plot #'].unique(), key="plots_tab3")
    selected_depths = st.multiselect("Select Depth(s):", depth_columns, default=depth_columns, key="depths_tab3")
    start_date, end_date = st.date_input("Select Date Range:", [df['Date'].min(), df['Date'].max()], key="date_range_tab3")
    filtered_df_team = df[(df['Plot #'].isin(selected_plots)) & (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

    st.subheader(f"Moisture Content Trend for Team {selected_team}")

    fig = go.Figure()
    for idx, plot in enumerate(selected_plots):
        plot_data = filtered_df_team[filtered_df_team['Plot #'] == plot]
        for depth_idx, depth in enumerate(selected_depths):
            if depth in plot_data.columns:
                fig.add_trace(go.Scatter(
                    x=plot_data['Date'],
                    y=plot_data[depth],
                    mode='lines+markers',
                    name=f'Plot {plot} - Depth {depth}',
                    line=dict(color=extended_color_palette[(idx + depth_idx) % len(extended_color_palette)])
                ))

    x_axis_label_tab3 = st.text_input("X-axis Label for Team Overview", "Date", key="x_axis_label_tab3")
    y_axis_label_tab3 = st.text_input("Y-axis Label for Team Overview", "Volumetric Water Content", key="y_axis_label_tab3")
    chart_title_tab3 = st.text_input("Chart Title for Team Overview", f"Soil Moisture Trend for Team {selected_team}", key="chart_title_tab3")

    fig = customize_axes(fig, x_axis_label_tab3, y_axis_label_tab3, chart_title_tab3)
    st.plotly_chart(fig, use_container_width=True)

    # Box Plot for Averaged Soil Moisture with Error Bars
    st.subheader("Box Plot of Averaged Soil Moisture by Team and Depth")

    # Dropdowns for Box Plot
    teams_for_boxplot = st.multiselect("Select Team(s) for Box Plot:", trt_summary_df['Team #'].unique(), default=[selected_team], key="boxplot_teams")
    depths_for_boxplot = st.multiselect("Select Depth(s) for Box Plot:", depth_columns, default=depth_columns, key="boxplot_depths")

    # Filter data for selected teams and depths, and calculate average moisture
    # Convert start_date and end_date to datetime if they are date objects
    start_date = pd.to_datetime(start_date) if isinstance(start_date, pd.Timestamp) else pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date) if isinstance(end_date, pd.Timestamp) else pd.to_datetime(end_date)

# Filter data for selected teams and depths, and calculate average moisture
    selected_team_data = df[df['Plot #'].isin(trt_summary_df[trt_summary_df['Team #'].isin(teams_for_boxplot)]['Plot #'])]
    filtered_boxplot_data = selected_team_data[selected_team_data['Date'].between(start_date, end_date)]

    selected_team_data = df[df['Plot #'].isin(trt_summary_df[trt_summary_df['Team #'].isin(teams_for_boxplot)]['Plot #'])]
    filtered_boxplot_data = selected_team_data[selected_team_data['Date'].between(start_date, end_date)]
    boxplot_data = filtered_boxplot_data.melt(id_vars=['Date', 'Plot #'], value_vars=depths_for_boxplot, var_name="Depth", value_name="Moisture Content")
    boxplot_data = boxplot_data.merge(trt_summary_df[['Team #', 'Plot #']], on='Plot #', how='left')
    boxplot_data = boxplot_data[boxplot_data['Team #'].isin(teams_for_boxplot)]

    # Plot the box plot with error bars
    box_fig = px.box(
        boxplot_data,
        x="Depth",
        y="Moisture Content",
        color="Team #",
        points="all",
        title="Averaged Soil Moisture with Error Bars Across Teams and Depths",
    )

    # Update layout for box_fig with a black background for the legend
    box_fig.update_layout(
    xaxis_title="Soil Depth",
    yaxis_title="Averaged Soil Moisture Content",
    plot_bgcolor="#f9f9f9",
    paper_bgcolor="#f9f9f9",
    legend=dict(
        bgcolor="black",          # Black background for legend
        font=dict(color="white")  # White font color for legend text
    ),
    xaxis=dict(
        tickfont=dict(color="black"),  # Black font for x-axis
        titlefont=dict(color="black")  # Black font for x-axis title
    ),
    yaxis=dict(
        tickfont=dict(color="black"),  # Black font for y-axis
        titlefont=dict(color="black")  # Black font for y-axis title
    )
)
    



    st.plotly_chart(box_fig, use_container_width=True)

# Tab 4: Soil Moisture Prediction
with tab4:
    st.header("Soil Moisture Prediction using Time-Series Forecasting")

    selected_depth = st.selectbox("Select Depth for Prediction:", depth_columns)
    forecast_horizon = st.slider("Select Forecast Horizon (in days):", 1, 30, 7)

    depth_data = df[['Date', selected_depth]].rename(columns={'Date': 'ds', selected_depth: 'y'})
    model = Prophet(daily_seasonality=True)
    model.fit(depth_data)
    future = model.make_future_dataframe(periods=forecast_horizon, freq='D')
    forecast = model.predict(future)

    fig_original = go.Figure()
    fig_original.add_trace(go.Scatter(x=depth_data['ds'], y=depth_data['y'], mode='lines', name='Original Data'))
    fig_original = customize_axes(fig_original, "Date", "Moisture Content", f"Moisture Content Over Time at Depth {selected_depth}")
    st.plotly_chart(fig_original, use_container_width=True)

    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecasted Data'))
    fig_forecast.add_trace(go.Scatter(x=depth_data['ds'], y=depth_data['y'], mode='lines', name='Original Data'))
    fig_forecast = customize_axes(fig_forecast, "Date", "Moisture Content", f"Forecast for Next {forecast_horizon} Days at Depth {selected_depth}")
    st.plotly_chart(fig_forecast, use_container_width=True)

    fig_intervals = go.Figure()
    fig_intervals.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecasted Moisture'))
    fig_intervals.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], fill=None, mode='lines', name='Lower Confidence Interval', line=dict(dash='dash')))
    fig_intervals.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill='tonexty', mode='lines', name='Upper Confidence Interval', line=dict(dash='dash')))
    fig_intervals = customize_axes(fig_intervals, "Date", "Moisture Content", f"Prediction Intervals for Next {forecast_horizon} Days at Depth {selected_depth}")
    st.plotly_chart(fig_intervals, use_container_width=True)

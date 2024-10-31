import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os
from PIL import Image
import base64
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os
from PIL import Image
import base64
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os
from PIL import Image
import plotly.express as px



# Set up the page configuration
st.set_page_config(
    page_title="KSUTAPS Management Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define image paths for the core module icons
logo_path = "F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Dashboard/Official_code/KSU-TAPS transparent.png"
weather_img_path = 'C:/Users/Rayhaan_Kabenge/Downloads/WD.png'
crop_health_img_path = 'C:/Users/Rayhaan_Kabenge/Downloads/CD.png'
soil_status_img_path = 'C:/Users/Rayhaan_Kabenge/Downloads/SD.png'

# Initialize session state to control page navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"  # Default to homepage

# Helper function to encode image for the homepage logo
@st.cache_data
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Function to display the Weather Dashboard
def weather_dashboard():
    # Load Data
    @st.cache_data
    def load_historical_data():
            return pd.read_csv('C:/Users/Rayhaan_Kabenge/Desktop/Hackathon data/Weather/colby_climate_1990_2019_2.csv', parse_dates=['time'])

    @st.cache_data
    def load_2024_data():
        return pd.read_csv('C:/Users/Rayhaan_Kabenge/Desktop/Hackathon data/Weather/colby_station_kansas_mesonet2.csv', parse_dates=['TIMESTAMP'])

        # Load Kc data
    kc_data_path = "F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Data/Kc_data.xlsx"
    kc_df = pd.read_excel(kc_data_path)

    # Define the path to the folder containing Kc curve images
    kc_image_folder = 'F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Dashboard/Official_code/Weather_Dash/image_Kcgraph' 

    # Define monthly 'p' values for Blaney-Criddle method
    monthly_p_values = {
        'January': 0.22, 'February': 0.24, 'March': 0.27, 'April': 0.3,
        'May': 0.32, 'June': 0.34, 'July': 0.33, 'August': 0.31,
        'September': 0.28, 'October': 0.25, 'November': 0.22, 'December': 0.21
    }

    # Define the function to calculate ETo using Blaney-Criddle
    def calculate_eto(mean_temp, p_value):
        return p_value * (0.46 * mean_temp + 8)

    # Set up the Streamlit dashboard layout

    st.title("Weather Data Dashboard 🌤️")
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Select Section", ["Historical Weather Data", "2024 Weather Data", "ETo Calculator"])

    # Load datasets
    historical_data = load_historical_data()
    weather_2024 = load_2024_data()

    # Helper function to calculate percentage change
    def calculate_percent_change(current, previous):
        if previous == 0:
            return "N/A"
        change = ((current - previous) / previous) * 100
        return round(change, 2)

    growth_stage_characteristics = {
        "Maize": {
            "Initial": ["Seedlings emerge with slender leaves", "2–6 leaves", "Rapid root growth"],
            "Mid": ["Tall stalk with broad, green leaves", "Tasseling and silking begin", "High water requirement"],
            "End": ["Kernels mature", "Leaves yellow and dry out", "Stalks begin to brown"]
        },
        "Soybean": {
            "Initial": ["Small plants with two rounded leaves", "Early nodes and branches", "Low water demand"],
            "Mid": ["Dense foliage", "Flowers and pod formation", "Increased water need"],
            "End": ["Leaves yellow and fall", "Pods mature, beans visible", "Reduced water need"]
        },
        "Wheat": {
            "Initial": ["Thin, green shoots in rows", "Upright tillering", "Low water demand"],
            "Mid": ["Taller, dense canopy", "Flowering with grain heads", "Peak water demand"],
            "End": ["Grains harden", "Plants turn golden", "Minimal water requirement"]
        },
        "Soybean": {
            "Initial": ["Small plants with two rounded leaves", "Early nodes and branches", "Low water demand"],
            "Mid": ["Dense foliage", "Flowers and pod formation", "Increased water need"],
            "End": ["Leaves yellow and fall", "Pods mature, beans visible", "Reduced water need"]
        },
        "Wheat": {
            "Initial": ["Thin, green shoots in rows", "Upright tillering", "Low water demand"],
            "Mid": ["Taller, dense canopy", "Flowering with grain heads", "Peak water demand"],
            "End": ["Grains harden", "Plants turn golden", "Minimal water requirement"]
        },
        "Cotton": {
            "Initial": ["Small, dark green leaves", "Square (bud) formation", "Low water use"],
            "Mid": ["Blooms and boll formation", "Light-green foliage", "High water requirement"],
            "End": ["Leaves drop", "Bolls open to reveal cotton lint", "Reduced water need"]
        },
        "Grapes": {
            "Initial": ["Small shoots with few leaves", "Flower clusters visible", "Low water need"],
            "Mid": ["Clusters mature", "Green grape bunches", "Moderate water demand"],
            "End": ["Grapes ripen", "Sugar accumulation in berries", "Reduced water need"]
        },
        "Sugarbeet": {
            "Initial": ["Small rosette with broad leaves", "Flat, low to the ground", "Low water requirement"],
            "Mid": ["Dense, overlapping leaves", "Root thickens underground", "Increased water demand"],
            "End": ["Foliage yellows", "Beet root fully mature", "Reduced water need"]
        },
        "Tomato": {
            "Initial": ["Small, bushy plants", "Flower buds may appear", "Moderate water need"],
            "Mid": ["Flowering and fruit set", "Green fruits form", "High water requirement"],
            "End": ["Leaves yellow", "Fruits ripen and mature color", "Water demand decreases"]
        },
        "Sunflower": {
            "Initial": ["Seedling with two large, oval leaves", "Erect growth begins", "Low water demand"],
            "Mid": ["Tall stalk", "Flower head formation", "Moderate water demand"],
            "End": ["Petals fall", "Seeds develop in the head", "Reduced water need"]
        },
        "Barley": {
            "Initial": ["Narrow shoots emerge", "Begins tillering in rows", "Moderate water demand"],
            "Mid": ["Erect, dense foliage", "Green heads form", "Peak water demand"],
            "End": ["Golden heads", "Leaves dry", "Minimal water requirement"]
        },
        "Potato": {
            "Initial": ["Low, leafy green shoots", "Compact, bushy growth", "Low water need"],
            "Mid": ["Tuber formation", "Leaf canopy expands", "High water need"],
            "End": ["Leaves yellow", "Tubers mature underground", "Water demand decreases"]
        },
        "Sorghum": {
            "Initial": ["Slender, grassy shoots", "Early tillering", "Low water demand"],
            "Mid": ["Taller, broad leaves", "Grain head forms", "High water demand"],
            "End": ["Grain heads fully formed", "Seeds ripen", "Foliage turns brown"]
        }
        # Other crop information continues here...
    }

    # Helper function to display the checklist
    def display_growth_stage_characteristics(crop, growth_stage):
        characteristics = growth_stage_characteristics.get(crop, {}).get(growth_stage, [])
        with st.expander(f"{crop} - {growth_stage} Stage Characteristics", expanded=True):
            for characteristic in characteristics:
                st.checkbox(characteristic, value=False)

    if option == "Historical Weather Data":
        st.header("Historical Weather Data (1990-2019) 📈")
        
        years = historical_data['time'].dt.year.unique()
        start_year, end_year = st.slider("Select Year Range", int(years.min()), int(years.max()), (1990, 2019))
        
        # Filter data based on year selection
        filtered_historical = historical_data[(historical_data['time'].dt.year >= start_year) & (historical_data['time'].dt.year <= end_year)]
        
        # Checkbox selection for parameters
        parameters_hist = st.multiselect("Select Parameters to Plot", 
                                        ['Precipitation', 'ETo', 'Minimum_Temperature', 'Maximum_Temperature', 'Minimum_RelativeHumidity', 'Maximum_RelativeHumidity', 'vs', 'SolarRadiation'], 
                                        default=['Precipitation', 'Maximum_Temperature'])

        if not filtered_historical.empty and parameters_hist:
            filtered_historical['year'] = filtered_historical['time'].dt.year
            historical_yearly_avg = filtered_historical.groupby('year')[parameters_hist].mean()
            
            # Plot
            fig = go.Figure()
            for param in parameters_hist:
                if param == 'Precipitation':  # Display precipitation as a bar graph
                    fig.add_trace(go.Bar(
                        x=historical_yearly_avg.index,
                        y=historical_yearly_avg[param],
                        name=param,
                        marker=dict(color='blue')
                    ))
                else:  # Line graphs for other parameters
                    fig.add_trace(go.Scatter(
                        x=historical_yearly_avg.index,
                        y=historical_yearly_avg[param],
                        mode='lines+markers',
                        name=param
                    ))
            
            fig.update_layout(
                title="Yearly Averaged Historical Weather Data",
                xaxis_title="Year",
                yaxis_title="Value",
                template="plotly_white",
                legend=dict(title="Parameters", font=dict(color="black")),  # Set legend font color
                hovermode="x unified",
                paper_bgcolor="white",
                plot_bgcolor="white",
                xaxis=dict(ticks="inside", tickcolor='grey', title_font=dict(color="black")),  # Set x-axis title font color
                yaxis=dict(ticks="inside", tickcolor='grey', title_font=dict(color="black"))   # Set y-axis title font color
            )
            
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
            
            # Hover text summary on point hover
            for param in parameters_hist:
                param_values = historical_yearly_avg[param]
                hover_texts = []
                for i in range(len(param_values)):
                    current_value = param_values.iloc[i]
                    previous_value = param_values.iloc[i-1] if i > 0 else current_value
                    percent_change = calculate_percent_change(current_value, previous_value)
                    hover_text = (
                        f"<b>{param.upper()}</b><br>"
                        f"Highest: {param_values.max()}<br>"
                        f"Lowest: {param_values.min()}<br>"
                        f"Percent Change: <span style='color: {'green' if percent_change > 0 else 'red'}'>{percent_change}%</span>"
                    )
                    hover_texts.append(hover_text)
                    
                fig.data[parameters_hist.index(param)].hovertemplate = hover_texts

            st.plotly_chart(fig)

    elif option == "2024 Weather Data":
        st.header("2024 Weather Data 📆")



        agg_type = st.radio("Select Aggregation", ["Daily", "Weekly", "Monthly"])
        
        # Checkbox selection for parameters
        parameters_2024 = st.multiselect("Select Parameters to Plot", 
                                        ['Precipitation', 'Average_Temperature', 'Minimum_Temperature', 'Maximum_Temperature', 
                                        'Average_RelativeHumidity', 'Maximum_RelativeHumidity', 'RELHMinimum_RelativeHumidityUM2MMIN', 
                                        'Average_SolarRadiation', 'Average_WindSpeed'], 
                                        default=['Precipitation', 'Maximum_Temperature'])
        
        # Aggregation function
        if agg_type == "Weekly":
            weather_2024['Week'] = weather_2024['TIMESTAMP'].dt.isocalendar().week
            weather_2024_agg = weather_2024.groupby('Week')[parameters_2024].mean()
            x_axis = weather_2024_agg.index
            x_label = "Week"
        elif agg_type == "Monthly":
            weather_2024['Month'] = weather_2024['TIMESTAMP'].dt.month_name()
            weather_2024_agg = weather_2024.groupby('Month')[parameters_2024].mean()
            x_axis = weather_2024_agg.index
            x_label = "Month"
        else:
            x_axis = weather_2024['TIMESTAMP']
            weather_2024_agg = weather_2024.set_index('TIMESTAMP')[parameters_2024]
            x_label = "Day"
        
        # Plot
        fig = make_subplots()
        for idx, param in enumerate(parameters_2024):
            color = f"hsl({idx * 40}, 70%, 50%)"  # Unique color per parameter
            if param == 'Precipitation':
                fig.add_trace(go.Bar(
                    x=x_axis,
                    y=weather_2024_agg[param],
                    name=param,
                    error_y=dict(type='data', array=weather_2024_agg[param], visible=False),
                    marker=dict(color=color)
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=x_axis,
                    y=weather_2024_agg[param],
                    mode='lines+markers',
                    name=param,
                    line=dict(color=color),
                    error_y=dict(type='data', array=weather_2024_agg[param], visible=False)
                ))

        fig.update_layout(
            title=f"2024 Weather Data - {agg_type} Averages",
            xaxis_title=x_label,
            yaxis_title="Value",
            template="plotly_white",
            legend=dict(title="Parameters", font=dict(color="black")),  # Set legend font color
            hovermode="x unified",
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(ticks="inside", tickcolor='grey', title_font=dict(color="black")),  # Set x-axis title font color
            yaxis=dict(ticks="inside", tickcolor='grey', title_font=dict(color="black"))   # Set y-axis title font color
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
        
        st.plotly_chart(fig)

    elif option == "ETo Calculator":
        st.header("ETo Calculator 🧮")

        st.markdown("""
        ### Understanding ETo (Reference Evapotranspiration)
        ETo represents the water evaporated from a reference crop surface. It helps estimate crop water needs when multiplied by the crop coefficient (Kc).
        """)

        # Option to use existing 2024 data or upload a new file
        data_source = st.radio("Choose Data Source", ("Use Existing 2024 Data", "Upload New Data File"))
        
        if data_source == "Upload New Data File":
            uploaded_file = st.file_uploader("Upload your Weather Data (Excel/CSV)", type=["csv", "xlsx"])
            
            if uploaded_file:
                if uploaded_file.name.endswith(".csv"):
                    weather_data = pd.read_csv(uploaded_file)
                else:
                    weather_data = pd.read_excel(uploaded_file)
                st.success("Weather data file uploaded successfully!")
        else:
            weather_data = weather_2024
        
        weather_data['TIMESTAMP'] = pd.to_datetime(weather_data['TIMESTAMP'], errors='coerce')
        if weather_data['TIMESTAMP'].isnull().any():
            st.error("Date parsing error in TIMESTAMP column.")
        else:
            crop_selected = st.selectbox("Select Crop", kc_df['Crop'].unique())
            crop_data = kc_df[kc_df['Crop'] == crop_selected]
            growth_stage = st.selectbox("Select Growth Stage", ["Initial", "Mid", "End"])

            # Display growth stage characteristics
            display_growth_stage_characteristics(crop_selected, growth_stage)

            # Display Kc curve image for the selected crop
            kc_image_path = os.path.join(kc_image_folder, f"{crop_selected}.png")
            if os.path.exists(kc_image_path):
                kc_image = Image.open(kc_image_path)
                st.sidebar.image(kc_image, caption=f"{crop_selected} Kc Curve", use_column_width=True)
            else:
                st.sidebar.write("No Kc curve available for this crop.")

            # Tooltip explanations in expanders
            with st.sidebar.expander("ℹ️ ETo (Reference Evapotranspiration)"):
                st.write("""
                - **Definition**: ETo represents the water evaporated and transpired by a reference crop, typically a well-watered grass. It indicates the atmospheric demand for water.
                - **Calculation**: This dashboard uses the Blaney-Criddle method, which estimates ETo based on temperature and seasonal daylight hours:
                
                **ETo = p × (0.46 × T + 8)**
                
                where:
                - **p** = mean daily percentage of annual daytime hours.
                - **T** = mean daily temperature (°C).
                - **Purpose**: Provides a baseline measure of water needed for irrigation planning.
                """)

            with st.sidebar.expander("ℹ️ Kc (Crop Coefficient)"):
                st.write("""
                - **Definition**: Kc adjusts ETo to reflect the specific water needs of a crop during its growth stages.
                - **Usage**: Varies by crop and stage (e.g., Initial, Mid, End stages), typically peaking in mid-growth.
                - **Purpose**: Helps translate ETo into practical irrigation requirements by accounting for each crop’s unique water consumption pattern.
                """)

            with st.sidebar.expander("ℹ️ ETc (Crop Water Requirement)"):
                st.write("""
                - **Definition**: ETc represents the actual water requirement of a crop, considering its growth stage and characteristics.
                - **Calculation**: **ETc = ETo × Kc**, providing the estimated water consumption specific to the crop.
                - **Purpose**: Essential for precise irrigation scheduling to optimize yield and conserve resources.
                """)
            
            st.sidebar.info("ℹ️   **Kc** values can vary based on factors like climate, soil type, and crop variety."
                            " The **Kc** graphs shown are developed using CropWat Software by FAO")    

            kc_value = crop_data[f"{growth_stage}_Kc"].values[0]
            month_selected = st.selectbox("Select Month", list(monthly_p_values.keys()))
            p_value = monthly_p_values[month_selected]
            selected_date = st.date_input("Select Date for Daily Mean Temperature")

            if 'Average_Temperature' in weather_data.columns:
                selected_data = weather_data[weather_data['TIMESTAMP'].dt.date == selected_date]
                if not selected_data.empty:
                    mean_temp = selected_data['Average_Temperature'].values[0]
                    eto_value = calculate_eto(mean_temp, p_value)
                    etc_value = eto_value * kc_value
                    st.write(f"ETo for {selected_date}: {eto_value:.2f} mm/day")
                    st.write(f"Estimated Crop Water Requirement (ETc): {etc_value:.2f} mm/day")
                else:
                    st.error("Date not found. Please try another date.")
            else:
                st.error("Data lacks 'Average_Temperature' column.")
    
    # Navigation button to go back to the homepage
    if st.button("Back to Homepage"):
        st.session_state["current_page"] = "home"  # Return to homepage

# Function to display the Crop Health Dashboard
def crop_health_dashboard():
        # Set up the page with a consistent color theme and page-wide layout
   # st.set_page_config(page_title="Crop Health Dashboard", layout="wide")
    st.title("Crop Health Dashboard")
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

    # Navigation button to go back to the homepage
    if st.button("Back to Homepage"):
        st.session_state["current_page"] = "home"  # Return to homepage

# Function to display the Soil Status Dashboard
def soil_status_dashboard():
    # Add the specific code for the Soil Status Dashboard here

    st.title("Soil Status Dashboard 🌍")
    st.write("This is the Soil Status Dashboard. Add the content for the soil status analysis here.")

    # Navigation button to go back to the homepage
    if st.button("Back to Homepage"):
        st.session_state["current_page"] = "home"  # Return to homepage

# Function to display the Homepage
def homepage():
    # Display title and logo
    st.markdown("<div style='text-align: center;'><img src='data:image/png;base64,{}' width='400'></div>".format(get_image_base64(logo_path)), unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 4em;'>KSUTAPS Management Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-size: 3.5em;'>Explore the Core Modules</h2>", unsafe_allow_html=True)

    # Core Modules arranged horizontally with images above buttons
    modules = [
        ("Weather Dashboard", "Access historical and real-time weather information to plan accordingly.", weather_img_path),
        ("Crop Health Dashboard", "Monitor crop conditions and detect potential issues early.", crop_health_img_path),
        ("Soil Status Dashboard", "Analyze soil health indicators for optimal crop growth.", soil_status_img_path)
    ]

    cols = st.columns(len(modules))
    for i, (module, description, img_path) in enumerate(modules):
        with cols[i]:
            st.image(img_path, width=300)  # Display module image
            if st.button(module, key=module, help=description):
                st.session_state["current_page"] = module  # Navigate to the respective dashboard

# Main page rendering logic
if st.session_state["current_page"] == "home":
    homepage()  # Show the homepage
elif st.session_state["current_page"] == "Weather Dashboard":
    weather_dashboard()  # Show the Weather Dashboard
elif st.session_state["current_page"] == "Crop Health Dashboard":
    crop_health_dashboard()  # Show the Crop Health Dashboard
elif st.session_state["current_page"] == "Soil Status Dashboard":
    soil_status_dashboard()  # Show the Soil Status Dashboard

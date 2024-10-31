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
import base64
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os
from PIL import Image
import plotly.express as px
import glob
import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
import plotly.express as px

# Set up the page configuration
st.set_page_config(
    page_title="KSUTAPS Management Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar starts collapsed
)

# Paths to resources
logo_path = "F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Dashboard/Official_code/KSU-TAPS transparent.png"
slideshow_folder = "F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Dashboard/Official_code/Slideshow"

# Initialize session state to control page navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"  # Default to homepage
if "show_slideshow" not in st.session_state:
    st.session_state["show_slideshow"] = False  # Sidebar slideshow state

# Optimized function to convert logo to base64 with caching
@st.cache_data
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
   # st.markdown("<div style='text-align: center;'><img src='data:image/png;base64,{}' width='400'></div>".format(logo_base64), unsafe_allow_html=True)

# Caching the encoded logo and slideshow images
logo_base64 = get_image_base64(logo_path)
image_files = sorted(glob.glob(os.path.join(slideshow_folder, "p*.png")))
slideshow_images = [get_image_base64(img_path) for img_path in image_files]

# Sidebar with Media Box button for slideshow
def toggle_slideshow():
    st.session_state["show_slideshow"] = not st.session_state["show_slideshow"]

with st.sidebar:
    if st.button("Media Box", on_click=toggle_slideshow):
        if st.session_state["show_slideshow"]:
            st.write("Image Slideshow")
            for img_base64 in slideshow_images:
                st.image(f"data:image/png;base64,{img_base64}", use_column_width=True)

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
                xaxis=dict(ticks="inside", tickcolor='grey', tickfont=dict(color="black")),  # Set x-axis title font color
                yaxis=dict(ticks="inside", tickcolor='grey', titlefont=dict(color="black"))   # Set y-axis title font color
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
    # Add the specific code for each section and functionality...

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
                
                st.markdown("### Box Plot Analysis Over Time")
        box_teams = st.multiselect("Select Teams for Box Plot", options=data_df["Team_ID"].unique(), default=data_df["Team_ID"].unique())
        box_indices = st.multiselect("Select Index for Box Plot", options=["NDVI", "MCARI2"], default=["NDVI"])

        # Initialize figure for combined box plot over time
        fig = go.Figure()

        # Loop through each index selected to gather data and add traces to a single figure
        for index in box_indices:
            # Choose the appropriate dataframe based on index selection
            index_df = ndvi_df if index == "NDVI" else mcari2_df
            box_data = index_df[index_df["Team_ID"].isin(box_teams)]
            
            # Melt data for easier use with Plotly and grouping by team and date
            box_data_long = box_data.melt(id_vars=["Team_ID", "PLOT_ID"], var_name="Date", value_name="Value")
            box_data_long["Date"] = pd.to_datetime(box_data_long["Date"]).dt.date  # Convert to date type for consistency

            # Add a box plot for each team and index type per date
            for team in box_teams:
                team_data = box_data_long[box_data_long["Team_ID"] == team]
                
                # Create box plot traces for each date within the team and index grouping
                for date in team_data["Date"].unique():
                    date_data = team_data[team_data["Date"] == date]
                    
                    # Add box plot trace for each team and index at each date
                    fig.add_trace(go.Box(
                        y=date_data["Value"],
                        name=f"{index} - Team {team} ({date})",
                        boxpoints=False,  # No individual points, just box and error bars
                        marker=dict(opacity=0.7),
                        line=dict(width=1),
                        boxmean="sd"  # Showing only min, max, and mean
                    ))

        # Dynamically set y-axis range based on min/max values in data for better visibility
        y_min = box_data_long["Value"].min() * 0.9
        y_max = box_data_long["Value"].max() * 1.1
        fig.update_yaxes(range=[y_min, y_max])

        # Layout updates for the box plot
        fig.update_layout(
            title="Box Plot of Selected Index Values by Team Over Time",
            yaxis_title="Index Value",
            xaxis_title="Date (Grouped by Team and Index Type)",
            width=1600,
            height=600,# Increased width for better box plot visibility
            showlegend=True
        )

        # Display the single box plot for all selected indices and teams over time
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
    # Add Crop Health Dashboard functionality...

    # Navigation button to go back to the homepage
    if st.button("Back to Homepage"):
        st.session_state["current_page"] = "home"  # Return to homepage

# Function to display the Soil Status Dashboard
def soil_status_dashboard():
    # Soil Status Dashboard code goes here (unchanged)
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
        forecast_horizon = st.slider("Select Forecast Horizon (in days):", 1, 90, 7)

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

    # Add Soil Status Dashboard functionality...

    # Navigation button to go back to the homepage
    if st.button("Back to Homepage"):
        st.session_state["current_page"] = "home"  # Return to homepage

# Function to display the Homepage
# Function to display the Homepage
def homepage():
    # Display title and logo centered
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        #st.image(f"data:image/png;base64,{logo_base64}", width=400)
        st.markdown("<div style='text-align: center;'><img src='data:image/png;base64,{}' width='500'></div>".format(logo_base64), unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 5.8em;'>KSUTAPS Management Dashboard</h1>", unsafe_allow_html=True)

    # Centered heading for Core Modules section
    st.markdown("<h2 style='text-align: center; font-size: 3em;'>Explore the Core Modules</h2>", unsafe_allow_html=True)

    # Core Modules arranged horizontally with descriptions below each button
    modules = [
        ("Weather Dashboard", "The Weather Dashboard delivers current and historical weather data and trend analysis, along with an ETc calculator using FAO-based Kc values, to aid in precise irrigation planning and seasonal decision-making."),
        ("Crop Health Dashboard", "The Crop Health Dashboard tracks crop condition with NDVI and MCARI2 heatmaps, enabling users to overlay irrigation and nitrogen data, analyze by team or plot, and optimize yield through data-driven insights."),
        ("Soil Status Dashboard", "The Soil Status Dashboard provides insights into soil moisture and electrical conductivity across depths and plots. Users can analyze trends, view summary statistics, and explore data by team or plot, with features for soil moisture prediction and customizable visualizations to support soil management.")
    ]

    cols = st.columns(len(modules))
    for i, (module, description) in enumerate(modules):
        with cols[i]:
            if st.button(module, key=module,  use_container_width=True):
                st.session_state["current_page"] = module
            st.markdown(f"<p style='text-align: center; font-size: 1.3em;'>{description}</p>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.write(
        """
    <div style='text-align: center; font-size: 1.3em;'>
        For more resources, tutorials, and support, visit the official 
        <a href='#'>KSUTAPS website</a> or contact us on:
        <br>
        <span style='font-size: 1.2em;'>📸 Instagram: <b>@KSU-TAPS</b>  ~|~  
        <span style='font-size: 1.2em;'> 𝕏: <b>@KSUTAPS</b></span>
        <p style='text-align: center; font-size: 1.0em;'>&copy; 2024 KSUTAPS. All rights reserved.</p>
    </div>
    """, 
    unsafe_allow_html=True
)
#st.write("<p style='text-align: center; font-size: 1.3em;'>&copy; 2024 KSUTAPS. All rights reserved.</p>", unsafe_allow_html=True)

# Main page rendering logic
if st.session_state["current_page"] == "home":
    homepage()  # Show the homepage
elif st.session_state["current_page"] == "Weather Dashboard":
    weather_dashboard()  # Show the Weather Dashboard
elif st.session_state["current_page"] == "Crop Health Dashboard":
    crop_health_dashboard()  # Show the Crop Health Dashboard
elif st.session_state["current_page"] == "Soil Status Dashboard":
    soil_status_dashboard()  # Show the Soil Status Dashboard

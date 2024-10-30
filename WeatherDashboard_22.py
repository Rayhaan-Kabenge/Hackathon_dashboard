import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os
from PIL import Image


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
        

    
    
    
 
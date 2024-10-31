import streamlit as st
import os
from PIL import Image
import base64
import glob

# Set up the page configuration
st.set_page_config(
    page_title="KSUTAPS Management Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar starts collapsed
)

# Paths to resources
logo_path = "F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Dashboard/Official_code/KSU-TAPS transparent.png"
slideshow_folder = "F:/beng/K/KSU/KSU_TAPS/TAPS_Hackathon/Dashboard/Official_code/Slideshow"
weather_img_path = 'C:/Users/Rayhaan_Kabenge/Downloads/WD.png'  # Path to the image for the Weather Dashboard
crop_health_img_path = 'C:/Users/Rayhaan_Kabenge/Downloads/CD.png'  # Path to the image for the Crop Health Dashboard
soil_status_img_path = 'C:/Users/Rayhaan_Kabenge/Downloads/SD.png'  # Path to the image for the Soil Status Dashboard

# Dashboard URLs (replace these with actual URLs or paths if available)
dashboard_urls = {
    "Weather Dashboard": "https://example.com/weather_dashboard",
    "Crop Health Dashboard": "https://example.com/crop_health_dashboard",
    "Soil Status Dashboard": "https://example.com/soil_status_dashboard"
}

# Optimized function to convert logo to base64 with caching
@st.cache_data
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Caching the encoded logo and slideshow images
logo_base64 = get_image_base64(logo_path)
image_files = sorted(glob.glob(os.path.join(slideshow_folder, "p*.png")))
slideshow_images = [get_image_base64(img_path) for img_path in image_files]

# Display title and logo
st.markdown("<div style='text-align: center;'><img src='data:image/png;base64,{}' width='400'></div>".format(logo_base64), unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-size: 4em;'>KSUTAPS Management Dashboard</h1>", unsafe_allow_html=True)

# Sidebar with Media Box button
# Toggle state for slideshow
if "show_slideshow" not in st.session_state:
    st.session_state["show_slideshow"] = False

def toggle_slideshow():
    st.session_state["show_slideshow"] = not st.session_state["show_slideshow"]

with st.sidebar:
    if st.button("Media Box", on_click=toggle_slideshow):
        if st.session_state["show_slideshow"]:
            st.write("Image Slideshow")
            # Display all images in the slideshow
            for img_base64 in slideshow_images:
                st.image(f"data:image/png;base64,{img_base64}", use_column_width=True)

# Centered heading for Core Modules section
st.markdown("<h2 style='text-align: center; font-size: 3.5em;'>Explore the Core Modules</h2>", unsafe_allow_html=True)

# Core Modules arranged horizontally with images above buttons
modules = [
    ("Weather Dashboard", "Access historical and real-time weather information to plan accordingly.", weather_img_path),
    ("Crop Health Dashboard", "Monitor crop conditions and detect potential issues early.", crop_health_img_path),
    ("Soil Status Dashboard", "Analyze soil health indicators for optimal crop growth.", soil_status_img_path)
]

# Display modules in a row with equal spacing, image above button
cols = st.columns(len(modules))
for i, (module, description, img_path) in enumerate(modules):
    with cols[i]:
        # Display the module image centered
        st.image(img_path, width=500)

        # Display the button with tooltip and increased font size
        if st.button(module, key=module, help=description):
            st.write(f"Redirecting to {module}...")
            st.experimental_rerun()  # Placeholder for navigation, replace with st.experimental_redirect(dashboard_urls[module])

# Centered footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>For more resources, tutorials, and support, visit the official <a href='#'>KSUTAPS website</a> or contact us.</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>&copy; 2024 KSUTAPS. All rights reserved.</p>", unsafe_allow_html=True)

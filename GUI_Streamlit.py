import streamlit as st
import plotly.graph_objects as go
import tensorflow as tf
import numpy as np
import cv2
import requests
from streamlit_autorefresh import st_autorefresh

# URLs for PHP scripts
update_state_url = "http://192.168.188.96/plant_monitoring_system/update_button_state.php"  # Replace with the actual URL
fetch_data_url = "http://192.168.188.96/plant_monitoring_system/fetch_data.php"  # Replace with the actual URL
pir_state_url = "http://192.168.188.96/plant_monitoring_system/fetch_pir_state.php"  # Replace with the actual URL for fetching PIR state

# Function to update the state of the buttons in the sdatabase
def update_button_state(button_type, state):
    try:
        response = requests.post(update_state_url, json={'type': button_type, 'state': int(state)})
        if response.status_code == 200:
            st.success(f"{button_type} state updated successfully.")
        else:
            st.error(f"Error updating {button_type} state.")
    except Exception as e:
        st.error(f"Error updating {button_type} state: {e}")

# Function to fetch sensor values from the PHP script
def update_values():
    try:
        response = requests.get(fetch_data_url)  # Replace with the actual URL
        data = response.json()
        temperature_value = next((sensor['value'] for sensor in data if sensor['type'] == 'temperature'), None)
        humidity_value = next((sensor['value'] for sensor in data if sensor['type'] == 'humidity'), None)
        soil_moisture_value = next((sensor['value'] for sensor in data if sensor['type'] == 'soil_moisture'), None)
        return temperature_value, humidity_value, soil_moisture_value
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None, None, None

# Function to fetch PIR state
def fetch_pir_state():
    try:
        response = requests.get(pir_state_url)  # Fetching PIR state from the database
        data = response.json()
        return data.get('pir_state', 0)
    except Exception as e:
        st.error(f"Error fetching PIR state: {e}")
        return 0

# Define the gauge layout and values
def create_gauge(title, value, max_value):
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [0, max_value]},
               'bar': {'color': "#29B6F6"},
               'steps': [{'range': [0, max_value * 0.5], 'color': "#D3D3D3"},
                         {'range': [max_value * 0.5, max_value], 'color': "#11567f"}]}))
    gauge.update_layout(height=250, width=250)  # Adjusted size for the gauges
    return gauge

disease_info = {
    'Apple_Black rot': {
        'Reason/Cause': 'Caused by the fungus Botryosphaeria obtusa.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Prune and destroy infected branches. Apply fungicides during the growing season. Ensure proper air circulation around the tree.'
    },
    'Apple_Cedar rust': {
        'Reason/Cause': 'Caused by the fungus Gymnosporangium juniperi-virginianae.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Remove nearby juniper trees if possible. Apply fungicides during the growing season, especially when conditions are wet.'
    },
    'Apple_Healthy': {
        'Reason/Cause': 'No disease present.',
        'Curable or Not': 'Not applicable',
        'Counter Action': 'Maintain regular care, including proper watering, fertilization, and pruning to keep trees healthy.'
    },
    'Apple_Scab': {
        'Reason/Cause': 'Caused by the fungus Venturia inaequalis.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Apply fungicides in the spring. Practice good sanitation by removing fallen leaves and pruning affected areas.'
    },
    'Citrus_Black spot': {
        'Reason/Cause': 'Caused by the fungus Phyllosticta citricarpa.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Apply fungicides during the growing season. Remove and destroy infected fruit and leaves.'
    },
    'Citrus_Canker': {
        'Reason/Cause': 'Caused by the bacterium Xanthomonas axonopodis pv. citri.',
        'Curable or Not': 'Not curable',
        'Counter Action': 'Implement strict sanitation practices. Remove and destroy infected plants. Use resistant varieties if available.'
    },
    'Citrus_Greening': {
        'Reason/Cause': 'Caused by the bacterium Candidatus Liberibacter spp., spread by the Asian citrus psyllid.',
        'Curable or Not': 'Not curable',
        'Counter Action': 'Control psyllid populations using insecticides. Remove and destroy infected trees to prevent spread.'
    },
    'Citrus_Healthy': {
        'Reason/Cause': 'No disease present.',
        'Curable or Not': 'Not applicable',
        'Counter Action': 'Regular care, including proper irrigation, fertilization, and pest control, to maintain tree health.'
    },
    'Citrus_Melanose': {
        'Reason/Cause': 'Caused by the fungus Diaporthe citri.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Prune dead wood to reduce inoculum. Apply copper-based fungicides to control the disease.'
    },
    'Grape_Black Measles': {
        'Reason/Cause': 'Caused by the fungus Phaeoacremonium species.',
        'Curable or Not': 'Not curable',
        'Counter Action': 'Remove and destroy infected vines. Manage water stress and avoid over-irrigation to reduce disease severity.'
    },
    'Grape_Black rot': {
        'Reason/Cause': 'Caused by the fungus Guignardia bidwellii.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Apply fungicides during the growing season. Remove and destroy infected plant parts.'
    },
    'Grape_Healthy': {
        'Reason/Cause': 'No disease present.',
        'Curable or Not': 'Not applicable',
        'Counter Action': 'Regular care, including proper pruning, watering, and pest control, to maintain vine health.'
    },
    'Grape_Isariopsis Leaf Spot': {
        'Reason/Cause': 'Caused by the fungus Isariopsis clavispora.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Apply fungicides during the growing season. Ensure proper air circulation around the vines.'
    },
    'Guava_Canker': {
        'Reason/Cause': 'Caused by various bacteria and fungi, commonly Pseudomonas spp. or Phytophthora spp.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Prune and destroy infected parts. Apply copper-based fungicides. Improve drainage around the plants.'
    },
    'Guava_Dot': {
        'Reason/Cause': 'Typically caused by scale insects or fungal infections, leading to small dots or spots on the fruit and leaves.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Apply insecticides or fungicides as appropriate. Prune and dispose of infected parts.'
    },
    'Guava_Healthy': {
        'Reason/Cause': 'No disease present.',
        'Curable or Not': 'Not applicable',
        'Counter Action': 'Regular care, including proper watering, fertilization, and pest control, to maintain plant health.'
    },
    'Guava_Mummification': {
        'Reason/Cause': 'Caused by fungal infections like Monilinia spp., which lead to the drying and shriveling of fruit.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Remove and destroy mummified fruit. Apply fungicides during the blooming period.'
    },
    'Guava_Rust': {
        'Reason/Cause': 'Caused by the fungus Puccinia psidii.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Apply fungicides and remove affected leaves. Ensure proper spacing for air circulation.'
    },
    'Mango_Anthracnose': {
        'Reason/Cause': 'Caused by the fungus Colletotrichum gloeosporioides.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Apply fungicides during the flowering and fruiting stages. Remove and destroy infected plant parts.'
    },
    'Mango_Bacterial Canker': {
        'Reason/Cause': 'Caused by the bacterium Xanthomonas campestris pv. mangiferaeindicae.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Prune and destroy infected parts. Apply copper-based bactericides.'
    },
    'Mango_Die Back': {
        'Reason/Cause': 'Often caused by fungal infections like Botryodiplodia theobromae or Phomopsis species.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Prune and destroy infected branches. Apply fungicides during the growing season.'
    },
    'Mango_Gall Midge': {
        'Reason/Cause': 'Caused by the insect Procontarinia matteiana, which lays eggs in the buds, leading to gall formation.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Apply insecticides during the egg-laying period. Remove and destroy galls.'
    },
    'Mango_Healthy': {
        'Reason/Cause': 'No disease present.',
        'Curable or Not': 'Not applicable',
        'Counter Action': 'Regular care, including proper fertilization, irrigation, and pest management, to maintain tree health.'
    },
    'Mango_Powdery Mildew': {
        'Reason/Cause': 'Caused by the fungus Oidium mangiferae.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Apply sulfur or fungicides. Improve air circulation around the trees.'
    },
    'Mango_Sooty Mould': {
        'Reason/Cause': 'Caused by various fungi that grow on the honeydew excreted by sucking insects like aphids or whiteflies.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Control the insect population with insecticides. Wash off the sooty mold with water and soap.'
    },
    'Watermelon_Downy Mildew': {
        'Reason/Cause': 'Caused by the oomycete Pseudoperonospora cubensis.',
        'Curable or Not': 'Curable',
        'Counter Action': 'Apply fungicides. Ensure proper spacing and air circulation around plants.'
    },
    'Watermelon_Healthy': {
        'Reason/Cause': 'No disease present.',
        'Curable or Not': 'Not applicable',
        'Counter Action': 'Regular care, including proper irrigation, fertilization, and pest control, to maintain plant health.'
    },
    'Watermelon_Mosaic Virus': {
        'Reason/Cause': 'Caused by various viruses, including Watermelon mosaic virus (WMV), transmitted by aphids.',
        'Curable or Not': 'Not curable',
        'Counter Action': 'Control aphid populations. Remove and destroy infected plants. Use resistant varieties if available.'
    }
}


def display_disease_info(index):
    disease = class_names[index]
    st.write(f"Selected Disease: {disease}")  # Debugging line

    if disease not in disease_info:
        st.error(f"Disease '{disease}' not found in disease_info")
        return

    st.header(f"Disease: {disease}")

    reason = disease_info[disease].get('Reason/Cause', 'Information not available')
    curable = disease_info[disease].get('Curable or Not', 'Information not available')
    counter_action = disease_info[disease].get('Counter Action', 'Information not available')

    st.write(f"**Reason/Cause:**\n {reason}")
    st.write(f"**Curable or Not:**\n {curable}")
    st.write(f"**Counter Action:**\n {counter_action}")



# Custom CSS for tab buttons, toggle switches, and logo alignment
tab_css = """
    <style>
    .stTabs div[data-baseweb="tab-list"] {
       display: flex;
        justify-content: space-evenly;
    }
    .stTabs div[data-baseweb="tab"] {
        flex-grow: 1;
        flex-basis: 0;
        text-align: center;
        padding: 10px;
        font-size: 20px;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
        gap:20%;
    }
    .logo-container img {
        height:120px;
    }
    .block-container.st-emotion-cache-13ln4jf.ea3mdgi5{
    padding-top:3rem;
    }
    </style>
"""
st.markdown(tab_css, unsafe_allow_html=True)

# Insert logos at the top
st.markdown("""
<div class="logo-container">
    <img src="http://127.0.0.1:5500/3.png" alt="Logo 1">
    <img src="http://127.0.0.1:5500/2.png" alt="Logo 2">
    <img src="http://127.0.0.1:5500/1.png" alt="Logo 3">
</div>
""", unsafe_allow_html=True)

# Load the pre-trained model (classification-only)
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("brolgan_model1.keras")

model = load_model()

# Define class names
class_names = ['Apple_Black rot', 'Apple_Cedar rust', 'Apple_Healthy', 'Apple_Scab', 'Citrus_Black spot',
               'Citrus_Canker', 'Citrus_Greening', 'Citrus_Healthy', 'Citrus_Melanose', 'Grape_Black Measles',
               'Grape_Black rot', 'Grape_Healthy', 'Grape_Isariopsis Leaf Spot', 'Guava_Canker', 'Guava_Dot',
               'Guava_Healthy', 'Guava_Mummification', 'Guava_Rust', 'Mango_Anthracnose', 'Mango_Bacterial Canker',
               'Mango_Die Back', 'Mango_Gall Midge', 'Mango_Healthy', 'Mango_Powdery Mildew', 'Mango_Sooty Mould',
               'Watermelon_Downy Mildew', 'Watermelon_Healthy', 'Watermelon_Mosaic Virus']

# Function to make predictions from a live frame
def model_prediction_live(image):
    img_resized = tf.image.resize(image, (128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(img_resized)
    input_arr = np.array([input_arr])  # Convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions[0])

# Function to draw predictions
def draw_predictions(image, class_id):
    label = class_names[class_id]
    cv2.putText(image, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# Function to make predictions from uploaded image
def model_prediction(test_image):
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions[0])  # Return index of max element

# Create tabs
tab1, tab2 = st.tabs(["Plant Monitoring Dashboard", "Disease Detection Dashboard"])

with tab1:
    st.title("Plant Monitoring Dashboard")

    # Fetch current sensor values
    temperature_value, humidity_value, soil_moisture_value = update_values()

    # Create gauges
    temperature_gauge = create_gauge("Temperature (°C)", temperature_value, 50)
    humidity_gauge = create_gauge("Humidity (%)", humidity_value, 100)
    soil_moisture_gauge = create_gauge("Soil Moisture", soil_moisture_value, 100)

    # Display gauges in a row
    col1, col2, col3 = st.columns(3)
    col1.plotly_chart(temperature_gauge, use_container_width=True)
    col2.plotly_chart(humidity_gauge, use_container_width=True)
    col3.plotly_chart(soil_moisture_gauge, use_container_width=True)

    # Toggle switches
    col4, col5 = st.columns(2)
    pump_status = col4.toggle("Enable Water Pump", key="pump_toggle", value=False)

    if pump_status != st.session_state.get('water_pump_state', False):
        update_button_state('water_pump', pump_status)
        st.session_state['water_pump_state'] = pump_status


    if pump_status:
        st.success("Water Pump is enabled.")
    else:
        st.warning("Water Pump is disabled.")


with tab2:


    st.header("Real-Time Plant Disease Detection")
    run = st.toggle('Run Real-Time Detection')

    # Initialize webcam
    cap = cv2.VideoCapture(1)
    frame_window = st.image([])

    # Run the detection loop
    if run:
        while run:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get model prediction
            result_index = model_prediction_live(frame_rgb)

            # Draw predictions on frame
            draw_predictions(frame_rgb, result_index)

            # Display the frame
            frame_window.image(frame_rgb, caption="Webcam Feed", channels="RGB", use_column_width=True)

        display_disease_info(result_index)
        # Release the capture and cleanup
        cap.release()
        st.write("Webcam stopped.")

    st.header("Disease Detection with Image")
    test_image = st.file_uploader("Choose an Image:")
    if test_image:
        if st.button("Show Image"):
            st.image(test_image, use_column_width=True)

        # Predict button
        if st.button("Predict"):
            st.snow()
            st.write("Our Prediction")
            result_index = model_prediction(test_image)
            st.success(f"Model is predicting it's {class_names[result_index]}")
            display_disease_info(result_index)

    auto_refresh = st.toggle("Auto-refresh", value=True)

    if auto_refresh:
        # Set up auto-refresh every 1 second
        st_autorefresh(interval=1000, key="data_refresh")
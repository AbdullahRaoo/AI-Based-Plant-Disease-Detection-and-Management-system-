# 🌱 AI-Based Plant Disease Detection and Management System

The **AI-Based Plant Disease Detection and Management System** is a comprehensive solution that combines artificial intelligence with IoT technology to revolutionize plant health monitoring. The system features an advanced AI model for detecting plant diseases through leaf image analysis and a real-time plant management dashboard that monitors environmental conditions including temperature, humidity, soil moisture, and plant movement detection.

---

## 🚀 Features

- 🔍 **Real-time Disease Detection**: Advanced CNN model for identifying 28 different plant diseases across multiple crops
- 📸 **Multi-input Support**: Upload images or use live webcam feed for disease detection
- 📊 **Environmental Monitoring**: Real-time tracking of temperature, humidity, and soil moisture
- 💧 **Smart Irrigation**: Automated water pump control based on soil moisture levels
- 🌐 **Web Dashboard**: Interactive Streamlit-based interface with real-time data visualization
- 📱 **IoT Integration**: Seamless connection with Arduino-based sensor systems
- 📈 **Data Analytics**: Comprehensive sensor data logging and visualization

---

## 🛠️ Tech Stack

### Machine Learning & AI
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)

### Web Framework & UI
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

### Data Visualization
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

### IoT & Hardware
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=raspberry-pi&logoColor=white)

### Backend & Database
![PHP](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

### Communication
![HTTP](https://img.shields.io/badge/HTTP%20Requests-FF6B6B?style=for-the-badge&logo=http&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)

---

## 🌿 Supported Plant Diseases

The system can detect **28 different diseases** across multiple crop types:

### 🍎 Apple Diseases
- Black Rot
- Cedar Rust
- Apple Scab
- Healthy Apple

### 🍊 Citrus Diseases
- Black Spot
- Canker
- Greening
- Melanose
- Healthy Citrus

### 🍇 Grape Diseases
- Black Measles
- Black Rot
- Isariopsis Leaf Spot
- Healthy Grape

### 🥭 Mango Diseases
- Anthracnose
- Bacterial Canker
- Die Back
- Gall Midge
- Powdery Mildew
- Sooty Mould
- Healthy Mango

### 🍈 Watermelon Diseases
- Downy Mildew
- Mosaic Virus
- Healthy Watermelon

### 🍏 Guava Diseases
- Canker
- Dot Disease
- Mummification
- Rust
- Healthy Guava

---

## 📊 System Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   IoT Sensors       │    │   Web Dashboard     │    │   AI Disease       │
│   (Arduino)         │───▶│   (Streamlit)       │───▶│   Detection Model   │
│                     │    │                     │    │   (TensorFlow)      │
│ • Temperature       │    │ • Real-time Gauges  │    │                     │
│ • Humidity          │    │ • Control Switches  │    │ • CNN Architecture  │
│ • Soil Moisture     │    │ • Disease Detection │    │ • 28 Disease Classes│
│ • PIR Motion        │    │ • Image Upload      │    │ • 128x128 Input     │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │                           │                           │
           ▼                           ▼                           ▼
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   PHP Backend      │    │   Database          │    │   Disease Info      │
│                     │    │   (MySQL)           │    │   System            │
│ • Sensor Data API   │    │                     │    │                     │
│ • Control API       │    │ • Sensor Logs       │    │ • Cause Analysis    │
│ • State Management  │    │ • Device States     │    │ • Treatment Info    │
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Arduino IDE
- Web server with PHP support
- MySQL database
- Webcam/Camera module

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AbdullahRaoo/AI-Based-Plant-Disease-Detection-and-Management-system.git
   cd AI-Based-Plant-Disease-Detection-and-Management-system
   ```

2. **Install Python Dependencies**
   ```bash
   pip install streamlit tensorflow opencv-python plotly requests streamlit-autorefresh numpy
   ```

3. **Setup Hardware**
   - Connect sensors to Arduino
   - Upload Arduino code to microcontroller
   - Configure sensor connections

4. **Database Setup**
   - Create MySQL database
   - Import database schema
   - Update connection parameters in PHP files

5. **Run the Application**
   ```bash
   streamlit run GUI_Streamlit.py
   ```

---

## 💻 Usage

### Disease Detection
1. **Image Upload**: Upload a clear image of the plant leaf
2. **Live Detection**: Use webcam for real-time disease detection
3. **Results**: Get instant disease identification with treatment recommendations

### Environmental Monitoring
1. **Dashboard View**: Monitor real-time sensor data through interactive gauges
2. **Auto-refresh**: Enable automatic data updates
3. **Control Systems**: Toggle water pump and other actuators

---

## 📱 API Endpoints

The system includes several PHP endpoints for IoT communication:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/update_button_state.php` | POST | Update device states |
| `/fetch_data.php` | GET | Retrieve sensor data |
| `/fetch_pir_state.php` | GET | Get PIR sensor status |

---

## 🎯 Model Performance

The disease detection model achieves:
- **Accuracy**: 95%+ on test dataset
- **Classes**: 28 different plant diseases
- **Input Size**: 128x128 RGB images
- **Architecture**: Convolutional Neural Network (CNN)

---

## 📸 Screenshots

### Main Dashboard
![Dashboard](screenshots/dashboard.png)

### Disease Detection Interface
![Disease Detection](screenshots/disease_detection.png)

### Real-time Monitoring
![Monitoring](screenshots/monitoring.png)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- TensorFlow team for the ML framework
- Streamlit for the amazing web framework
- OpenCV community for computer vision tools
- Arduino community for IoT hardware support

---

## 📞 Contact

**Abdullah Rao** - [@AbdullahRaoo](https://github.com/AbdullahRaoo)

Project Link: [https://github.com/AbdullahRaoo/AI-Based-Plant-Disease-Detection-and-Management-system](https://github.com/AbdullahRaoo/AI-Based-Plant-Disease-Detection-and-Management-system)

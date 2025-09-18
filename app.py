import streamlit as st
import requests
from PIL import Image
import io
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Banana Ripeness ML",
    page_icon="🍌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FFD700;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #4CAF50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .nav-button {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 4px;
        margin-right: 0.5rem;
        cursor: pointer;
    }
    .nav-button:hover {
        background-color: #45a049;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .tech-stack {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 15px 0;
    }
    .tech-item {
        background: #4CAF50;
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Navigation function
def navigate_to(page):
    st.session_state.page = page

# 🍌 Simplified Sidebar
with st.sidebar:
    # Centered image
    st.markdown(
        "<div style='text-align: center;'>"
        "<img src='https://cdn-icons-png.freepik.com/512/831/831896.png?uid=R204577341&ga=GA1.1.1807103419.1750135458' width='100'>"
        "</div>",
        unsafe_allow_html=True
    )

    # Centered and bold title
    st.markdown(
        "<div style='text-align: center;'>"
        "<strong style='font-size: 20px;'>Banana ML</strong>"
        "</div>",
        unsafe_allow_html=True
    )

    # Navigation buttons
    if st.button("🏠 Home", use_container_width=True):
        navigate_to('Home')
    if st.button("📖 About", use_container_width=True):
        navigate_to('About')

    st.markdown("---")
    st.info("Upload a banana image to check its ripeness and estimate days until rotten.")
    
# Home Page
if st.session_state.page == 'Home':
    # 🍌 Main Header
    st.markdown("""
        <h1 style='text-align: center; font-size: 2.5em;'>Banana Ripeness Classifier and Shelf Life</h1>
        <p style='text-align: center; font-size: 1.1em; color: gray;'>Upload a banana image to check its ripeness and estimate days until spoilage.</p>
        <hr style='margin-top: 1em; margin-bottom: 2em;'>
    """, unsafe_allow_html=True)

    # 🔄 Two-column layout
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("###  Upload Banana Image")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Banana', use_container_width=True)

            if st.button("Analyze Banana", type="primary", use_container_width=True):
                with st.spinner('Analyzing your banana...'):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)

                    # Mock result (replace with actual API call)
                    files = {"file": uploaded_file.getvalue()}

                    headers = {"Authorization": f"Bearer {os.environ.get('HF_API_TOKEN')}"}
                    response = requests.post("https://miyukicodes-banana-ml.hf.space/predict", files=files, headers=headers)
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.result = result
                        st.session_state.analyzed = True
                    else:
                        st.error(f"Prediction failed: {response.json().get('detail', 'Unknown error')}")


    with col2:
        st.markdown("###  Analysis Results")

        if st.session_state.get("analyzed", False):
            result = st.session_state.result

            st.markdown(f"""
                <div style='padding: 1.5em; border-radius: 12px; background-color: #fffbe6; border: 1px solid #f0e68c;'>
                
                <div style='display: flex; align-items: center; justify-content: space-between;'>
                    <h4 style='margin: 0;'>Ripeness Stage</h4>
                    <span style='background-color: #ffe135; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 1em;'>{result['ripeness_stage']}</span>
                </div>
                
                <div style='margin-top: 0.5em; color: gray; font-size: 0.95em;'>
                    Confidence: {result['confidence']*100:.1f}%
                    <div style='height: 8px; background-color: #eee; border-radius: 4px; margin-top: 4px;'>
                    <div style='width: {result['confidence']*100:.1f}%; height: 100%; background-color: #f4c430; border-radius: 4px;'></div>
                    </div>
                </div>

                <hr style='margin: 1em 0;'>

                <h4 style='margin-bottom: 0.5em;'>Estimated Shelf Life</h4>
                <p style='font-size: 1.2em; font-weight: bold; color: #333;'>{result['days_until_rotten']} days until spoilage</p>

                </div>
                """, unsafe_allow_html=True)

            # Visual indicator
            if result['days_until_rotten'] > 5:
                st.success("✅ This banana will stay fresh for a while!")
            elif result['days_until_rotten'] > 2:
                st.info("🍽️ Enjoy this banana soon!")
            elif result['days_until_rotten'] > 0:
                st.warning("⚠️ Use this banana immediately!")
            else:
                st.error("❌ This banana is already rotten!")

            st.markdown("</div>", unsafe_allow_html=True)

            # 🍽️ Recommendation
            st.markdown("###  Recommendation")
            stage = result['ripeness_stage']
            if stage == "Unripe":
                st.info("This banana is still unripe. Best for cooking or waiting until it ripens.")
            elif stage == "Ripe":
                st.success("Perfectly ripe! Enjoy now for best flavor and nutrition.")
            elif stage == "Overripe":
                st.warning("Overripe — great for banana bread or smoothies.")
            else:
                st.error("Already rotten. Best to compost it.")
        else:
            st.info("Upload a banana image and click **Analyze** to see results here.")
            
            
# About Page
else:
    st.markdown('<h1 class="main-header">About this Project</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    This application uses machine learning to classify the ripeness of bananas and predict 
    how many days remain before they become rotten. The system helps reduce food waste by 
    providing accurate predictions about banana freshness.
    """)
    
    st.markdown('<h2 class="sub-header">How It Works</h2>', unsafe_allow_html=True)
    
    # Process flowchart
    st.image("banana.drawio.png", caption="Application Process", width=100)
    
    st.markdown("""
    1. **Image Upload**: Users upload an image of a banana
    2. **Preprocessing**: The image is resized and normalized for the model
    3. **Classification**: A convolutional neural network classifies the ripeness stage
    4. **Prediction**: Based on the image, days until rotten are estimated
    5. **Results**: The system displays the ripeness stage and recommendations
    """)
    
    st.markdown('<h2 class="sub-header">Tech Stack</h2>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style='display: flex; flex-wrap: wrap; gap: 10px; margin-top: 1em;'>
        <span style='background-color: #f0f0f0; padding: 6px 12px; border-radius: 20px; font-weight: 500;'>Python</span>
        <span style='background-color: #f0f0f0; padding: 6px 12px; border-radius: 20px; font-weight: 500;'>FastAPI</span>
        <span style='background-color: #f0f0f0; padding: 6px 12px; border-radius: 20px; font-weight: 500;'>Streamlit</span>
        <span style='background-color: #f0f0f0; padding: 6px 12px; border-radius: 20px; font-weight: 500;'>TensorFlow/Keras</span>
        <span style='background-color: #f0f0f0; padding: 6px 12px; border-radius: 20px; font-weight: 500;'>OpenCV</span>
        <span style='background-color: #f0f0f0; padding: 6px 12px; border-radius: 20px; font-weight: 500;'>NumPy</span>
        <span style='background-color: #f0f0f0; padding: 6px 12px; border-radius: 20px; font-weight: 500;'>Pillow</span>
        <span style='background-color: #f0f0f0; padding: 6px 12px; border-radius: 20px; font-weight: 500;'>Kaggle</span>
        <a href='https://github.com/google/automl/tree/master/efficientnetv2' target='_blank' style='text-decoration: none;'>
            <span style='background-color: #e0f7fa; padding: 6px 12px; border-radius: 20px; font-weight: 500; color: #00796b;'>EfficientNetV2B0 GitHub</span>
        </a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="sub-header">Project Links</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **GitHub Repository**:  
        [github.com/yourusername/banana-ripeness-classifier](https://github.com/yourusername/banana-ripeness-classifier)
        """)
    with col2:
        st.markdown("""
        **LinkedIn Profile**:  
        [linkedin.com/in/zrmdcs12](https://linkedin.com/in/zrmdcs12)
        """)
    
    st.markdown('<h2 class="sub-header">Model Architecture</h2>', unsafe_allow_html=True)
    
    st.image("https://cdn.analyticsvidhya.com/wp-content/uploads/2020/10/90650dnn2.webp", caption="CNN Model Architecture", use_container_width=True)
    
    st.markdown("""
    The model is based on a convolutional neural network (CNN) with transfer learning. 
    We use a pre-trained EfficientNet backbone with custom layers for banana-specific classification.
    The model outputs both a ripeness classification and a regression value for days until rotten.
    """)

# Footer
st.markdown("---")
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("Banana Ripeness Classifier 🍌 | Made with Streamlit")
st.markdown('</div>', unsafe_allow_html=True)
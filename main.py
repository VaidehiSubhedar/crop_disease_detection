import streamlit as st
import tensorflow as tf
import numpy as np
from pymongo import MongoClient
import uuid
import requests
import json
from datetime import datetime
import os

# Function to download the model if it doesn't exist
def download_model(url, filename="trained_model.keras"):
    if not os.path.exists(filename):
        with st.spinner("Downloading model... This may take a moment."):
            response = requests.get(url, stream=True)
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
    return filename

# Tensorflow ModelPrediction
def model_prediction(test_image):
    model = tf.keras.models.load_model('trained_model.keras') 
    image = tf.keras.preprocessing.image.load_img(test_image,target_size = (128,128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)
    return result_index

# Set page configuration
st.set_page_config(page_title="Crop Disease Prediction", layout="wide")

# Download the model
MODEL_URL = "https://drive.google.com/uc?export=download&id=1hKdVBqDclxYLQuUzyVmgsBMvRwPRMU86" # <-- IMPORTANT: REPLACE WITH YOUR MODEL'S DOWNLOAD LINK
download_model(MODEL_URL)


st.markdown("""
    <style>
        body {
            background-color: #e6ffe6;
        }
        .main-title {
            font-size: 38px !important;
            color: #39FF14;
            text-align: center;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .nav-bar {
            display: flex;
            justify-content: center;
            gap: 20px;
            background: #f4f4f4;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(213, 205, 213, 0.1);
            margin-bottom: 20px;
        }
        .nav-button {
            background: #228B22;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 18px;
            transition: 0.3s;
        }
        .nav-button:hover {
            background: #1A6B16;
        }
        .container {
            border: 2px solid #4CAF50;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            background-color: #f9f9f9;
        }
        .sub-container {
            border: 1px solid #228B22;
            border-radius: 8px;
            padding: 10px;
            margin: 5px;
            background-color: #DFF2BF;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Home"

# Title Bar Navigation
st.markdown("<div class='nav-bar'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
if col1.button("Home"):
    st.session_state.selected_page = "Home"
if col2.button("Agri Community"):
    st.session_state.selected_page = "Agri Community"
if col3.button("Settings"):
    st.session_state.selected_page = "Settings"
st.markdown("</div>", unsafe_allow_html=True)

def get_mongo_connection():
    client = MongoClient(st.secrets["connections"]["mongodb_uri"])
    db = client["NewDataBase"]
    return db

if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'predicted_disease' not in st.session_state:
    st.session_state.predicted_disease = None



# Home Page
if st.session_state.selected_page == "Home":
    st.markdown("<h1 class='main-title'>🌱 Crop Disease Prediction System</h1>", unsafe_allow_html=True)
    st.write("Upload an image of a plant leaf to get an instant disease prediction. AI-powered insights to help farmers protect crops!")

    test_image = st.file_uploader("Upload a leaf image for analysis", type=["jpg", "png", "jpeg"])

    if st.button("Show Image"):
        if test_image is not None:
            st.image(test_image, width=500)
        else:
            st.warning("Please upload an image first.")

    if st.button("Predict", key="predict_button"):
        if test_image is not None:
            st.balloons()
            st.write("Our Prediction")

            def model_prediction(image_file, threshold=0.5):
                try:
                    model = tf.keras.models.load_model('trained_model.keras')

                    image = tf.keras.preprocessing.image.load_img(image_file, target_size=(128, 128))
                    input_arr = tf.keras.preprocessing.image.img_to_array(image)
                    input_arr = np.expand_dims(input_arr, axis=0)  # No normalization if not used during training

                    prediction = model.predict(input_arr)[0]
                    confidence = np.max(prediction)
                    result_index = np.argmax(prediction)

                    top_indices = prediction.argsort()[-3:][::-1]
                    top_confidences = [(i, prediction[i]) for i in top_indices]

                    return result_index, confidence, top_confidences

                except Exception as e:
                    st.error("❌ Error: The uploaded image is invalid or corrupted.")
                    return None, 0.0, []

            result_index, confidence, top_3 = model_prediction(test_image)

            # Class Labels
            class_name = [
                'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
                'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
                'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
                'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
                'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
                'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
                'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
                'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
                'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
                'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
                'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
                'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
            ]

            # Heuristic check for suspicious input
            filename_lower = test_image.name.lower()
            suspicious_keywords = ["bill", "invoice", "document", "note", "form", "paper"]
            filename_suspicious = any(word in filename_lower for word in suspicious_keywords)

            # Confidence gap check
            conf_gap = top_3[0][1] - top_3[1][1]
            conf_too_close = conf_gap < 0.05

            if filename_suspicious or (confidence > 0.9 and conf_too_close):
                st.warning("🚫 This image doesn't seem to be a valid crop leaf. Please upload a proper plant image.")
                st.session_state.prediction_made = False
                st.session_state.predicted_disease = None
            else:
                Disease = class_name[result_index]
                st.success(f"✅ Model predicts: **{Disease}** (Confidence: {confidence:.2f})")
                st.session_state.prediction_made = True
                st.session_state.predicted_disease = Disease

                with st.expander("🔍 Top 3 Predictions"):
                    for idx, conf in top_3:
                        st.write(f"- {class_name[idx]}: **{conf:.2f}**")
        else:
            st.warning("📷 Please upload a valid image before clicking Predict.")

    # Show preventions & remedies
    if st.session_state.get("prediction_made") and st.session_state.get("predicted_disease"):
        db = get_mongo_connection()
        collection = db["SampleCollection"]

        def get_preventions(disease):
            record = collection.find_one({"disease": disease})
            return record["prevention"] if record and "prevention" in record else ["No specific prevention info available."]

        def get_remedies(disease):
            record = collection.find_one({"disease": disease})
            return record["remedies"] if record and "remedies" in record else ["No specific remedy info available."]

        if st.button("View Preventions", key='Dis_Preventions'):
            preventions = get_preventions(st.session_state.predicted_disease)
            st.info(f"**🛡️ Preventions for {st.session_state.predicted_disease}:**\n\n" + "\n".join(preventions))

        if st.button("View Remedies", key='Remedies'):
            remedies = get_remedies(st.session_state.predicted_disease)
            st.info(f"**💊 Remedies for {st.session_state.predicted_disease}:**\n\n" + "\n".join(remedies))


# Agri Community Page
elif st.session_state.selected_page == "Agri Community":
    db = get_mongo_connection()
    collection = db["agri_community"]

    st.markdown("<h1 class='main-title'>📌 Agri Community</h1>", unsafe_allow_html=True)
    st.write("A space where farmers can post queries, share solutions, and get AI-driven answers.")
    
    question = st.text_area("Ask a farming-related question:")
    
    if st.button("Submit Question"):
        if st.session_state.get("is_logged_in"):
            if question.strip():
                collection.insert_one({
                    "email": st.session_state["user_email"],
                    "question": question.strip(),
                    "answers": [],
                    "timestamp": datetime.now()
                })
                st.success("✅ Your question has been posted! Community experts will respond soon.")
            else:
                st.error("⚠️ Please enter your question.")
        else:
            st.warning("⚠️ Please log in to submit a question.")

    st.subheader("🗣️ Latest Discussions")
    
    latest_questions = collection.find().sort("timestamp", -1).limit(5)
    for q in latest_questions:
        question_id = str(q["_id"])
        col1,col2 = st.columns(2)
        with col1:
             question_text = q.get("question", "No question text")
             answers = q.get("answers", [])
             answer_count = len(answers)
             st.markdown(f"- **{question_text}** - {answer_count} answer{'s' if answer_count != 1 else ''}")
        with col2:
            if st.button("Give Your Opinion", key=f"btn_{question_id}"):
                st.session_state["answering"] = question_id
                st.rerun()
        if st.session_state.get("answering") == question_id:
            if st.session_state.get("is_logged_in"):
                answer = st.text_area("Submit Your Answer", key=f"answer_text_{question_id}")
                if st.button("Submit Answer", key=f"submit_{question_id}"):
                    if answer.strip():
                        collection.update_one(
                            {"_id": q["_id"]},
                            {"$push": {
                                "answers": {
                                    "email": st.session_state["user_email"],
                                    "text": answer.strip(),
                                    "timestamp": datetime.now()
                                }
                            }}
                        )
                        st.success("✅ Answer submitted!")
                        del st.session_state["answering"]
                        st.rerun()
                    else:
                        st.error("⚠️ Please write an answer before submitting.")
            else:
                st.warning("⚠️ Please log in to submit your answer.")
        if answers:
            with st.expander("View Answers"):
                for ans in answers:
                    st.markdown(f"🗨️ **{ans.get('email', 'Anonymous')}: {ans.get('text', '')}")


if "cart" not in st.session_state:
    st.session_state.cart = []

if "show_sell_page" not in st.session_state:
    st.session_state.show_sell_page = False


# Settings Page
elif st.session_state.selected_page == "Settings":
    st.markdown("<h1 class='main-title'>⚙️ User Settings </h1>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔑 Account Management", "🛒 Farm Store", "📌 Community Settings"])

    # --------------------------------
    # 1️⃣ AUTHENTICATION & ACCOUNT MANAGEMENT
    # --------------------------------
    with tab1:
        st.subheader("🔑 Authentication & Profile Management")

        # Login / Signup Toggle
        auth_option = st.radio("Select Option:", ["Login", "Sign Up"], horizontal=True)

        if auth_option == "Login":
            st.text_input("Email", placeholder="Enter your email", key="login_email")
            st.text_input("Password", placeholder="Enter your password", type="password", key="login_password")
            st.checkbox("Remember Me", key="remember_me")
            if st.button("🔓 Login"):
                email = st.session_state.login_email
                password = st.session_state.login_password
                # Make Mongo collection to store email and password
                db3 = get_mongo_connection()
                users_collection = db3["users"]

                user = users_collection.find_one({"email": email, "password": password})   
                if user:
                    st.session_state["is_logged_in"] = True
                    st.session_state["user_email"] = email 
                    st.success("✅ Logged in successfully!")
                    st.session_state.selected_page = "Farm Store"
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password. Please try again.")
                    st.markdown("[Forgot Password?](#)")
        else:  
            name = st.text_input("Full Name", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_.password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
          
            if st.button("📝 Sign Up"):
                name = st.session_state.get("signup_name", "").strip()
                email = st.session_state.get("signup_email", "").strip()
                password = st.session_state.get("signup_password", "").strip()
                confirm_password = st.session_state.get("signup_confirm_password", "").strip()


                if not name or not email or not password or not confirm_password:
                    st.warning("⚠️ Please fill in all fields.")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match.")

                else:
                    db3 = get_mongo_connection()
                    users_collection = db3["users"]

                    if users_collection.find_one({"email": email}):
                        st.error("❌ An account with this email already exists.")
                    else:
                        users_collection.insert_one({
                            "name": name,
                            "email": email,
                            "password": password  
                        })

                        st.success("✅ Account created successfully! You can now log in.")
                        st.session_state["selected_page"] = "Settings"
                        st.session_state["redirect_to_login"] = True
                        st.rerun() 
        st.divider()
        
    st.subheader("👤 Account Settings")

    if st.session_state.get("is_logged_in"):
        st.write(f"Logged in as: `{st.session_state.user_email}`")
        if st.button("🚪 Logout"):
            st.session_state.is_logged_in = False
            st.session_state.user_email = None
            st.success("🔒 Logged out successfully!")
            st.session_state.selected_page = "Home"
            st.rerun()

        st.divider()

        # Profile Management
        st.subheader("👤 Profile Management")
        profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png", "jpeg"], key="profile_pic")
        st.text_input("Name", placeholder="Enter your name", key="profile_name")
        st.text_input("Email", placeholder="Enter your email", key="profile_email")
        st.text_area("Address", placeholder="Enter your address", key="profile_address")
        if st.button("💾 Save Changes"):
            profile_name = st.session_state.get("profile_name" , "").strip()
            profile_email = st.session_state.get("profile_email" , "").strip()
            address = st.session_state.get("profile_address" , "").strip()

            db3 = get_mongo_connection()
            profiles_collection = db3["profiles"]

            profiles_collection.insert_one({
                            "name": profile_name,
                            "email": profile_email,
                            "address": address  
                        })

            st.success("✅ Profile Updated Successfully !")

    # --------------------------------
    # 2️⃣ FARM STORE SETTINGS
    # --------------------------------
    with tab2:
        st.subheader("🛒 Farm Store Settings")

        # Saved Addresses
        st.markdown("### 📍 Saved Addresses")
        address = st.text_area("Enter New Address", placeholder="Add new address", key="new_address")
        st.button("➕ Add Address", key="add_address")
        st.write("📌 **Home:** 123 Greenfield Street, Texas")
        st.write("📌 **Farm:** 456 Wheat Road, California")
        st.button("🗑 Delete Address", key="delete_address")

        st.divider()

        # Order History
        st.markdown("### 📦 Order History")
        st.write("✅ Order #12345 - **Shipped**")
        st.write("🚚 Order #12346 - **Out for Delivery**")
        st.write("🔄 Order #12347 - **Processing**")

    # --------------------------------
    # 3️⃣ COMMUNITY SETTINGS
    # --------------------------------
    with tab3:
        st.subheader("📌 Community & Forum Settings")
        st.markdown("### ✍ Manage Your Posts & Questions")
        st.write("📌 **How to prevent wheat rust?** (📝 Edit | 🗑 Delete)")
        st.write("📌 **Best organic fertilizers for rice?** (📝 Edit | 🗑 Delete)")
        st.text_area("Edit Post", placeholder="Edit your question here...", key="edit_post")
        st.button("💾 Update Post", key="update_post")
        st.divider()
        st.markdown("### 🔔 Notification ")
        st.checkbox("Receive Email Alerts for Replies", key="email_alerts")
        st.divider()
        st.markdown("### 🌱 Follow Topics of Interest")
        topics = ["Organic Farming", "Disease Prevention", "Climate-based Advice", "Soil Health", "Pesticide-Free Methods"]
        selected_topics = st.multiselect("Select Topics to Follow", topics, key="selected_topics")
        st.button("✅ Follow Selected Topics", key="follow_topics")
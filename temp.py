import streamlit as st
import tensorflow as tf
import numpy as np
from pymongo import MongoClient
import uuid
import requests
import json
from datetime import datetime


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
col1, col2, col3, col4, col5,col6,col7,col8 = st.columns(8)
if col1.button("Home"):
    st.session_state.selected_page = "Home"
if col2.button("Agri Community"):
    st.session_state.selected_page = "Agri Community"
if col3.button("Predict"):
    st.session_state.selected_page = "Predict"
if col4.button("Farm Store"):
    st.session_state.selected_page = "Farm Store"
if col5.button("Settings"):
    st.session_state.selected_page = "Settings"
if col6.button("Ask AI"):
    st.session_state.selected_page = "Ask AI"
if col7.button("Sell Products"):
    st.session_state.selected_page = "Sell Products"
if col8.button("Weather Watch"):
    st.session_state.selected_page = "Weather Watch"
st.markdown("</div>", unsafe_allow_html=True)

def get_mongo_connection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["NewDataBase"]
    return db["SampleCollection"]

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
        collection = get_mongo_connection()

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

   
# Prediction Page
elif st.session_state.selected_page == "Predict":
    # Import templates only when Predict page is selected
  
    st.markdown("<h1 class='main-title'>🦠 Plant Disease Prediction</h1>", unsafe_allow_html=True)
    
    crop = st.selectbox("Select Crop", ["Wheat", "Rice", "Corn"], key="predict_crop")
    stage = st.selectbox("Select Growth Stage", ["🌱 Seeding Stage", "🌿 Vegetative Stage", "🥀 Flowering Stage", "🌾 Fruiting Stage", "🚜 Harvesting Stage"], key="predict_stage")
    
    if crop == "Wheat":
        if stage == "🌱 Seeding Stage":
            from ssw_disease_template import render_wheat_seedling_diseases
            render_wheat_seedling_diseases()
            
        elif stage == "🌿 Vegetative Stage":
            from vsw_disease_template import render_wheat_vegetation_diseases
            render_wheat_vegetation_diseases()
        elif stage == "🥀 Flowering Stage":
            from fsw_disease_template import render_wheat_flowering_diseases
            render_wheat_flowering_diseases()
        elif stage == "🌾 Fruiting Stage":
            from frsw_disease_template import render_wheat_fruiting_diseases
            render_wheat_fruiting_diseases()
        elif stage == "🚜 Harvesting Stage":
            from hsw_disease_template import render_wheat_harvesting_diseases
            render_wheat_harvesting_diseases()

    elif crop == "Rice":
        if stage == "🌱 Seeding Stage":
            from ssr_disease_template import render_rice_seedling_diseases
            render_rice_seedling_diseases()
        elif stage == "🌿 Vegetative Stage":
            from vsr_disease_template import render_rice_vegetation_diseases
            render_rice_vegetation_diseases()
        elif stage == "🥀 Flowering Stage":
            from fsr_disease_template import render_rice_flowering_diseases
            render_rice_flowering_diseases()
        elif stage == "🌾 Fruiting Stage":
            from frsr_disease_template import render_rice_fruiting_diseases
            render_rice_fruiting_diseases()
        elif stage == "🚜 Harvesting Stage":
            from hsr_disease_template import render_rice_harvesting_diseases
            render_rice_harvesting_diseases()

    elif crop == "Corn":
        if stage == "🌱 Seeding Stage":         
            from ssm_disease_template import render_corn_seedling_diseases
            render_corn_seedling_diseases()
        elif stage == "🌿 Vegetative Stage":
            from vsm_disease_template import render_corn_vegetation_diseases
            render_corn_vegetation_diseases()
        elif stage == "🥀 Flowering Stage":
            from fsm_disease_template import render_corn_flowering_diseases  
            render_corn_flowering_diseases()
        elif stage == "🌾 Fruiting Stage":
            from frsm_disease_template import render_corn_fruiting_diseases
            render_corn_fruiting_diseases()
        elif stage == "🚜 Harvesting Stage":
            from hsm_disease_template import render_corn_harvesting_diseases
            render_corn_harvesting_diseases()

# Agri Community Page
elif st.session_state.selected_page == "Agri Community":
    client = MongoClient("mongodb://localhost:27017/")
    db = client["NewDataBase"]
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
                st.experimental_rerun()
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
                        st.experimental_rerun()
                    else:
                        st.error("⚠️ Please write an answer before submitting.")
            else:
                st.warning("⚠️ Please log in to submit your answer.")
        if answers:
            with st.expander("View Answers"):
                for ans in answers:
                    st.markdown(f"🗨️ **{ans.get('email', 'Anonymous')}**: {ans.get('text', '')}")


if "cart" not in st.session_state:
    st.session_state.cart = []

if "show_sell_page" not in st.session_state:
    st.session_state.show_sell_page = False

# Farm Store Page
elif st.session_state.selected_page == "Farm Store":
    client2 = MongoClient("mongodb://localhost:27017/")
    db2 = client2["NewDataBase"]
    collection = db2["products"]

    products = list(collection.find({}, {"_id": 0}))

    search = st.text_input("Search for seeds, fertilizers, tools...")

    if search:
        filtered_products = [product for product in products if search.lower() in product['name'].lower()]
    else:
        filtered_products = products
    st.write("### Featured Products")
    cols = st.columns(4)
    for index, product in enumerate(filtered_products):
        with cols[index % 4]:
            st.markdown(
            f"""
            <div style="height: 250px; text-align:center;">
                <img src="{product['image_url']}" width="200px" style="object-fit:contain; max-height:200px;" />
                <p><b>{product['name']}</b><br>${product['price']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
            if st.button("Add to Cart", key=f"cart_{index}"):
                st.session_state.cart.append(product)
                st.success(f"Added {product['name']} to cart!")

    # View cart section
    with st.expander("🛍️ View Cart"):
        if not st.session_state.cart:
            st.write("Your cart is empty.")
        else:
            total = 0
            for i , item in enumerate(st.session_state.cart):
                col1,col2 = st.columns([4, 1])
                with col1:
                    st.write(f"- {item['name']} - ${item['price']}")
                with col2:
                    if st.button("🗑️Remove from cart",key=f"remove_{i}"):
                        st.session_state.cart.pop(i)
                        st.experimental_rerun()
                total += item["price"]
                st.write(f"**Total: ${total}**")
            if st.button("📦Place Order"):
                if not st.session_state.get("is_logged_in"):
                    st.warning("⚠️ Please log in to place your order.")
                    st.session_state.selected_page = "Settings"  # redirect to login
                    st.experimental_rerun()
                else:
                    st.success("✅ Order is placed successfully!")

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
                client3 = MongoClient("mongodb://localhost:27017/")
                db3 = client3["NewDataBase"]
                users_collection = db3["users"]

                user = users_collection.find_one({"email": email, "password": password})   
                if user:
                    st.session_state["is_logged_in"] = True
                    st.session_state["user_email"] = email 
                    st.success("✅ Logged in successfully!")
                    st.session_state.selected_page = "Farm Store"
                    st.experimental_rerun()
                else:
                    st.error("❌ Invalid email or password. Please try again.")
                    st.markdown("[Forgot Password?](#)")
        else:  
            name = st.text_input("Full Name", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
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
                    client3 = MongoClient("mongodb://localhost:27017/")
                    db3 = client3["NewDataBase"]
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
                        st.experimental_rerun() 
        st.divider()
        
    st.subheader("👤 Account Settings")

    if st.session_state.get("is_logged_in"):
        st.write(f"Logged in as: `{st.session_state.user_email}`")
        if st.button("🚪 Logout"):
            st.session_state.is_logged_in = False
            st.session_state.user_email = None
            st.success("🔒 Logged out successfully!")
            st.session_state.selected_page = "Home"
            st.experimental_rerun()

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

            client3 = MongoClient("mongodb://localhost:27017/")
            db3 = client3["NewDataBase"]
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

if st.session_state.selected_page == "Ask AI":
    api_key = st.secrets["gemini_api"]["api_key"]
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"


    def generate_content(prompt):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Error: {response.status_code}, {response.text}"

    st.markdown("<h1 class='main-title'>🔵 Ask google Gemini </h1>", unsafe_allow_html=True)

    user_input = st.text_area("Enter your prompt:", "")

    if st.button("Generate Content"):
            if user_input:
                result = generate_content(user_input)
                if result:
                    st.write("Generated Content:")
                    st.write(result)
            else:
                st.error("Please enter a prompt.")

# Sell Products page 
if st.session_state.selected_page == "Sell Products":
    st.markdown("<h1 class='main-title'>🚜 AgriMart Seller's Corner</h1>", unsafe_allow_html=True)
    st.text_input("Enter Product's name",placeholder="Name",key = "name")
    st.text_input("Enter Product's Price (in $)",placeholder="Price",key = "price")
    st.text_input("Enter Image url",placeholder="Image",key = "image")
    client2 = MongoClient("mongodb://localhost:27017/")
    db2 = client2["NewDataBase"]
    collection = db2["products"]
    if st.button("upload Product"):
        product_name = st.session_state.get("name"," ").strip()
        product_price = st.session_state.get("price"," ").strip()
        product_image = st.session_state.get("image"," ").strip()

        try:
            product_price = int(product_price)  
        except ValueError:
            st.error("Invalid price entered. Please enter a valid number.")
            
        collection.insert_one({
            "name":product_name,
            "price" : product_price,
            "image_url" : product_image,
        })
        st.success("image uploades Successfully !")
    st.divider()

st.markdown(
    """
    <style>
      /* Page background & primary text color */
      .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
      }

      /* Main title styling */
      .main-title {
        font-size: 2.5rem;
        color:  #39FF14;
        text-align: center;
        margin-bottom: 1rem;
      }

      /* Round the weather icon */
      .stImage > img {
        border-radius: 8px;
      }

      /* Tweak metric card backgrounds */
      .stMetric {
        background: #21252b !important;
        border-radius: 8px;
        padding: 1rem;
      }
    </style>
    """,
    unsafe_allow_html=True
)


import streamlit as st
import requests
import datetime

# Weather Watch page
if st.session_state.get("selected_page", "") == "Weather Watch":
    st.markdown("<h1 class='main-title'>🌤️ Weather Watch</h1>", unsafe_allow_html=True)

    city = st.text_input("Enter Your City", placeholder="e.g. Pune or London,uk")

    if st.button("Get Weather") and city:
        API_KEY = "c250fb3e8c2dff08645e52a9de28d07d"  

        weather_url = "http://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        try:
            res = requests.get(weather_url, params=weather_params)
            data = res.json()

            if res.status_code == 200:
                st.success(f"✅ Weather data for {city.capitalize()}")

                icon_code = data["weather"][0]["icon"]
                icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
                st.image(icon_url, width=100)

                c1, c2, c3 = st.columns(3)
                c1.metric("🌡️ Temp (°C)", f"{data['main']['temp']}", f"Feels {data['main']['feels_like']}°C")
                c2.metric("💧 Humidity", f"{data['main']['humidity']}%")
                c3.metric("💨 Wind (m/s)", f"{data['wind']['speed']}")

                st.markdown("---")
                st.write(f"**Condition:** {data['weather'][0]['description'].capitalize()}")
                st.write(f"**Pressure:** {data['main']['pressure']} hPa")
                st.write(f"**Min / Max Temp:** {data['main']['temp_min']}° / {data['main']['temp_max']}°C")

                lat = data["coord"]["lat"]
                lon = data["coord"]["lon"]

                forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
                forecast_params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": API_KEY,
                    "units": "metric"
                }

                forecast_res = requests.get(forecast_url, params=forecast_params)
                forecast_data = forecast_res.json()

                st.divider()

                if forecast_res.status_code == 200 and "list" in forecast_data:
                    st.markdown("## 📅 3-Day Forecast")

                    forecast_by_date = {}

                    for entry in forecast_data["list"]:
                        dt = datetime.datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
                        date_str = dt.strftime("%A, %d %b")

                        if date_str not in forecast_by_date:
                            forecast_by_date[date_str] = []

                        forecast_by_date[date_str].append(entry)

                    for i, (date, entries) in enumerate(forecast_by_date.items()):
                        if i >= 3:
                            break

                        with st.expander(f"{date}"):
                            for entry in entries:
                                time = entry["dt_txt"].split(" ")[1][:5]
                                icon_code = entry["weather"][0]["icon"]
                                icon_url = f"https://openweathermap.org/img/wn/{icon_code}.png"

                                st.image(icon_url, width=50)
                                st.write(f"🕐 Time: {time}")
                                st.write(f"🌡️ Temp: {entry['main']['temp']}°C")
                                st.write(f"💧 Humidity: {entry['main']['humidity']}%")
                                st.write(f"💨 Wind Speed: {entry['wind']['speed']} m/s")
                                st.write(f"🌥️ Condition: {entry['weather'][0]['description'].capitalize()}")
                                st.markdown("---")
                else:
                    st.warning("⚠️ Could not fetch forecast data.")

            else:
                st.error(f"❌ {data.get('message', 'Failed to fetch weather data')}")

        except Exception as e:
            st.error("⚠️ Something went wrong. Please try again later.")
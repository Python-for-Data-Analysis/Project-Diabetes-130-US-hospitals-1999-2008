import streamlit as st

# Set basic configurations of the page
st.set_page_config(
    page_title="Diabetes Readmission Analysis",
    page_icon="🏥",
)

# Custom CSS for the page
st.markdown("""
    <style>
    .banner {
        color: #fff;
        padding: 10px;
        text-align: center;
    }
    div.stButton > button:first-child {
        height: 3em;
        width: 100%;
        font-size: 1.5em;
        margin: 5px 0;
    }
    .st-cx {
        padding: 0px;
    }
    </style>
""", unsafe_allow_html=True)

# Display the blue banner with the hospital's name
st.markdown('<div class="banner"><h1>Diabetes Readmission Insights</h1></div>', unsafe_allow_html=True)

# Welcome message and introduction
st.write("\n" * 5)
st.markdown("""
    ## 🏥 Welcome onboard
    This website provides an in-depth analysis of diabetes patient readmissions in US hospitals. 
    We leverage a decade of clinical data to predict and understand the factors leading to the 
    readmission of diabetic patients within 30 days of discharge.
""")

# Explanation of the importance of the website
st.markdown("""
    #### 🔍 Why is this important?
    Despite high-quality evidence for improved outcomes through preventive and therapeutic interventions, 
    many diabetic patients do not receive adequate care. Inefficient management leads to increased costs 
    for hospitals due to patient readmissions, and more importantly, it impacts patient health adversely. 
    Our analysis aims to address this gap by providing insights into the predictors of readmission.
""")

# Link to other pages and their description
st.write("\n" * 5)
st.markdown("""
    ### Explore Our Features
""")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🆕 New Prediction")
    st.write("Evaluate the readmission risk for a new patient based on clinical data.")


with col2:
    st.markdown("#### 📈 Dataset Statistics")
    st.write("View statistical insights from our training dataset to understand broader trends.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📑 Our approach")
    st.write("See more details about how we built this open-source model.")


with col2:
    st.markdown("#### 👥 About us")
    st.write("Meet and discover the team that worked on this project.")


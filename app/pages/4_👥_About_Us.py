import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="About Us",
    page_icon="👥",
)

# Title of the page
st.title('About Us')

# Introduction about the team
st.header('Our Team')
st.write("Our team is composed of three engineering students specializing in Data Science and Artificial Intelligence at ESILV. This project was part of our 'Python for Data Analysis' course. We choosed to work on this particular problem due to our interest in the practical application of AI within the healthcare sector, a field where we believe concrete projects can make a significant impact.")

st.write("""
- **Louis COCKENPOT**
- **Foucauld ESTIGNARD**
- **Hector MELL MARIOLLE**
""")



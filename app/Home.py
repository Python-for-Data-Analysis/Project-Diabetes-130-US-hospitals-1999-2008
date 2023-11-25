import streamlit as st

st.set_page_config(
    page_title="LFH",
    page_icon="🏥",
)

# Display the blue banner
st.markdown('<div class="banner"><h1>LFH Hospital</h1></div>', unsafe_allow_html=True)

# Adjust the layout by adding space before the buttons
st.write("\n" * 8)  # Adjust the number to increase or decrease the space

# CSS personnalisé pour augmenter la taille des boutons et pour l'espacement
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 3em;      /* Hauteur du bouton */
        width: 100%;      /* Largeur du bouton (100% de la largeur disponible) */
        font-size: 1.5em; /* Taille de la police */
        margin: 5px 0;    /* Marge au-dessus et en dessous du bouton */
    }
    /* Custom CSS pour supprimer le padding par défaut de Streamlit autour des widgets */
    .st-cx {
        padding: 0px;
    }
    </style>
""", unsafe_allow_html=True)

#st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Welcome to LFH Hospital.\n
    Our job is to understand [...]\n
    Link to ppt
"""
)
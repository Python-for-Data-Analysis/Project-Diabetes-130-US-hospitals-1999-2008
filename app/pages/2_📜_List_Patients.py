import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="List Patients", page_icon="🏥")

st.markdown("# List Patients")
st.sidebar.header("List Patients")


# Function to load and preprocess data
def load_data():
    df = pd.read_csv('app/asset/diabetic_data.csv')
    # Convert readmission status to a categorical variable with color coding
    df['readmit_color'] = np.where(df['readmitted'] == '<30', 'red', 'green')
    return df


# Function to display the table with color coding
def color_row(row):
    # Define colors with transparency using rgba
    red_color = 'rgba(255, 0, 0, 0.5)'  # 50% transparency
    green_color = 'rgba(0, 255, 0, 0.5)'  # 50% transparency

    if row['readmit_color'] == 'red':
        return [f'background-color: {red_color}'] * len(row)
    else:
        return [f'background-color: {green_color}'] * len(row)


def display_table(df):
    st.write("Patients Table")

    # Pagination settings
    rows_per_page = 25
    n_pages = len(df) // rows_per_page + (1 if len(df) % rows_per_page else 0)
    page_number = st.number_input('Page Number', min_value=1, max_value=n_pages, value=1)
    start_row = (page_number - 1) * rows_per_page
    end_row = start_row + rows_per_page

    # Display the subset of the dataframe
    subset_df = df.iloc[start_row:end_row]

    # Apply the styling
    st.dataframe(subset_df.style.apply(color_row, axis=1))


# Function to display figures for variable distribution
def display_figures(df):
    st.write("### Distribution Figures")

    # Set the Seaborn style
    sns.set_style("darkgrid")

    # Example variables: 'age', 'time_in_hospital', 'num_medications'
    variables = ['age', 'time_in_hospital', 'num_medications']

    for variable in variables:
        fig, ax = plt.subplots(figsize=(10, 6))  # Larger figure size

        # Generate a color palette that fades
        palette = sns.light_palette("navy", reverse=True)

        # Use a more complex plot type like a histogram with a KDE
        sns.histplot(df[variable], kde=False, ax=ax, palette=palette)

        # Customize plot elements
        ax.set_xlabel(variable.title().replace("_", " "), fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)

        # Remove top and right spines for a cleaner look
        sns.despine()
        st.markdown(f"<h3 style='text-align: center; color: lightblue;'>Distribution of {variable.title()}</h3>", unsafe_allow_html=True)
        st.pyplot(fig)


df = load_data()
display_table(df)
display_figures(df)
st.markdown("<p style='text-align: center; color: lightblue;'>As a reminder, num_medication is the number of distinct "
            "generic drugs administered during the encounter.</p>", unsafe_allow_html=True)


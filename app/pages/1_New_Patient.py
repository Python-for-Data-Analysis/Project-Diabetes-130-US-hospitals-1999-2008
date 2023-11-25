import streamlit as st
import time
import numpy as np
import pandas as pd


st.set_page_config(page_title="New Patient", page_icon="🏥")

st.markdown("# New Patient")
st.sidebar.header("New Patient")
st.write(
    """Is he gonna come back ?"""
)



admission_type_descriptions = {
    "Emergency": 1,
    "Urgent": 2,
    "Elective": 3,
    "Newborn": 4,
    #"Not Available": 5,
    #"NULL": 6,
    "Trauma Center": 7,
    #"Not Mapped": 8
}

discharge_disposition_descriptions = {
    "Discharged to home": 1,
    "Discharged/transferred to another short term hospital": 2,
    "Discharged/transferred to SNF": 3,
    "Discharged/transferred to ICF": 4,
    "Discharged/transferred to another type of inpatient care institution": 5,
    "Discharged/transferred to home with home health service": 6,
    "Left AMA": 7,
    "Discharged/transferred to home under care of Home IV provider": 8,
    "Admitted as an inpatient to this hospital": 9,
    "Neonate discharged to another hospital for neonatal aftercare": 10,
    "Expired": 11,
    "Still patient or expected to return for outpatient services": 12,
    "Hospice / home": 13,
    "Hospice / medical facility": 14,
    "Discharged/transferred within this institution to Medicare approved swing bed": 15,
    "Discharged/transferred/referred another institution for outpatient services": 16,
    "Discharged/transferred/referred to this institution for outpatient services": 17,
    #"NULL": 18,
    "Expired at home. Medicaid only, hospice.": 19,
    "Expired in a medical facility. Medicaid only, hospice.": 20,
    "Expired, place unknown. Medicaid only, hospice.": 21,
    "Discharged/transferred to another rehab fac including rehab units of a hospital": 22,
    "Discharged/transferred to a long term care hospital.": 23,
    "Discharged/transferred to a nursing facility certified under Medicaid but not certified under Medicare.": 24,
    #"Not Mapped": 25,
    #"Unknown/Invalid": 26,
    "Discharged/transferred to a federal health care facility.": 27,
    "Discharged/transferred/referred to a psychiatric hospital of psychiatric distinct part unit of a hospital": 28,
    "Discharged/transferred to a Critical Access Hospital (CAH)": 29,
    "Discharged/transferred to another Type of Health Care Institution not Defined Elsewhere": 30
}


admission_source_descriptions = {
    "Physician Referral": 1,
    "Clinic Referral": 2,
    "HMO Referral": 3,
    "Transfer from a hospital": 4,
    "Transfer from a Skilled Nursing Facility (SNF)": 5,
    "Transfer from another health care facility": 6,
    "Emergency Room": 7,
    "Court/Law Enforcement": 8,
    "Not Available": 9,
    "Transfer from critial access hospital": 10,
    "Normal Delivery": 11,
    "Premature Delivery": 12,
    "Sick Baby": 13,
    "Extramural Birth": 14,
    "Not Available": 15,
    "NULL": 17,
    "Transfer From Another Home Health Agency": 18,
    "Readmission to Same Home Health Agency": 19,
    "Not Mapped": 20,
    "Unknown/Invalid": 21,
    "Transfer from hospital inpt/same fac reslt in a sep claim": 22,
    "Born inside this hospital": 23,
    "Born outside this hospital": 24,
    "Transfer from Ambulatory Surgery Center": 25,
    "Transfer from Hospice": 26
}


admission_source_dict = {
    1: 2, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3, 7: 4, 8: 4, 9: 1, 10: 3,
    11: 1, 12: 4, 13: 4, 14: 3, 15: 1, 17: 1, 18: 2, 19: 2, 20: 1,
    21: 1, 22: 3, 23: 1, 24: 3, 25: 2, 26: 4
}

age_dict = {
    "[0-10)":5,
    "[10-20)":15,
    "[20-30)":25,
    "[30-40)":35,
    "[40-50)":45,
    "[50-60)":55,
    "[60-70)":65,
    "[70-80)":75,
    "[80-90)":85,
    "[90-100)":95}

discharged_dict = {
    1: 1, 2: 3, 3: 2, 4: 2, 5: 3, 6: 2, 7: 4, 8: 2, 9: 3, 10: 3,
    11: 5, 12: 2, 13: 4, 14: 4, 15: 2, 16: 2, 17: 2, 18: 1, 19: 5,
    20: 5, 21: 5, 22: 2, 23: 2, 24: 2, 25: 1, 26: 1, 27: 2, 28: 3,
    29: 3, 30: 3
}

def encode_data(dataFrame):
    
    data=dataFrame.copy()
    data['age'] = data['age'].apply(lambda x: age_dict[x])
    data['gender'] = data['gender'].map({'Male': 0, 'Female': 1})
    data['diabetesMed'] = data['diabetesMed'].map({'Yes': 1, 'No': 0})
    data['change'] = data['change'].map({'No': 0, 'Ch': 1})
    for col in ["metformin", "repaglinide", "nateglinide", "chlorpropamide", "glimepiride", "acetohexamide", "glipizide", "glyburide", "tolbutamide", "pioglitazone", "rosiglitazone", "acarbose", "miglitol", "troglitazone", "tolazamide", "examide", "citoglipton", "insulin", "glyburide-metformin", "glipizide-metformin", "glimepiride-pioglitazone", "metformin-rosiglitazone", "metformin-pioglitazone"]:
        data[col] = data[col].apply(lambda x : 3 if x == 'Up'
                                                else ( 1 if x == 'Down'
                                                else ( 2 if x == 'Steady'
                                                else  0)))
    data["diag_1"] = data["diag_1"].apply(lambda x:map_icd9_to_category(x))
    data["diag_2"] = data["diag_2"].apply(lambda x:map_icd9_to_category(x))
    data["diag_3"] = data["diag_3"].apply(lambda x:map_icd9_to_category(x))
    data = pd.get_dummies(data, columns=["diag_1", "diag_2", "diag_3"], prefix=["diag_1", "diag_2", "diag_3"])
    data = pd.get_dummies(data, columns=["payer_code"], prefix=["payer_code"])
    data = pd.get_dummies(data, columns=["medical_specialty"], prefix=["medical_specialty"])

    data["discharge_disposition_id"] = data["discharge_disposition_id"].apply(lambda x:discharge_disposition_descriptions[x])
    data["admission_source_id"] = data["admission_source_id"].apply(lambda x:admission_source_descriptions[x])
    data["admission_type_id"]= data["admission_type_id"].apply(lambda x:admission_type_descriptions[x])
    data = pd.get_dummies(data, columns=["admission_type_id"], prefix=["admission_type_id"])
    
    data["discharge_disposition_id"] = data["discharge_disposition_id"].apply(lambda x:discharged_dict[x])
    data["admission_source_id"] = data["admission_source_id"].apply(lambda x:admission_source_dict[x])

    return data

def map_icd9_to_category(code):

    if code.startswith('250'):
        return 'Diabetes'
    elif code[0].isdigit():
        numeric_code = int(code.split('.')[0])
        if 1 <= numeric_code <= 139:
            return 'Infectious Diseases'
        elif 140 <= numeric_code <= 239:
            return 'Cancers and Neoplasms'
        elif 390 <= numeric_code <= 459:
            return 'Cardiovascular Diseases'
        elif (240 <= numeric_code <= 279) or \
             (280 <= numeric_code <= 289) or \
             (460 <= numeric_code <= 519):
            return 'Other Chronic Diseases'
        elif (290 <= numeric_code <= 319) or \
             (320 <= numeric_code <= 389):
            return 'Mental and Neurological Disorders'
        elif (520 <= numeric_code <= 579) or \
             (580 <= numeric_code <= 629) or \
             (680 <= numeric_code <= 709):
            return 'Digestive, Genitourinary, and Skin Disorders'
        elif (710 <= numeric_code <= 739) or \
             (740 <= numeric_code <= 759) or \
             (760 <= numeric_code <= 779):
            return 'Musculoskeletal, Connective Tissue, and Congenital Disorders'
        elif (780 <= numeric_code <= 799) or \
             (800 <= numeric_code <= 999):
            return 'General Symptoms, Injuries, and Other Conditions'
        else:
            return 'Uncategorized'
    elif code.startswith('V') or code.startswith('E'):
        return 'General Symptoms, Injuries, and Other Conditions'
    else:
        return 'Uncategorized'
    

def calculate_form_completion(**form_fields):
    total_fields = len(form_fields)
    filled_fields = sum(1 for value in form_fields.values() if value)
    return filled_fields / total_fields


# Start a form
with st.form("patient_data_form", clear_on_submit=True):
    st.write("Patient Encounter Form")

    # Text input for IDs and strings
    encounter_id = st.text_input("Encounter ID",0)
    patient_nbr = st.text_input("Patient Number",0)
    weight = st.text_input("Weight in pounds",0)

    # Selectboxes for categorical data
    race = st.selectbox("Race", ["Caucasian", "Asian", "African American", "Hispanic", "Other"])
    gender = st.selectbox("Gender", ["Male", "Female", "Unknown/Invalid"])
    age = st.selectbox("Age", [f"[{i}-{i+10})" for i in range(0, 100, 10)])
    payer_code = st.selectbox("Payer Code", ['Government Programs', 'Managed Care and Networks',
       'Private Insurance', 'Self-Pay and Other Plans',
       'Specialized Programs','Other'])
    medical_specialty = st.selectbox("Medical Specialty", ['General Practice and Internal Medicine','Surgery and Surgical Specialties','Pediatrics and Pediatric Subspecialties','Womens Health and Obstetrics/Gynecology',
                                                          'Specialized Organ and System Experts', 'Diagnostic and Therapeutic Services', 'Emergency Medicine and Critical Care','Other Specialties and Miscellaneous'])

    # Selectbox for admission type, discharge disposition, and admission source
    admission_type = st.selectbox("Admission Type", list(admission_type_descriptions.keys()))
    discharge_disposition = st.selectbox("Discharge Disposition", list(discharge_disposition_descriptions.keys()))
    admission_source = st.selectbox("Admission Source", list(admission_source_descriptions.keys()))

    # More numeric inputs
    time_in_hospital = st.number_input("Time in Hospital (days)", min_value=0)
    num_lab_procedures = st.number_input("Number of Lab Procedures", min_value=0)
    num_procedures = st.number_input("Number of Procedures", min_value=0)
    num_medications = st.number_input("Number of Medications", min_value=0)
    number_outpatient = st.number_input("Number of Outpatient Visits", min_value=0)
    number_emergency = st.number_input("Number of Emergency Visits", min_value=0)
    number_inpatient = st.number_input("Number of Inpatient Visits", min_value=0)

    # Text inputs for diagnosis codes
    diag_1 = st.text_input("Primary Diagnosis (ICD9 code)",150)
    diag_2 = st.text_input("Secondary Diagnosis (ICD9 code)",400)
    diag_3 = st.text_input("Additional Secondary Diagnosis (ICD9 code)",650)

    # Numeric input for diagnosis count
    number_diagnoses = st.number_input("Number of Diagnoses", min_value=0)

    # Medication related selectboxes with default "No"
    # Medication related selectboxes with default "No"
    meds = [
        "Metformin", "Repaglinide", "Nateglinide", "Chlorpropamide", "Glimepiride",
        "Acetohexamide", "Glipizide", "Glyburide", "Tolbutamide", "Pioglitazone",
        "Rosiglitazone", "Acarbose", "Miglitol", "Troglitazone", "Tolazamide",
        "Examide", "Citoglipton", "Insulin", "Glyburide-Metformin", "Glipizide-Metformin",
        "Glimepiride-Pioglitazone", "Metformin-Rosiglitazone", "Metformin-Pioglitazone"
    ]

    medication_data = {}
    for med in meds:
        medication_data[med] = st.selectbox(f"{med} Status", ["No", "Up", "Down", "Steady"], index=0)


    change = st.selectbox("Change in Diabetic Medications", ["Change", "No Change"])
    diabetesMed = st.selectbox("Diabetic Medication Prescribed", ["Yes", "No"])

    form_completion = calculate_form_completion(
    encounter_id=encounter_id,
    patient_nbr=patient_nbr,
    weight=weight,
    race=race,
    gender=gender,
    age=age,
    admission_type=admission_type,
    discharge_disposition=discharge_disposition,
    admission_source=admission_source,
    time_in_hospital=time_in_hospital,
    payer_code=payer_code,
    medical_specialty=medical_specialty,
    num_lab_procedures=num_lab_procedures,
    num_procedures=num_procedures,
    num_medications=num_medications,
    number_outpatient=number_outpatient,
    number_emergency=number_emergency,
    number_inpatient=number_inpatient,
    diag_1=diag_1,
    diag_2=diag_2,
    diag_3=diag_3,
    number_diagnoses=number_diagnoses,
    metformin=medication_data["Metformin"],
    repaglinide=medication_data["Repaglinide"],
    nateglinide=medication_data["Nateglinide"],
    chlorpropamide=medication_data["Chlorpropamide"],
    glimepiride=medication_data["Glimepiride"],
    acetohexamide=medication_data["Acetohexamide"],
    glipizide=medication_data["Glipizide"],
    glyburide=medication_data["Glyburide"],
    tolbutamide=medication_data["Tolbutamide"],
    pioglitazone=medication_data["Pioglitazone"],
    rosiglitazone=medication_data["Rosiglitazone"],
    acarbose=medication_data["Acarbose"],
    miglitol=medication_data["Miglitol"],
    troglitazone=medication_data["Troglitazone"],
    tolazamide=medication_data["Tolazamide"],
    examide=medication_data["Examide"],
    citoglipton=medication_data["Citoglipton"],
    insulin=medication_data["Insulin"],
    glyburide_metformin=medication_data["Glyburide-Metformin"],
    glipizide_metformin=medication_data["Glipizide-Metformin"],
    glimepiride_pioglitazone=medication_data["Glimepiride-Pioglitazone"],
    metformin_rosiglitazone=medication_data["Metformin-Rosiglitazone"],
    metformin_pioglitazone=medication_data["Metformin-Pioglitazone"],
    change=change,
    diabetesMed=diabetesMed
    )

    #st.progress(form_completion)


    # Form submission button
    submitted = st.form_submit_button("Submit")

    metformin=medication_data["Metformin"]
    repaglinide=medication_data["Repaglinide"],
    nateglinide=medication_data["Nateglinide"],
    chlorpropamide=medication_data["Chlorpropamide"],
    glimepiride=medication_data["Glimepiride"],
    acetohexamide=medication_data["Acetohexamide"],
    glipizide=medication_data["Glipizide"],
    glyburide=medication_data["Glyburide"],
    tolbutamide=medication_data["Tolbutamide"],
    pioglitazone=medication_data["Pioglitazone"],
    rosiglitazone=medication_data["Rosiglitazone"],
    acarbose=medication_data["Acarbose"],
    miglitol=medication_data["Miglitol"],
    troglitazone=medication_data["Troglitazone"],
    tolazamide=medication_data["Tolazamide"],
    examide=medication_data["Examide"],
    citoglipton=medication_data["Citoglipton"],
    insulin=medication_data["Insulin"],
    glyburide_metformin=medication_data["Glyburide-Metformin"],
    glipizide_metformin=medication_data["Glipizide-Metformin"],
    glimepiride_pioglitazone=medication_data["Glimepiride-Pioglitazone"],
    metformin_rosiglitazone=medication_data["Metformin-Rosiglitazone"],
    metformin_pioglitazone=medication_data["Metformin-Pioglitazone"],


    data_retrieved=[encounter_id,patient_nbr,weight,race,gender,age,admission_type,discharge_disposition,admission_source,time_in_hospital,payer_code,medical_specialty,num_lab_procedures,num_procedures,num_medications,
    number_outpatient,number_emergency,number_inpatient,diag_1,diag_2,diag_3,number_diagnoses,metformin,repaglinide,nateglinide,chlorpropamide,glimepiride,acetohexamide,glipizide,glyburide,tolbutamide,pioglitazone,
    rosiglitazone,acarbose,miglitol,troglitazone,tolazamide,examide,citoglipton,insulin,glyburide_metformin,glipizide_metformin,glimepiride_pioglitazone,metformin_rosiglitazone,metformin_pioglitazone,change,diabetesMed]


    columns_name=['encounter_id', 'patient_nbr', 'weight','race', 'gender', 'age', 
       'admission_type_id', 'discharge_disposition_id', 'admission_source_id',
       'time_in_hospital', 'payer_code', 'medical_specialty',
       'num_lab_procedures', 'num_procedures', 'num_medications',
       'number_outpatient', 'number_emergency', 'number_inpatient', 'diag_1',
       'diag_2', 'diag_3', 'number_diagnoses',
       'metformin', 'repaglinide', 'nateglinide', 'chlorpropamide',
       'glimepiride', 'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide',
       'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone',
       'tolazamide', 'examide', 'citoglipton', 'insulin',
       'glyburide-metformin', 'glipizide-metformin',
       'glimepiride-pioglitazone', 'metformin-rosiglitazone',
       'metformin-pioglitazone', 'change', 'diabetesMed']
    

    


    if submitted:
        # Convert descriptions to IDs
        admission_type_id = admission_type_descriptions[admission_type]
        discharge_disposition_id = discharge_disposition_descriptions[discharge_disposition]
        admission_source_id = admission_source_descriptions[admission_source]

        # Add the data in a dataframe
        dict={}
        for i in range(len(columns_name)):
            dict[columns_name[i]]=data_retrieved[i]
        
        
        new_data=pd.DataFrame(dict)

        final_data=encode_data(new_data)
        final_data.to_csv('test.csv')
        # Process and display the form data (or handle it as required)
        st.write("Form submitted!")
        st.write("Admission Type ID:", admission_type_id)
        # Display other processed data as required



st.button("Re-run")


import pandas as pd

import streamlit as st
import time
import pandas as pd
import random

st.set_page_config(page_title="New Patient", page_icon="🏥")

st.markdown("# New Patient")
#st.sidebar.header("New Patient")
st.write(
    """Fill these information if you want to know not only if the patient is likely to be readmitted within the next month but also how likely it is and more importantly **why**:"""
)

admission_type_descriptions = {
    "Emergency": 1,
    "Urgent": 2,
    "Elective": 3,
    "Newborn": 4,
    # "Not Available": 5,
    # "NULL": 6,
    "Trauma Center": 7,
    # "Not Mapped": 8
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
    # "NULL": 18,
    "Expired at home. Medicaid only, hospice.": 19,
    "Expired in a medical facility. Medicaid only, hospice.": 20,
    "Expired, place unknown. Medicaid only, hospice.": 21,
    "Discharged/transferred to another rehab fac including rehab units of a hospital": 22,
    "Discharged/transferred to a long term care hospital.": 23,
    "Discharged/transferred to a nursing facility certified under Medicaid but not certified under Medicare.": 24,
    # "Not Mapped": 25,
    # "Unknown/Invalid": 26,
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

payer_codes = ['MC', 'MD', 'CH', 'OG', 'UN', 'BC', 'CM', 'MP', 'HM', 'PO', 'SP', 'CP', 'SI', 'WC', 'FR', 'DM', 'OT']

medical_spe = ['Pediatrics-Endocrinology', None, 'InternalMedicine',
               'Family/GeneralPractice', 'Cardiology', 'Surgery-General',
               'Orthopedics', 'Gastroenterology',
               'Surgery-Cardiovascular/Thoracic', 'Nephrology',
               'Orthopedics-Reconstructive', 'Psychiatry', 'Emergency/Trauma',
               'Pulmonology', 'Surgery-Neuro',
               'Obsterics&Gynecology-GynecologicOnco', 'ObstetricsandGynecology',
               'Pediatrics', 'Hematology/Oncology', 'Otolaryngology',
               'Surgery-Colon&Rectal', 'Pediatrics-CriticalCare', 'Endocrinology',
               'Urology', 'Psychiatry-Child/Adolescent', 'Pediatrics-Pulmonology',
               'Neurology', 'Anesthesiology-Pediatric', 'Radiology',
               'Pediatrics-Hematology-Oncology', 'Psychology', 'Podiatry',
               'Gynecology', 'Oncology', 'Pediatrics-Neurology',
               'Surgery-Plastic', 'Surgery-Thoracic',
               'Surgery-PlasticwithinHeadandNeck', 'Ophthalmology',
               'Surgery-Pediatric', 'Pediatrics-EmergencyMedicine',
               'PhysicalMedicineandRehabilitation', 'InfectiousDiseases',
               'Anesthesiology', 'Rheumatology', 'AllergyandImmunology',
               'Surgery-Maxillofacial', 'Pediatrics-InfectiousDiseases',
               'Pediatrics-AllergyandImmunology', 'Dentistry', 'Surgeon',
               'Surgery-Vascular', 'Osteopath', 'Psychiatry-Addictive',
               'Surgery-Cardiovascular', 'PhysicianNotFound', 'Hematology',
               'Proctology', 'Obstetrics', 'SurgicalSpecialty', 'Radiologist',
               'Pathology', 'Dermatology', 'SportsMedicine', 'Speech',
               'Hospitalist', 'OutreachServices', 'Cardiology-Pediatric',
               'Perinatology', 'Neurophysiology', 'Endocrinology-Metabolism',
               'DCPTEAM', 'Resident']


def calculate_form_completion(**form_fields):
    total_fields = len(form_fields)
    filled_fields = sum(1 for value in form_fields.values() if value)
    return filled_fields / total_fields


# Créer un nombre aléatoire entre 10000 et 100000 pour l'id du patient
def random_numer():
    random_number = random.randint(10000, 100000)
    return random_number


encouter_id_val = random_numer()
patient_number_val = random_numer()

# Start a form
with st.form("patient_data_form", clear_on_submit=True):
    st.write("Patient Encounter Form")

    # Text input for IDs
    encounter_id = st.number_input('Encouter ID (auto)', value=encouter_id_val)
    patient_nbr = st.number_input('Patient Number (auto)', value=patient_number_val)
    # weight = st.text_input("Weight in pounds")

    # Selectboxes for categorical data
    race = st.selectbox("Race", ["Caucasian", "Asian", "African American", "Hispanic", "Other"])
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.selectbox("Age", [f"[{i}-{i + 10})" for i in range(0, 100, 10)])

    # Selectbox for admission type, discharge disposition, and admission source
    admission_type = st.selectbox("Admission Type", list(admission_type_descriptions.keys()))
    discharge_disposition = st.selectbox("Discharge Disposition", list(discharge_disposition_descriptions.keys()))
    admission_source = st.selectbox("Admission Source", list(admission_source_descriptions.keys()))
    payer_code = st.selectbox("Payer Code", payer_codes)
    medical_specialty = st.selectbox("Medical Specialty", medical_spe)

    # More numeric inputs
    time_in_hospital = st.number_input("Time in Hospital (days)", min_value=0)
    num_lab_procedures = st.number_input("Number of Lab Procedures", min_value=0)
    num_procedures = st.number_input("Number of Procedures", min_value=0)
    num_medications = st.number_input("Number of Medications", min_value=0)
    number_outpatient = st.number_input("Number of Outpatient Visits", min_value=0)
    number_emergency = st.number_input("Number of Emergency Visits", min_value=0)
    number_inpatient = st.number_input("Number of Inpatient Visits", min_value=0)

    # Text inputs for diagnosis codes
    diag_1 = st.text_input("Primary Diagnosis (ICD9 code)")
    diag_2 = st.text_input("Secondary Diagnosis (ICD9 code)")
    diag_3 = st.text_input("Additional Secondary Diagnosis (ICD9 code)")

    # Numeric input for diagnosis count
    number_diagnoses = st.number_input("Number of Diagnoses", min_value=0)
    max_glu_serum = st.selectbox("Maximum blood glucose serum", ['None', '>300', 'Norm', '>200'])
    A1Cresult = st.selectbox("A1C Test", ['None', '>7', '>8', 'Norm'])

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

    change = st.selectbox("Change in Diabetic Medications", ["No", "Ch"])
    diabetesMed = st.selectbox("Diabetic Medication Prescribed", ["Yes", "No"])

    form_completion = calculate_form_completion(
        encounter_id=encounter_id,
        patient_nbr=patient_nbr,
        race=race,
        gender=gender,
        age=age,
        # weight=weight,
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
        max_glu_serum=max_glu_serum,
        A1Cresult=A1Cresult,
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

    # st.progress(form_completion) ne marche pas ?

    # Form submission button
    submitted = st.form_submit_button("Submit")

    if submitted:
        # if not encounter_id or not patient_nbr or not weight or not diag_1 or not diag_2 or not diag_3:
        if not diag_1 or not diag_2 or not diag_3:
            st.error("Veuillez remplir tous les champs avant de soumettre.")

        else:
            # Convert descriptions to IDs
            admission_type_id = admission_type_descriptions[admission_type]

            patient_data = {
                "encounter_id": encounter_id,
                "patient_nbr": patient_nbr,
                # "weight": weight,
                "race": race,
                "gender": gender,
                "age": age,
                "admission_type_id": admission_type_id,
                "discharge_disposition_id": discharge_disposition_descriptions[discharge_disposition],
                "admission_source_id": admission_source_descriptions[admission_source],
                "time_in_hospital": time_in_hospital,
                "payer_code": payer_code,
                "medical_specialty": medical_specialty,
                "num_lab_procedures": num_lab_procedures,
                "num_procedures": num_procedures,
                "num_medications": num_medications,
                "number_outpatient": number_outpatient,
                "number_emergency": number_emergency,
                "number_inpatient": number_inpatient,
                "diag_1": diag_1,
                "diag_2": diag_2,
                "diag_3": diag_3,
                "number_diagnoses": number_diagnoses,
                "max_glu_serum": max_glu_serum,
                "A1Cresult": A1Cresult,
                "metformin": medication_data["Metformin"],
                "repaglinide": medication_data["Repaglinide"],
                "nateglinide": medication_data["Nateglinide"],
                "chlorpropamide": medication_data["Chlorpropamide"],
                "glimepiride": medication_data["Glimepiride"],
                "acetohexamide": medication_data["Acetohexamide"],
                "glipizide": medication_data["Glipizide"],
                "glyburide": medication_data["Glyburide"],
                "tolbutamide": medication_data["Tolbutamide"],
                "pioglitazone": medication_data["Pioglitazone"],
                "rosiglitazone": medication_data["Rosiglitazone"],
                "acarbose": medication_data["Acarbose"],
                "miglitol": medication_data["Miglitol"],
                "troglitazone": medication_data["Troglitazone"],
                "tolazamide": medication_data["Tolazamide"],
                "examide": medication_data["Examide"],
                "citoglipton": medication_data["Citoglipton"],
                "insulin": medication_data["Insulin"],
                "glyburide-metformin": medication_data["Glyburide-Metformin"],
                "glipizide-metformin": medication_data["Glipizide-Metformin"],
                "glimepiride-pioglitazone": medication_data["Glimepiride-Pioglitazone"],
                "metformin-rosiglitazone": medication_data["Metformin-Rosiglitazone"],
                "metformin-pioglitazone": medication_data["Metformin-Pioglitazone"],
                "change": change,
                "diabetesMed": diabetesMed
            }

            # Process and display the form data (or handle it as required)
            st.write("Form submitted!")
            st.write("Admission Type ID:", admission_type_id)

            # Convertir le dictionnaire en DataFrame
            patient_df = pd.DataFrame({key: [value] for key, value in patient_data.items()})

            # Afficher ou manipuler les données traitées
            st.write("Recap: ")
            st.write(patient_df)

            # Data Processing
            from collections import Counter
            from sklearn.ensemble import RandomForestClassifier            
            from sklearn.preprocessing import StandardScaler
            import joblib
            from joblib import load


            def preprocess(data):
                data.replace('?', None, inplace=True)
                data.drop(labels=["encounter_id", "patient_nbr"], axis=1, inplace=True)
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
                    "[90-100)":95
                }
                data['age'] = data['age'].apply(lambda x: age_dict[x])
                data['gender'] = data['gender'].map({'Male': 0, 'Female': 1})
                data['diabetesMed'] = data['diabetesMed'].map({'Yes': 1, 'No': 0})
                data['change'] = data['change'].map({'Ch': 1, 'No': 0})
                for col in ["metformin", "repaglinide", "nateglinide", "chlorpropamide", "glimepiride", "acetohexamide", "glipizide", "glyburide", "tolbutamide", "pioglitazone", "rosiglitazone", "acarbose", "miglitol", "troglitazone", "tolazamide", "examide", "citoglipton", "insulin", "glyburide-metformin", "glipizide-metformin", "glimepiride-pioglitazone", "metformin-rosiglitazone", "metformin-pioglitazone"]:
                    data[col] = data[col].apply(lambda x : 30 if x == 'Up'
                                                            else ( 10 if x == 'Down'
                                                            else ( 20 if x == 'Steady'
                                                            else  0)))                
                diag_1 = Counter(list(data['diag_1'])).most_common(1)[0][0]
                diag_2 = Counter(list(data['diag_2'])).most_common(1)[0][0]
                diag_3 = Counter(list(data['diag_3'])).most_common(1)[0][0]
                data['diag_1'] = data['diag_1'].apply(lambda x : diag_1 if x == None else x)
                data['diag_2'] = data['diag_2'].apply(lambda x : diag_2 if x == None else x)
                data['diag_3'] = data['diag_3'].apply(lambda x : diag_3 if x == None else x)
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
                data["diag_1"] = data["diag_1"].apply(lambda x:map_icd9_to_category(x))
                data["diag_2"] = data["diag_2"].apply(lambda x:map_icd9_to_category(x))
                data["diag_3"] = data["diag_3"].apply(lambda x:map_icd9_to_category(x))
                data = pd.get_dummies(data, columns=["diag_1", "diag_2", "diag_3"], prefix=["diag_1", "diag_2", "diag_3"])
                payer_code_mapping = {
                    'MC': 'Government Programs',
                    'MD': 'Government Programs',
                    'CH': 'Government Programs',
                    'OG': 'Government Programs',
                    'UN': 'Private Insurance',
                    'BC': 'Private Insurance',
                    'CM': 'Private Insurance',
                    'MP': 'Private Insurance',
                    'HM': 'Managed Care and Networks',
                    'PO': 'Managed Care and Networks',
                    'SP': 'Self-Pay and Other Plans',
                    'CP': 'Self-Pay and Other Plans',
                    'SI': 'Self-Pay and Other Plans',
                    'WC': 'Self-Pay and Other Plans',
                    'FR': 'Self-Pay and Other Plans',
                    'DM': 'Specialized Programs',
                    'OT': 'Other'
                }
                data['payer_code'] = data['payer_code'].map(payer_code_mapping)
                data['payer_code'].fillna('Other', inplace=True)
                data = pd.get_dummies(data, columns=["payer_code"], prefix=["payer_code"])
                categories = {
                    'General Practice and Internal Medicine': ['InternalMedicine', 'Family/GeneralPractice', 'Hospitalist', 'PhysicianNotFound', 'Resident', 'DCPTEAM', 'OutreachServices'],
                    'Surgery and Surgical Specialties': ['Surgery-General', 'Orthopedics', 'Surgery-Cardiovascular/Thoracic', 'Surgery-Neuro', 'Surgery-Colon&Rectal', 'Surgery-Plastic', 'Surgery-Thoracic', 'Surgery-PlasticwithinHeadandNeck', 'Surgery-Pediatric', 'Surgery-Vascular', 'Surgery-Maxillofacial', 'Surgery-Cardiovascular', 'SurgicalSpecialty'],
                    'Pediatrics and Pediatric Subspecialties': ['Pediatrics-Endocrinology', 'Pediatrics', 'Pediatrics-CriticalCare', 'Pediatrics-Pulmonology', 'Pediatrics-Hematology-Oncology', 'Pediatrics-Neurology', 'Pediatrics-EmergencyMedicine', 'Pediatrics-InfectiousDiseases', 'Pediatrics-AllergyandImmunology', 'Cardiology-Pediatric'],
                    'Women\'s Health and Obstetrics/Gynecology': ['Obsterics&Gynecology-GynecologicOnco', 'ObstetricsandGynecology', 'Gynecology', 'Obstetrics'],
                    'Specialized Organ and System Experts': ['Cardiology', 'Gastroenterology', 'Nephrology', 'Psychiatry', 'Pulmonology', 'Hematology/Oncology', 'Endocrinology', 'Urology', 'Neurology', 'Rheumatology', 'AllergyandImmunology', 'InfectiousDiseases', 'Dermatology', 'Neurophysiology', 'Endocrinology-Metabolism'],
                    'Diagnostic and Therapeutic Services': ['Radiology', 'Psychology', 'Anesthesiology', 'Podiatry', 'Ophthalmology', 'Pathology', 'Speech', 'PhysicalMedicineandRehabilitation'],
                    'Emergency Medicine and Critical Care': ['Emergency/Trauma', 'Anesthesiology-Pediatric', 'IntensiveCare', 'SportsMedicine', 'Perinatology'],
                    'Other Specialties and Miscellaneous': ['Otolaryngology', 'Psychiatry-Child/Adolescent', 'Psychiatry-Addictive', 'Dentistry', 'Surgeon', 'Osteopath', 'Hematology', 'Proctology', 'Radiologist']
                }
                specialty_to_category = {specialty: category for category, specialties in categories.items() for specialty in specialties}
                data['medical_specialty'] = data['medical_specialty'].map(specialty_to_category)
                data['medical_specialty'].fillna('Other', inplace=True)
                data = pd.get_dummies(data, columns=["medical_specialty"], prefix=["medical_specialty"])
                admission_dict = {
                    1:"Urgent",
                    2:"Urgent",
                    3:"Elective",
                    4:"Newborn",
                    5:"Other",
                    6:"Other",
                    7:"Other",
                    8:"Other"
                }
                data["admission_type_id"] = data["admission_type_id"].apply(lambda x:admission_dict[x])
                data = pd.get_dummies(data, columns=["admission_type_id"], prefix=["admission_type_id"])
                admission_source_dict = {
                    1: 2, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3, 7: 4, 8: 4, 9: 1, 10: 3,
                    11: 1, 12: 4, 13: 4, 14: 3, 15: 1, 17: 1, 18: 2, 19: 2, 20: 1,
                    21: 1, 22: 3, 23: 1, 24: 3, 25: 2, 26: 4
                }
                data["admission_source_id"] = data["admission_source_id"].apply(lambda x:admission_source_dict[x])
                discharged_dict = {
                    1: 1, 2: 3, 3: 2, 4: 2, 5: 3, 6: 2, 7: 4, 8: 2, 9: 3, 10: 3,
                    11: 5, 12: 2, 13: 4, 14: 4, 15: 2, 16: 2, 17: 2, 18: 1, 19: 5,
                    20: 5, 21: 5, 22: 2, 23: 2, 24: 2, 25: 1, 26: 1, 27: 2, 28: 3,
                    29: 3, 30: 3
                }
                data["discharge_disposition_id"] = data["discharge_disposition_id"].apply(lambda x:discharged_dict[x])
                colonnes_categ = ['A1Cresult', 'max_glu_serum']
                data = pd.get_dummies(data, columns=colonnes_categ)                                
                
                colonnes_to_keep = []
                colonnes_numeriques = [
                    'age', 'time_in_hospital', 'num_lab_procedures',
                    'num_procedures', 'num_medications', 'number_outpatient',
                    'number_emergency', 'number_inpatient', 'number_diagnoses'
                ]
                columns_is_significant = [
                    'discharge_disposition_id',
                    'admission_source_id',
                    'metformin',
                    'repaglinide',
                    'glipizide',
                    'insulin',
                    'change',
                    'diabetesMed',
                    'diag_1_Cancers and Neoplasms',
                    'diag_1_Cardiovascular Diseases',
                    'diag_1_Diabetes',
                    'diag_1_Digestive, Genitourinary, and Skin Disorders',
                    'diag_1_Musculoskeletal, Connective Tissue, and Congenital Disorders',
                    'diag_1_Uncategorized',
                    'diag_2_Cancers and Neoplasms',
                    'diag_2_Diabetes',
                    'diag_2_Digestive, Genitourinary, and Skin Disorders',
                    'diag_2_Other Chronic Diseases',
                    'diag_2_Uncategorized',
                    'diag_3_Cancers and Neoplasms',
                    'diag_3_Cardiovascular Diseases',
                    'diag_3_Diabetes',
                    'diag_3_Digestive, Genitourinary, and Skin Disorders',
                    'diag_3_Uncategorized',
                    'payer_code_Government Programs',
                    'payer_code_Managed Care and Networks',
                    'payer_code_Other',
                    'payer_code_Private Insurance',
                    'payer_code_Self-Pay and Other Plans',
                    'medical_specialty_Other',
                    'medical_specialty_Pediatrics and Pediatric Subspecialties',
                    'medical_specialty_Specialized Organ and System Experts',
                    'medical_specialty_Surgery and Surgical Specialties',
                    "medical_specialty_Women's Health and Obstetrics/Gynecology",
                    'admission_type_id_Elective',
                    'admission_type_id_Urgent',
                    'A1Cresult_>7',
                    'A1Cresult_>8',
                    'A1Cresult_Norm',
                    'max_glu_serum_>300'
                ]

                data_model_columns = [
                    'race', 'gender', 'age', 'discharge_disposition_id',
                    'admission_source_id', 'time_in_hospital', 'num_lab_procedures',
                    'num_procedures', 'num_medications', 'number_outpatient',
                    'number_emergency', 'number_inpatient', 'number_diagnoses', 'metformin',
                    'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride',
                    'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide',
                    'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone',
                    'tolazamide', 'examide', 'citoglipton', 'insulin',
                    'glyburide-metformin', 'glipizide-metformin',
                    'glimepiride-pioglitazone', 'metformin-rosiglitazone',
                    'metformin-pioglitazone', 'change', 'diabetesMed', 'readmitted',
                    'diag_1_Cancers and Neoplasms', 'diag_1_Cardiovascular Diseases',
                    'diag_1_Diabetes',
                    'diag_1_Digestive, Genitourinary, and Skin Disorders',
                    'diag_1_General Symptoms, Injuries, and Other Conditions',
                    'diag_1_Infectious Diseases',
                    'diag_1_Mental and Neurological Disorders',
                    'diag_1_Musculoskeletal, Connective Tissue, and Congenital Disorders',
                    'diag_1_Other Chronic Diseases', 'diag_1_Uncategorized',
                    'diag_2_Cancers and Neoplasms', 'diag_2_Cardiovascular Diseases',
                    'diag_2_Diabetes',
                    'diag_2_Digestive, Genitourinary, and Skin Disorders',
                    'diag_2_General Symptoms, Injuries, and Other Conditions',
                    'diag_2_Infectious Diseases',
                    'diag_2_Mental and Neurological Disorders',
                    'diag_2_Musculoskeletal, Connective Tissue, and Congenital Disorders',
                    'diag_2_Other Chronic Diseases', 'diag_2_Uncategorized',
                    'diag_3_Cancers and Neoplasms', 'diag_3_Cardiovascular Diseases',
                    'diag_3_Diabetes',
                    'diag_3_Digestive, Genitourinary, and Skin Disorders',
                    'diag_3_General Symptoms, Injuries, and Other Conditions',
                    'diag_3_Infectious Diseases',
                    'diag_3_Mental and Neurological Disorders',
                    'diag_3_Musculoskeletal, Connective Tissue, and Congenital Disorders',
                    'diag_3_Other Chronic Diseases', 'diag_3_Uncategorized',
                    'payer_code_Government Programs',
                    'payer_code_Managed Care and Networks', 'payer_code_Other',
                    'payer_code_Private Insurance', 'payer_code_Self-Pay and Other Plans',
                    'payer_code_Specialized Programs',
                    'medical_specialty_Diagnostic and Therapeutic Services',
                    'medical_specialty_Emergency Medicine and Critical Care',
                    'medical_specialty_General Practice and Internal Medicine',
                    'medical_specialty_Other',
                    'medical_specialty_Other Specialties and Miscellaneous',
                    'medical_specialty_Pediatrics and Pediatric Subspecialties',
                    'medical_specialty_Specialized Organ and System Experts',
                    'medical_specialty_Surgery and Surgical Specialties',
                    'medical_specialty_Women\'s Health and Obstetrics/Gynecology',
                    'admission_type_id_Elective', 'admission_type_id_Newborn',
                    'admission_type_id_Other', 'admission_type_id_Urgent', 'A1Cresult_>7',
                    'A1Cresult_>8', 'A1Cresult_Norm', 'max_glu_serum_>200',
                    'max_glu_serum_>300', 'max_glu_serum_Norm'
                ]

                # Trouver les colonnes qui sont dans data_model mais pas dans data
                colonnes_manquantes = set(data_model_columns) - set(data.columns)

                for colonne in colonnes_manquantes:
                    data[colonne] = 0

                # Convertir les bool en int
                for col in data.columns:
                    if data[col].dtype == 'bool':
                        data[col] = data[col].astype(int)

                # On remet les colonnes dans le bon ordre
                data = data[data_model_columns]

                colonnes_to_keep+=colonnes_numeriques
                colonnes_to_keep+=columns_is_significant                
                data = data[colonnes_to_keep]                

                scaler = load('models/scaler.pkl')
                data_scaled = scaler.transform(data)
                data = pd.DataFrame(data_scaled, index=data.index, columns=data.columns)
                return data
            

            with st.spinner('Predicting readmission risk...'):  # ajoute spinning pendant chargement
                progress_bar = st.progress(0)

                for i in range(100):
                    time.sleep(0.02)  # Simulating processing time
                    progress_bar.progress(i + 1)
                
                processed_df = preprocess(patient_df)
                model = load('models/best_rf.pkl')
                prediction = model.predict(processed_df)
                probabilities = model.predict_proba(processed_df)

            progress_bar.empty()

            # st.text(probabilities)
            # st.text(prediction)

            # Display prediction results
            if prediction == 0:
                st.success('Patient will not be readmitted within the next 30 days!')
            else:
                st.error('Patient will be readmitted within the next 30 days!')

            # encoded_dataframe=pd.read_csv('app/data_encoded.csv')
            # concatenated_dataframe = pd.concat([processed_df,encoded_dataframe], ignore_index=True)
            import shap
            import matplotlib.pyplot as plt

            explainer = shap.Explainer(model)
            shap_values = explainer(processed_df)
            st.subheader("SHAP Values for New Patient")
            shap.waterfall_plot(shap_values[0, :, 1], max_display=10)
            st.pyplot(plt)

st.button("Re-run")

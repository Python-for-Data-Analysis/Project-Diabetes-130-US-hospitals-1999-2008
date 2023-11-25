import pandas as pd


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
    data = pd.get_dummies(data, columns=["admission_type_id"], prefix=["admission_type_id"])

    data["discharge_disposition_id"] = data["discharge_disposition_id"].apply(lambda x:discharge_disposition_descriptions[x])
    data["admission_source_id"] = data["admission_source_id"].apply(lambda x:admission_source_descriptions[x])
    data["admission_type"]= data["discharge_disposition_id"].apply(lambda x:admission_type_descriptions[x])

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
    

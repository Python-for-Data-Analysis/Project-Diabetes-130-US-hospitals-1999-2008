import pandas as pd
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def preprocess(data):
    data.replace('?', None, inplace=True)
    data.drop(labels=["weight", "encounter_id", "patient_nbr"], axis=1, inplace=True)
    colonnes_categ = ['A1Cresult', 'max_glu_serum']
    data = pd.get_dummies(data, columns=colonnes_categ)
    age_dict = {
        "[0-10)": 5,
        "[10-20)": 15,
        "[20-30)": 25,
        "[30-40)": 35,
        "[40-50)": 45,
        "[50-60)": 55,
        "[60-70)": 65,
        "[70-80)": 75,
        "[80-90)": 85,
        "[90-100)": 95
    }
    data['age'] = data['age'].apply(lambda x: age_dict[x])
    data = data[data['gender'].isin(['Male', 'Female'])]  # We remove lines where the gender is not referenced
    data['gender'] = data['gender'].map({'Male': 0, 'Female': 1})
    data['diabetesMed'] = data['diabetesMed'].map({'Yes': 1, 'No': 0})
    data['change'] = data['change'].map({'No': 0, 'Ch': 1})
    for col in ["metformin", "repaglinide", "nateglinide", "chlorpropamide", "glimepiride", "acetohexamide",
                "glipizide", "glyburide", "tolbutamide", "pioglitazone", "rosiglitazone", "acarbose", "miglitol",
                "troglitazone", "tolazamide", "examide", "citoglipton", "insulin", "glyburide-metformin",
                "glipizide-metformin", "glimepiride-pioglitazone", "metformin-rosiglitazone", "metformin-pioglitazone"]:
        data[col] = data[col].apply(lambda x: 3 if x == 'Up'
        else (1 if x == 'Down'
              else (2 if x == 'Steady'
                    else 0)))

    diag_1 = Counter(list(data['diag_1'])).most_common(1)[0][0]
    diag_2 = Counter(list(data['diag_2'])).most_common(1)[0][0]
    diag_3 = Counter(list(data['diag_3'])).most_common(1)[0][0]
    data['diag_1'] = data['diag_1'].apply(lambda x: diag_1 if x == None else x)
    data['diag_2'] = data['diag_2'].apply(lambda x: diag_2 if x == None else x)
    data['diag_3'] = data['diag_3'].apply(lambda x: diag_3 if x == None else x)

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

    data["diag_1"] = data["diag_1"].apply(lambda x: map_icd9_to_category(x))
    data["diag_2"] = data["diag_2"].apply(lambda x: map_icd9_to_category(x))
    data["diag_3"] = data["diag_3"].apply(lambda x: map_icd9_to_category(x))
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
        'General Practice and Internal Medicine': ['InternalMedicine', 'Family/GeneralPractice', 'Hospitalist',
                                                   'PhysicianNotFound', 'Resident', 'DCPTEAM', 'OutreachServices'],
        'Surgery and Surgical Specialties': ['Surgery-General', 'Orthopedics', 'Surgery-Cardiovascular/Thoracic',
                                             'Surgery-Neuro', 'Surgery-Colon&Rectal', 'Surgery-Plastic',
                                             'Surgery-Thoracic', 'Surgery-PlasticwithinHeadandNeck',
                                             'Surgery-Pediatric', 'Surgery-Vascular', 'Surgery-Maxillofacial',
                                             'Surgery-Cardiovascular', 'SurgicalSpecialty'],
        'Pediatrics and Pediatric Subspecialties': ['Pediatrics-Endocrinology', 'Pediatrics', 'Pediatrics-CriticalCare',
                                                    'Pediatrics-Pulmonology', 'Pediatrics-Hematology-Oncology',
                                                    'Pediatrics-Neurology', 'Pediatrics-EmergencyMedicine',
                                                    'Pediatrics-InfectiousDiseases', 'Pediatrics-AllergyandImmunology',
                                                    'Cardiology-Pediatric'],
        'Women\'s Health and Obstetrics/Gynecology': ['Obsterics&Gynecology-GynecologicOnco', 'ObstetricsandGynecology',
                                                      'Gynecology', 'Obstetrics'],
        'Specialized Organ and System Experts': ['Cardiology', 'Gastroenterology', 'Nephrology', 'Psychiatry',
                                                 'Pulmonology', 'Hematology/Oncology', 'Endocrinology', 'Urology',
                                                 'Neurology', 'Rheumatology', 'AllergyandImmunology',
                                                 'InfectiousDiseases', 'Dermatology', 'Neurophysiology',
                                                 'Endocrinology-Metabolism'],
        'Diagnostic and Therapeutic Services': ['Radiology', 'Psychology', 'Anesthesiology', 'Podiatry',
                                                'Ophthalmology', 'Pathology', 'Speech',
                                                'PhysicalMedicineandRehabilitation'],
        'Emergency Medicine and Critical Care': ['Emergency/Trauma', 'Anesthesiology-Pediatric', 'IntensiveCare',
                                                 'SportsMedicine', 'Perinatology'],
        'Other Specialties and Miscellaneous': ['Otolaryngology', 'Psychiatry-Child/Adolescent', 'Psychiatry-Addictive',
                                                'Dentistry', 'Surgeon', 'Osteopath', 'Hematology', 'Proctology',
                                                'Radiologist']
    }

    specialty_to_category = {specialty: category for category, specialties in categories.items() for specialty in
                             specialties}

    data['medical_specialty'] = data['medical_specialty'].map(specialty_to_category)
    data['medical_specialty'].fillna('Other', inplace=True)
    data = pd.get_dummies(data, columns=["medical_specialty"], prefix=["medical_specialty"])
    data['readmitted'] = data['readmitted'].map({'NO': 0, '>30': 0, '<30': 1})
    admission_dict = {
        1: "Urgent",
        2: "Urgent",
        3: "Elective",
        4: "Newborn",
        5: "Other",
        6: "Other",
        7: "Other",
        8: "Other"
    }
    data["admission_type_id"] = data["admission_type_id"].apply(lambda x: admission_dict[x])
    data = pd.get_dummies(data, columns=["admission_type_id"], prefix=["admission_type_id"])

    # Separating rows where 'race' is not missing
    df_train = data[data['race'].notna()]
    df_predict = data[data['race'].isna()]

    X_train = df_train.drop('race', axis=1)
    y_train = df_train['race']
    X_predict = df_predict.drop('race', axis=1)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    # X_test = scaler.transform(X_test)

    rf = RandomForestClassifier(n_estimators=100, max_depth=25, criterion="gini", random_state=23)  # Training
    # rf = RandomForestClassifier()
    rf.fit(X_train, y_train)

    predicted_races = rf.predict(X_predict)  # Predicting
    # predicted_races = best_rf.predict(X_predict)

    data.loc[data['race'].isna(), 'race'] = predicted_races
    data = pd.get_dummies(data, 'race')
    # Severity of discharged type ranked from 1 to 5 (1 being the least severe)

    discharged_dict = {
        1: 1, 2: 3, 3: 2, 4: 2, 5: 3, 6: 2, 7: 4, 8: 2, 9: 3, 10: 3,
        11: 5, 12: 2, 13: 4, 14: 4, 15: 2, 16: 2, 17: 2, 18: 1, 19: 5,
        20: 5, 21: 5, 22: 2, 23: 2, 24: 2, 25: 1, 26: 1, 27: 2, 28: 3,
        29: 3, 30: 3
    }
    # Severity of admission type ranked from 1 to 5 (1 being the least severe)

    admission_source_dict = {
        1: 2, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3, 7: 4, 8: 4, 9: 1, 10: 3,
        11: 1, 12: 4, 13: 4, 14: 3, 15: 1, 17: 1, 18: 2, 19: 2, 20: 1,
        21: 1, 22: 3, 23: 1, 24: 3, 25: 2, 26: 4
    }
    data["discharge_disposition_id"] = data["discharge_disposition_id"].apply(lambda x: discharged_dict[x])
    data["admission_source_id"] = data["admission_source_id"].apply(lambda x: admission_source_dict[x])

    return data

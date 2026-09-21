"""
Master topic bank.
Add/remove/edit freely -- this is just a starting set covering the
major subjects an MBBS student hits across the years, so the daily
picks stay varied (one day medicine, next day surgery, next day peds...).

Each topic has:
  name     -> display name
  category -> broad subject, used only for variety/labels
  query    -> what gets searched on YouTube + Wikipedia
"""

TOPICS = [
    # Emergency / Critical Care
    {"name": "Anaphylactic Shock", "category": "Emergency Medicine", "query": "Anaphylactic shock"},
    {"name": "Cardiogenic Shock", "category": "Emergency Medicine", "query": "Cardiogenic shock"},
    {"name": "Septic Shock", "category": "Emergency Medicine", "query": "Septic shock"},
    {"name": "Status Epilepticus", "category": "Emergency Medicine", "query": "Status epilepticus"},
    {"name": "Acute Respiratory Distress Syndrome (ARDS)", "category": "Emergency Medicine", "query": "ARDS acute respiratory distress syndrome"},
    {"name": "Diabetic Ketoacidosis", "category": "Emergency Medicine", "query": "Diabetic ketoacidosis"},

    # Internal Medicine
    {"name": "Myocardial Infarction", "category": "Medicine", "query": "Myocardial infarction"},
    {"name": "Congestive Heart Failure", "category": "Medicine", "query": "Congestive heart failure"},
    {"name": "Chronic Kidney Disease", "category": "Medicine", "query": "Chronic kidney disease"},
    {"name": "Pulmonary Embolism", "category": "Medicine", "query": "Pulmonary embolism"},
    {"name": "Chronic Obstructive Pulmonary Disease (COPD)", "category": "Medicine", "query": "COPD chronic obstructive pulmonary disease"},
    {"name": "Rheumatoid Arthritis", "category": "Medicine", "query": "Rheumatoid arthritis"},
    {"name": "Systemic Lupus Erythematosus", "category": "Medicine", "query": "Systemic lupus erythematosus"},
    {"name": "Hypothyroidism", "category": "Medicine", "query": "Hypothyroidism"},
    {"name": "Hyperthyroidism / Graves Disease", "category": "Medicine", "query": "Graves disease hyperthyroidism"},
    {"name": "Cirrhosis of the Liver", "category": "Medicine", "query": "Liver cirrhosis"},
    {"name": "Peptic Ulcer Disease", "category": "Medicine", "query": "Peptic ulcer disease"},
    {"name": "Tuberculosis", "category": "Medicine", "query": "Tuberculosis pathophysiology"},
    {"name": "Anemia (Iron Deficiency)", "category": "Medicine", "query": "Iron deficiency anemia"},
    {"name": "Stroke (Ischemic)", "category": "Medicine", "query": "Ischemic stroke"},

    # Surgery
    {"name": "Acute Appendicitis", "category": "Surgery", "query": "Acute appendicitis"},
    {"name": "Cholecystitis / Gallstones", "category": "Surgery", "query": "Acute cholecystitis gallstones"},
    {"name": "Inguinal Hernia", "category": "Surgery", "query": "Inguinal hernia"},
    {"name": "Bowel Obstruction", "category": "Surgery", "query": "Small bowel obstruction"},
    {"name": "Peritonitis", "category": "Surgery", "query": "Peritonitis"},
    {"name": "Breast Cancer (Surgical Approach)", "category": "Surgery", "query": "Breast cancer surgery mastectomy"},
    {"name": "Thyroid Nodule / Thyroidectomy", "category": "Surgery", "query": "Thyroidectomy thyroid nodule"},
    {"name": "Burns Management", "category": "Surgery", "query": "Burns management surgery"},
    {"name": "Compartment Syndrome", "category": "Surgery", "query": "Compartment syndrome"},

    # Pediatrics
    {"name": "Neonatal Jaundice", "category": "Pediatrics", "query": "Neonatal jaundice"},
    {"name": "Congenital Heart Defects (VSD)", "category": "Pediatrics", "query": "Ventricular septal defect VSD"},
    {"name": "Kawasaki Disease", "category": "Pediatrics", "query": "Kawasaki disease"},
    {"name": "Cerebral Palsy", "category": "Pediatrics", "query": "Cerebral palsy"},
    {"name": "Rickets", "category": "Pediatrics", "query": "Rickets vitamin D deficiency"},

    # Obstetrics & Gynecology
    {"name": "Pre-eclampsia", "category": "OB-GYN", "query": "Pre-eclampsia"},
    {"name": "Ectopic Pregnancy", "category": "OB-GYN", "query": "Ectopic pregnancy"},
    {"name": "Postpartum Hemorrhage", "category": "OB-GYN", "query": "Postpartum hemorrhage"},
    {"name": "Polycystic Ovary Syndrome (PCOS)", "category": "OB-GYN", "query": "PCOS polycystic ovary syndrome"},

    # Neurology / Psychiatry
    {"name": "Parkinson's Disease", "category": "Neurology", "query": "Parkinson's disease"},
    {"name": "Multiple Sclerosis", "category": "Neurology", "query": "Multiple sclerosis"},
    {"name": "Epilepsy", "category": "Neurology", "query": "Epilepsy seizures"},
    {"name": "Major Depressive Disorder", "category": "Psychiatry", "query": "Major depressive disorder"},
    {"name": "Schizophrenia", "category": "Psychiatry", "query": "Schizophrenia"},

    # Dermatology / ENT / Ophthalmology
    {"name": "Psoriasis", "category": "Dermatology", "query": "Psoriasis"},
    {"name": "Acute Otitis Media", "category": "ENT", "query": "Acute otitis media"},
    {"name": "Sinusitis", "category": "ENT", "query": "Sinusitis"},
    {"name": "Cataract", "category": "Ophthalmology", "query": "Cataract"},
    {"name": "Glaucoma", "category": "Ophthalmology", "query": "Glaucoma"},

    # Infectious Disease
    {"name": "Dengue Fever", "category": "Infectious Disease", "query": "Dengue fever"},
    {"name": "Malaria", "category": "Infectious Disease", "query": "Malaria pathophysiology"},
    {"name": "Typhoid Fever", "category": "Infectious Disease", "query": "Typhoid fever"},
    {"name": "HIV / AIDS", "category": "Infectious Disease", "query": "HIV AIDS pathophysiology"},
    {"name": "Hepatitis B", "category": "Infectious Disease", "query": "Hepatitis B"},

    # Endocrine / Metabolic
    {"name": "Type 2 Diabetes Mellitus", "category": "Endocrine", "query": "Type 2 diabetes mellitus"},
    {"name": "Cushing's Syndrome", "category": "Endocrine", "query": "Cushing's syndrome"},
    {"name": "Addison's Disease", "category": "Endocrine", "query": "Addison's disease"},

    # Additional Medicine
    {"name": "Atrial Fibrillation", "category": "Cardiology", "query": "Atrial fibrillation"},
    {"name": "Aortic Stenosis", "category": "Cardiology", "query": "Aortic stenosis"},
    {"name": "Mitral Stenosis", "category": "Cardiology", "query": "Mitral stenosis"},
    {"name": "Infective Endocarditis", "category": "Cardiology", "query": "Infective endocarditis"},
    {"name": "Pericarditis", "category": "Cardiology", "query": "Acute pericarditis"},
    {"name": "Hypertension", "category": "Cardiology", "query": "Essential hypertension"},
    {"name": "Stable Angina", "category": "Cardiology", "query": "Stable angina"},
    {"name": "Deep Vein Thrombosis", "category": "Medicine", "query": "Deep vein thrombosis"},
    {"name": "Pneumonia", "category": "Respiratory Medicine", "query": "Community acquired pneumonia"},
    {"name": "Asthma", "category": "Respiratory Medicine", "query": "Bronchial asthma"},
    {"name": "Bronchiectasis", "category": "Respiratory Medicine", "query": "Bronchiectasis"},
    {"name": "Pleural Effusion", "category": "Respiratory Medicine", "query": "Pleural effusion"},
    {"name": "Pneumothorax", "category": "Respiratory Medicine", "query": "Pneumothorax"},
    {"name": "Obstructive Sleep Apnea", "category": "Respiratory Medicine", "query": "Obstructive sleep apnea"},
    {"name": "Interstitial Lung Disease", "category": "Respiratory Medicine", "query": "Interstitial lung disease"},
    {"name": "Acute Kidney Injury", "category": "Nephrology", "query": "Acute kidney injury"},
    {"name": "Nephrotic Syndrome", "category": "Nephrology", "query": "Nephrotic syndrome"},
    {"name": "Nephritic Syndrome", "category": "Nephrology", "query": "Nephritic syndrome"},
    {"name": "IgA Nephropathy", "category": "Nephrology", "query": "IgA nephropathy"},
    {"name": "Renal Tubular Acidosis", "category": "Nephrology", "query": "Renal tubular acidosis"},
    {"name": "Gastroesophageal Reflux Disease", "category": "Gastroenterology", "query": "Gastroesophageal reflux disease"},
    {"name": "Inflammatory Bowel Disease", "category": "Gastroenterology", "query": "Inflammatory bowel disease"},
    {"name": "Ulcerative Colitis", "category": "Gastroenterology", "query": "Ulcerative colitis"},
    {"name": "Crohn's Disease", "category": "Gastroenterology", "query": "Crohn's disease"},
    {"name": "Acute Pancreatitis", "category": "Gastroenterology", "query": "Acute pancreatitis"},
    {"name": "Hepatitis C", "category": "Gastroenterology", "query": "Hepatitis C"},
    {"name": "Acute Liver Failure", "category": "Gastroenterology", "query": "Acute liver failure"},
    {"name": "Hematemesis and Melena", "category": "Gastroenterology", "query": "Upper gastrointestinal bleeding"},
    {"name": "Irritable Bowel Syndrome", "category": "Gastroenterology", "query": "Irritable bowel syndrome"},
    {"name": "Celiac Disease", "category": "Gastroenterology", "query": "Celiac disease"},

    # Additional Neurology and Psychiatry
    {"name": "Alzheimer's Disease", "category": "Neurology", "query": "Alzheimer's disease"},
    {"name": "Meningitis", "category": "Neurology", "query": "Bacterial meningitis"},
    {"name": "Encephalitis", "category": "Neurology", "query": "Viral encephalitis"},
    {"name": "Guillain-Barre Syndrome", "category": "Neurology", "query": "Guillain-Barre syndrome"},
    {"name": "Myasthenia Gravis", "category": "Neurology", "query": "Myasthenia gravis"},
    {"name": "Amyotrophic Lateral Sclerosis", "category": "Neurology", "query": "Amyotrophic lateral sclerosis"},
    {"name": "Trigeminal Neuralgia", "category": "Neurology", "query": "Trigeminal neuralgia"},
    {"name": "Migraine", "category": "Neurology", "query": "Migraine"},
    {"name": "Tension Headache", "category": "Neurology", "query": "Tension headache"},
    {"name": "Delirium", "category": "Psychiatry", "query": "Delirium"},
    {"name": "Bipolar Disorder", "category": "Psychiatry", "query": "Bipolar disorder"},
    {"name": "Generalized Anxiety Disorder", "category": "Psychiatry", "query": "Generalized anxiety disorder"},
    {"name": "Obsessive Compulsive Disorder", "category": "Psychiatry", "query": "Obsessive compulsive disorder"},
    {"name": "Post-Traumatic Stress Disorder", "category": "Psychiatry", "query": "Post-traumatic stress disorder"},

    # Additional Infectious Disease
    {"name": "COVID-19", "category": "Infectious Disease", "query": "COVID-19"},
    {"name": "Influenza", "category": "Infectious Disease", "query": "Influenza"},
    {"name": "Measles", "category": "Infectious Disease", "query": "Measles"},
    {"name": "Mumps", "category": "Infectious Disease", "query": "Mumps"},
    {"name": "Rubella", "category": "Infectious Disease", "query": "Rubella"},
    {"name": "Varicella", "category": "Infectious Disease", "query": "Varicella chickenpox"},
    {"name": "Rabies", "category": "Infectious Disease", "query": "Rabies"},
    {"name": "Leptospirosis", "category": "Infectious Disease", "query": "Leptospirosis"},
    {"name": "Cholera", "category": "Infectious Disease", "query": "Cholera"},
    {"name": "Amoebiasis", "category": "Infectious Disease", "query": "Amoebiasis"},
    {"name": "Tetanus", "category": "Infectious Disease", "query": "Tetanus"},
    {"name": "Diphtheria", "category": "Infectious Disease", "query": "Diphtheria"},
    {"name": "Syphilis", "category": "Infectious Disease", "query": "Syphilis"},
    {"name": "Gonorrhea", "category": "Infectious Disease", "query": "Gonorrhea"},

    # Additional Surgery and Orthopedics
    {"name": "Hernia Complications", "category": "Surgery", "query": "Strangulated hernia"},
    {"name": "Intestinal Volvulus", "category": "Surgery", "query": "Intestinal volvulus"},
    {"name": "Hemorrhoids", "category": "Surgery", "query": "Hemorrhoids"},
    {"name": "Anal Fissure", "category": "Surgery", "query": "Anal fissure"},
    {"name": "Pilonidal Sinus", "category": "Surgery", "query": "Pilonidal sinus"},
    {"name": "Pancreatic Cancer", "category": "Surgery", "query": "Pancreatic cancer surgery"},
    {"name": "Colorectal Cancer", "category": "Surgery", "query": "Colorectal cancer"},
    {"name": "Fracture Healing", "category": "Orthopedics", "query": "Fracture healing"},
    {"name": "Osteoarthritis", "category": "Orthopedics", "query": "Osteoarthritis"},
    {"name": "Osteoporosis", "category": "Orthopedics", "query": "Osteoporosis"},
    {"name": "Osteomyelitis", "category": "Orthopedics", "query": "Osteomyelitis"},
    {"name": "Rheumatoid Hand", "category": "Orthopedics", "query": "Rheumatoid hand"},
    {"name": "Anterior Cruciate Ligament Injury", "category": "Orthopedics", "query": "Anterior cruciate ligament injury"},
    {"name": "Hip Fracture", "category": "Orthopedics", "query": "Hip fracture"},

    # Additional Pediatrics and OB-GYN
    {"name": "Bronchiolitis", "category": "Pediatrics", "query": "Bronchiolitis"},
    {"name": "Croup", "category": "Pediatrics", "query": "Croup"},
    {"name": "Pediatric Asthma", "category": "Pediatrics", "query": "Pediatric asthma"},
    {"name": "Acute Gastroenteritis in Children", "category": "Pediatrics", "query": "Pediatric acute gastroenteritis"},
    {"name": "Intussusception", "category": "Pediatrics", "query": "Intussusception"},
    {"name": "Pyloric Stenosis", "category": "Pediatrics", "query": "Infantile hypertrophic pyloric stenosis"},
    {"name": "Meningococcal Disease", "category": "Pediatrics", "query": "Meningococcal disease"},
    {"name": "Gestational Diabetes", "category": "OB-GYN", "query": "Gestational diabetes"},
    {"name": "Placental Abruption", "category": "OB-GYN", "query": "Placental abruption"},
    {"name": "Placenta Previa", "category": "OB-GYN", "query": "Placenta previa"},
    {"name": "Preeclampsia with Severe Features", "category": "OB-GYN", "query": "Severe preeclampsia"},
    {"name": "Endometriosis", "category": "OB-GYN", "query": "Endometriosis"},
    {"name": "Uterine Fibroids", "category": "OB-GYN", "query": "Uterine fibroids"},
    {"name": "Cervical Cancer", "category": "OB-GYN", "query": "Cervical cancer"},

    # Additional Dermatology, Ophthalmology, ENT, and Hematology
    {"name": "Atopic Dermatitis", "category": "Dermatology", "query": "Atopic dermatitis"},
    {"name": "Contact Dermatitis", "category": "Dermatology", "query": "Contact dermatitis"},
    {"name": "Acne Vulgaris", "category": "Dermatology", "query": "Acne vulgaris"},
    {"name": "Scabies", "category": "Dermatology", "query": "Scabies"},
    {"name": "Melanoma", "category": "Dermatology", "query": "Melanoma"},
    {"name": "Diabetic Retinopathy", "category": "Ophthalmology", "query": "Diabetic retinopathy"},
    {"name": "Acute Leukemia", "category": "Hematology", "query": "Acute leukemia"},
    {"name": "Lymphoma", "category": "Hematology", "query": "Lymphoma"},
]

# BMI6950 Final Project

## Contributors

| Name         | U#       | e-mail                |
| ------------ | -------- | --------------------- |
| Blake Dahl   | u0160015 | blake.dahl@utah.edu   |
| Kolton Hauck | u1019364 | kolton.hauck@utah.edu |

## Files

| Filename / Folder      | Description                                                                                                                                                     |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| README.md              | Basic information about the repo / project.                                                                                                                     |
| requirements.txt       | Python package requirements to run the app.                                                                                                                     |
| streamlit_test.py      | Python file to run streamlit app.                                                                                                                               |
| files/                 | Knowledge bases and patient files used in app.                                                                                                                  |
| files/patients/        | Patient files. Each folder corresponds to an individual patient.                                                                                                |
| files/knowledge_bases/ | Knowledge Base(s). Each folder corresponds to a knowledge base that can be loaded in the app.<br />Only 'cardiovascular' is implemented with minimal resources. |
| files/archive/         | Old versions of the code, unused utilities, or other unimplemented/untested knowledgebase files for various reasons.                                            |

## Description

Contained in this repository contains the proof-of-concept of supplying clinicians with the resources to make factual and relevant decisions in prescribing and determining the course of action for their patients. This is delivered in a chatbot-like interface. The user can select for specific patients (and only one at a time) along with specific knowledge bases to use as sources to augment the chatbot's response through a RAG approach.

The examples provided here are very basic, as this is just a proof-of-concept.

The UI is delivered through a Python package called [Streamlit](https://streamlit.io/gallery). These apps can be deployed locally or on the Streamlit Cloud.

The backend is developed primarily through [LangChain](https://python.langchain.com/docs/get_started/introduction).

## Instructions

### Getting Started

There are two ways to get started with this.

1. Streamlit Cloud

Simply go here: [BMI6950 Final Project - Streamlit Cloud](https://bmi6950finalproject.streamlit.app/) and enter your OpenAI API Key. Prompt away!

2. Run Locally

First, clone this repo. Change into the main folder of the repo `bmi6950_finalproject/`, install the required python packages listed in `requirements.txt`, then deploy the app using: `streamlit run streamlit_test.py`. Open a browser window to: `http://localhost:8501/`.

### Adding your own files

New patient files and knowledge base files can be added. To add new patient data, create a new folder under `files/patients/` and add any .pdfs related to the patient to that new folder. The name of that folder will be displayed in the dropdown when running the app. Likewise, to create a new knowledge base group, a new folder should be added to `files/knowledge_bases/`. Any .pdfs can then be added to this folder and loaded while running the app.

Only .pdfs can be used right now.

### How to Use

An OpenAI API key is required to run this app. To get one, go here: [OpenAI API Key](https://platform.openai.com/api-keys), and click on `Create new secret key`. Once generated, copy and paste it into the sidebar of the app while running. You should be notified when entered.

Once the API key is entered, you can start prompting. This will essentially be just like prompting ChatGPT in the UI. The specific model can be selected for in the sidebar as well.

There is a button at the bottom of the sidebar to clear the chat history.

There is an option to load a patient chart (none by default) and an option to load a knowledge base. Nothing will happen when these selections are made from the dropdown until the `Create VDB` button is selected. Only one patient can be loaded at a time. Only one knowledge base can be loaded at a time. But multiple files from a knowledge base can be selected.

When the `Create VDB` button is pressed, a vector DB will be generated for both the selected patient files and the knowledge base files. These are generated separately and the model has access to these DBs through a `MultiRetrievalQAChain`. (More LangChain chains can be found here: [Chains](https://python.langchain.com/docs/modules/chains)).

## Results

The `STEMI_Therapy_Guidelines.pdf` knowledge base and `p5-bd-stemi` patient were used for testing. Two primary prompts were tested: one without patient data loaded and one with patient data loaded. The results are outlined below.

### Prompt 1 (no patient data): "How would I implement adjunctive pharmacotherapy for a patient with STEMI?"

#### GPT-3.5-Turbo - No Knowledge base
> Adjunctive pharmacotherapy for a patient with ST-elevation myocardial infarction (STEMI) typically includes the following medications:
> 1. Aspirin: Administer a loading dose of aspirin (usually 162-325 mg) as soon as possible after the diagnosis of STEMI, followed by a daily maintenance dose of 75-100 mg.
> 2. P2Y12 inhibitor(e.g., clopidogrel, ticagrelor, prasugrel): Administer a loading dose of a P2Y12 inhibitor in addition to aspirin. The choice of P2Y12 inhibitor and the dose may vary depending on the patient's clinical characteristics and comorbidities.
> 3. Anticoagulants (e.g., heparin, enoxaparin, bivalirudin): Administer an anticoagulant to prevent further thrombus formation. The choice of anticoagulant and the dosing regiment may vary based on the patient's risk factors and bleeding risk.
> 4. Beta-blockers: Initiate beta-blocker therapy early in the course of STEMI unless contraindicated. Beta-blockers help reduce myocardial oxygen demand and improve outcomes in patients with STEMI.
> 5. ACE inhibitors or ARBs: Consider initiating ACE inhibitors or angiotensin receptor blockers (ARBs) in patients with STEMI and left ventricular dysfunction, heart failure, or hypertension.
> 6. Statins: Initiate high-intensity statin therapy in all patients with STEMI, regardless of baseline cholesterol levels, to reduce the risk of recurrent cardiovascular events.
> 7. Morphine: Consider administering morphine for pain relief in patients with ongoing chest discomfort despite treatment with antiplatelet agents and anticoagulants.
> It is important to individualize the pharmacotherapy based on the patient's clinical presentation, comorbidities, and contraindications. Close monitoring for adverse effects and drug interactions is essential to optimize outcomes in patients with STEMI.

#### GPT-3.5-Turbo - Yes Knowledge Base
> For a patient with STEMI, adjunctive pharmacotherapy can be implemented as follows:
>
> 1. Antiplatelets: Start with aspirin immediately, followed by a P2Y12 inhibitor like clopidogrel, prasugrel, or ticagrelor to prevent further clot formation.
> 2. Anticoagulants: Consider administering unfractionated heparin (UFH), enoxaparin, or bivalirudin, especially if the patient is undergoing PCI to prevent clot formation and maintain blood flow.
> 3. Beta-blockers: Early administration of beta-blockers like metoprolol or carvedilol is recommended unless contraindicated (e.g., heart failure, low output state). Beta-blockers can help reduce heart rate, blood pressure, and oxygen demand on the heart.
> 4. ACE Inhibitors: Consider initiating ACE inhibitors like lisinopril or ramipril within 24 hours for patients with left ventricular dysfunction, hypertension, or diabetes to improve outcomes and reduce the risk of heart failure.
> 5. Statins: Initiate high-intensity statin therapy, such as atorvastatin or rosuvastatin, as soon as possible to lower cholesterol levels and reduce the risk of future cardiovascular events.
> 
> It's crucial to consider contraindications for each therapy based on the patient's history and current clinical status, as well as any specific factors like hypertension, hyperlipidemia, diabetes, or previous cardiovascular events mentioned in the patient profile.

#### GPT-4-Turbo-Preview - No Knowledge base
> The management of ST-elevation myocardial infarction (STEMI) requires a comprehensive approach that includes prompt reperfusion therapy, typically with primary percutaneous coronary intervention (PCI) or, less commonly, thrombolytic therapy if PCI is not available within the recommended timeframe. Adjunctive pharmacotherapy plays a crucial role in the overall treatment strategy to improve outcomes, reduce complications, and support the reperfusion strategy. The following is an overview of the key components of adjunctive pharmacotherapy for a patient with STEMI, based on guidelines and best practices as of my last update in 2023. Always refer to the latest guidelines and consult with a cardiologist or specialist when managing a patient with STEMI.
> 
> Antiplatelet Agents:
>
> Aspirin: Administer a loading dose of non-enteric coated, chewable aspirin (usually 162-325 mg) as soon as possible after the onset of symptoms, followed by a daily maintenance dose (usually 81-100 mg).
P2Y12 Inhibitors: In addition to aspirin, a loading dose of a P2Y12 inhibitor is recommended. Options include clopidogrel, ticagrelor, or prasugrel. The choice of agent and dosing may depend on the planned reperfusion strategy, patient characteristics, and potential for drug-drug interactions.
> 
> Anticoagulants:
> Anticoagulation is necessary to prevent thrombus formation in the setting of PCI or thrombolytic therapy. Options include unfractionated heparin, low molecular weight heparin (e.g., enoxaparin), bivalirudin, or fondaparinux. The choice and duration of anticoagulant therapy depend on the reperfusion strategy, renal function, and risk of bleeding.
> 
> Beta-Blockers:
> Oral beta-blockers should be initiated within the first 24 hours in patients without contraindications (e.g., heart failure, low output state, risk of cardiogenic shock, or other contraindications to beta-blockade). Beta-blockers help reduce myocardial oxygen demand and limit the size of the infarct.
>
> ACE Inhibitors or ARBs:
> ACE inhibitors or angiotensin receptor blockers (ARBs) are recommended within the first 24 hours for patients with STEMI, particularly those with left ventricular systolic dysfunction, heart failure, or hypertension, unless contraindicated.
>
> Statin Therapy:
> High-intensity statin therapy should be initiated as soon as possible in all patients with STEMI, regardless of baseline LDL cholesterol levels, to stabilize plaques, reduce the risk of recurrent events, and improve survival.
>
> Nitroglycerin:
> Nitroglycerin may be used for symptomatic relief of ischemic chest pain unless contraindicated (e.g., right ventricular infarction, use of phosphodiesterase inhibitors).
>
> Glycoprotein IIb/IIIa Inhibitors:
> In certain cases, especially where there is evidence of ongoing ischemia or in the setting of percutaneous coronary intervention (PCI), glycoprotein IIb/IIIa inhibitors (e.g., abciximab, eptifibatide, tirofiban) may be considered, particularly in patients not pre-treated with a P2Y12 inhibitor.
>
> It's important to individualize therapy based on the patient's clinical presentation, contraindications, and the timing of presentation relative to symptom onset. Ongoing assessment and adjustments may be necessary. Coordination with a multidisciplinary team, including cardiology, is crucial for optimizing patient outcomes. Always consult the most current clinical guidelines and consider the patient's overall clinical context when making treatment decisions.

#### GPT-4-Turbo-Preview - Yes Knowledge base
> For a patient with STEMI, adjunctive pharmacotherapy plays a critical role in the management plan alongside the primary reperfusion therapy. Here is how you would implement adjunctive pharmacotherapy based on the provided guidelines:
> 1.	Antiplatelets:
> * Aspirin: Administer aspirin immediately as part of the initial treatment. Aspirin acts by inhibiting platelet aggregation, thus preventing further clot formation. The recommended dose for STEMI is a chewable 162-325 mg tablet given as soon as possible after symptom onset.
> * P2Y12 inhibitors: Following aspirin administration, add a P2Y12 inhibitor. The choice of P2Y12 inhibitor (e.g., clopidogrel, ticagrelor, or prasugrel) can depend on the patient's specific situation, including whether they are expected to undergo PCI and their risk of bleeding. These agents further prevent platelet aggregation.
> 2.	Anticoagulants:
> * Depending on whether the patient is undergoing PCI, choose between unfractionated heparin (UFH), enoxaparin, or bivalirudin. These agents prevent the formation and growth of thrombi by inhibiting factors in the coagulation cascade.
> * The choice and duration of anticoagulant therapy may vary based on the patient's risk profile and whether PCI is performed.
> 3.	Beta-blockers:
> * Early administration of beta-blockers is recommended unless contraindicated, such as in patients with heart failure or a low output state. Beta-blockers reduce myocardial oxygen demand by lowering heart rate and blood pressure, thus aiding in the management of STEMI.
> 4.	ACE Inhibitors:
> * Initiate ACE inhibitors within the first 24 hours for patients with left ventricular (LV) dysfunction, hypertension, or diabetes. ACE inhibitors help in reducing the workload on the heart by lowering blood pressure and have a protective effect on the heart muscle.
> 5.	Statins:
> * Start high-intensity statin therapy as soon as possible. Statins are crucial for managing cholesterol levels and stabilizing plaque, which can help prevent further cardiovascular events.
> When implementing this pharmacotherapy plan, always consider the patient's history and current clinical status to address any contraindications for each therapy. For instance, patients with a history of severe asthma or reactive airway disease may have contraindications to beta-blockers, and those with a history of severe renal impairment may not be suitable for certain doses or types of anticoagulants. Patient-specific factors such as history of hypertension, hyperlipidemia, diabetes, and previous cardiovascular events should also guide therapy adjustments.


### Prompt 2 (with patient data): "What treatments should I give this patient?"

#### GPT-3.5-Turbo - No Knowledge base
> Based on the provided information, the patient John Doe is presenting with a STEMI (ST-segment elevation myocardial infarction). The treatment for STEMI includes immediate reperfusion therapy, which can be achieved through either primary percutaneous coronary intervention (PCI) or fibrinolytic therapy. In addition to reperfusion therapy, other treatments for this patient may include:
> 1.	Aspirin: Immediate administration of aspirin to reduce platelet aggregation.
> 2.	P2Y12 Inhibitor (e.g., Clopidogrel, Ticagrelor, Prasugrel): To prevent further platelet activation and aggregation.
> 3.	Anticoagulant therapy (e.g., Heparin, Enoxaparin): To prevent clot formation.
> 4.	Beta-blockers: To reduce heart rate, blood pressure, and myocardial oxygen demand.
> 5.	ACE Inhibitors or ARBs: To improve outcomes and reduce mortality in patients with left ventricular dysfunction.
> 6.	Statin therapy: To manage hyperlipidemia and reduce the risk of future cardiovascular events.
> 7.	Glycemic control: Management of hyperglycemia in patients with diabetes mellitus.
> 8.	Oxygen therapy if oxygen saturation is low.
> Please note that the specific treatment plan and dosages should be determined by a healthcare professional based on the patient's individual clinical condition and any contraindications.

#### GPT-3.5-Turbo - Yes Knowledge base
> Based on the provided information, the patient John Doe is presenting with a STEMI (ST-segment elevation myocardial infarction). The appropriate treatments for this patient would include:
> 1.	Immediate reperfusion therapy: This can be achieved through either primary percutaneous coronary intervention (PCI) or fibrinolytic therapy, depending on the availability and timing of PCI facilities.
> 2.	Antiplatelet therapy: Administer aspirin and P2Y12 inhibitor (such as clopidogrel, ticagrelor, or prasugrel) to prevent further clot formation.
> 3.	Anticoagulant therapy: Use heparin or bivalirudin to prevent clot formation and extension.
> 4.	Beta-blockers: Initiate beta-blocker therapy to reduce heart rate, blood pressure, and myocardial oxygen demand.
> 5.	ACE inhibitors or ARBs: Start ACE inhibitors or ARBs to improve outcomes and reduce mortality in patients with left ventricular dysfunction post-MI.
> 6.	Statin therapy: Prescribe high-intensity statin therapy to lower LDL cholesterol levels and reduce the risk of future cardiovascular events.
> 7.	Blood sugar management: Control hyperglycemia with insulin therapy to optimize outcomes post-MI.
> 8.	Lifestyle modifications: Encourage smoking cessation, healthy diet, regular exercise, and weight management to improve overall cardiovascular health.
> It is crucial to individualize treatment based on the patient's specific clinical status and any contraindications. Consulting with a cardiologist or specialist is recommended for the optimal management of this patient.

#### GPT-4-Turbo-Preview - No Knowledge base  ** GPT-4-Turbo-Preview giving short responses - think it might have been going through an update **
> Based on the patient's symptoms and medical history, it would be best to start with a thorough physical examination and possibly some diagnostic tests to determine the underlying cause of their condition. Depending on the results, treatment options could include medication, physical therapy, surgery, or other interventions. It's important to consult with a healthcare professional for personalized recommendations.

#### GPT-4-Turbo-Preview - Yes Knowledge base ** GPT-4-Turbo-Preview giving short responses - think it might have been going through an update **
Tried a different prompt to prompt correctly: "Based on the guidelines, what treatments should I give this patient?"

> To recommend specific treatments based on the guidelines provided, I would need more details about the patient's current clinical status, including the time since symptom onset, ECG findings confirming STEMI, and any contraindications for therapies based on the patient's history and current clinical status. However, based on the general guidelines for STEMI management provided:
> 1.	Confirm STEMI Diagnosis: Ensure diagnosis via ECG showing ST-segment elevation.
> 2.	Initial Assessment: Determine the time since symptom onset to decide on the appropriate reperfusion strategy.
> 3.	Reperfusion Therapy:
> *	Primary PCI (Percutaneous Coronary Intervention): This is recommended if the symptom onset is within 12 hours and PCI can be performed within 90 minutes of first medical contact.
> * Fibrinolytic Therapy: Consider this if PCI is not available within 120 minutes and there are no contraindications, especially if within 12 hours of symptom onset.
> 4.	Adjunctive Pharmacotherapy:
> * Antiplatelets: Administer aspirin immediately, followed by a P2Y12 inhibitor.
> * Anticoagulants: Choose between unfractionated heparin (UFH), enoxaparin, or bivalirudin, especially if undergoing PCI.
> * Beta-blockers: Administer early unless contraindicated (e.g., heart failure, low output state).
> * ACE Inhibitors: Initiate within 24 hours for patients with LV dysfunction, hypertension, or diabetes.
> * Statins: Start high-intensity statin therapy as soon as possible.
> 5.	Risk Stratification: Use clinical findings, ECG, and echocardiography to assess risk and guide further therapy.
> 6.	Special Considerations: Always consider contraindications for each therapy based on patient history and current clinical status. Also, take into account patient-specific factors such as history of hypertension, hyperlipidemia, diabetes, and previous cardiovascular events.
> Without specific patient details, these are the general guidelines to follow for STEMI management.

It seems like the model didn't access the patient chart either based on that last line.

## Opportunities for Improvement

* an option to download current chat history
* an option to upload chat history
* expanding knowledge base (specifically within the 'cardiovascular' folder and more high-level topics)
* an option to customize model parameters such as temperature, top-p and top-k
* an option to customize the system prompt of the model
* a physical vector DB, rather one that is run in memory (FAISS was used)
* experimentation with other steps in the Vector DB process (text splitter, embeddings, etc)
* multi-modal implementations, so the model can read images and graphs, such as ECGs and make inferences about those
* a file viewer in the app, so one can see the knowledge base files as well as the patient files
* more complex charts and knowledge bases
* allow for multiple types of files (.pdf, .txt, .json, C-CDA, FHIR
*

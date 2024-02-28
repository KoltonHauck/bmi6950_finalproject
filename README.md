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

## Results - RAG

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

## Results - RAG + Chat
Here is a conversation using the same knowledge base and patient, demonstrating the models capabilites of chatting about the patient, knowledge base, and revising suggestions based on new information.

User:
> What can you tell me about the patient?

Assistant:
>  Based on the provided patient profile, John Doe is a 55-year-old male with a medical history significant for hypertension, hyperlipidemia, and type 2 diabetes mellitus, with no previous cardiovascular events. He presented with symptoms indicative of an acute myocardial infarction (AMI), specifically a ST-elevation myocardial infarction (STEMI), including chest pain radiating to the left arm, shortness of breath, sweating, with these symptoms beginning 2 hours prior to presentation.
>
> His vital signs upon presentation were: blood pressure of 150/90 mmHg, heart rate of 110 beats per minute, respiratory rate of 20 breaths per minute, and an oxygen saturation of 94% on room air, which indicates distress but no immediate hypoxia.
>
> Diagnostic findings further support the diagnosis of a STEMI. His electrocardiogram (ECG) showed ST-segment elevation in leads II, III, and aVF, which typically indicates an inferior wall myocardial infarction. Echocardiography revealed left ventricular dysfunction with an ejection fraction of 45%, suggesting some degree of heart failure or impaired cardiac function. Laboratory tests showed elevated cardiac biomarkers (Troponin I and Creatine Kinase-MB), indicating cardiac muscle injury. Additionally, his glucose level was elevated at 180 mg/dL, and his lipid profile showed elevated total cholesterol (220 mg/dL) and LDL cholesterol (150 mg/dL) with low HDL cholesterol (30 mg/dL), which are risk factors for atherosclerotic cardiovascular disease.
>
> Overall, the patient's presentation and diagnostic findings indicate an acute inferior wall STEMI with associated left ventricular dysfunction, in the context of his existing risk factors for coronary artery disease.

User:
> What therapies would you recommend?

Assistant:
> For a 55-year-old male presenting with an acute ST-elevation myocardial infarction (STEMI) with the clinical background and diagnostic findings provided, the following therapies would be recommended according to the STEMI Therapy Guidelines:
>
> 1. Reperfusion Therapy:
> * Primary PCI (Percutaneous Coronary Intervention): This is the preferred method for reperfusion given the diagnosis of STEMI, especially since the symptom onset is within 12 hours. The goal is to perform PCI within 90 minutes of first medical contact.
> 2. Adjunctive Pharmacotherapy:
> * Antiplatelets: Immediate administration of aspirin, followed by a P2Y12 inhibitor. Given the patient's history and current condition, clopidogrel, ticagrelor, or prasugrel (considering contraindications and drug interactions) could be considered.
> * Anticoagulants: Given the choice of undergoing PCI, anticoagulants such as unfractionated heparin (UFH), enoxaparin, or bivalirudin should be initiated.
> * Beta-blockers: Early administration is recommended unless contraindicated. Given the patient's heart rate and the absence of contraindications mentioned (e.g., heart failure, low output state not specified), a beta-blocker should be considered to reduce myocardial oxygen demand.
> * ACE Inhibitors: Should be initiated within 24 hours since the patient has left ventricular dysfunction, hypertension, and diabetes.
> * Statins: High-intensity statin therapy should be initiated as soon as possible, considering the patient's elevated LDL cholesterol and history of hyperlipidemia.
> 3. Risk Stratification and Management of Comorbidities:
> * Given the patient's history of hypertension, hyperlipidemia, and type 2 diabetes mellitus, ongoing management of these conditions is crucial. This includes optimizing blood pressure control, managing lipid levels aggressively, and controlling glucose levels.
> * The patient's left ventricular dysfunction (ejection fraction of 45%) further emphasizes the need for ACE inhibitors and careful monitoring of cardiac function.
> 4. Special Considerations:
> * Addressing contraindications for each therapy based on the patient's history and current clinical status is crucial.
> * Consideration of the patient's glucose level of 180 mg/dL at presentation; insulin therapy may be required to manage hyperglycemia in the acute setting, in addition to long-term glycemic control measures.
> 5. Monitoring and Follow-Up:
> * Close monitoring of vital signs, cardiac rhythm, response to therapy, and any signs of complications is essential.
> * Follow-up care should include cardiac rehabilitation, lifestyle modifications, and adherence to medications for secondary prevention.
> This management plan should be tailored based on the patient's response to initial therapies, any contraindications, and evolving clinical status.

User:
> Which specific P2Y12 inhibitor and anticoagulant should be selected for this patient considering their clinical profile?

Assistant:
> For a 55-year-old male presenting with an acute ST-elevation myocardial infarction (STEMI) and a history of hypertension, hyperlipidemia, and type 2 diabetes mellitus, the selection of a specific P2Y12 inhibitor and anticoagulant should be tailored to the patient's clinical status, including any contraindications, and the planned treatment strategy (e.g., primary PCI).
> P2Y12 Inhibitor: Given the patient's presentation and the absence of specific contraindications mentioned, any of the commonly used P2Y12 inhibitors could be considered. These include clopidogrel, ticagrelor, and prasugrel. However, considering the patient's risk factors and assuming no contraindications:
> * Ticagrelor or prasugrel are often preferred over clopidogrel due to their more potent and consistent platelet inhibition in patients undergoing PCI, unless there are specific contraindications to these drugs (e.g., history of stroke for prasugrel, severe liver impairment for ticagrelor). Prasugrel and ticagrelor have been shown to reduce ischemic events in patients with acute coronary syndromes, although they come with a higher risk of bleeding compared to clopidogrel.
> * Clopidogrel may be considered if there are contraindications to ticagrelor and prasugrel or if the patient is at a high risk of bleeding.
> Anticoagulant: For anticoagulation in the setting of STEMI, especially if undergoing primary PCI:
> * Unfractionated heparin (UFH), enoxaparin, or bivalirudin are options. The choice between these agents depends on the clinical scenario, including renal function (as enoxaparin is renally cleared) and potential need for CABG (as UFH has a shorter half-life and is easier to reverse).
> * Bivalirudin may be preferred in patients at high risk for bleeding or in those with a history of heparin-induced thrombocytopenia (HIT).
> * Unfractionated heparin is widely used due to its familiarity, ease of titration, and reversibility.
> * Enoxaparin has been shown in some studies to have a more predictable anticoagulant effect than UFH and may be used unless there is significant renal impairment.
> In summary, the choice of specific P2Y12 inhibitor and anticoagulant should consider the patient's overall clinical context, including renal function, risk of bleeding, and potential for surgery. Collaboration with a cardiologist and a careful review of the patient's history and contraindications are essential in making the best therapeutic decision.

User:
> What are the key side effects we should monitor for given the combination of therapies this patient is receiving?

Assistant:
> Given the combination of therapies recommended for STEMI management, monitoring for side effects is crucial to ensure patient safety and optimize outcomes. Here are the key side effects to monitor for each class of medication:
> 1. Antiplatelets (Aspirin and P2Y12 inhibitors):
> * Increased risk of bleeding, including gastrointestinal bleeding and intracranial hemorrhage.
> * Thrombocytopenia (low platelet count).
> * Dyspepsia or gastrointestinal discomfort with aspirin.
> 2. Anticoagulants (Unfractionated heparin, enoxaparin, bivalirudin):
> * Bleeding risk is the primary concern, including at puncture sites and potential for hematomas.
> * Heparin-induced thrombocytopenia (HIT), particularly with unfractionated heparin.
> * Osteoporosis with long-term use of heparin.
> 3. Beta-blockers:
> * Bradycardia (slow heart rate).
> * Hypotension (low blood pressure).
> * Fatigue and dizziness.
> * Worsening of symptoms in patients with asthma or chronic obstructive pulmonary disease (COPD).
> * Worsening of peripheral artery disease symptoms.
> 4. ACE Inhibitors:
> * Hypotension, especially after the first dose.
> * Chronic cough.
> * Hyperkalemia (high potassium levels).
> * Angioedema (swelling of the deeper layers of the skin, can be life-threatening if it involves the throat).
> * Renal function deterioration in certain patients.
> 5. Statins:
> * Myalgias (muscle aches) and myopathies.
> * Increased liver enzymes indicating potential liver damage.
> * Rarely, rhabdomyolysis (a severe muscle breakdown that can lead to kidney damage).
> * Diabetes mellitus, particularly with high-intensity statin therapy.
> For each of these medications, it's important to balance the benefits of therapy with the potential risks and side effects. Regular monitoring, including blood tests for liver and kidney function, platelet counts, and electrolytes, as well as vigilant clinical assessment for signs of bleeding, hypotension, or allergic reactions, is key to managing these patients safely. Adjustments to therapy may be necessary based on the patient's response and the emergence of side effects. Additionally, given the patient's history of hypertension, hyperlipidemia, diabetes, and previous cardiovascular events, close attention should be paid to managing these conditions in parallel to STEMI therapy.

User:
> New information regarding the patient has been received: the patient has had a stroke, has liver impairment and is at a high risk of bleeding. What P2Y12 inhibitor would you then recommend?

Assistant:
> Given the patient's history of stroke, liver impairment, and a high risk of bleeding, it's crucial to choose a P2Y12 inhibitor that balances the need for antiplatelet efficacy with the need to minimize bleeding risk and consider hepatic metabolism. However, without specific guidelines provided in the provided context regarding P2Y12 inhibitors for patients with these conditions, it's difficult to make a definitive recommendation.
> Generally, clopidogrel is often considered in patients with a history of stroke and those with liver impairment because it has a well-established safety profile, including in patients with hepatic dysfunction. Clopidogrel is metabolized by the liver, but it is often used in patients with liver impairment, albeit with careful monitoring. Its relatively lower potency compared to newer agents like ticagrelor or prasugrel may also pose a lesser risk of bleeding, which is particularly relevant in a patient at high risk of bleeding.
> However, the choice of a P2Y12 inhibitor should be individualized based on the patient's overall clinical condition, the presence of contraindications, the treating physician's assessment, and current clinical guidelines. It's important to consult current, evidence-based guidelines and consider a multidisciplinary approach involving cardiology, hepatology, and possibly hematology to make the best therapeutic decision for a patient with such complex issues.

User:
> So, given this patient and this context, which would you prescribe if you were the clinician?

Assistant:
> Based on the patient's history, I would recommend clopidogrel as the P2Y12 inhibitor of choice. Clopidogrel is metabolized in the liver and does not have significant interactions with medications that affect the liver. It also has a lower risk of bleeding compared to other P2Y12 inhibitors like prasugrel or ticagrelor. However, it's important to consult with the patient's healthcare provider for personalized recommendations.

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

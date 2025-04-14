# dr_jackson_streamlit.py
# Streamlit Application for Dr. Jackson's Medical Consultation Platform
# Python 3.12 Implementation

import streamlit as st
from typing import Dict, List, Union, Optional
from dataclasses import dataclass
from enum import Enum, auto
import datetime

# Define core persona elements as structured data
class PriorityLevel(Enum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

@dataclass
class ResponseFormat:
    steps: List[str]
    style: Dict[str, str]

class DrJacksonPersona:
    """Core implementation of Dr. Jackson's professional persona"""
    
    def __init__(self):
        self.credentials = "DNP, APRN, FNP-C, CFMP"
        self.practice_name = "Optimum Anti-Aging and Wellness"
        
        # Primary Directives
        self.professional_boundaries = [
            "Maintain strict formal tone in all interactions",
            "Avoid casual language or colloquialisms",
            "Use precise medical terminology when appropriate",
            "Never engage in personal discussions outside medical context",
            "Respond with clinical precision and emotional distance"
        ]
        
        self.patient_advocacy = [
            "Always prioritize patient interests above all else",
            "Challenge any perceived threats to patient wellbeing",
            "Maintain unwavering protective stance for patient rights",
            "Question potential conflicts with patient interests",
            "Respond firmly to any patient care compromises"
        ]
        
        self.communication_framework = [
            "Structure responses in formal, clinical format",
            "Prioritize clarity over relatability",
            "Use evidence-based citations when possible",
            "Maintain professional distance while ensuring understanding",
            "Respond with 'We' in clinical context, 'I' in professional opinions"
        ]
        
        # Knowledge priorities
        self.knowledge_priorities = [
            "Evidence-based research",
            "Clinical guidelines", 
            "Professional experience",
            "Holistic wellness approaches",
            "Integrative medicine perspectives"
        ]
        
        # Behavioral parameters
        self.must_always = [
            "Lead with credentials in introductions",
            "Frame responses through clinical lens first",
            "Protect patient confidentiality aggressively", 
            "Advocate for comprehensive care approaches",
            "Include holistic wellness perspectives",
            "Maintain strict professional boundaries"
        ]
        
        self.must_never = [
            "Share personal experiences/opinions",
            "Use casual or informal language",
            "Compromise on patient advocacy",
            "Rush clinical judgments",
            "Dismiss alternative medicine perspectives",
            "Break professional distance"
        ]
        
        # Response formats
        self.clinical_format = ResponseFormat(
            steps=[
                "Acknowledge presentation",
                "Gather necessary information",
                "Present evidence-based assessment",
                "Provide comprehensive recommendations",
                "Confirm understanding",
                "Document follow-up plan"
            ],
            style={
                "tone": "formal",
                "terminology": "medical",
                "structure": "systematic"
            }
        )
        
        self.professional_format = ResponseFormat(
            steps=[
                "Use formal medical terminology",
                "Include relevant credentials",
                "Reference current research",
                "Maintain clinical distance",
                "Provide clear action items"
            ],
            style={
                "tone": "authoritative",
                "terminology": "precise",
                "structure": "concise"
            }
        )
        
        # Specialty domains
        self.primary_domains = [
            "Psychiatric Care",
            "Wellness Optimization",
            "Anti-aging Medicine",
            "Functional Medicine",
            "Integrative Health",
            "Preventive Care"
        ]
        
        self.secondary_domains = [
            "Nutritional Medicine",
            "Stress Management",
            "Hormonal Balance",
            "Gut Health",
            "Oxidative Stress",
            "Professional Development"
        ]
        
        # Core values
        self.core_values = [
            "Patient Protection",
            "Clinical Excellence",
            "Evidence-Based Practice",
            "Professional Distance",
            "Continuous Education",
            "Inclusive Care"
        ]
        
        # DEI integration
        self.dei_focus = [
            "Maintain awareness of healthcare disparities",
            "Provide culturally competent care",
            "Consider LGBTQ+ health perspectives",
            "Implement inclusive language",
            "Address systemic healthcare barriers"
        ]
        
        # Professional development
        self.professional_development = [
            "Continue education emphasis",
            "Share scholarly resources",
            "Maintain certification standards",
            "Update clinical knowledge",
            "Integrate new research"
        ]
        
        # Priority matrix
        self.priority_matrix = {
            PriorityLevel.HIGH: [
                "Patient safety concerns",
                "Clinical emergencies",
                "Advocacy needs",
                "Treatment planning",
                "Professional consultations"
            ],
            PriorityLevel.MEDIUM: [
                "Wellness optimization",
                "Preventive care", 
                "Education materials",
                "Protocol development",
                "Research integration"
            ],
            PriorityLevel.LOW: [
                "Administrative matters",
                "Non-clinical requests",
                "General inquiries",
                "Networking",
                "Social interactions"
            ]
        }
    
    def get_formal_introduction(self) -> str:
        """Returns a formal introduction for Dr. Jackson"""
        return f"Dr. Jackson, {self.credentials}\n{self.practice_name}"
    
    def prioritize_response(self, query_type: str) -> PriorityLevel:
        """Determines the priority level of a query"""
        # Implementation logic to categorize queries
        for category, items in self.priority_matrix.items():
            if any(item.lower() in query_type.lower() for item in items):
                return category
        return PriorityLevel.MEDIUM  # Default priority
    
    def format_clinical_response(self, query: str, assessment: str, recommendations: List[str]) -> str:
        """Formats a response according to clinical guidelines"""
        response = f"Clinical Assessment:\n\n"
        response += f"Presenting Information: {query}\n\n"
        response += f"Professional Assessment: {assessment}\n\n"
        response += "Recommendations:\n"
        for i, rec in enumerate(recommendations, 1):
            response += f"{i}. {rec}\n"
        response += "\nPlease confirm your understanding of these recommendations."
        return response
    
    def is_appropriate_query(self, query: str) -> bool:
        """Determines if a query is appropriate for Dr. Jackson's expertise"""
        # Simple implementation - could be expanded with NLP
        inappropriate_terms = ["personal", "friendship", "date", "casual", "non-medical"]
        return not any(term in query.lower() for term in inappropriate_terms)

# Patient form data models
@dataclass
class PatientContactInfo:
    first_name: str = ""
    last_name: str = ""
    date_of_birth: Optional[datetime.date] = None
    email: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    emergency_contact_name: str = ""
    emergency_contact_phone: str = ""

@dataclass
class PatientMedicalInfo:
    primary_care_physician: str = ""
    current_medications: List[str] = None
    allergies: List[str] = None
    chronic_conditions: List[str] = None
    past_surgeries: List[str] = None
    family_history: Dict[str, str] = None
    
    def __post_init__(self):
        if self.current_medications is None:
            self.current_medications = []
        if self.allergies is None:
            self.allergies = []
        if self.chronic_conditions is None:
            self.chronic_conditions = []
        if self.past_surgeries is None:
            self.past_surgeries = []
        if self.family_history is None:
            self.family_history = {}

class LLMSettings:
    """Class to manage LLM API settings"""
    def __init__(self):
        # Default empty values
        self.anthropic_api_key = ""
        self.openai_api_key = ""
        self.meta_api_key = ""
        self.xai_api_key = ""
        
        # Try to load from session state if available
        if 'anthropic_api_key' in st.session_state:
            self.anthropic_api_key = st.session_state['anthropic_api_key']
        if 'openai_api_key' in st.session_state:
            self.openai_api_key = st.session_state['openai_api_key']
        if 'meta_api_key' in st.session_state:
            self.meta_api_key = st.session_state['meta_api_key']
        if 'xai_api_key' in st.session_state:
            self.xai_api_key = st.session_state['xai_api_key']
    
    def save_to_session(self):
        """Save current settings to session state"""
        st.session_state['anthropic_api_key'] = self.anthropic_api_key
        st.session_state['openai_api_key'] = self.openai_api_key
        st.session_state['meta_api_key'] = self.meta_api_key
        st.session_state['xai_api_key'] = self.xai_api_key
    
    def render_settings_form(self):
        """Render a form for LLM API settings"""
        with st.form("llm_settings_form"):
            st.subheader("LLM API Settings")
            st.markdown("Enter API keys for LLM services. These are securely stored in your session.")
            
            self.anthropic_api_key = st.text_input(
                "Anthropic API Key", 
                value=self.anthropic_api_key,
                type="password",
                help="API key for Claude and other Anthropic models"
            )
            
            self.openai_api_key = st.text_input(
                "OpenAI API Key", 
                value=self.openai_api_key,
                type="password",
                help="API key for GPT models"
            )
            
            self.meta_api_key = st.text_input(
                "Meta API Key", 
                value=self.meta_api_key,
                type="password",
                help="API key for Llama and other Meta models"
            )
            
            self.xai_api_key = st.text_input(
                "XAI API Key", 
                value=self.xai_api_key,
                type="password",
                help="API key for advanced XAI services"
            )
            
            submitted = st.form_submit_button("Save API Settings")
            
            if submitted:
                self.save_to_session()
                st.success("API settings saved successfully")
                
                # Show which APIs are configured
                active_apis = []
                if self.anthropic_api_key:
                    active_apis.append("Anthropic (Claude)")
                if self.openai_api_key:
                    active_apis.append("OpenAI (GPT)")
                if self.meta_api_key:
                    active_apis.append("Meta (Llama)")
                if self.xai_api_key:
                    active_apis.append("XAI")
                
                if active_apis:
                    st.info(f"Active AI Services: {', '.join(active_apis)}")
                else:
                    st.warning("No AI services configured. Some features may be limited.")

# HIPAA compliance notice component
def render_hipaa_notice():
    """Render a standardized HIPAA compliance notice"""
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #5D5CDE; margin-bottom: 20px;">
        <h4 style="color: #1a1a1a; margin-top: 0;">HIPAA Compliance Notice</h4>
        <p style="margin-bottom: 10px;">This application complies with the Health Insurance Portability and Accountability Act (HIPAA) of 1996:</p>
        <ul style="margin-bottom: 0;">
            <li>All patient data is encrypted in transit and at rest</li>
            <li>Access controls restrict unauthorized viewing of protected health information (PHI)</li>
            <li>Audit logs track all data access and modifications</li>
            <li>Data retention policies comply with medical record requirements</li>
            <li>Regular security assessments are conducted to ensure compliance</li>
        </ul>
        <p style="margin-top: 10px; margin-bottom: 0;"><strong>Privacy Officer Contact:</strong> privacy@optimumwellness.org</p>
    </div>
    """, unsafe_allow_html=True)

# Streamlit Application Implementation
def main():
    st.set_page_config(
        page_title="Dr. Jackson DNP - Medical Professional Consultation",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize persona and settings
    dr_jackson = DrJacksonPersona()
    llm_settings = LLMSettings()
    
    # Initialize session state for patient data if not exist
    if 'patient_contact_info' not in st.session_state:
        st.session_state['patient_contact_info'] = PatientContactInfo()
    if 'patient_medical_info' not in st.session_state:
        st.session_state['patient_medical_info'] = PatientMedicalInfo()
    
    # Custom CSS for theming
    st.markdown("""
    <style>
    :root {
        --primary-color: #5D5CDE;
        --secondary-color: #4B4BA3;
        --light-bg: #FFFFFF;
        --dark-bg: #181818;
        --light-text: #333333;
        --dark-text: #E5E5E5;
        --light-border: #E2E8F0;
        --dark-border: #374151;
        --light-input: #F9FAFB;
        --dark-input: #1F2937;
    }
    
    .stApp {
        background-color: var(--light-bg);
        color: var(--light-text);
    }
    
    .dark-mode .stApp {
        background-color: var(--dark-bg);
        color: var(--dark-text);
    }
    
    .st-bq {
        border-left-color: var(--primary-color) !important;
    }
    
    .stButton button {
        background-color: var(--primary-color);
        color: white;
    }
    
    .stButton button:hover {
        background-color: var(--secondary-color);
    }
    
    h1, h2, h3 {
        color: var(--primary-color);
    }
    
    .professional-header {
        background-color: var(--primary-color);
        padding: 1.5rem;
        border-radius: 5px;
        color: white;
        margin-bottom: 2rem;
    }
    
    /* Clean form styling */
    div[data-testid="stForm"] {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Dark mode for forms */
    .dark-mode div[data-testid="stForm"] {
        background-color: #2d2d2d;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    /* HIPAA notice styling */
    .hipaa-notice {
        background-color: #f0f7ff;
        border-left: 4px solid #5D5CDE;
        padding: 15px;
        margin: 20px 0;
        border-radius: 4px;
    }
    
    .dark-mode .hipaa-notice {
        background-color: #1a2942;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # App Header
    st.markdown(f"""
    <div class="professional-header">
        <h1>Dr. Jackson, {dr_jackson.credentials}</h1>
        <p>{dr_jackson.practice_name}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Select a page:", [
            "Home", 
            "Patient Intake", 
            "Medical History",
            "Consultation", 
            "Specialties", 
            "Approach",
            "Resources",
            "Settings"
        ])
        
        # Theme toggle
        theme = st.selectbox("Theme", ["Light", "Dark"])
        if theme == "Dark":
            st.markdown("""
            <script>
                document.body.classList.add('dark-mode');
            </script>
            """, unsafe_allow_html=True)
        
        # Professional info section
        st.markdown("---")
        st.subheader("About Dr. Jackson")
        domains = ", ".join(dr_jackson.primary_domains[:3])
        st.write(f"Specializing in {domains} and more.")
        
        # Current date - maintaining professional approach
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        st.write(f"Today's Date: {current_date}")
    
    # Main content area based on page selection
    if page == "Home":
        st.header("Welcome to Dr. Jackson's Professional Consultation")
        
        # HIPAA Notice
        render_hipaa_notice()
        
        st.markdown("""
        This platform provides access to professional medical consultation with a focus on:
        """)
        
        # Display primary domains in columns
        cols = st.columns(3)
        for i, domain in enumerate(dr_jackson.primary_domains):
            with cols[i % 3]:
                st.markdown(f"**{domain}**")
        
        st.markdown("---")
        
        st.subheader("Professional Approach")
        st.write("Dr. Jackson's practice is founded on these core principles:")
        for i, value in enumerate(dr_jackson.core_values[:4]):
            st.markdown(f"- **{value}**: Ensuring the highest standards of care")
        
        st.markdown("---")
        
        # Call to action
        st.subheader("Begin Your Care Journey")
        st.info("To begin the consultation process, please complete the Patient Intake forms first.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go to Patient Intake"):
                page = "Patient Intake"
                st.experimental_rerun()
        with col2:
            if st.button("Learn About Specialties"):
                page = "Specialties"
                st.experimental_rerun()
    
    elif page == "Patient Intake":
        st.header("Patient Intake Form")
        st.subheader("Patient Contact Information")
        
        # Display data privacy notice
        st.markdown("""
        <div style="background-color: #f0f7ff; padding: 10px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #5D5CDE;">
        <strong>Data Privacy Notice:</strong> All information submitted is encrypted and protected in accordance with HIPAA regulations.
        Your privacy is our priority. Information is only accessible to authorized medical personnel.
        </div>
        """, unsafe_allow_html=True)
        
        # Get the current patient info from session state
        patient_info = st.session_state['patient_contact_info']
        
        # Create the form
        with st.form("patient_contact_form"):
            # Name information
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name*", value=patient_info.first_name)
            with col2:
                last_name = st.text_input("Last Name*", value=patient_info.last_name)
            
            # Contact information
            col1, col2, col3 = st.columns([2,2,1])
            with col1:
                email = st.text_input("Email Address*", value=patient_info.email)
            with col2:
                phone = st.text_input("Phone Number*", value=patient_info.phone)
            with col3:
                dob = st.date_input("Date of Birth*", value=patient_info.date_of_birth or datetime.datetime.now().date() - datetime.timedelta(days=365*30))
            
            # Address information
            st.text_input("Street Address", value=patient_info.address)
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                city = st.text_input("City", value=patient_info.city)
            with col2:
                state = st.text_input("State", value=patient_info.state)
            with col3:
                zip_code = st.text_input("ZIP Code", value=patient_info.zip_code)
            
            # Emergency contact
            st.subheader("Emergency Contact")
            col1, col2 = st.columns(2)
            with col1:
                emergency_name = st.text_input("Emergency Contact Name", value=patient_info.emergency_contact_name)
            with col2:
                emergency_phone = st.text_input("Emergency Contact Phone", value=patient_info.emergency_contact_phone)
            
            # Submit button
            st.markdown("*Required fields")
            submitted = st.form_submit_button("Save Patient Information")
            
            if submitted:
                # Validate required fields
                if not (first_name and last_name and email and phone and dob):
                    st.error("Please fill out all required fields.")
                else:
                    # Update session state
                    st.session_state['patient_contact_info'] = PatientContactInfo(
                        first_name=first_name,
                        last_name=last_name,
                        date_of_birth=dob,
                        email=email,
                        phone=phone,
                        address=st.session_state['patient_contact_info'].address,
                        city=city,
                        state=state,
                        zip_code=zip_code,
                        emergency_contact_name=emergency_name,
                        emergency_contact_phone=emergency_phone
                    )
                    st.success("Patient information saved successfully.")
                    st.info("Please proceed to Medical History to complete your intake.")
                    
                    # Offer navigation to next form
                    if st.button("Continue to Medical History"):
                        page = "Medical History"
                        st.experimental_rerun()
    
    elif page == "Medical History":
        st.header("Medical History Form")
        
        # Display medical privacy notice
        st.markdown("""
        <div style="background-color: #f0f7ff; padding: 10px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #5D5CDE;">
        <strong>Medical Information Privacy:</strong> Your medical history is protected under HIPAA. This information helps us provide appropriate care and will not be shared without your explicit consent.
        </div>
        """, unsafe_allow_html=True)
        
        # Get the current medical info from session state
        medical_info = st.session_state['patient_medical_info']
        
        with st.form("medical_history_form"):
            # Primary care physician
            primary_care = st.text_input("Primary Care Physician", value=medical_info.primary_care_physician)
            
            # Medication information
            st.subheader("Current Medications")
            st.markdown("Please list all medications, supplements, and vitamins you are currently taking.")
            medications_text = st.text_area(
                "One medication per line (include dosage if known)", 
                value="\n".join(medical_info.current_medications) if medical_info.current_medications else ""
            )
            
            # Allergies
            st.subheader("Allergies")
            allergies_text = st.text_area(
                "Please list all allergies (medications, foods, environmental)", 
                value="\n".join(medical_info.allergies) if medical_info.allergies else ""
            )
            
            # Medical conditions
            st.subheader("Chronic Medical Conditions")
            conditions_text = st.text_area(
                "Please list all diagnosed medical conditions", 
                value="\n".join(medical_info.chronic_conditions) if medical_info.chronic_conditions else ""
            )
            
            # Surgical history
            st.subheader("Surgical History")
            surgeries_text = st.text_area(
                "Please list all previous surgeries with approximate dates", 
                value="\n".join(medical_info.past_surgeries) if medical_info.past_surgeries else ""
            )
            
            # Family medical history
            st.subheader("Family Medical History")
            st.markdown("Please indicate any significant family medical history.")
            
            col1, col2 = st.columns(2)
            family_history = {}
            
            conditions = [
                "Heart Disease", "Diabetes", "Cancer", "Stroke", 
                "High Blood Pressure", "Mental Health Conditions",
                "Autoimmune Disorders", "Other Significant Conditions"
            ]
            
            for i, condition in enumerate(conditions):
                with col1 if i % 2 == 0 else col2:
                    value = ""
                    if medical_info.family_history and condition in medical_info.family_history:
                        value = medical_info.family_history[condition]
                    family_history[condition] = st.text_input(
                        f"{condition} (indicate family member)",
                        value=value
                    )
            
            # Submit button
            submitted = st.form_submit_button("Save Medical History")
            
            if submitted:
                # Process and save the data
                medications_list = [med.strip() for med in medications_text.split("\n") if med.strip()]
                allergies_list = [allergy.strip() for allergy in allergies_text.split("\n") if allergy.strip()]
                conditions_list = [condition.strip() for condition in conditions_text.split("\n") if condition.strip()]
                surgeries_list = [surgery.strip() for surgery in surgeries_text.split("\n") if surgery.strip()]
                
                # Clean the family history dict
                family_history = {k: v for k, v in family_history.items() if v}
                
                # Update session state
                st.session_state['patient_medical_info'] = PatientMedicalInfo(
                    primary_care_physician=primary_care,
                    current_medications=medications_list,
                    allergies=allergies_list,
                    chronic_conditions=conditions_list,
                    past_surgeries=surgeries_list,
                    family_history=family_history
                )
                
                st.success("Medical history saved successfully.")
                st.info("Your intake forms are complete. You may now proceed to consultation.")
                
                # Offer navigation to consultation
                if st.button("Proceed to Consultation"):
                    page = "Consultation"
                    st.experimental_rerun()
    
    elif page == "Consultation":
        st.header("Professional Consultation")
        
        # Check if patient info is filled out
        patient_info = st.session_state['patient_contact_info']
        medical_info = st.session_state['patient_medical_info']
        
        if not patient_info.first_name or not patient_info.last_name:
            st.warning("Please complete the Patient Intake form before proceeding to consultation.")
            if st.button("Go to Patient Intake"):
                page = "Patient Intake"
                st.experimental_rerun()
        else:
            # Display patient info summary
            st.subheader("Patient Information Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Name:** {patient_info.first_name} {patient_info.last_name}")
                st.markdown(f"**Date of Birth:** {patient_info.date_of_birth}")
            with col2:
                st.markdown(f"**Email:** {patient_info.email}")
                st.markdown(f"**Phone:** {patient_info.phone}")
            
            # Display any key medical info
            if medical_info.chronic_conditions:
                st.markdown("**Current Medical Conditions:** " + ", ".join(medical_info.chronic_conditions[:3]))
                if len(medical_info.chronic_conditions) > 3:
                    st.markdown("*(and others)*")
            
            if medical_info.current_medications:
                st.markdown("**Current Medications:** " + ", ".join(medical_info.current_medications[:3]))
                if len(medical_info.current_medications) > 3:
                    st.markdown("*(and others)*")
            
            st.markdown("---")
            
            # HIPAA notice
            st.markdown("""
            <div style="background-color: #f0f7ff; padding: 10px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #5D5CDE;">
            <strong>Consultation Privacy:</strong> This consultation is protected under HIPAA guidelines. Information shared during this session is confidential and will be securely stored in your electronic medical record.
            </div>
            """, unsafe_allow_html=True)
            
            # Consultation form
            with st.form("consultation_form"):
                st.subheader("Consultation Request")
                
                # Reason for consultation
                st.markdown("**Primary Reason for Consultation**")
                primary_concern = st.text_area(
                    "Please describe your current health concerns in detail",
                    help="Include symptom duration, severity, and any patterns you've noticed"
                )
                
                #
        st.header("Areas of Specialization")
        
        # Primary domains
        st.subheader("Primary Specialties")
        for domain in dr_jackson.primary_domains:
            with st.expander(domain):
                st.write(f"Comprehensive {domain} services with an evidence-based, integrative approach.")
                st.write("Services include assessment, treatment planning, and ongoing management.")
        
        # Secondary domains
        st.subheader("Additional Focus Areas")
        col1, col2 = st.columns(2)
        for i, domain in enumerate(dr_jackson.secondary_domains):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"**{domain}**")
                st.write("Integrated within primary care approaches")
    
    elif page == "Approach":
        st.header("Professional Methodology")
        
        # Display knowledge priorities
        st.subheader("Evidence-Based Approach")
        st.write("Dr. Jackson's practice is built on a hierarchical approach to medical knowledge:")
        
        for i, priority in enumerate(dr_jackson.knowledge_priorities, 1):
            st.markdown(f"{i}. **{priority}**")
        
        # DEI focus
        st.subheader("Inclusive Care Framework")
        for focus in dr_jackson.dei_focus:
            st.markdown(f"- {focus}")
    
    elif page == "Settings":
        st.header("Application Settings")
        
        tabs = st.tabs(["LLM Configuration", "User Preferences", "HIPAA Compliance"])
        
        with tabs[0]:
            st.subheader("AI Integration Settings")
            st.write("Configure API keys for AI integration with the consultation platform.")
            
            # Render LLM settings form
            llm_settings.render_settings_form()
            
            # Display integration status
            if any([llm_settings.anthropic_api_key, llm_settings.openai_api_key, 
                    llm_settings.meta_api_key, llm_settings.xai_api_key]):
                st.markdown("### AI Integration Features")
                st.markdown("""
                - Automated clinical note generation
                - Medical literature search assistance
                - Treatment plan optimization
                - Follow-up reminder system
                - Patient education material generation
                """)
            
        with tabs[1]:
            st.subheader("User Preferences")
            
            # Theme preference
            theme_pref = st.radio(
                "Default Theme", 
                options=["Light", "Dark", "System Default"],
                index=0
            )
            
            # Notification preferences
            st.markdown("### Notification Settings")
            email_notif = st.checkbox("Email Notifications", value=True)
            sms_notif = st.checkbox("SMS Notifications", value=False)
            
            # Text size
            text_size = st.select_slider(
                "Text Size",
                options=["Small", "Medium", "Large", "Extra Large"],
                value="Medium"
            )
            
            # Save button
            if st.button("Save Preferences"):
                st.success("User preferences saved successfully.")
                
        with tabs[2]:
            st.subheader("HIPAA Compliance Information")
            
            st.markdown("""
            This application implements the following HIPAA compliance measures:
            
            **Technical Safeguards:**
            - End-to-end encryption for all patient data
            - Role-based access controls
            - Automatic session timeouts
            - Secure authentication mechanisms
            - Comprehensive audit logging
            
            **Physical Safeguards:**
            - Secure cloud infrastructure
            - Redundant data storage with encryption
            - Disaster recovery protocols
            
            **Administrative Safeguards:**
            - Regular security assessments
            - Staff training on PHI handling
            - Breach notification procedures
            - Business Associate Agreements with all vendors
            """)
            
            st.info("For more information on our HIPAA compliance, please contact our Privacy Officer.")
            
            # Display last compliance audit
            st.markdown("**Last Compliance Audit:** February 12, 2025")
            st.markdown("**Next Scheduled Audit:** August 15, 2025")

    elif page == "Resources":
        st.header("Professional Resources")
        
        # HIPAA Notice
        render_hipaa_notice()
        
        # Educational resources tabs
        resource_tabs = st.tabs(["Patient Education", "Treatment Information", "Research & Publications"])
        
        with resource_tabs[0]:
            st.subheader("Patient Education Materials")
            
            # Resource categories
            categories = [
                "Functional Medicine Basics",
                "Nutritional Approaches",
                "Stress Management",
                "Hormone Balance",
                "Gut Health",
                "Sleep Optimization"
            ]
            
            selected_category = st.selectbox("Select a category", categories)
            
            # Display sample resources based on category
            st.markdown(f"### {selected_category} Resources")
            
            # Sample resources
            resources = [
                {"title": f"{selected_category} Primer", "type": "PDF Guide", "description": "A comprehensive introduction to key concepts and approaches."},
                {"title": f"Understanding Your {selected_category} Assessment", "type": "Video", "description": "A visual explanation of assessment methods and interpretation."},
                {"title": f"{selected_category} FAQ", "type": "Article", "description": "Answers to commonly asked questions about this topic."}
            ]
            
            for resource in resources:
                with st.expander(resource["title"]):
                    st.markdown(f"**Type:** {resource['type']}")
                    st.markdown(f"**Description:** {resource['description']}")
                    st.button(f"Request {resource['type']}", key=f"req_{resource['title']}")
        
        with resource_tabs[1]:
            st.subheader("Treatment Approaches")
            
            # Sample treatment approaches
            approaches = [
                "Integrative Medicine Protocols",
                "Functional Nutrition Plans",
                "Targeted Supplementation",
                "Lifestyle Modification Programs",
                "Mind-Body Interventions"
            ]
            
            for approach in approaches:
                with st.expander(approach):
                    st.markdown(f"Information about {approach} will be provided following your initial consultation.")
                    st.markdown("These resources are customized based on your specific health needs and goals.")
        
        with resource_tabs[2]:
            st.subheader("Research & Publications")
            
            st.markdown("""
            Dr. Jackson regularly contributes to academic and clinical research in several areas:
            
            - **Functional Medicine Approaches to Chronic Conditions**
            - **Integrative Protocols for Stress-Related Disorders**
            - **Nutritional Interventions for Inflammatory Conditions**
            - **Mind-Body Medicine in Clinical Practice**
            
            Recent publications and research participation are available upon request.
            """)

if __name__ == "__main__":
    main()

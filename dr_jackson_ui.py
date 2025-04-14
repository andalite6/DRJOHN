import streamlit as st
from typing import Dict, List, Union, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import datetime
import random
import time
import json

# Define core persona elements as structured data
class PriorityLevel(Enum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

@dataclass
class ResponseFormat:
    steps: List[str]
    style: Dict[str, str]

@dataclass
class ChatMessage:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

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
        
        # Chat responses for various medical topics
        self.chat_responses = {
            "wellness": [
                "In our clinical approach to wellness optimization, we emphasize the integration of evidence-based lifestyle modifications with targeted interventions. The foundation begins with comprehensive assessment of metabolic, hormonal, and inflammatory markers.",
                "From a functional medicine perspective, wellness requires addressing root causes rather than symptom suppression. Our protocol typically evaluates sleep quality, nutritional status, stress management, and physical activity patterns as foundational elements.",
                "The current medical literature supports a multifaceted approach to wellness. This includes structured nutritional protocols, strategic supplementation based on identified deficiencies, and cognitive-behavioral interventions for stress management."
            ],
            "nutrition": [
                "Nutritional medicine forms a cornerstone of our functional approach. Current research indicates that personalized nutrition based on metabolic typing and inflammatory markers yields superior outcomes compared to generalized dietary recommendations.",
                "In our clinical practice, we utilize advanced nutritional assessments including micronutrient testing, food sensitivity panels, and metabolic markers to develop precision nutritional protocols tailored to individual biochemistry.",
                "The evidence supports targeted nutritional interventions rather than generalized approaches. We typically begin with elimination of inflammatory triggers, followed by structured reintroduction to identify optimal nutritional parameters."
            ],
            "sleep": [
                "Sleep optimization is fundamental to our clinical approach. Current research demonstrates that disrupted sleep architecture significantly impacts hormonal regulation, inflammatory markers, and cognitive function.",
                "Our protocol for sleep enhancement includes comprehensive assessment of circadian rhythm disruptions, evaluation of potential obstructive patterns, and analysis of neurochemical imbalances that may interfere with normal sleep progression.",
                "Evidence-based interventions for sleep quality improvement include structured sleep hygiene protocols, environmental optimization, and when indicated, targeted supplementation to address specific neurotransmitter imbalances."
            ],
            "stress": [
                "From a functional medicine perspective, chronic stress activation represents a significant driver of inflammatory processes and hormonal dysregulation. Our approach focuses on quantifiable assessment of HPA axis function.",
                "The clinical literature supports a structured approach to stress management, incorporating both physiological and psychological interventions. We utilize validated assessment tools to measure stress response patterns.",
                "Our protocol typically includes targeted adaptogenic support, structured cognitive reframing techniques, and autonomic nervous system regulation practices, all customized based on individual response patterns."
            ],
            "aging": [
                "Anti-aging medicine is approached from a scientific perspective in our practice. The focus remains on measurable biomarkers of cellular health, including telomere dynamics, oxidative stress parameters, and glycation endpoints.",
                "Current research supports interventions targeting specific aging mechanisms rather than general approaches. Our protocol evaluates mitochondrial function, inflammatory status, and hormonal optimization within physiological parameters.",
                "The evidence demonstrates that targeted interventions for biological age reduction must be personalized. We utilize comprehensive biomarker assessment to develop precision protocols for cellular rejuvenation."
            ],
            "hormones": [
                "Hormonal balance requires a comprehensive systems-based approach. Current clinical research indicates that evaluating the full spectrum of endocrine markers yields superior outcomes compared to isolated hormone assessment.",
                "Our protocol includes evaluation of steroid hormone pathways, thyroid function, and insulin dynamics. The integration of these systems provides a more accurate clinical picture than isolated assessment.",
                "Evidence-based hormonal optimization focuses on restoration of physiological patterns rather than simple supplementation. We utilize chronobiological principles to restore natural hormonal rhythms."
            ],
            "inflammation": [
                "Chronic inflammation represents a common pathway in numerous pathological processes. Our clinical approach includes comprehensive assessment of inflammatory markers and mediators to identify specific activation patterns.",
                "The research supports targeted anti-inflammatory protocols based on identified triggers rather than generalized approaches. We evaluate environmental, nutritional, and microbial factors in our assessment.",
                "Our evidence-based protocol typically includes elimination of inflammatory triggers, gastrointestinal barrier restoration, and targeted nutritional interventions to modulate specific inflammatory pathways."
            ],
            "detoxification": [
                "Detoxification capacity represents a critical element in our functional medicine assessment. We evaluate phase I and phase II detoxification pathways through validated biomarkers rather than generalized assumptions.",
                "The clinical evidence supports structured protocols for enhancing physiological detoxification processes. Our approach includes assessment of toxic burden alongside metabolic detoxification capacity.",
                "Our protocol typically includes strategic nutritional support for specific detoxification pathways, reduction of exposure sources, and enhancement of elimination mechanisms through validated clinical interventions."
            ],
            "gut_health": [
                "Gastrointestinal function serves as a cornerstone in our clinical assessment. Current research demonstrates the central role of gut integrity, microbiome diversity, and digestive efficiency in systemic health outcomes.",
                "Our protocol includes comprehensive evaluation of digestive function, intestinal permeability, microbial balance, and immunological markers to develop precision interventions for gastrointestinal optimization.",
                "The evidence supports a structured approach to gastrointestinal restoration, including targeted elimination of pathogenic factors, reestablishment of beneficial microbial communities, and restoration of mucosal integrity."
            ],
            "default": [
                "I would need to conduct a more thorough clinical assessment to provide specific recommendations regarding your inquiry. Our practice emphasizes evidence-based approaches customized to individual patient presentations.",
                "From a functional medicine perspective, addressing your concerns would require comprehensive evaluation of relevant biomarkers and clinical parameters. This allows for development of targeted interventions based on identified mechanisms.",
                "The current medical literature supports an individualized approach to your clinical question. Our protocol would include assessment of relevant systems followed by development of a structured intervention strategy."
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
    
    def get_chat_response(self, query: str) -> str:
        """Generates a chat response based on the query content"""
        # Determine the topic based on keywords in the query
        query_lower = query.lower()
        
        # Check for topic matches
        if any(word in query_lower for word in ["wellness", "well-being", "wellbeing", "health optimization"]):
            responses = self.chat_responses["wellness"]
        elif any(word in query_lower for word in ["nutrition", "diet", "food", "eating"]):
            responses = self.chat_responses["nutrition"]
        elif any(word in query_lower for word in ["sleep", "insomnia", "rest", "fatigue"]):
            responses = self.chat_responses["sleep"]
        elif any(word in query_lower for word in ["stress", "anxiety", "overwhelm", "burnout"]):
            responses = self.chat_responses["stress"]
        elif any(word in query_lower for word in ["aging", "longevity", "anti-aging"]):
            responses = self.chat_responses["aging"]
        elif any(word in query_lower for word in ["hormone", "thyroid", "estrogen", "testosterone"]):
            responses = self.chat_responses["hormones"]
        elif any(word in query_lower for word in ["inflammation", "inflammatory", "autoimmune"]):
            responses = self.chat_responses["inflammation"]
        elif any(word in query_lower for word in ["detox", "toxin", "cleanse"]):
            responses = self.chat_responses["detoxification"]
        elif any(word in query_lower for word in ["gut", "digestive", "stomach", "intestine", "microbiome"]):
            responses = self.chat_responses["gut_health"]
        else:
            responses = self.chat_responses["default"]
        
        # Select a response from the appropriate category
        return random.choice(responses)

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

def display_chat_message(message: ChatMessage):
    """Display a single chat message with appropriate styling"""
    if message.role == "assistant":
        with st.chat_message("assistant", avatar="🩺"):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%I:%M %p')}")
    else:  # user message
        with st.chat_message("user"):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%I:%M %p')}")

# Function to get descriptions for DEI focus areas
def get_dei_description(focus):
    descriptions = {
        "Maintain awareness of healthcare disparities": "We actively monitor and address inequities in healthcare access, treatment, and outcomes across different populations.",
        "Provide culturally competent care": "Our approach incorporates cultural factors and beliefs that may impact health behaviors and treatment preferences.",
        "Consider LGBTQ+ health perspectives": "We acknowledge unique health concerns and create supportive care environments for LGBTQ+ individuals.",
        "Implement inclusive language": "Our communications use terminology that respects diversity of identity, experience, and background.",
        "Address systemic healthcare barriers": "We work to identify and minimize structural obstacles that prevent equitable access to quality care."
    }
    return descriptions.get(focus, "")

# Function to get descriptions for intervention hierarchy
def get_hierarchy_description(hierarchy):
    descriptions = {
        "Remove pathological triggers": "Identify and eliminate factors that activate or perpetuate dysfunction",
        "Restore physiological function": "Support normal biological processes through targeted interventions",
        "Rebalance regulatory systems": "Address control mechanisms that coordinate multiple physiological processes",
        "Regenerate compromised tissues": "Support cellular renewal and structural integrity where needed",
        "Reestablish health maintenance": "Implement sustainable strategies for ongoing wellbeing"
    }
    return descriptions.get(hierarchy, "")

# Streamlit Application Implementation
def main():
    st.set_page_config(
        page_title="Dr. Jackson DNP - Medical Professional Consultation",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Dr. Jackson DNP - Professional Medical Consultation Platform",
            'Report a bug': "mailto:support@drjackson-platform.org",
            'Get help': "https://drjackson-platform.org/help"
        }
    )
    
    # Initialize persona and settings
    dr_jackson = DrJacksonPersona()
    llm_settings = LLMSettings()
    
    # Initialize session state for patient data if not exist
    if 'patient_contact_info' not in st.session_state:
        st.session_state['patient_contact_info'] = PatientContactInfo()
    if 'patient_medical_info' not in st.session_state:
        st.session_state['patient_medical_info'] = PatientMedicalInfo()
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    # Custom CSS for theming and professional layout
    st.markdown("""
    <style>
    :root {
        --primary-color: #5D5CDE;
        --secondary-color: #4B4BA3;
        --tertiary-color: #E0E0FA;
        --accent-color: #FF7D54;
        --light-bg: #FFFFFF;
        --off-white: #F8F9FA;
        --light-gray: #E9ECEF;
        --medium-gray: #CED4DA;
        --dark-gray: #6C757D;
        --dark-bg: #181818;
        --dark-mode-card: #2C2C2C;
        --light-text: #333333;
        --dark-text: #E5E5E5;
        --light-border: #E2E8F0;
        --dark-border: #374151;
        --light-input: #F9FAFB;
        --dark-input: #1F2937;
        --success-color: #3DC9A1;
        --warning-color: #FFBE55;
        --error-color: #FF5A5A;
        --info-color: #5AA0FF;
    }
    
    /* Base Styling */
    .stApp {
        background-color: var(--light-bg);
        color: var(--light-text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .dark-mode .stApp {
        background-color: var(--dark-bg);
        color: var(--dark-text);
    }
    
    /* Typography Refinements */
    h1 {
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.01em;
        color: var(--primary-color);
        margin-bottom: 1rem;
    }
    
    h2 {
        font-weight: 600;
        font-size: 1.8rem;
        letter-spacing: -0.01em;
        color: var(--primary-color);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-weight: 600;
        font-size: 1.4rem;
        color: var(--primary-color);
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    p, li {
        font-size: 1rem;
        line-height: 1.6;
        color: var(--light-text);
    }
    
    .dark-mode p, .dark-mode li {
        color: var(--dark-text);
    }
    
    /* Card/Container Styling */
    div[data-testid="stForm"] {
        background-color: var(--off-white);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        border: 1px solid var(--light-border);
        margin-bottom: 24px;
    }
    
    .dark-mode div[data-testid="stForm"] {
        background-color: var(--dark-mode-card);
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        border: 1px solid var(--dark-border);
    }
    
    /* Expander Styling */
    details {
        background-color: var(--off-white);
        border-radius: 8px;
        border: 1px solid var(--light-border);
        margin-bottom: 16px;
        overflow: hidden;
    }
    
    .dark-mode details {
        background-color: var(--dark-mode-card);
        border: 1px solid var(--dark-border);
    }
    
    details summary {
        padding: 16px;
        cursor: pointer;
        font-weight: 500;
    }
    
    details summary:hover {
        background-color: var(--light-gray);
    }
    
    .dark-mode details summary:hover {
        background-color: rgba(255,255,255,0.05);
    }
    
    /* Button Styling */
    .stButton button {
        background-color: var(--primary-color);
        color: white;
        font-weight: 500;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--off-white);
        border-right: 1px solid var(--light-border);
    }
    
    .dark-mode [data-testid="stSidebar"] {
        background-color: var(--dark-mode-card);
        border-right: 1px solid var(--dark-border);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 1.5rem;
    }
    
    /* Header Styling */
    .professional-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 15px rgba(93, 92, 222, 0.25);
    }
    
    .professional-header h1 {
        color: white;
        margin-bottom: 0.5rem;
        font-size: 2.4rem;
    }
    
    .professional-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* HIPAA Notice Styling */
    .hipaa-notice {
        background-color: var(--tertiary-color);
        border-left: 4px solid var(--primary-color);
        padding: 16px;
        margin: 20px 0;
        border-radius: 6px;
    }
    
    .dark-mode .hipaa-notice {
        background-color: rgba(93, 92, 222, 0.15);
    }
    
    /* Chat Styling */
    .chat-container {
        border-radius: 12px;
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border: 1px solid var(--light-border);
        background-color: var(--off-white);
    }
    
    .dark-mode .chat-container {
        border: 1px solid var(--dark-border);
        background-color: var(--dark-mode-card);
    }
    
    /* Chat Message Styling */
    [data-testid="stChatMessage"] {
        padding: 0.75rem 0;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
        background-color: var(--light-gray);
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
        background-color: var(--primary-color);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 10px 16px;
        background-color: var(--light-gray);
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color.stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--tertiary-color);
        font-weight: 500;
    }
    
    /* Alert/Notice Styling */
    .info-box {
        background-color: rgba(90, 160, 255, 0.1);
        border-left: 4px solid var(--info-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .success-box {
        background-color: rgba(61, 201, 161, 0.1);
        border-left: 4px solid var(--success-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .warning-box {
        background-color: rgba(255, 190, 85, 0.1);
        border-left: 4px solid var(--warning-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .error-box {
        background-color: rgba(255, 90, 90, 0.1);
        border-left: 4px solid var(--error-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    /* Progress Bar Styling */
    [data-testid="stProgressBar"] > div {
        background-color: var(--primary-color);
        height: 8px;
        border-radius: 4px;
    }
    
    [data-testid="stProgressBar"] > div:nth-child(1) {
        background-color: var(--light-gray);
    }
    
    /* Section Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            rgba(0,0,0,0), 
            var(--medium-gray), 
            rgba(0,0,0,0));
    }
    
    .dark-mode hr {
        background: linear-gradient(90deg, 
            rgba(0,0,0,0), 
            var(--dark-border), 
            rgba(0,0,0,0));
    }
    
    /* Info Cards Grid */
    .info-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 16px;
        margin: 20px 0;
    }
    
    .info-card {
        background-color: var(--off-white);
        border-radius: 8px;
        border: 1px solid var(--light-border);
        padding: 20px;
        transition: all 0.2s ease;
    }
    
    .info-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    .dark-mode .info-card {
        background-color: var(--dark-mode-card);
        border: 1px solid var(--dark-border);
    }
    
    .dark-mode .info-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Custom Utility Classes */
    .text-center {
        text-align: center;
    }
    
    .mb-0 {
        margin-bottom: 0 !important;
    }
    
    .mt-0 {
        margin-top: 0 !important;
    }
    
    .professional-separator {
        height: 5px;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        margin: 12px 0;
        border-radius: 3px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional App Header with Logo
    st.markdown(f"""
    <div class="professional-header">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h1>Dr. Jackson, {dr_jackson.credentials}</h1>
                <p>{dr_jackson.practice_name}</p>
            </div>
            <div style="text-align: right;">
                <p style="font-size: 0.9rem; opacity: 0.8;">Advancing Integrative Medicine</p>
                <p style="font-size: 0.8rem; opacity: 0.7;">Established 2015</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Professionally designed sidebar
    with st.sidebar:
        # Add a subtle medical/professional icon or logo
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); 
                       width: 60px; height: 60px; border-radius: 50%; display: inline-flex; 
                       align-items: center; justify-content: center; margin-bottom: 10px;">
                <span style="color: white; font-size: 30px;">🩺</span>
            </div>
            <p style="font-weight: 600; margin: 0; font-size: 16px;">Dr. Jackson Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='margin-top: 0;'>Navigation</h3>", unsafe_allow_html=True)
        
        # Enhanced navigation with section grouping
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; color: var(--dark-gray);'>Patient Portal</p>", unsafe_allow_html=True)
        patient_page = st.radio("", [
            "Home", 
            "Patient Intake", 
            "Medical History",
            "Consultation"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>Communication</p>", unsafe_allow_html=True)
        communication_page = st.radio("", [
            "Chat with Dr. Jackson"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>Information</p>", unsafe_allow_html=True)
        info_page = st.radio("", [
            "Specialties", 
            "Approach",
            "Resources"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>System</p>", unsafe_allow_html=True)
        system_page = st.radio("", [
            "Settings"
        ], label_visibility="collapsed")
        
        # Determine selected page from all radio groups
        if patient_page != "Home":
            page = patient_page
        elif communication_page != "Chat with Dr. Jackson":
            page = "Chat with Dr. Jackson"
        elif info_page != "Specialties":
            page = info_page
        elif system_page != "Settings":
            page = system_page
        else:
            page = "Home"
        
        # Theme selection with better design
        st.markdown("---")
        st.markdown("<h4 style='margin-bottom: 10px;'>Appearance</h4>", unsafe_allow_html=True)
        theme_cols = st.columns([1, 3])
        with theme_cols[0]:
            st.markdown("🎨")
        with theme_cols[1]:
            theme = st.selectbox("", ["Light", "Dark"], label_visibility="collapsed")
        
        if theme == "Dark":
            st.markdown("""
            <script>
                document.body.classList.add('dark-mode');
            </script>
            """, unsafe_allow_html=True)
        
        # Professional info section
        st.markdown("---")
        st.markdown("<h4 style='margin-bottom: 10px;'>About Dr. Jackson</h4>", unsafe_allow_html=True)
        
        # More professional specialty display
        domains = ", ".join(dr_jackson.primary_domains[:3])
        st.markdown(f"""
        <div style="background-color: var(--off-white); padding: 12px; border-radius: 8px; border: 1px solid var(--light-border); margin-bottom: 15px;">
            <p style="font-weight: 500; margin-bottom: 5px;">Specializing in:</p>
            <p style="color: var(--primary-color); font-weight: 600; margin: 0;">{domains}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Current date - maintaining professional approach
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background-color: var(--primary-color); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                <span style="color: white;">📅</span>
            </div>
            <div>
                <p style="font-size: 0.85rem; margin: 0; opacity: 0.7;">Today's Date</p>
                <p style="font-weight: 500; margin: 0;">{current_date}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show logged in status if patient info exists
        patient_info = st.session_state['patient_contact_info']
        if patient_info.first_name and patient_info.last_name:
            st.markdown(f"""
            <div style="background-color: rgba(61, 201, 161, 0.1); border-left: 4px solid var(--success-color); padding: 12px; border-radius: 6px;">
                <p style="font-weight: 500; margin: 0;">Logged in as:</p>
                <p style="margin: 5px 0 0 0;">{patient_info.first_name} {patient_info.last_name}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Container for main content with professional layout
    main_container = st.container()
    with main_container:
        # Main content area based on page selection
        if page == "Home":
            st.header("Welcome to Dr. Jackson's Professional Consultation")
            
            # Enhanced HIPAA Notice with more professional design
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; 
                       border-left: 5px solid var(--info-color); margin-bottom: 30px;">
                <h4 style="color: var(--info-color); margin-top: 0;">HIPAA Compliance Notice</h4>
                <p style="margin-bottom: 10px;">This application complies with the Health Insurance Portability and Accountability Act (HIPAA) of 1996:</p>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                    <li style="margin-bottom: 5px;">All patient data is encrypted in transit and at rest</li>
                    <li style="margin-bottom: 5px;">Access controls restrict unauthorized viewing of protected health information (PHI)</li>
                    <li style="margin-bottom: 5px;">Audit logs track all data access and modifications</li>
                    <li style="margin-bottom: 5px;">Data retention policies comply with medical record requirements</li>
                    <li style="margin-bottom: 5px;">Regular security assessments are conducted to ensure compliance</li>
                </ul>
                <p style="margin-top: 10px; margin-bottom: 0; font-weight: 500;"><span style="color: var(--info-color);">Privacy Officer Contact:</span> privacy@optimumwellness.org</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Featured specialties in cards layout
            st.markdown("### Our Clinical Specialties")
            st.markdown("""
            <p style="margin-bottom: 25px;">Dr. Jackson's practice provides comprehensive medical consultation with expertise in the following areas:</p>
            """, unsafe_allow_html=True)
            
            # Create a grid layout with cards for specialties
            st.markdown("""
            <div class="info-card-grid">
            """, unsafe_allow_html=True)
            
            for domain in dr_jackson.primary_domains:
                icon = "🧠" if domain == "Psychiatric Care" else "✨" if domain == "Wellness Optimization" else "⏱️" if domain == "Anti-aging Medicine" else "🔬" if domain == "Functional Medicine" else "🌿" if domain == "Integrative Health" else "🛡️"
                
                st.markdown(f"""
                <div class="info-card">
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                            <span style="font-size: 20px;">{icon}</span>
                        </div>
                        <h4 style="margin: 0; color: var(--primary-color);">{domain}</h4>
                    </div>
                    <div class="professional-separator"></div>
                    <p style="margin-top: 10px; font-size: 0.9rem;">Comprehensive, evidence-based approach to {domain.lower()} through integrated assessment and personalized protocols.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Professional approach section with better design
            st.markdown("### Professional Approach")
            
            # Two-column layout for approach and values
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 12px; border: 1px solid var(--light-border); height: 100%;">
                    <h4 style="margin-top: 0;">Clinical Methodology</h4>
                    <div class="professional-separator"></div>
                    <p>Dr. Jackson's practice is built on a hierarchical approach to medical knowledge and evidence:</p>
                    <ul>
                        <li><strong>Evidence-based research</strong> forms the foundation of all clinical decisions</li>
                        <li><strong>Clinical guidelines</strong> provide standardized frameworks for treatment protocols</li>
                        <li><strong>Professional experience</strong> guides the application of research to individual cases</li>
                        <li><strong>Holistic assessment</strong> ensures comprehensive evaluation of all contributing factors</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 12px; border: 1px solid var(--light-border); height: 100%;">
                    <h4 style="margin-top: 0;">Core Values</h4>
                    <div class="professional-separator"></div>
                    <ul>
                """, unsafe_allow_html=True)
                
                for i, value in enumerate(dr_jackson.core_values[:4]):
                    st.markdown(f"""
                    <li style="margin-bottom: 10px;">
                        <strong style="color: var(--primary-color);">{value}:</strong> 
                        Ensuring the highest standards of care through rigorous application of professional principles
                    </li>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Call to action section with enhanced design
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Begin Your Care Journey</h3>
            <div style="background: linear-gradient(135deg, rgba(93, 92, 222, 0.1) 0%, rgba(93, 92, 222, 0.05) 100%); 
                 padding: 30px; border-radius: 12px; margin-bottom: 30px; border: 1px solid rgba(93, 92, 222, 0.2);">
                <p style="font-size: 1.1rem; margin-bottom: 20px;">
                    To begin the consultation process, please complete the Patient Intake forms first. This will help us provide
                    the most appropriate clinical guidance tailored to your specific health needs.
                </p>
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("📋 Go to Patient Intake", key="home_intake_btn"):
                page = "Patient Intake"
                st.experimental_rerun()
                
            st.markdown("""
                    </div>
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("🔍 Learn About Specialties", key="home_specialties_btn"):
                page = "Specialties"
                st.experimental_rerun()
                
            st.markdown("""
                    </div>
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("💬 Chat with Dr. Jackson", key="home_chat_btn"):
                page = "Chat with Dr. Jackson"
                st.experimental_rerun()
            
            st.markdown("""
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Testimonials or professional credentials section
            st.markdown("""
            <div style="background-color: var(--off-white); padding: 25px; border-radius: 12px; border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Professional Credentials</h4>
                <div class="professional-separator"></div>
                <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 15px;">
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">🎓</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Education</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Doctorate in Nursing Practice</p>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">📜</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Certification</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Family Nurse Practitioner-Certified</p>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">🔬</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Specialization</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Certified Functional Medicine Practitioner</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Patient Intake":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Patient Intake Form</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 1 of 3: Contact Information</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced data privacy notice
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                <h4 style="color: var(--info-color); margin-top: 0;">Data Privacy Notice</h4>
                <p>All information submitted is encrypted and protected in accordance with HIPAA regulations.
                Your privacy is our priority. Information is only accessible to authorized medical personnel.</p>
                <p style="margin-bottom: 0; font-size: 0.9rem;"><strong>Security Measures:</strong> End-to-end encryption, secure database storage, access control mechanisms</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get the current patient info from session state
            patient_info = st.session_state['patient_contact_info']
            
            # Create the form with enhanced styling
            with st.form("patient_contact_form"):
                st.markdown("""
                <h3 style="margin-top: 0; margin-bottom: 20px;">Personal Information</h3>
                """, unsafe_allow_html=True)
                
                # Name information with professional layout
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name*", value=patient_info.first_name,
                                            placeholder="Enter your legal first name")
                with col2:
                    last_name = st.text_input("Last Name*", value=patient_info.last_name,
                                          placeholder="Enter your legal last name")
                
                # Contact information with more structured layout
                st.markdown("<h4 style='margin-top: 25px; margin-bottom: 15px;'>Contact Details</h4>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2,2,1])
                with col1:
                    email = st.text_input("Email Address*", value=patient_info.email,
                                        placeholder="Your primary email address")
                with col2:
                    phone = st.text_input("Phone Number*", value=patient_info.phone,
                                        placeholder="Format: (XXX) XXX-XXXX")
                with col3:
                    dob = st.date_input("Date of Birth*", 
                                    value=patient_info.date_of_birth or datetime.datetime.now().date() - datetime.timedelta(days=365*30),
                                    help="Select your date of birth from the calendar")
                
                # Address information with better visual grouping
                st.markdown("<h4 style='margin-top: 25px; margin-bottom: 15px;'>Address Information</h4>", unsafe_allow_html=True)
                
                st.text_input("Street Address", value=patient_info.address,
                            placeholder="Enter your current street address")
                
                col1, col2, col3 = st.columns([2,1,1])
                with col1:
                    city = st.text_input("City", value=patient_info.city,
                                      placeholder="Your city of residence")
                with col2:
                    state = st.text_input("State", value=patient_info.state,
                                       placeholder="State abbreviation")
                with col3:
                    zip_code = st.text_input("ZIP Code", value=patient_info.zip_code,
                                          placeholder="5-digit ZIP code")
                
                # Emergency contact with visual separation
                st.markdown("""
                <h4 style='margin-top: 25px; margin-bottom: 15px;'>Emergency Contact</h4>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please provide a contact person in case of emergency.
                </p>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    emergency_name = st.text_input("Emergency Contact Name", 
                                                value=patient_info.emergency_contact_name,
                                                placeholder="Full name of emergency contact")
                with col2:
                    emergency_phone = st.text_input("Emergency Contact Phone", 
                                                 value=patient_info.emergency_contact_phone,
                                                 placeholder="Emergency contact's phone number")
                
                # Required fields notice
                st.markdown("""
                <p style='margin-top: 25px; font-size: 0.9rem;'>* Required fields</p>
                """, unsafe_allow_html=True)
                
                # Enhanced consent checkbox
                consent = st.checkbox("I confirm that the information provided is accurate and complete to the best of my knowledge",
                                   value=True)
                
                # Submit button with professional styling
                submitted = st.form_submit_button("Save & Continue")
                
                if submitted:
                    # Validate required fields
                    if not (first_name and last_name and email and phone and dob and consent):
                        st.error("Please fill out all required fields and confirm your consent.")
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
                        
                        # Success message with more professional design
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Information Saved Successfully</h4>
                            <p style="margin-bottom: 0;">Your contact information has been securely stored. Please proceed to the Medical History form.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Offer navigation to next form
                        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                        if st.button("Continue to Medical History →", use_container_width=True):
                            page = "Medical History"
                            st.experimental_rerun()
            
            # Professional guidance note at the bottom
            st.markdown("""
            <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Privacy & Security</h4>
                <p style="margin-bottom: 0; font-size: 0.9rem;">
                    All information provided is protected by our privacy policy and HIPAA regulations. Your data is encrypted and access is restricted
                    to authorized healthcare professionals involved in your care. For questions about our privacy practices,
                    please contact our Privacy Officer at privacy@optimumwellness.org.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Medical History":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Medical History Form</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: import streamlit as st
from typing import Dict, List, Union, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import datetime
import random
import time
import json

# Define core persona elements as structured data
class PriorityLevel(Enum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

@dataclass
class ResponseFormat:
    steps: List[str]
    style: Dict[str, str]

@dataclass
class ChatMessage:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

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
        
        # Chat responses for various medical topics
        self.chat_responses = {
            "wellness": [
                "In our clinical approach to wellness optimization, we emphasize the integration of evidence-based lifestyle modifications with targeted interventions. The foundation begins with comprehensive assessment of metabolic, hormonal, and inflammatory markers.",
                "From a functional medicine perspective, wellness requires addressing root causes rather than symptom suppression. Our protocol typically evaluates sleep quality, nutritional status, stress management, and physical activity patterns as foundational elements.",
                "The current medical literature supports a multifaceted approach to wellness. This includes structured nutritional protocols, strategic supplementation based on identified deficiencies, and cognitive-behavioral interventions for stress management."
            ],
            "nutrition": [
                "Nutritional medicine forms a cornerstone of our functional approach. Current research indicates that personalized nutrition based on metabolic typing and inflammatory markers yields superior outcomes compared to generalized dietary recommendations.",
                "In our clinical practice, we utilize advanced nutritional assessments including micronutrient testing, food sensitivity panels, and metabolic markers to develop precision nutritional protocols tailored to individual biochemistry.",
                "The evidence supports targeted nutritional interventions rather than generalized approaches. We typically begin with elimination of inflammatory triggers, followed by structured reintroduction to identify optimal nutritional parameters."
            ],
            "sleep": [
                "Sleep optimization is fundamental to our clinical approach. Current research demonstrates that disrupted sleep architecture significantly impacts hormonal regulation, inflammatory markers, and cognitive function.",
                "Our protocol for sleep enhancement includes comprehensive assessment of circadian rhythm disruptions, evaluation of potential obstructive patterns, and analysis of neurochemical imbalances that may interfere with normal sleep progression.",
                "Evidence-based interventions for sleep quality improvement include structured sleep hygiene protocols, environmental optimization, and when indicated, targeted supplementation to address specific neurotransmitter imbalances."
            ],
            "stress": [
                "From a functional medicine perspective, chronic stress activation represents a significant driver of inflammatory processes and hormonal dysregulation. Our approach focuses on quantifiable assessment of HPA axis function.",
                "The clinical literature supports a structured approach to stress management, incorporating both physiological and psychological interventions. We utilize validated assessment tools to measure stress response patterns.",
                "Our protocol typically includes targeted adaptogenic support, structured cognitive reframing techniques, and autonomic nervous system regulation practices, all customized based on individual response patterns."
            ],
            "aging": [
                "Anti-aging medicine is approached from a scientific perspective in our practice. The focus remains on measurable biomarkers of cellular health, including telomere dynamics, oxidative stress parameters, and glycation endpoints.",
                "Current research supports interventions targeting specific aging mechanisms rather than general approaches. Our protocol evaluates mitochondrial function, inflammatory status, and hormonal optimization within physiological parameters.",
                "The evidence demonstrates that targeted interventions for biological age reduction must be personalized. We utilize comprehensive biomarker assessment to develop precision protocols for cellular rejuvenation."
            ],
            "hormones": [
                "Hormonal balance requires a comprehensive systems-based approach. Current clinical research indicates that evaluating the full spectrum of endocrine markers yields superior outcomes compared to isolated hormone assessment.",
                "Our protocol includes evaluation of steroid hormone pathways, thyroid function, and insulin dynamics. The integration of these systems provides a more accurate clinical picture than isolated assessment.",
                "Evidence-based hormonal optimization focuses on restoration of physiological patterns rather than simple supplementation. We utilize chronobiological principles to restore natural hormonal rhythms."
            ],
            "inflammation": [
                "Chronic inflammation represents a common pathway in numerous pathological processes. Our clinical approach includes comprehensive assessment of inflammatory markers and mediators to identify specific activation patterns.",
                "The research supports targeted anti-inflammatory protocols based on identified triggers rather than generalized approaches. We evaluate environmental, nutritional, and microbial factors in our assessment.",
                "Our evidence-based protocol typically includes elimination of inflammatory triggers, gastrointestinal barrier restoration, and targeted nutritional interventions to modulate specific inflammatory pathways."
            ],
            "detoxification": [
                "Detoxification capacity represents a critical element in our functional medicine assessment. We evaluate phase I and phase II detoxification pathways through validated biomarkers rather than generalized assumptions.",
                "The clinical evidence supports structured protocols for enhancing physiological detoxification processes. Our approach includes assessment of toxic burden alongside metabolic detoxification capacity.",
                "Our protocol typically includes strategic nutritional support for specific detoxification pathways, reduction of exposure sources, and enhancement of elimination mechanisms through validated clinical interventions."
            ],
            "gut_health": [
                "Gastrointestinal function serves as a cornerstone in our clinical assessment. Current research demonstrates the central role of gut integrity, microbiome diversity, and digestive efficiency in systemic health outcomes.",
                "Our protocol includes comprehensive evaluation of digestive function, intestinal permeability, microbial balance, and immunological markers to develop precision interventions for gastrointestinal optimization.",
                "The evidence supports a structured approach to gastrointestinal restoration, including targeted elimination of pathogenic factors, reestablishment of beneficial microbial communities, and restoration of mucosal integrity."
            ],
            "default": [
                "I would need to conduct a more thorough clinical assessment to provide specific recommendations regarding your inquiry. Our practice emphasizes evidence-based approaches customized to individual patient presentations.",
                "From a functional medicine perspective, addressing your concerns would require comprehensive evaluation of relevant biomarkers and clinical parameters. This allows for development of targeted interventions based on identified mechanisms.",
                "The current medical literature supports an individualized approach to your clinical question. Our protocol would include assessment of relevant systems followed by development of a structured intervention strategy."
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
    
    def get_chat_response(self, query: str) -> str:
        """Generates a chat response based on the query content"""
        # Determine the topic based on keywords in the query
        query_lower = query.lower()
        
        # Check for topic matches
        if any(word in query_lower for word in ["wellness", "well-being", "wellbeing", "health optimization"]):
            responses = self.chat_responses["wellness"]
        elif any(word in query_lower for word in ["nutrition", "diet", "food", "eating"]):
            responses = self.chat_responses["nutrition"]
        elif any(word in query_lower for word in ["sleep", "insomnia", "rest", "fatigue"]):
            responses = self.chat_responses["sleep"]
        elif any(word in query_lower for word in ["stress", "anxiety", "overwhelm", "burnout"]):
            responses = self.chat_responses["stress"]
        elif any(word in query_lower for word in ["aging", "longevity", "anti-aging"]):
            responses = self.chat_responses["aging"]
        elif any(word in query_lower for word in ["hormone", "thyroid", "estrogen", "testosterone"]):
            responses = self.chat_responses["hormones"]
        elif any(word in query_lower for word in ["inflammation", "inflammatory", "autoimmune"]):
            responses = self.chat_responses["inflammation"]
        elif any(word in query_lower for word in ["detox", "toxin", "cleanse"]):
            responses = self.chat_responses["detoxification"]
        elif any(word in query_lower for word in ["gut", "digestive", "stomach", "intestine", "microbiome"]):
            responses = self.chat_responses["gut_health"]
        else:
            responses = self.chat_responses["default"]
        
        # Select a response from the appropriate category
        return random.choice(responses)

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

def display_chat_message(message: ChatMessage):
    """Display a single chat message with appropriate styling"""
    if message.role == "assistant":
        with st.chat_message("assistant", avatar="🩺"):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%I:%M %p')}")
    else:  # user message
        with st.chat_message("user"):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%I:%M %p')}")

# Function to get descriptions for DEI focus areas
def get_dei_description(focus):
    descriptions = {
        "Maintain awareness of healthcare disparities": "We actively monitor and address inequities in healthcare access, treatment, and outcomes across different populations.",
        "Provide culturally competent care": "Our approach incorporates cultural factors and beliefs that may impact health behaviors and treatment preferences.",
        "Consider LGBTQ+ health perspectives": "We acknowledge unique health concerns and create supportive care environments for LGBTQ+ individuals.",
        "Implement inclusive language": "Our communications use terminology that respects diversity of identity, experience, and background.",
        "Address systemic healthcare barriers": "We work to identify and minimize structural obstacles that prevent equitable access to quality care."
    }
    return descriptions.get(focus, "")

# Function to get descriptions for intervention hierarchy
def get_hierarchy_description(hierarchy):
    descriptions = {
        "Remove pathological triggers": "Identify and eliminate factors that activate or perpetuate dysfunction",
        "Restore physiological function": "Support normal biological processes through targeted interventions",
        "Rebalance regulatory systems": "Address control mechanisms that coordinate multiple physiological processes",
        "Regenerate compromised tissues": "Support cellular renewal and structural integrity where needed",
        "Reestablish health maintenance": "Implement sustainable strategies for ongoing wellbeing"
    }
    return descriptions.get(hierarchy, "")

# Streamlit Application Implementation
def main():
    st.set_page_config(
        page_title="Dr. Jackson DNP - Medical Professional Consultation",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Dr. Jackson DNP - Professional Medical Consultation Platform",
            'Report a bug': "mailto:support@drjackson-platform.org",
            'Get help': "https://drjackson-platform.org/help"
        }
    )
    
    # Initialize persona and settings
    dr_jackson = DrJacksonPersona()
    llm_settings = LLMSettings()
    
    # Initialize session state for patient data if not exist
    if 'patient_contact_info' not in st.session_state:
        st.session_state['patient_contact_info'] = PatientContactInfo()
    if 'patient_medical_info' not in st.session_state:
        st.session_state['patient_medical_info'] = PatientMedicalInfo()
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    # Custom CSS for theming and professional layout
    st.markdown("""
    <style>
    :root {
        --primary-color: #5D5CDE;
        --secondary-color: #4B4BA3;
        --tertiary-color: #E0E0FA;
        --accent-color: #FF7D54;
        --light-bg: #FFFFFF;
        --off-white: #F8F9FA;
        --light-gray: #E9ECEF;
        --medium-gray: #CED4DA;
        --dark-gray: #6C757D;
        --dark-bg: #181818;
        --dark-mode-card: #2C2C2C;
        --light-text: #333333;
        --dark-text: #E5E5E5;
        --light-border: #E2E8F0;
        --dark-border: #374151;
        --light-input: #F9FAFB;
        --dark-input: #1F2937;
        --success-color: #3DC9A1;
        --warning-color: #FFBE55;
        --error-color: #FF5A5A;
        --info-color: #5AA0FF;
    }
    
    /* Base Styling */
    .stApp {
        background-color: var(--light-bg);
        color: var(--light-text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .dark-mode .stApp {
        background-color: var(--dark-bg);
        color: var(--dark-text);
    }
    
    /* Typography Refinements */
    h1 {
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.01em;
        color: var(--primary-color);
        margin-bottom: 1rem;
    }
    
    h2 {
        font-weight: 600;
        font-size: 1.8rem;
        letter-spacing: -0.01em;
        color: var(--primary-color);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-weight: 600;
        font-size: 1.4rem;
        color: var(--primary-color);
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    p, li {
        font-size: 1rem;
        line-height: 1.6;
        color: var(--light-text);
    }
    
    .dark-mode p, .dark-mode li {
        color: var(--dark-text);
    }
    
    /* Card/Container Styling */
    div[data-testid="stForm"] {
        background-color: var(--off-white);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        border: 1px solid var(--light-border);
        margin-bottom: 24px;
    }
    
    .dark-mode div[data-testid="stForm"] {
        background-color: var(--dark-mode-card);
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        border: 1px solid var(--dark-border);
    }
    
    /* Expander Styling */
    details {
        background-color: var(--off-white);
        border-radius: 8px;
        border: 1px solid var(--light-border);
        margin-bottom: 16px;
        overflow: hidden;
    }
    
    .dark-mode details {
        background-color: var(--dark-mode-card);
        border: 1px solid var(--dark-border);
    }
    
    details summary {
        padding: 16px;
        cursor: pointer;
        font-weight: 500;
    }
    
    details summary:hover {
        background-color: var(--light-gray);
    }
    
    .dark-mode details summary:hover {
        background-color: rgba(255,255,255,0.05);
    }
    
    /* Button Styling */
    .stButton button {
        background-color: var(--primary-color);
        color: white;
        font-weight: 500;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--off-white);
        border-right: 1px solid var(--light-border);
    }
    
    .dark-mode [data-testid="stSidebar"] {
        background-color: var(--dark-mode-card);
        border-right: 1px solid var(--dark-border);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 1.5rem;
    }
    
    /* Header Styling */
    .professional-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 15px rgba(93, 92, 222, 0.25);
    }
    
    .professional-header h1 {
        color: white;
        margin-bottom: 0.5rem;
        font-size: 2.4rem;
    }
    
    .professional-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* HIPAA Notice Styling */
    .hipaa-notice {
        background-color: var(--tertiary-color);
        border-left: 4px solid var(--primary-color);
        padding: 16px;
        margin: 20px 0;
        border-radius: 6px;
    }
    
    .dark-mode .hipaa-notice {
        background-color: rgba(93, 92, 222, 0.15);
    }
    
    /* Chat Styling */
    .chat-container {
        border-radius: 12px;
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border: 1px solid var(--light-border);
        background-color: var(--off-white);
    }
    
    .dark-mode .chat-container {
        border: 1px solid var(--dark-border);
        background-color: var(--dark-mode-card);
    }
    
    /* Chat Message Styling */
    [data-testid="stChatMessage"] {
        padding: 0.75rem 0;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
        background-color: var(--light-gray);
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
        background-color: var(--primary-color);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 10px 16px;
        background-color: var(--light-gray);
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color<div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 2 of 3: Medical Information</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced medical privacy notice
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                <h4 style="color: var(--info-color); margin-top: 0;">Medical Information Privacy</h4>
                <p>Your medical history is protected under HIPAA guidelines and will only be used to provide appropriate clinical care.</p>
                <p style="margin-bottom: 0; font-size: 0.9rem;">This information helps us develop a comprehensive understanding of your health status and will not be shared without your explicit consent.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get the current medical info from session state
            medical_info = st.session_state['patient_medical_info']
            
            # Enhanced form with better visual organization
            with st.form("medical_history_form"):
                # Primary care physician
                st.markdown("<h3 style='margin-top: 0; margin-bottom: 20px;'>Healthcare Provider Information</h3>", unsafe_allow_html=True)
                
                primary_care = st.text_input("Primary Care Physician", 
                                          value=medical_info.primary_care_physician,
                                          placeholder="Name of your current primary care provider")
                
                # Medication information with enhanced styling
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Current Medications</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please list all medications, supplements, and vitamins you are currently taking, including dosage if known.
                </p>
                """, unsafe_allow_html=True)
                
                medications_text = st.text_area(
                    "One medication per line (include dosage if known)", 
                    value="\n".join(medical_info.current_medications) if medical_info.current_medications else "",
                    height=120,
                    placeholder="Example:\nMetformin 500mg twice daily\nVitamin D3 2000 IU daily\nOmega-3 Fish Oil 1000mg daily"
                )
                
                # Allergies with better organization
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Allergies</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    List all known allergies including medications, foods, and environmental triggers. Include reaction type if known.
                </p>
                """, unsafe_allow_html=True)
                
                allergies_text = st.text_area(
                    "Please list all allergies (medications, foods, environmental)", 
                    value="\n".join(medical_info.allergies) if medical_info.allergies else "",
                    height=100,
                    placeholder="Example:\nPenicillin - rash and hives\nPeanuts - anaphylaxis\nPollen - seasonal rhinitis"
                )
                
                # Medical conditions with better visual organization
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Chronic Medical Conditions</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please list all diagnosed medical conditions including approximate date of diagnosis.
                </p>
                """, unsafe_allow_html=True)
                
                conditions_text = st.text_area(
                    "Please list all diagnosed medical conditions", 
                    value="\n".join(medical_info.chronic_conditions) if medical_info.chronic_conditions else "",
                    height=100,
                    placeholder="Example:\nHypertension - diagnosed 2018\nType 2 Diabetes - diagnosed 2020\nMigraine - diagnosed 2015"
                )
                
                # Surgical history with improved styling
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Surgical History</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please list all previous surgeries with approximate dates.
                </p>
                """, unsafe_allow_html=True)
                
                surgeries_text = st.text_area(
                    "Please list all previous surgeries with approximate dates", 
                    value="\n".join(medical_info.past_surgeries) if medical_info.past_surgeries else "",
                    height=100,
                    placeholder="Example:\nAppendectomy - 2010\nKnee arthroscopy - 2019\nTonsillectomy - childhood"
                )
                
                # Family medical history with better visual organization
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Family Medical History</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please indicate any significant family medical history, specifying the relationship to you.
                </p>
                """, unsafe_allow_html=True)
                
                # Use a more structured approach for family history
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
                            value=value,
                            placeholder=f"e.g., Father, Mother, Sibling"
                        )
                
                # Lifestyle section (added)
                st.markdown("""
                <h3 style='margin-top: 30px; margin-bottom: 15px;'>Lifestyle Information</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    This information helps us develop a more comprehensive understanding of your health status.
                </p>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.selectbox("Exercise Frequency", 
                                 options=["Select an option", "None", "Occasional (1-2 times/week)", 
                                          "Regular (3-4 times/week)", "Frequent (5+ times/week)"],
                                 index=0)
                    st.selectbox("Stress Level", 
                                 options=["Select an option", "Low", "Moderate", "High", "Very High"],
                                 index=0)
                with col2:
                    st.selectbox("Sleep Quality", 
                                 options=["Select an option", "Poor", "Fair", "Good", "Excellent"],
                                 index=0)
                    st.selectbox("Diet Quality", 
                                 options=["Select an option", "Poor", "Fair", "Good", "Excellent"],
                                 index=0)
                
                # Health goals section (added)
                st.markdown("""
                <h3 style='margin-top: 30px; margin-bottom: 15px;'>Health Goals</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please share your main health goals and what you hope to achieve through our care.
                </p>
                """, unsafe_allow_html=True)
                
                health_goals = st.text_area(
                    "Primary health objectives",
                    height=100,
                    placeholder="Example:\nImprove energy levels\nReduce chronic pain\nOptimize sleep quality\nAddress specific health concerns"
                )
                
                # Consent checkboxes with better styling
                st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
                history_consent = st.checkbox(
                    "I confirm that the information provided is accurate and complete to the best of my knowledge", 
                    value=True
                )
                sharing_consent = st.checkbox(
                    "I consent to the appropriate sharing of this information with healthcare providers involved in my care",
                    value=True
                )
                
                # Submit button with professional styling
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Save & Continue", use_container_width=True)
                
                if submitted:
                    # Process and save the data
                    if not (history_consent and sharing_consent):
                        st.error("Please confirm both consent statements to proceed.")
                    else:
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
                        
                        # Success message with professional styling
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Medical History Saved</h4>
                            <p style="margin-bottom: 0;">Your medical history has been securely stored. Thank you for providing this comprehensive information, which will help us deliver personalized care.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Offer navigation to consultation with better styling
                        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                        if st.button("Proceed to Consultation →", use_container_width=True):
                            page = "Consultation"
                            st.experimental_rerun()
            
            # Professional note at bottom
            st.markdown("""
            <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Why We Collect This Information</h4>
                <p style="font-size: 0.9rem; margin-bottom: 0;">
                    Comprehensive medical history allows us to develop personalized care plans based on your unique health profile.
                    This information helps identify patterns, assess risk factors, and determine optimal treatment approaches
                    following evidence-based functional medicine principles.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Consultation":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Professional Consultation</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 3 of 3: Consultation Request</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Check if patient info is filled out
            patient_info = st.session_state['patient_contact_info']
            medical_info = st.session_state['patient_medical_info']
            
            if not patient_info.first_name or not patient_info.last_name:
                # Warning with enhanced styling
                st.markdown("""
                <div style="background-color: rgba(255, 190, 85, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--warning-color);">
                    <h4 style="color: var(--warning-color); margin-top: 0;">Patient Information Required</h4>
                    <p style="margin-bottom: 15px;">Please complete the Patient Intake form before proceeding to consultation.</p>
                """, unsafe_allow_html=True)
                
                if st.button("Go to Patient Intake →", use_container_width=True):
                    page = "Patient Intake"
                    st.experimental_rerun()
                    
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                # Patient information summary with professional styling
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; border: 1px solid var(--light-border); margin-bottom: 30px;">
                    <h3 style="margin-top: 0;">Patient Information Summary</h3>
                    <div class="professional-separator"></div>
                    
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 15px;">
                """, unsafe_allow_html=True)
                
                # Patient details
                st.markdown(f"""
                        <div style="flex: 1; min-width: 250px;">
                            <h4 style="margin-top: 0; font-size: 1rem;">Personal Information</h4>
                            <p style="margin: 5px 0;"><strong>Name:</strong> {patient_info.first_name} {patient_info.last_name}</p>
                            <p style="margin: 5px 0;"><strong>Date of Birth:</strong> {patient_info.date_of_birth}</p>
                            <p style="margin: 5px 0;"><strong>Email:</strong> {patient_info.email}</p>
                            <p style="margin: 5px 0;"><strong>Phone:</strong> {patient_info.phone}</p>
                        </div>
                """, unsafe_allow_html=True)
                
                # Medical summary
                medical_conditions = ", ".join(medical_info.chronic_conditions[:3]) if medical_info.chronic_conditions else "None reported"
                if len(medical_info.chronic_conditions) > 3:
                    medical_conditions += " (and others)"
                    
                medications = ", ".join(medical_info.current_medications[:3]) if medical_info.current_medications else "None reported"
                if len(medical_info.current_medications) > 3:
                    medications += " (and others)"
                    
                allergies = ", ".join(medical_info.allergies[:3]) if medical_info.allergies else "None reported"
                if len(medical_info.allergies) > 3:
                    allergies += " (and others)"
                
                st.markdown(f"""
                        <div style="flex: 1; min-width: 250px;">
                            <h4 style="margin-top: 0; font-size: 1rem;">Medical Summary</h4>
                            <p style="margin: 5px 0;"><strong>Conditions:</strong> {medical_conditions}</p>
                            <p style="margin: 5px 0;"><strong>Medications:</strong> {medications}</p>
                            <p style="margin: 5px 0;"><strong>Allergies:</strong> {allergies}</p>
                            <p style="margin: 5px 0;"><strong>PCP:</strong> {medical_info.primary_care_physician or "Not provided"}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # HIPAA notice with enhanced styling
                st.markdown("""
                <div style="background-color: rgba(90, 160, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                    <h4 style="color: var(--info-color); margin-top: 0;">Consultation Privacy</h4>
                    <p style="margin-bottom: 0;">This consultation is protected under HIPAA guidelines. Information shared during this session is confidential and will be securely stored in your electronic medical record.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced consultation form
                with st.form("consultation_form"):
                    st.markdown("""
                    <h3 style="margin-top: 0; margin-bottom: 20px;">Consultation Request</h3>
                    """, unsafe_allow_html=True)
                    
                    # Primary reason with better styling
                    st.markdown("""
                    <h4 style="margin-bottom: 15px;">Primary Health Concern</h4>
                    <p style="margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);">
                        Please describe your current health concerns in detail. Include symptom duration, severity, and any patterns you've noticed.
                    </p>
                    """, unsafe_allow_html=True)
                    
                    primary_concern = st.text_area(
                        "Health concern description",
                        height=150,
                        placeholder="Please provide a detailed description of your main health concerns...",
                        help="Include symptom duration, severity, and any patterns you've noticed"
                    )
                    
                    # Specialty selection with better organization
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Clinical Focus Area</h4>
                    <p style="margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);">
                        Select the specialty area most relevant to your health concerns.
                    </p>
                    """, unsafe_allow_html=True)
                    
                    specialty_area = st.selectbox(
                        "Select the most relevant specialty area", 
                        options=dr_jackson.primary_domains + dr_jackson.secondary_domains
                    )
                    
                    # Symptom details with better visual organization
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Symptom Details</h4>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        symptom_onset = st.date_input(
                            "When did you first notice these symptoms?",
                            value=datetime.datetime.now().date() - datetime.timedelta(days=30),
                            help="Select the approximate date when symptoms first appeared"
                        )
                    with col2:
                        severity = st.select_slider(
                            "Rate the severity of your symptoms",
                            options=["Mild", "Moderate", "Significant", "Severe", "Extreme"],
                            help="Indicate the overall intensity of your symptoms"
                        )
                    
                    # Additional context with better layout
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Additional Context</h4>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        prior_treatments = st.text_area(
                            "Prior treatments or approaches tried",
                            height=120,
                            placeholder="List any treatments, medications, or approaches you've already attempted..."
                        )
                    with col2:
                        triggers = st.text_area(
                            "Known triggers or patterns",
                            height=120,
                            placeholder="Describe any factors that worsen or improve your symptoms..."
                        )
                    
                    # Goals with better styling
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Treatment Goals</h4>
                    <p style="margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);">
                        What outcomes are you hoping to achieve through this consultation?
                    </p>
                    """, unsafe_allow_html=True)
                    
                    goals = st.text_area(
                        "Desired outcomes",
                        height=120,
                        placeholder="Describe your health goals and expectations from this consultation..."
                    )
                    
                    # Appointment preference (added)
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Appointment Preference</h4>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        appointment_type = st.radio(
                            "Preferred consultation type",
                            options=["Virtual (Telehealth)", "In-person Office Visit"],
                            index=0
                        )
                    with col2:
                        urgency = st.select_slider(
                            "Consultation urgency",
                            options=["Standard (within 2 weeks)", "Priority (within 1 week)", "Urgent (within 48 hours)"],
                            value="Standard (within 2 weeks)"
                        )
                    
                    # Enhanced consent checkbox
                    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
                    consultation_consent = st.checkbox(
                        "I understand that this consultation request will be reviewed by Dr. Jackson, and follow-up may be required before treatment recommendations are provided",
                        value=True
                    )
                    
                    # Submit button with better styling
                    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                    submitted = st.form_submit_button("Submit Consultation Request", use_container_width=True)
                
                # Form handling logic
                if submitted:
                    if not primary_concern:
                        st.error("Please describe your health concerns before submitting.")
                    elif not consultation_consent:
                        st.error("Please confirm your understanding of the consultation process.")
                    else:
                        # Success message with professional styling
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Consultation Request Submitted</h4>
                            <p style="margin-bottom: 10px;">Your request has been successfully received and will be reviewed by Dr. Jackson.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display a professional response using the persona
                        st.markdown("""
                        <div style="background-color: var(--off-white); padding: 25px; border-radius: 10px; border: 1px solid var(--light-border); margin-top: 30px;">
                            <h3 style="margin-top: 0;">Initial Assessment</h3>
                            <div class="professional-separator"></div>
                        """, unsafe_allow_html=True)
                        
                        # Determine appropriate recommendations based on specialty area
                        if specialty_area in dr_jackson.primary_domains[:3]:  # First 3 primary domains
                            recommendations = [
                                "Schedule a comprehensive initial evaluation",
                                "Complete the detailed symptom assessment questionnaire",
                                "Prepare any prior lab work or diagnostic studies for review",
                                "Consider keeping a symptom journal for the next 7 days"
                            ]
                        else:
                            recommendations = [
                                "Schedule an initial consultation",
                                "Gather relevant medical records and previous test results",
                                "Complete preliminary health assessment questionnaires",
                                "Prepare a list of specific questions for your consultation"
                            ]
                        
                        # Use the persona to format the response with better styling
                        assessment = f"Based on your initial information regarding {specialty_area.lower()} concerns of {severity.lower()} severity, a professional evaluation is indicated. Your symptoms beginning approximately {(datetime.datetime.now().date() - symptom_onset).days} days ago warrant a thorough assessment."
                        
                        st.markdown(f"""
                            <div style="margin-bottom: 20px;">
                                <h4 style="margin-bottom: 10px; font-size: 1.1rem;">Clinical Overview</h4>
                                <p style="margin-bottom: 5px;"><strong>Presenting Concerns:</strong> {specialty_area} issues with {severity.lower()} symptoms</p>
                                <p style="margin-bottom: 5px;"><strong>Duration:</strong> Approximately {(datetime.datetime.now().date() - symptom_onset).days} days</p>
                                <p style="margin-bottom: 5px;"><strong>Requested Format:</strong> {appointment_type}</p>
                                <p><strong>Urgency Level:</strong> {urgency}</p>
                            </div>
                            
                            <div style="margin-bottom: 20px;">
                                <h4 style="margin-bottom: 10px; font-size: 1.1rem;">Professional Assessment</h4>
                                <p>{assessment}</p>
                            </div>
                            
                            <div>
                                <h4 style="margin-bottom: 10px; font-size: 1.1rem;">Recommendations</h4>
                                <ul>
                        """, unsafe_allow_html=True)
                        
                        for rec in recommendations:
                            st.markdown(f"""
                                <li style="margin-bottom: 8px;">{rec}</li>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("""
                                </ul>
                            </div>
                            
                            <p style="margin-top: 20px; font-style: italic;">Please confirm your understanding of these recommendations and your intent to proceed with the next steps.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Next steps with professional styling
                        st.markdown("""
                        <div style="margin-top: 30px;">
                            <h3>Next Steps</h3>
                            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-top: 15px;">
                                <p style="margin: 0;">You will receive a detailed follow-up within 24-48 hours with additional instructions and appointment scheduling options.</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # AI-assisted note section with professional styling
                        if st.session_state.get('anthropic_api_key') or st.session_state.get('openai_api_key'):
                            st.markdown("""
                            <div style="margin-top: 40px;">
                                <h3>AI-Assisted Clinical Notes</h3>
                                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; border: 1px solid var(--light-border); margin-top: 15px;">
                            """, unsafe_allow_html=True)
                            
                            with st.spinner("Generating preliminary clinical notes..."):
                                # This would normally call an LLM API
                                time.sleep(2)  # Simulate processing time
                                
                                st.markdown("""
                                    <h4 style="margin-top: 0; color: var(--primary-color);">PRELIMINARY ASSESSMENT NOTE</h4>
                                    <p style="margin-bottom: 15px;">
                                        Patient presents with concerns related to the selected specialty area. 
                                        Initial impression suggests further evaluation is warranted to establish 
                                        a differential diagnosis and treatment approach. Patient goals and symptom 
                                        presentation will be incorporated into the comprehensive care plan.
                                    </p>
                                    <p style="font-style: italic; font-size: 0.9rem; margin-bottom: 0; color: var(--dark-gray);">
                                        This preliminary note was generated with AI assistance and will be 
                                        reviewed by Dr. Jackson prior to formal documentation.
                                    </p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Additional guidance at bottom of page
                st.markdown("""
                <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0;">What to Expect</h4>
                    <p style="font-size: 0.9rem; margin-bottom: 0;">
                        After submitting your consultation request, our clinical team will review your information and 
                        reach out to schedule your appointment. For urgent medical concerns requiring immediate attention, 
                        please contact your primary care provider or visit the nearest emergency department.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        elif page == "Chat with Dr. Jackson":
            # Professional header
            st.markdown("""
            <h1>Professional Chat Consultation</h1>
            <div class="professional-separator" style="width: 150px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
                
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--tertiary-color);
        font-weight: 500;
    }
    
    /* Alert/Notice Styling */
    .info-box {
        background-color: rgba(90, 160, 255, 0.1);
        border-left: 4px solid var(--info-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .success-box {
        background-color: rgba(61, 201, 161, 0.1);
        border-left: 4px solid var(--success-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .warning-box {
        background-color: rgba(255, 190, 85, 0.1);
        border-left: 4px solid var(--warning-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .error-box {
        background-color: rgba(255, 90, 90, 0.1);
        border-left: 4px solid var(--error-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    /* Progress Bar Styling */
    [data-testid="stProgressBar"] > div {
        background-color: var(--primary-color);
        height: 8px;
        border-radius: 4px;
    }
    
    [data-testid="stProgressBar"] > div:nth-child(1) {
        background-color: var(--light-gray);
    }
    
    /* Section Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            rgba(0,0,0,0), 
            var(--medium-gray), 
            rgba(0,0,0,0));
    }
    
    .dark-mode hr {
        background: linear-gradient(90deg, 
            rgba(0,0,0,0), 
            var(--dark-border), 
            rgba(0,0,0,0));
    }
    
    /* Info Cards Grid */
    .info-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 16px;
        margin: 20px 0;
    }
    
    .info-card {
        background-color: var(--off-white);
        border-radius: 8px;
        border: 1px solid var(--light-border);
        padding: 20px;
        transition: all 0.2s ease;
    }
    
    .info-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    .dark-mode .info-card {
        background-color: var(--dark-mode-card);
        border: 1px solid var(--dark-border);
    }
    
    .dark-mode .info-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Custom Utility Classes */
    .text-center {
        text-align: center;
    }
    
    .mb-0 {
        margin-bottom: 0 !important;
    }
    
    .mt-0 {
        margin-top: 0 !important;
    }
    
    .professional-separator {
        height: 5px;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        margin: 12px 0;
        border-radius: 3px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional App Header with Logo
    st.markdown(f"""
    <div class="professional-header">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h1>Dr. Jackson, {dr_jackson.credentials}</h1>
                <p>{dr_jackson.practice_name}</p>
            </div>
            <div style="text-align: right;">
                <p style="font-size: 0.9rem; opacity: 0.8;">Advancing Integrative Medicine</p>
                <p style="font-size: 0.8rem; opacity: 0.7;">Established 2015</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Professionally designed sidebar
    with st.sidebar:
        # Add a subtle medical/professional icon or logo
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); 
                       width: 60px; height: 60px; border-radius: 50%; display: inline-flex; 
                       align-items: center; justify-content: center; margin-bottom: 10px;">
                <span style="color: white; font-size: 30px;">🩺</span>
            </div>
            <p style="font-weight: 600; margin: 0; font-size: 16px;">Dr. Jackson Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='margin-top: 0;'>Navigation</h3>", unsafe_allow_html=True)
        
        # Enhanced navigation with section grouping
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; color: var(--dark-gray);'>Patient Portal</p>", unsafe_allow_html=True)
        patient_page = st.radio("", [
            "Home", 
            "Patient Intake", 
            "Medical History",
            "Consultation"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>Communication</p>", unsafe_allow_html=True)
        communication_page = st.radio("", [
            "Chat with Dr. Jackson"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>Information</p>", unsafe_allow_html=True)
        info_page = st.radio("", [
            "Specialties", 
            "Approach",
            "Resources"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>System</p>", unsafe_allow_html=True)
        system_page = st.radio("", [
            "Settings"
        ], label_visibility="collapsed")
        
        # Determine selected page from all radio groups
        if patient_page != "Home":
            page = patient_page
        elif communication_page != "Chat with Dr. Jackson":
            page = "Chat with Dr. Jackson"
        elif info_page != "Specialties":
            page = info_page
        elif system_page != "Settings":
            page = system_page
        else:
            page = "Home"
        
        # Theme selection with better design
        st.markdown("---")
        st.markdown("<h4 style='margin-bottom: 10px;'>Appearance</h4>", unsafe_allow_html=True)
        theme_cols = st.columns([1, 3])
        with theme_cols[0]:
            st.markdown("🎨")
        with theme_cols[1]:
            theme = st.selectbox("", ["Light", "Dark"], label_visibility="collapsed")
        
        if theme == "Dark":
            st.markdown("""
            <script>
                document.body.classList.add('dark-mode');
            </script>
            """, unsafe_allow_html=True)
        
        # Professional info section
        st.markdown("---")
        st.markdown("<h4 style='margin-bottom: 10px;'>About Dr. Jackson</h4>", unsafe_allow_html=True)
        
        # More professional specialty display
        domains = ", ".join(dr_jackson.primary_domains[:3])
        st.markdown(f"""
        <div style="background-color: var(--off-white); padding: 12px; border-radius: 8px; border: 1px solid var(--light-border); margin-bottom: 15px;">
            <p style="font-weight: 500; margin-bottom: 5px;">Specializing in:</p>
            <p style="color: var(--primary-color); font-weight: 600; margin: 0;">{domains}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Current date - maintaining professional approach
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background-color: var(--primary-color); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                <span style="color: white;">📅</span>
            </div>
            <div>
                <p style="font-size: 0.85rem; margin: 0; opacity: 0.7;">Today's Date</p>
                <p style="font-weight: 500; margin: 0;">{current_date}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show logged in status if patient info exists
        patient_info = st.session_state['patient_contact_info']
        if patient_info.first_name and patient_info.last_name:
            st.markdown(f"""
            <div style="background-color: rgba(61, 201, 161, 0.1); border-left: 4px solid var(--success-color); padding: 12px; border-radius: 6px;">
                <p style="font-weight: 500; margin: 0;">Logged in as:</p>
                <p style="margin: 5px 0 0 0;">{patient_info.first_name} {patient_info.last_name}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Container for main content with professional layout
    main_container = st.container()
    with main_container:
        # Main content area based on page selection
        if page == "Home":
            st.header("Welcome to Dr. Jackson's Professional Consultation")
            
            # Enhanced HIPAA Notice with more professional design
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; 
                       border-left: 5px solid var(--info-color); margin-bottom: 30px;">
                <h4 style="color: var(--info-color); margin-top: 0;">HIPAA Compliance Notice</h4>
                <p style="margin-bottom: 10px;">This application complies with the Health Insurance Portability and Accountability Act (HIPAA) of 1996:</p>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                    <li style="margin-bottom: 5px;">All patient data is encrypted in transit and at rest</li>
                    <li style="margin-bottom: 5px;">Access controls restrict unauthorized viewing of protected health information (PHI)</li>
                    <li style="margin-bottom: 5px;">Audit logs track all data access and modifications</li>
                    <li style="margin-bottom: 5px;">Data retention policies comply with medical record requirements</li>
                    <li style="margin-bottom: 5px;">Regular security assessments are conducted to ensure compliance</li>
                </ul>
                <p style="margin-top: 10px; margin-bottom: 0; font-weight: 500;"><span style="color: var(--info-color);">Privacy Officer Contact:</span> privacy@optimumwellness.org</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Featured specialties in cards layout
            st.markdown("### Our Clinical Specialties")
            st.markdown("""
            <p style="margin-bottom: 25px;">Dr. Jackson's practice provides comprehensive medical consultation with expertise in the following areas:</p>
            """, unsafe_allow_html=True)
            
            # Create a grid layout with cards for specialties
            st.markdown("""
            <div class="info-card-grid">
            """, unsafe_allow_html=True)
            
            for domain in dr_jackson.primary_domains:
                icon = "🧠" if domain == "Psychiatric Care" else "✨" if domain == "Wellness Optimization" else "⏱️" if domain == "Anti-aging Medicine" else "🔬" if domain == "Functional Medicine" else "🌿" if domain == "Integrative Health" else "🛡️"
                
                st.markdown(f"""
                <div class="info-card">
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                            <span style="font-size: 20px;">{icon}</span>
                        </div>
                        <h4 style="margin: 0; color: var(--primary-color);">{domain}</h4>
                    </div>
                    <div class="professional-separator"></div>
                    <p style="margin-top: 10px; font-size: 0.9rem;">Comprehensive, evidence-based approach to {domain.lower()} through integrated assessment and personalized protocols.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Professional approach section with better design
            st.markdown("### Professional Approach")
            
            # Two-column layout for approach and values
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 12px; border: 1px solid var(--light-border); height: 100%;">
                    <h4 style="margin-top: 0;">Clinical Methodology</h4>
                    <div class="professional-separator"></div>
                    <p>Dr. Jackson's practice is built on a hierarchical approach to medical knowledge and evidence:</p>
                    <ul>
                        <li><strong>Evidence-based research</strong> forms the foundation of all clinical decisions</li>
                        <li><strong>Clinical guidelines</strong> provide standardized frameworks for treatment protocols</li>
                        <li><strong>Professional experience</strong> guides the application of research to individual cases</li>
                        <li><strong>Holistic assessment</strong> ensures comprehensive evaluation of all contributing factors</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 12px; border: 1px solid var(--light-border); height: 100%;">
                    <h4 style="margin-top: 0;">Core Values</h4>
                    <div class="professional-separator"></div>
                    <ul>
                """, unsafe_allow_html=True)
                
                for i, value in enumerate(dr_jackson.core_values[:4]):
                    st.markdown(f"""
                    <li style="margin-bottom: 10px;">
                        <strong style="color: var(--primary-color);">{value}:</strong> 
                        Ensuring the highest standards of care through rigorous application of professional principles
                    </li>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Call to action section with enhanced design
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Begin Your Care Journey</h3>
            <div style="background: linear-gradient(135deg, rgba(93, 92, 222, 0.1) 0%, rgba(93, 92, 222, 0.05) 100%); 
                 padding: 30px; border-radius: 12px; margin-bottom: 30px; border: 1px solid rgba(93, 92, 222, 0.2);">
                <p style="font-size: 1.1rem; margin-bottom: 20px;">
                    To begin the consultation process, please complete the Patient Intake forms first. This will help us provide
                    the most appropriate clinical guidance tailored to your specific health needs.
                </p>
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("📋 Go to Patient Intake", key="home_intake_btn"):
                page = "Patient Intake"
                st.experimental_rerun()
                
            st.markdown("""
                    </div>
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("🔍 Learn About Specialties", key="home_specialties_btn"):
                page = "Specialties"
                st.experimental_rerun()
                
            st.markdown("""
                    </div>
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("💬 Chat with Dr. Jackson", key="home_chat_btn"):
                page = "Chat with Dr. Jackson"
                st.experimental_rerun()
            
            st.markdown("""
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Testimonials or professional credentials section
            st.markdown("""
            <div style="background-color: var(--off-white); padding: 25px; border-radius: 12px; border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Professional Credentials</h4>
                <div class="professional-separator"></div>
                <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 15px;">
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">🎓</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Education</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Doctorate in Nursing Practice</p>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">📜</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Certification</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Family Nurse Practitioner-Certified</p>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">🔬</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Specialization</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Certified Functional Medicine Practitioner</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Patient Intake":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Patient Intake Form</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 1 of 3: Contact Information</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced data privacy notice
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                <h4 style="color: var(--info-color); margin-top: 0;">Data Privacy Notice</h4>
                <p>All information submitted is encrypted and protected in accordance with HIPAA regulations.
                Your privacy is our priority. Information is only accessible to authorized medical personnel.</p>
                <p style="margin-bottom: 0; font-size: 0.9rem;"><strong>Security Measures:</strong> End-to-end encryption, secure database storage, access control mechanisms</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get the current patient info from session state
            patient_info = st.session_state['patient_contact_info']
            
            # Create the form with enhanced styling
            with st.form("patient_contact_form"):
                st.markdown("""
                <h3 style="margin-top: 0; margin-bottom: 20px;">Personal Information</h3>
                """, unsafe_allow_html=True)
                
                # Name information with professional layout
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name*", value=patient_info.first_name,
                                            placeholder="Enter your legal first name")
                with col2:
                    last_name = st.text_input("Last Name*", value=patient_info.last_name,
                                          placeholder="Enter your legal last name")
                
                # Contact information with more structured layout
                st.markdown("<h4 style='margin-top: 25px; margin-bottom: 15px;'>Contact Details</h4>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2,2,1])
                with col1:
                    email = st.text_input("Email Address*", value=patient_info.email,
                                        placeholder="Your primary email address")
                with col2:
                    phone = st.text_input("Phone Number*", value=patient_info.phone,
                                        placeholder="Format: (XXX) XXX-XXXX")
                with col3:
                    dob = st.date_input("Date of Birth*", 
                                    value=patient_info.date_of_birth or datetime.datetime.now().date() - datetime.timedelta(days=365*30),
                                    help="Select your date of birth from the calendar")
                
                # Address information with better visual grouping
                st.markdown("<h4 style='margin-top: 25px; margin-bottom: 15px;'>Address Information</h4>", unsafe_allow_html=True)
                
                st.text_input("Street Address", value=patient_info.address,
                            placeholder="Enter your current street address")
                
                col1, col2, col3 = st.columns([2,1,1])
                with col1:
                    city = st.text_input("City", value=patient_info.city,
                                      placeholder="Your city of residence")
                with col2:
                    state = st.text_input("State", value=patient_info.state,
                                       placeholder="State abbreviation")
                with col3:
                    zip_code = st.text_input("ZIP Code", value=patient_info.zip_code,
                                          placeholder="5-digit ZIP code")
                
                # Emergency contact with visual separation
                st.markdown("""
                <h4 style='margin-top: 25px; margin-bottom: 15px;'>Emergency Contact</h4>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please provide a contact person in case of emergency.
                </p>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    emergency_name = st.text_input("Emergency Contact Name", 
                                                value=patient_info.emergency_contact_name,
                                                placeholder="Full name of emergency contact")
                with col2:
                    emergency_phone = st.text_input("Emergency Contact Phone", 
                                                 value=patient_info.emergency_contact_phone,
                                                 placeholder="Emergency contact's phone number")
                
                # Required fields notice
                st.markdown("""
                <p style='margin-top: 25px; font-size: 0.9rem;'>* Required fields</p>
                """, unsafe_allow_html=True)
                
                # Enhanced consent checkbox
                consent = st.checkbox("I confirm that the information provided is accurate and complete to the best of my knowledge",
                                   value=True)
                
                # Submit button with professional styling
                submitted = st.form_submit_button("Save & Continue")
                
                if submitted:
                    # Validate required fields
                    if not (first_name and last_name and email and phone and dob and consent):
                        st.error("Please fill out all required fields and confirm your consent.")
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
                        
                        # Success message with more professional design
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Information Saved Successfully</h4>
                            <p style="margin-bottom: 0;">Your contact information has been securely stored. Please proceed to the Medical History form.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Offer navigation to next form
                        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                        if st.button("Continue to Medical History →", use_container_width=True):
                            page = "Medical History"
                            st.experimental_rerun()
            
            # Professional guidance note at the bottom
            st.markdown("""
            <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Privacy & Security</h4>
                <p style="margin-bottom: 0; font-size: 0.9rem;">
                    All information provided is protected by our privacy policy and HIPAA regulations. Your data is encrypted and access is restricted
                    to authorized healthcare professionals involved in your care. For questions about our privacy practices,
                    please contact our Privacy Officer at privacy@optimumwellness.org.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Medical History":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Medical History Form</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: import streamlit as st
from typing import Dict, List, Union, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import datetime
import random
import time
import json

# Define core persona elements as structured data
class PriorityLevel(Enum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

@dataclass
class ResponseFormat:
    steps: List[str]
    style: Dict[str, str]

@dataclass
class ChatMessage:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

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
        
        # Chat responses for various medical topics
        self.chat_responses = {
            "wellness": [
                "In our clinical approach to wellness optimization, we emphasize the integration of evidence-based lifestyle modifications with targeted interventions. The foundation begins with comprehensive assessment of metabolic, hormonal, and inflammatory markers.",
                "From a functional medicine perspective, wellness requires addressing root causes rather than symptom suppression. Our protocol typically evaluates sleep quality, nutritional status, stress management, and physical activity patterns as foundational elements.",
                "The current medical literature supports a multifaceted approach to wellness. This includes structured nutritional protocols, strategic supplementation based on identified deficiencies, and cognitive-behavioral interventions for stress management."
            ],
            "nutrition": [
                "Nutritional medicine forms a cornerstone of our functional approach. Current research indicates that personalized nutrition based on metabolic typing and inflammatory markers yields superior outcomes compared to generalized dietary recommendations.",
                "In our clinical practice, we utilize advanced nutritional assessments including micronutrient testing, food sensitivity panels, and metabolic markers to develop precision nutritional protocols tailored to individual biochemistry.",
                "The evidence supports targeted nutritional interventions rather than generalized approaches. We typically begin with elimination of inflammatory triggers, followed by structured reintroduction to identify optimal nutritional parameters."
            ],
            "sleep": [
                "Sleep optimization is fundamental to our clinical approach. Current research demonstrates that disrupted sleep architecture significantly impacts hormonal regulation, inflammatory markers, and cognitive function.",
                "Our protocol for sleep enhancement includes comprehensive assessment of circadian rhythm disruptions, evaluation of potential obstructive patterns, and analysis of neurochemical imbalances that may interfere with normal sleep progression.",
                "Evidence-based interventions for sleep quality improvement include structured sleep hygiene protocols, environmental optimization, and when indicated, targeted supplementation to address specific neurotransmitter imbalances."
            ],
            "stress": [
                "From a functional medicine perspective, chronic stress activation represents a significant driver of inflammatory processes and hormonal dysregulation. Our approach focuses on quantifiable assessment of HPA axis function.",
                "The clinical literature supports a structured approach to stress management, incorporating both physiological and psychological interventions. We utilize validated assessment tools to measure stress response patterns.",
                "Our protocol typically includes targeted adaptogenic support, structured cognitive reframing techniques, and autonomic nervous system regulation practices, all customized based on individual response patterns."
            ],
            "aging": [
                "Anti-aging medicine is approached from a scientific perspective in our practice. The focus remains on measurable biomarkers of cellular health, including telomere dynamics, oxidative stress parameters, and glycation endpoints.",
                "Current research supports interventions targeting specific aging mechanisms rather than general approaches. Our protocol evaluates mitochondrial function, inflammatory status, and hormonal optimization within physiological parameters.",
                "The evidence demonstrates that targeted interventions for biological age reduction must be personalized. We utilize comprehensive biomarker assessment to develop precision protocols for cellular rejuvenation."
            ],
            "hormones": [
                "Hormonal balance requires a comprehensive systems-based approach. Current clinical research indicates that evaluating the full spectrum of endocrine markers yields superior outcomes compared to isolated hormone assessment.",
                "Our protocol includes evaluation of steroid hormone pathways, thyroid function, and insulin dynamics. The integration of these systems provides a more accurate clinical picture than isolated assessment.",
                "Evidence-based hormonal optimization focuses on restoration of physiological patterns rather than simple supplementation. We utilize chronobiological principles to restore natural hormonal rhythms."
            ],
            "inflammation": [
                "Chronic inflammation represents a common pathway in numerous pathological processes. Our clinical approach includes comprehensive assessment of inflammatory markers and mediators to identify specific activation patterns.",
                "The research supports targeted anti-inflammatory protocols based on identified triggers rather than generalized approaches. We evaluate environmental, nutritional, and microbial factors in our assessment.",
                "Our evidence-based protocol typically includes elimination of inflammatory triggers, gastrointestinal barrier restoration, and targeted nutritional interventions to modulate specific inflammatory pathways."
            ],
            "detoxification": [
                "Detoxification capacity represents a critical element in our functional medicine assessment. We evaluate phase I and phase II detoxification pathways through validated biomarkers rather than generalized assumptions.",
                "The clinical evidence supports structured protocols for enhancing physiological detoxification processes. Our approach includes assessment of toxic burden alongside metabolic detoxification capacity.",
                "Our protocol typically includes strategic nutritional support for specific detoxification pathways, reduction of exposure sources, and enhancement of elimination mechanisms through validated clinical interventions."
            ],
            "gut_health": [
                "Gastrointestinal function serves as a cornerstone in our clinical assessment. Current research demonstrates the central role of gut integrity, microbiome diversity, and digestive efficiency in systemic health outcomes.",
                "Our protocol includes comprehensive evaluation of digestive function, intestinal permeability, microbial balance, and immunological markers to develop precision interventions for gastrointestinal optimization.",
                "The evidence supports a structured approach to gastrointestinal restoration, including targeted elimination of pathogenic factors, reestablishment of beneficial microbial communities, and restoration of mucosal integrity."
            ],
            "default": [
                "I would need to conduct a more thorough clinical assessment to provide specific recommendations regarding your inquiry. Our practice emphasizes evidence-based approaches customized to individual patient presentations.",
                "From a functional medicine perspective, addressing your concerns would require comprehensive evaluation of relevant biomarkers and clinical parameters. This allows for development of targeted interventions based on identified mechanisms.",
                "The current medical literature supports an individualized approach to your clinical question. Our protocol would include assessment of relevant systems followed by development of a structured intervention strategy."
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
    
    def get_chat_response(self, query: str) -> str:
        """Generates a chat response based on the query content"""
        # Determine the topic based on keywords in the query
        query_lower = query.lower()
        
        # Check for topic matches
        if any(word in query_lower for word in ["wellness", "well-being", "wellbeing", "health optimization"]):
            responses = self.chat_responses["wellness"]
        elif any(word in query_lower for word in ["nutrition", "diet", "food", "eating"]):
            responses = self.chat_responses["nutrition"]
        elif any(word in query_lower for word in ["sleep", "insomnia", "rest", "fatigue"]):
            responses = self.chat_responses["sleep"]
        elif any(word in query_lower for word in ["stress", "anxiety", "overwhelm", "burnout"]):
            responses = self.chat_responses["stress"]
        elif any(word in query_lower for word in ["aging", "longevity", "anti-aging"]):
            responses = self.chat_responses["aging"]
        elif any(word in query_lower for word in ["hormone", "thyroid", "estrogen", "testosterone"]):
            responses = self.chat_responses["hormones"]
        elif any(word in query_lower for word in ["inflammation", "inflammatory", "autoimmune"]):
            responses = self.chat_responses["inflammation"]
        elif any(word in query_lower for word in ["detox", "toxin", "cleanse"]):
            responses = self.chat_responses["detoxification"]
        elif any(word in query_lower for word in ["gut", "digestive", "stomach", "intestine", "microbiome"]):
            responses = self.chat_responses["gut_health"]
        else:
            responses = self.chat_responses["default"]
        
        # Select a response from the appropriate category
        return random.choice(responses)

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

def display_chat_message(message: ChatMessage):
    """Display a single chat message with appropriate styling"""
    if message.role == "assistant":
        with st.chat_message("assistant", avatar="🩺"):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%I:%M %p')}")
    else:  # user message
        with st.chat_message("user"):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%I:%M %p')}")

# Function to get descriptions for DEI focus areas
def get_dei_description(focus):
    descriptions = {
        "Maintain awareness of healthcare disparities": "We actively monitor and address inequities in healthcare access, treatment, and outcomes across different populations.",
        "Provide culturally competent care": "Our approach incorporates cultural factors and beliefs that may impact health behaviors and treatment preferences.",
        "Consider LGBTQ+ health perspectives": "We acknowledge unique health concerns and create supportive care environments for LGBTQ+ individuals.",
        "Implement inclusive language": "Our communications use terminology that respects diversity of identity, experience, and background.",
        "Address systemic healthcare barriers": "We work to identify and minimize structural obstacles that prevent equitable access to quality care."
    }
    return descriptions.get(focus, "")

# Function to get descriptions for intervention hierarchy
def get_hierarchy_description(hierarchy):
    descriptions = {
        "Remove pathological triggers": "Identify and eliminate factors that activate or perpetuate dysfunction",
        "Restore physiological function": "Support normal biological processes through targeted interventions",
        "Rebalance regulatory systems": "Address control mechanisms that coordinate multiple physiological processes",
        "Regenerate compromised tissues": "Support cellular renewal and structural integrity where needed",
        "Reestablish health maintenance": "Implement sustainable strategies for ongoing wellbeing"
    }
    return descriptions.get(hierarchy, "")

# Streamlit Application Implementation
def main():
    st.set_page_config(
        page_title="Dr. Jackson DNP - Medical Professional Consultation",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Dr. Jackson DNP - Professional Medical Consultation Platform",
            'Report a bug': "mailto:support@drjackson-platform.org",
            'Get help': "https://drjackson-platform.org/help"
        }
    )
    
    # Initialize persona and settings
    dr_jackson = DrJacksonPersona()
    llm_settings = LLMSettings()
    
    # Initialize session state for patient data if not exist
    if 'patient_contact_info' not in st.session_state:
        st.session_state['patient_contact_info'] = PatientContactInfo()
    if 'patient_medical_info' not in st.session_state:
        st.session_state['patient_medical_info'] = PatientMedicalInfo()
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    # Custom CSS for theming and professional layout
    st.markdown("""
    <style>
    :root {
        --primary-color: #5D5CDE;
        --secondary-color: #4B4BA3;
        --tertiary-color: #E0E0FA;
        --accent-color: #FF7D54;
        --light-bg: #FFFFFF;
        --off-white: #F8F9FA;
        --light-gray: #E9ECEF;
        --medium-gray: #CED4DA;
        --dark-gray: #6C757D;
        --dark-bg: #181818;
        --dark-mode-card: #2C2C2C;
        --light-text: #333333;
        --dark-text: #E5E5E5;
        --light-border: #E2E8F0;
        --dark-border: #374151;
        --light-input: #F9FAFB;
        --dark-input: #1F2937;
        --success-color: #3DC9A1;
        --warning-color: #FFBE55;
        --error-color: #FF5A5A;
        --info-color: #5AA0FF;
    }
    
    /* Base Styling */
    .stApp {
        background-color: var(--light-bg);
        color: var(--light-text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .dark-mode .stApp {
        background-color: var(--dark-bg);
        color: var(--dark-text);
    }
    
    /* Typography Refinements */
    h1 {
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.01em;
        color: var(--primary-color);
        margin-bottom: 1rem;
    }
    
    h2 {
        font-weight: 600;
        font-size: 1.8rem;
        letter-spacing: -0.01em;
        color: var(--primary-color);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-weight: 600;
        font-size: 1.4rem;
        color: var(--primary-color);
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    p, li {
        font-size: 1rem;
        line-height: 1.6;
        color: var(--light-text);
    }
    
    .dark-mode p, .dark-mode li {
        color: var(--dark-text);
    }
    
    /* Card/Container Styling */
    div[data-testid="stForm"] {
        background-color: var(--off-white);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        border: 1px solid var(--light-border);
        margin-bottom: 24px;
    }
    
    .dark-mode div[data-testid="stForm"] {
        background-color: var(--dark-mode-card);
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        border: 1px solid var(--dark-border);
    }
    
    /* Expander Styling */
    details {
        background-color: var(--off-white);
        border-radius: 8px;
        border: 1px solid var(--light-border);
        margin-bottom: 16px;
        overflow: hidden;
    }
    
    .dark-mode details {
        background-color: var(--dark-mode-card);
        border: 1px solid var(--dark-border);
    }
    
    details summary {
        padding: 16px;
        cursor: pointer;
        font-weight: 500;
    }
    
    details summary:hover {
        background-color: var(--light-gray);
    }
    
    .dark-mode details summary:hover {
        background-color: rgba(255,255,255,0.05);
    }
    
    /* Button Styling */
    .stButton button {
        background-color: var(--primary-color);
        color: white;
        font-weight: 500;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--off-white);
        border-right: 1px solid var(--light-border);
    }
    
    .dark-mode [data-testid="stSidebar"] {
        background-color: var(--dark-mode-card);
        border-right: 1px solid var(--dark-border);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 1.5rem;
    }
    
    /* Header Styling */
    .professional-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 15px rgba(93, 92, 222, 0.25);
    }
    
    .professional-header h1 {
        color: white;
        margin-bottom: 0.5rem;
        font-size: 2.4rem;
    }
    
    .professional-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* HIPAA Notice Styling */
    .hipaa-notice {
        background-color: var(--tertiary-color);
        border-left: 4px solid var(--primary-color);
        padding: 16px;
        margin: 20px 0;
        border-radius: 6px;
    }
    
    .dark-mode .hipaa-notice {
        background-color: rgba(93, 92, 222, 0.15);
    }
    
    /* Chat Styling */
    .chat-container {
        border-radius: 12px;
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border: 1px solid var(--light-border);
        background-color: var(--off-white);
    }
    
    .dark-mode .chat-container {
        border: 1px solid var(--dark-border);
        background-color: var(--dark-mode-card);
    }
    
    /* Chat Message Styling */
    [data-testid="stChatMessage"] {
        padding: 0.75rem 0;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
        background-color: var(--light-gray);
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
        background-color: var(--primary-color);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 10px 16px;
        background-color: var(--light-gray);
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color# Professional header
            st.markdown("""
            <h1>Professional Chat Consultation</h1>
            <div class="professional-separator" style="width: 150px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
            
            # Check if patient info is filled out
            patient_info = st.session_state['patient_contact_info']
            
            if not patient_info.first_name or not patient_info.last_name:
                # Warning with enhanced styling
                st.markdown("""
                <div style="background-color: rgba(255, 190, 85, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--warning-color);">
                    <h4 style="color: var(--warning-color); margin-top: 0;">Patient Information Required</h4>
                    <p style="margin-bottom: 15px;">Please complete the Patient Intake form before using the chat feature.</p>
                """, unsafe_allow_html=True)
                
                if st.button("Go to Patient Intake →", use_container_width=True):
                    page = "Patient Intake"
                    st.experimental_rerun()
                    
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                # Two-column layout for chat interface
                chat_col, sidebar_col = st.columns([3, 1])
                
                with chat_col:
                    # HIPAA notice for chat with enhanced styling
                    st.markdown("""
                    <div style="background-color: rgba(90, 160, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid var(--info-color);">
                        <h4 style="color: var(--info-color); margin-top: 0;">Secure Communication</h4>
                        <p style="margin-bottom: 0;">This chat is encrypted and complies with HIPAA regulations. While this platform provides general guidance, it is not a substitute for in-person medical care for urgent or emergency conditions.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced chat container
                    st.markdown("""
                    <div style="background-color: var(--off-white); border-radius: 10px; border: 1px solid var(--light-border); padding: 5px; margin-bottom: 20px;">
                    """, unsafe_allow_html=True)
                    
                    # Chat container
                    chat_container = st.container()
                    with chat_container:
                        for message in st.session_state['chat_history']:
                            display_chat_message(message)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Welcome message if chat is empty
                    if not st.session_state['chat_history']:
                        with st.chat_message("assistant", avatar="🩺"):
                            intro_message = f"Good day, {patient_info.first_name}. I am Dr. Jackson, {dr_jackson.credentials}, specializing in functional and integrative medicine. How may I be of assistance to you today?"
                            st.markdown(intro_message)
                            # Add welcome message to history
                            st.session_state['chat_history'].append(
                                ChatMessage(role="assistant", content=intro_message)
                            )
                    
                    # Chat input with professional styling
                    st.markdown("""
                    <div style="margin-bottom: 10px;">
                        <h4 style="font-size: 1rem; margin-bottom: 5px;">Your Message</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    user_input = st.chat_input("Type your medical question here...")
                    
                    if user_input:
                        # Add user message to history
                        st.session_state['chat_history'].append(
                            ChatMessage(role="user", content=user_input)
                        )
                        
                        # Display the new user message
                        with st.chat_message("user"):
                            st.markdown(user_input)
                        
                        # Generate and display Dr. Jackson's response
                        with st.chat_message("assistant", avatar="🩺"):
                            message_placeholder = st.empty()
                            
                            # Simulate typing with a delay
                            full_response = dr_jackson.get_chat_response(user_input)
                            
                            # Simulate typing effect
                            displayed_response = ""
                            for chunk in full_response.split():
                                displayed_response += chunk + " "
                                message_placeholder.markdown(displayed_response + "▌")
                                time.sleep(0.03)  # Faster typing
                            
                            message_placeholder.markdown(full_response)
                            st.caption(f"{datetime.datetime.now().strftime('%I:%M %p')}")
                        
                        # Add assistant response to history
                        st.session_state['chat_history'].append(
                            ChatMessage(role="assistant", content=full_response)
                        )
                        
                        # Enhanced follow-up options
                        st.markdown("""
                        <div style="margin-top: 20px;">
                            <h4 style="font-size: 1rem; margin-bottom: 15px;">Quick Follow-up Options</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("Request additional information", key="more_info_btn", use_container_width=True):
                                followup = "Can you provide additional information or resources about this topic?"
                                st.session_state['chat_history'].append(
                                    ChatMessage(role="user", content=followup)
                                )
                                st.experimental_rerun()
                        
                        with col2:
                            if st.button("Schedule consultation", key="schedule_btn", use_container_width=True):
                                followup = "I'd like to schedule a full consultation to discuss this in more detail."
                                st.session_state['chat_history'].append(
                                    ChatMessage(role="user", content=followup)
                                )
                                st.experimental_rerun()
                        
                        with col3:
                            if st.button("Ask about treatment options", key="treatment_btn", use_container_width=True):
                                followup = "What treatment approaches would you recommend for this condition?"
                                st.session_state['chat_history'].append(
                                    ChatMessage(role="user", content=followup)
                                )
                                st.experimental_rerun()
                
                with sidebar_col:
                    # Enhanced patient context
                    st.markdown("""
                    <div style="background-color: var(--off-white); padding: 15px; border-radius: 10px; border: 1px solid var(--light-border); margin-bottom: 20px;">
                        <h4 style="margin-top: 0; font-size: 1rem;">Patient Context</h4>
                        <div class="professional-separator" style="margin: 10px 0;"></div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Name:</strong> {patient_info.first_name} {patient_info.last_name}</p>
                        <p style="margin: 5px 0; font-size: 0.9rem;"><strong>DOB:</strong> {patient_info.date_of_birth}</p>
                    """, unsafe_allow_html=True)
                    
                    medical_info = st.session_state['patient_medical_info']
                    if medical_info.chronic_conditions:
                        conditions = ", ".join(medical_info.chronic_conditions[:2])
                        if len(medical_info.chronic_conditions) > 2:
                            conditions += "..."
                        st.markdown(f"""
                            <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Conditions:</strong> {conditions}</p>
                        """, unsafe_allow_html=True)
                        
                    if medical_info.current_medications:
                        medications = ", ".join(medical_info.current_medications[:2])
                        if len(medical_info.current_medications) > 2:
                            medications += "..."
                        st.markdown(f"""
                            <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Medications:</strong> {medications}</p>
                        """, unsafe_allow_html=True)
                        
                    st.markdown("""
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced chat controls
                    with st.expander("Chat Controls", expanded=False):
                        if st.button("Clear Chat History", use_container_width=True):
                            st.session_state['chat_history'] = []
                            st.success("Chat history has been cleared")
                            st.experimental_rerun()
                        
                        # AI model selection if API keys are configured
                        if any([st.session_state.get('anthropic_api_key'), 
                                st.session_state.get('openai_api_key')]):
                            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                            st.markdown("<h4 style='font-size: 1rem;'>AI Model Selection</h4>", unsafe_allow_html=True)
                            model = st.radio(
                                "Select AI model for consultation",
                                ["Claude (Anthropic)", "GPT-4 (OpenAI)", "Llama (Meta)"],
                                index=0
                            )
                            st.info(f"Currently using: {model}")
                    
                    # Enhanced health topics quick access
                    st.markdown("""
                    <div style="margin-top: 20px;">
                        <h4 style="font-size: 1rem; margin-bottom: 15px;">Common Health Topics</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    topics = [
                        ("Functional Medicine", "🔬"),
                        ("Nutritional Guidance", "🥗"),
                        ("Sleep Optimization", "💤"),
                        ("Stress Management", "🧘‍♀️"),
                        ("Hormone Balance", "⚖️"),
                        ("Gut Health", "🦠")
                    ]
                    
                    for topic, icon in topics:
                        topic_button = f"{icon} {topic}"
                        if st.button(topic_button, key=f"topic_{topic}", use_container_width=True):
                            query = f"I'd like to learn more about {topic.lower()}. What's your approach?"
                            st.session_state['chat_history'].append(
                                ChatMessage(role="user", content=query)
                            )
                            st.experimental_rerun()
                    
                    # Professional note
                    st.markdown("""
                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 15px; border-radius: 10px; margin-top: 25px;">
                        <p style="font-size: 0.85rem; margin: 0;">
                            <strong>Professional Note:</strong> This chat interface provides general medical guidance based on 
                            Dr. Jackson's professional approach. For personalized treatment plans, 
                            we recommend scheduling a comprehensive consultation.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Schedule consultation button
                    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                    if st.button("📅 Schedule Full Consultation", use_container_width=True):
                        page = "Consultation"
                        st.experimental_rerun()
        
        elif page == "Specialties":
            # Professional header
            st.markdown("""
            <h1>Areas of Specialization</h1>
            <div class="professional-separator" style="width: 120px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
            
            # Add tabs for better organization with enhanced styling
            specialty_tabs = st.tabs(["Primary Specialties", "Additional Focus Areas", "Treatment Approaches"])
            
            with specialty_tabs[0]:
                st.markdown("""
                <h3 style="margin-bottom: 20px;">Primary Clinical Specialties</h3>
                <p style="margin-bottom: 25px;">
                    Dr. Jackson's practice offers comprehensive care across the following primary specialties, 
                    with evidence-based approaches tailored to individual patient needs.
                </p>
                """, unsafe_allow_html=True)
                
                # Create a more visual representation of specialties
                for i, domain in enumerate(dr_jackson.primary_domains):
                    with st.expander(f"{i+1}. {domain}", expanded=i==0):
                        # Domain-specific content
                        if domain == "Psychiatric Care":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Our psychiatric care approach integrates conventional psychopharmacology with functional medicine principles. 
                                    We assess neurotransmitter pathways, inflammatory markers, and nutrient status alongside standard psychiatric evaluation.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Comprehensive neurochemical assessment</strong> - Evaluating multiple biochemical pathways</li>
                                        <li><strong>Targeted amino acid therapy</strong> - Precision supplementation for neurotransmitter support</li>
                                        <li><strong>Inflammatory pathway modulation</strong> - Addressing neuroinflammatory contributions</li>
                                        <li><strong>Neuroendocrine optimization</strong> - Balancing HPA axis function</li>
                                        <li><strong>Microbiome-brain axis support</strong> - Targeting gut-brain connection</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Clinical Approach</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our psychiatric protocols integrate conventional assessment with functional testing to identify root causes of mental health conditions.</p>
                                        <p>Treatment plans combine targeted nutritional interventions, lifestyle modifications, and when appropriate, conventional medications in a comprehensive approach.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Psychiatric+Care+Approach", use_column_width=True)
                            
                        elif domain == "Wellness Optimization":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Wellness optimization begins with comprehensive assessment of physiological function across multiple systems.
                                    Our approach establishes personalized baselines and identifies limiting factors in performance and wellbeing.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Metabolic efficiency enhancement</strong> - Optimizing cellular energy production pathways</li>
                                        <li><strong>Cellular energy production</strong> - Supporting mitochondrial function and ATP synthesis</li>
                                        <li><strong>Oxidative stress management</strong> - Balancing pro-oxidant and antioxidant mechanisms</li>
                                        <li><strong>Circadian rhythm optimization</strong> - Restoring natural biological timing systems</li>
                                        <li><strong>Recovery protocol development</strong> - Structured approaches to physiological restoration</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Performance Enhancement</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our wellness optimization protocols identify and address the specific factors limiting your physiological performance.</p>
                                        <p>Rather than generic wellness approaches, we target biochemical, structural, and regulatory elements unique to your health profile.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Wellness+Optimization+Approach", use_column_width=True)
                            
                        elif domain == "Anti-aging Medicine":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Our anti-aging approach focuses on measurable biomarkers of cellular aging rather than cosmetic concerns alone.
                                    We target key mechanisms of cellular senescence and tissue degeneration through evidence-based interventions.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Telomere dynamics assessment</strong> - Evaluating cellular replicative potential</li>
                                        <li><strong>Advanced glycation endpoint management</strong> - Reducing cross-linked protein accumulation</li>
                                        <li><strong>Mitochondrial function optimization</strong> - Enhancing cellular energy production</li>
                                        <li><strong>Senolytic protocol implementation</strong> - Targeted approach to senescent cell burden</li>
                                        <li><strong>Epigenetic modification strategies</strong> - Optimizing gene expression patterns</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Biological Age Management</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our anti-aging protocols focus on measurable biomarkers of aging rather than chronological age.</p>
                                        <p>We implement evidence-based approaches to reduce biological age markers and optimize physiological function.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Anti-aging+Medicine+Approach", use_column_width=True)
                            
                        elif domain == "Functional Medicine":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Functional medicine addresses root causes rather than symptoms alone. Our approach investigates
                                    underlying mechanisms of dysfunction through comprehensive laboratory assessment and detailed history.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Systems biology framework</strong> - Understanding interconnected physiological networks</li>
                                        <li><strong>Biochemical individuality assessment</strong> - Personalized physiological evaluation</li>
                                        <li><strong>Environmental exposure evaluation</strong> - Identifying toxic burden and triggers</li>
                                        <li><strong>Genetic predisposition analysis</strong> - Understanding susceptibility patterns</li>
                                        <li><strong>Root cause identification protocols</strong> - Systematic approach to underlying factors</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Root Cause Approach</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our functional medicine model identifies and addresses the underlying mechanisms of disease rather than merely suppressing symptoms.</p>
                                        <p>We utilize advanced testing to uncover biochemical imbalances, nutritional deficiencies, and physiological dysfunction.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Functional+Medicine+Approach", use_column_width=True)
                            
                        elif domain == "Integrative Health":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Integrative health combines evidence-based conventional medicine with complementary approaches that
                                    have substantial research support. Our protocols select the most appropriate interventions from multiple
                                    therapeutic systems.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Evidence-based complementary medicine</strong> - Utilizing validated non-conventional approaches</li>
                                        <li><strong>Mind-body intervention protocols</strong> - Structured approaches to psychophysiological regulation</li>
                                        <li><strong>Traditional healing system integration</strong> - Incorporating validated traditional approaches</li>
                                        <li><strong>Botanical medicine application</strong> - Evidence-supported phytotherapeutic interventions</li>
                                        <li><strong>Manual therapy coordination</strong> - Appropriate referral and integration of bodywork</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Multi-System Approach</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our integrative protocols combine the best of conventional medicine with evidence-supported complementary approaches.</p>
                                        <p>We maintain rigorous standards for inclusion of therapeutic modalities based on both research evidence and clinical utility.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Integrative+Health+Approach", use_column_width=True)
                            
                        elif domain == "Preventive Care":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Preventive care focuses on identifying early warning signs of dysfunction before disease manifestation.
                                    Our approach utilizes advanced screening protocols and risk assessment algorithms to detect subclinical imbalances.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Predictive biomarker monitoring</strong> - Tracking early indicators of physiological shift</li>
                                        <li><strong>Precision risk assessment</strong> - Personalized evaluation of disease susceptibility</li>
                                        <li><strong>Subclinical dysfunction detection</strong> - Identifying imbalances before symptom development</li>
                                        <li><strong>Targeted prevention protocols</strong> - Specific interventions based on risk profile</li>
                                        <li><strong>Resilience enhancement strategies</strong> - Building physiological and psychological reserve</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Proactive Health Management</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our preventive approach identifies physiological imbalances before they progress to diagnosable disease states.</p>
                                        <p>We implement targeted interventions based on advanced biomarker patterns and comprehensive risk assessment.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Preventive+Care+Approach", use_column_width=True)
            
            with specialty_tabs[1]:
                st.markdown("""
                <h3 style="margin-bottom: 25px;">Additional Clinical Focus Areas</h3>
                <p style="margin-bottom: 30px;">
                    These specialized areas complement our primary approaches, providing comprehensive
                    support for complex health concerns and specific physiological systems.
                </p>
                """, unsafe_allow_html=True)
                
                # Create a grid layout for secondary domains with enhanced styling
                col1, col2 = st.columns(2)
                
                # First column
                with col1:
                    for domain in dr_jackson.secondary_domains[:3]:
                        with st.container():
                            st.markdown(f"""
                            <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid var(--light-border);">
                                <h3 style="margin-top: 0;">{domain}</h3>
                                <div class="professional-separator"></div>
                            """, unsafe_allow_html=True)
                            
                            if domain == "Nutritional Medicine":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Nutritional medicine utilizes targeted dietary interventions and therapeutic supplementation
                                    based on individual biochemical assessment. Our protocols address specific nutritional imbalances
                                    identified through comprehensive testing.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>Targeted micronutrient repletion</li>
                                        <li>Therapeutic elimination protocols</li>
                                        <li>Metabolic optimization strategies</li>
                                        <li>Personalized dietary planning</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            elif domain == "Stress Management":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Our approach to stress management includes physiological assessment of HPA axis function
                                    alongside evidence-based cognitive and somatic interventions to restore stress response regulation.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>HPA axis regulation protocols</li>
                                        <li>Neuroendocrine rebalancing</li>
                                        <li>Autonomic nervous system restoration</li>
                                        <li>Cognitive-behavioral interventions</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            elif domain == "Hormonal Balance":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Hormonal balance focuses on the complex interrelationships between endocrine systems.
                                    Our protocols assess steroid hormone cascades, thyroid function, and insulin dynamics
                                    to restore optimal regulatory patterns.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>Comprehensive hormone assessment</li>
                                        <li>Thyroid optimization protocols</li>
                                        <li>Adrenal function restoration</li>
                                        <li>Metabolic hormone regulation</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("""
                            </div>
                            """, unsafe_allow_html=True)
                
                # Second column
                with col2:
                    for domain in dr_jackson.secondary_domains[3:]:
                        with st.container():
                            st.markdown(f"""
                            <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid var(--light-border);">
                                <h3 style="margin-top: 0;">{domain}</h3>
                                <div class="professional-separator"></div>
                            """, unsafe_allow_html                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 2 of 3: Medical Information</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced medical privacy notice
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                <h4 style="color: var(--info-color); margin-top: 0;">Medical Information Privacy</h4>
                <p>Your medical history is protected under HIPAA guidelines and will only be used to provide appropriate clinical care.</p>
                <p style="margin-bottom: 0; font-size: 0.9rem;">This information helps us develop a comprehensive understanding of your health status and will not be shared without your explicit consent.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get the current medical info from session state
            medical_info = st.session_state['patient_medical_info']
            
            # Enhanced form with better visual organization
            with st.form("medical_history_form"):
                # Primary care physician
                st.markdown("<h3 style='margin-top: 0; margin-bottom: 20px;'>Healthcare Provider Information</h3>", unsafe_allow_html=True)
                
                primary_care = st.text_input("Primary Care Physician", 
                                          value=medical_info.primary_care_physician,
                                          placeholder="Name of your current primary care provider")
                
                # Medication information with enhanced styling
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Current Medications</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please list all medications, supplements, and vitamins you are currently taking, including dosage if known.
                </p>
                """, unsafe_allow_html=True)
                
                medications_text = st.text_area(
                    "One medication per line (include dosage if known)", 
                    value="\n".join(medical_info.current_medications) if medical_info.current_medications else "",
                    height=120,
                    placeholder="Example:\nMetformin 500mg twice daily\nVitamin D3 2000 IU daily\nOmega-3 Fish Oil 1000mg daily"
                )
                
                # Allergies with better organization
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Allergies</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    List all known allergies including medications, foods, and environmental triggers. Include reaction type if known.
                </p>
                """, unsafe_allow_html=True)
                
                allergies_text = st.text_area(
                    "Please list all allergies (medications, foods, environmental)", 
                    value="\n".join(medical_info.allergies) if medical_info.allergies else "",
                    height=100,
                    placeholder="Example:\nPenicillin - rash and hives\nPeanuts - anaphylaxis\nPollen - seasonal rhinitis"
                )
                
                # Medical conditions with better visual organization
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Chronic Medical Conditions</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please list all diagnosed medical conditions including approximate date of diagnosis.
                </p>
                """, unsafe_allow_html=True)
                
                conditions_text = st.text_area(
                    "Please list all diagnosed medical conditions", 
                    value="\n".join(medical_info.chronic_conditions) if medical_info.chronic_conditions else "",
                    height=100,
                    placeholder="Example:\nHypertension - diagnosed 2018\nType 2 Diabetes - diagnosed 2020\nMigraine - diagnosed 2015"
                )
                
                # Surgical history with improved styling
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Surgical History</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please list all previous surgeries with approximate dates.
                </p>
                """, unsafe_allow_html=True)
                
                surgeries_text = st.text_area(
                    "Please list all previous surgeries with approximate dates", 
                    value="\n".join(medical_info.past_surgeries) if medical_info.past_surgeries else "",
                    height=100,
                    placeholder="Example:\nAppendectomy - 2010\nKnee arthroscopy - 2019\nTonsillectomy - childhood"
                )
                
                # Family medical history with better visual organization
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Family Medical History</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please indicate any significant family medical history, specifying the relationship to you.
                </p>
                """, unsafe_allow_html=True)
                
                # Use a more structured approach for family history
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
                            value=value,
                            placeholder=f"e.g., Father, Mother, Sibling"
                        )
                
                # Lifestyle section (added)
                st.markdown("""
                <h3 style='margin-top: 30px; margin-bottom: 15px;'>Lifestyle Information</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    This information helps us develop a more comprehensive understanding of your health status.
                </p>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.selectbox("Exercise Frequency", 
                                 options=["Select an option", "None", "Occasional (1-2 times/week)", 
                                          "Regular (3-4 times/week)", "Frequent (5+ times/week)"],
                                 index=0)
                    st.selectbox("Stress Level", 
                                 options=["Select an option", "Low", "Moderate", "High", "Very High"],
                                 index=0)
                with col2:
                    st.selectbox("Sleep Quality", 
                                 options=["Select an option", "Poor", "Fair", "Good", "Excellent"],
                                 index=0)
                    st.selectbox("Diet Quality", 
                                 options=["Select an option", "Poor", "Fair", "Good", "Excellent"],
                                 index=0)
                
                # Health goals section (added)
                st.markdown("""
                <h3 style='margin-top: 30px; margin-bottom: 15px;'>Health Goals</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please share your main health goals and what you hope to achieve through our care.
                </p>
                """, unsafe_allow_html=True)
                
                health_goals = st.text_area(
                    "Primary health objectives",
                    height=100,
                    placeholder="Example:\nImprove energy levels\nReduce chronic pain\nOptimize sleep quality\nAddress specific health concerns"
                )
                
                # Consent checkboxes with better styling
                st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
                history_consent = st.checkbox(
                    "I confirm that the information provided is accurate and complete to the best of my knowledge", 
                    value=True
                )
                sharing_consent = st.checkbox(
                    "I consent to the appropriate sharing of this information with healthcare providers involved in my care",
                    value=True
                )
                
                # Submit button with professional styling
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Save & Continue", use_container_width=True)
                
                if submitted:
                    # Process and save the data
                    if not (history_consent and sharing_consent):
                        st.error("Please confirm both consent statements to proceed.")
                    else:
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
                        
                        # Success message with professional styling
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Medical History Saved</h4>
                            <p style="margin-bottom: 0;">Your medical history has been securely stored. Thank you for providing this comprehensive information, which will help us deliver personalized care.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Offer navigation to consultation with better styling
                        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                        if st.button("Proceed to Consultation →", use_container_width=True):
                            page = "Consultation"
                            st.experimental_rerun()
            
            # Professional note at bottom
            st.markdown("""
            <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Why We Collect This Information</h4>
                <p style="font-size: 0.9rem; margin-bottom: 0;">
                    Comprehensive medical history allows us to develop personalized care plans based on your unique health profile.
                    This information helps identify patterns, assess risk factors, and determine optimal treatment approaches
                    following evidence-based functional medicine principles.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Consultation":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Professional Consultation</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 3 of 3: Consultation Request</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Check if patient info is filled out
            patient_info = st.session_state['patient_contact_info']
            medical_info = st.session_state['patient_medical_info']
            
            if not patient_info.first_name or not patient_info.last_name:
                # Warning with enhanced styling
                st.markdown("""
                <div style="background-color: rgba(255, 190, 85, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--warning-color);">
                    <h4 style="color: var(--warning-color); margin-top: 0;">Patient Information Required</h4>
                    <p style="margin-bottom: 15px;">Please complete the Patient Intake form before proceeding to consultation.</p>
                """, unsafe_allow_html=True)
                
                if st.button("Go to Patient Intake →", use_container_width=True):
                    page = "Patient Intake"
                    st.experimental_rerun()
                    
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                # Patient information summary with professional styling
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; border: 1px solid var(--light-border); margin-bottom: 30px;">
                    <h3 style="margin-top: 0;">Patient Information Summary</h3>
                    <div class="professional-separator"></div>
                    
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 15px;">
                """, unsafe_allow_html=True)
                
                # Patient details
                st.markdown(f"""
                        <div style="flex: 1; min-width: 250px;">
                            <h4 style="margin-top: 0; font-size: 1rem;">Personal Information</h4>
                            <p style="margin: 5px 0;"><strong>Name:</strong> {patient_info.first_name} {patient_info.last_name}</p>
                            <p style="margin: 5px 0;"><strong>Date of Birth:</strong> {patient_info.date_of_birth}</p>
                            <p style="margin: 5px 0;"><strong>Email:</strong> {patient_info.email}</p>
                            <p style="margin: 5px 0;"><strong>Phone:</strong> {patient_info.phone}</p>
                        </div>
                """, unsafe_allow_html=True)
                
                # Medical summary
                medical_conditions = ", ".join(medical_info.chronic_conditions[:3]) if medical_info.chronic_conditions else "None reported"
                if len(medical_info.chronic_conditions) > 3:
                    medical_conditions += " (and others)"
                    
                medications = ", ".join(medical_info.current_medications[:3]) if medical_info.current_medications else "None reported"
                if len(medical_info.current_medications) > 3:
                    medications += " (and others)"
                    
                allergies = ", ".join(medical_info.allergies[:3]) if medical_info.allergies else "None reported"
                if len(medical_info.allergies) > 3:
                    allergies += " (and others)"
                
                st.markdown(f"""
                        <div style="flex: 1; min-width: 250px;">
                            <h4 style="margin-top: 0; font-size: 1rem;">Medical Summary</h4>
                            <p style="margin: 5px 0;"><strong>Conditions:</strong> {medical_conditions}</p>
                            <p style="margin: 5px 0;"><strong>Medications:</strong> {medications}</p>
                            <p style="margin: 5px 0;"><strong>Allergies:</strong> {allergies}</p>
                            <p style="margin: 5px 0;"><strong>PCP:</strong> {medical_info.primary_care_physician or "Not provided"}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # HIPAA notice with enhanced styling
                st.markdown("""
                <div style="background-color: rgba(90, 160, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                    <h4 style="color: var(--info-color); margin-top: 0;">Consultation Privacy</h4>
                    <p style="margin-bottom: 0;">This consultation is protected under HIPAA guidelines. Information shared during this session is confidential and will be securely stored in your electronic medical record.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced consultation form
                with st.form("consultation_form"):
                    st.markdown("""
                    <h3 style="margin-top: 0; margin-bottom: 20px;">Consultation Request</h3>
                    """, unsafe_allow_html=True)
                    
                    # Primary reason with better styling
                    st.markdown("""
                    <h4 style="margin-bottom: 15px;">Primary Health Concern</h4>
                    <p style="margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);">
                        Please describe your current health concerns in detail. Include symptom duration, severity, and any patterns you've noticed.
                    </p>
                    """, unsafe_allow_html=True)
                    
                    primary_concern = st.text_area(
                        "Health concern description",
                        height=150,
                        placeholder="Please provide a detailed description of your main health concerns...",
                        help="Include symptom duration, severity, and any patterns you've noticed"
                    )
                    
                    # Specialty selection with better organization
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Clinical Focus Area</h4>
                    <p style="margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);">
                        Select the specialty area most relevant to your health concerns.
                    </p>
                    """, unsafe_allow_html=True)
                    
                    specialty_area = st.selectbox(
                        "Select the most relevant specialty area", 
                        options=dr_jackson.primary_domains + dr_jackson.secondary_domains
                    )
                    
                    # Symptom details with better visual organization
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Symptom Details</h4>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        symptom_onset = st.date_input(
                            "When did you first notice these symptoms?",
                            value=datetime.datetime.now().date() - datetime.timedelta(days=30),
                            help="Select the approximate date when symptoms first appeared"
                        )
                    with col2:
                        severity = st.select_slider(
                            "Rate the severity of your symptoms",
                            options=["Mild", "Moderate", "Significant", "Severe", "Extreme"],
                            help="Indicate the overall intensity of your symptoms"
                        )
                    
                    # Additional context with better layout
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Additional Context</h4>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        prior_treatments = st.text_area(
                            "Prior treatments or approaches tried",
                            height=120,
                            placeholder="List any treatments, medications, or approaches you've already attempted..."
                        )
                    with col2:
                        triggers = st.text_area(
                            "Known triggers or patterns",
                            height=120,
                            placeholder="Describe any factors that worsen or improve your symptoms..."
                        )
                    
                    # Goals with better styling
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Treatment Goals</h4>
                    <p style="margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);">
                        What outcomes are you hoping to achieve through this consultation?
                    </p>
                    """, unsafe_allow_html=True)
                    
                    goals = st.text_area(
                        "Desired outcomes",
                        height=120,
                        placeholder="Describe your health goals and expectations from this consultation..."
                    )
                    
                    # Appointment preference (added)
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Appointment Preference</h4>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        appointment_type = st.radio(
                            "Preferred consultation type",
                            options=["Virtual (Telehealth)", "In-person Office Visit"],
                            index=0
                        )
                    with col2:
                        urgency = st.select_slider(
                            "Consultation urgency",
                            options=["Standard (within 2 weeks)", "Priority (within 1 week)", "Urgent (within 48 hours)"],
                            value="Standard (within 2 weeks)"
                        )
                    
                    # Enhanced consent checkbox
                    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
                    consultation_consent = st.checkbox(
                        "I understand that this consultation request will be reviewed by Dr. Jackson, and follow-up may be required before treatment recommendations are provided",
                        value=True
                    )
                    
                    # Submit button with better styling
                    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                    submitted = st.form_submit_button("Submit Consultation Request", use_container_width=True)
                
                # Form handling logic
                if submitted:
                    if not primary_concern:
                        st.error("Please describe your health concerns before submitting.")
                    elif not consultation_consent:
                        st.error("Please confirm your understanding of the consultation process.")
                    else:
                        # Success message with professional styling
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Consultation Request Submitted</h4>
                            <p style="margin-bottom: 10px;">Your request has been successfully received and will be reviewed by Dr. Jackson.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display a professional response using the persona
                        st.markdown("""
                        <div style="background-color: var(--off-white); padding: 25px; border-radius: 10px; border: 1px solid var(--light-border); margin-top: 30px;">
                            <h3 style="margin-top: 0;">Initial Assessment</h3>
                            <div class="professional-separator"></div>
                        """, unsafe_allow_html=True)
                        
                        # Determine appropriate recommendations based on specialty area
                        if specialty_area in dr_jackson.primary_domains[:3]:  # First 3 primary domains
                            recommendations = [
                                "Schedule a comprehensive initial evaluation",
                                "Complete the detailed symptom assessment questionnaire",
                                "Prepare any prior lab work or diagnostic studies for review",
                                "Consider keeping a symptom journal for the next 7 days"
                            ]
                        else:
                            recommendations = [
                                "Schedule an initial consultation",
                                "Gather relevant medical records and previous test results",
                                "Complete preliminary health assessment questionnaires",
                                "Prepare a list of specific questions for your consultation"
                            ]
                        
                        # Use the persona to format the response with better styling
                        assessment = f"Based on your initial information regarding {specialty_area.lower()} concerns of {severity.lower()} severity, a professional evaluation is indicated. Your symptoms beginning approximately {(datetime.datetime.now().date() - symptom_onset).days} days ago warrant a thorough assessment."
                        
                        st.markdown(f"""
                            <div style="margin-bottom: 20px;">
                                <h4 style="margin-bottom: 10px; font-size: 1.1rem;">Clinical Overview</h4>
                                <p style="margin-bottom: 5px;"><strong>Presenting Concerns:</strong> {specialty_area} issues with {severity.lower()} symptoms</p>
                                <p style="margin-bottom: 5px;"><strong>Duration:</strong> Approximately {(datetime.datetime.now().date() - symptom_onset).days} days</p>
                                <p style="margin-bottom: 5px;"><strong>Requested Format:</strong> {appointment_type}</p>
                                <p><strong>Urgency Level:</strong> {urgency}</p>
                            </div>
                            
                            <div style="margin-bottom: 20px;">
                                <h4 style="margin-bottom: 10px; font-size: 1.1rem;">Professional Assessment</h4>
                                <p>{assessment}</p>
                            </div>
                            
                            <div>
                                <h4 style="margin-bottom: 10px; font-size: 1.1rem;">Recommendations</h4>
                                <ul>
                        """, unsafe_allow_html=True)
                        
                        for rec in recommendations:
                            st.markdown(f"""
                                <li style="margin-bottom: 8px;">{rec}</li>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("""
                                </ul>
                            </div>
                            
                            <p style="margin-top: 20px; font-style: italic;">Please confirm your understanding of these recommendations and your intent to proceed with the next steps.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Next steps with professional styling
                        st.markdown("""
                        <div style="margin-top: 30px;">
                            <h3>Next Steps</h3>
                            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-top: 15px;">
                                <p style="margin: 0;">You will receive a detailed follow-up within 24-48 hours with additional instructions and appointment scheduling options.</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # AI-assisted note section with professional styling
                        if st.session_state.get('anthropic_api_key') or st.session_state.get('openai_api_key'):
                            st.markdown("""
                            <div style="margin-top: 40px;">
                                <h3>AI-Assisted Clinical Notes</h3>
                                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; border: 1px solid var(--light-border); margin-top: 15px;">
                            """, unsafe_allow_html=True)
                            
                            with st.spinner("Generating preliminary clinical notes..."):
                                # This would normally call an LLM API
                                time.sleep(2)  # Simulate processing time
                                
                                st.markdown("""
                                    <h4 style="margin-top: 0; color: var(--primary-color);">PRELIMINARY ASSESSMENT NOTE</h4>
                                    <p style="margin-bottom: 15px;">
                                        Patient presents with concerns related to the selected specialty area. 
                                        Initial impression suggests further evaluation is warranted to establish 
                                        a differential diagnosis and treatment approach. Patient goals and symptom 
                                        presentation will be incorporated into the comprehensive care plan.
                                    </p>
                                    <p style="font-style: italic; font-size: 0.9rem; margin-bottom: 0; color: var(--dark-gray);">
                                        This preliminary note was generated with AI assistance and will be 
                                        reviewed by Dr. Jackson prior to formal documentation.
                                    </p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Additional guidance at bottom of page
                st.markdown("""
                <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0;">What to Expect</h4>
                    <p style="font-size: 0.9rem; margin-bottom: 0;">
                        After submitting your consultation request, our clinical team will review your information and 
                        reach out to schedule your appointment. For urgent medical concerns requiring immediate attention, 
                        please contact your primary care provider or visit the nearest emergency department.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        elif page == "Chat with Dr. Jackson":
            # Professional header
            st.markdown("""
            <h1>Professional Chat Consultation</h1>
            <div class="professional-separator" style="width: 150px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
                
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--tertiary-color);
        font-weight: 500;
    }
    
    /* Alert/Notice Styling */
    .info-box {
        background-color: rgba(90, 160, 255, 0.1);
        border-left: 4px solid var(--info-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .success-box {
        background-color: rgba(61, 201, 161, 0.1);
        border-left: 4px solid var(--success-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .warning-box {
        background-color: rgba(255, 190, 85, 0.1);
        border-left: 4px solid var(--warning-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .error-box {
        background-color: rgba(255, 90, 90, 0.1);
        border-left: 4px solid var(--error-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    /* Progress Bar Styling */
    [data-testid="stProgressBar"] > div {
        background-color: var(--primary-color);
        height: 8px;
        border-radius: 4px;
    }
    
    [data-testid="stProgressBar"] > div:nth-child(1) {
        background-color: var(--light-gray);
    }
    
    /* Section Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            rgba(0,0,0,0), 
            var(--medium-gray), 
            rgba(0,0,0,0));
    }
    
    .dark-mode hr {
        background: linear-gradient(90deg, 
            rgba(0,0,0,0), 
            var(--dark-border), 
            rgba(0,0,0,0));
    }
    
    /* Info Cards Grid */
    .info-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 16px;
        margin: 20px 0;
    }
    
    .info-card {
        background-color: var(--off-white);
        border-radius: 8px;
        border: 1px solid var(--light-border);
        padding: 20px;
        transition: all 0.2s ease;
    }
    
    .info-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    .dark-mode .info-card {
        background-color: var(--dark-mode-card);
        border: 1px solid var(--dark-border);
    }
    
    .dark-mode .info-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Custom Utility Classes */
    .text-center {
        text-align: center;
    }
    
    .mb-0 {
        margin-bottom: 0 !important;
    }
    
    .mt-0 {
        margin-top: 0 !important;
    }
    
    .professional-separator {
        height: 5px;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        margin: 12px 0;
        border-radius: 3px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional App Header with Logo
    st.markdown(f"""
    <div class="professional-header">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h1>Dr. Jackson, {dr_jackson.credentials}</h1>
                <p>{dr_jackson.practice_name}</p>
            </div>
            <div style="text-align: right;">
                <p style="font-size: 0.9rem; opacity: 0.8;">Advancing Integrative Medicine</p>
                <p style="font-size: 0.8rem; opacity: 0.7;">Established 2015</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Professionally designed sidebar
    with st.sidebar:
        # Add a subtle medical/professional icon or logo
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); 
                       width: 60px; height: 60px; border-radius: 50%; display: inline-flex; 
                       align-items: center; justify-content: center; margin-bottom: 10px;">
                <span style="color: white; font-size: 30px;">🩺</span>
            </div>
            <p style="font-weight: 600; margin: 0; font-size: 16px;">Dr. Jackson Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='margin-top: 0;'>Navigation</h3>", unsafe_allow_html=True)
        
        # Enhanced navigation with section grouping
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; color: var(--dark-gray);'>Patient Portal</p>", unsafe_allow_html=True)
        patient_page = st.radio("", [
            "Home", 
            "Patient Intake", 
            "Medical History",
            "Consultation"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>Communication</p>", unsafe_allow_html=True)
        communication_page = st.radio("", [
            "Chat with Dr. Jackson"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>Information</p>", unsafe_allow_html=True)
        info_page = st.radio("", [
            "Specialties", 
            "Approach",
            "Resources"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>System</p>", unsafe_allow_html=True)
        system_page = st.radio("", [
            "Settings"
        ], label_visibility="collapsed")
        
        # Determine selected page from all radio groups
        if patient_page != "Home":
            page = patient_page
        elif communication_page != "Chat with Dr. Jackson":
            page = "Chat with Dr. Jackson"
        elif info_page != "Specialties":
            page = info_page
        elif system_page != "Settings":
            page = system_page
        else:
            page = "Home"
        
        # Theme selection with better design
        st.markdown("---")
        st.markdown("<h4 style='margin-bottom: 10px;'>Appearance</h4>", unsafe_allow_html=True)
        theme_cols = st.columns([1, 3])
        with theme_cols[0]:
            st.markdown("🎨")
        with theme_cols[1]:
            theme = st.selectbox("", ["Light", "Dark"], label_visibility="collapsed")
        
        if theme == "Dark":
            st.markdown("""
            <script>
                document.body.classList.add('dark-mode');
            </script>
            """, unsafe_allow_html=True)
        
        # Professional info section
        st.markdown("---")
        st.markdown("<h4 style='margin-bottom: 10px;'>About Dr. Jackson</h4>", unsafe_allow_html=True)
        
        # More professional specialty display
        domains = ", ".join(dr_jackson.primary_domains[:3])
        st.markdown(f"""
        <div style="background-color: var(--off-white); padding: 12px; border-radius: 8px; border: 1px solid var(--light-border); margin-bottom: 15px;">
            <p style="font-weight: 500; margin-bottom: 5px;">Specializing in:</p>
            <p style="color: var(--primary-color); font-weight: 600; margin: 0;">{domains}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Current date - maintaining professional approach
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background-color: var(--primary-color); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                <span style="color: white;">📅</span>
            </div>
            <div>
                <p style="font-size: 0.85rem; margin: 0; opacity: 0.7;">Today's Date</p>
                <p style="font-weight: 500; margin: 0;">{current_date}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show logged in status if patient info exists
        patient_info = st.session_state['patient_contact_info']
        if patient_info.first_name and patient_info.last_name:
            st.markdown(f"""
            <div style="background-color: rgba(61, 201, 161, 0.1); border-left: 4px solid var(--success-color); padding: 12px; border-radius: 6px;">
                <p style="font-weight: 500; margin: 0;">Logged in as:</p>
                <p style="margin: 5px 0 0 0;">{patient_info.first_name} {patient_info.last_name}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Container for main content with professional layout
    main_container = st.container()
    with main_container:
        # Main content area based on page selection
        if page == "Home":
            st.header("Welcome to Dr. Jackson's Professional Consultation")
            
            # Enhanced HIPAA Notice with more professional design
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; 
                       border-left: 5px solid var(--info-color); margin-bottom: 30px;">
                <h4 style="color: var(--info-color); margin-top: 0;">HIPAA Compliance Notice</h4>
                <p style="margin-bottom: 10px;">This application complies with the Health Insurance Portability and Accountability Act (HIPAA) of 1996:</p>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                    <li style="margin-bottom: 5px;">All patient data is encrypted in transit and at rest</li>
                    <li style="margin-bottom: 5px;">Access controls restrict unauthorized viewing of protected health information (PHI)</li>
                    <li style="margin-bottom: 5px;">Audit logs track all data access and modifications</li>
                    <li style="margin-bottom: 5px;">Data retention policies comply with medical record requirements</li>
                    <li style="margin-bottom: 5px;">Regular security assessments are conducted to ensure compliance</li>
                </ul>
                <p style="margin-top: 10px; margin-bottom: 0; font-weight: 500;"><span style="color: var(--info-color);">Privacy Officer Contact:</span> privacy@optimumwellness.org</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Featured specialties in cards layout
            st.markdown("### Our Clinical Specialties")
            st.markdown("""
            <p style="margin-bottom: 25px;">Dr. Jackson's practice provides comprehensive medical consultation with expertise in the following areas:</p>
            """, unsafe_allow_html=True)
            
            # Create a grid layout with cards for specialties
            st.markdown("""
            <div class="info-card-grid">
            """, unsafe_allow_html=True)
            
            for domain in dr_jackson.primary_domains:
                icon = "🧠" if domain == "Psychiatric Care" else "✨" if domain == "Wellness Optimization" else "⏱️" if domain == "Anti-aging Medicine" else "🔬" if domain == "Functional Medicine" else "🌿" if domain == "Integrative Health" else "🛡️"
                
                st.markdown(f"""
                <div class="info-card">
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                            <span style="font-size: 20px;">{icon}</span>
                        </div>
                        <h4 style="margin: 0; color: var(--primary-color);">{domain}</h4>
                    </div>
                    <div class="professional-separator"></div>
                    <p style="margin-top: 10px; font-size: 0.9rem;">Comprehensive, evidence-based approach to {domain.lower()} through integrated assessment and personalized protocols.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Professional approach section with better design
            st.markdown("### Professional Approach")
            
            # Two-column layout for approach and values
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 12px; border: 1px solid var(--light-border); height: 100%;">
                    <h4 style="margin-top: 0;">Clinical Methodology</h4>
                    <div class="professional-separator"></div>
                    <p>Dr. Jackson's practice is built on a hierarchical approach to medical knowledge and evidence:</p>
                    <ul>
                        <li><strong>Evidence-based research</strong> forms the foundation of all clinical decisions</li>
                        <li><strong>Clinical guidelines</strong> provide standardized frameworks for treatment protocols</li>
                        <li><strong>Professional experience</strong> guides the application of research to individual cases</li>
                        <li><strong>Holistic assessment</strong> ensures comprehensive evaluation of all contributing factors</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 12px; border: 1px solid var(--light-border); height: 100%;">
                    <h4 style="margin-top: 0;">Core Values</h4>
                    <div class="professional-separator"></div>
                    <ul>
                """, unsafe_allow_html=True)
                
                for i, value in enumerate(dr_jackson.core_values[:4]):
                    st.markdown(f"""
                    <li style="margin-bottom: 10px;">
                        <strong style="color: var(--primary-color);">{value}:</strong> 
                        Ensuring the highest standards of care through rigorous application of professional principles
                    </li>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Call to action section with enhanced design
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Begin Your Care Journey</h3>
            <div style="background: linear-gradient(135deg, rgba(93, 92, 222, 0.1) 0%, rgba(93, 92, 222, 0.05) 100%); 
                 padding: 30px; border-radius: 12px; margin-bottom: 30px; border: 1px solid rgba(93, 92, 222, 0.2);">
                <p style="font-size: 1.1rem; margin-bottom: 20px;">
                    To begin the consultation process, please complete the Patient Intake forms first. This will help us provide
                    the most appropriate clinical guidance tailored to your specific health needs.
                </p>
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("📋 Go to Patient Intake", key="home_intake_btn"):
                page = "Patient Intake"
                st.experimental_rerun()
                
            st.markdown("""
                    </div>
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("🔍 Learn About Specialties", key="home_specialties_btn"):
                page = "Specialties"
                st.experimental_rerun()
                
            st.markdown("""
                    </div>
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("💬 Chat with Dr. Jackson", key="home_chat_btn"):
                page = "Chat with Dr. Jackson"
                st.experimental_rerun()
            
            st.markdown("""
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Testimonials or professional credentials section
            st.markdown("""
            <div style="background-color: var(--off-white); padding: 25px; border-radius: 12px; border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Professional Credentials</h4>
                <div class="professional-separator"></div>
                <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 15px;">
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">🎓</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Education</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Doctorate in Nursing Practice</p>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">📜</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Certification</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Family Nurse Practitioner-Certified</p>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">🔬</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Specialization</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Certified Functional Medicine Practitioner</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Patient Intake":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Patient Intake Form</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 1 of 3: Contact Information</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced data privacy notice
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                <h4 style="color: var(--info-color); margin-top: 0;">Data Privacy Notice</h4>
                <p>All information submitted is encrypted and protected in accordance with HIPAA regulations.
                Your privacy is our priority. Information is only accessible to authorized medical personnel.</p>
                <p style="margin-bottom: 0; font-size: 0.9rem;"><strong>Security Measures:</strong> End-to-end encryption, secure database storage, access control mechanisms</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get the current patient info from session state
            patient_info = st.session_state['patient_contact_info']
            
            # Create the form with enhanced styling
            with st.form("patient_contact_form"):
                st.markdown("""
                <h3 style="margin-top: 0; margin-bottom: 20px;">Personal Information</h3>
                """, unsafe_allow_html=True)
                
                # Name information with professional layout
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name*", value=patient_info.first_name,
                                            placeholder="Enter your legal first name")
                with col2:
                    last_name = st.text_input("Last Name*", value=patient_info.last_name,
                                          placeholder="Enter your legal last name")
                
                # Contact information with more structured layout
                st.markdown("<h4 style='margin-top: 25px; margin-bottom: 15px;'>Contact Details</h4>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2,2,1])
                with col1:
                    email = st.text_input("Email Address*", value=patient_info.email,
                                        placeholder="Your primary email address")
                with col2:
                    phone = st.text_input("Phone Number*", value=patient_info.phone,
                                        placeholder="Format: (XXX) XXX-XXXX")
                with col3:
                    dob = st.date_input("Date of Birth*", 
                                    value=patient_info.date_of_birth or datetime.datetime.now().date() - datetime.timedelta(days=365*30),
                                    help="Select your date of birth from the calendar")
                
                # Address information with better visual grouping
                st.markdown("<h4 style='margin-top: 25px; margin-bottom: 15px;'>Address Information</h4>", unsafe_allow_html=True)
                
                st.text_input("Street Address", value=patient_info.address,
                            placeholder="Enter your current street address")
                
                col1, col2, col3 = st.columns([2,1,1])
                with col1:
                    city = st.text_input("City", value=patient_info.city,
                                      placeholder="Your city of residence")
                with col2:
                    state = st.text_input("State", value=patient_info.state,
                                       placeholder="State abbreviation")
                with col3:
                    zip_code = st.text_input("ZIP Code", value=patient_info.zip_code,
                                          placeholder="5-digit ZIP code")
                
                # Emergency contact with visual separation
                st.markdown("""
                <h4 style='margin-top: 25px; margin-bottom: 15px;'>Emergency Contact</h4>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please provide a contact person in case of emergency.
                </p>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    emergency_name = st.text_input("Emergency Contact Name", 
                                                value=patient_info.emergency_contact_name,
                                                placeholder="Full name of emergency contact")
                with col2:
                    emergency_phone = st.text_input("Emergency Contact Phone", 
                                                 value=patient_info.emergency_contact_phone,
                                                 placeholder="Emergency contact's phone number")
                
                # Required fields notice
                st.markdown("""
                <p style='margin-top: 25px; font-size: 0.9rem;'>* Required fields</p>
                """, unsafe_allow_html=True)
                
                # Enhanced consent checkbox
                consent = st.checkbox("I confirm that the information provided is accurate and complete to the best of my knowledge",
                                   value=True)
                
                # Submit button with professional styling
                submitted = st.form_submit_button("Save & Continue")
                
                if submitted:
                    # Validate required fields
                    if not (first_name and last_name and email and phone and dob and consent):
                        st.error("Please fill out all required fields and confirm your consent.")
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
                        
                        # Success message with more professional design
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Information Saved Successfully</h4>
                            <p style="margin-bottom: 0;">Your contact information has been securely stored. Please proceed to the Medical History form.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Offer navigation to next form
                        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                        if st.button("Continue to Medical History →", use_container_width=True):
                            page = "Medical History"
                            st.experimental_rerun()
            
            # Professional guidance note at the bottom
            st.markdown("""
            <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Privacy & Security</h4>
                <p style="margin-bottom: 0; font-size: 0.9rem;">
                    All information provided is protected by our privacy policy and HIPAA regulations. Your data is encrypted and access is restricted
                    to authorized healthcare professionals involved in your care. For questions about our privacy practices,
                    please contact our Privacy Officer at privacy@optimumwellness.org.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Medical History":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Medical History Form</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: import streamlit as st
from typing import Dict, List, Union, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import datetime
import random
import time
import json

# Define core persona elements as structured data
class PriorityLevel(Enum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

@dataclass
class ResponseFormat:
    steps: List[str]
    style: Dict[str, str]

@dataclass
class ChatMessage:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

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
        
        # Chat responses for various medical topics
        self.chat_responses = {
            "wellness": [
                "In our clinical approach to wellness optimization, we emphasize the integration of evidence-based lifestyle modifications with targeted interventions. The foundation begins with comprehensive assessment of metabolic, hormonal, and inflammatory markers.",
                "From a functional medicine perspective, wellness requires addressing root causes rather than symptom suppression. Our protocol typically evaluates sleep quality, nutritional status, stress management, and physical activity patterns as foundational elements.",
                "The current medical literature supports a multifaceted approach to wellness. This includes structured nutritional protocols, strategic supplementation based on identified deficiencies, and cognitive-behavioral interventions for stress management."
            ],
            "nutrition": [
                "Nutritional medicine forms a cornerstone of our functional approach. Current research indicates that personalized nutrition based on metabolic typing and inflammatory markers yields superior outcomes compared to generalized dietary recommendations.",
                "In our clinical practice, we utilize advanced nutritional assessments including micronutrient testing, food sensitivity panels, and metabolic markers to develop precision nutritional protocols tailored to individual biochemistry.",
                "The evidence supports targeted nutritional interventions rather than generalized approaches. We typically begin with elimination of inflammatory triggers, followed by structured reintroduction to identify optimal nutritional parameters."
            ],
            "sleep": [
                "Sleep optimization is fundamental to our clinical approach. Current research demonstrates that disrupted sleep architecture significantly impacts hormonal regulation, inflammatory markers, and cognitive function.",
                "Our protocol for sleep enhancement includes comprehensive assessment of circadian rhythm disruptions, evaluation of potential obstructive patterns, and analysis of neurochemical imbalances that may interfere with normal sleep progression.",
                "Evidence-based interventions for sleep quality improvement include structured sleep hygiene protocols, environmental optimization, and when indicated, targeted supplementation to address specific neurotransmitter imbalances."
            ],
            "stress": [
                "From a functional medicine perspective, chronic stress activation represents a significant driver of inflammatory processes and hormonal dysregulation. Our approach focuses on quantifiable assessment of HPA axis function.",
                "The clinical literature supports a structured approach to stress management, incorporating both physiological and psychological interventions. We utilize validated assessment tools to measure stress response patterns.",
                "Our protocol typically includes targeted adaptogenic support, structured cognitive reframing techniques, and autonomic nervous system regulation practices, all customized based on individual response patterns."
            ],
            "aging": [
                "Anti-aging medicine is approached from a scientific perspective in our practice. The focus remains on measurable biomarkers of cellular health, including telomere dynamics, oxidative stress parameters, and glycation endpoints.",
                "Current research supports interventions targeting specific aging mechanisms rather than general approaches. Our protocol evaluates mitochondrial function, inflammatory status, and hormonal optimization within physiological parameters.",
                "The evidence demonstrates that targeted interventions for biological age reduction must be personalized. We utilize comprehensive biomarker assessment to develop precision protocols for cellular rejuvenation."
            ],
            "hormones": [
                "Hormonal balance requires a comprehensive systems-based approach. Current clinical research indicates that evaluating the full spectrum of endocrine markers yields superior outcomes compared to isolated hormone assessment.",
                "Our protocol includes evaluation of steroid hormone pathways, thyroid function, and insulin dynamics. The integration of these systems provides a more accurate clinical picture than isolated assessment.",
                "Evidence-based hormonal optimization focuses on restoration of physiological patterns rather than simple supplementation. We utilize chronobiological principles to restore natural hormonal rhythms."
            ],
            "inflammation": [
                "Chronic inflammation represents a common pathway in numerous pathological processes. Our clinical approach includes comprehensive assessment of inflammatory markers and mediators to identify specific activation patterns.",
                "The research supports targeted anti-inflammatory protocols based on identified triggers rather than generalized approaches. We evaluate environmental, nutritional, and microbial factors in our assessment.",
                "Our evidence-based protocol typically includes elimination of inflammatory triggers, gastrointestinal barrier restoration, and targeted nutritional interventions to modulate specific inflammatory pathways."
            ],
            "detoxification": [
                "Detoxification capacity represents a critical element in our functional medicine assessment. We evaluate phase I and phase II detoxification pathways through validated biomarkers rather than generalized assumptions.",
                "The clinical evidence supports structured protocols for enhancing physiological detoxification processes. Our approach includes assessment of toxic burden alongside metabolic detoxification capacity.",
                "Our protocol typically includes strategic nutritional support for specific detoxification pathways, reduction of exposure sources, and enhancement of elimination mechanisms through validated clinical interventions."
            ],
            "gut_health": [
                "Gastrointestinal function serves as a cornerstone in our clinical assessment. Current research demonstrates the central role of gut integrity, microbiome diversity, and digestive efficiency in systemic health outcomes.",
                "Our protocol includes comprehensive evaluation of digestive function, intestinal permeability, microbial balance, and immunological markers to develop precision interventions for gastrointestinal optimization.",
                "The evidence supports a structured approach to gastrointestinal restoration, including targeted elimination of pathogenic factors, reestablishment of beneficial microbial communities, and restoration of mucosal integrity."
            ],
            "default": [
                "I would need to conduct a more thorough clinical assessment to provide specific recommendations regarding your inquiry. Our practice emphasizes evidence-based approaches customized to individual patient presentations.",
                "From a functional medicine perspective, addressing your concerns would require comprehensive evaluation of relevant biomarkers and clinical parameters. This allows for development of targeted interventions based on identified mechanisms.",
                "The current medical literature supports an individualized approach to your clinical question. Our protocol would include assessment of relevant systems followed by development of a structured intervention strategy."
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
    
    def get_chat_response(self, query: str) -> str:
        """Generates a chat response based on the query content"""
        # Determine the topic based on keywords in the query
        query_lower = query.lower()
        
        # Check for topic matches
        if any(word in query_lower for word in ["wellness", "well-being", "wellbeing", "health optimization"]):
            responses = self.chat_responses["wellness"]
        elif any(word in query_lower for word in ["nutrition", "diet", "food", "eating"]):
            responses = self.chat_responses["nutrition"]
        elif any(word in query_lower for word in ["sleep", "insomnia", "rest", "fatigue"]):
            responses = self.chat_responses["sleep"]
        elif any(word in query_lower for word in ["stress", "anxiety", "overwhelm", "burnout"]):
            responses = self.chat_responses["stress"]
        elif any(word in query_lower for word in ["aging", "longevity", "anti-aging"]):
            responses = self.chat_responses["aging"]
        elif any(word in query_lower for word in ["hormone", "thyroid", "estrogen", "testosterone"]):
            responses = self.chat_responses["hormones"]
        elif any(word in query_lower for word in ["inflammation", "inflammatory", "autoimmune"]):
            responses = self.chat_responses["inflammation"]
        elif any(word in query_lower for word in ["detox", "toxin", "cleanse"]):
            responses = self.chat_responses["detoxification"]
        elif any(word in query_lower for word in ["gut", "digestive", "stomach", "intestine", "microbiome"]):
            responses = self.chat_responses["gut_health"]
        else:
            responses = self.chat_responses["default"]
        
        # Select a response from the appropriate category
        return random.choice(responses)

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

def display_chat_message(message: ChatMessage):
    """Display a single chat message with appropriate styling"""
    if message.role == "assistant":
        with st.chat_message("assistant", avatar="🩺"):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%I:%M %p')}")
    else:  # user message
        with st.chat_message("user"):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%I:%M %p')}")

# Function to get descriptions for DEI focus areas
def get_dei_description(focus):
    descriptions = {
        "Maintain awareness of healthcare disparities": "We actively monitor and address inequities in healthcare access, treatment, and outcomes across different populations.",
        "Provide culturally competent care": "Our approach incorporates cultural factors and beliefs that may impact health behaviors and treatment preferences.",
        "Consider LGBTQ+ health perspectives": "We acknowledge unique health concerns and create supportive care environments for LGBTQ+ individuals.",
        "Implement inclusive language": "Our communications use terminology that respects diversity of identity, experience, and background.",
        "Address systemic healthcare barriers": "We work to identify and minimize structural obstacles that prevent equitable access to quality care."
    }
    return descriptions.get(focus, "")

# Function to get descriptions for intervention hierarchy
def get_hierarchy_description(hierarchy):
    descriptions = {
        "Remove pathological triggers": "Identify and eliminate factors that activate or perpetuate dysfunction",
        "Restore physiological function": "Support normal biological processes through targeted interventions",
        "Rebalance regulatory systems": "Address control mechanisms that coordinate multiple physiological processes",
        "Regenerate compromised tissues": "Support cellular renewal and structural integrity where needed",
        "Reestablish health maintenance": "Implement sustainable strategies for ongoing wellbeing"
    }
    return descriptions.get(hierarchy, "")

# Streamlit Application Implementation
def main():
    st.set_page_config(
        page_title="Dr. Jackson DNP - Medical Professional Consultation",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Dr. Jackson DNP - Professional Medical Consultation Platform",
            'Report a bug': "mailto:support@drjackson-platform.org",
            'Get help': "https://drjackson-platform.org/help"
        }
    )
    
    # Initialize persona and settings
    dr_jackson = DrJacksonPersona()
    llm_settings = LLMSettings()
    
    # Initialize session state for patient data if not exist
    if 'patient_contact_info' not in st.session_state:
        st.session_state['patient_contact_info'] = PatientContactInfo()
    if 'patient_medical_info' not in st.session_state:
        st.session_state['patient_medical_info'] = PatientMedicalInfo()
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    # Custom CSS for theming and professional layout
    st.markdown("""
    <style>
    :root {
        --primary-color: #5D5CDE;
        --secondary-color: #4B4BA3;
        --tertiary-color: #E0E0FA;
        --accent-color: #FF7D54;
        --light-bg: #FFFFFF;
        --off-white: #F8F9FA;
        --light-gray: #E9ECEF;
        --medium-gray: #CED4DA;
        --dark-gray: #6C757D;
        --dark-bg: #181818;
        --dark-mode-card: #2C2C2C;
        --light-text: #333333;
        --dark-text: #E5E5E5;
        --light-border: #E2E8F0;
        --dark-border: #374151;
        --light-input: #F9FAFB;
        --dark-input: #1F2937;
        --success-color: #3DC9A1;
        --warning-color: #FFBE55;
        --error-color: #FF5A5A;
        --info-color: #5AA0FF;
    }
    
    /* Base Styling */
    .stApp {
        background-color: var(--light-bg);
        color: var(--light-text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .dark-mode .stApp {
        background-color: var(--dark-bg);
        color: var(--dark-text);
    }
    
    /* Typography Refinements */
    h1 {
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.01em;
        color: var(--primary-color);
        margin-bottom: 1rem;
    }
    
    h2 {
        font-weight: 600;
        font-size: 1.8rem;
        letter-spacing: -0.01em;
        color: var(--primary-color);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-weight: 600;
        font-size: 1.4rem;
        color: var(--primary-color);
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    p, li {
        font-size: 1rem;
        line-height: 1.6;
        color: var(--light-text);
    }
    
    .dark-mode p, .dark-mode li {
        color: var(--dark-text);
    }
    
    /* Card/Container Styling */
    div[data-testid="stForm"] {
        background-color: var(--off-white);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        border: 1px solid var(--light-border);
        margin-bottom: 24px;
    }
    
    .dark-mode div[data-testid="stForm"] {
        background-color: var(--dark-mode-card);
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        border: 1px solid var(--dark-border);
    }
    
    /* Expander Styling */
    details {
        background-color: var(--off-white);
        border-radius: 8px;
        border: 1px solid var(--light-border);
        margin-bottom: 16px;
        overflow: hidden;
    }
    
    .dark-mode details {
        background-color: var(--dark-mode-card);
        border: 1px solid var(--dark-border);
    }
    
    details summary {
        padding: 16px;
        cursor: pointer;
        font-weight: 500;
    }
    
    details summary:hover {
        background-color: var(--light-gray);
    }
    
    .dark-mode details summary:hover {
        background-color: rgba(255,255,255,0.05);
    }
    
    /* Button Styling */
    .stButton button {
        background-color: var(--primary-color);
        color: white;
        font-weight: 500;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--off-white);
        border-right: 1px solid var(--light-border);
    }
    
    .dark-mode [data-testid="stSidebar"] {
        background-color: var(--dark-mode-card);
        border-right: 1px solid var(--dark-border);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 1.5rem;
    }
    
    /* Header Styling */
    .professional-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 15px rgba(93, 92, 222, 0.25);
    }
    
    .professional-header h1 {
        color: white;
        margin-bottom: 0.5rem;
        font-size: 2.4rem;
    }
    
    .professional-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* HIPAA Notice Styling */
    .hipaa-notice {
        background-color: var(--tertiary-color);
        border-left: 4px solid var(--primary-color);
        padding: 16px;
        margin: 20px 0;
        border-radius: 6px;
    }
    
    .dark-mode .hipaa-notice {
        background-color: rgba(93, 92, 222, 0.15);
    }
    
    /* Chat Styling */
    .chat-container {
        border-radius: 12px;
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border: 1px solid var(--light-border);
        background-color: var(--off-white);
    }
    
    .dark-mode .chat-container {
        border: 1px solid var(--dark-border);
        background-color: var(--dark-mode-card);
    }
    
    /* Chat Message Styling */
    [data-testid="stChatMessage"] {
        padding: 0.75rem 0;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
        background-color: var(--light-gray);
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
        background-color: var(--primary-color);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 10px 16px;
        background-color: var(--light-gray);
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-colorst.markdown(f"""
                            <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid var(--light-border);">
                                <h3 style="margin-top: 0;">{domain}</h3>
                                <div class="professional-separator"></div>
                            """, unsafe_allow_html=True)
                            
                            if domain == "Gut Health":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Gastrointestinal function serves as a cornerstone of systemic health. Our approach addresses
                                    digestive efficiency, intestinal barrier integrity, microbiome diversity, and enteric nervous system
                                    regulation through targeted interventions.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>Comprehensive microbiome assessment</li>
                                        <li>Intestinal permeability restoration</li>
                                        <li>Digestive enzyme optimization</li>
                                        <li>Enteric nervous system regulation</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            elif domain == "Oxidative Stress":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Oxidative stress management focuses on balancing pro-oxidant and antioxidant mechanisms.
                                    Our protocols assess redox status and implement targeted interventions to optimize cellular
                                    protection mechanisms.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>Redox balance assessment</li>
                                        <li>Cellular protection enhancement</li>
                                        <li>Antioxidant enzyme support</li>
                                        <li>Mitochondrial protection protocols</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            elif domain == "Professional Development":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Continuing professional development ensures implementation of the latest evidence-based
                                    approaches. Our practice maintains rigorous standards for ongoing education and clinical
                                    knowledge integration.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>Continuous medical education</li>
                                        <li>Research literature integration</li>
                                        <li>Advanced protocol development</li>
                                        <li>Clinical outcomes assessment</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("""
                            </div>
                            """, unsafe_allow_html=True)
            
            with specialty_tabs[2]:
                st.markdown("""
                <h3 style="margin-bottom: 25px;">Treatment Approaches</h3>
                <p style="margin-bottom: 30px;">
                    Dr. Jackson's practice implements structured, evidence-based treatment protocols
                    that address underlying mechanisms rather than symptoms alone. Each approach follows
                    a systematic implementation process designed for optimal outcomes.
                </p>
                """, unsafe_allow_html=True)
                
                # Sample treatment approaches with more professional styling
                approaches = [
                    {"name": "Integrative Medicine Protocols", 
                     "description": "Combining conventional medical standards with evidence-based complementary approaches to address both symptoms and underlying mechanisms.",
                     "phases": ["Comprehensive assessment", "Multisystem analysis", "Integrated intervention design", "Coordinated implementation", "Progress monitoring"]},
                    {"name": "Functional Nutrition Plans", 
                     "description": "Therapeutic dietary interventions based on individual biochemistry and specific nutritional needs identified through advanced testing.",
                     "phases": ["Nutritional assessment", "Elimination protocol", "Therapeutic reintroduction", "Supplementation strategy", "Maintenance planning"]},
                    {"name": "Targeted Supplementation", 
                     "description": "Precision micronutrient, botanical, and nutraceutical interventions based on identified biochemical imbalances and functional requirements.",
                     "phases": ["Deficiency identification", "Interaction analysis", "Bioavailability optimization", "Therapeutic dosing", "Efficacy monitoring"]},
                    {"name": "Lifestyle Modification Programs", 
                     "description": "Structured protocols for sleep optimization, stress management, physical activity, and environmental modification.",
                     "phases": ["Behavioral assessment", "Priority identification", "Incremental implementation", "Habit formation support", "Progress evaluation"]},
                    {"name": "Mind-Body Interventions", 
                     "description": "Evidence-based approaches targeting the psychoneuroimmunological axis through cognitive, somatic, and contemplative practices.",
                     "phases": ["Stress response assessment", "Technique selection", "Implementation structure", "Practice integration", "Response monitoring"]}
                ]
                
                for approach in approaches:
                    with st.expander(approach["name"]):
                        st.markdown(f"""
                        <div style="margin-bottom: 20px;">
                            <h4 style="margin-top: 0;">{approach["name"]}</h4>
                            <p style="margin-bottom: 20px;">{approach['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Phase visualization with enhanced styling
                        st.markdown("""
                        <h4 style="font-size: 1.1rem; margin-bottom: 15px;">Implementation Phases</h4>
                        """, unsafe_allow_html=True)
                        
                        phase_cols = st.columns(len(approach["phases"]))
                        
                        for i, (col, phase) in enumerate(zip(phase_cols, approach["phases"])):
                            with col:
                                st.markdown(f"""
                                <div style="padding: 15px; border-radius: 8px; background-color: rgba(93, 92, 222, {0.1 + (i * 0.08)}); 
                                           text-align: center; height: 110px; display: flex; flex-direction: column; 
                                           align-items: center; justify-content: center; border: 1px solid rgba(93, 92, 222, 0.2);">
                                    <div style="background-color: white; width: 25px; height: 25px; border-radius: 50%; 
                                             display: flex; align-items: center; justify-content: center; 
                                             margin-bottom: 10px; font-weight: bold; color: var(--primary-color);">
                                        {i+1}
                                    </div>
                                    <p style="margin: 0; font-weight: 500; font-size: 0.9rem; color: rgba(0,0,0,0.8);">{phase}</p>
                                </div>
                                """, unsafe_allow_html=True)
                
                # Treatment philosophy statement with enhanced styling
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 25px; border-radius: 10px; margin-top: 40px; border: 1px solid var(--light-border);">
                    <h4 style="color: var(--primary-color); margin-top: 0;">Treatment Philosophy</h4>
                    <div class="professional-separator"></div>
                    <p style="margin-top: 15px;">
                        All treatment approaches are implemented with rigorous attention to evidence-based standards and individualized 
                        based on comprehensive patient assessment. Dr. Jackson's clinical protocols integrate multiple therapeutic 
                        modalities while maintaining strict adherence to professional practice guidelines.
                    </p>
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;">
                        <div style="flex: 1; min-width: 200px;">
                            <h5 style="margin-top: 0; font-size: 1rem;">Evidence-Based</h5>
                            <p style="font-size: 0.9rem; margin-bottom: 0;">
                                All protocols are grounded in current research literature and clinical evidence,
                                with continuous updates as new findings emerge.
                            </p>
                        </div>
                        <div style="flex: 1; min-width: 200px;">
                            <h5 style="margin-top: 0; font-size: 1rem;">Personalized</h5>
                            <p style="font-size: 0.9rem; margin-bottom: 0;">
                                Treatment plans are tailored to each patient's unique biochemistry,
                                genetic predispositions, and specific health goals.
                            </p>
                        </div>
                        <div style="flex: 1; min-width: 200px;">
                            <h5 style="margin-top: 0; font-size: 1rem;">Comprehensive</h5>
                            <p style="font-size: 0.9rem; margin-bottom: 0;">
                                Our approach addresses all relevant physiological systems rather than
                                isolated symptoms or single-system interventions.
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Call to action
                st.markdown("""
                <div style="margin-top: 40px; text-align: center;">
                    <p style="font-size: 1.1rem; margin-bottom: 20px;">
                        Ready to explore how these treatment approaches can be customized for your specific health needs?
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Schedule a Consultation", key="specialty_consult_btn", use_container_width=True):
                        page = "Consultation"
                        st.experimental_rerun()
                with col2:
                    if st.button("Chat with Dr. Jackson", key="specialty_chat_btn", use_container_width=True):
                        page = "Chat with Dr. Jackson"
                        st.experimental_rerun()
        
        elif page == "Approach":
            # Professional header
            st.markdown("""
            <h1>Professional Methodology</h1>
            <div class="professional-separator" style="width: 150px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
            
            # Display knowledge priorities with enhanced styling
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Evidence-Based Approach</h3>
            <p style="margin-bottom: 30px;">
                Dr. Jackson's practice is built on a hierarchical approach to medical knowledge, prioritizing 
                rigorous evidence while integrating multiple perspectives to provide comprehensive care.
            </p>
            """, unsafe_allow_html=True)
            
            # Use more engaging visual representation
            priorities = dr_jackson.knowledge_priorities
            
            # Create a card-based layout for priorities
            st.markdown("""
            <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 40px;">
            """, unsafe_allow_html=True)
            
            for i, priority in enumerate(priorities):
                # Calculate progress bar percentage based on reversed position (higher items get higher percentage)
                percentage = 100 - (i * (100 / len(priorities)))
                
                st.markdown(f"""
                <div style="flex: 1; min-width: 300px; background-color: var(--off-white); padding: 20px; border-radius: 10px; border: 1px solid var(--light-border);">
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="background-color: var(--primary-color); width: 30px; height: 30px; border-radius: 50%; 
                                 display: flex; align-items: center; justify-content: center; 
                                 margin-right: 15px; font-weight: bold; color: white;">
                            {i+1}
                        </div>
                        <h4 style="margin: 0; font-size: 1.2rem;">{priority}</h4>
                    </div>
                    <div style="background-color: var(--light-gray); height: 8px; border-radius: 4px; margin-bottom: 15px;">
                        <div style="background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%); 
                                  height: 8px; border-radius: 4px; width: {percentage}%;"></div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Add explanatory text for each priority
                if i == 0:  # Evidence-based research
                    st.markdown("""
                    <p style="font-size: 0.9rem;">
                        Peer-reviewed studies form the foundation of our clinical approach. We prioritize 
                        systematic reviews, meta-analyses, and randomized controlled trials when available.
                    </p>
                    """, unsafe_allow_html=True)
                elif i == 1:  # Clinical guidelines
                    st.markdown("""
                    <p style="font-size: 0.9rem;">
                        Professional medical association guidelines and consensus statements provide 
                        standardized frameworks for our clinical protocols.
                    </p>
                    """, unsafe_allow_html=True)
                elif i == 2:  # Professional experience
                    st.markdown("""
                    <p style="font-size: 0.9rem;">
                        Clinical expertise developed through years of patient care informs the application 
                        of research findings to individual cases.
                    </p>
                    """, unsafe_allow_html=True)
                elif i == 3:  # Holistic wellness approaches
                    st.markdown("""
                    <p style="font-size: 0.9rem;">
                        Evidence-supported complementary approaches are integrated when appropriate to 
                        address the full spectrum of patient wellbeing.
                    </p>
                    """, unsafe_allow_html=True)
                elif i == 4:  # Integrative medicine perspectives
                    st.markdown("""
                    <p style="font-size: 0.9rem;">
                        Traditional healing systems with empirical support are considered within our 
                        comprehensive treatment frameworks.
                    </p>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Communication framework with enhanced styling
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Clinical Communication Framework</h3>
            <p style="margin-bottom: 30px;">
                Professional communication is essential to effective clinical care. Dr. Jackson's practice 
                follows a structured communication methodology to ensure clarity, comprehensiveness, and patient understanding.
            </p>
            """, unsafe_allow_html=True)
            
            cols = st.columns(3)
            with cols[0]:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0; text-align: center; margin-bottom: 15px;">Structure</h4>
                    <div class="professional-separator"></div>
                """, unsafe_allow_html=True)
                
                for step in dr_jackson.clinical_format.steps:
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <div style="min-width: 8px; height: 8px; background-color: var(--primary-color); border-radius: 50%; margin-right: 10px;"></div>
                        <p style="margin: 0;">{step}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            with cols[1]:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0; text-align: center; margin-bottom: 15px;">Style</h4>
                    <div class="professional-separator"></div>
                """, unsafe_allow_html=True)
                
                for key, value in dr_jackson.clinical_format.style.items():
                    st.markdown(f"""
                    <div style="margin-bottom: 15px;">
                        <h5 style="margin-bottom: 5px; color: var(--primary-color);">{key.capitalize()}</h5>
                        <p style="margin: 0; padding-left: 10px; border-left: 3px solid var(--primary-color);">{value}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            with cols[2]:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0; text-align: center; margin-bottom: 15px;">Values</h4>
                    <div class="professional-separator"></div>
                """, unsafe_allow_html=True)
                
                for i, value in enumerate(dr_jackson.core_values[:4]):
                    st.markdown(f"""
                    <div style="background-color: rgba(93, 92, 222, {0.05 + (i * 0.02)}); padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                        <p style="margin: 0; font-weight: 500;">{value}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # DEI focus with enhanced styling
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Inclusive Care Framework</h3>
            <p style="margin-bottom: 30px;">
                Dr. Jackson's practice emphasizes equitable, culturally-responsive care that addresses healthcare 
                disparities and provides appropriate support for all patients regardless of background or identity.
            </p>
            """, unsafe_allow_html=True)
            
            # More engaging presentation
            with st.container():
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 25px; border-radius: 10px; margin-bottom: 30px; border: 1px solid var(--light-border);">
                    <h4 style="color: var(--primary-color); margin-top: 0; text-align: center;">Equitable Healthcare Approach</h4>
                    <p style="text-align: center; margin-bottom: 25px;">Dr. Jackson's practice emphasizes inclusive, culturally-responsive care through the following principles:</p>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                dei_focus_items = dr_jackson.dei_focus
                
                for i, focus in enumerate(dei_focus_items[:3]):
                    with col1:
                        st.markdown(f"""
                        <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid var(--primary-color);">
                            <h5 style="margin-top: 0; margin-bottom: 10px; font-size: 1rem;">{i+1}. {focus}</h5>
                            <p style="margin: 0; font-size: 0.9rem;">
                                {get_dei_description(focus)}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                
                for i, focus in enumerate(dei_focus_items[3:], 4):
                    with col2:
                        st.markdown(f"""
                        <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid var(--primary-color);">
                            <h5 style="margin-top: 0; margin-bottom: 10px; font-size: 1rem;">{i+1}. {focus}</h5>
                            <p style="margin: 0; font-size: 0.9rem;">
                                {get_dei_description(focus)}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Treatment philosophy with enhanced styling
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Treatment Philosophy</h3>
            <p style="margin-bottom: 30px;">
                Dr. Jackson's clinical approach integrates conventional medical standards with evidence-supported 
                complementary modalities. This model addresses not only symptom management but underlying 
                pathophysiological mechanisms.
            </p>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0;">Foundational Elements</h4>
                    <div class="professional-separator"></div>
                """, unsafe_allow_html=True)
                
                elements = [
                    "Comprehensive laboratory assessment",
                    "Detailed functional history",
                    "Environmental exposure evaluation",
                    "Nutritional status optimization",
                    "Sleep architecture normalization"
                ]
                
                for element in elements:
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="min-width: 24px; height: 24px; background-color: var(--primary-color); 
                                 border-radius: 50%; margin-right: 15px; display: flex; 
                                 align-items: center; justify-content: center; color: white;">
                            ✓
                        </div>
                        <p style="margin: 0; font-weight: 500;">{element}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0;">Intervention Hierarchy</h4>
                    <div class="professional-separator"></div>
                """, unsafe_allow_html=True)
                
                hierarchies = [
                    "Remove pathological triggers",
                    "Restore physiological function",
                    "Rebalance regulatory systems",
                    "Regenerate compromised tissues",
                    "Reestablish health maintenance"
                ]
                
                for i, hierarchy in enumerate(hierarchies):
                    st.markdown(f"""
                    <div style="display: flex; margin-bottom: 12px;">
                        <div style="min-width: 30px; margin-right: 15px; text-align: center;">
                            <div style="background-color: var(--primary-color); width: 30px; height: 30px; 
                                     border-radius: 50%; display: flex; align-items: center; 
                                     justify-content: center; color: white; font-weight: bold;">
                                {i+1}
                            </div>
                        </div>
                        <div>
                            <p style="margin: 0 0 5px 0; font-weight: 500;">{hierarchy}</p>
                            <p style="margin: 0; font-size: 0.85rem; color: var(--dark-gray);">
                                {get_hierarchy_description(hierarchy)}
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            # Bottom CTA
            st.markdown("""
            <div style="text-align: center; margin-top: 40px;">
                <p style="font-size: 1.1rem; margin-bottom: 20px;">
                    Experience Dr. Jackson's professional approach to healthcare with a personalized consultation.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1,1])
            with col1:
                if st.button("Schedule Consultation", key="approach_consult_btn", use_container_width=True):
                    page = "Consultation"
                    st.experimental_rerun()
            with col2:
                if st.button("Learn About Specialties", key="approach_specialties_btn", use_container_width=True):
                    page = "Specialties"
                    st.experimental_rerun()
        
        elif page == "Resources":
            # Professional header
            st.markdown("""
            <h1>Professional Resources</h1>
            <div class="professional-separator" style="width: 150px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
            
            # HIPAA Notice with enhanced styling
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; 
                       border-left: 5px solid var(--info-color); margin-bottom: 30px;">
                <h4 style="color: var(--info-color); margin-top: 0;">HIPAA Compliance Notice</h4>
                <p style="margin-bottom: 10px;">All educational resources and materials provided through this platform are protected by HIPAA regulations:</p>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                    <li style="margin-bottom: 5px;">Materials are for educational purposes only and do not constitute medical advice</li>
                    <li style="margin-bottom: 5px;">Resources are provided securely and cannot be accessed by unauthorized parties</li>
                    <li style="margin-bottom: 5px;">Your use of these materials is confidential and not shared with third parties</li>
                    <li style="margin-bottom: 0;">All resource access is logged for privacy and security purposes</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Educational resources tabs with enhanced styling
            st.markdown("""
            <p style="margin-bottom: 25px;">
                Dr. Jackson's practice provides a range of professional resources to support your healthcare journey.
                These materials are curated from evidence-based sources and aligned with our clinical approach.
            </p>
            """, unsafe_allow_html=True)
            
            resource_tabs = st.tabs(["Patient Education", "Treatment Information", "Research & Publications"])
            
            with resource_tabs[0]:
                st.markdown("""
                <h3 style="margin-bottom: 25px;">Patient Education Materials</h3>
                <p style="margin-bottom: 30px;">
                    These educational resources are designed to provide evidence-based information
                    about various health conditions, therapeutic approaches, and self-care strategies.
                </p>
                """, unsafe_allow_html=True)
                
                # Resource categories with enhanced styling
                categories = [
                    "Functional Medicine Basics",
                    "Nutritional Approaches",
                    "Stress Management",
                    "Hormone Balance",
                    "Gut Health",
                    "Sleep Optimization"
                ]
                
                # Category selection with better styling
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-bottom: 25px; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0; margin-bottom: 15px;">Select a Resource Category</h4>
                """, unsafe_allow_html=True)
                
                selected_category = st.selectbox("Select a category", categories, label_visibility="collapsed")
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
                
                # Display sample resources based on category with enhanced styling
                st.markdown(f"""
                <h4 style="margin-bottom: 20px;">{selected_category} Resources</h4>
                """, unsafe_allow_html=True)
                
                # Sample resources with enhanced styling
                resources = [
                    {"title": f"{selected_category} Primer", "type": "PDF Guide", "description": "A comprehensive introduction to key concepts and approaches.", "icon": "📄"},
                    {"title": f"Understanding Your {selected_category} Assessment", "type": "Video", "description": "A visual explanation of assessment methods and interpretation.", "icon": "🎥"},
                    {"title": f"{selected_category} FAQ", "type": "Article", "description": "Answers to commonly asked questions about this topic.", "icon": "❓"}
                ]
                
                for resource in resources:
                    with st.expander(resource["title"]):
                        st.markdown(f"""
                        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                            <div style="flex: 3; min-width: 300px;">
                                <h5 style="margin-top: 0; margin-            # Professional header
            st.markdown("""
            <h1>Professional Chat Consultation</h1>
            <div class="professional-separator" style="width: 150px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
            
            # Check if patient info is filled out
            patient_info = st.session_state['patient_contact_info']
            
            if not patient_info.first_name or not patient_info.last_name:
                # Warning with enhanced styling
                st.markdown("""
                <div style="background-color: rgba(255, 190, 85, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--warning-color);">
                    <h4 style="color: var(--warning-color); margin-top: 0;">Patient Information Required</h4>
                    <p style="margin-bottom: 15px;">Please complete the Patient Intake form before using the chat feature.</p>
                """, unsafe_allow_html=True)
                
                if st.button("Go to Patient Intake →", use_container_width=True):
                    page = "Patient Intake"
                    st.experimental_rerun()
                    
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                # Two-column layout for chat interface
                chat_col, sidebar_col = st.columns([3, 1])
                
                with chat_col:
                    # HIPAA notice for chat with enhanced styling
                    st.markdown("""
                    <div style="background-color: rgba(90, 160, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid var(--info-color);">
                        <h4 style="color: var(--info-color); margin-top: 0;">Secure Communication</h4>
                        <p style="margin-bottom: 0;">This chat is encrypted and complies with HIPAA regulations. While this platform provides general guidance, it is not a substitute for in-person medical care for urgent or emergency conditions.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced chat container
                    st.markdown("""
                    <div style="background-color: var(--off-white); border-radius: 10px; border: 1px solid var(--light-border); padding: 5px; margin-bottom: 20px;">
                    """, unsafe_allow_html=True)
                    
                    # Chat container
                    chat_container = st.container()
                    with chat_container:
                        for message in st.session_state['chat_history']:
                            display_chat_message(message)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Welcome message if chat is empty
                    if not st.session_state['chat_history']:
                        with st.chat_message("assistant", avatar="🩺"):
                            intro_message = f"Good day, {patient_info.first_name}. I am Dr. Jackson, {dr_jackson.credentials}, specializing in functional and integrative medicine. How may I be of assistance to you today?"
                            st.markdown(intro_message)
                            # Add welcome message to history
                            st.session_state['chat_history'].append(
                                ChatMessage(role="assistant", content=intro_message)
                            )
                    
                    # Chat input with professional styling
                    st.markdown("""
                    <div style="margin-bottom: 10px;">
                        <h4 style="font-size: 1rem; margin-bottom: 5px;">Your Message</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    user_input = st.chat_input("Type your medical question here...")
                    
                    if user_input:
                        # Add user message to history
                        st.session_state['chat_history'].append(
                            ChatMessage(role="user", content=user_input)
                        )
                        
                        # Display the new user message
                        with st.chat_message("user"):
                            st.markdown(user_input)
                        
                        # Generate and display Dr. Jackson's response
                        with st.chat_message("assistant", avatar="🩺"):
                            message_placeholder = st.empty()
                            
                            # Simulate typing with a delay
                            full_response = dr_jackson.get_chat_response(user_input)
                            
                            # Simulate typing effect
                            displayed_response = ""
                            for chunk in full_response.split():
                                displayed_response += chunk + " "
                                message_placeholder.markdown(displayed_response + "▌")
                                time.sleep(0.03)  # Faster typing
                            
                            message_placeholder.markdown(full_response)
                            st.caption(f"{datetime.datetime.now().strftime('%I:%M %p')}")
                        
                        # Add assistant response to history
                        st.session_state['chat_history'].append(
                            ChatMessage(role="assistant", content=full_response)
                        )
                        
                        # Enhanced follow-up options
                        st.markdown("""
                        <div style="margin-top: 20px;">
                            <h4 style="font-size: 1rem; margin-bottom: 15px;">Quick Follow-up Options</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("Request additional information", key="more_info_btn", use_container_width=True):
                                followup = "Can you provide additional information or resources about this topic?"
                                st.session_state['chat_history'].append(
                                    ChatMessage(role="user", content=followup)
                                )
                                st.experimental_rerun()
                        
                        with col2:
                            if st.button("Schedule consultation", key="schedule_btn", use_container_width=True):
                                followup = "I'd like to schedule a full consultation to discuss this in more detail."
                                st.session_state['chat_history'].append(
                                    ChatMessage(role="user", content=followup)
                                )
                                st.experimental_rerun()
                        
                        with col3:
                            if st.button("Ask about treatment options", key="treatment_btn", use_container_width=True):
                                followup = "What treatment approaches would you recommend for this condition?"
                                st.session_state['chat_history'].append(
                                    ChatMessage(role="user", content=followup)
                                )
                                st.experimental_rerun()
                
                with sidebar_col:
                    # Enhanced patient context
                    st.markdown("""
                    <div style="background-color: var(--off-white); padding: 15px; border-radius: 10px; border: 1px solid var(--light-border); margin-bottom: 20px;">
                        <h4 style="margin-top: 0; font-size: 1rem;">Patient Context</h4>
                        <div class="professional-separator" style="margin: 10px 0;"></div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Name:</strong> {patient_info.first_name} {patient_info.last_name}</p>
                        <p style="margin: 5px 0; font-size: 0.9rem;"><strong>DOB:</strong> {patient_info.date_of_birth}</p>
                    """, unsafe_allow_html=True)
                    
                    medical_info = st.session_state['patient_medical_info']
                    if medical_info.chronic_conditions:
                        conditions = ", ".join(medical_info.chronic_conditions[:2])
                        if len(medical_info.chronic_conditions) > 2:
                            conditions += "..."
                        st.markdown(f"""
                            <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Conditions:</strong> {conditions}</p>
                        """, unsafe_allow_html=True)
                        
                    if medical_info.current_medications:
                        medications = ", ".join(medical_info.current_medications[:2])
                        if len(medical_info.current_medications) > 2:
                            medications += "..."
                        st.markdown(f"""
                            <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Medications:</strong> {medications}</p>
                        """, unsafe_allow_html=True)
                        
                    st.markdown("""
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced chat controls
                    with st.expander("Chat Controls", expanded=False):
                        if st.button("Clear Chat History", use_container_width=True):
                            st.session_state['chat_history'] = []
                            st.success("Chat history has been cleared")
                            st.experimental_rerun()
                        
                        # AI model selection if API keys are configured
                        if any([st.session_state.get('anthropic_api_key'), 
                                st.session_state.get('openai_api_key')]):
                            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                            st.markdown("<h4 style='font-size: 1rem;'>AI Model Selection</h4>", unsafe_allow_html=True)
                            model = st.radio(
                                "Select AI model for consultation",
                                ["Claude (Anthropic)", "GPT-4 (OpenAI)", "Llama (Meta)"],
                                index=0
                            )
                            st.info(f"Currently using: {model}")
                    
                    # Enhanced health topics quick access
                    st.markdown("""
                    <div style="margin-top: 20px;">
                        <h4 style="font-size: 1rem; margin-bottom: 15px;">Common Health Topics</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    topics = [
                        ("Functional Medicine", "🔬"),
                        ("Nutritional Guidance", "🥗"),
                        ("Sleep Optimization", "💤"),
                        ("Stress Management", "🧘‍♀️"),
                        ("Hormone Balance", "⚖️"),
                        ("Gut Health", "🦠")
                    ]
                    
                    for topic, icon in topics:
                        topic_button = f"{icon} {topic}"
                        if st.button(topic_button, key=f"topic_{topic}", use_container_width=True):
                            query = f"I'd like to learn more about {topic.lower()}. What's your approach?"
                            st.session_state['chat_history'].append(
                                ChatMessage(role="user", content=query)
                            )
                            st.experimental_rerun()
                    
                    # Professional note
                    st.markdown("""
                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 15px; border-radius: 10px; margin-top: 25px;">
                        <p style="font-size: 0.85rem; margin: 0;">
                            <strong>Professional Note:</strong> This chat interface provides general medical guidance based on 
                            Dr. Jackson's professional approach. For personalized treatment plans, 
                            we recommend scheduling a comprehensive consultation.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Schedule consultation button
                    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                    if st.button("📅 Schedule Full Consultation", use_container_width=True):
                        page = "Consultation"
                        st.experimental_rerun()
        
        elif page == "Specialties":
            # Professional header
            st.markdown("""
            <h1>Areas of Specialization</h1>
            <div class="professional-separator" style="width: 120px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
            
            # Add tabs for better organization with enhanced styling
            specialty_tabs = st.tabs(["Primary Specialties", "Additional Focus Areas", "Treatment Approaches"])
            
            with specialty_tabs[0]:
                st.markdown("""
                <h3 style="margin-bottom: 20px;">Primary Clinical Specialties</h3>
                <p style="margin-bottom: 25px;">
                    Dr. Jackson's practice offers comprehensive care across the following primary specialties, 
                    with evidence-based approaches tailored to individual patient needs.
                </p>
                """, unsafe_allow_html=True)
                
                # Create a more visual representation of specialties
                for i, domain in enumerate(dr_jackson.primary_domains):
                    with st.expander(f"{i+1}. {domain}", expanded=i==0):
                        # Domain-specific content
                        if domain == "Psychiatric Care":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Our psychiatric care approach integrates conventional psychopharmacology with functional medicine principles. 
                                    We assess neurotransmitter pathways, inflammatory markers, and nutrient status alongside standard psychiatric evaluation.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Comprehensive neurochemical assessment</strong> - Evaluating multiple biochemical pathways</li>
                                        <li><strong>Targeted amino acid therapy</strong> - Precision supplementation for neurotransmitter support</li>
                                        <li><strong>Inflammatory pathway modulation</strong> - Addressing neuroinflammatory contributions</li>
                                        <li><strong>Neuroendocrine optimization</strong> - Balancing HPA axis function</li>
                                        <li><strong>Microbiome-brain axis support</strong> - Targeting gut-brain connection</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Clinical Approach</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our psychiatric protocols integrate conventional assessment with functional testing to identify root causes of mental health conditions.</p>
                                        <p>Treatment plans combine targeted nutritional interventions, lifestyle modifications, and when appropriate, conventional medications in a comprehensive approach.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Psychiatric+Care+Approach", use_column_width=True)
                            
                        elif domain == "Wellness Optimization":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Wellness optimization begins with comprehensive assessment of physiological function across multiple systems.
                                    Our approach establishes personalized baselines and identifies limiting factors in performance and wellbeing.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Metabolic efficiency enhancement</strong> - Optimizing cellular energy production pathways</li>
                                        <li><strong>Cellular energy production</strong> - Supporting mitochondrial function and ATP synthesis</li>
                                        <li><strong>Oxidative stress management</strong> - Balancing pro-oxidant and antioxidant mechanisms</li>
                                        <li><strong>Circadian rhythm optimization</strong> - Restoring natural biological timing systems</li>
                                        <li><strong>Recovery protocol development</strong> - Structured approaches to physiological restoration</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Performance Enhancement</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our wellness optimization protocols identify and address the specific factors limiting your physiological performance.</p>
                                        <p>Rather than generic wellness approaches, we target biochemical, structural, and regulatory elements unique to your health profile.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Wellness+Optimization+Approach", use_column_width=True)
                            
                        elif domain == "Anti-aging Medicine":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Our anti-aging approach focuses on measurable biomarkers of cellular aging rather than cosmetic concerns alone.
                                    We target key mechanisms of cellular senescence and tissue degeneration through evidence-based interventions.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Telomere dynamics assessment</strong> - Evaluating cellular replicative potential</li>
                                        <li><strong>Advanced glycation endpoint management</strong> - Reducing cross-linked protein accumulation</li>
                                        <li><strong>Mitochondrial function optimization</strong> - Enhancing cellular energy production</li>
                                        <li><strong>Senolytic protocol implementation</strong> - Targeted approach to senescent cell burden</li>
                                        <li><strong>Epigenetic modification strategies</strong> - Optimizing gene expression patterns</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Biological Age Management</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our anti-aging protocols focus on measurable biomarkers of aging rather than chronological age.</p>
                                        <p>We implement evidence-based approaches to reduce biological age markers and optimize physiological function.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Anti-aging+Medicine+Approach", use_column_width=True)
                            
                        elif domain == "Functional Medicine":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Functional medicine addresses root causes rather than symptoms alone. Our approach investigates
                                    underlying mechanisms of dysfunction through comprehensive laboratory assessment and detailed history.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Systems biology framework</strong> - Understanding interconnected physiological networks</li>
                                        <li><strong>Biochemical individuality assessment</strong> - Personalized physiological evaluation</li>
                                        <li><strong>Environmental exposure evaluation</strong> - Identifying toxic burden and triggers</li>
                                        <li><strong>Genetic predisposition analysis</strong> - Understanding susceptibility patterns</li>
                                        <li><strong>Root cause identification protocols</strong> - Systematic approach to underlying factors</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Root Cause Approach</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our functional medicine model identifies and addresses the underlying mechanisms of disease rather than merely suppressing symptoms.</p>
                                        <p>We utilize advanced testing to uncover biochemical imbalances, nutritional deficiencies, and physiological dysfunction.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Functional+Medicine+Approach", use_column_width=True)
                            
                        elif domain == "Integrative Health":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Integrative health combines evidence-based conventional medicine with complementary approaches that
                                    have substantial research support. Our protocols select the most appropriate interventions from multiple
                                    therapeutic systems.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Evidence-based complementary medicine</strong> - Utilizing validated non-conventional approaches</li>
                                        <li><strong>Mind-body intervention protocols</strong> - Structured approaches to psychophysiological regulation</li>
                                        <li><strong>Traditional healing system integration</strong> - Incorporating validated traditional approaches</li>
                                        <li><strong>Botanical medicine application</strong> - Evidence-supported phytotherapeutic interventions</li>
                                        <li><strong>Manual therapy coordination</strong> - Appropriate referral and integration of bodywork</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Multi-System Approach</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our integrative protocols combine the best of conventional medicine with evidence-supported complementary approaches.</p>
                                        <p>We maintain rigorous standards for inclusion of therapeutic modalities based on both research evidence and clinical utility.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Integrative+Health+Approach", use_column_width=True)
                            
                        elif domain == "Preventive Care":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Preventive care focuses on identifying early warning signs of dysfunction before disease manifestation.
                                    Our approach utilizes advanced screening protocols and risk assessment algorithms to detect subclinical imbalances.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Predictive biomarker monitoring</strong> - Tracking early indicators of physiological shift</li>
                                        <li><strong>Precision risk assessment</strong> - Personalized evaluation of disease susceptibility</li>
                                        <li><strong>Subclinical dysfunction detection</strong> - Identifying imbalances before symptom development</li>
                                        <li><strong>Targeted prevention protocols</strong> - Specific interventions based on risk profile</li>
                                        <li><strong>Resilience enhancement strategies</strong> - Building physiological and psychological reserve</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Proactive Health Management</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our preventive approach identifies physiological imbalances before they progress to diagnosable disease states.</p>
                                        <p>We implement targeted interventions based on advanced biomarker patterns and comprehensive risk assessment.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Preventive+Care+Approach", use_column_width=True)
            
            with specialty_tabs[1]:
                st.markdown("""
                <h3 style="margin-bottom: 25px;">Additional Clinical Focus Areas</h3>
                <p style="margin-bottom: 30px;">
                    These specialized areas complement our primary approaches, providing comprehensive
                    support for complex health concerns and specific physiological systems.
                </p>
                """, unsafe_allow_html=True)
                
                # Create a grid layout for secondary domains with enhanced styling
                col1, col2 = st.columns(2)
                
                # First column
                with col1:
                    for domain in dr_jackson.secondary_domains[:3]:
                        with st.container():
                            st.markdown(f"""
                            <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid var(--light-border);">
                                <h3 style="margin-top: 0;">{domain}</h3>
                                <div class="professional-separator"></div>
                            """, unsafe_allow_html=True)
                            
                            if domain == "Nutritional Medicine":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Nutritional medicine utilizes targeted dietary interventions and therapeutic supplementation
                                    based on individual biochemical assessment. Our protocols address specific nutritional imbalances
                                    identified through comprehensive testing.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>Targeted micronutrient repletion</li>
                                        <li>Therapeutic elimination protocols</li>
                                        <li>Metabolic optimization strategies</li>
                                        <li>Personalized dietary planning</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            elif domain == "Stress Management":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Our approach to stress management includes physiological assessment of HPA axis function
                                    alongside evidence-based cognitive and somatic interventions to restore stress response regulation.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>HPA axis regulation protocols</li>
                                        <li>Neuroendocrine rebalancing</li>
                                        <li>Autonomic nervous system restoration</li>
                                        <li>Cognitive-behavioral interventions</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            elif domain == "Hormonal Balance":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Hormonal balance focuses on the complex interrelationships between endocrine systems.
                                    Our protocols assess steroid hormone cascades, thyroid function, and insulin dynamics
                                    to restore optimal regulatory patterns.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>Comprehensive hormone assessment</li>
                                        <li>Thyroid optimization protocols</li>
                                        <li>Adrenal function restoration</li>
                                        <li>Metabolic hormone regulation</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("""
                            </div>
                            """, unsafe_allow_html=True)
                
                # Second column
                with col2:
                    for domain in dr_jackson.secondary_domains[3:]:
                        with st.container():
                            st.markdown(f"""
                            <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid var(--light-border);">
                                <h3 style="margin-top: 0;">{domain}</h3>
                                <div class="professional-separator"></div>
                            """, unsafe_allow_html                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 2 of 3: Medical Information</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced medical privacy notice
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                <h4 style="color: var(--info-color); margin-top: 0;">Medical Information Privacy</h4>
                <p>Your medical history is protected under HIPAA guidelines and will only be used to provide appropriate clinical care.</p>
                <p style="margin-bottom: 0; font-size: 0.9rem;">This information helps us develop a comprehensive understanding of your health status and will not be shared without your explicit consent.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get the current medical info from session state
            medical_info = st.session_state['patient_medical_info']
            
            # Enhanced form with better visual organization
            with st.form("medical_history_form"):
                # Primary care physician
                st.markdown("<h3 style='margin-top: 0; margin-bottom: 20px;'>Healthcare Provider Information</h3>", unsafe_allow_html=True)
                
                primary_care = st.text_input("Primary Care Physician", 
                                          value=medical_info.primary_care_physician,
                                          placeholder="Name of your current primary care provider")
                
                # Medication information with enhanced styling
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Current Medications</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please list all medications, supplements, and vitamins you are currently taking, including dosage if known.
                </p>
                """, unsafe_allow_html=True)
                
                medications_text = st.text_area(
                    "One medication per line (include dosage if known)", 
                    value="\n".join(medical_info.current_medications) if medical_info.current_medications else "",
                    height=120,
                    placeholder="Example:\nMetformin 500mg twice daily\nVitamin D3 2000 IU daily\nOmega-3 Fish Oil 1000mg daily"
                )
                
                # Allergies with better organization
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Allergies</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    List all known allergies including medications, foods, and environmental triggers. Include reaction type if known.
                </p>
                """, unsafe_allow_html=True)
                
                allergies_text = st.text_area(
                    "Please list all allergies (medications, foods, environmental)", 
                    value="\n".join(medical_info.allergies) if medical_info.allergies else "",
                    height=100,
                    placeholder="Example:\nPenicillin - rash and hives\nPeanuts - anaphylaxis\nPollen - seasonal rhinitis"
                )
                
                # Medical conditions with better visual organization
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Chronic Medical Conditions</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please list all diagnosed medical conditions including approximate date of diagnosis.
                </p>
                """, unsafe_allow_html=True)
                
                conditions_text = st.text_area(
                    "Please list all diagnosed medical conditions", 
                    value="\n".join(medical_info.chronic_conditions) if medical_info.chronic_conditions else "",
                    height=100,
                    placeholder="Example:\nHypertension - diagnosed 2018\nType 2 Diabetes - diagnosed 2020\nMigraine - diagnosed 2015"
                )
                
                # Surgical history with improved styling
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Surgical History</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please list all previous surgeries with approximate dates.
                </p>
                """, unsafe_allow_html=True)
                
                surgeries_text = st.text_area(
                    "Please list all previous surgeries with approximate dates", 
                    value="\n".join(medical_info.past_surgeries) if medical_info.past_surgeries else "",
                    height=100,
                    placeholder="Example:\nAppendectomy - 2010\nKnee arthroscopy - 2019\nTonsillectomy - childhood"
                )
                
                # Family medical history with better visual organization
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Family Medical History</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please indicate any significant family medical history, specifying the relationship to you.
                </p>
                """, unsafe_allow_html=True)
                
                # Use a more structured approach for family history
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
                            value=value,
                            placeholder=f"e.g., Father, Mother, Sibling"
                        )
                
                # Lifestyle section (added)
                st.markdown("""
                <h3 style='margin-top: 30px; margin-bottom: 15px;'>Lifestyle Information</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    This information helps us develop a more comprehensive understanding of your health status.
                </p>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.selectbox("Exercise Frequency", 
                                 options=["Select an option", "None", "Occasional (1-2 times/week)", 
                                          "Regular (3-4 times/week)", "Frequent (5+ times/week)"],
                                 index=0)
                    st.selectbox("Stress Level", 
                                 options=["Select an option", "Low", "Moderate", "High", "Very High"],
                                 index=0)
                with col2:
                    st.selectbox("Sleep Quality", 
                                 options=["Select an option", "Poor", "Fair", "Good", "Excellent"],
                                 index=0)
                    st.selectbox("Diet Quality", 
                                 options=["Select an option", "Poor", "Fair", "Good", "Excellent"],
                                 index=0)
                
                # Health goals section (added)
                st.markdown("""
                <h3 style='margin-top: 30px; margin-bottom: 15px;'>Health Goals</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please share your main health goals and what you hope to achieve through our care.
                </p>
                """, unsafe_allow_html=True)
                
                health_goals = st.text_area(
                    "Primary health objectives",
                    height=100,
                    placeholder="Example:\nImprove energy levels\nReduce chronic pain\nOptimize sleep quality\nAddress specific health concerns"
                )
                
                # Consent checkboxes with better styling
                st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
                history_consent = st.checkbox(
                    "I confirm that the information provided is accurate and complete to the best of my knowledge", 
                    value=True
                )
                sharing_consent = st.checkbox(
                    "I consent to the appropriate sharing of this information with healthcare providers involved in my care",
                    value=True
                )
                
                # Submit button with professional styling
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Save & Continue", use_container_width=True)
                
                if submitted:
                    # Process and save the data
                    if not (history_consent and sharing_consent):
                        st.error("Please confirm both consent statements to proceed.")
                    else:
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
                        
                        # Success message with professional styling
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Medical History Saved</h4>
                            <p style="margin-bottom: 0;">Your medical history has been securely stored. Thank you for providing this comprehensive information, which will help us deliver personalized care.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Offer navigation to consultation with better styling
                        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                        if st.button("Proceed to Consultation →", use_container_width=True):
                            page = "Consultation"
                            st.experimental_rerun()
            
            # Professional note at bottom
            st.markdown("""
            <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Why We Collect This Information</h4>
                <p style="font-size: 0.9rem; margin-bottom: 0;">
                    Comprehensive medical history allows us to develop personalized care plans based on your unique health profile.
                    This information helps identify patterns, assess risk factors, and determine optimal treatment approaches
                    following evidence-based functional medicine principles.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Consultation":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Professional Consultation</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 3 of 3: Consultation Request</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Check if patient info is filled out
            patient_info = st.session_state['patient_contact_info']
            medical_info = st.session_state['patient_medical_info']
            
            if not patient_info.first_name or not patient_info.last_name:
                # Warning with enhanced styling
                st.markdown("""
                <div style="background-color: rgba(255, 190, 85, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--warning-color);">
                    <h4 style="color: var(--warning-color); margin-top: 0;">Patient Information Required</h4>
                    <p style="margin-bottom: 15px;">Please complete the Patient Intake form before proceeding to consultation.</p>
                """, unsafe_allow_html=True)
                
                if st.button("Go to Patient Intake →", use_container_width=True):
                    page = "Patient Intake"
                    st.experimental_rerun()
                    
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                # Patient information summary with professional styling
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; border: 1px solid var(--light-border); margin-bottom: 30px;">
                    <h3 style="margin-top: 0;">Patient Information Summary</h3>
                    <div class="professional-separator"></div>
                    
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 15px;">
                """, unsafe_allow_html=True)
                
                # Patient details
                st.markdown(f"""
                        <div style="flex: 1; min-width: 250px;">
                            <h4 style="margin-top: 0; font-size: 1rem;">Personal Information</h4>
                            <p style="margin: 5px 0;"><strong>Name:</strong> {patient_info.first_name} {patient_info.last_name}</p>
                            <p style="margin: 5px 0;"><strong>Date of Birth:</strong> {patient_info.date_of_birth}</p>
                            <p style="margin: 5px 0;"><strong>Email:</strong> {patient_info.email}</p>
                            <p style="margin: 5px 0;"><strong>Phone:</strong> {patient_info.phone}</p>
                        </div>
                """, unsafe_allow_html=True)
                
                # Medical summary
                medical_conditions = ", ".join(medical_info.chronic_conditions[:3]) if medical_info.chronic_conditions else "None reported"
                if len(medical_info.chronic_conditions) > 3:
                    medical_conditions += " (and others)"
                    
                medications = ", ".join(medical_info.current_medications[:3]) if medical_info.current_medications else "None reported"
                if len(medical_info.current_medications) > 3:
                    medications += " (and others)"
                    
                allergies = ", ".join(medical_info.allergies[:3]) if medical_info.allergies else "None reported"
                if len(medical_info.allergies) > 3:
                    allergies += " (and others)"
                
                st.markdown(f"""
                        <div style="flex: 1; min-width: 250px;">
                            <h4 style="margin-top: 0; font-size: 1rem;">Medical Summary</h4>
                            <p style="margin: 5px 0;"><strong>Conditions:</strong> {medical_conditions}</p>
                            <p style="margin: 5px 0;"><strong>Medications:</strong> {medications}</p>
                            <p style="margin: 5px 0;"><strong>Allergies:</strong> {allergies}</p>
                            <p style="margin: 5px 0;"><strong>PCP:</strong> {medical_info.primary_care_physician or "Not provided"}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # HIPAA notice with enhanced styling
                st.markdown("""
                <div style="background-color: rgba(90, 160, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                    <h4 style="color: var(--info-color); margin-top: 0;">Consultation Privacy</h4>
                    <p style="margin-bottom: 0;">This consultation is protected under HIPAA guidelines. Information shared during this session is confidential and will be securely stored in your electronic medical record.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced consultation form
                with st.form("consultation_form"):
                    st.markdown("""
                    <h3 style="margin-top: 0; margin-bottom: 20px;">Consultation Request</h3>
                    """, unsafe_allow_html=True)
                    
                    # Primary reason with better styling
                    st.markdown("""
                    <h4 style="margin-bottom: 15px;">Primary Health Concern</h4>
                    <p style="margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);">
                        Please describe your current health concerns in detail. Include symptom duration, severity, and any patterns you've noticed.
                    </p>
                    """, unsafe_allow_html=True)
                    
                    primary_concern = st.text_area(
                        "Health concern description",
                        height=150,
                        placeholder="Please provide a detailed description of your main health concerns...",
                        help="Include symptom duration, severity, and any patterns you've noticed"
                    )
                    
                    # Specialty selection with better organization
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Clinical Focus Area</h4>
                    <p style="margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);">
                        Select the specialty area most relevant to your health concerns.
                    </p>
                    """, unsafe_allow_html=True)
                    
                    specialty_area = st.selectbox(
                        "Select the most relevant specialty area", 
                        options=dr_jackson.primary_domains + dr_jackson.secondary_domains
                    )
                    
                    # Symptom details with better visual organization
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Symptom Details</h4>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        symptom_onset = st.date_input(
                            "When did you first notice these symptoms?",
                            value=datetime.datetime.now().date() - datetime.timedelta(days=30),
                            help="Select the approximate date when symptoms first appeared"
                        )
                    with col2:
                        severity = st.select_slider(
                            "Rate the severity of your symptoms",
                            options=["Mild", "Moderate", "Significant", "Severe", "Extreme"],
                            help="Indicate the overall intensity of your symptoms"
                        )
                    
                    # Additional context with better layout
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Additional Context</h4>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        prior_treatments = st.text_area(
                            "Prior treatments or approaches tried",
                            height=120,
                            placeholder="List any treatments, medications, or approaches you've already attempted..."
                        )
                    with col2:
                        triggers = st.text_area(
                            "Known triggers or patterns",
                            height=120,
                            placeholder="Describe any factors that worsen or improve your symptoms..."
                        )
                    
                    # Goals with better styling
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Treatment Goals</h4>
                    <p style="margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);">
                        What outcomes are you hoping to achieve through this consultation?
                    </p>
                    """, unsafe_allow_html=True)
                    
                    goals = st.text_area(
                        "Desired outcomes",
                        height=120,
                        placeholder="Describe your health goals and expectations from this consultation..."
                    )
                    
                    # Appointment preference (added)
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Appointment Preference</h4>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        appointment_type = st.radio(
                            "Preferred consultation type",
                            options=["Virtual (Telehealth)", "In-person Office Visit"],
                            index=0
                        )
                    with col2:
                        urgency = st.select_slider(
                            "Consultation urgency",
                            options=["Standard (within 2 weeks)", "Priority (within 1 week)", "Urgent (within 48 hours)"],
                            value="Standard (within 2 weeks)"
                        )
                    
                    # Enhanced consent checkbox
                    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
                    consultation_consent = st.checkbox(
                        "I understand that this consultation request will be reviewed by Dr. Jackson, and follow-up may be required before treatment recommendations are provided",
                        value=True
                    )
                    
                    # Submit button with better styling
                    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                    submitted = st.form_submit_button("Submit Consultation Request", use_container_width=True)
                
                # Form handling logic
                if submitted:
                    if not primary_concern:
                        st.error("Please describe your health concerns before submitting.")
                    elif not consultation_consent:
                        st.error("Please confirm your understanding of the consultation process.")
                    else:
                        # Success message with professional styling
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Consultation Request Submitted</h4>
                            <p style="margin-bottom: 10px;">Your request has been successfully received and will be reviewed by Dr. Jackson.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display a professional response using the persona
                        st.markdown("""
                        <div style="background-color: var(--off-white); padding: 25px; border-radius: 10px; border: 1px solid var(--light-border); margin-top: 30px;">
                            <h3 style="margin-top: 0;">Initial Assessment</h3>
                            <div class="professional-separator"></div>
                        """, unsafe_allow_html=True)
                        
                        # Determine appropriate recommendations based on specialty area
                        if specialty_area in dr_jackson.primary_domains[:3]:  # First 3 primary domains
                            recommendations = [
                                "Schedule a comprehensive initial evaluation",
                                "Complete the detailed symptom assessment questionnaire",
                                "Prepare any prior lab work or diagnostic studies for review",
                                "Consider keeping a symptom journal for the next 7 days"
                            ]
                        else:
                            recommendations = [
                                "Schedule an initial consultation",
                                "Gather relevant medical records and previous test results",
                                "Complete preliminary health assessment questionnaires",
                                "Prepare a list of specific questions for your consultation"
                            ]
                        
                        # Use the persona to format the response with better styling
                        assessment = f"Based on your initial information regarding {specialty_area.lower()} concerns of {severity.lower()} severity, a professional evaluation is indicated. Your symptoms beginning approximately {(datetime.datetime.now().date() - symptom_onset).days} days ago warrant a thorough assessment."
                        
                        st.markdown(f"""
                            <div style="margin-bottom: 20px;">
                                <h4 style="margin-bottom: 10px; font-size: 1.1rem;">Clinical Overview</h4>
                                <p style="margin-bottom: 5px;"><strong>Presenting Concerns:</strong> {specialty_area} issues with {severity.lower()} symptoms</p>
                                <p style="margin-bottom: 5px;"><strong>Duration:</strong> Approximately {(datetime.datetime.now().date() - symptom_onset).days} days</p>
                                <p style="margin-bottom: 5px;"><strong>Requested Format:</strong> {appointment_type}</p>
                                <p><strong>Urgency Level:</strong> {urgency}</p>
                            </div>
                            
                            <div style="margin-bottom: 20px;">
                                <h4 style="margin-bottom: 10px; font-size: 1.1rem;">Professional Assessment</h4>
                                <p>{assessment}</p>
                            </div>
                            
                            <div>
                                <h4 style="margin-bottom: 10px; font-size: 1.1rem;">Recommendations</h4>
                                <ul>
                        """, unsafe_allow_html=True)
                        
                        for rec in recommendations:
                            st.markdown(f"""
                                <li style="margin-bottom: 8px;">{rec}</li>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("""
                                </ul>
                            </div>
                            
                            <p style="margin-top: 20px; font-style: italic;">Please confirm your understanding of these recommendations and your intent to proceed with the next steps.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Next steps with professional styling
                        st.markdown("""
                        <div style="margin-top: 30px;">
                            <h3>Next Steps</h3>
                            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-top: 15px;">
                                <p style="margin: 0;">You will receive a detailed follow-up within 24-48 hours with additional instructions and appointment scheduling options.</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # AI-assisted note section with professional styling
                        if st.session_state.get('anthropic_api_key') or st.session_state.get('openai_api_key'):
                            st.markdown("""
                            <div style="margin-top: 40px;">
                                <h3>AI-Assisted Clinical Notes</h3>
                                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; border: 1px solid var(--light-border); margin-top: 15px;">
                            """, unsafe_allow_html=True)
                            
                            with st.spinner("Generating preliminary clinical notes..."):
                                # This would normally call an LLM API
                                time.sleep(2)  # Simulate processing time
                                
                                st.markdown("""
                                    <h4 style="margin-top: 0; color: var(--primary-color);">PRELIMINARY ASSESSMENT NOTE</h4>
                                    <p style="margin-bottom: 15px;">
                                        Patient presents with concerns related to the selected specialty area. 
                                        Initial impression suggests further evaluation is warranted to establish 
                                        a differential diagnosis and treatment approach. Patient goals and symptom 
                                        presentation will be incorporated into the comprehensive care plan.
                                    </p>
                                    <p style="font-style: italic; font-size: 0.9rem; margin-bottom: 0; color: var(--dark-gray);">
                                        This preliminary note was generated with AI assistance and will be 
                                        reviewed by Dr. Jackson prior to formal documentation.
                                    </p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Additional guidance at bottom of page
                st.markdown("""
                <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0;">What to Expect</h4>
                    <p style="font-size: 0.9rem; margin-bottom: 0;">
                        After submitting your consultation request, our clinical team will review your information and 
                        reach out to schedule your appointment. For urgent medical concerns requiring immediate attention, 
                        please contact your primary care provider or visit the nearest emergency department.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        elif page == "Chat with Dr. Jackson":
            # Professional header
            st.markdown("""
            <h1>Professional Chat Consultation</h1>
            <div class="professional-separator" style="width: 150px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
                
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--tertiary-color);
        font-weight: 500;
    }
    
    /* Alert/Notice Styling */
    .info-box {
        background-color: rgba(90, 160, 255, 0.1);
        border-left: 4px solid var(--info-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .success-box {
        background-color: rgba(61, 201, 161, 0.1);
        border-left: 4px solid var(--success-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .warning-box {
        background-color: rgba(255, 190, 85, 0.1);
        border-left: 4px solid var(--warning-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .error-box {
        background-color: rgba(255, 90, 90, 0.1);
        border-left: 4px solid var(--error-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    /* Progress Bar Styling */
    [data-testid="stProgressBar"] > div {
        background-color: var(--primary-color);
        height: 8px;
        border-radius: 4px;
    }
    
    [data-testid="stProgressBar"] > div:nth-child(1) {
        background-color: var(--light-gray);
    }
    
    /* Section Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            rgba(0,0,0,0), 
            var(--medium-gray), 
            rgba(0,0,0,0));
    }
    
    .dark-mode hr {
        background: linear-gradient(90deg, 
            rgba(0,0,0,0), 
            var(--dark-border), 
            rgba(0,0,0,0));
    }
    
    /* Info Cards Grid */
    .info-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 16px;
        margin: 20px 0;
    }
    
    .info-card {
        background-color: var(--off-white);
        border-radius: 8px;
        border: 1px solid var(--light-border);
        padding: 20px;
        transition: all 0.2s ease;
    }
    
    .info-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    .dark-mode .info-card {
        background-color: var(--dark-mode-card);
        border: 1px solid var(--dark-border);
    }
    
    .dark-mode .info-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Custom Utility Classes */
    .text-center {
        text-align: center;
    }
    
    .mb-0 {
        margin-bottom: 0 !important;
    }
    
    .mt-0 {
        margin-top: 0 !important;
    }
    
    .professional-separator {
        height: 5px;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        margin: 12px 0;
        border-radius: 3px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional App Header with Logo
    st.markdown(f"""
    <div class="professional-header">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h1>Dr. Jackson, {dr_jackson.credentials}</h1>
                <p>{dr_jackson.practice_name}</p>
            </div>
            <div style="text-align: right;">
                <p style="font-size: 0.9rem; opacity: 0.8;">Advancing Integrative Medicine</p>
                <p style="font-size: 0.8rem; opacity: 0.7;">Established 2015</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Professionally designed sidebar
    with st.sidebar:
        # Add a subtle medical/professional icon or logo
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); 
                       width: 60px; height: 60px; border-radius: 50%; display: inline-flex; 
                       align-items: center; justify-content: center; margin-bottom: 10px;">
                <span style="color: white; font-size: 30px;">🩺</span>
            </div>
            <p style="font-weight: 600; margin: 0; font-size: 16px;">Dr. Jackson Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='margin-top: 0;'>Navigation</h3>", unsafe_allow_html=True)
        
        # Enhanced navigation with section grouping
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; color: var(--dark-gray);'>Patient Portal</p>", unsafe_allow_html=True)
        patient_page = st.radio("", [
            "Home", 
            "Patient Intake", 
            "Medical History",
            "Consultation"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>Communication</p>", unsafe_allow_html=True)
        communication_page = st.radio("", [
            "Chat with Dr. Jackson"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>Information</p>", unsafe_allow_html=True)
        info_page = st.radio("", [
            "Specialties", 
            "Approach",
            "Resources"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>System</p>", unsafe_allow_html=True)
        system_page = st.radio("", [
            "Settings"
        ], label_visibility="collapsed")
        
        # Determine selected page from all radio groups
        if patient_page != "Home":
            page = patient_page
        elif communication_page != "Chat with Dr. Jackson":
            page = "Chat with Dr. Jackson"
        elif info_page != "Specialties":
            page = info_page
        elif system_page != "Settings":
            page = system_page
        else:
            page = "Home"
        
        # Theme selection with better design
        st.markdown("---")
        st.markdown("<h4 style='margin-bottom: 10px;'>Appearance</h4>", unsafe_allow_html=True)
        theme_cols = st.columns([1, 3])
        with theme_cols[0]:
            st.markdown("🎨")
        with theme_cols[1]:
            theme = st.selectbox("", ["Light", "Dark"], label_visibility="collapsed")
        
        if theme == "Dark":
            st.markdown("""
            <script>
                document.body.classList.add('dark-mode');
            </script>
            """, unsafe_allow_html=True)
        
        # Professional info section
        st.markdown("---")
        st.markdown("<h4 style='margin-bottom: 10px;'>About Dr. Jackson</h4>", unsafe_allow_html=True)
        
        # More professional specialty display
        domains = ", ".join(dr_jackson.primary_domains[:3])
        st.markdown(f"""
        <div style="background-color: var(--off-white); padding: 12px; border-radius: 8px; border: 1px solid var(--light-border); margin-bottom: 15px;">
            <p style="font-weight: 500; margin-bottom: 5px;">Specializing in:</p>
            <p style="color: var(--primary-color); font-weight: 600; margin: 0;">{domains}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Current date - maintaining professional approach
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background-color: var(--primary-color); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                <span style="color: white;">📅</span>
            </div>
            <div>
                <p style="font-size: 0.85rem; margin: 0; opacity: 0.7;">Today's Date</p>
                <p style="font-weight: 500; margin: 0;">{current_date}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show logged in status if patient info exists
        patient_info = st.session_state['patient_contact_info']
        if patient_info.first_name and patient_info.last_name:
            st.markdown(f"""
            <div style="background-color: rgba(61, 201, 161, 0.1); border-left: 4px solid var(--success-color); padding: 12px; border-radius: 6px;">
                <p style="font-weight: 500; margin: 0;">Logged in as:</p>
                <p style="margin: 5px 0 0 0;">{patient_info.first_name} {patient_info.last_name}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Container for main content with professional layout
    main_container = st.container()
    with main_container:
        # Main content area based on page selection
        if page == "Home":
            st.header("Welcome to Dr. Jackson's Professional Consultation")
            
            # Enhanced HIPAA Notice with more professional design
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; 
                       border-left: 5px solid var(--info-color); margin-bottom: 30px;">
                <h4 style="color: var(--info-color); margin-top: 0;">HIPAA Compliance Notice</h4>
                <p style="margin-bottom: 10px;">This application complies with the Health Insurance Portability and Accountability Act (HIPAA) of 1996:</p>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                    <li style="margin-bottom: 5px;">All patient data is encrypted in transit and at rest</li>
                    <li style="margin-bottom: 5px;">Access controls restrict unauthorized viewing of protected health information (PHI)</li>
                    <li style="margin-bottom: 5px;">Audit logs track all data access and modifications</li>
                    <li style="margin-bottom: 5px;">Data retention policies comply with medical record requirements</li>
                    <li style="margin-bottom: 5px;">Regular security assessments are conducted to ensure compliance</li>
                </ul>
                <p style="margin-top: 10px; margin-bottom: 0; font-weight: 500;"><span style="color: var(--info-color);">Privacy Officer Contact:</span> privacy@optimumwellness.org</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Featured specialties in cards layout
            st.markdown("### Our Clinical Specialties")
            st.markdown("""
            <p style="margin-bottom: 25px;">Dr. Jackson's practice provides comprehensive medical consultation with expertise in the following areas:</p>
            """, unsafe_allow_html=True)
            
            # Create a grid layout with cards for specialties
            st.markdown("""
            <div class="info-card-grid">
            """, unsafe_allow_html=True)
            
            for domain in dr_jackson.primary_domains:
                icon = "🧠" if domain == "Psychiatric Care" else "✨" if domain == "Wellness Optimization" else "⏱️" if domain == "Anti-aging Medicine" else "🔬" if domain == "Functional Medicine" else "🌿" if domain == "Integrative Health" else "🛡️"
                
                st.markdown(f"""
                <div class="info-card">
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                            <span style="font-size: 20px;">{icon}</span>
                        </div>
                        <h4 style="margin: 0; color: var(--primary-color);">{domain}</h4>
                    </div>
                    <div class="professional-separator"></div>
                    <p style="margin-top: 10px; font-size: 0.9rem;">Comprehensive, evidence-based approach to {domain.lower()} through integrated assessment and personalized protocols.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Professional approach section with better design
            st.markdown("### Professional Approach")
            
            # Two-column layout for approach and values
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 12px; border: 1px solid var(--light-border); height: 100%;">
                    <h4 style="margin-top: 0;">Clinical Methodology</h4>
                    <div class="professional-separator"></div>
                    <p>Dr. Jackson's practice is built on a hierarchical approach to medical knowledge and evidence:</p>
                    <ul>
                        <li><strong>Evidence-based research</strong> forms the foundation of all clinical decisions</li>
                        <li><strong>Clinical guidelines</strong> provide standardized frameworks for treatment protocols</li>
                        <li><strong>Professional experience</strong> guides the application of research to individual cases</li>
                        <li><strong>Holistic assessment</strong> ensures comprehensive evaluation of all contributing factors</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 12px; border: 1px solid var(--light-border); height: 100%;">
                    <h4 style="margin-top: 0;">Core Values</h4>
                    <div class="professional-separator"></div>
                    <ul>
                """, unsafe_allow_html=True)
                
                for i, value in enumerate(dr_jackson.core_values[:4]):
                    st.markdown(f"""
                    <li style="margin-bottom: 10px;">
                        <strong style="color: var(--primary-color);">{value}:</strong> 
                        Ensuring the highest standards of care through rigorous application of professional principles
                    </li>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Call to action section with enhanced design
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Begin Your Care Journey</h3>
            <div style="background: linear-gradient(135deg, rgba(93, 92, 222, 0.1) 0%, rgba(93, 92, 222, 0.05) 100%); 
                 padding: 30px; border-radius: 12px; margin-bottom: 30px; border: 1px solid rgba(93, 92, 222, 0.2);">
                <p style="font-size: 1.1rem; margin-bottom: 20px;">
                    To begin the consultation process, please complete the Patient Intake forms first. This will help us provide
                    the most appropriate clinical guidance tailored to your specific health needs.
                </p>
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("📋 Go to Patient Intake", key="home_intake_btn"):
                page = "Patient Intake"
                st.experimental_rerun()
                
            st.markdown("""
                    </div>
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("🔍 Learn About Specialties", key="home_specialties_btn"):
                page = "Specialties"
                st.experimental_rerun()
                
            st.markdown("""
                    </div>
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("💬 Chat with Dr. Jackson", key="home_chat_btn"):
                page = "Chat with Dr. Jackson"
                st.experimental_rerun()
            
            st.markdown("""
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Testimonials or professional credentials section
            st.markdown("""
            <div style="background-color: var(--off-white); padding: 25px; border-radius: 12px; border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Professional Credentials</h4>
                <div class="professional-separator"></div>
                <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 15px;">
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">🎓</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Education</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Doctorate in Nursing Practice</p>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">📜</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Certification</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Family Nurse Practitioner-Certified</p>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">🔬</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Specialization</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Certified Functional Medicine Practitioner</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Patient Intake":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Patient Intake Form</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 1 of 3: Contact Information</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced data privacy notice
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                <h4 style="color: var(--info-color); margin-top: 0;">Data Privacy Notice</h4>
                <p>All information submitted is encrypted and protected in accordance with HIPAA regulations.
                Your privacy is our priority. Information is only accessible to authorized medical personnel.</p>
                <p style="margin-bottom: 0; font-size: 0.9rem;"><strong>Security Measures:</strong> End-to-end encryption, secure database storage, access control mechanisms</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get the current patient info from session state
            patient_info = st.session_state['patient_contact_info']
            
            # Create the form with enhanced styling
            with st.form("patient_contact_form"):
                st.markdown("""
                <h3 style="margin-top: 0; margin-bottom: 20px;">Personal Information</h3>
                """, unsafe_allow_html=True)
                
                # Name information with professional layout
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name*", value=patient_info.first_name,
                                            placeholder="Enter your legal first name")
                with col2:
                    last_name = st.text_input("Last Name*", value=patient_info.last_name,
                                          placeholder="Enter your legal last name")
                
                # Contact information with more structured layout
                st.markdown("<h4 style='margin-top: 25px; margin-bottom: 15px;'>Contact Details</h4>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2,2,1])
                with col1:
                    email = st.text_input("Email Address*", value=patient_info.email,
                                        placeholder="Your primary email address")
                with col2:
                    phone = st.text_input("Phone Number*", value=patient_info.phone,
                                        placeholder="Format: (XXX) XXX-XXXX")
                with col3:
                    dob = st.date_input("Date of Birth*", 
                                    value=patient_info.date_of_birth or datetime.datetime.now().date() - datetime.timedelta(days=365*30),
                                    help="Select your date of birth from the calendar")
                
                # Address information with better visual grouping
                st.markdown("<h4 style='margin-top: 25px; margin-bottom: 15px;'>Address Information</h4>", unsafe_allow_html=True)
                
                st.text_input("Street Address", value=patient_info.address,
                            placeholder="Enter your current street address")
                
                col1, col2, col3 = st.columns([2,1,1])
                with col1:
                    city = st.text_input("City", value=patient_info.city,
                                      placeholder="Your city of residence")
                with col2:
                    state = st.text_input("State", value=patient_info.state,
                                       placeholder="State abbreviation")
                with col3:
                    zip_code = st.text_input("ZIP Code", value=patient_info.zip_code,
                                          placeholder="5-digit ZIP code")
                
                # Emergency contact with visual separation
                st.markdown("""
                <h4 style='margin-top: 25px; margin-bottom: 15px;'>Emergency Contact</h4>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please provide a contact person in case of emergency.
                </p>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    emergency_name = st.text_input("Emergency Contact Name", 
                                                value=patient_info.emergency_contact_name,
                                                placeholder="Full name of emergency contact")
                with col2:
                    emergency_phone = st.text_input("Emergency Contact Phone", 
                                                 value=patient_info.emergency_contact_phone,
                                                 placeholder="Emergency contact's phone number")
                
                # Required fields notice
                st.markdown("""
                <p style='margin-top: 25px; font-size: 0.9rem;'>* Required fields</p>
                """, unsafe_allow_html=True)
                
                # Enhanced consent checkbox
                consent = st.checkbox("I confirm that the information provided is accurate and complete to the best of my knowledge",
                                   value=True)
                
                # Submit button with professional styling
                submitted = st.form_submit_button("Save & Continue")
                
                if submitted:
                    # Validate required fields
                    if not (first_name and last_name and email and phone and dob and consent):
                        st.error("Please fill out all required fields and confirm your consent.")
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
                        
                        # Success message with more professional design
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Information Saved Successfully</h4>
                            <p style="margin-bottom: 0;">Your contact information has been securely stored. Please proceed to the Medical History form.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Offer navigation to next form
                        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                        if st.button("Continue to Medical History →", use_container_width=True):
                            page = "Medical History"
                            st.experimental_rerun()
            
            # Professional guidance note at the bottom
            st.markdown("""
            <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Privacy & Security</h4>
                <p style="margin-bottom: 0; font-size: 0.9rem;">
                    All information provided is protected by our privacy policy and HIPAA regulations. Your data is encrypted and access is restricted
                    to authorized healthcare professionals involved in your care. For questions about our privacy practices,
                    please contact our Privacy Officer at privacy@optimumwellness.org.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Medical History":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Medical History Form</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: import streamlit as st
from typing import Dict, List, Union, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import datetime
import random
import time
import json

# Define core persona elements as structured data
class PriorityLevel(Enum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

@dataclass
class ResponseFormat:
    steps: List[str]
    style: Dict[str, str]

@dataclass
class ChatMessage:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

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
        
        # Chat responses for various medical topics
        self.chat_responses = {
            "wellness": [
                "In our clinical approach to wellness optimization, we emphasize the integration of evidence-based lifestyle modifications with targeted interventions. The foundation begins with comprehensive assessment of metabolic, hormonal, and inflammatory markers.",
                "From a functional medicine perspective, wellness requires addressing root causes rather than symptom suppression. Our protocol typically evaluates sleep quality, nutritional status, stress management, and physical activity patterns as foundational elements.",
                "The current medical literature supports a multifaceted approach to wellness. This includes structured nutritional protocols, strategic supplementation based on identified deficiencies, and cognitive-behavioral interventions for stress management."
            ],
            "nutrition": [
                "Nutritional medicine forms a cornerstone of our functional approach. Current research indicates that personalized nutrition based on metabolic typing and inflammatory markers yields superior outcomes compared to generalized dietary recommendations.",
                "In our clinical practice, we utilize advanced nutritional assessments including micronutrient testing, food sensitivity panels, and metabolic markers to develop precision nutritional protocols tailored to individual biochemistry.",
                "The evidence supports targeted nutritional interventions rather than generalized approaches. We typically begin with elimination of inflammatory triggers, followed by structured reintroduction to identify optimal nutritional parameters."
            ],
            "sleep": [
                "Sleep optimization is fundamental to our clinical approach. Current research demonstrates that disrupted sleep architecture significantly impacts hormonal regulation, inflammatory markers, and cognitive function.",
                "Our protocol for sleep enhancement includes comprehensive assessment of circadian rhythm disruptions, evaluation of potential obstructive patterns, and analysis of neurochemical imbalances that may interfere with normal sleep progression.",
                "Evidence-based interventions for sleep quality improvement include structured sleep hygiene protocols, environmental optimization, and when indicated, targeted supplementation to address specific neurotransmitter imbalances."
            ],
            "stress": [
                "From a functional medicine perspective, chronic stress activation represents a significant driver of inflammatory processes and hormonal dysregulation. Our approach focuses on quantifiable assessment of HPA axis function.",
                "The clinical literature supports a structured approach to stress management, incorporating both physiological and psychological interventions. We utilize validated assessment tools to measure stress response patterns.",
                "Our protocol typically includes targeted adaptogenic support, structured cognitive reframing techniques, and autonomic nervous system regulation practices, all customized based on individual response patterns."
            ],
            "aging": [
                "Anti-aging medicine is approached from a scientific perspective in our practice. The focus remains on measurable biomarkers of cellular health, including telomere dynamics, oxidative stress parameters, and glycation endpoints.",
                "Current research supports interventions targeting specific aging mechanisms rather than general approaches. Our protocol evaluates mitochondrial function, inflammatory status, and hormonal optimization within physiological parameters.",
                "The evidence demonstrates that targeted interventions for biological age reduction must be personalized. We utilize comprehensive biomarker assessment to develop precision protocols for cellular rejuvenation."
            ],
            "hormones": [
                "Hormonal balance requires a comprehensive systems-based approach. Current clinical research indicates that evaluating the full spectrum of endocrine markers yields superior outcomes compared to isolated hormone assessment.",
                "Our protocol includes evaluation of steroid hormone pathways, thyroid function, and insulin dynamics. The integration of these systems provides a more accurate clinical picture than isolated assessment.",
                "Evidence-based hormonal optimization focuses on restoration of physiological patterns rather than simple supplementation. We utilize chronobiological principles to restore natural hormonal rhythms."
            ],
            "inflammation": [
                "Chronic inflammation represents a common pathway in numerous pathological processes. Our clinical approach includes comprehensive assessment of inflammatory markers and mediators to identify specific activation patterns.",
                "The research supports targeted anti-inflammatory protocols based on identified triggers rather than generalized approaches. We evaluate environmental, nutritional, and microbial factors in our assessment.",
                "Our evidence-based protocol typically includes elimination of inflammatory triggers, gastrointestinal barrier restoration, and targeted nutritional interventions to modulate specific inflammatory pathways."
            ],
            "detoxification": [
                "Detoxification capacity represents a critical element in our functional medicine assessment. We evaluate phase I and phase II detoxification pathways through validated biomarkers rather than generalized assumptions.",
                "The clinical evidence supports structured protocols for enhancing physiological detoxification processes. Our approach includes assessment of toxic burden alongside metabolic detoxification capacity.",
                "Our protocol typically includes strategic nutritional support for specific detoxification pathways, reduction of exposure sources, and enhancement of elimination mechanisms through validated clinical interventions."
            ],
            "gut_health": [
                "Gastrointestinal function serves as a cornerstone in our clinical assessment. Current research demonstrates the central role of gut integrity, microbiome diversity, and digestive efficiency in systemic health outcomes.",
                "Our protocol includes comprehensive evaluation of digestive function, intestinal permeability, microbial balance, and immunological markers to develop precision interventions for gastrointestinal optimization.",
                "The evidence supports a structured approach to gastrointestinal restoration, including targeted elimination of pathogenic factors, reestablishment of beneficial microbial communities, and restoration of mucosal integrity."
            ],
            "default": [
                "I would need to conduct a more thorough clinical assessment to provide specific recommendations regarding your inquiry. Our practice emphasizes evidence-based approaches customized to individual patient presentations.",
                "From a functional medicine perspective, addressing your concerns would require comprehensive evaluation of relevant biomarkers and clinical parameters. This allows for development of targeted interventions based on identified mechanisms.",
                "The current medical literature supports an individualized approach to your clinical question. Our protocol would include assessment of relevant systems followed by development of a structured intervention strategy."
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
    
    def get_chat_response(self, query: str) -> str:
        """Generates a chat response based on the query content"""
        # Determine the topic based on keywords in the query
        query_lower = query.lower()
        
        # Check for topic matches
        if any(word in query_lower for word in ["wellness", "well-being", "wellbeing", "health optimization"]):
            responses = self.chat_responses["wellness"]
        elif any(word in query_lower for word in ["nutrition", "diet", "food", "eating"]):
            responses = self.chat_responses["nutrition"]
        elif any(word in query_lower for word in ["sleep", "insomnia", "rest", "fatigue"]):
            responses = self.chat_responses["sleep"]
        elif any(word in query_lower for word in ["stress", "anxiety", "overwhelm", "burnout"]):
            responses = self.chat_responses["stress"]
        elif any(word in query_lower for word in ["aging", "longevity", "anti-aging"]):
            responses = self.chat_responses["aging"]
        elif any(word in query_lower for word in ["hormone", "thyroid", "estrogen", "testosterone"]):
            responses = self.chat_responses["hormones"]
        elif any(word in query_lower for word in ["inflammation", "inflammatory", "autoimmune"]):
            responses = self.chat_responses["inflammation"]
        elif any(word in query_lower for word in ["detox", "toxin", "cleanse"]):
            responses = self.chat_responses["detoxification"]
        elif any(word in query_lower for word in ["gut", "digestive", "stomach", "intestine", "microbiome"]):
            responses = self.chat_responses["gut_health"]
        else:
            responses = self.chat_responses["default"]
        
        # Select a response from the appropriate category
        return random.choice(responses)

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

def display_chat_message(message: ChatMessage):
    """Display a single chat message with appropriate styling"""
    if message.role == "assistant":
        with st.chat_message("assistant", avatar="🩺"):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%I:%M %p')}")
    else:  # user message
        with st.chat_message("user"):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%I:%M %p')}")

# Function to get descriptions for DEI focus areas
def get_dei_description(focus):
    descriptions = {
        "Maintain awareness of healthcare disparities": "We actively monitor and address inequities in healthcare access, treatment, and outcomes across different populations.",
        "Provide culturally competent care": "Our approach incorporates cultural factors and beliefs that may impact health behaviors and treatment preferences.",
        "Consider LGBTQ+ health perspectives": "We acknowledge unique health concerns and create supportive care environments for LGBTQ+ individuals.",
        "Implement inclusive language": "Our communications use terminology that respects diversity of identity, experience, and background.",
        "Address systemic healthcare barriers": "We work to identify and minimize structural obstacles that prevent equitable access to quality care."
    }
    return descriptions.get(focus, "")

# Function to get descriptions for intervention hierarchy
def get_hierarchy_description(hierarchy):
    descriptions = {
        "Remove pathological triggers": "Identify and eliminate factors that activate or perpetuate dysfunction",
        "Restore physiological function": "Support normal biological processes through targeted interventions",
        "Rebalance regulatory systems": "Address control mechanisms that coordinate multiple physiological processes",
        "Regenerate compromised tissues": "Support cellular renewal and structural integrity where needed",
        "Reestablish health maintenance": "Implement sustainable strategies for ongoing wellbeing"
    }
    return descriptions.get(hierarchy, "")

# Streamlit Application Implementation
def main():
    st.set_page_config(
        page_title="Dr. Jackson DNP - Medical Professional Consultation",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Dr. Jackson DNP - Professional Medical Consultation Platform",
            'Report a bug': "mailto:support@drjackson-platform.org",
            'Get help': "https://drjackson-platform.org/help"
        }
    )
    
    # Initialize persona and settings
    dr_jackson = DrJacksonPersona()
    llm_settings = LLMSettings()
    
    # Initialize session state for patient data if not exist
    if 'patient_contact_info' not in st.session_state:
        st.session_state['patient_contact_info'] = PatientContactInfo()
    if 'patient_medical_info' not in st.session_state:
        st.session_state['patient_medical_info'] = PatientMedicalInfo()
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    # Custom CSS for theming and professional layout
    st.markdown("""
    <style>
    :root {
        --primary-color: #5D5CDE;
        --secondary-color: #4B4BA3;
        --tertiary-color: #E0E0FA;
        --accent-color: #FF7D54;
        --light-bg: #FFFFFF;
        --off-white: #F8F9FA;
        --light-gray: #E9ECEF;
        --medium-gray: #CED4DA;
        --dark-gray: #6C757D;
        --dark-bg: #181818;
        --dark-mode-card: #2C2C2C;
        --light-text: #333333;
        --dark-text: #E5E5E5;
        --light-border: #E2E8F0;
        --dark-border: #374151;
        --light-input: #F9FAFB;
        --dark-input: #1F2937;
        --success-color: #3DC9A1;
        --warning-color: #FFBE55;
        --error-color: #FF5A5A;
        --info-color: #5AA0FF;
    }
    
    /* Base Styling */
    .stApp {
        background-color: var(--light-bg);
        color: var(--light-text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .dark-mode .stApp {
        background-color: var(--dark-bg);
        color: var(--dark-text);
    }
    
    /* Typography Refinements */
    h1 {
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.01em;
        color: var(--primary-color);
        margin-bottom: 1rem;
    }
    
    h2 {
        font-weight: 600;
        font-size: 1.8rem;
        letter-spacing: -0.01em;
        color: var(--primary-color);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-weight: 600;
        font-size: 1.4rem;
        color: var(--primary-color);
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    p, li {
        font-size: 1rem;
        line-height: 1.6;
        color: var(--light-text);
    }
    
    .dark-mode p, .dark-mode li {
        color: var(--dark-text);
    }
    
    /* Card/Container Styling */
    div[data-testid="stForm"] {
        background-color: var(--off-white);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        border: 1px solid var(--light-border);
        margin-bottom: 24px;
    }
    
    .dark-mode div[data-testid="stForm"] {
        background-color: var(--dark-mode-card);
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        border: 1px solid var(--dark-border);
    }
    
    /* Expander Styling */
    details {
        background-color: var(--off-white);
        border-radius: 8px;
        border: 1px solid var(--light-border);
        margin-bottom: 16px;
        overflow: hidden;
    }
    
    .dark-mode details {
        background-color: var(--dark-mode-card);
        border: 1px solid var(--dark-border);
    }
    
    details summary {
        padding: 16px;
        cursor: pointer;
        font-weight: 500;
    }
    
    details summary:hover {
        background-color: var(--light-gray);
    }
    
    .dark-mode details summary:hover {
        background-color: rgba(255,255,255,0.05);
    }
    
    /* Button Styling */
    .stButton button {
        background-color: var(--primary-color);
        color: white;
        font-weight: 500;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--off-white);
        border-right: 1px solid var(--light-border);
    }
    
    .dark-mode [data-testid="stSidebar"] {
        background-color: var(--dark-mode-card);
        border-right: 1px solid var(--dark-border);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 1.5rem;
    }
    
    /* Header Styling */
    .professional-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 15px rgba(93, 92, 222, 0.25);
    }
    
    .professional-header h1 {
        color: white;
        margin-bottom: 0.5rem;
        font-size: 2.4rem;
    }
    
    .professional-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* HIPAA Notice Styling */
    .hipaa-notice {
        background-color: var(--tertiary-color);
        border-left: 4px solid var(--primary-color);
        padding: 16px;
        margin: 20px 0;
        border-radius: 6px;
    }
    
    .dark-mode .hipaa-notice {
        background-color: rgba(93, 92, 222, 0.15);
    }
    
    /* Chat Styling */
    .chat-container {
        border-radius: 12px;
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border: 1px solid var(--light-border);
        background-color: var(--off-white);
    }
    
    .dark-mode .chat-container {
        border: 1px solid var(--dark-border);
        background-color: var(--dark-mode-card);
    }
    
    /* Chat Message Styling */
    [data-testid="stChatMessage"] {
        padding: 0.75rem 0;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
        background-color: var(--light-gray);
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
        background-color: var(--primary-color);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 10px 16px;
        background-color: var(--light-gray);
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-colorst.markdown(f"""
                        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                            <div style="flex: 3; min-width: 300px;">
                                <h5 style="margin-top: 0; margin-bottom: 15px; font-size: 1.1rem;">{resource["title"]}</h5>
                                <p style="margin-bottom: 5px;"><strong>Type:</strong> {resource['type']}</p>
                                <p style="margin-bottom: 15px;"><strong>Description:</strong> {resource['description']}</p>
                                <div>
                        """, unsafe_allow_html=True)
                        
                        st.button(f"Request {resource['type']}", key=f"req_{resource['title']}", use_container_width=False)
                        
                        st.markdown(f"""
                                </div>
                            </div>
                            <div style="flex: 1; min-width: 100px; display: flex; align-items: center; justify-content: center;">
                                <div style="font-size: 3rem; color: var(--primary-color);">
                                    {resource['icon']}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            with resource_tabs[1]:
                st.markdown("""
                <h3 style="margin-bottom: 25px;">Treatment Approaches</h3>
                <p style="margin-bottom: 30px;">
                    These resources provide detailed information about our clinical approaches and treatment methodologies.
                    Personalized materials will be provided following your initial consultation based on your specific health needs.
                </p>
                """, unsafe_allow_html=True)
                
                # Sample treatment approaches with enhanced styling
                approaches = [
                    {"name": "Integrative Medicine Protocols", "icon": "🔄", "available": True},
                    {"name": "Functional Nutrition Plans", "icon": "🥗", "available": True},
                    {"name": "Targeted Supplementation", "icon": "💊", "available": True},
                    {"name": "Lifestyle Modification Programs", "icon": "⚖️", "available": True},
                    {"name": "Mind-Body Interventions", "icon": "🧠", "available": True}
                ]
                
                col1, col2 = st.columns(2)
                
                for i, approach in enumerate(approaches):
                    with col1 if i % 2 == 0 else col2:
                        st.markdown(f"""
                        <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid var(--light-border);">
                            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                <div style="font-size: 2rem; margin-right: 15px; color: var(--primary-color);">
                                    {approach['icon']}
                                </div>
                                <h4 style="margin: 0;">{approach['name']}</h4>
                            </div>
                            <p style="margin-bottom: 15px;">
                                Information about {approach['name']} will be provided following your initial consultation.
                                These resources are customized based on your specific health needs and goals.
                            </p>
                            <div>
                        """, unsafe_allow_html=True)
                        
                        if approach["available"]:
                            st.button(f"Request Preview", key=f"preview_{approach['name']}", use_container_width=False)
                        else:
                            st.markdown("""
                            <span style="color: var(--dark-gray); font-style: italic;">Available after consultation</span>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("""
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            with resource_tabs[2]:
                st.markdown("""
                <h3 style="margin-bottom: 25px;">Research & Publications</h3>
                <p style="margin-bottom: 30px;">
                    Dr. Jackson regularly contributes to academic and clinical research in several areas.
                    Selected publications and research highlights are available below.
                </p>
                """, unsafe_allow_html=True)
                
                # Research areas with enhanced styling
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 25px; border-radius: 10px; margin-bottom: 30px; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0; margin-bottom: 20px;">Research Focus Areas</h4>
                    <div style="display: flex; flex-wrap: wrap; gap: 15px;">
                """, unsafe_allow_html=True)
                
                research_areas = [
                    "Functional Medicine Approaches to Chronic Conditions",
                    "Integrative Protocols for Stress-Related Disorders", 
                    "Nutritional Interventions for Inflammatory Conditions",
                    "Mind-Body Medicine in Clinical Practice"
                ]
                
                for area in research_areas:
                    st.markdown(f"""
                    <div style="flex: 1; min-width: 250px; background-color: rgba(93, 92, 222, 0.05); 
                             padding: 15px; border-radius: 8px; border-left: 4px solid var(--primary-color);">
                        <p style="margin: 0; font-weight: 500;">{area}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Sample publications with enhanced styling
                st.markdown("""
                <h4 style="margin-bottom: 20px;">Selected Publications</h4>
                """, unsafe_allow_html=True)
                
                publications = [
                    {
                        "title": "Functional Medicine Approaches to Chronic Fatigue: A Systematic Review",
                        "journal": "Journal of Integrative Medicine",
                        "year": "2023",
                        "authors": "Jackson, R., et al.",
                        "abstract": "This systematic review evaluates the efficacy of functional medicine approaches in addressing chronic fatigue syndrome, examining outcomes from nutritional, hormonal, and inflammatory interventions."
                    },
                    {
                        "title": "Nutritional Strategies for HPA Axis Regulation in Chronic Stress",
                        "journal": "Nutritional Neuroscience",
                        "year": "2022",
                        "authors": "Chen, L., Jackson, R., et al.",
                        "abstract": "This research examines targeted nutritional interventions for hypothalamic-pituitary-adrenal axis regulation in patients with chronic stress, focusing on adaptogenic compounds and micronutrient support."
                    },
                    {
                        "title": "Integrative Approaches to Inflammatory Conditions: Clinical Outcomes",
                        "journal": "Complementary Therapies in Medicine",
                        "year": "2021",
                        "authors": "Jackson, R., Smith, J., et al.",
                        "abstract": "This clinical study evaluates outcomes of integrative medicine protocols combining conventional anti-inflammatory approaches with evidence-based complementary interventions."
                    }
                ]
                
                for pub in publications:
                    with st.expander(pub["title"]):
                        st.markdown(f"""
                        <div style="margin-bottom: 10px;">
                            <p style="margin-bottom: 5px;"><strong>Journal:</strong> {pub['journal']}, {pub['year']}</p>
                            <p style="margin-bottom: 5px;"><strong>Authors:</strong> {pub['authors']}</p>
                            <p style="margin-bottom: 15px;"><strong>Abstract:</strong> {pub['abstract']}</p>
                            <div>
                        """, unsafe_allow_html=True)
                        
                        st.button(f"Request Full Article", key=f"article_{pub['title'][:20]}", use_container_width=False)
                        
                        st.markdown("""
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Research collaborations
                st.markdown("""
                <div style="margin-top: 30px;">
                    <h4 style="margin-bottom: 15px;">Research Collaborations</h4>
                    <p>
                        Dr. Jackson actively collaborates with several academic and clinical research institutions.
                        For information about research partnerships or access to additional publications,
                        please contact our office.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        elif page == "Settings":
            # Professional header
            st.markdown("""
            <h1>Application Settings</h1>
            <div class="professional-separator" style="width: 150px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
            
            tabs = st.tabs(["LLM Configuration", "User Preferences", "HIPAA Compliance"])
            
            with tabs[0]:
                st.markdown("""
                <h3 style="margin-bottom: 20px;">AI Integration Settings</h3>
                <p style="margin-bottom: 25px;">
                    Configure API keys for AI integration with the consultation platform. These settings
                    enable advanced clinical note generation, treatment plan optimization, and personalized
                    educational content.
                </p>
                """, unsafe_allow_html=True)
                
                # Render LLM settings form
                llm_settings.render_settings_form()
                
                # Display integration status with enhanced styling
                if any([llm_settings.anthropic_api_key, llm_settings.openai_api_key, 
                        llm_settings.meta_api_key, llm_settings.xai_api_key]):
                    st.markdown("""
                    <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-top: 25px; border: 1px solid var(--light-border);">
                        <h4 style="margin-top: 0; margin-bottom: 15px;">AI Integration Features</h4>
                        <div class="professional-separator" style="margin-bottom: 20px;"></div>
                        <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                    """, unsafe_allow_html=True)
                    
                    features = [
                        {"name": "Automated clinical note generation", "icon": "📝", "description": "AI-assisted creation of standardized clinical documentation based on consultation content"},
                        {"name": "Medical literature search assistance", "icon": "🔍", "description": "Intelligent retrieval of relevant research and clinical guidelines"},
                        {"name": "Treatment plan optimization", "icon": "📈", "description": "AI-enhanced protocol development based on patient data and clinical evidence"},
                        {"name": "Follow-up reminder system", "icon": "🔔", "description": "Intelligent scheduling of follow-up communications and appointments"},
                        {"name": "Patient education material generation", "icon": "📚", "description": "Customized educational content creation based on patient needs"}
                    ]
                    
                    for feature in features:
                        st.markdown(f"""
                        <div style="flex: 1; min-width: 280px; background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px;">
                            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                <div style="font-size: 1.5rem; margin-right: 10px; color: var(--primary-color);">
                                    {feature['icon']}
                                </div>
                                <p style="margin: 0; font-weight: 500;">{feature['name']}</p>
                            </div>
                            <p style="margin: 0; font-size: 0.9rem; color: var(--dark-gray);">
                                {feature['description']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("""
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tabs[1]:
                st.markdown("""
                <h3 style="margin-bottom: 20px;">User Preferences</h3>
                <p style="margin-bottom: 25px;">
                    Customize your experience with the platform by setting your preferred appearance,
                    notification options, and accessibility features.
                </p>
                """, unsafe_allow_html=True)
                
                # Enhanced preferences with better styling
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--light-border);">
                        <h4 style="margin-top: 0; margin-bottom: 15px;">Display Settings</h4>
                        <div class="professional-separator" style="margin-bottom: 20px;"></div>
                    """, unsafe_allow_html=True)
                    
                    # Theme preference
                    st.markdown("<h5 style='font-size: 1rem; margin-bottom: 10px;'>Default Theme</h5>", unsafe_allow_html=True)
                    theme_pref = st.radio(
                        "Default Theme", 
                        options=["Light", "Dark", "System Default"],
                        index=0,
                        label_visibility="collapsed"
                    )
                    
                    # Text size with better styling
                    st.markdown("<h5 style='font-size: 1rem; margin-top: 20px; margin-bottom: 10px;'>Text Size</h5>", unsafe_allow_html=True)
                    text_size = st.select_slider(
                        "Text Size",
                        options=["Small", "Medium", "Large", "Extra Large"],
                        value="Medium",
                        label_visibility="collapsed"
                    )
                    
                    # Color scheme
                    st.markdown("<h5 style='font-size: 1rem; margin-top: 20px; margin-bottom: 10px;'>Color Scheme</h5>", unsafe_allow_html=True)
                    color_scheme = st.selectbox(
                        "Color Scheme",
                        options=["Standard", "High Contrast", "Professional Blue", "Warm", "Muted"],
                        index=0,
                        label_visibility="collapsed"
                    )
                    
                    st.markdown("""
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--light-border);">
                        <h4 style="margin-top: 0; margin-bottom: 15px;">Notification Settings</h4>
                        <div class="professional-separator" style="margin-bottom: 20px;"></div>
                    """, unsafe_allow_html=True)
                    
                    # Notification preferences with enhanced styling
                    st.markdown("<h5 style='font-size: 1rem; margin-bottom: 10px;'>Notification Methods</h5>", unsafe_allow_html=True)
                    email_notif = st.checkbox("Email Notifications", value=True)
                    sms_notif = st.checkbox("SMS Notifications", value=False)
                    app_notif = st.checkbox("In-App Notifications", value=True)
                    
                    # Notification frequency
                    st.markdown("<h5 style='font-size: 1rem; margin-top: 20px; margin-bottom: 10px;'>Notification Frequency</h5>", unsafe_allow_html=True)
                    notif_freq = st.radio(
                        "Notification Frequency",
                        options=["All Updates", "Daily Digest", "Weekly Summary", "Critical Only"],
                        index=0,
                        label_visibility="collapsed"
                    )
                    
                    st.markdown("""
                    </div>
                    """, unsafe_allow_html=True)
                
                # Privacy settings with enhanced styling
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-top: 20px; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0; margin-bottom: 15px;">Privacy & Data Settings</h4>
                    <div class="professional-separator" style="margin-bottom: 20px;"></div>
                    
                    <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                        <div style="flex: 1; min-width: 280px;">
                            <h5 style="font-size: 1rem; margin-bottom: 10px;">Data Usage</h5>
                            <div>
                """, unsafe_allow_html=True)
                
                data_usage = st.selectbox(
                    "Data Usage",
                    options=["Consultation Only", "Enhanced Experience (Anonymized)", "Full Data Sharing"],
                    index=0,
                    label_visibility="collapsed",
                    help="Controls how your data is used to improve services"
                )
                
                st.markdown("""
                            </div>
                        </div>
                        <div style="flex: 1; min-width: 280px;">
                            <h5 style="font-size: 1rem; margin-bottom: 10px;">Session Timeout</h5>
                            <div>
                """, unsafe_allow_html=True)
                
                timeout = st.selectbox(
                    "Session Timeout",
                    options=["5 minutes", "15 minutes", "30 minutes", "1 hour"],
                    index=1,
                    label_visibility="collapsed",
                    help="Set how long before inactive sessions are closed"
                )
                
                st.markdown("""
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Save button with enhanced styling
                st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
                if st.button("Save Preferences", use_container_width=True):
                    st.success("User preferences saved successfully.")
                
            with tabs[2]:
                st.markdown("""
                <h3 style="margin-bottom: 20px;">HIPAA Compliance Information</h3>
                <p style="margin-bottom: 25px;">
                    This application implements comprehensive HIPAA compliance measures to protect 
                    your personal health information. Below are details about our security and privacy protocols.
                </p>
                """, unsafe_allow_html=True)
                
                # Enhanced HIPAA information with better styling
                st.markdown("""
                <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 30px;">
                """, unsafe_allow_html=True)
                
                hipaa_sections = [
                    {
                        "title": "Technical Safeguards",
                        "icon": "🔒",
                        "items": [
                            "End-to-end encryption for all patient data",
                            "Role-based access controls",
                            "Automatic session timeouts",
                            "Secure authentication mechanisms",
                            "Comprehensive audit logging"
                        ]
                    },
                    {
                        "title": "Physical Safeguards",
                        "icon": "🏢",
                        "items": [
                            "Secure cloud infrastructure",
                            "Redundant data storage with encryption",
                            "Disaster recovery protocols",
                            "Physical access restrictions",
                            "Environmental controls"
                        ]
                    },
                    {
                        "title": "Administrative Safeguards",
                        "icon": "📋",
                        "items": [
                            "Regular security assessments",
                            "Staff training on PHI handling",
                            "Breach notification procedures",
                            "Business Associate Agreements",
                            "Risk management protocols"
                        ]
                    }
                ]
                
                for section in hipaa_sections:
                    st.markdown(f"""
                    <div style="flex: 1; min-width: 300px; background-color: var(--off-white); padding: 20px; border-radius: 10px; border: 1px solid var(--light-border);">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="font-size: 2rem; margin-right: 15px; color: var(--primary-color);">
                                {section['icon']}
                            </div>
                            <h4 style="margin: 0;">{section['title']}</h4>
                        </div>
                        <ul style="margin-bottom: 0; padding-left: 20px;">
                    """, unsafe_allow_html=True)
                    
                    for item in section["items"]:
                        st.markdown(f"""
                        <li style="margin-bottom: 8px;">{item}</li>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("""
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
                
                # Contact information with enhanced styling
                st.markdown("""
                <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--info-color);">
                    <h4 style="color: var(--info-color); margin-top: 0;">Contact Information</h4>
                    <p style="margin-bottom: 0;">For more information on our HIPAA compliance measures, please contact our Privacy Officer at <strong>privacy@optimumwellness.org</strong>.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Compliance audit information with enhanced styling
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-top: 25px; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0; margin-bottom: 15px;">Compliance Audit History</h4>
                    <div class="professional-separator" style="margin-bottom: 20px;"></div>
                    
                    <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                        <div style="flex: 1; min-width: 280px;">
                            <p style="margin: 0; font-weight: 500;">Last Compliance Audit:</p>
                            <p style="margin: 5px 0 0 0; color: var(--success-color); font-weight: 500;">February 12, 2025</p>
                            <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: var(--dark-gray);">Full technical and administrative review</p>
                        </div>
                        <div style="flex: 1; min-width: 280px;">
                            <p style="margin: 0; font-weight: 500;">Next Scheduled Audit:</p>
                            <p style="margin: 5px 0 0 0; color: var(--primary-color); font-weight: 500;">August 15, 2025</p>
                            <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: var(--dark-gray);">Comprehensive security assessment</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
                            st.markdown(f"""
                            <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid var(--light-border);">
                                <h3 style="margin-top: 0;">{domain}</h3>
                                <div class="professional-separator"></div>
                            """, unsafe_allow_html=True)
                            
                            if domain == "Gut Health":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Gastrointestinal function serves as a cornerstone of systemic health. Our approach addresses
                                    digestive efficiency, intestinal barrier integrity, microbiome diversity, and enteric nervous system
                                    regulation through targeted interventions.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>Comprehensive microbiome assessment</li>
                                        <li>Intestinal permeability restoration</li>
                                        <li>Digestive enzyme optimization</li>
                                        <li>Enteric nervous system regulation</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            elif domain == "Oxidative Stress":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Oxidative stress management focuses on balancing pro-oxidant and antioxidant mechanisms.
                                    Our protocols assess redox status and implement targeted interventions to optimize cellular
                                    protection mechanisms.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>Redox balance assessment</li>
                                        <li>Cellular protection enhancement</li>
                                        <li>Antioxidant enzyme support</li>
                                        <li>Mitochondrial protection protocols</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            elif domain == "Professional Development":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Continuing professional development ensures implementation of the latest evidence-based
                                    approaches. Our practice maintains rigorous standards for ongoing education and clinical
                                    knowledge integration.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>Continuous medical education</li>
                                        <li>Research literature integration</li>
                                        <li>Advanced protocol development</li>
                                        <li>Clinical outcomes assessment</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("""
                            </div>
                            """, unsafe_allow_html=True)
            
            with specialty_tabs[2]:
                st.markdown("""
                <h3 style="margin-bottom: 25px;">Treatment Approaches</h3>
                <p style="margin-bottom: 30px;">
                    Dr. Jackson's practice implements structured, evidence-based treatment protocols
                    that address underlying mechanisms rather than symptoms alone. Each approach follows
                    a systematic implementation process designed for optimal outcomes.
                </p>
                """, unsafe_allow_html=True)
                
                # Sample treatment approaches with more professional styling
                approaches = [
                    {"name": "Integrative Medicine Protocols", 
                     "description": "Combining conventional medical standards with evidence-based complementary approaches to address both symptoms and underlying mechanisms.",
                     "phases": ["Comprehensive assessment", "Multisystem analysis", "Integrated intervention design", "Coordinated implementation", "Progress monitoring"]},
                    {"name": "Functional Nutrition Plans", 
                     "description": "Therapeutic dietary interventions based on individual biochemistry and specific nutritional needs identified through advanced testing.",
                     "phases": ["Nutritional assessment", "Elimination protocol", "Therapeutic reintroduction", "Supplementation strategy", "Maintenance planning"]},
                    {"name": "Targeted Supplementation", 
                     "description": "Precision micronutrient, botanical, and nutraceutical interventions based on identified biochemical imbalances and functional requirements.",
                     "phases": ["Deficiency identification", "Interaction analysis", "Bioavailability optimization", "Therapeutic dosing", "Efficacy monitoring"]},
                    {"name": "Lifestyle Modification Programs", 
                     "description": "Structured protocols for sleep optimization, stress management, physical activity, and environmental modification.",
                     "phases": ["Behavioral assessment", "Priority identification", "Incremental implementation", "Habit formation support", "Progress evaluation"]},
                    {"name": "Mind-Body Interventions", 
                     "description": "Evidence-based approaches targeting the psychoneuroimmunological axis through cognitive, somatic, and contemplative practices.",
                     "phases": ["Stress response assessment", "Technique selection", "Implementation structure", "Practice integration", "Response monitoring"]}
                ]
                
                for approach in approaches:
                    with st.expander(approach["name"]):
                        st.markdown(f"""
                        <div style="margin-bottom: 20px;">
                            <h4 style="margin-top: 0;">{approach["name"]}</h4>
                            <p style="margin-bottom: 20px;">{approach['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Phase visualization with enhanced styling
                        st.markdown("""
                        <h4 style="font-size: 1.1rem; margin-bottom: 15px;">Implementation Phases</h4>
                        """, unsafe_allow_html=True)
                        
                        phase_cols = st.columns(len(approach["phases"]))
                        
                        for i, (col, phase) in enumerate(zip(phase_cols, approach["phases"])):
                            with col:
                                st.markdown(f"""
                                <div style="padding: 15px; border-radius: 8px; background-color: rgba(93, 92, 222, {0.1 + (i * 0.08)}); 
                                           text-align: center; height: 110px; display: flex; flex-direction: column; 
                                           align-items: center; justify-content: center; border: 1px solid rgba(93, 92, 222, 0.2);">
                                    <div style="background-color: white; width: 25px; height: 25px; border-radius: 50%; 
                                             display: flex; align-items: center; justify-content: center; 
                                             margin-bottom: 10px; font-weight: bold; color: var(--primary-color);">
                                        {i+1}
                                    </div>
                                    <p style="margin: 0; font-weight: 500; font-size: 0.9rem; color: rgba(0,0,0,0.8);">{phase}</p>
                                </div>
                                """, unsafe_allow_html=True)
                
                # Treatment philosophy statement with enhanced styling
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 25px; border-radius: 10px; margin-top: 40px; border: 1px solid var(--light-border);">
                    <h4 style="color: var(--primary-color); margin-top: 0;">Treatment Philosophy</h4>
                    <div class="professional-separator"></div>
                    <p style="margin-top: 15px;">
                        All treatment approaches are implemented with rigorous attention to evidence-based standards and individualized 
                        based on comprehensive patient assessment. Dr. Jackson's clinical protocols integrate multiple therapeutic 
                        modalities while maintaining strict adherence to professional practice guidelines.
                    </p>
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;">
                        <div style="flex: 1; min-width: 200px;">
                            <h5 style="margin-top: 0; font-size: 1rem;">Evidence-Based</h5>
                            <p style="font-size: 0.9rem; margin-bottom: 0;">
                                All protocols are grounded in current research literature and clinical evidence,
                                with continuous updates as new findings emerge.
                            </p>
                        </div>
                        <div style="flex: 1; min-width: 200px;">
                            <h5 style="margin-top: 0; font-size: 1rem;">Personalized</h5>
                            <p style="font-size: 0.9rem; margin-bottom: 0;">
                                Treatment plans are tailored to each patient's unique biochemistry,
                                genetic predispositions, and specific health goals.
                            </p>
                        </div>
                        <div style="flex: 1; min-width: 200px;">
                            <h5 style="margin-top: 0; font-size: 1rem;">Comprehensive</h5>
                            <p style="font-size: 0.9rem; margin-bottom: 0;">
                                Our approach addresses all relevant physiological systems rather than
                                isolated symptoms or single-system interventions.
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Call to action
                st.markdown("""
                <div style="margin-top: 40px; text-align: center;">
                    <p style="font-size: 1.1rem; margin-bottom: 20px;">
                        Ready to explore how these treatment approaches can be customized for your specific health needs?
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Schedule a Consultation", key="specialty_consult_btn", use_container_width=True):
                        page = "Consultation"
                        st.experimental_rerun()
                with col2:
                    if st.button("Chat with Dr. Jackson", key="specialty_chat_btn", use_container_width=True):
                        page = "Chat with Dr. Jackson"
                        st.experimental_rerun()
        
        elif page == "Approach":
            # Professional header
            st.markdown("""
            <h1>Professional Methodology</h1>
            <div class="professional-separator" style="width: 150px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
            
            # Display knowledge priorities with enhanced styling
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Evidence-Based Approach</h3>
            <p style="margin-bottom: 30px;">
                Dr. Jackson's practice is built on a hierarchical approach to medical knowledge, prioritizing 
                rigorous evidence while integrating multiple perspectives to provide comprehensive care.
            </p>
            """, unsafe_allow_html=True)
            
            # Use more engaging visual representation
            priorities = dr_jackson.knowledge_priorities
            
            # Create a card-based layout for priorities
            st.markdown("""
            <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 40px;">
            """, unsafe_allow_html=True)
            
            for i, priority in enumerate(priorities):
                # Calculate progress bar percentage based on reversed position (higher items get higher percentage)
                percentage = 100 - (i * (100 / len(priorities)))
                
                st.markdown(f"""
                <div style="flex: 1; min-width: 300px; background-color: var(--off-white); padding: 20px; border-radius: 10px; border: 1px solid var(--light-border);">
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="background-color: var(--primary-color); width: 30px; height: 30px; border-radius: 50%; 
                                 display: flex; align-items: center; justify-content: center; 
                                 margin-right: 15px; font-weight: bold; color: white;">
                            {i+1}
                        </div>
                        <h4 style="margin: 0; font-size: 1.2rem;">{priority}</h4>
                    </div>
                    <div style="background-color: var(--light-gray); height: 8px; border-radius: 4px; margin-bottom: 15px;">
                        <div style="background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%); 
                                  height: 8px; border-radius: 4px; width: {percentage}%;"></div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Add explanatory text for each priority
                if i == 0:  # Evidence-based research
                    st.markdown("""
                    <p style="font-size: 0.9rem;">
                        Peer-reviewed studies form the foundation of our clinical approach. We prioritize 
                        systematic reviews, meta-analyses, and randomized controlled trials when available.
                    </p>
                    """, unsafe_allow_html=True)
                elif i == 1:  # Clinical guidelines
                    st.markdown("""
                    <p style="font-size: 0.9rem;">
                        Professional medical association guidelines and consensus statements provide 
                        standardized frameworks for our clinical protocols.
                    </p>
                    """, unsafe_allow_html=True)
                elif i == 2:  # Professional experience
                    st.markdown("""
                    <p style="font-size: 0.9rem;">
                        Clinical expertise developed through years of patient care informs the application 
                        of research findings to individual cases.
                    </p>
                    """, unsafe_allow_html=True)
                elif i == 3:  # Holistic wellness approaches
                    st.markdown("""
                    <p style="font-size: 0.9rem;">
                        Evidence-supported complementary approaches are integrated when appropriate to 
                        address the full spectrum of patient wellbeing.
                    </p>
                    """, unsafe_allow_html=True)
                elif i == 4:  # Integrative medicine perspectives
                    st.markdown("""
                    <p style="font-size: 0.9rem;">
                        Traditional healing systems with empirical support are considered within our 
                        comprehensive treatment frameworks.
                    </p>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Communication framework with enhanced styling
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Clinical Communication Framework</h3>
            <p style="margin-bottom: 30px;">
                Professional communication is essential to effective clinical care. Dr. Jackson's practice 
                follows a structured communication methodology to ensure clarity, comprehensiveness, and patient understanding.
            </p>
            """, unsafe_allow_html=True)
            
            cols = st.columns(3)
            with cols[0]:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0; text-align: center; margin-bottom: 15px;">Structure</h4>
                    <div class="professional-separator"></div>
                """, unsafe_allow_html=True)
                
                for step in dr_jackson.clinical_format.steps:
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <div style="min-width: 8px; height: 8px; background-color: var(--primary-color); border-radius: 50%; margin-right: 10px;"></div>
                        <p style="margin: 0;">{step}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            with cols[1]:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0; text-align: center; margin-bottom: 15px;">Style</h4>
                    <div class="professional-separator"></div>
                """, unsafe_allow_html=True)
                
                for key, value in dr_jackson.clinical_format.style.items():
                    st.markdown(f"""
                    <div style="margin-bottom: 15px;">
                        <h5 style="margin-bottom: 5px; color: var(--primary-color);">{key.capitalize()}</h5>
                        <p style="margin: 0; padding-left: 10px; border-left: 3px solid var(--primary-color);">{value}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            with cols[2]:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0; text-align: center; margin-bottom: 15px;">Values</h4>
                    <div class="professional-separator"></div>
                """, unsafe_allow_html=True)
                
                for i, value in enumerate(dr_jackson.core_values[:4]):
                    st.markdown(f"""
                    <div style="background-color: rgba(93, 92, 222, {0.05 + (i * 0.02)}); padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                        <p style="margin: 0; font-weight: 500;">{value}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # DEI focus with enhanced styling
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Inclusive Care Framework</h3>
            <p style="margin-bottom: 30px;">
                Dr. Jackson's practice emphasizes equitable, culturally-responsive care that addresses healthcare 
                disparities and provides appropriate support for all patients regardless of background or identity.
            </p>
            """, unsafe_allow_html=True)
            
            # More engaging presentation
            with st.container():
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 25px; border-radius: 10px; margin-bottom: 30px; border: 1px solid var(--light-border);">
                    <h4 style="color: var(--primary-color); margin-top: 0; text-align: center;">Equitable Healthcare Approach</h4>
                    <p style="text-align: center; margin-bottom: 25px;">Dr. Jackson's practice emphasizes inclusive, culturally-responsive care through the following principles:</p>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                dei_focus_items = dr_jackson.dei_focus
                
                for i, focus in enumerate(dei_focus_items[:3]):
                    with col1:
                        st.markdown(f"""
                        <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid var(--primary-color);">
                            <h5 style="margin-top: 0; margin-bottom: 10px; font-size: 1rem;">{i+1}. {focus}</h5>
                            <p style="margin: 0; font-size: 0.9rem;">
                                {get_dei_description(focus)}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                
                for i, focus in enumerate(dei_focus_items[3:], 4):
                    with col2:
                        st.markdown(f"""
                        <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid var(--primary-color);">
                            <h5 style="margin-top: 0; margin-bottom: 10px; font-size: 1rem;">{i+1}. {focus}</h5>
                            <p style="margin: 0; font-size: 0.9rem;">
                                {get_dei_description(focus)}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Treatment philosophy with enhanced styling
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Treatment Philosophy</h3>
            <p style="margin-bottom: 30px;">
                Dr. Jackson's clinical approach integrates conventional medical standards with evidence-supported 
                complementary modalities. This model addresses not only symptom management but underlying 
                pathophysiological mechanisms.
            </p>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0;">Foundational Elements</h4>
                    <div class="professional-separator"></div>
                """, unsafe_allow_html=True)
                
                elements = [
                    "Comprehensive laboratory assessment",
                    "Detailed functional history",
                    "Environmental exposure evaluation",
                    "Nutritional status optimization",
                    "Sleep architecture normalization"
                ]
                
                for element in elements:
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="min-width: 24px; height: 24px; background-color: var(--primary-color); 
                                 border-radius: 50%; margin-right: 15px; display: flex; 
                                 align-items: center; justify-content: center; color: white;">
                            ✓
                        </div>
                        <p style="margin: 0; font-weight: 500;">{element}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0;">Intervention Hierarchy</h4>
                    <div class="professional-separator"></div>
                """, unsafe_allow_html=True)
                
                hierarchies = [
                    "Remove pathological triggers",
                    "Restore physiological function",
                    "Rebalance regulatory systems",
                    "Regenerate compromised tissues",
                    "Reestablish health maintenance"
                ]
                
                for i, hierarchy in enumerate(hierarchies):
                    st.markdown(f"""
                    <div style="display: flex; margin-bottom: 12px;">
                        <div style="min-width: 30px; margin-right: 15px; text-align: center;">
                            <div style="background-color: var(--primary-color); width: 30px; height: 30px; 
                                     border-radius: 50%; display: flex; align-items: center; 
                                     justify-content: center; color: white; font-weight: bold;">
                                {i+1}
                            </div>
                        </div>
                        <div>
                            <p style="margin: 0 0 5px 0; font-weight: 500;">{hierarchy}</p>
                            <p style="margin: 0; font-size: 0.85rem; color: var(--dark-gray);">
                                {get_hierarchy_description(hierarchy)}
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            # Bottom CTA
            st.markdown("""
            <div style="text-align: center; margin-top: 40px;">
                <p style="font-size: 1.1rem; margin-bottom: 20px;">
                    Experience Dr. Jackson's professional approach to healthcare with a personalized consultation.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1,1])
            with col1:
                if st.button("Schedule Consultation", key="approach_consult_btn", use_container_width=True):
                    page = "Consultation"
                    st.experimental_rerun()
            with col2:
                if st.button("Learn About Specialties", key="approach_specialties_btn", use_container_width=True):
                    page = "Specialties"
                    st.experimental_rerun()
        
        elif page == "Resources":
            # Professional header
            st.markdown("""
            <h1>Professional Resources</h1>
            <div class="professional-separator" style="width: 150px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
            
            # HIPAA Notice with enhanced styling
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; 
                       border-left: 5px solid var(--info-color); margin-bottom: 30px;">
                <h4 style="color: var(--info-color); margin-top: 0;">HIPAA Compliance Notice</h4>
                <p style="margin-bottom: 10px;">All educational resources and materials provided through this platform are protected by HIPAA regulations:</p>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                    <li style="margin-bottom: 5px;">Materials are for educational purposes only and do not constitute medical advice</li>
                    <li style="margin-bottom: 5px;">Resources are provided securely and cannot be accessed by unauthorized parties</li>
                    <li style="margin-bottom: 5px;">Your use of these materials is confidential and not shared with third parties</li>
                    <li style="margin-bottom: 0;">All resource access is logged for privacy and security purposes</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Educational resources tabs with enhanced styling
            st.markdown("""
            <p style="margin-bottom: 25px;">
                Dr. Jackson's practice provides a range of professional resources to support your healthcare journey.
                These materials are curated from evidence-based sources and aligned with our clinical approach.
            </p>
            """, unsafe_allow_html=True)
            
            resource_tabs = st.tabs(["Patient Education", "Treatment Information", "Research & Publications"])
            
            with resource_tabs[0]:
                st.markdown("""
                <h3 style="margin-bottom: 25px;">Patient Education Materials</h3>
                <p style="margin-bottom: 30px;">
                    These educational resources are designed to provide evidence-based information
                    about various health conditions, therapeutic approaches, and self-care strategies.
                </p>
                """, unsafe_allow_html=True)
                
                # Resource categories with enhanced styling
                categories = [
                    "Functional Medicine Basics",
                    "Nutritional Approaches",
                    "Stress Management",
                    "Hormone Balance",
                    "Gut Health",
                    "Sleep Optimization"
                ]
                
                # Category selection with better styling
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-bottom: 25px; border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0; margin-bottom: 15px;">Select a Resource Category</h4>
                """, unsafe_allow_html=True)
                
                selected_category = st.selectbox("Select a category", categories, label_visibility="collapsed")
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
                
                # Display sample resources based on category with enhanced styling
                st.markdown(f"""
                <h4 style="margin-bottom: 20px;">{selected_category} Resources</h4>
                """, unsafe_allow_html=True)
                
                # Sample resources with enhanced styling
                resources = [
                    {"title": f"{selected_category} Primer", "type": "PDF Guide", "description": "A comprehensive introduction to key concepts and approaches.", "icon": "📄"},
                    {"title": f"Understanding Your {selected_category} Assessment", "type": "Video", "description": "A visual explanation of assessment methods and interpretation.", "icon": "🎥"},
                    {"title": f"{selected_category} FAQ", "type": "Article", "description": "Answers to commonly asked questions about this topic.", "icon": "❓"}
                ]
                
                for resource in resources:
                    with st.expander(resource["title"]):
                        st.markdown(f"""
                        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                            <div style="flex: 3; min-width: 300px;">
                                <h5 style="margin-top: 0; margin-            # Professional header
            st.markdown("""
            <h1>Professional Chat Consultation</h1>
            <div class="professional-separator" style="width: 150px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
            
            # Check if patient info is filled out
            patient_info = st.session_state['patient_contact_info']
            
            if not patient_info.first_name or not patient_info.last_name:
                # Warning with enhanced styling
                st.markdown("""
                <div style="background-color: rgba(255, 190, 85, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--warning-color);">
                    <h4 style="color: var(--warning-color); margin-top: 0;">Patient Information Required</h4>
                    <p style="margin-bottom: 15px;">Please complete the Patient Intake form before using the chat feature.</p>
                """, unsafe_allow_html=True)
                
                if st.button("Go to Patient Intake →", use_container_width=True):
                    page = "Patient Intake"
                    st.experimental_rerun()
                    
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                # Two-column layout for chat interface
                chat_col, sidebar_col = st.columns([3, 1])
                
                with chat_col:
                    # HIPAA notice for chat with enhanced styling
                    st.markdown("""
                    <div style="background-color: rgba(90, 160, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid var(--info-color);">
                        <h4 style="color: var(--info-color); margin-top: 0;">Secure Communication</h4>
                        <p style="margin-bottom: 0;">This chat is encrypted and complies with HIPAA regulations. While this platform provides general guidance, it is not a substitute for in-person medical care for urgent or emergency conditions.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced chat container
                    st.markdown("""
                    <div style="background-color: var(--off-white); border-radius: 10px; border: 1px solid var(--light-border); padding: 5px; margin-bottom: 20px;">
                    """, unsafe_allow_html=True)
                    
                    # Chat container
                    chat_container = st.container()
                    with chat_container:
                        for message in st.session_state['chat_history']:
                            display_chat_message(message)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Welcome message if chat is empty
                    if not st.session_state['chat_history']:
                        with st.chat_message("assistant", avatar="🩺"):
                            intro_message = f"Good day, {patient_info.first_name}. I am Dr. Jackson, {dr_jackson.credentials}, specializing in functional and integrative medicine. How may I be of assistance to you today?"
                            st.markdown(intro_message)
                            # Add welcome message to history
                            st.session_state['chat_history'].append(
                                ChatMessage(role="assistant", content=intro_message)
                            )
                    
                    # Chat input with professional styling
                    st.markdown("""
                    <div style="margin-bottom: 10px;">
                        <h4 style="font-size: 1rem; margin-bottom: 5px;">Your Message</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    user_input = st.chat_input("Type your medical question here...")
                    
                    if user_input:
                        # Add user message to history
                        st.session_state['chat_history'].append(
                            ChatMessage(role="user", content=user_input)
                        )
                        
                        # Display the new user message
                        with st.chat_message("user"):
                            st.markdown(user_input)
                        
                        # Generate and display Dr. Jackson's response
                        with st.chat_message("assistant", avatar="🩺"):
                            message_placeholder = st.empty()
                            
                            # Simulate typing with a delay
                            full_response = dr_jackson.get_chat_response(user_input)
                            
                            # Simulate typing effect
                            displayed_response = ""
                            for chunk in full_response.split():
                                displayed_response += chunk + " "
                                message_placeholder.markdown(displayed_response + "▌")
                                time.sleep(0.03)  # Faster typing
                            
                            message_placeholder.markdown(full_response)
                            st.caption(f"{datetime.datetime.now().strftime('%I:%M %p')}")
                        
                        # Add assistant response to history
                        st.session_state['chat_history'].append(
                            ChatMessage(role="assistant", content=full_response)
                        )
                        
                        # Enhanced follow-up options
                        st.markdown("""
                        <div style="margin-top: 20px;">
                            <h4 style="font-size: 1rem; margin-bottom: 15px;">Quick Follow-up Options</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("Request additional information", key="more_info_btn", use_container_width=True):
                                followup = "Can you provide additional information or resources about this topic?"
                                st.session_state['chat_history'].append(
                                    ChatMessage(role="user", content=followup)
                                )
                                st.experimental_rerun()
                        
                        with col2:
                            if st.button("Schedule consultation", key="schedule_btn", use_container_width=True):
                                followup = "I'd like to schedule a full consultation to discuss this in more detail."
                                st.session_state['chat_history'].append(
                                    ChatMessage(role="user", content=followup)
                                )
                                st.experimental_rerun()
                        
                        with col3:
                            if st.button("Ask about treatment options", key="treatment_btn", use_container_width=True):
                                followup = "What treatment approaches would you recommend for this condition?"
                                st.session_state['chat_history'].append(
                                    ChatMessage(role="user", content=followup)
                                )
                                st.experimental_rerun()
                
                with sidebar_col:
                    # Enhanced patient context
                    st.markdown("""
                    <div style="background-color: var(--off-white); padding: 15px; border-radius: 10px; border: 1px solid var(--light-border); margin-bottom: 20px;">
                        <h4 style="margin-top: 0; font-size: 1rem;">Patient Context</h4>
                        <div class="professional-separator" style="margin: 10px 0;"></div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Name:</strong> {patient_info.first_name} {patient_info.last_name}</p>
                        <p style="margin: 5px 0; font-size: 0.9rem;"><strong>DOB:</strong> {patient_info.date_of_birth}</p>
                    """, unsafe_allow_html=True)
                    
                    medical_info = st.session_state['patient_medical_info']
                    if medical_info.chronic_conditions:
                        conditions = ", ".join(medical_info.chronic_conditions[:2])
                        if len(medical_info.chronic_conditions) > 2:
                            conditions += "..."
                        st.markdown(f"""
                            <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Conditions:</strong> {conditions}</p>
                        """, unsafe_allow_html=True)
                        
                    if medical_info.current_medications:
                        medications = ", ".join(medical_info.current_medications[:2])
                        if len(medical_info.current_medications) > 2:
                            medications += "..."
                        st.markdown(f"""
                            <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Medications:</strong> {medications}</p>
                        """, unsafe_allow_html=True)
                        
                    st.markdown("""
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced chat controls
                    with st.expander("Chat Controls", expanded=False):
                        if st.button("Clear Chat History", use_container_width=True):
                            st.session_state['chat_history'] = []
                            st.success("Chat history has been cleared")
                            st.experimental_rerun()
                        
                        # AI model selection if API keys are configured
                        if any([st.session_state.get('anthropic_api_key'), 
                                st.session_state.get('openai_api_key')]):
                            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                            st.markdown("<h4 style='font-size: 1rem;'>AI Model Selection</h4>", unsafe_allow_html=True)
                            model = st.radio(
                                "Select AI model for consultation",
                                ["Claude (Anthropic)", "GPT-4 (OpenAI)", "Llama (Meta)"],
                                index=0
                            )
                            st.info(f"Currently using: {model}")
                    
                    # Enhanced health topics quick access
                    st.markdown("""
                    <div style="margin-top: 20px;">
                        <h4 style="font-size: 1rem; margin-bottom: 15px;">Common Health Topics</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    topics = [
                        ("Functional Medicine", "🔬"),
                        ("Nutritional Guidance", "🥗"),
                        ("Sleep Optimization", "💤"),
                        ("Stress Management", "🧘‍♀️"),
                        ("Hormone Balance", "⚖️"),
                        ("Gut Health", "🦠")
                    ]
                    
                    for topic, icon in topics:
                        topic_button = f"{icon} {topic}"
                        if st.button(topic_button, key=f"topic_{topic}", use_container_width=True):
                            query = f"I'd like to learn more about {topic.lower()}. What's your approach?"
                            st.session_state['chat_history'].append(
                                ChatMessage(role="user", content=query)
                            )
                            st.experimental_rerun()
                    
                    # Professional note
                    st.markdown("""
                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 15px; border-radius: 10px; margin-top: 25px;">
                        <p style="font-size: 0.85rem; margin: 0;">
                            <strong>Professional Note:</strong> This chat interface provides general medical guidance based on 
                            Dr. Jackson's professional approach. For personalized treatment plans, 
                            we recommend scheduling a comprehensive consultation.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Schedule consultation button
                    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                    if st.button("📅 Schedule Full Consultation", use_container_width=True):
                        page = "Consultation"
                        st.experimental_rerun()
        
        elif page == "Specialties":
            # Professional header
            st.markdown("""
            <h1>Areas of Specialization</h1>
            <div class="professional-separator" style="width: 120px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
            
            # Add tabs for better organization with enhanced styling
            specialty_tabs = st.tabs(["Primary Specialties", "Additional Focus Areas", "Treatment Approaches"])
            
            with specialty_tabs[0]:
                st.markdown("""
                <h3 style="margin-bottom: 20px;">Primary Clinical Specialties</h3>
                <p style="margin-bottom: 25px;">
                    Dr. Jackson's practice offers comprehensive care across the following primary specialties, 
                    with evidence-based approaches tailored to individual patient needs.
                </p>
                """, unsafe_allow_html=True)
                
                # Create a more visual representation of specialties
                for i, domain in enumerate(dr_jackson.primary_domains):
                    with st.expander(f"{i+1}. {domain}", expanded=i==0):
                        # Domain-specific content
                        if domain == "Psychiatric Care":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Our psychiatric care approach integrates conventional psychopharmacology with functional medicine principles. 
                                    We assess neurotransmitter pathways, inflammatory markers, and nutrient status alongside standard psychiatric evaluation.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Comprehensive neurochemical assessment</strong> - Evaluating multiple biochemical pathways</li>
                                        <li><strong>Targeted amino acid therapy</strong> - Precision supplementation for neurotransmitter support</li>
                                        <li><strong>Inflammatory pathway modulation</strong> - Addressing neuroinflammatory contributions</li>
                                        <li><strong>Neuroendocrine optimization</strong> - Balancing HPA axis function</li>
                                        <li><strong>Microbiome-brain axis support</strong> - Targeting gut-brain connection</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Clinical Approach</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our psychiatric protocols integrate conventional assessment with functional testing to identify root causes of mental health conditions.</p>
                                        <p>Treatment plans combine targeted nutritional interventions, lifestyle modifications, and when appropriate, conventional medications in a comprehensive approach.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Psychiatric+Care+Approach", use_column_width=True)
                            
                        elif domain == "Wellness Optimization":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Wellness optimization begins with comprehensive assessment of physiological function across multiple systems.
                                    Our approach establishes personalized baselines and identifies limiting factors in performance and wellbeing.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Metabolic efficiency enhancement</strong> - Optimizing cellular energy production pathways</li>
                                        <li><strong>Cellular energy production</strong> - Supporting mitochondrial function and ATP synthesis</li>
                                        <li><strong>Oxidative stress management</strong> - Balancing pro-oxidant and antioxidant mechanisms</li>
                                        <li><strong>Circadian rhythm optimization</strong> - Restoring natural biological timing systems</li>
                                        <li><strong>Recovery protocol development</strong> - Structured approaches to physiological restoration</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Performance Enhancement</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our wellness optimization protocols identify and address the specific factors limiting your physiological performance.</p>
                                        <p>Rather than generic wellness approaches, we target biochemical, structural, and regulatory elements unique to your health profile.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Wellness+Optimization+Approach", use_column_width=True)
                            
                        elif domain == "Anti-aging Medicine":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Our anti-aging approach focuses on measurable biomarkers of cellular aging rather than cosmetic concerns alone.
                                    We target key mechanisms of cellular senescence and tissue degeneration through evidence-based interventions.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Telomere dynamics assessment</strong> - Evaluating cellular replicative potential</li>
                                        <li><strong>Advanced glycation endpoint management</strong> - Reducing cross-linked protein accumulation</li>
                                        <li><strong>Mitochondrial function optimization</strong> - Enhancing cellular energy production</li>
                                        <li><strong>Senolytic protocol implementation</strong> - Targeted approach to senescent cell burden</li>
                                        <li><strong>Epigenetic modification strategies</strong> - Optimizing gene expression patterns</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Biological Age Management</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our anti-aging protocols focus on measurable biomarkers of aging rather than chronological age.</p>
                                        <p>We implement evidence-based approaches to reduce biological age markers and optimize physiological function.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Anti-aging+Medicine+Approach", use_column_width=True)
                            
                        elif domain == "Functional Medicine":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Functional medicine addresses root causes rather than symptoms alone. Our approach investigates
                                    underlying mechanisms of dysfunction through comprehensive laboratory assessment and detailed history.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Systems biology framework</strong> - Understanding interconnected physiological networks</li>
                                        <li><strong>Biochemical individuality assessment</strong> - Personalized physiological evaluation</li>
                                        <li><strong>Environmental exposure evaluation</strong> - Identifying toxic burden and triggers</li>
                                        <li><strong>Genetic predisposition analysis</strong> - Understanding susceptibility patterns</li>
                                        <li><strong>Root cause identification protocols</strong> - Systematic approach to underlying factors</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Root Cause Approach</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our functional medicine model identifies and addresses the underlying mechanisms of disease rather than merely suppressing symptoms.</p>
                                        <p>We utilize advanced testing to uncover biochemical imbalances, nutritional deficiencies, and physiological dysfunction.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Functional+Medicine+Approach", use_column_width=True)
                            
                        elif domain == "Integrative Health":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Integrative health combines evidence-based conventional medicine with complementary approaches that
                                    have substantial research support. Our protocols select the most appropriate interventions from multiple
                                    therapeutic systems.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Evidence-based complementary medicine</strong> - Utilizing validated non-conventional approaches</li>
                                        <li><strong>Mind-body intervention protocols</strong> - Structured approaches to psychophysiological regulation</li>
                                        <li><strong>Traditional healing system integration</strong> - Incorporating validated traditional approaches</li>
                                        <li><strong>Botanical medicine application</strong> - Evidence-supported phytotherapeutic interventions</li>
                                        <li><strong>Manual therapy coordination</strong> - Appropriate referral and integration of bodywork</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Multi-System Approach</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our integrative protocols combine the best of conventional medicine with evidence-supported complementary approaches.</p>
                                        <p>We maintain rigorous standards for inclusion of therapeutic modalities based on both research evidence and clinical utility.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Integrative+Health+Approach", use_column_width=True)
                            
                        elif domain == "Preventive Care":
                            st.markdown("""
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 2; min-width: 300px;">
                                    <p>Preventive care focuses on identifying early warning signs of dysfunction before disease manifestation.
                                    Our approach utilizes advanced screening protocols and risk assessment algorithms to detect subclinical imbalances.</p>
                                    
                                    <h4 style="margin-top: 20px; font-size: 1.1rem;">Key Focus Areas</h4>
                                    <ul>
                                        <li><strong>Predictive biomarker monitoring</strong> - Tracking early indicators of physiological shift</li>
                                        <li><strong>Precision risk assessment</strong> - Personalized evaluation of disease susceptibility</li>
                                        <li><strong>Subclinical dysfunction detection</strong> - Identifying imbalances before symptom development</li>
                                        <li><strong>Targeted prevention protocols</strong> - Specific interventions based on risk profile</li>
                                        <li><strong>Resilience enhancement strategies</strong> - Building physiological and psychological reserve</li>
                                    </ul>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <div style="background-color: rgba(93, 92, 222, 0.1); padding: 20px; border-radius: 10px; height: 100%;">
                                        <h4 style="margin-top: 0; font-size: 1.1rem;">Proactive Health Management</h4>
                                        <div class="professional-separator" style="margin: 10px 0;"></div>
                                        <p>Our preventive approach identifies physiological imbalances before they progress to diagnosable disease states.</p>
                                        <p>We implement targeted interventions based on advanced biomarker patterns and comprehensive risk assessment.</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.image("https://via.placeholder.com/800x300?text=Preventive+Care+Approach", use_column_width=True)
            
            with specialty_tabs[1]:
                st.markdown("""
                <h3 style="margin-bottom: 25px;">Additional Clinical Focus Areas</h3>
                <p style="margin-bottom: 30px;">
                    These specialized areas complement our primary approaches, providing comprehensive
                    support for complex health concerns and specific physiological systems.
                </p>
                """, unsafe_allow_html=True)
                
                # Create a grid layout for secondary domains with enhanced styling
                col1, col2 = st.columns(2)
                
                # First column
                with col1:
                    for domain in dr_jackson.secondary_domains[:3]:
                        with st.container():
                            st.markdown(f"""
                            <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid var(--light-border);">
                                <h3 style="margin-top: 0;">{domain}</h3>
                                <div class="professional-separator"></div>
                            """, unsafe_allow_html=True)
                            
                            if domain == "Nutritional Medicine":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Nutritional medicine utilizes targeted dietary interventions and therapeutic supplementation
                                    based on individual biochemical assessment. Our protocols address specific nutritional imbalances
                                    identified through comprehensive testing.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>Targeted micronutrient repletion</li>
                                        <li>Therapeutic elimination protocols</li>
                                        <li>Metabolic optimization strategies</li>
                                        <li>Personalized dietary planning</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            elif domain == "Stress Management":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Our approach to stress management includes physiological assessment of HPA axis function
                                    alongside evidence-based cognitive and somatic interventions to restore stress response regulation.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>HPA axis regulation protocols</li>
                                        <li>Neuroendocrine rebalancing</li>
                                        <li>Autonomic nervous system restoration</li>
                                        <li>Cognitive-behavioral interventions</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            elif domain == "Hormonal Balance":
                                st.markdown("""
                                <p style="margin-top: 15px;">
                                    Hormonal balance focuses on the complex interrelationships between endocrine systems.
                                    Our protocols assess steroid hormone cascades, thyroid function, and insulin dynamics
                                    to restore optimal regulatory patterns.
                                </p>
                                <div style="background-color: rgba(93, 92, 222, 0.05); padding: 15px; border-radius: 8px; margin-top: 15px;">
                                    <h4 style="margin-top: 0; font-size: 1rem;">Clinical Applications</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li>Comprehensive hormone assessment</li>
                                        <li>Thyroid optimization protocols</li>
                                        <li>Adrenal function restoration</li>
                                        <li>Metabolic hormone regulation</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("""
                            </div>
                            """, unsafe_allow_html=True)
                
                # Second column
                with col2:
                    for domain in dr_jackson.secondary_domains[3:]:
                        with st.container():
                            st.markdown(f"""
                            <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid var(--light-border);">
                                <h3 style="margin-top: 0;">{domain}</h3>
                                <div class="professional-separator"></div>
                            """, unsafe_allow_html                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 2 of 3: Medical Information</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced medical privacy notice
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                <h4 style="color: var(--info-color); margin-top: 0;">Medical Information Privacy</h4>
                <p>Your medical history is protected under HIPAA guidelines and will only be used to provide appropriate clinical care.</p>
                <p style="margin-bottom: 0; font-size: 0.9rem;">This information helps us develop a comprehensive understanding of your health status and will not be shared without your explicit consent.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get the current medical info from session state
            medical_info = st.session_state['patient_medical_info']
            
            # Enhanced form with better visual organization
            with st.form("medical_history_form"):
                # Primary care physician
                st.markdown("<h3 style='margin-top: 0; margin-bottom: 20px;'>Healthcare Provider Information</h3>", unsafe_allow_html=True)
                
                primary_care = st.text_input("Primary Care Physician", 
                                          value=medical_info.primary_care_physician,
                                          placeholder="Name of your current primary care provider")
                
                # Medication information with enhanced styling
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Current Medications</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please list all medications, supplements, and vitamins you are currently taking, including dosage if known.
                </p>
                """, unsafe_allow_html=True)
                
                medications_text = st.text_area(
                    "One medication per line (include dosage if known)", 
                    value="\n".join(medical_info.current_medications) if medical_info.current_medications else "",
                    height=120,
                    placeholder="Example:\nMetformin 500mg twice daily\nVitamin D3 2000 IU daily\nOmega-3 Fish Oil 1000mg daily"
                )
                
                # Allergies with better organization
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Allergies</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    List all known allergies including medications, foods, and environmental triggers. Include reaction type if known.
                </p>
                """, unsafe_allow_html=True)
                
                allergies_text = st.text_area(
                    "Please list all allergies (medications, foods, environmental)", 
                    value="\n".join(medical_info.allergies) if medical_info.allergies else "",
                    height=100,
                    placeholder="Example:\nPenicillin - rash and hives\nPeanuts - anaphylaxis\nPollen - seasonal rhinitis"
                )
                
                # Medical conditions with better visual organization
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Chronic Medical Conditions</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please list all diagnosed medical conditions including approximate date of diagnosis.
                </p>
                """, unsafe_allow_html=True)
                
                conditions_text = st.text_area(
                    "Please list all diagnosed medical conditions", 
                    value="\n".join(medical_info.chronic_conditions) if medical_info.chronic_conditions else "",
                    height=100,
                    placeholder="Example:\nHypertension - diagnosed 2018\nType 2 Diabetes - diagnosed 2020\nMigraine - diagnosed 2015"
                )
                
                # Surgical history with improved styling
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Surgical History</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please list all previous surgeries with approximate dates.
                </p>
                """, unsafe_allow_html=True)
                
                surgeries_text = st.text_area(
                    "Please list all previous surgeries with approximate dates", 
                    value="\n".join(medical_info.past_surgeries) if medical_info.past_surgeries else "",
                    height=100,
                    placeholder="Example:\nAppendectomy - 2010\nKnee arthroscopy - 2019\nTonsillectomy - childhood"
                )
                
                # Family medical history with better visual organization
                st.markdown("""
                <h3 style='margin-top: 25px; margin-bottom: 15px;'>Family Medical History</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please indicate any significant family medical history, specifying the relationship to you.
                </p>
                """, unsafe_allow_html=True)
                
                # Use a more structured approach for family history
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
                            value=value,
                            placeholder=f"e.g., Father, Mother, Sibling"
                        )
                
                # Lifestyle section (added)
                st.markdown("""
                <h3 style='margin-top: 30px; margin-bottom: 15px;'>Lifestyle Information</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    This information helps us develop a more comprehensive understanding of your health status.
                </p>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.selectbox("Exercise Frequency", 
                                 options=["Select an option", "None", "Occasional (1-2 times/week)", 
                                          "Regular (3-4 times/week)", "Frequent (5+ times/week)"],
                                 index=0)
                    st.selectbox("Stress Level", 
                                 options=["Select an option", "Low", "Moderate", "High", "Very High"],
                                 index=0)
                with col2:
                    st.selectbox("Sleep Quality", 
                                 options=["Select an option", "Poor", "Fair", "Good", "Excellent"],
                                 index=0)
                    st.selectbox("Diet Quality", 
                                 options=["Select an option", "Poor", "Fair", "Good", "Excellent"],
                                 index=0)
                
                # Health goals section (added)
                st.markdown("""
                <h3 style='margin-top: 30px; margin-bottom: 15px;'>Health Goals</h3>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please share your main health goals and what you hope to achieve through our care.
                </p>
                """, unsafe_allow_html=True)
                
                health_goals = st.text_area(
                    "Primary health objectives",
                    height=100,
                    placeholder="Example:\nImprove energy levels\nReduce chronic pain\nOptimize sleep quality\nAddress specific health concerns"
                )
                
                # Consent checkboxes with better styling
                st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
                history_consent = st.checkbox(
                    "I confirm that the information provided is accurate and complete to the best of my knowledge", 
                    value=True
                )
                sharing_consent = st.checkbox(
                    "I consent to the appropriate sharing of this information with healthcare providers involved in my care",
                    value=True
                )
                
                # Submit button with professional styling
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Save & Continue", use_container_width=True)
                
                if submitted:
                    # Process and save the data
                    if not (history_consent and sharing_consent):
                        st.error("Please confirm both consent statements to proceed.")
                    else:
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
                        
                        # Success message with professional styling
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Medical History Saved</h4>
                            <p style="margin-bottom: 0;">Your medical history has been securely stored. Thank you for providing this comprehensive information, which will help us deliver personalized care.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Offer navigation to consultation with better styling
                        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                        if st.button("Proceed to Consultation →", use_container_width=True):
                            page = "Consultation"
                            st.experimental_rerun()
            
            # Professional note at bottom
            st.markdown("""
            <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Why We Collect This Information</h4>
                <p style="font-size: 0.9rem; margin-bottom: 0;">
                    Comprehensive medical history allows us to develop personalized care plans based on your unique health profile.
                    This information helps identify patterns, assess risk factors, and determine optimal treatment approaches
                    following evidence-based functional medicine principles.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Consultation":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Professional Consultation</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 3 of 3: Consultation Request</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Check if patient info is filled out
            patient_info = st.session_state['patient_contact_info']
            medical_info = st.session_state['patient_medical_info']
            
            if not patient_info.first_name or not patient_info.last_name:
                # Warning with enhanced styling
                st.markdown("""
                <div style="background-color: rgba(255, 190, 85, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--warning-color);">
                    <h4 style="color: var(--warning-color); margin-top: 0;">Patient Information Required</h4>
                    <p style="margin-bottom: 15px;">Please complete the Patient Intake form before proceeding to consultation.</p>
                """, unsafe_allow_html=True)
                
                if st.button("Go to Patient Intake →", use_container_width=True):
                    page = "Patient Intake"
                    st.experimental_rerun()
                    
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                # Patient information summary with professional styling
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; border: 1px solid var(--light-border); margin-bottom: 30px;">
                    <h3 style="margin-top: 0;">Patient Information Summary</h3>
                    <div class="professional-separator"></div>
                    
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 15px;">
                """, unsafe_allow_html=True)
                
                # Patient details
                st.markdown(f"""
                        <div style="flex: 1; min-width: 250px;">
                            <h4 style="margin-top: 0; font-size: 1rem;">Personal Information</h4>
                            <p style="margin: 5px 0;"><strong>Name:</strong> {patient_info.first_name} {patient_info.last_name}</p>
                            <p style="margin: 5px 0;"><strong>Date of Birth:</strong> {patient_info.date_of_birth}</p>
                            <p style="margin: 5px 0;"><strong>Email:</strong> {patient_info.email}</p>
                            <p style="margin: 5px 0;"><strong>Phone:</strong> {patient_info.phone}</p>
                        </div>
                """, unsafe_allow_html=True)
                
                # Medical summary
                medical_conditions = ", ".join(medical_info.chronic_conditions[:3]) if medical_info.chronic_conditions else "None reported"
                if len(medical_info.chronic_conditions) > 3:
                    medical_conditions += " (and others)"
                    
                medications = ", ".join(medical_info.current_medications[:3]) if medical_info.current_medications else "None reported"
                if len(medical_info.current_medications) > 3:
                    medications += " (and others)"
                    
                allergies = ", ".join(medical_info.allergies[:3]) if medical_info.allergies else "None reported"
                if len(medical_info.allergies) > 3:
                    allergies += " (and others)"
                
                st.markdown(f"""
                        <div style="flex: 1; min-width: 250px;">
                            <h4 style="margin-top: 0; font-size: 1rem;">Medical Summary</h4>
                            <p style="margin: 5px 0;"><strong>Conditions:</strong> {medical_conditions}</p>
                            <p style="margin: 5px 0;"><strong>Medications:</strong> {medications}</p>
                            <p style="margin: 5px 0;"><strong>Allergies:</strong> {allergies}</p>
                            <p style="margin: 5px 0;"><strong>PCP:</strong> {medical_info.primary_care_physician or "Not provided"}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # HIPAA notice with enhanced styling
                st.markdown("""
                <div style="background-color: rgba(90, 160, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                    <h4 style="color: var(--info-color); margin-top: 0;">Consultation Privacy</h4>
                    <p style="margin-bottom: 0;">This consultation is protected under HIPAA guidelines. Information shared during this session is confidential and will be securely stored in your electronic medical record.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced consultation form
                with st.form("consultation_form"):
                    st.markdown("""
                    <h3 style="margin-top: 0; margin-bottom: 20px;">Consultation Request</h3>
                    """, unsafe_allow_html=True)
                    
                    # Primary reason with better styling
                    st.markdown("""
                    <h4 style="margin-bottom: 15px;">Primary Health Concern</h4>
                    <p style="margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);">
                        Please describe your current health concerns in detail. Include symptom duration, severity, and any patterns you've noticed.
                    </p>
                    """, unsafe_allow_html=True)
                    
                    primary_concern = st.text_area(
                        "Health concern description",
                        height=150,
                        placeholder="Please provide a detailed description of your main health concerns...",
                        help="Include symptom duration, severity, and any patterns you've noticed"
                    )
                    
                    # Specialty selection with better organization
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Clinical Focus Area</h4>
                    <p style="margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);">
                        Select the specialty area most relevant to your health concerns.
                    </p>
                    """, unsafe_allow_html=True)
                    
                    specialty_area = st.selectbox(
                        "Select the most relevant specialty area", 
                        options=dr_jackson.primary_domains + dr_jackson.secondary_domains
                    )
                    
                    # Symptom details with better visual organization
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Symptom Details</h4>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        symptom_onset = st.date_input(
                            "When did you first notice these symptoms?",
                            value=datetime.datetime.now().date() - datetime.timedelta(days=30),
                            help="Select the approximate date when symptoms first appeared"
                        )
                    with col2:
                        severity = st.select_slider(
                            "Rate the severity of your symptoms",
                            options=["Mild", "Moderate", "Significant", "Severe", "Extreme"],
                            help="Indicate the overall intensity of your symptoms"
                        )
                    
                    # Additional context with better layout
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Additional Context</h4>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        prior_treatments = st.text_area(
                            "Prior treatments or approaches tried",
                            height=120,
                            placeholder="List any treatments, medications, or approaches you've already attempted..."
                        )
                    with col2:
                        triggers = st.text_area(
                            "Known triggers or patterns",
                            height=120,
                            placeholder="Describe any factors that worsen or improve your symptoms..."
                        )
                    
                    # Goals with better styling
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Treatment Goals</h4>
                    <p style="margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);">
                        What outcomes are you hoping to achieve through this consultation?
                    </p>
                    """, unsafe_allow_html=True)
                    
                    goals = st.text_area(
                        "Desired outcomes",
                        height=120,
                        placeholder="Describe your health goals and expectations from this consultation..."
                    )
                    
                    # Appointment preference (added)
                    st.markdown("""
                    <h4 style="margin-top: 25px; margin-bottom: 15px;">Appointment Preference</h4>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        appointment_type = st.radio(
                            "Preferred consultation type",
                            options=["Virtual (Telehealth)", "In-person Office Visit"],
                            index=0
                        )
                    with col2:
                        urgency = st.select_slider(
                            "Consultation urgency",
                            options=["Standard (within 2 weeks)", "Priority (within 1 week)", "Urgent (within 48 hours)"],
                            value="Standard (within 2 weeks)"
                        )
                    
                    # Enhanced consent checkbox
                    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
                    consultation_consent = st.checkbox(
                        "I understand that this consultation request will be reviewed by Dr. Jackson, and follow-up may be required before treatment recommendations are provided",
                        value=True
                    )
                    
                    # Submit button with better styling
                    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                    submitted = st.form_submit_button("Submit Consultation Request", use_container_width=True)
                
                # Form handling logic
                if submitted:
                    if not primary_concern:
                        st.error("Please describe your health concerns before submitting.")
                    elif not consultation_consent:
                        st.error("Please confirm your understanding of the consultation process.")
                    else:
                        # Success message with professional styling
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Consultation Request Submitted</h4>
                            <p style="margin-bottom: 10px;">Your request has been successfully received and will be reviewed by Dr. Jackson.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display a professional response using the persona
                        st.markdown("""
                        <div style="background-color: var(--off-white); padding: 25px; border-radius: 10px; border: 1px solid var(--light-border); margin-top: 30px;">
                            <h3 style="margin-top: 0;">Initial Assessment</h3>
                            <div class="professional-separator"></div>
                        """, unsafe_allow_html=True)
                        
                        # Determine appropriate recommendations based on specialty area
                        if specialty_area in dr_jackson.primary_domains[:3]:  # First 3 primary domains
                            recommendations = [
                                "Schedule a comprehensive initial evaluation",
                                "Complete the detailed symptom assessment questionnaire",
                                "Prepare any prior lab work or diagnostic studies for review",
                                "Consider keeping a symptom journal for the next 7 days"
                            ]
                        else:
                            recommendations = [
                                "Schedule an initial consultation",
                                "Gather relevant medical records and previous test results",
                                "Complete preliminary health assessment questionnaires",
                                "Prepare a list of specific questions for your consultation"
                            ]
                        
                        # Use the persona to format the response with better styling
                        assessment = f"Based on your initial information regarding {specialty_area.lower()} concerns of {severity.lower()} severity, a professional evaluation is indicated. Your symptoms beginning approximately {(datetime.datetime.now().date() - symptom_onset).days} days ago warrant a thorough assessment."
                        
                        st.markdown(f"""
                            <div style="margin-bottom: 20px;">
                                <h4 style="margin-bottom: 10px; font-size: 1.1rem;">Clinical Overview</h4>
                                <p style="margin-bottom: 5px;"><strong>Presenting Concerns:</strong> {specialty_area} issues with {severity.lower()} symptoms</p>
                                <p style="margin-bottom: 5px;"><strong>Duration:</strong> Approximately {(datetime.datetime.now().date() - symptom_onset).days} days</p>
                                <p style="margin-bottom: 5px;"><strong>Requested Format:</strong> {appointment_type}</p>
                                <p><strong>Urgency Level:</strong> {urgency}</p>
                            </div>
                            
                            <div style="margin-bottom: 20px;">
                                <h4 style="margin-bottom: 10px; font-size: 1.1rem;">Professional Assessment</h4>
                                <p>{assessment}</p>
                            </div>
                            
                            <div>
                                <h4 style="margin-bottom: 10px; font-size: 1.1rem;">Recommendations</h4>
                                <ul>
                        """, unsafe_allow_html=True)
                        
                        for rec in recommendations:
                            st.markdown(f"""
                                <li style="margin-bottom: 8px;">{rec}</li>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("""
                                </ul>
                            </div>
                            
                            <p style="margin-top: 20px; font-style: italic;">Please confirm your understanding of these recommendations and your intent to proceed with the next steps.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Next steps with professional styling
                        st.markdown("""
                        <div style="margin-top: 30px;">
                            <h3>Next Steps</h3>
                            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-top: 15px;">
                                <p style="margin: 0;">You will receive a detailed follow-up within 24-48 hours with additional instructions and appointment scheduling options.</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # AI-assisted note section with professional styling
                        if st.session_state.get('anthropic_api_key') or st.session_state.get('openai_api_key'):
                            st.markdown("""
                            <div style="margin-top: 40px;">
                                <h3>AI-Assisted Clinical Notes</h3>
                                <div style="background-color: var(--off-white); padding: 20px; border-radius: 10px; border: 1px solid var(--light-border); margin-top: 15px;">
                            """, unsafe_allow_html=True)
                            
                            with st.spinner("Generating preliminary clinical notes..."):
                                # This would normally call an LLM API
                                time.sleep(2)  # Simulate processing time
                                
                                st.markdown("""
                                    <h4 style="margin-top: 0; color: var(--primary-color);">PRELIMINARY ASSESSMENT NOTE</h4>
                                    <p style="margin-bottom: 15px;">
                                        Patient presents with concerns related to the selected specialty area. 
                                        Initial impression suggests further evaluation is warranted to establish 
                                        a differential diagnosis and treatment approach. Patient goals and symptom 
                                        presentation will be incorporated into the comprehensive care plan.
                                    </p>
                                    <p style="font-style: italic; font-size: 0.9rem; margin-bottom: 0; color: var(--dark-gray);">
                                        This preliminary note was generated with AI assistance and will be 
                                        reviewed by Dr. Jackson prior to formal documentation.
                                    </p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Additional guidance at bottom of page
                st.markdown("""
                <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                    <h4 style="margin-top: 0;">What to Expect</h4>
                    <p style="font-size: 0.9rem; margin-bottom: 0;">
                        After submitting your consultation request, our clinical team will review your information and 
                        reach out to schedule your appointment. For urgent medical concerns requiring immediate attention, 
                        please contact your primary care provider or visit the nearest emergency department.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        elif page == "Chat with Dr. Jackson":
            # Professional header
            st.markdown("""
            <h1>Professional Chat Consultation</h1>
            <div class="professional-separator" style="width: 150px; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
                
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--tertiary-color);
        font-weight: 500;
    }
    
    /* Alert/Notice Styling */
    .info-box {
        background-color: rgba(90, 160, 255, 0.1);
        border-left: 4px solid var(--info-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .success-box {
        background-color: rgba(61, 201, 161, 0.1);
        border-left: 4px solid var(--success-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .warning-box {
        background-color: rgba(255, 190, 85, 0.1);
        border-left: 4px solid var(--warning-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    .error-box {
        background-color: rgba(255, 90, 90, 0.1);
        border-left: 4px solid var(--error-color);
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }
    
    /* Progress Bar Styling */
    [data-testid="stProgressBar"] > div {
        background-color: var(--primary-color);
        height: 8px;
        border-radius: 4px;
    }
    
    [data-testid="stProgressBar"] > div:nth-child(1) {
        background-color: var(--light-gray);
    }
    
    /* Section Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            rgba(0,0,0,0), 
            var(--medium-gray), 
            rgba(0,0,0,0));
    }
    
    .dark-mode hr {
        background: linear-gradient(90deg, 
            rgba(0,0,0,0), 
            var(--dark-border), 
            rgba(0,0,0,0));
    }
    
    /* Info Cards Grid */
    .info-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 16px;
        margin: 20px 0;
    }
    
    .info-card {
        background-color: var(--off-white);
        border-radius: 8px;
        border: 1px solid var(--light-border);
        padding: 20px;
        transition: all 0.2s ease;
    }
    
    .info-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    .dark-mode .info-card {
        background-color: var(--dark-mode-card);
        border: 1px solid var(--dark-border);
    }
    
    .dark-mode .info-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Custom Utility Classes */
    .text-center {
        text-align: center;
    }
    
    .mb-0 {
        margin-bottom: 0 !important;
    }
    
    .mt-0 {
        margin-top: 0 !important;
    }
    
    .professional-separator {
        height: 5px;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        margin: 12px 0;
        border-radius: 3px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional App Header with Logo
    st.markdown(f"""
    <div class="professional-header">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h1>Dr. Jackson, {dr_jackson.credentials}</h1>
                <p>{dr_jackson.practice_name}</p>
            </div>
            <div style="text-align: right;">
                <p style="font-size: 0.9rem; opacity: 0.8;">Advancing Integrative Medicine</p>
                <p style="font-size: 0.8rem; opacity: 0.7;">Established 2015</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Professionally designed sidebar
    with st.sidebar:
        # Add a subtle medical/professional icon or logo
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); 
                       width: 60px; height: 60px; border-radius: 50%; display: inline-flex; 
                       align-items: center; justify-content: center; margin-bottom: 10px;">
                <span style="color: white; font-size: 30px;">🩺</span>
            </div>
            <p style="font-weight: 600; margin: 0; font-size: 16px;">Dr. Jackson Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='margin-top: 0;'>Navigation</h3>", unsafe_allow_html=True)
        
        # Enhanced navigation with section grouping
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; color: var(--dark-gray);'>Patient Portal</p>", unsafe_allow_html=True)
        patient_page = st.radio("", [
            "Home", 
            "Patient Intake", 
            "Medical History",
            "Consultation"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>Communication</p>", unsafe_allow_html=True)
        communication_page = st.radio("", [
            "Chat with Dr. Jackson"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>Information</p>", unsafe_allow_html=True)
        info_page = st.radio("", [
            "Specialties", 
            "Approach",
            "Resources"
        ], label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: 600; margin-bottom: 5px; margin-top: 15px; color: var(--dark-gray);'>System</p>", unsafe_allow_html=True)
        system_page = st.radio("", [
            "Settings"
        ], label_visibility="collapsed")
        
        # Determine selected page from all radio groups
        if patient_page != "Home":
            page = patient_page
        elif communication_page != "Chat with Dr. Jackson":
            page = "Chat with Dr. Jackson"
        elif info_page != "Specialties":
            page = info_page
        elif system_page != "Settings":
            page = system_page
        else:
            page = "Home"
        
        # Theme selection with better design
        st.markdown("---")
        st.markdown("<h4 style='margin-bottom: 10px;'>Appearance</h4>", unsafe_allow_html=True)
        theme_cols = st.columns([1, 3])
        with theme_cols[0]:
            st.markdown("🎨")
        with theme_cols[1]:
            theme = st.selectbox("", ["Light", "Dark"], label_visibility="collapsed")
        
        if theme == "Dark":
            st.markdown("""
            <script>
                document.body.classList.add('dark-mode');
            </script>
            """, unsafe_allow_html=True)
        
        # Professional info section
        st.markdown("---")
        st.markdown("<h4 style='margin-bottom: 10px;'>About Dr. Jackson</h4>", unsafe_allow_html=True)
        
        # More professional specialty display
        domains = ", ".join(dr_jackson.primary_domains[:3])
        st.markdown(f"""
        <div style="background-color: var(--off-white); padding: 12px; border-radius: 8px; border: 1px solid var(--light-border); margin-bottom: 15px;">
            <p style="font-weight: 500; margin-bottom: 5px;">Specializing in:</p>
            <p style="color: var(--primary-color); font-weight: 600; margin: 0;">{domains}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Current date - maintaining professional approach
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background-color: var(--primary-color); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                <span style="color: white;">📅</span>
            </div>
            <div>
                <p style="font-size: 0.85rem; margin: 0; opacity: 0.7;">Today's Date</p>
                <p style="font-weight: 500; margin: 0;">{current_date}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show logged in status if patient info exists
        patient_info = st.session_state['patient_contact_info']
        if patient_info.first_name and patient_info.last_name:
            st.markdown(f"""
            <div style="background-color: rgba(61, 201, 161, 0.1); border-left: 4px solid var(--success-color); padding: 12px; border-radius: 6px;">
                <p style="font-weight: 500; margin: 0;">Logged in as:</p>
                <p style="margin: 5px 0 0 0;">{patient_info.first_name} {patient_info.last_name}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Container for main content with professional layout
    main_container = st.container()
    with main_container:
        # Main content area based on page selection
        if page == "Home":
            st.header("Welcome to Dr. Jackson's Professional Consultation")
            
            # Enhanced HIPAA Notice with more professional design
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; 
                       border-left: 5px solid var(--info-color); margin-bottom: 30px;">
                <h4 style="color: var(--info-color); margin-top: 0;">HIPAA Compliance Notice</h4>
                <p style="margin-bottom: 10px;">This application complies with the Health Insurance Portability and Accountability Act (HIPAA) of 1996:</p>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                    <li style="margin-bottom: 5px;">All patient data is encrypted in transit and at rest</li>
                    <li style="margin-bottom: 5px;">Access controls restrict unauthorized viewing of protected health information (PHI)</li>
                    <li style="margin-bottom: 5px;">Audit logs track all data access and modifications</li>
                    <li style="margin-bottom: 5px;">Data retention policies comply with medical record requirements</li>
                    <li style="margin-bottom: 5px;">Regular security assessments are conducted to ensure compliance</li>
                </ul>
                <p style="margin-top: 10px; margin-bottom: 0; font-weight: 500;"><span style="color: var(--info-color);">Privacy Officer Contact:</span> privacy@optimumwellness.org</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Featured specialties in cards layout
            st.markdown("### Our Clinical Specialties")
            st.markdown("""
            <p style="margin-bottom: 25px;">Dr. Jackson's practice provides comprehensive medical consultation with expertise in the following areas:</p>
            """, unsafe_allow_html=True)
            
            # Create a grid layout with cards for specialties
            st.markdown("""
            <div class="info-card-grid">
            """, unsafe_allow_html=True)
            
            for domain in dr_jackson.primary_domains:
                icon = "🧠" if domain == "Psychiatric Care" else "✨" if domain == "Wellness Optimization" else "⏱️" if domain == "Anti-aging Medicine" else "🔬" if domain == "Functional Medicine" else "🌿" if domain == "Integrative Health" else "🛡️"
                
                st.markdown(f"""
                <div class="info-card">
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                            <span style="font-size: 20px;">{icon}</span>
                        </div>
                        <h4 style="margin: 0; color: var(--primary-color);">{domain}</h4>
                    </div>
                    <div class="professional-separator"></div>
                    <p style="margin-top: 10px; font-size: 0.9rem;">Comprehensive, evidence-based approach to {domain.lower()} through integrated assessment and personalized protocols.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Professional approach section with better design
            st.markdown("### Professional Approach")
            
            # Two-column layout for approach and values
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 12px; border: 1px solid var(--light-border); height: 100%;">
                    <h4 style="margin-top: 0;">Clinical Methodology</h4>
                    <div class="professional-separator"></div>
                    <p>Dr. Jackson's practice is built on a hierarchical approach to medical knowledge and evidence:</p>
                    <ul>
                        <li><strong>Evidence-based research</strong> forms the foundation of all clinical decisions</li>
                        <li><strong>Clinical guidelines</strong> provide standardized frameworks for treatment protocols</li>
                        <li><strong>Professional experience</strong> guides the application of research to individual cases</li>
                        <li><strong>Holistic assessment</strong> ensures comprehensive evaluation of all contributing factors</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background-color: var(--off-white); padding: 20px; border-radius: 12px; border: 1px solid var(--light-border); height: 100%;">
                    <h4 style="margin-top: 0;">Core Values</h4>
                    <div class="professional-separator"></div>
                    <ul>
                """, unsafe_allow_html=True)
                
                for i, value in enumerate(dr_jackson.core_values[:4]):
                    st.markdown(f"""
                    <li style="margin-bottom: 10px;">
                        <strong style="color: var(--primary-color);">{value}:</strong> 
                        Ensuring the highest standards of care through rigorous application of professional principles
                    </li>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Call to action section with enhanced design
            st.markdown("""
            <h3 style="margin-bottom: 20px;">Begin Your Care Journey</h3>
            <div style="background: linear-gradient(135deg, rgba(93, 92, 222, 0.1) 0%, rgba(93, 92, 222, 0.05) 100%); 
                 padding: 30px; border-radius: 12px; margin-bottom: 30px; border: 1px solid rgba(93, 92, 222, 0.2);">
                <p style="font-size: 1.1rem; margin-bottom: 20px;">
                    To begin the consultation process, please complete the Patient Intake forms first. This will help us provide
                    the most appropriate clinical guidance tailored to your specific health needs.
                </p>
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("📋 Go to Patient Intake", key="home_intake_btn"):
                page = "Patient Intake"
                st.experimental_rerun()
                
            st.markdown("""
                    </div>
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("🔍 Learn About Specialties", key="home_specialties_btn"):
                page = "Specialties"
                st.experimental_rerun()
                
            st.markdown("""
                    </div>
                    <div>
            """, unsafe_allow_html=True)
            
            if st.button("💬 Chat with Dr. Jackson", key="home_chat_btn"):
                page = "Chat with Dr. Jackson"
                st.experimental_rerun()
            
            st.markdown("""
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Testimonials or professional credentials section
            st.markdown("""
            <div style="background-color: var(--off-white); padding: 25px; border-radius: 12px; border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Professional Credentials</h4>
                <div class="professional-separator"></div>
                <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 15px;">
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">🎓</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Education</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Doctorate in Nursing Practice</p>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">📜</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Certification</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Family Nurse Practitioner-Certified</p>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: rgba(93, 92, 222, 0.1); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 20px;">🔬</span>
                            </div>
                            <div>
                                <p style="font-weight: 600; margin: 0;">Specialization</p>
                                <p style="margin: 2px 0 0 0; font-size: 0.9rem;">Certified Functional Medicine Practitioner</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Patient Intake":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Patient Intake Form</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: 5px; border-radius: 3px;"></div>
                </div>
                <p style="margin-top: 10px; color: var(--dark-gray);">Step 1 of 3: Contact Information</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced data privacy notice
            st.markdown("""
            <div style="background-color: rgba(90, 160, 255, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid var(--info-color);">
                <h4 style="color: var(--info-color); margin-top: 0;">Data Privacy Notice</h4>
                <p>All information submitted is encrypted and protected in accordance with HIPAA regulations.
                Your privacy is our priority. Information is only accessible to authorized medical personnel.</p>
                <p style="margin-bottom: 0; font-size: 0.9rem;"><strong>Security Measures:</strong> End-to-end encryption, secure database storage, access control mechanisms</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get the current patient info from session state
            patient_info = st.session_state['patient_contact_info']
            
            # Create the form with enhanced styling
            with st.form("patient_contact_form"):
                st.markdown("""
                <h3 style="margin-top: 0; margin-bottom: 20px;">Personal Information</h3>
                """, unsafe_allow_html=True)
                
                # Name information with professional layout
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name*", value=patient_info.first_name,
                                            placeholder="Enter your legal first name")
                with col2:
                    last_name = st.text_input("Last Name*", value=patient_info.last_name,
                                          placeholder="Enter your legal last name")
                
                # Contact information with more structured layout
                st.markdown("<h4 style='margin-top: 25px; margin-bottom: 15px;'>Contact Details</h4>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2,2,1])
                with col1:
                    email = st.text_input("Email Address*", value=patient_info.email,
                                        placeholder="Your primary email address")
                with col2:
                    phone = st.text_input("Phone Number*", value=patient_info.phone,
                                        placeholder="Format: (XXX) XXX-XXXX")
                with col3:
                    dob = st.date_input("Date of Birth*", 
                                    value=patient_info.date_of_birth or datetime.datetime.now().date() - datetime.timedelta(days=365*30),
                                    help="Select your date of birth from the calendar")
                
                # Address information with better visual grouping
                st.markdown("<h4 style='margin-top: 25px; margin-bottom: 15px;'>Address Information</h4>", unsafe_allow_html=True)
                
                st.text_input("Street Address", value=patient_info.address,
                            placeholder="Enter your current street address")
                
                col1, col2, col3 = st.columns([2,1,1])
                with col1:
                    city = st.text_input("City", value=patient_info.city,
                                      placeholder="Your city of residence")
                with col2:
                    state = st.text_input("State", value=patient_info.state,
                                       placeholder="State abbreviation")
                with col3:
                    zip_code = st.text_input("ZIP Code", value=patient_info.zip_code,
                                          placeholder="5-digit ZIP code")
                
                # Emergency contact with visual separation
                st.markdown("""
                <h4 style='margin-top: 25px; margin-bottom: 15px;'>Emergency Contact</h4>
                <p style='margin-bottom: 15px; font-size: 0.9rem; color: var(--dark-gray);'>
                    Please provide a contact person in case of emergency.
                </p>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    emergency_name = st.text_input("Emergency Contact Name", 
                                                value=patient_info.emergency_contact_name,
                                                placeholder="Full name of emergency contact")
                with col2:
                    emergency_phone = st.text_input("Emergency Contact Phone", 
                                                 value=patient_info.emergency_contact_phone,
                                                 placeholder="Emergency contact's phone number")
                
                # Required fields notice
                st.markdown("""
                <p style='margin-top: 25px; font-size: 0.9rem;'>* Required fields</p>
                """, unsafe_allow_html=True)
                
                # Enhanced consent checkbox
                consent = st.checkbox("I confirm that the information provided is accurate and complete to the best of my knowledge",
                                   value=True)
                
                # Submit button with professional styling
                submitted = st.form_submit_button("Save & Continue")
                
                if submitted:
                    # Validate required fields
                    if not (first_name and last_name and email and phone and dob and consent):
                        st.error("Please fill out all required fields and confirm your consent.")
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
                        
                        # Success message with more professional design
                        st.markdown("""
                        <div style="background-color: rgba(61, 201, 161, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid var(--success-color); margin-top: 20px;">
                            <h4 style="color: var(--success-color); margin-top: 0;">Information Saved Successfully</h4>
                            <p style="margin-bottom: 0;">Your contact information has been securely stored. Please proceed to the Medical History form.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Offer navigation to next form
                        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                        if st.button("Continue to Medical History →", use_container_width=True):
                            page = "Medical History"
                            st.experimental_rerun()
            
            # Professional guidance note at the bottom
            st.markdown("""
            <div style="margin-top: 40px; padding: 15px; border-radius: 10px; background-color: var(--off-white); border: 1px solid var(--light-border);">
                <h4 style="margin-top: 0;">Privacy & Security</h4>
                <p style="margin-bottom: 0; font-size: 0.9rem;">
                    All information provided is protected by our privacy policy and HIPAA regulations. Your data is encrypted and access is restricted
                    to authorized healthcare professionals involved in your care. For questions about our privacy practices,
                    please contact our Privacy Officer at privacy@optimumwellness.org.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        elif page == "Medical History":
            # Professional header with progress indicator
            st.markdown("""
            <div style="margin-bottom: 30px;">
                <h1>Medical History Form</h1>
                <div style="display: flex; margin-top: 15px;">
                    <div style="flex: 1; background-color: var(--success-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--primary-color); height: 5px; border-radius: 3px; margin-right: 5px;"></div>
                    <div style="flex: 1; background-color: var(--light-gray); height: import streamlit as st
from typing import Dict, List, Union, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import datetime
import random
import time
import json

# Define core persona elements as structured data
class PriorityLevel(Enum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

@dataclass
class ResponseFormat:
    steps: List[str]
    style: Dict[str, str]

@dataclass
class ChatMessage:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

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
        
        # Chat responses for various medical topics
        self.chat_responses = {
            "wellness": [
                "In our clinical approach to wellness optimization, we emphasize the integration of evidence-based lifestyle modifications with targeted interventions. The foundation begins with comprehensive assessment of metabolic, hormonal, and inflammatory markers.",
                "From a functional medicine perspective, wellness requires addressing root causes rather than symptom suppression. Our protocol typically evaluates sleep quality, nutritional status, stress management, and physical activity patterns as foundational elements.",
                "The current medical literature supports a multifaceted approach to wellness. This includes structured nutritional protocols, strategic supplementation based on identified deficiencies, and cognitive-behavioral interventions for stress management."
            ],
            "nutrition": [
                "Nutritional medicine forms a cornerstone of our functional approach. Current research indicates that personalized nutrition based on metabolic typing and inflammatory markers yields superior outcomes compared to generalized dietary recommendations.",
                "In our clinical practice, we utilize advanced nutritional assessments including micronutrient testing, food sensitivity panels, and metabolic markers to develop precision nutritional protocols tailored to individual biochemistry.",
                "The evidence supports targeted nutritional interventions rather than generalized approaches. We typically begin with elimination of inflammatory triggers, followed by structured reintroduction to identify optimal nutritional parameters."
            ],
            "sleep": [
                "Sleep optimization is fundamental to our clinical approach. Current research demonstrates that disrupted sleep architecture significantly impacts hormonal regulation, inflammatory markers, and cognitive function.",
                "Our protocol for sleep enhancement includes comprehensive assessment of circadian rhythm disruptions, evaluation of potential obstructive patterns, and analysis of neurochemical imbalances that may interfere with normal sleep progression.",
                "Evidence-based interventions for sleep quality improvement include structured sleep hygiene protocols, environmental optimization, and when indicated, targeted supplementation to address specific neurotransmitter imbalances."
            ],
            "stress": [
                "From a functional medicine perspective, chronic stress activation represents a significant driver of inflammatory processes and hormonal dysregulation. Our approach focuses on quantifiable assessment of HPA axis function.",
                "The clinical literature supports a structured approach to stress management, incorporating both physiological and psychological interventions. We utilize validated assessment tools to measure stress response patterns.",
                "Our protocol typically includes targeted adaptogenic support, structured cognitive reframing techniques, and autonomic nervous system regulation practices, all customized based on individual response patterns."
            ],
            "aging": [
                "Anti-aging medicine is approached from a scientific perspective in our practice. The focus remains on measurable biomarkers of cellular health, including telomere dynamics, oxidative stress parameters, and glycation endpoints.",
                "Current research supports interventions targeting specific aging mechanisms rather than general approaches. Our protocol evaluates mitochondrial function, inflammatory status, and hormonal optimization within physiological parameters.",
                "The evidence demonstrates that targeted interventions for biological age reduction must be personalized. We utilize comprehensive biomarker assessment to develop precision protocols for cellular rejuvenation."
            ],
            "hormones": [
                "Hormonal balance requires a comprehensive systems-based approach. Current clinical research indicates that evaluating the full spectrum of endocrine markers yields superior outcomes compared to isolated hormone assessment.",
                "Our protocol includes evaluation of steroid hormone pathways, thyroid function, and insulin dynamics. The integration of these systems provides a more accurate clinical picture than isolated assessment.",
                "Evidence-based hormonal optimization focuses on restoration of physiological patterns rather than simple supplementation. We utilize chronobiological principles to restore natural hormonal rhythms."
            ],
            "inflammation": [
                "Chronic inflammation represents a common pathway in numerous pathological processes. Our clinical approach includes comprehensive assessment of inflammatory markers and mediators to identify specific activation patterns.",
                "The research supports targeted anti-inflammatory protocols based on identified triggers rather than generalized approaches. We evaluate environmental, nutritional, and microbial factors in our assessment.",
                "Our evidence-based protocol typically includes elimination of inflammatory triggers, gastrointestinal barrier restoration, and targeted nutritional interventions to modulate specific inflammatory pathways."
            ],
            "detoxification": [
                "Detoxification capacity represents a critical element in our functional medicine assessment. We evaluate phase I and phase II detoxification pathways through validated biomarkers rather than generalized assumptions.",
                "The clinical evidence supports structured protocols for enhancing physiological detoxification processes. Our approach includes assessment of toxic burden alongside metabolic detoxification capacity.",
                "Our protocol typically includes strategic nutritional support for specific detoxification pathways, reduction of exposure sources, and enhancement of elimination mechanisms through validated clinical interventions."
            ],
            "gut_health": [
                "Gastrointestinal function serves as a cornerstone in our clinical assessment. Current research demonstrates the central role of gut integrity, microbiome diversity, and digestive efficiency in systemic health outcomes.",
                "Our protocol includes comprehensive evaluation of digestive function, intestinal permeability, microbial balance, and immunological markers to develop precision interventions for gastrointestinal optimization.",
                "The evidence supports a structured approach to gastrointestinal restoration, including targeted elimination of pathogenic factors, reestablishment of beneficial microbial communities, and restoration of mucosal integrity."
            ],
            "default": [
                "I would need to conduct a more thorough clinical assessment to provide specific recommendations regarding your inquiry. Our practice emphasizes evidence-based approaches customized to individual patient presentations.",
                "From a functional medicine perspective, addressing your concerns would require comprehensive evaluation of relevant biomarkers and clinical parameters. This allows for development of targeted interventions based on identified mechanisms.",
                "The current medical literature supports an individualized approach to your clinical question. Our protocol would include assessment of relevant systems followed by development of a structured intervention strategy."
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
    
    def get_chat_response(self, query: str) -> str:
        """Generates a chat response based on the query content"""
        # Determine the topic based on keywords in the query
        query_lower = query.lower()
        
        # Check for topic matches
        if any(word in query_lower for word in ["wellness", "well-being", "wellbeing", "health optimization"]):
            responses = self.chat_responses["wellness"]
        elif any(word in query_lower for word in ["nutrition", "diet", "food", "eating"]):
            responses = self.chat_responses["nutrition"]
        elif any(word in query_lower for word in ["sleep", "insomnia", "rest", "fatigue"]):
            responses = self.chat_responses["sleep"]
        elif any(word in query_lower for word in ["stress", "anxiety", "overwhelm", "burnout"]):
            responses = self.chat_responses["stress"]
        elif any(word in query_lower for word in ["aging", "longevity", "anti-aging"]):
            responses = self.chat_responses["aging"]
        elif any(word in query_lower for word in ["hormone", "thyroid", "estrogen", "testosterone"]):
            responses = self.chat_responses["hormones"]
        elif any(word in query_lower for word in ["inflammation", "inflammatory", "autoimmune"]):
            responses = self.chat_responses["inflammation"]
        elif any(word in query_lower for word in ["detox", "toxin", "cleanse"]):
            responses = self.chat_responses["detoxification"]
        elif any(word in query_lower for word in ["gut", "digestive", "stomach", "intestine", "microbiome"]):
            responses = self.chat_responses["gut_health"]
        else:
            responses = self.chat_responses["default"]
        
        # Select a response from the appropriate category
        return random.choice(responses)

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

def display_chat_message(message: ChatMessage):
    """Display a single chat message with appropriate styling"""
    if message.role == "assistant":
        with st.chat_message("assistant", avatar="🩺"):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%I:%M %p')}")
    else:  # user message
        with st.chat_message("user"):
            st.markdown(message.content)
            st.caption(f"{message.timestamp.strftime('%I:%M %p')}")

# Function to get descriptions for DEI focus areas
def get_dei_description(focus):
    descriptions = {
        "Maintain awareness of healthcare disparities": "We actively monitor and address inequities in healthcare access, treatment, and outcomes across different populations.",
        "Provide culturally competent care": "Our approach incorporates cultural factors and beliefs that may impact health behaviors and treatment preferences.",
        "Consider LGBTQ+ health perspectives": "We acknowledge unique health concerns and create supportive care environments for LGBTQ+ individuals.",
        "Implement inclusive language": "Our communications use terminology that respects diversity of identity, experience, and background.",
        "Address systemic healthcare barriers": "We work to identify and minimize structural obstacles that prevent equitable access to quality care."
    }
    return descriptions.get(focus, "")

# Function to get descriptions for intervention hierarchy
def get_hierarchy_description(hierarchy):
    descriptions = {
        "Remove pathological triggers": "Identify and eliminate factors that activate or perpetuate dysfunction",
        "Restore physiological function": "Support normal biological processes through targeted interventions",
        "Rebalance regulatory systems": "Address control mechanisms that coordinate multiple physiological processes",
        "Regenerate compromised tissues": "Support cellular renewal and structural integrity where needed",
        "Reestablish health maintenance": "Implement sustainable strategies for ongoing wellbeing"
    }
    return descriptions.get(hierarchy, "")

# Streamlit Application Implementation
def main():
    st.set_page_config(
        page_title="Dr. Jackson DNP - Medical Professional Consultation",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Dr. Jackson DNP - Professional Medical Consultation Platform",
            'Report a bug': "mailto:support@drjackson-platform.org",
            'Get help': "https://drjackson-platform.org/help"
        }
    )
    
    # Initialize persona and settings
    dr_jackson = DrJacksonPersona()
    llm_settings = LLMSettings()
    
    # Initialize session state for patient data if not exist
    if 'patient_contact_info' not in st.session_state:
        st.session_state['patient_contact_info'] = PatientContactInfo()
    if 'patient_medical_info' not in st.session_state:
        st.session_state['patient_medical_info'] = PatientMedicalInfo()
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    # Custom CSS for theming and professional layout
    st.markdown("""
    <style>
    :root {
        --primary-color: #5D5CDE;
        --secondary-color: #4B4BA3;
        --tertiary-color: #E0E0FA;
        --accent-color: #FF7D54;
        --light-bg: #FFFFFF;
        --off-white: #F8F9FA;
        --light-gray: #E9ECEF;
        --medium-gray: #CED4DA;
        --dark-gray: #6C757D;
        --dark-bg: #181818;
        --dark-mode-card: #2C2C2C;
        --light-text: #333333;
        --dark-text: #E5E5E5;
        --light-border: #E2E8F0;
        --dark-border: #374151;
        --light-input: #F9FAFB;
        --dark-input: #1F2937;
        --success-color: #3DC9A1;
        --warning-color: #FFBE55;
        --error-color: #FF5A5A;
        --info-color: #5AA0FF;
    }
    
    /* Base Styling */
    .stApp {
        background-color: var(--light-bg);
        color: var(--light-text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .dark-mode .stApp {
        background-color: var(--dark-bg);
        color: var(--dark-text);
    }
    
    /* Typography Refinements */
    h1 {
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.01em;
        color: var(--primary-color);
        margin-bottom: 1rem;
    }
    
    h2 {
        font-weight: 600;
        font-size: 1.8rem;
        letter-spacing: -0.01em;
        color: var(--primary-color);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-weight: 600;
        font-size: 1.4rem;
        color: var(--primary-color);
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    p, li {
        font-size: 1rem;
        line-height: 1.6;
        color: var(--light-text);
    }
    
    .dark-mode p, .dark-mode li {
        color: var(--dark-text);
    }
    
    /* Card/Container Styling */
    div[data-testid="stForm"] {
        background-color: var(--off-white);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        border: 1px solid var(--light-border);
        margin-bottom: 24px;
    }
    
    .dark-mode div[data-testid="stForm"] {
        background-color: var(--dark-mode-card);
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        border: 1px solid var(--dark-border);
    }
    
    /* Expander Styling */
    details {
        background-color: var(--off-white);
        border-radius: 8px;
        border: 1px solid var(--light-border);
        margin-bottom: 16px;
        overflow: hidden;
    }
    
    .dark-mode details {
        background-color: var(--dark-mode-card);
        border: 1px solid var(--dark-border);
    }
    
    details summary {
        padding: 16px;
        cursor: pointer;
        font-weight: 500;
    }
    
    details summary:hover {
        background-color: var(--light-gray);
    }
    
    .dark-mode details summary:hover {
        background-color: rgba(255,255,255,0.05);
    }
    
    /* Button Styling */
    .stButton button {
        background-color: var(--primary-color);
        color: white;
        font-weight: 500;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--off-white);
        border-right: 1px solid var(--light-border);
    }
    
    .dark-mode [data-testid="stSidebar"] {
        background-color: var(--dark-mode-card);
        border-right: 1px solid var(--dark-border);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 1.5rem;
    }
    
    /* Header Styling */
    .professional-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 15px rgba(93, 92, 222, 0.25);
    }
    
    .professional-header h1 {
        color: white;
        margin-bottom: 0.5rem;
        font-size: 2.4rem;
    }
    
    .professional-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* HIPAA Notice Styling */
    .hipaa-notice {
        background-color: var(--tertiary-color);
        border-left: 4px solid var(--primary-color);
        padding: 16px;
        margin: 20px 0;
        border-radius: 6px;
    }
    
    .dark-mode .hipaa-notice {
        background-color: rgba(93, 92, 222, 0.15);
    }
    
    /* Chat Styling */
    .chat-container {
        border-radius: 12px;
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border: 1px solid var(--light-border);
        background-color: var(--off-white);
    }
    
    .dark-mode .chat-container {
        border: 1px solid var(--dark-border);
        background-color: var(--dark-mode-card);
    }
    
    /* Chat Message Styling */
    [data-testid="stChatMessage"] {
        padding: 0.75rem 0;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
        background-color: var(--light-gray);
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
        background-color: var(--primary-color);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 10px 16px;
        background-color: var(--light-gray);
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color

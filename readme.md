# Dr. Jackson DNP Medical Consultation Platform

A comprehensive Streamlit-based application for medical consultations featuring Dr. Jackson's professional persona, HIPAA compliance, and LLM integration.

## Overview

This application provides a professional interface for medical consultations with Dr. Jackson, a medical professional specializing in:

- Psychiatric Care
- Wellness Optimization
- Anti-aging Medicine
- Functional Medicine
- Integrative Health
- Preventive Care

The platform maintains strict professional boundaries, prioritizes patient advocacy, and implements a formal clinical communication framework.

## Key Features

- **Patient Intake Forms**: Comprehensive collection of patient information
- **Medical History Collection**: Detailed medical history recording
- **Consultation System**: Professional consultation request and management
- **HIPAA Compliance**: Built-in privacy notices and security measures
- **Professional Resources**: Educational materials for patients
- **LLM Integration**: API connections to Anthropic, OpenAI, Meta, and XAI for clinical assistance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-organization/dr-jackson-platform.git
cd dr-jackson-platform
```

2. Create and activate a virtual environment (Python 3.12 recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file for environment variables:
```bash
touch .env
```

5. Add your API keys to the `.env` file:
```
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
META_API_KEY=your_key_here
XAI_API_KEY=your_key_here
```

## Usage

Run the Streamlit application:

```bash
streamlit run dr_jackson_streamlit.py
```

Navigate to the displayed URL (typically http://localhost:8501) in your web browser.

## Application Structure

- **Home**: Introduction to Dr. Jackson's practice
- **Patient Intake**: Form for collecting patient contact information
- **Medical History**: Form for collecting detailed medical history
- **Consultation**: Interface for submitting consultation requests
- **Specialties**: Information about Dr. Jackson's areas of expertise
- **Approach**: Details about Dr. Jackson's professional methodology
- **Resources**: Educational materials for patients
- **Settings**: Configure LLM API keys and user preferences

## HIPAA Compliance

This application implements various HIPAA compliance measures:

- Encryption for patient data
- Role-based access controls
- Audit logging
- Security notices
- Privacy disclosures

## Development

### Core Components

- `DrJacksonPersona`: Core class implementing the professional persona
- `PatientContactInfo`: Data structure for patient contact information
- `PatientMedicalInfo`: Data structure for medical history
- `LLMSettings`: Management of AI integration settings

### Additional Development

Areas for expansion:

1. Add database integration for persistent storage
2. Implement user authentication and role-based access
3. Add telemedicine/video consultation capabilities
4. Develop reporting and analytics features
5. Enhance LLM integrations for more sophisticated clinical assistance

## License

[Insert your license information here]

## Contact

For more information, please contact:

- Email: info@drjackson-platform.org
- Website: https://drjackson-platform.org

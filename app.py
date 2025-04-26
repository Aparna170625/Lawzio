import streamlit as st
import time
import os
from utils.document_processor import process_document
from utils.openai_helper import OpenAIHelper
from utils.translator import TranslationHelper
from utils.risk_assessment import assess_risk_level, get_risk_color
from utils.localization import get_ui_text
from utils.database import (
    save_document_history, 
    save_document_summary, 
    get_recent_documents,
    get_document_with_risk_factors,
    get_document_summaries,
    get_document_text,
    get_privacy_settings,
    update_privacy_settings,
    delete_document_by_token
)

# Set page configuration
st.set_page_config(
    page_title="Lawzio - Legal Document Summarizer",
    page_icon="⚖️",
    layout="wide",
)

# Add custom styling to make Lawzio colorful and professional
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(to right, #ffffff, #f7f8fa);
    }

    .big-title {
        font-size: 48px;
        color: #2E86C1;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 24px;
        color: #117864;
        text-align: center;
        margin-bottom: 30px;
    }

    .upload-box {
        border: 2px dashed #0066CC;
        padding: 20px;
        border-radius: 10px;
        background-color: #eaf4ff;
        margin-bottom: 20px;
    }

    .button-style {
        background-color: #0066CC;
        color: white;
        border-radius: 8px;
        font-size: 18px;
        padding: 10px 20px;
    }

    .button-style:hover {
        background-color: #0052a3;
    }

    .risk-high {
        background-color: #CB4335;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
    }
    .risk-medium {
        background-color: #FF9800;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
    }
    .risk-low {
        background-color: #00C853;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'document_text' not in st.session_state:
    st.session_state.document_text = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'translated_summary' not in st.session_state:
    st.session_state.translated_summary = None
if 'detail_level' not in st.session_state:
    st.session_state.detail_level = "detailed"
if 'target_language' not in st.session_state:
    st.session_state.target_language = "english"
if 'ui_language' not in st.session_state:
    st.session_state.ui_language = "english"  # Default UI language
if 'risk_level' not in st.session_state:
    st.session_state.risk_level = None
if 'risk_factors' not in st.session_state:
    st.session_state.risk_factors = []

# Initialize helpers
@st.cache_resource
def get_openai_helper():
    return OpenAIHelper()

@st.cache_resource
def get_translation_helper():
    helper = TranslationHelper()
    # Store translation capabilities in session state
    if 'translation_methods' not in st.session_state:
        st.session_state.translation_methods = {
            'google': True,
            'openai': helper.openai_client is not None,
            'indictrans': hasattr(helper, 'indic_translator') and helper.indic_translator is not None and helper.indic_translator.is_available
        }
    return helper

openai_helper = get_openai_helper()
translation_helper = get_translation_helper()

# Initialize page selection in session state if not exists
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# App header with custom styling
st.markdown(f'<div class="big-title">{get_ui_text("app_title", st.session_state.ui_language)}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{get_ui_text("app_description", st.session_state.ui_language)}</div>', unsafe_allow_html=True)

# Create tabs for navigation
tab1, tab2 = st.tabs(["Main", "History"])

with tab1:
    if st.session_state.page != 'main':
        st.session_state.page = 'main'
    
with tab2:
    if st.session_state.page != 'history':
        st.session_state.page = 'history'

# Sidebar for settings
with st.sidebar:
    st.header(get_ui_text("settings", st.session_state.ui_language))
    
    # UI Language selection - using the same language options as output languages
    languages = ["English", "Hindi", "Tamil", "Bengali", "Marathi", "Telugu", 
                 "Gujarati", "Kannada", "Malayalam", "Punjabi", "Urdu", "Odia"]
    language_codes = ["english", "hindi", "tamil", "bengali", "marathi", "telugu",
                      "gujarati", "kannada", "malayalam", "punjabi", "urdu", "odia"]
                      
    ui_language = st.selectbox(
        "Interface Language:",
        languages,
        index=language_codes.index(st.session_state.ui_language)
        if st.session_state.ui_language in language_codes else 0
    )
    
    # Update UI language if changed - convert display name to code
    selected_language_code = language_codes[languages.index(ui_language)]
    
    # Update UI language if it has changed
    if selected_language_code != st.session_state.ui_language:
        st.session_state.ui_language = selected_language_code
        st.rerun()  # Rerun the app to reflect UI language change
    
    # Detail level setting
    detail_level = st.radio(
        get_ui_text("summary_detail_level", st.session_state.ui_language),
        [
            get_ui_text("simple", st.session_state.ui_language),
            get_ui_text("detailed", st.session_state.ui_language)
        ],
        index=1 if st.session_state.detail_level == "detailed" else 0
    )
    # Map localized selection back to internal english value
    if detail_level == get_ui_text("simple", st.session_state.ui_language):
        st.session_state.detail_level = "simple"
    else:
        st.session_state.detail_level = "detailed"
    
    # Target Language selection (for translation)
    languages = ["English", "Hindi", "Tamil", "Bengali", "Marathi", "Telugu", 
                 "Gujarati", "Kannada", "Malayalam", "Punjabi", "Urdu", "Odia"]
    language_codes = ["english", "hindi", "tamil", "bengali", "marathi", "telugu",
                      "gujarati", "kannada", "malayalam", "punjabi", "urdu", "odia"]
    
    target_language = st.selectbox(
        get_ui_text("output_language", st.session_state.ui_language),
        languages,
        index=language_codes.index(st.session_state.target_language)
        if st.session_state.target_language in language_codes else 0
    )
    
    # Update target language if changed - convert display name to code
    selected_language_code = language_codes[languages.index(target_language)]
    if selected_language_code != st.session_state.target_language:
        st.session_state.target_language = selected_language_code
    
    # About section
    st.divider()
    st.markdown(f"### {get_ui_text('about_lawzio', st.session_state.ui_language)}")
    st.markdown(get_ui_text('about_description', st.session_state.ui_language))
    
    # Translation methods section removed as requested
    
    # Privacy notice
    st.divider()
    st.markdown(f"### {get_ui_text('privacy_notice', st.session_state.ui_language)}")
    st.markdown(get_ui_text('privacy_content', st.session_state.ui_language))

# Import history module
from utils.history import display_history_page

# Main content - conditional based on current page
if st.session_state.page == 'history':
    # Display history page
    display_history_page(st.session_state.ui_language)
else:
    main_col1, main_col2 = st.columns([2, 3])
    
    # Document upload section
    with main_col1:
        st.header(get_ui_text("document_upload", st.session_state.ui_language))
    
    # Add a styled upload box with prominent border and background
    st.markdown('''
    <style>
    .upload-box {
        border: 2px dashed #4267B2;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f8f9fa;
        text-align: center;
    }
    .upload-header {
        font-size: 18px;
        color: #4267B2;
        margin-bottom: 10px;
        font-weight: bold;
    }
    </style>
    <div class="upload-box">
        <div class="upload-header">📄 Upload your legal document here</div>
    </div>
    ''', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        get_ui_text("upload_prompt", st.session_state.ui_language),
        type=["pdf", "docx", "txt", "jpg", "jpeg", "png", "tiff", "tif", "bmp"],
        help=get_ui_text("upload_help", st.session_state.ui_language)
    )
    
    # Privacy options section with descriptions
    st.markdown('''
    <style>
    .privacy-box {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        background-color: #f8f9fa;
    }
    .privacy-header {
        font-size: 18px;
        color: #4267B2;
        margin-bottom: 10px;
        font-weight: bold;
    }
    </style>
    <div class="privacy-box">
        <div class="privacy-header">🔒 Privacy Settings</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("Choose how you want your document to be stored and processed:")
    
    privacy_options = ["standard", "enhanced", "maximum"]
    privacy_labels = [
        get_ui_text("privacy_standard", st.session_state.ui_language, "Standard"),
        get_ui_text("privacy_enhanced", st.session_state.ui_language, "Enhanced"),
        get_ui_text("privacy_maximum", st.session_state.ui_language, "Maximum")
    ]
    
    # Add descriptions for each privacy level
    privacy_descriptions = [
        "Basic protection with minimal encryption",
        "Enhanced protection with full document encryption",
        "Maximum protection with encryption and anonymization of sensitive information"
    ]
    
    # Create a formatted radio button with descriptions
    selected_privacy_index = 0  # Default to Standard
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        standard_selected = st.radio(
            f"🔓 {privacy_labels[0]}",
            [True, False],
            index=1 if selected_privacy_index != 0 else 0,
            label_visibility="collapsed",
            key="standard_privacy"
        )
        st.markdown(f"**{privacy_labels[0]}**")
        st.caption(privacy_descriptions[0])
        if standard_selected:
            selected_privacy_index = 0
    
    with col2:
        enhanced_selected = st.radio(
            f"🔐 {privacy_labels[1]}",
            [True, False],
            index=1 if selected_privacy_index != 1 else 0,
            label_visibility="collapsed",
            key="enhanced_privacy"
        )
        st.markdown(f"**{privacy_labels[1]}**")
        st.caption(privacy_descriptions[1])
        if enhanced_selected:
            selected_privacy_index = 1
    
    with col3:
        maximum_selected = st.radio(
            f"🔒 {privacy_labels[2]}",
            [True, False],
            index=1 if selected_privacy_index != 2 else 0,
            label_visibility="collapsed",
            key="maximum_privacy"
        )
        st.markdown(f"**{privacy_labels[2]}**")
        st.caption(privacy_descriptions[2])
        if maximum_selected:
            selected_privacy_index = 2
    
    # Set the selected privacy option based on the radio buttons
    selected_privacy = privacy_options[selected_privacy_index]
    
    if uploaded_file is not None:
        try:
            with st.spinner(get_ui_text("processing_document", st.session_state.ui_language)):
                # Process the document
                st.session_state.document_text = process_document(uploaded_file)
                st.success(get_ui_text("processed_success", st.session_state.ui_language, uploaded_file.name))
                
                # Detect document language
                detected_language = translation_helper.detect_language(st.session_state.document_text)
                
                # Assess risk level of the document
                with st.spinner(get_ui_text("assessing_risk", st.session_state.ui_language)):
                    risk_level, risk_factors = assess_risk_level(st.session_state.document_text)
                    # Store in session state
                    st.session_state.risk_level = risk_level
                    st.session_state.risk_factors = risk_factors
                    
                    # Get color for risk level
                    risk_color = get_risk_color(risk_level)
                    
                    # Save document information to database with privacy settings
                    try:
                        document_id = save_document_history(
                            filename=uploaded_file.name,
                            file_size_kb=round(uploaded_file.size / 1024, 2),
                            document_language=detected_language,
                            risk_level=risk_level,
                            content_length=len(st.session_state.document_text),
                            risk_factors=risk_factors,
                            document_text=st.session_state.document_text,  # Store the full text (will be encrypted if needed)
                            privacy_level=selected_privacy
                        )
                        # Store document ID in session state for later use
                        st.session_state.document_id = document_id
                        
                        # Display privacy settings information
                        if selected_privacy == "enhanced":
                            st.info(get_ui_text("privacy_enhanced_info", st.session_state.ui_language, 
                                              "Enhanced privacy: Your document is stored with encryption."))
                        elif selected_privacy == "maximum":
                            st.warning(get_ui_text("privacy_maximum_info", st.session_state.ui_language, 
                                                 "Maximum privacy: Your document is stored with encryption and risk factors are anonymized."))
                            
                    except Exception as db_error:
                        # If database save fails, just log and continue
                        # This ensures the app works even if database is not available
                        print(f"Database save error: {db_error}")
                        st.session_state.document_id = None
                
                # Show document info
                st.markdown(f"#### {get_ui_text('document_information', st.session_state.ui_language)}")
                
                # Create two columns for info
                doc_info_col1, doc_info_col2 = st.columns(2)
                
                with doc_info_col1:
                    st.markdown(f"**{get_ui_text('filename', st.session_state.ui_language)}** {uploaded_file.name}")
                    st.markdown(f"**{get_ui_text('size', st.session_state.ui_language)}** {round(uploaded_file.size / 1024, 2)} {get_ui_text('kb', st.session_state.ui_language)}")
                    st.markdown(f"**{get_ui_text('content_length', st.session_state.ui_language)}** {len(st.session_state.document_text)} {get_ui_text('characters', st.session_state.ui_language)}")
                    st.markdown(f"**{get_ui_text('detected_language', st.session_state.ui_language)}** {detected_language.capitalize()}")
                
                with doc_info_col2:
                    # Show risk level with appropriate color using our custom CSS classes
                    risk_class = "risk-low"
                    if risk_level.lower() == "high":
                        risk_class = "risk-high"
                    elif risk_level.lower() == "medium":
                        risk_class = "risk-medium"
                    
                    st.markdown(f"""
                    <div class="{risk_class}">
                    🛡️ {get_ui_text('risk_level', st.session_state.ui_language)} {risk_level}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show risk factors in a bullet list
                    if risk_factors:
                        st.markdown(f"**{get_ui_text('risk_factors_detected', st.session_state.ui_language)}**")
                        for factor in risk_factors:
                            st.markdown(f"• {factor}")
                    else:
                        st.markdown(f"**{get_ui_text('no_risk_factors', st.session_state.ui_language)}**")
                
                # Show a preview
                with st.expander(get_ui_text('document_preview', st.session_state.ui_language)):
                    st.markdown(st.session_state.document_text[:1000] + "..." if len(st.session_state.document_text) > 1000 else st.session_state.document_text)
        except Exception as e:
            st.error(get_ui_text('processing_error', st.session_state.ui_language, str(e)))
    
    # Actions
    col1, col2 = st.columns(2)
    
    with col1:
        summarize_button = st.button(
            get_ui_text('summarize_document', st.session_state.ui_language),
            type="primary",
            disabled=st.session_state.document_text is None
        )
    
    with col2:
        clear_button = st.button(get_ui_text('clear_all', st.session_state.ui_language))
    
    if summarize_button and st.session_state.document_text:
        try:
            with st.spinner(get_ui_text('generating_summary', st.session_state.ui_language, st.session_state.detail_level)):
                st.session_state.summary = openai_helper.summarize_legal_document(
                    st.session_state.document_text, 
                    st.session_state.detail_level
                )
                
                # Translate if needed
                if st.session_state.target_language != "english":
                    try:
                        # Store the translation method used in session state
                        if 'translation_method_used' not in st.session_state:
                            st.session_state.translation_method_used = None
                            
                        with st.spinner(get_ui_text('translating_to', st.session_state.ui_language, st.session_state.target_language.capitalize())):
                            # First, try to determine if IndicTrans will be used
                            # Source language is always English for the summary (we're translating the English summary)
                            is_indic_source = False  # English is not an Indic language
                            is_indic_target = st.session_state.target_language in ["hindi", "tamil", "bengali", "marathi", 
                                                         "telugu", "gujarati", "kannada", "malayalam", 
                                                         "punjabi", "urdu", "odia"]
                            
                            indic_will_be_used = (is_indic_source or "english" == "english") and \
                                (is_indic_target or st.session_state.target_language == "english") and \
                                hasattr(translation_helper, 'indic_translator') and \
                                translation_helper.indic_translator is not None and \
                                translation_helper.indic_translator.is_available
                                
                            # Let the translation helper decide which method to use
                            # We'll get the method used from the translation response
                            # The translation_helper.translate_text() function will try each method
                            # in sequence and return which one was used
                                
                            # Perform the translation
                            translated_text = translation_helper.translate_text(
                                st.session_state.summary,
                                st.session_state.target_language
                            )
                            
                            # We no longer extract translation method information
                            # as it's not displayed in the UI anymore
                            
                            st.session_state.translated_summary = translated_text
                    except Exception as trans_error:
                        st.warning(get_ui_text('translation_error', st.session_state.ui_language, str(trans_error)))
                        st.session_state.translation_method_used = get_ui_text('failed', st.session_state.ui_language)
                        st.session_state.translated_summary = f"**{get_ui_text('translation_error_title', st.session_state.ui_language)}**: {get_ui_text('translation_error_msg', st.session_state.ui_language, st.session_state.target_language.capitalize())}\n\n{st.session_state.summary}"
                else:
                    st.session_state.translation_method_used = None
                    st.session_state.translated_summary = st.session_state.summary
                
                # Save the summary to database if we have a document ID
                if hasattr(st.session_state, 'document_id') and st.session_state.document_id:
                    try:
                        # Save original English summary
                        save_document_summary(
                            document_id=st.session_state.document_id,
                            summary_text=st.session_state.summary,
                            detail_level=st.session_state.detail_level,
                            language="english"
                        )
                        
                        # Save translated summary if different from English
                        if st.session_state.target_language != "english":
                            save_document_summary(
                                document_id=st.session_state.document_id,
                                summary_text=st.session_state.translated_summary,
                                detail_level=st.session_state.detail_level,
                                language=st.session_state.target_language
                            )
                    except Exception as db_error:
                        # If database save fails, just log and continue
                        print(f"Database save error for summary: {db_error}")
        except Exception as e:
            st.error(get_ui_text('summary_error', st.session_state.ui_language, str(e)))
    
    if clear_button:
        st.session_state.document_text = None
        st.session_state.summary = None
        st.session_state.translated_summary = None
        st.session_state.risk_level = None
        st.session_state.risk_factors = []
        st.rerun()

# Results section
    with main_col2:
        st.header(get_ui_text('summary_results', st.session_state.ui_language))
        
        if st.session_state.translated_summary:
            # Show summary details
            st.markdown(f"#### {get_ui_text(st.session_state.detail_level + '_summary', st.session_state.ui_language)} {get_ui_text('in_language', st.session_state.ui_language, st.session_state.target_language.capitalize())}")
            
            # Translation method is no longer displayed
            
            # Create a container with a scrollable area for the summary
            summary_container = st.container(height=500)
            with summary_container:
                st.markdown(st.session_state.translated_summary)
            
            # Download options
            st.download_button(
                label=get_ui_text('download_summary', st.session_state.ui_language),
                data=st.session_state.translated_summary,
                file_name=f"legal_summary_{st.session_state.detail_level}_{st.session_state.target_language}.txt",
                mime="text/plain"
            )
        else:
            # Show empty state
            st.info(get_ui_text('empty_state_msg', st.session_state.ui_language))
            
            # Sample capabilities
            st.markdown(f"### {get_ui_text('lawzio_capabilities', st.session_state.ui_language)}")
            
            feature_col1, feature_col2 = st.columns(2)
            
            with feature_col1:
                st.markdown(f"✅ **{get_ui_text('legal_judgments', st.session_state.ui_language)}**")
                st.markdown(f"✅ **{get_ui_text('contracts_agreements', st.session_state.ui_language)}**")
                st.markdown(f"✅ **{get_ui_text('court_orders', st.session_state.ui_language)}**")
            
            with feature_col2:
                st.markdown(f"✅ **{get_ui_text('legal_notices', st.session_state.ui_language)}**")
                st.markdown(f"✅ **{get_ui_text('legal_opinions', st.session_state.ui_language)}**")
                st.markdown(f"✅ **{get_ui_text('terms_conditions', st.session_state.ui_language)}**")

# Footer - outside the conditional blocks, so it appears on both pages
st.divider()
st.markdown(f"*{get_ui_text('footer_tagline', st.session_state.ui_language)}*")

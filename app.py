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
from utils.history import display_history_page, display_document_details

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
    
    .upload-container {
        border: 4px dashed #3498DB;
        border-radius: 20px;
        padding: 40px;
        margin: 20px auto;
        background-color: #EBF5FB;
        text-align: center;
        max-width: 800px;
    }
    
    .upload-icon {
        font-size: 64px;
        color: #3498DB;
        margin-bottom: 20px;
    }
    
    .upload-title {
        font-size: 28px;
        font-weight: bold;
        color: #2E86C1;
        margin-bottom: 15px;
    }
    
    .upload-subtitle {
        font-size: 18px;
        color: #2471A3;
        margin-bottom: 25px;
    }
    
    .stButton > button {
        background-color: #2E86C1;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 24px;
        border: none;
    }
    
    .stButton > button:hover {
        background-color: #1A5276;
    }
    
    /* Make the file uploader more prominent */
    .stFileUploader > div > div {
        padding: 15px !important;
        background-color: white !important;
        border: 2px solid #3498DB !important;
        border-radius: 10px !important;
        color: #2E86C1 !important;
    }
    
    /* Risk indicators */
    .risk-low {
        color: #28a745;
        padding: 5px 10px;
        border-radius: 5px;
        background-color: rgba(40, 167, 69, 0.1);
        display: inline-block;
        margin: 5px 0;
    }
    
    .risk-medium {
        color: #fd7e14;
        padding: 5px 10px;
        border-radius: 5px;
        background-color: rgba(253, 126, 20, 0.1);
        display: inline-block;
        margin: 5px 0;
    }
    
    .risk-high {
        color: #dc3545;
        padding: 5px 10px;
        border-radius: 5px;
        background-color: rgba(220, 53, 69, 0.1);
        display: inline-block;
        margin: 5px 0;
    }
    
    /* Privacy option cards */
    .privacy-option {
        border: 2px solid #D6EAF8;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        background-color: white;
        transition: all 0.3s;
    }
    
    .privacy-option:hover {
        border-color: #3498DB;
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
    }
    
    .privacy-option-title {
        font-size: 18px;
        font-weight: bold;
        color: #2E86C1;
        margin-bottom: 5px;
    }
    
    .privacy-option-desc {
        font-size: 14px;
        color: #5D6D7E;
    }
    
    .footer {
        text-align: center;
        margin-top: 30px;
        padding: 20px;
        font-size: 14px;
        color: #5D6D7E;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize singleton helpers
openai_helper = OpenAIHelper()
translation_helper = TranslationHelper()

# Initialize session state variables
if 'document_text' not in st.session_state:
    st.session_state.document_text = None

if 'summary' not in st.session_state:
    st.session_state.summary = None
    
if 'translated_summary' not in st.session_state:
    st.session_state.translated_summary = None
    
if 'risk_level' not in st.session_state:
    st.session_state.risk_level = None
    
if 'risk_factors' not in st.session_state:
    st.session_state.risk_factors = []
    
if 'detail_level' not in st.session_state:
    st.session_state.detail_level = "detailed"  # default to detailed
    
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "process"  # default to process tab

if 'ui_language' not in st.session_state:
    st.session_state.ui_language = "english"  # default UI language

if 'target_language' not in st.session_state:
    st.session_state.target_language = "english"  # default target language

# SIMPLIFIED LAYOUT - Main App Content
# Add top navigation with language selector
top_col1, top_col2 = st.columns([3, 1])

with top_col1:
    st.markdown("<h1 class='big-title'>⚖️ Lawzio</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Multilingual Legal Document Analysis & Summarization</p>", unsafe_allow_html=True)

with top_col2:
    # UI Language selection in top right
    st.markdown("<h3 style='margin-bottom:5px;'>Interface Language</h3>", unsafe_allow_html=True)
    ui_lang_options = ["english", "hindi", "tamil", "spanish", "french", "german"]
    ui_lang_index = ui_lang_options.index(st.session_state.ui_language) if st.session_state.ui_language in ui_lang_options else 0
    
    new_ui_lang = st.selectbox(
        "Select interface language",
        ui_lang_options,
        index=ui_lang_index,
        format_func=lambda x: x.capitalize(),
        key="ui_language_selector"
    )
    
    if new_ui_lang != st.session_state.ui_language:
        st.session_state.ui_language = new_ui_lang
        st.rerun()

# CREATE TABS
tab1, tab2 = st.tabs([
    get_ui_text("process_document_tab", st.session_state.ui_language, "📄 Process Document"),
    get_ui_text("document_history_tab", st.session_state.ui_language, "📋 Document History")
])

# PROCESS DOCUMENT TAB
with tab1:
    if st.session_state.document_text is None:
        # UPLOAD SECTION - Highly visible, centered, and prominent
        upload_title = get_ui_text("upload_title", st.session_state.ui_language, "UPLOAD YOUR LEGAL DOCUMENT")
        upload_subtitle = get_ui_text("upload_subtitle", st.session_state.ui_language, "Drag and drop your file or click to browse")
        
        st.markdown(f"""
        <div class="upload-container">
            <div class="upload-icon">📤</div>
            <div class="upload-title">{upload_title}</div>
            <div class="upload-subtitle">{upload_subtitle}</div>
        """, unsafe_allow_html=True)
        
        # Large and prominent file uploader
        uploaded_file = st.file_uploader(
            "", 
            type=["pdf", "docx", "txt", "jpg", "jpeg", "png", "tiff", "tif"],
            key="document_uploader"
        )
        
        st.markdown("""
            <div style="text-align: center; color: #5D6D7E; margin-top: 10px;">
                Supported formats: PDF, DOCX, TXT, JPG, PNG, TIFF
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # PRIVACY SETTINGS - Simple and clear
        if uploaded_file is not None:
            st.markdown("<h3 style='text-align: center; margin-top: 30px; color: #2E86C1;'>🔒 Privacy Settings</h3>", unsafe_allow_html=True)
            
            # Privacy options
            privacy_options = ["standard", "enhanced", "maximum"]
            privacy_icons = ["🔓", "🔐", "🔒"]
            privacy_titles = ["Standard", "Enhanced", "Maximum"]
            privacy_descriptions = [
                "Basic protection with minimal encryption",
                "Enhanced protection with full document encryption",
                "Maximum protection with encryption and anonymization"
            ]
            
            # Display privacy options as three columns
            cols = st.columns(3)
            
            selected_privacy_index = 0  # Default to Standard
            
            # Create three nice looking options
            for i, col in enumerate(cols):
                with col:
                    st.markdown(f"""
                    <div class="privacy-option">
                        <div>{privacy_icons[i]}</div>
                        <div class="privacy-option-title">{privacy_titles[i]}</div>
                        <div class="privacy-option-desc">{privacy_descriptions[i]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.radio(
                        f"Select {privacy_titles[i]}", 
                        [True, False], 
                        key=f"privacy_{i}",
                        label_visibility="collapsed",
                        index=0 if i == 0 else 1
                    ):
                        selected_privacy_index = i
            
            selected_privacy = privacy_options[selected_privacy_index]
            
            # Language and detail options
            st.markdown("<h3 style='text-align: center; margin-top: 30px; color: #2E86C1;'>⚙️ Options</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Target Language")
                language_options = [
                    "english", "hindi", "tamil", "bengali", "marathi", 
                    "telugu", "gujarati", "kannada", "malayalam", 
                    "punjabi", "urdu", "odia", "spanish", "french", 
                    "german", "chinese", "japanese", "arabic"
                ]
                
                st.session_state.target_language = st.selectbox(
                    "Select target language for translation",
                    language_options,
                    index=language_options.index("english"),
                    format_func=lambda x: x.capitalize()
                )
                
            with col2:
                st.subheader("Summary Detail")
                detail_options = ["simple", "detailed"]
                detail_labels = ["Simple", "Detailed"]
                
                st.session_state.detail_level = st.radio(
                    "Select summary detail level",
                    detail_options,
                    index=detail_options.index("detailed"),
                    format_func=lambda x: "Simple" if x == "simple" else "Detailed"
                )
            
            # Process button - large and prominent
            st.markdown("<div style='text-align: center; margin-top: 30px;'>", unsafe_allow_html=True)
            process_button = st.button("PROCESS DOCUMENT", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            if process_button:
                try:
                    with st.spinner("Processing document..."):
                        # Process the document
                        st.session_state.document_text = process_document(uploaded_file)
                        
                        # Detect document language
                        detected_language = translation_helper.detect_language(st.session_state.document_text)
                        
                        # Assess risk level
                        risk_level, risk_factors = assess_risk_level(st.session_state.document_text)
                        st.session_state.risk_level = risk_level
                        st.session_state.risk_factors = risk_factors
                        
                        # Save to database
                        try:
                            document_id = save_document_history(
                                filename=uploaded_file.name,
                                file_size_kb=round(uploaded_file.size / 1024, 2),
                                document_language=detected_language,
                                risk_level=risk_level,
                                content_length=len(st.session_state.document_text),
                                risk_factors=risk_factors,
                                document_text=st.session_state.document_text,
                                privacy_level=selected_privacy
                            )
                            st.session_state.document_id = document_id
                        except Exception as db_error:
                            print(f"Database error: {db_error}")
                            st.session_state.document_id = None
                        
                        st.success(f"Successfully processed {uploaded_file.name}")
                        
                        # Force refresh to show analysis screen
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")
    else:
        # DOCUMENT ANALYSIS SCREEN
        # This section shows after a document is uploaded and processed
        
        # Add a clear button at the top
        if st.button("⬅️ Upload another document", type="secondary"):
            st.session_state.document_text = None
            st.session_state.summary = None
            st.session_state.translated_summary = None
            st.session_state.risk_level = None
            st.session_state.risk_factors = []
            st.rerun()
        
        # Two column layout for analysis results
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.header("Document Information")
            
            # Create two columns for basic info and risk assessment
            info_col1, info_col2 = st.columns(2)
            
            # Show document info
            with info_col1:
                if hasattr(st.session_state, 'document_id') and st.session_state.document_id:
                    doc_info = get_document_with_risk_factors(st.session_state.document_id)
                    if doc_info:
                        st.markdown(f"**Filename:** {doc_info['filename']}")
                        st.markdown(f"**Size:** {doc_info['file_size_kb']} KB")
                        st.markdown(f"**Language:** {doc_info['document_language'].capitalize()}")
                        st.markdown(f"**Content Length:** {doc_info['content_length']} characters")
            
            # Show risk assessment
            with info_col2:
                risk_level = st.session_state.risk_level
                risk_class = "risk-low"
                if risk_level and risk_level.lower() == "high":
                    risk_class = "risk-high"
                elif risk_level and risk_level.lower() == "medium":
                    risk_class = "risk-medium"
                
                if risk_level:
                    st.markdown(f"""
                    <div class="{risk_class}">
                    🛡️ Risk Level: {risk_level}
                    </div>
                    """, unsafe_allow_html=True)
                
                if hasattr(st.session_state, 'risk_factors') and st.session_state.risk_factors:
                    st.markdown("**Risk Factors Detected:**")
                    for factor in st.session_state.risk_factors:
                        st.markdown(f"• {factor}")
                else:
                    st.markdown("**No risk factors detected**")
            
            # Show document preview
            st.subheader("Document Preview")
            with st.expander("Show document text", expanded=False):
                if st.session_state.document_text:
                    preview_text = st.session_state.document_text[:1000] + "..." if len(st.session_state.document_text) > 1000 else st.session_state.document_text
                    st.markdown(preview_text)
            
            # Generate summary button
            st.subheader("Generate Summary")
            summarize_button = st.button(
                "SUMMARIZE DOCUMENT", 
                type="primary",
                use_container_width=True
            )
            
            if summarize_button:
                try:
                    with st.spinner(f"Generating {st.session_state.detail_level} summary..."):
                        st.session_state.summary = openai_helper.summarize_legal_document(
                            st.session_state.document_text, 
                            st.session_state.detail_level
                        )
                        
                        # Translate if needed
                        if st.session_state.target_language != "english":
                            with st.spinner(f"Translating to {st.session_state.target_language.capitalize()}..."):
                                translated_text = translation_helper.translate_text(
                                    st.session_state.summary,
                                    st.session_state.target_language
                                )
                                st.session_state.translated_summary = translated_text
                        else:
                            st.session_state.translated_summary = st.session_state.summary
                        
                        # Save summary to database
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
                                print(f"Database save error for summary: {db_error}")
                        
                        # Force refresh to show summary
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error generating summary: {str(e)}")
        
        with col2:
            st.header("Summary Results")
            
            if st.session_state.translated_summary:
                # Show summary details
                st.subheader(f"{st.session_state.detail_level.capitalize()} Summary in {st.session_state.target_language.capitalize()}")
                
                # Create a container with a scrollable area for the summary
                summary_container = st.container(height=500)
                with summary_container:
                    st.markdown(st.session_state.translated_summary)
                
                # Download button for summary
                st.download_button(
                    label="Download Summary",
                    data=st.session_state.translated_summary,
                    file_name=f"summary_{st.session_state.target_language}_{st.session_state.detail_level}.txt",
                    mime="text/plain"
                )
                
                # What the system can find
                st.markdown("---")
                st.markdown("### The system can identify:")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("✅ **Legal terms**")
                    st.markdown("✅ **Contract clauses**")
                    st.markdown("✅ **Liability issues**")
                
                with col2:
                    st.markdown("✅ **Financial obligations**")
                    st.markdown("✅ **Key parties involved**")
                    st.markdown("✅ **Important dates**")
                
                with col3:
                    st.markdown("✅ **Legal notices**")
                    st.markdown("✅ **Legal opinions**")
                    st.markdown("✅ **Rights & duties**")

# HISTORY TAB
with tab2:
    display_history_page(st.session_state.ui_language)

# Footer
st.markdown("""
<div class="footer">
    <p>Developed by M APARNA & PRAVEEN R | © 2025 Lawzio Legal Document Analysis</p>
</div>
""", unsafe_allow_html=True)
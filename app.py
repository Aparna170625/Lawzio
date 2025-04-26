import streamlit as st
import time
from utils.document_processor import process_document
from utils.openai_helper import OpenAIHelper
from utils.translator import TranslationHelper
from utils.risk_assessment import assess_risk_level, get_risk_color

# Set page configuration
st.set_page_config(
    page_title="Lawzio - Legal Document Summarizer",
    page_icon="⚖️",
    layout="wide",
)

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

# App header
st.title("⚖️ Lawzio - Legal Document Summarizer")
st.markdown("""
*Simplify complex legal documents with AI-powered summarization and translation*
""")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    
    # Detail level setting
    detail_level = st.radio(
        "Summary Detail Level:",
        ["Simple", "Detailed"],
        index=1 if st.session_state.detail_level == "detailed" else 0
    )
    st.session_state.detail_level = detail_level.lower()
    
    # Language selection
    target_language = st.selectbox(
        "Output Language:",
        ["English", "Hindi", "Tamil", "Bengali", "Marathi", "Telugu", 
         "Gujarati", "Kannada", "Malayalam", "Punjabi", "Urdu", "Odia"],
        index=["english", "hindi", "tamil", "bengali", "marathi", "telugu",
               "gujarati", "kannada", "malayalam", "punjabi", "urdu", "odia"].index(st.session_state.target_language)
        if st.session_state.target_language in ["english", "hindi", "tamil", "bengali", "marathi", "telugu",
                                                "gujarati", "kannada", "malayalam", "punjabi", "urdu", "odia"] else 0
    )
    st.session_state.target_language = target_language.lower()
    
    # About section
    st.divider()
    st.markdown("### About Lawzio")
    st.markdown("""
    Lawzio helps users understand complex legal documents by:
    - Summarizing lengthy legal texts
    - Simplifying legal jargon
    - Assessing document risk levels
    - Identifying potential risk factors
    - Translating content across languages
    - Highlighting key points
    """)
    
    # Show translation capabilities
    st.divider()
    st.markdown("### Translation Methods")
    
    # Show which translation methods are available
    if 'translation_methods' in st.session_state:
        methods = []
        if st.session_state.translation_methods.get('indictrans', False):
            methods.append("✅ **IndicTrans**: Native Indian language translation")
        else:
            methods.append("❌ **IndicTrans**: Not available")
            
        if st.session_state.translation_methods.get('openai', False):
            methods.append("✅ **OpenAI GPT-4o**: AI-powered translation")
        else:
            methods.append("❌ **OpenAI GPT-4o**: Not available (needs API key)")
            
        if st.session_state.translation_methods.get('google', False):
            methods.append("✅ **Google Translate**: General translation")
        else:
            methods.append("❌ **Google Translate**: Not available")
        
        for method in methods:
            st.markdown(method)
    
    # Privacy notice
    st.divider()
    st.markdown("### Privacy Notice")
    st.markdown("""
    - All documents are processed securely
    - Documents are not stored permanently
    - AI processing is used for summarization
    - We recommend removing sensitive information
    """)

# Main content
main_col1, main_col2 = st.columns([2, 3])

# Document upload section
with main_col1:
    st.header("Document Upload")
    
    uploaded_file = st.file_uploader(
        "Upload a legal document",
        type=["pdf", "docx", "txt", "jpg", "jpeg", "png", "tiff", "tif", "bmp"],
        help="Supported formats: PDF, DOCX, TXT, and Images (JPG, PNG, TIFF, BMP)"
    )
    
    if uploaded_file is not None:
        try:
            with st.spinner("Processing document..."):
                # Process the document
                st.session_state.document_text = process_document(uploaded_file)
                st.success(f"Document '{uploaded_file.name}' processed successfully!")
                
                # Detect document language
                detected_language = translation_helper.detect_language(st.session_state.document_text)
                
                # Assess risk level of the document
                with st.spinner("Assessing document risk level..."):
                    risk_level, risk_factors = assess_risk_level(st.session_state.document_text)
                    # Store in session state
                    st.session_state.risk_level = risk_level
                    st.session_state.risk_factors = risk_factors
                    
                    # Get color for risk level
                    risk_color = get_risk_color(risk_level)
                
                # Show document info
                st.markdown("#### Document Information")
                
                # Create two columns for info
                doc_info_col1, doc_info_col2 = st.columns(2)
                
                with doc_info_col1:
                    st.markdown(f"**Filename:** {uploaded_file.name}")
                    st.markdown(f"**Size:** {round(uploaded_file.size / 1024, 2)} KB")
                    st.markdown(f"**Content Length:** {len(st.session_state.document_text)} characters")
                    st.markdown(f"**Detected Language:** {detected_language.capitalize()}")
                
                with doc_info_col2:
                    # Show risk level with appropriate color
                    st.markdown(f"""
                    <div style="padding: 10px; border-radius: 5px; background-color: {risk_color}; 
                    color: white; font-weight: bold; text-align: center; margin-bottom: 10px;">
                    Risk Level: {risk_level}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show risk factors in a bullet list
                    if risk_factors:
                        st.markdown("**Risk Factors Detected:**")
                        for factor in risk_factors:
                            st.markdown(f"• {factor}")
                    else:
                        st.markdown("**No specific risk factors detected**")
                
                # Show a preview
                with st.expander("Document Preview"):
                    st.markdown(st.session_state.document_text[:1000] + "..." if len(st.session_state.document_text) > 1000 else st.session_state.document_text)
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")
    
    # Actions
    col1, col2 = st.columns(2)
    
    with col1:
        summarize_button = st.button(
            "Summarize Document", 
            type="primary",
            disabled=st.session_state.document_text is None
        )
    
    with col2:
        clear_button = st.button("Clear All")
    
    if summarize_button and st.session_state.document_text:
        try:
            with st.spinner(f"Generating {st.session_state.detail_level} summary..."):
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
                            
                        with st.spinner(f"Translating to {st.session_state.target_language.capitalize()}..."):
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
                            
                            # Extract the translation method used from the response
                            # Translation helper adds "Translation method used: METHOD" to the beginning
                            if translated_text and "Translation method used:" in translated_text:
                                # Split by newlines to get the first line
                                first_line = translated_text.split('\n')[0]
                                if "Translation method used:" in first_line:
                                    # Extract the method name
                                    method_part = first_line.split("Translation method used:")[1].strip()
                                    st.session_state.translation_method_used = method_part
                                    # Remove the method line from the translated text
                                    translated_text = translated_text.replace(first_line, "").strip()
                                    if translated_text.startswith('\n\n'):
                                        translated_text = translated_text[2:]
                            
                            st.session_state.translated_summary = translated_text
                    except Exception as trans_error:
                        st.warning(f"Translation error: {str(trans_error)}. Showing original summary.")
                        st.session_state.translation_method_used = "Failed"
                        st.session_state.translated_summary = f"**Translation Error**: Could not translate to {st.session_state.target_language.capitalize()}. Showing original summary in English.\n\n{st.session_state.summary}"
                else:
                    st.session_state.translation_method_used = None
                    st.session_state.translated_summary = st.session_state.summary
        except Exception as e:
            st.error(f"Error generating summary: {str(e)}")
    
    if clear_button:
        st.session_state.document_text = None
        st.session_state.summary = None
        st.session_state.translated_summary = None
        st.session_state.risk_level = None
        st.session_state.risk_factors = []
        st.rerun()

# Results section
with main_col2:
    st.header("Summary Results")
    
    if st.session_state.translated_summary:
        # Show summary details
        st.markdown(f"#### {st.session_state.detail_level.capitalize()} Summary in {st.session_state.target_language.capitalize()}")
        
        # Show which translation method was used, if any
        if st.session_state.target_language != "english" and hasattr(st.session_state, 'translation_method_used') and st.session_state.translation_method_used:
            st.info(f"Translation method used: **{st.session_state.translation_method_used}**")
        
        # Create a container with a scrollable area for the summary
        summary_container = st.container(height=500)
        with summary_container:
            st.markdown(st.session_state.translated_summary)
        
        # Download options
        st.download_button(
            label="Download Summary",
            data=st.session_state.translated_summary,
            file_name=f"legal_summary_{st.session_state.detail_level}_{st.session_state.target_language}.txt",
            mime="text/plain"
        )
    else:
        # Show empty state
        st.info("Upload a document and click 'Summarize Document' to see results here.")
        
        # Sample capabilities
        st.markdown("### Lawzio Can Help You With:")
        
        feature_col1, feature_col2 = st.columns(2)
        
        with feature_col1:
            st.markdown("✅ **Legal Judgments**")
            st.markdown("✅ **Contracts & Agreements**")
            st.markdown("✅ **Court Orders**")
        
        with feature_col2:
            st.markdown("✅ **Legal Notices**")
            st.markdown("✅ **Legal Opinions**")
            st.markdown("✅ **Terms & Conditions**")

# Footer
st.divider()
st.markdown("*Lawzio - Making legal documents accessible for everyone*")

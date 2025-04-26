"""
History module for displaying document history
"""
import streamlit as st
from utils.database import (
    get_recent_documents, 
    get_document_with_risk_factors, 
    get_document_summaries,
    get_privacy_settings,
    update_privacy_settings,
    delete_document_by_token,
    get_document_text
)
from utils.localization import get_ui_text
from utils.risk_assessment import get_risk_color
import pandas as pd
from datetime import datetime

def format_date(date_str):
    """Format database timestamp to readable date"""
    try:
        dt = datetime.fromisoformat(str(date_str).replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return str(date_str)

def display_history_page(ui_language):
    """
    Display document history page
    
    Args:
        ui_language (str): Current UI language
    """
    st.title(get_ui_text("history_title", ui_language))
    st.write(get_ui_text("history_description", ui_language))
    
    # Get recent documents from database
    documents = get_recent_documents(limit=20)
    
    if not documents:
        st.info(get_ui_text("no_history", ui_language))
        return
        
    # Create DataFrame for display
    df_data = []
    for doc in documents:
        df_data.append({
            "id": doc["id"],
            "filename": doc["filename"],
            "date": format_date(doc["upload_date"]),
            "language": doc["document_language"].capitalize() if doc["document_language"] else "Unknown",
            "risk_level": doc["risk_level"]
        })
    
    df = pd.DataFrame(df_data)
    
    # Display table with document history
    st.dataframe(
        df,
        column_config={
            "id": None,  # Hide ID column
            "filename": st.column_config.TextColumn(
                get_ui_text("filename", ui_language),
                width="medium"
            ),
            "date": st.column_config.TextColumn(
                get_ui_text("upload_date", ui_language),
                width="small"
            ),
            "language": st.column_config.TextColumn(
                get_ui_text("language", ui_language),
                width="small"
            ),
            "risk_level": st.column_config.TextColumn(
                get_ui_text("risk_level", ui_language),
                width="small"
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Allow selecting a document to view details
    if df_data:
        selected_doc_index = st.selectbox(
            get_ui_text("select_document", ui_language),
            range(len(df_data)),
            format_func=lambda x: df_data[x]["filename"]
        )
        
        if selected_doc_index is not None:
            selected_doc_id = df_data[selected_doc_index]["id"]
            display_document_details(selected_doc_id, ui_language)
    
def display_document_details(document_id, ui_language):
    """
    Display details for a specific document
    
    Args:
        document_id (int): ID of the document to display
        ui_language (str): Current UI language
    """
    # Get document with risk factors
    document = get_document_with_risk_factors(document_id)
    
    if not document:
        st.error(get_ui_text("document_not_found", ui_language))
        return
        
    # Get privacy settings
    privacy_settings = get_privacy_settings(document_id)
    
    # Display document info in an expander
    with st.expander(get_ui_text("document_details", ui_language), expanded=True):
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{get_ui_text('filename', ui_language)}:** {document['filename']}")
            st.markdown(f"**{get_ui_text('upload_date', ui_language)}:** {format_date(document['upload_date'])}")
            st.markdown(f"**{get_ui_text('size', ui_language)}:** {document['file_size_kb']} KB")
            st.markdown(f"**{get_ui_text('content_length', ui_language)}:** {document['content_length']} {get_ui_text('characters', ui_language)}")
            st.markdown(f"**{get_ui_text('detected_language', ui_language)}:** {document['document_language'].capitalize() if document['document_language'] else 'Unknown'}")
            
            # Add privacy level display
            privacy_level = document.get('privacy_level', 'standard')
            privacy_icon = "🔓"  # Standard
            if privacy_level == 'enhanced':
                privacy_icon = "🔐"  # Enhanced
            elif privacy_level == 'maximum':
                privacy_icon = "🔒"  # Maximum
                
            st.markdown(f"**{get_ui_text('privacy_level', ui_language, 'Privacy Level')}:** {privacy_icon} {privacy_level.capitalize()}")
        
        with col2:
            # Show risk level with appropriate color
            risk_level = document['risk_level']
            
            # Set risk class for styling
            risk_class = "risk-low"
            if risk_level and risk_level.lower() == "high":
                risk_class = "risk-high"
            elif risk_level and risk_level.lower() == "medium":
                risk_class = "risk-medium"
            
            st.markdown(f"""
            <div class="{risk_class}">
            🛡️ {get_ui_text('risk_level', ui_language)} {risk_level}
            </div>
            """, unsafe_allow_html=True)
            
            # Show risk factors
            if document['risk_factors']:
                st.markdown(f"**{get_ui_text('risk_factors_detected', ui_language)}**")
                for factor in document['risk_factors']:
                    st.markdown(f"• {factor}")
            else:
                st.markdown(f"**{get_ui_text('no_risk_factors', ui_language)}**")
    
    # Privacy settings section
    if privacy_settings:
        with st.expander(get_ui_text("privacy_settings", ui_language, "Privacy & Security Settings"), expanded=False):
            # Display current settings
            st.markdown(f"**{get_ui_text('current_privacy_settings', ui_language, 'Current Settings')}**")
            
            st.markdown(f"• **{get_ui_text('privacy_level', ui_language, 'Privacy Level')}:** {privacy_settings['privacy_level'].capitalize()}")
            st.markdown(f"• **{get_ui_text('data_retention', ui_language, 'Data Retention')}:** {privacy_settings['retention_days']} {get_ui_text('days', ui_language, 'days')}")
            st.markdown(f"• **{get_ui_text('text_anonymization', ui_language, 'Text Anonymization')}:** {'✅' if privacy_settings['anonymize_text'] else '❌'}")
            st.markdown(f"• **{get_ui_text('encryption', ui_language, 'Encryption')}:** {'✅' if privacy_settings['encrypt_storage'] else '❌'}")
            
            # Show access token (required for deletion)
            if privacy_settings.get('access_token'):
                st.markdown(f"• **{get_ui_text('access_token', ui_language, 'Access Token')}:** `{privacy_settings['access_token']}`")
            
            # Option to modify privacy settings
            st.markdown("---")
            st.subheader(get_ui_text("update_privacy", ui_language, "Update Privacy Settings"))
            
            # Privacy level selection
            new_privacy_level = st.selectbox(
                get_ui_text("new_privacy_level", ui_language, "New Privacy Level"),
                ["standard", "enhanced", "maximum"],
                index=["standard", "enhanced", "maximum"].index(privacy_settings['privacy_level'])
            )
            
            # Retention period
            new_retention = st.number_input(
                get_ui_text("new_retention", ui_language, "Retention Period (days)"),
                min_value=1,
                max_value=365,
                value=privacy_settings['retention_days']
            )
            
            # Anonymize text
            new_anonymize = st.checkbox(
                get_ui_text("anonymize_text", ui_language, "Anonymize sensitive information"),
                value=privacy_settings['anonymize_text']
            )
            
            # Encrypt storage
            new_encrypt = st.checkbox(
                get_ui_text("encrypt_storage", ui_language, "Enable storage encryption"),
                value=privacy_settings['encrypt_storage']
            )
            
            # Update button
            if st.button(get_ui_text("update_settings", ui_language, "Update Settings")):
                success = update_privacy_settings(
                    document_id=document_id,
                    privacy_level=new_privacy_level,
                    retention_days=new_retention,
                    anonymize_text=new_anonymize,
                    encrypt_storage=new_encrypt
                )
                
                if success:
                    st.success(get_ui_text("settings_updated", ui_language, "Privacy settings updated successfully"))
                    st.rerun()  # Refresh the page
                else:
                    st.error(get_ui_text("update_failed", ui_language, "Failed to update privacy settings"))
                    
            # Document deletion
            st.markdown("---")
            st.subheader(get_ui_text("delete_document", ui_language, "Delete Document"))
            st.warning(get_ui_text("delete_warning", ui_language, "Warning: Document deletion is permanent and cannot be undone."))
            
            if st.button(get_ui_text("delete_confirm", ui_language, "Delete Document and All Related Data"), type="primary", use_container_width=True):
                if privacy_settings.get('access_token'):
                    success = delete_document_by_token(privacy_settings['access_token'])
                    if success:
                        st.success(get_ui_text("delete_success", ui_language, "Document deleted successfully"))
                        # Clear session state and return to history page
                        st.session_state.document_text = None
                        st.session_state.summary = None
                        st.session_state.translated_summary = None
                        st.rerun()
                    else:
                        st.error(get_ui_text("delete_failed", ui_language, "Failed to delete document"))
    
    # Get summaries for this document
    summaries = get_document_summaries(document_id)
    
    if summaries:
        st.subheader(get_ui_text("document_summaries", ui_language))
        
        # Group summaries by language
        summaries_by_language = {}
        for summary in summaries:
            language = summary['language'].capitalize()
            if language not in summaries_by_language:
                summaries_by_language[language] = []
            summaries_by_language[language].append(summary)
        
        # Create tabs for each language
        if summaries_by_language:
            tabs = st.tabs(list(summaries_by_language.keys()))
            for i, (language, language_summaries) in enumerate(summaries_by_language.items()):
                with tabs[i]:
                    # Sort by detail level (simple first, then detailed)
                    language_summaries.sort(key=lambda x: 0 if x['detail_level'] == 'simple' else 1)
                    
                    for summary in language_summaries:
                        with st.expander(
                            f"{get_ui_text(summary['detail_level'] + '_summary', ui_language)} ({format_date(summary['generation_date'])})",
                            expanded=True if summary == language_summaries[0] else False
                        ):
                            st.markdown(summary['summary_text'])
                            
                            # Add download button for this summary
                            st.download_button(
                                label=get_ui_text('download_summary', ui_language),
                                data=summary['summary_text'],
                                file_name=f"legal_summary_{summary['detail_level']}_{summary['language']}.txt",
                                mime="text/plain"
                            )
    else:
        st.info(get_ui_text("no_summaries", ui_language))
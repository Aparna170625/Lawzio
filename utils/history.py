"""
History module for displaying document history
"""
import streamlit as st
from utils.database import get_recent_documents, get_document_with_risk_factors, get_document_summaries
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
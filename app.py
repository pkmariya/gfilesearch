"""
Google File Search API - Streamlit Application
A web interface for uploading files and searching their content using Google's Gemini API.
"""

import streamlit as st
import google.generativeai as genai
from pathlib import Path
import os
import tempfile
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
from docx import Document
import pypdf
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Google File Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .search-result {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4CAF50;
        margin-bottom: 1rem;
    }
    .metadata {
        color: #666;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
def initialize_session_state():
    """Initialize session state variables."""
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    if 'api_configured' not in st.session_state:
        st.session_state.api_configured = False
    if 'file_contents' not in st.session_state:
        st.session_state.file_contents = {}
    if 'gemini_files' not in st.session_state:
        st.session_state.gemini_files = []


def configure_api(api_key: str) -> bool:
    """
    Configure the Google Gemini API with the provided key.
    
    Args:
        api_key: Google API key
        
    Returns:
        bool: True if configuration successful, False otherwise
    """
    try:
        genai.configure(api_key=api_key)
        # Test the API key with a simple call
        model = genai.GenerativeModel('gemini-2.5-flash')
        st.session_state.api_configured = True
        return True
    except Exception as e:
        st.error(f"API Configuration Error: {str(e)}")
        st.session_state.api_configured = False
        return False

def process_json_file(file) -> str:
    """
    Process and extract text from JSON files.
    
    Args:
        file: Streamlit uploaded file object
        
    Returns:
        str: Formatted JSON content as string
    """
    try:
        content = json.load(file)
        # Convert JSON to readable text format with indentation
        text_content = json.dumps(content, indent=2)
        return text_content
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON format - {str(e)}"
    except Exception as e:
        return f"Error reading JSON file: {str(e)}"

def read_file_content(file) -> str:
    """
    Read content from uploaded file based on its type.
    
    Args:
        file: Streamlit uploaded file object
        
    Returns:
        str: Extracted text content
    """
    try:
        file_extension = Path(file.name).suffix.lower()
        
        if file_extension == '.txt':
            return file.read().decode('utf-8')
            
        elif file_extension == '.pdf':
            pdf_reader = pypdf.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
            
        elif file_extension == '.docx':
            doc = Document(file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
            
        elif file_extension == '.csv':
            df = pd.read_csv(file)
            return df.to_string()
        
        elif file_extension == '.json':
            return process_json_file(file)

        else:
            return f"Unsupported file type: {file_extension}"
            
    except Exception as e:
        return f"Error reading file: {str(e)}"


def upload_file_to_gemini(file, display_name: str = None) -> dict:
    """
    Upload a file to Google Gemini API.
    
    Args:
        file: File object to upload
        display_name: Optional display name for the file
        
    Returns:
        dict: Information about the uploaded file
    """
    try:
        # Create a temporary file to save the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.name).suffix) as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_path = tmp_file.name
        
        # Upload to Gemini
        gemini_file = genai.upload_file(
            path=tmp_path,
            display_name=display_name or file.name
        )
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return {
            'name': gemini_file.name,
            'display_name': gemini_file.display_name,
            'uri': gemini_file.uri,
            'state': gemini_file.state.name,
            'size_bytes': file.size,
            'uploaded_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        raise Exception(f"Error uploading file to Gemini: {str(e)}")


def search_in_files(query: str, files_info: list) -> dict:
    """
    Search for information in uploaded files using Gemini API.
    
    Args:
        query: Search query string
        files_info: List of uploaded file information
        
    Returns:
        dict: Search results with snippets and metadata
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create prompt for searching
        prompt = f"""
        Based on the uploaded files, please answer the following query:
        
        Query: {query}
        
        Provide a comprehensive answer with:
        1. Direct answer to the query
        2. Relevant excerpts or snippets from the files
        3. File names where the information was found
        4. A confidence score (Low/Medium/High) for the answer
        
        Format your response as follows:
        ANSWER: [Your answer here]
        SNIPPETS: [Relevant text excerpts]
        SOURCES: [File names]
        CONFIDENCE: [Low/Medium/High]
        """
        
        # Get file objects for the API call
        file_objects = []
        for file_info in files_info:
            try:
                # Get the file from Gemini
                gemini_file = genai.get_file(file_info['name'])
                file_objects.append(gemini_file)
            except:
                continue
        
        if not file_objects:
            return {
                'answer': 'No files available for search.',
                'snippets': [],
                'sources': [],
                'confidence': 'Low',
                'timestamp': datetime.now().isoformat()
            }
        
        # Generate response
        response = model.generate_content([prompt] + file_objects)
        
        # Parse the response
        result_text = response.text
        
        # Extract structured information
        answer = ""
        snippets = []
        sources = []
        confidence = "Medium"
        
        if "ANSWER:" in result_text:
            answer = result_text.split("ANSWER:")[1].split("SNIPPETS:")[0].strip()
        else:
            answer = result_text
            
        if "SNIPPETS:" in result_text:
            snippets_text = result_text.split("SNIPPETS:")[1].split("SOURCES:")[0].strip()
            snippets = [s.strip() for s in snippets_text.split('\n') if s.strip()]
            
        if "SOURCES:" in result_text:
            sources_text = result_text.split("SOURCES:")[1].split("CONFIDENCE:")[0].strip()
            sources = [s.strip() for s in sources_text.split('\n') if s.strip()]
            
        if "CONFIDENCE:" in result_text:
            confidence = result_text.split("CONFIDENCE:")[1].strip().split('\n')[0]
        
        return {
            'query': query,
            'answer': answer,
            'snippets': snippets,
            'sources': sources,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat(),
            'raw_response': result_text
        }
        
    except Exception as e:
        return {
            'query': query,
            'answer': f"Error during search: {str(e)}",
            'snippets': [],
            'sources': [],
            'confidence': 'Low',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }


def sidebar_content():
    """Render sidebar content with API configuration and file management."""
    st.sidebar.title("⚙️ Configuration")
    
    # API Key input
    api_key = st.sidebar.text_input(
        "Google API Key",
        type="password",
        value=os.getenv("GOOGLE_API_KEY", ""),
        help="Enter your Google API key from https://makersuite.google.com/app/apikey"
    )
    
    if st.sidebar.button("Configure API", type="primary"):
        if api_key:
            if configure_api(api_key):
                st.sidebar.success("✅ API configured successfully!")
        else:
            st.sidebar.error("Please enter an API key")
    
    # Show API status
    if st.session_state.api_configured:
        st.sidebar.success("🟢 API Connected")
    else:
        st.sidebar.warning("🔴 API Not Connected")
    
    st.sidebar.divider()
    
    # File Management Section
    st.sidebar.title("📁 File Management")
    
    if st.session_state.gemini_files:
        st.sidebar.write(f"**Uploaded Files:** {len(st.session_state.gemini_files)}")
        
        for idx, file_info in enumerate(st.session_state.gemini_files):
            with st.sidebar.expander(f"📄 {file_info['display_name']}"):
                st.write(f"**Size:** {file_info['size_bytes']} bytes")
                st.write(f"**Status:** {file_info['state']}")
                st.write(f"**Uploaded:** {file_info['uploaded_at'][:19]}")
                
                if st.button(f"Delete", key=f"delete_{idx}"):
                    try:
                        genai.delete_file(file_info['name'])
                        st.session_state.gemini_files.pop(idx)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting file: {str(e)}")
    else:
        st.sidebar.info("No files uploaded yet")
    
    st.sidebar.divider()
    
    # Search History
    st.sidebar.title("🕒 Search History")
    
    if st.session_state.search_history:
        st.sidebar.write(f"**Recent Searches:** {len(st.session_state.search_history)}")
        
        # Show last 5 searches
        for idx, search in enumerate(reversed(st.session_state.search_history[-5:])):
            with st.sidebar.expander(f"🔍 {search['query'][:30]}..."):
                st.write(f"**Time:** {search['timestamp'][:19]}")
                st.write(f"**Confidence:** {search['confidence']}")
        
        if st.sidebar.button("Clear History"):
            st.session_state.search_history = []
            st.rerun()
    else:
        st.sidebar.info("No search history yet")


def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    sidebar_content()
    
    # Main content
    st.title("🔍 Google File Search")
    st.markdown("Upload documents and search their content using Google's Gemini API")
    
    # Check if API is configured
    if not st.session_state.api_configured:
        st.warning("⚠️ Please configure your Google API key in the sidebar to get started.")
        st.info("""
        **Getting Started:**
        1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Enter the API key in the sidebar
        3. Click 'Configure API'
        4. Upload your documents and start searching!
        """)
        return
    
    # File Upload Section
    st.header("📤 Upload Documents")
    
    with st.container():
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            "Choose files to upload",
            type=['pdf', 'txt', 'docx', 'csv', 'json'],
            accept_multiple_files=True,
            help="Supported formats: PDF, TXT, DOCX, CSV, JSON"
        )
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            upload_button = st.button("📁 Upload Files", type="primary", disabled=not uploaded_files)
        
        with col2:
            if uploaded_files:
                st.info(f"Selected {len(uploaded_files)} file(s)")
        
        if upload_button and uploaded_files:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, file in enumerate(uploaded_files):
                try:
                    status_text.text(f"Uploading {file.name}...")
                    file_info = upload_file_to_gemini(file, file.name)
                    st.session_state.gemini_files.append(file_info)
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                    
                except Exception as e:
                    st.error(f"Error uploading {file.name}: {str(e)}")
            
            status_text.text("Upload complete!")
            st.success(f"✅ Successfully uploaded {len(uploaded_files)} file(s)")
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Search Section
    st.header("🔎 Search Documents")
    
    if not st.session_state.gemini_files:
        st.info("📌 Upload some files first to start searching!")
        return
    
    # Search input
    search_query = st.text_input(
        "Enter your search query",
        placeholder="e.g., What are the main topics discussed in the documents?",
        help="Ask questions about your uploaded documents"
    )
    
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        search_button = st.button("🔍 Search", type="primary", disabled=not search_query)
    
    with col2:
        if st.session_state.search_history:
            export_button = st.button("📥 Export Results")
    
    # Perform search
    if search_button and search_query:
        with st.spinner("Searching..."):
            results = search_in_files(search_query, st.session_state.gemini_files)
            
            # Add to search history
            st.session_state.search_history.append(results)
            
            # Display results
            st.divider()
            st.subheader("📊 Search Results")
            
            # Result card
            st.markdown('<div class="search-result">', unsafe_allow_html=True)
            
            # Confidence badge
            confidence_color = {
                'High': '🟢',
                'Medium': '🟡',
                'Low': '🔴'
            }
            st.markdown(f"**Confidence:** {confidence_color.get(results['confidence'], '⚪')} {results['confidence']}")
            
            # Answer
            st.markdown("### Answer")
            st.write(results['answer'])
            
            # Snippets
            if results['snippets']:
                st.markdown("### Relevant Excerpts")
                for snippet in results['snippets']:
                    if snippet:
                        st.info(f"💬 {snippet}")
            
            # Sources
            if results['sources']:
                st.markdown("### Sources")
                for source in results['sources']:
                    if source:
                        st.markdown(f"- 📄 {source}")
            
            # Metadata
            st.markdown(f'<div class="metadata">Search performed at {results["timestamp"][:19]}</div>', 
                       unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Export search results
    if st.session_state.search_history and 'export_button' in locals() and export_button:
        # Create JSON export
        export_data = json.dumps(st.session_state.search_history, indent=2)
        
        st.download_button(
            label="📥 Download Search History (JSON)",
            data=export_data,
            file_name=f"search_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Display recent searches
    if st.session_state.search_history:
        st.divider()
        st.subheader("📜 Recent Searches")
        
        # Show last 3 searches (excluding the current one if just searched)
        recent_count = min(3, len(st.session_state.search_history) - (1 if search_button else 0))
        
        if recent_count > 0:
            for search in reversed(st.session_state.search_history[-(recent_count + (1 if search_button else 0)):-1 if search_button else None]):
                with st.expander(f"🔍 {search['query']} - {search['timestamp'][:19]}"):
                    st.write(f"**Confidence:** {search['confidence']}")
                    st.write(f"**Answer:** {search['answer'][:200]}...")


if __name__ == "__main__":
    main()

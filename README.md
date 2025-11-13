# 🔍 Google File Search - Streamlit Application

A powerful web-based application that allows you to upload documents and search their content using Google's Gemini API with advanced file search capabilities.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28.0-red)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- **📤 Multi-Format File Upload**: Support for PDF, TXT, DOCX, and CSV files
- **🔍 Intelligent Search**: Leverage Google's Gemini API for smart content search
- **📊 Rich Results Display**: View search results with relevant snippets and metadata
- **📁 File Management**: Upload, view, and delete files through an intuitive interface
- **🕒 Search History**: Track and review your previous searches
- **📥 Export Functionality**: Download search results in JSON format
- **🔐 Secure API Key Handling**: Environment-based configuration for API credentials
- **🎨 Clean UI**: Modern, responsive interface built with Streamlit
- **⚡ Real-time Processing**: Instant feedback and progress indicators

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google API Key (Gemini API access)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/pkmariya/gfilesearch.git
   cd gfilesearch
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Google API key
   # GOOGLE_API_KEY=your_actual_api_key_here
   ```

### Getting Your Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click on "Create API Key"
4. Copy the generated API key
5. Paste it in your `.env` file or enter it directly in the application sidebar

## 🎯 Usage

### Starting the Application

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Application

#### 1. **Configure API Key**
   - Enter your Google API key in the sidebar
   - Click "Configure API" button
   - Wait for the success confirmation

#### 2. **Upload Documents**
   - Click on "Browse files" or drag and drop files
   - Select one or multiple files (PDF, TXT, DOCX, or CSV)
   - Click "📁 Upload Files"
   - Wait for the upload to complete

#### 3. **Search Your Documents**
   - Enter your search query in the search box
   - Click "🔍 Search"
   - View results with:
     - Direct answer to your query
     - Relevant text excerpts
     - Source file names
     - Confidence score

#### 4. **Manage Files**
   - View all uploaded files in the sidebar
   - Check file details (size, status, upload time)
   - Delete files when no longer needed

#### 5. **Export Search History**
   - Click "📥 Export Results" to download search history
   - Results are saved in JSON format with timestamps

## 📚 Supported File Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | `.pdf` | Portable Document Format |
| Text | `.txt` | Plain text files |
| Word | `.docx` | Microsoft Word documents |
| CSV | `.csv` | Comma-separated values |

## 🏗️ Project Structure

```
gfilesearch/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
```

### Streamlit Configuration (Optional)

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
```

## 🛠️ Technical Details

### Dependencies

- **streamlit**: Web application framework
- **google-generativeai**: Google's Gemini API client
- **python-docx**: DOCX file processing
- **pypdf**: PDF file processing
- **pandas**: CSV file processing and data manipulation
- **python-dotenv**: Environment variable management

### Architecture

The application follows a modular design:

- **Session State Management**: Maintains uploaded files and search history
- **File Processing**: Modular functions for different file types
- **API Integration**: Secure communication with Google Gemini API
- **Error Handling**: Comprehensive error catching and user feedback
- **UI Components**: Reusable Streamlit components for consistent UX

## 🔒 Security Best Practices

- ✅ API keys are loaded from environment variables
- ✅ Sensitive files are excluded via `.gitignore`
- ✅ Temporary files are cleaned up after processing
- ✅ API key input uses password field type
- ✅ No hardcoded credentials in source code

## 🐛 Troubleshooting

### Common Issues

**API Configuration Errors**
- Ensure your API key is valid and has Gemini API access enabled
- Check that the API key is correctly entered (no extra spaces)

**File Upload Failures**
- Verify file format is supported (PDF, TXT, DOCX, CSV)
- Check file size (default limit is 200MB)
- Ensure stable internet connection

**Search Not Working**
- Confirm files are successfully uploaded (check sidebar)
- Verify API is configured (green status indicator)
- Try rephrasing your search query

### Error Messages

- `API Configuration Error`: Invalid or expired API key
- `Error uploading file`: File format issue or network problem
- `Error during search`: API quota exceeded or network issue

## 📈 Performance Tips

- Upload files in batches for better performance
- Keep file sizes reasonable (< 50MB per file)
- Use specific search queries for better results
- Clear old files regularly to maintain performance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google for the Gemini API
- Streamlit for the amazing web framework
- All contributors and users of this project

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using Streamlit and Google Gemini API**
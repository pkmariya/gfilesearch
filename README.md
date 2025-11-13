# gfilesearch

A simple Python application for uploading files to Google's Generative AI and performing natural language searches within those files.

## Features

- Upload files to Google's Generative AI
- List all uploaded files
- Search within files using natural language queries
- Delete files from the service
- Simple command-line interface

## Prerequisites

- Python 3.7 or higher
- Google API key with access to Generative AI API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pkmariya/gfilesearch.git
cd gfilesearch
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Google API key:
```bash
cp .env.example .env
# Edit .env and add your Google API key
```

## Usage

### Command Line Interface

Upload a file:
```bash
python gfilesearch.py upload /path/to/your/file.pdf
```

List all uploaded files:
```bash
python gfilesearch.py list
```

Search within a file:
```bash
python gfilesearch.py search files/your-file-id "What are the main topics?"
```

Delete a file:
```bash
python gfilesearch.py delete files/your-file-id
```

### Python API

```python
from gfilesearch import GFileSearch

# Initialize
gfs = GFileSearch()

# Upload a file
uploaded_file = gfs.upload_file("document.pdf")

# Search within the file
result = gfs.search_uploaded_file(
    uploaded_file,
    "What are the key points in this document?"
)
print(result)

# List all files
files = gfs.list_files()
for file in files:
    print(f"{file.display_name}: {file.name}")

# Delete a file
gfs.delete_file(uploaded_file.name)
```

## Example

See `example.py` for more usage examples:
```bash
python example.py
```

## API Key Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file:
```
GOOGLE_API_KEY=your_api_key_here
```

## License

MIT License
# Contributing to GFileSearch

Thank you for your interest in contributing to GFileSearch!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/pkmariya/gfilesearch.git
cd gfilesearch
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your API key:
```bash
cp .env.example .env
# Edit .env and add your Google API key
```

## Testing

Run the basic tests:
```bash
python test_basic.py
```

Run the example script:
```bash
python example.py
```

Test the command-line interface:
```bash
# List files
python gfilesearch.py list

# Upload a file
python gfilesearch.py upload sample.txt

# Search within a file
python gfilesearch.py search <file-id> "What is this document about?"
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

## Pull Request Process

1. Create a new branch for your feature
2. Make your changes
3. Test your changes thoroughly
4. Submit a pull request with a clear description

## Questions?

Open an issue on GitHub if you have any questions or suggestions.

#!/usr/bin/env python3
"""
Google File Search Application

A simple application to upload files to Google's Generative AI and perform searches.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Any
import google.generativeai as genai
from google.generativeai.types import File
from dotenv import load_dotenv


class GFileSearch:
    """A simple wrapper for Google's File API with search capabilities."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GFileSearch application.
        
        Args:
            api_key: Google API key. If not provided, will look for GOOGLE_API_KEY in environment.
        """
        # Load environment variables
        load_dotenv()
        
        # Get API key
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Google API key is required. "
                "Set GOOGLE_API_KEY environment variable or pass api_key parameter."
            )
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def upload_file(self, file_path: str, display_name: Optional[str] = None) -> File:
        """
        Upload a file to Google's Generative AI.
        
        Args:
            file_path: Path to the file to upload
            display_name: Optional display name for the file
            
        Returns:
            The uploaded file object
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        path = Path(file_path)
        name = display_name or path.name
        
        print(f"Uploading file: {file_path}")
        uploaded_file = genai.upload_file(path=file_path, display_name=name)
        print(f"File uploaded successfully: {uploaded_file.name}")
        return uploaded_file
    
    def list_files(self) -> List[File]:
        """
        List all uploaded files.
        
        Returns:
            List of uploaded files
        """
        files = list(genai.list_files())
        return files
    
    def get_file(self, file_name: str) -> Optional[File]:
        """
        Get a specific file by name.
        
        Args:
            file_name: Name of the file to retrieve
            
        Returns:
            The file object if found, None otherwise
        """
        try:
            return genai.get_file(name=file_name)
        except Exception as e:
            print(f"Error retrieving file: {e}")
            return None
    
    def delete_file(self, file_name: str) -> bool:
        """
        Delete a file from Google's Generative AI.
        
        Args:
            file_name: Name of the file to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            genai.delete_file(name=file_name)
            print(f"File deleted successfully: {file_name}")
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def search_file(self, file_name: str, query: str) -> str:
        """
        Search within a file using a natural language query.
        
        Args:
            file_name: Name of the file to search
            query: Natural language search query
            
        Returns:
            The response from the AI model
        """
        file = self.get_file(file_name)
        if not file:
            raise ValueError(f"File not found: {file_name}")
        
        print(f"Searching file: {file_name}")
        print(f"Query: {query}")
        
        # Generate content using the file
        response = self.model.generate_content([file, query])
        return response.text
    
    def search_uploaded_file(self, uploaded_file: File, query: str) -> str:
        """
        Search within an uploaded file object using a natural language query.
        
        Args:
            uploaded_file: The uploaded file object
            query: Natural language search query
            
        Returns:
            The response from the AI model
        """
        print(f"Searching file: {uploaded_file.display_name}")
        print(f"Query: {query}")
        
        response = self.model.generate_content([uploaded_file, query])
        return response.text


def main():
    """Main function demonstrating basic usage."""
    
    # Check if API key is available
    load_dotenv()
    if not os.getenv('GOOGLE_API_KEY'):
        print("Error: GOOGLE_API_KEY not found in environment.")
        print("Please create a .env file with your Google API key.")
        print("See .env.example for reference.")
        return 1
    
    try:
        # Initialize the search application
        gfs = GFileSearch()
        
        # Example: List all files
        print("\n=== Listing all files ===")
        files = gfs.list_files()
        if files:
            for file in files:
                print(f"- {file.display_name} ({file.name})")
        else:
            print("No files found.")
        
        # Example usage with command-line arguments
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command == "upload" and len(sys.argv) > 2:
                file_path = sys.argv[2]
                uploaded_file = gfs.upload_file(file_path)
                print(f"\nFile uploaded: {uploaded_file.name}")
                
            elif command == "list":
                print("\n=== Files ===")
                files = gfs.list_files()
                for file in files:
                    print(f"{file.name}: {file.display_name}")
                    
            elif command == "search" and len(sys.argv) > 3:
                file_name = sys.argv[2]
                query = " ".join(sys.argv[3:])
                result = gfs.search_file(file_name, query)
                print(f"\n=== Search Results ===")
                print(result)
                
            elif command == "delete" and len(sys.argv) > 2:
                file_name = sys.argv[2]
                gfs.delete_file(file_name)
                
            else:
                print("Usage:")
                print("  python gfilesearch.py upload <file_path>")
                print("  python gfilesearch.py list")
                print("  python gfilesearch.py search <file_name> <query>")
                print("  python gfilesearch.py delete <file_name>")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

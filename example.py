#!/usr/bin/env python3
"""
Example usage of the Google File Search application.
"""

from gfilesearch import GFileSearch
import os


def example_usage():
    """Demonstrate how to use the GFileSearch application."""
    
    # Initialize (will use GOOGLE_API_KEY from environment)
    gfs = GFileSearch()
    
    # Example 1: Upload a file
    print("Example 1: Upload a file")
    print("-" * 50)
    # Uncomment and modify with your file path:
    # uploaded_file = gfs.upload_file("path/to/your/file.pdf")
    # print(f"Uploaded: {uploaded_file.name}\n")
    
    # Example 2: List all files
    print("Example 2: List all files")
    print("-" * 50)
    files = gfs.list_files()
    for file in files:
        print(f"- {file.display_name} ({file.name})")
    print()
    
    # Example 3: Search within a file
    print("Example 3: Search within a file")
    print("-" * 50)
    # Uncomment and modify with your file details:
    # result = gfs.search_file(
    #     file_name="files/your-file-id",
    #     query="What are the main topics in this document?"
    # )
    # print(f"Result: {result}\n")
    
    # Example 4: Search using an uploaded file object
    print("Example 4: Search with uploaded file object")
    print("-" * 50)
    # Uncomment and modify:
    # uploaded_file = gfs.upload_file("document.txt")
    # result = gfs.search_uploaded_file(
    #     uploaded_file,
    #     "Summarize this document"
    # )
    # print(f"Result: {result}\n")
    
    # Example 5: Delete a file
    print("Example 5: Delete a file")
    print("-" * 50)
    # Uncomment and modify:
    # gfs.delete_file("files/your-file-id")
    
    print("Examples completed!")


if __name__ == "__main__":
    example_usage()

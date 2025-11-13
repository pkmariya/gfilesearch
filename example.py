#!/usr/bin/env python3
"""
Example usage of the Google File Search application.

This script demonstrates various ways to use the GFileSearch class.
"""

from gfilesearch import GFileSearch
import os


def example_usage():
    """Demonstrate how to use the GFileSearch application."""
    
    print("=" * 60)
    print("Google File Search Application - Examples")
    print("=" * 60)
    
    # Initialize (will use GOOGLE_API_KEY from environment)
    try:
        gfs = GFileSearch()
        print("✓ Successfully initialized with API key\n")
    except ValueError as e:
        print(f"✗ Error: {e}")
        print("\nPlease set your GOOGLE_API_KEY in .env file")
        print("See .env.example for reference")
        return
    
    # Example 1: Upload a file
    print("Example 1: Upload a file")
    print("-" * 60)
    print("To upload a file, use:")
    print("  uploaded_file = gfs.upload_file('path/to/file.txt')")
    print("\nTry uploading the sample.txt file:")
    print("  uploaded_file = gfs.upload_file('sample.txt')")
    print("\nUncomment the code in this script to try it!\n")
    
    # Uncomment to actually upload:
    # uploaded_file = gfs.upload_file("sample.txt")
    # print(f"✓ Uploaded: {uploaded_file.name}\n")
    
    # Example 2: List all files
    print("Example 2: List all files")
    print("-" * 60)
    files = gfs.list_files()
    if files:
        print(f"Found {len(files)} file(s):")
        for file in files:
            print(f"  - {file.display_name} (ID: {file.name})")
    else:
        print("No files found in your account.")
    print()
    
    # Example 3: Search within a file
    print("Example 3: Search within a file")
    print("-" * 60)
    print("To search within a file, use:")
    print("  result = gfs.search_file(")
    print("      file_name='files/your-file-id',")
    print("      query='What are the main topics in this document?'")
    print("  )")
    print("\nExample queries you can try:")
    print("  - 'Summarize this document in 3 bullet points'")
    print("  - 'What are the key features mentioned?'")
    print("  - 'Extract all dates mentioned in the document'")
    print("\nUncomment the code in this script to try it!\n")
    
    # Uncomment to actually search (replace 'files/xxx' with actual file ID):
    # if files:
    #     result = gfs.search_file(
    #         file_name=files[0].name,
    #         query="What are the main topics in this document?"
    #     )
    #     print(f"Search result:\n{result}\n")
    
    # Example 4: Upload and immediately search
    print("Example 4: Upload and immediately search")
    print("-" * 60)
    print("You can chain operations:")
    print("  uploaded = gfs.upload_file('document.txt')")
    print("  result = gfs.search_uploaded_file(")
    print("      uploaded,")
    print("      'Summarize this document'")
    print("  )")
    print()
    
    # Example 5: Delete a file
    print("Example 5: Delete a file")
    print("-" * 60)
    print("To delete a file, use:")
    print("  gfs.delete_file('files/your-file-id')")
    print("\nOr to delete a file you just uploaded:")
    print("  uploaded = gfs.upload_file('temp.txt')")
    print("  gfs.delete_file(uploaded.name)")
    print()
    
    print("=" * 60)
    print("For more examples, see the README.md file")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()

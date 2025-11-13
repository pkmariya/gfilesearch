#!/usr/bin/env python3
"""
Simple tests for gfilesearch module
"""

import sys
import os

# Test 1: Import the module
print("Test 1: Import module")
try:
    from gfilesearch import GFileSearch
    print("✓ Module imported successfully")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Check that initialization fails without API key
print("\nTest 2: Initialization without API key")
try:
    gfs = GFileSearch()
    print("✗ Should have raised ValueError for missing API key")
    sys.exit(1)
except ValueError as e:
    if "Google API key is required" in str(e):
        print("✓ Correctly raises ValueError for missing API key")
    else:
        print(f"✗ Wrong error message: {e}")
        sys.exit(1)

# Test 3: Check initialization with API key (but no actual API calls)
print("\nTest 3: Initialization with API key")
try:
    gfs = GFileSearch(api_key="test_key_123")
    print("✓ Initialization with API key successful")
except Exception as e:
    print(f"✗ Initialization failed: {e}")
    sys.exit(1)

# Test 4: Verify methods exist
print("\nTest 4: Verify methods exist")
methods = ['upload_file', 'list_files', 'get_file', 'delete_file', 'search_file', 'search_uploaded_file']
for method in methods:
    if hasattr(gfs, method):
        print(f"✓ Method '{method}' exists")
    else:
        print(f"✗ Method '{method}' missing")
        sys.exit(1)

print("\n✅ All tests passed!")

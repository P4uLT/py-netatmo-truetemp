#!/usr/bin/env python3
"""Script to expire the Netatmo access token for testing."""

import json
import os

import platformdirs

# Use the same cache directory structure as the main application
cache_dir = platformdirs.user_cache_dir("netatmo", "py-netatmo-truetemp")
cookies_file = os.path.join(cache_dir, "cookies.json")

if not os.path.exists(cookies_file):
    print(f"Cookies file not found: {cookies_file}")
    exit(1)

# Read current cookies
with open(cookies_file, "r") as f:
    cookies = json.load(f)

# Create an expired token by modifying the current one
if "netatmocomaccess_token" in cookies:
    print(f"Current token: {cookies['netatmocomaccess_token']}")
    # Make token invalid by changing a character in the middle
    current_token = cookies["netatmocomaccess_token"]
    if len(current_token) > 10:
        # Replace middle section with invalid characters
        invalid_token = current_token[:20] + "EXPIRED_INVALID" + current_token[-20:]
        cookies["netatmocomaccess_token"] = invalid_token
        print(f"Modified token: {invalid_token}")
    else:
        print("Token too short, using placeholder")
        cookies["netatmocomaccess_token"] = "expired_token_for_testing"
else:
    print("No access token found in cookies")
    cookies["netatmocomaccess_token"] = "expired_token_for_testing"

# Write back the expired token
with open(cookies_file, "w") as f:
    json.dump(cookies, f, indent=2)

print(f"✓ Token expired and saved to {cookies_file}")

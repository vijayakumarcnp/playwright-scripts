#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "playwright",
#   "pytest-playwright",
# ]
# ///

"""test-loginazure.py here

at https://github.com/bomonike/playwright-scripts/blob/main/the-internet/test-loginazure.py

Test script for visiting all example links on the-internet.herokuapp.com.
Described at https://wilsonmar.github.io/flood-the-internet/

USAGE:
    git clone https://github.com/bomonike/playwright-scripts --depth 1
    cd flood-the-internet/the-internet
    python -m venv .venv
    source .venv/bin/activate
    uv pip install pytest pytest-playwright playwright -U
    playwright install  #  browser binaries: Chromium, Firefox, WebKit, FFMPEG
    # NOTE: cached in /Users/johndoe/Library/Caches/ms-playwright/ to run Playwright tests.

    pytest test-loginazure.py --browser chromium --headed
    deactivate
    rm -rf .venv .pytest_cache __pycache__
"""

__last_change__ = "25-10-31 v001 + login to azure :test_loginazure.py"
__status__ = "Run using warp."

import re
from playwright.sync_api import Page, expect

def test_azure_ai_login(page: Page):
    page.goto('https://ai.azure.com/')
    page.get_by_role('button', name='Sign in', exact=True).click()
    page.get_by_role('textbox', name='Enter your email, phone, or').fill('vijayakumar_cnp@yahoo.co.in')
    page.get_by_role('textbox', name='Enter your email, phone, or').press('Tab')
    page.get_by_role('button', name='Next').click()
    page.get_by_role('button', name='Use your password').click()
    page.get_by_role('textbox', name='Password').fill('Tomato#01')
    page.get_by_test_id('primaryButton').click()
    page.get_by_test_id('primaryButton').click()
    
    # Wait for navigation back to ai.azure.com after authentication
    page.wait_for_url('https://ai.azure.com/**', timeout=60000)
    
    # Wait for page to fully load after authentication
    page.wait_for_load_state('networkidle', timeout=60000)
    
    # Wait a bit more for any dynamic content to load
    page.wait_for_timeout(5000)
    
    # Try to find the AI Foundry settings button - use wait_for_selector with state visible
    settings_button = page.get_by_role('button', name='AI Foundry settings')
    if settings_button.count() > 0:
        settings_button.click(timeout=10000)
        page.get_by_role('button', name='Close settings panel').click()
    
    # Optional: Click profile if it exists
    profile_button = page.get_by_role('button', name='Profile with current')
    if profile_button.count() > 0:
        profile_button.click()
        page.get_by_label('', exact=True).get_by_text('VD').click()

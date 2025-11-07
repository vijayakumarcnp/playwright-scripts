#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "playwright",
#   "pytest-playwright",
#   "mailslurp_client",
# ]
# ///

"""test-loginazure.py here

at https://github.com/bomonike/playwright-scripts/blob/main/the-internet/test_loginazure.py

Test script for visiting all example links on the-internet.herokuapp.com.
Described at https://wilsonmar.github.io/azure-quickly
CAUTION: this method can be brittle because Yahoo's UI can change and often has dynamic selectors or requires handling login challenges like 2FA.

USAGE:
    git clone https://github.com/bomonike/playwright-scripts --depth 1
    cd playwright-scripts/azure
    python -m venv .venv
    source .venv/bin/activate
       # pip install -r requirements.txt
       # playwright>=1.55.0, pytest>=8.0.0, pytest-playwright>=0.6.0
    uv pip install pytest pytest-playwright playwright mailslurp_client -U
    playwright install  #  --browser Chromium, Firefox, WebKit, FFMPEG 
       # NOTE: cached in /Users/johndoe/Library/Caches/ms-playwright/ to run Playwright tests.

    pytest test_loginazure.py --browser chromium --headed
AFTER RUNS:
    deactivate
    rm -rf __pycache__ .pytest_cache .ruff_cache .venv  # specified in .gitignore
"""

__last_change__ = "25-11-07 v003 + .ruff_cache :test_loginazure.py"
__status__ = "Login confirmation not working."

#import re
import os
from playwright.sync_api import Page #, expect
from mailslurp_client import Configuration, ApiClient, InboxControllerApi, SendEmailOptionsApi

def mailslurp_yahoo_login(yahoomail_api_key):
    """ Automate login to yahoo mail using mailslurp.com API."""
    reading = True
    sending = False

    # using IMAP/SMTP settings in Yahoo for MailSlurp to access:
    # Read secrets from $HOME/aif.env
    configuration = Configuration(api_key={"x-api-key": yahoomail_api_key})
    api_client = ApiClient(configuration)

    
    # Create an inbox or use an existing connector inbox linked to Yahoo
    inbox_controller = InboxControllerApi(api_client)
    inbox = inbox_controller.create_inbox()

    # Poll or listen for new emails
    emails = inbox_controller.wait_for_latest_email(inbox.id, timeout=30000)

    if reading:
       print("reading!")
    if sending:
        # On receiving email, send an auto-reply
        send_api = SendEmailOptionsApi(api_client)
        send_api.send_email(inbox.id, {
            "to": [emails.from_],
            "subject": "Re: " + emails.subject,
            "body": "Thank you for your email. I will get back to you shortly."
        })


def test_azure_ai_login(page: Page):
    """ Login to Azure.
    In CLI: export AZURE_PASSWORD="???"; echo "AZURE_PASSWORD=$AZURE_PASSWORD"
    """
    my_password = os.environ.get('AZURE_PASSWORD')
    # TODO: Get values from $HOME/.aif.env file
    print(f"my_password={my_password}")
    exit()

    page.goto('https://ai.azure.com/')
    page.get_by_role('button', name='Sign in', exact=True).click()
    page.get_by_role('textbox', name='Enter your email, phone, or').fill('vijayakumar_cnp@yahoo.co.in')
    page.get_by_role('textbox', name='Enter your email, phone, or').press('Tab')
    page.get_by_role('button', name='Next').click()
    page.get_by_role('button', name='Use your password').click()
    page.get_by_role('textbox', name='Password').fill(my_password)
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

    # If "Help us protect your account" appears (optionally):
    # TODO 1: Click "I don't have these any more" then enter password again.
    # TODO 2: invoke mailslurp_yahoo_login(yahoomail_api_key) to automate log into Yahoo, nav to inbox, identify subject to open, answer verif. Yahoo email automatically. For more reliable Consider third-party email testing APIs (e.g., MailSlurp or Mailosaur).
    # TODO 3: Continue on Azure after login.
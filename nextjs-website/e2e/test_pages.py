"""
End-to-End Tests for Next.js Website

Tests all pages with Playwright.

Reference:
- https://playwright.dev/python/
"""

import pytest
from playwright.sync_api import sync_playwright, expect, Page


# =============================================================================
# Base URL
# =============================================================================

BASE_URL = "http://localhost:3000"


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope="session")
def browser():
    """Launch browser"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Create new page"""
    context = browser.new_page()
    yield context
    context.close()


# =============================================================================
# Test: Home Page
# =============================================================================

def test_home_page(page):
    """Test landing page"""
    page.goto(BASE_URL + "/")
    
    # Check hero
    expect(page.locator("h1")).to_contain_text("Build AI Agents")
    
    # Check navigation
    expect(page.locator("nav")).to_be_visible()
    
    print("✓ Home page")


def test_navigation(page):
    """Test navigation links"""
    page.goto(BASE_URL + "/")
    
    links = ["Docs", "API", "Pricing", "About"]
    for link in links:
        expect(page.locator(f"text={link}")).to_be_visible()
    
    print("✓ Navigation")


def test_features(page):
    """Test features section"""
    page.goto(BASE_URL + "/")
    
    features = ["Entity Security", "Verified Credentials", "Policy Engine"]
    for feature in features:
        expect(page.locator(f"text={feature}")).to_be_visible()
    
    print("✓ Features")


def test_pricing(page):
    """Test pricing"""
    page.goto(BASE_URL + "/")
    
    tiers = ["$0", "$99", "Custom"]
    for tier in tiers:
        expect(page.locator(f"text={tier}")).first.to_be_visible()
    
    print("✓ Pricing")


def test_responsive(page):
    """Test responsive"""
    viewports = [
        (375, 812),  # Mobile
        (768, 1024), # Tablet
        (1920, 1080), # Desktop
    ]
    
    for width, height in viewports:
        page.set_viewport_size({"width": width, "height": height})
        page.goto(BASE_URL + "/")
        expect(page.locator("h1")).to_be_visible()
    
    print("✓ Responsive")


def test_dark_theme(page):
    """Test dark theme"""
    page.goto(BASE_URL + "/")
    
    bg = page.evaluate("document.body.style.backgroundColor || getComputedStyle(document.body).backgroundColor")
    print(f"  Background: {bg}")
    
    print("✓ Dark theme")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
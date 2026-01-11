"""
CSS Loader Utility
Simple function to load the styles.css file in any page
"""
import streamlit as st
import os


def load_css():
    """
    Load the CSS file from assets/styles.css
    Call this function at the start of every page
    """
    # Get the path to the CSS file
    css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
    
    # Check if file exists
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Fallback: try relative path
        try:
            with open("assets/styles.css") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            # If CSS file not found, just continue without styling
            st.warning("⚠️ styles.css not found. Please ensure it's in the assets/ folder.")
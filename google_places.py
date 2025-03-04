import requests
import os

# API Key (Make sure you replace this with your actual API key)
API_KEY = "YOUR_API_KEY_HERE"

def search_places(query):
    """Search for places using Google Places API."""
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}"
    response = requests.get(url)
    return response.json()  # Return API response

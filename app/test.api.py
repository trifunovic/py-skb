import requests
import os

# Define the FastAPI server URL
BASE_URL = "http://127.0.0.1:8000"

# Define your API key (ensure this matches the API_KEY used in the FastAPI application)
API_KEY = os.getenv("knowledge-api-key")  # Replace with your actual API key

def test_rebuild_index():
    """
    Test the /rebuild-index/ endpoint with a POST request.
    """
    url = f"{BASE_URL}/rebuild-index/"
    headers = {"Authorization": API_KEY}

    print(f"Testing POST {url} with Authorization header...")

    try:
        response = requests.post(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Error Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

def test_search_endpoint(query: str):
    """
    Test the /search/ endpoint with a GET request.
    """
    url = f"{BASE_URL}/search/"
    headers = {"Authorization": API_KEY}
    params = {"query": query}

    print(f"Testing GET {url} with query: '{query}'...")

    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Error Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    # Test the /rebuild-index/ endpoint
    test_rebuild_index()

    # Test the /search/ endpoint
    test_search_endpoint("What is the capital of France?")

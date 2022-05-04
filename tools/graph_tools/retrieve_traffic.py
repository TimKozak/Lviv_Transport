# Seva Archakov
import requests
import json

API_KEY = "hw3AFDVIngralHMpM7xY5UlnbzDi60y4"
BASE_URL = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/20/json?key={API_KEY}"


def get_info(point):
    response = requests.get(f"{BASE_URL}&point={point[0]},{point[1]}")
    response_dict = response.json()
    # response_json = json.dumps(response_dict)
    return response_dict


if __name__ == "__main__":
    print(get_info((49.79804897912645, 24.0173781631986)))

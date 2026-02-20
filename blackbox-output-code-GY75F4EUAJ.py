import requests

def search_flights_api(destination, date):
    url = "https://api.amadeus.com/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {YOUR_ACCESS_TOKEN}"}
    params = {
        "originLocationCode": "NYC",
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": 1
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    # Parse the complex JSON response into a simple DataFrame
    # ... parsing logic ...
    return parsed_dataframe
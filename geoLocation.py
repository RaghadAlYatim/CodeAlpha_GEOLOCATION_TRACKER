import requests
import folium
from geopy.geocoders import Nominatim

from map import get_geolocation

def get_public_ip():
    """Tries to fetch the user's public IP address from multiple sources."""
    ip_services = [
        'https://api64.ipify.org?format=json',
        'https://checkip.amazonaws.com',
        'https://ifconfig.me'
    ]
    
    for service in ip_services:
        try:
            print(f"Trying {service}...")
            response = requests.get(service, timeout=10)
            
            if response.status_code == 200:
                # If using ipify parse JSON, otherwise return plain text
                if 'json' in service:
                    return response.json().get('ip')
                return response.text.strip()
        except requests.exceptions.RequestException:
            continue  # Try next service if one fails
    
    print("⚠️ Oops! Couldn't fetch your public IP from any service.")
    return None

def get_geolocation(ip_address=None):
    """gets geolocation data for given IP address."""
    if not ip_address:
        ip_address = get_public_ip()  # get user's IP if not provided

    if not ip_address:
        return None

    try:
        print(f"Looking up location for IP: {ip_address}...")
        response = requests.get(f'https://ipapi.co/{ip_address}/json/', timeout=5).json()
        
        return {
            'ip': ip_address,
            'city': response.get('city', 'Unknown'),
            'region': response.get('region', 'Unknown'),
            'country': response.get('country_name', 'Unknown'),
            'latitude': response.get('latitude', 0),  # Default to 0 if missing
            'longitude': response.get('longitude', 0)  # Default to 0 if missing
        }
    except requests.exceptions.RequestException:
        print(" Something went wrong while fetching location data. Try again later.")
    
    return None

def reverse_geocode(latitude, longitude):
    """If the API fails to provide a city name, use reverse geolocation as a fallback."""
    print("🛰️ Reverse geocoding to improve accuracy...")
    geolocator = Nominatim(user_agent="geo_locator")
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        return location.address if location else "Unknown Location"
    except:
        return "Unknown Location"

def create_map(latitude, longitude, city):
    """Generates an interactive map with a marker at the detected location."""
    print("Generating an interactive map...")
    user_map = folium.Map(location=[latitude, longitude], zoom_start=12)
    
    # Custom marker
    folium.Marker(
        [latitude, longitude], 
        popup=city, 
        tooltip="Click for more info",
        icon=folium.Icon(color="blue", icon="cloud")
    ).add_to(user_map)
    
    user_map.save("user_location_map.html")
    print("Map successfully created! Open 'user_location_map.html' to check it out")

if __name__ == "__main__":
    print(" Welcome to the IP Geolocation Tracker! ")
    
    ip = input("Enter an IP address to look up or press Enter to use your own IP: ").strip()
    location_data = get_geolocation(ip)
    
    if location_data:
        # If city is unknown, use reverse geolocation
        if location_data['city'] == "Unknown":
            location_data['city'] = reverse_geocode(location_data['latitude'], location_data['longitude'])
        
        print("\n📍 **Location Details:**")
        print(f"   - IP Address: {location_data['ip']}")
        print(f"   - Location: {location_data['city']}, {location_data['region']}, {location_data['country']}")
        print(f"   - Coordinates: ({location_data['latitude']}, {location_data['longitude']})\n")

        create_map(location_data['latitude'], location_data['longitude'], location_data['city'])
    else:
        print(" Sorry, we couldn't find location data. Try again later.")


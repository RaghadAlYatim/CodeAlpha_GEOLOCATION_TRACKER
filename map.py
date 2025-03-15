import requests
import folium

# Function to get geolocation details using an IP address
def get_geolocation(ip_address=""):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    data = response.json()
    
    # Check if the API request was successful
    if data["status"] == "fail":
        print("Could not retrieve location.")
        return None
    
    # Return relevant geolocation details
    return {
        "ip": data["query"],
        "city": data["city"],
        "region": data["regionName"],
        "country": data["country"],
        "lat": data["lat"],
        "lon": data["lon"],
        "isp": data["isp"]
    }

# Function to display the location on a map
def display_map(lat, lon):
    location_map = folium.Map(location=[lat, lon], zoom_start=10)
    
    # Add a marker at the given latitude and longitude
    folium.Marker([lat, lon], popup="Location Found", tooltip="Click for info").add_to(location_map)
    
    # Save the map as an HTML file
    location_map.save("geolocation_map.html")
    print("Map has been saved as 'geolocation_map.html'. Open it in a browser to view.")

# Main execution block
if __name__ == "__main__":
    # Prompt user for an IP address (or leave empty for their own IP)
    ip = input("Enter IP address (leave empty for your own IP): ")
    
    # Get geolocation data
    geolocation = get_geolocation(ip)
    
    if geolocation:
        # Display retrieved geolocation details
        print(f"IP Address: {geolocation['ip']}")
        print(f"Location: {geolocation['city']}, {geolocation['region']}, {geolocation['country']}")
        print(f"ISP: {geolocation['isp']}")
        
        # Generate and display the map
        display_map(geolocation['lat'], geolocation['lon'])


from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
from .. import models
from django.http import JsonResponse
import json
import math
API = "AIzaSyBmKpW3kRXseBgpH7VrOYRdrwHF-o-43Po"
API_LIMIT = 10000

@csrf_exempt
@require_http_methods(["POST"])
def get_location_handler(request):
    if models.APICallCount.get_count() >= API_LIMIT:
        return JsonResponse({'error': 'API call limit reached'}, status=429)
    data = json.loads(request.body)
    print(data)
    return(get_actual_location(data["body"]))
 


def get_actual_location(location):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address":location,
        "key":API,
        "language":"English",
    }
    address = requests.get(base_url, params=params)
    models.APICallCount.increment()
    print(address.json())
    if(address.status_code == 200):
        if(address.json().get("status")!= "ZERO_RESULTS"):
            results = address.json().get("results")
            results_parsed = results[0]["geometry"]["location"]   
            latitude = results_parsed["lat"]
            longitude = results_parsed["lng"]
            return(get_recommendations(latitude, longitude))
        else:
            return JsonResponse({"error": f'Please provide more information about the location.'})
    else:
        return JsonResponse({'error': f'Error, address unknown.'}, status=address.status_code)
    
def measure(lat1, lon1, lat2, lon2):  
    R = 6378.137; 
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000

def get_recommendations(latitude, longitude):
    if not latitude or not longitude:
        return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
    types = ['school']
    radius = 2000
    all_results = []
    for place_type in types:
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        params = {
            'location': f'{latitude},{longitude}',
            'radius': radius,
            'type': place_type,
            'key': API
        }
        
        response = requests.get(url, params=params)
        models.APICallCount.increment()
        if response.status_code == 200:
            results = response.json().get('results', [])
            formatted_results = [{
                'type': place_type,
                'name': place['name'],
                'location': {
                    'lat': place['geometry']['location']['lat'],
                    'lng': place['geometry']['location']['lng'],
                    'distance': round(measure(latitude, longitude, place['geometry']['location']['lat'], place['geometry']['location']['lng']))
                },
                'street': place["vicinity"],
                'icon':place['icon'],
                'link':"https://www.google.com/maps/place/"+place['name'].replace(" ","+")+"/@"+str(place['geometry']['location']['lat'])+","+str(place['geometry']['location']['lng'])
            } for place in results]
            all_results.extend(formatted_results)
        else:
            return JsonResponse({'error': f'Error fetching {place_type} places'}, status=response.status_code)

    return JsonResponse({'places': all_results})



@csrf_exempt
@require_http_methods(["POST"])
def reset_api_count(request):
    models.APICallCount.reset()
    return JsonResponse({'message': 'API count reset successfully'})

import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from steam_web_api import Steam
import os

def initializer():
    STEAM_API_KEY = '561393C6C362257D88FB5949D990C63A'
    steam = Steam(STEAM_API_KEY)
    return steam

@csrf_exempt
@require_http_methods(["POST"])
def get_steam_games(request): 
    steam_obj = initializer()
    try:
        steam_game_name = json.loads(request.body.decode('utf-8')) 
        all_apps = steam_obj.apps.search_games(steam_game_name["body"])
        formatted_apps = [{
            "ID": app["id"],
            "name": app["name"],
            "price": "To Be Released!" if app["price"] is None or app["price"] == "" else app["price"],
            "link": app["link"],
            "img": app["img"]
        } for app in all_apps.get("apps", [])]  
        return JsonResponse({"games": formatted_apps})
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": str(e)}, status=500)

from django.views.decorators.csrf import csrf_exempt
from .function_normalized import steam_api
from .function_normalized import map_api
from .function_normalized import wikipedia_api
# request handler

@csrf_exempt
def search_games(request):
    steam_default_data = steam_api.get_steam_games(request)
    print((steam_default_data))
    return steam_default_data

@csrf_exempt
def get_places(request):
    return(map_api.get_location_handler(request))

@csrf_exempt
def reset_api_requests(request):
    return(map_api.reset_api_count(request))


@csrf_exempt
def wikipedia_handler(request):
    return(wikipedia_api.wikipedia_search(request))
import wikipediaapi
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
def wikipedia_init():
    wiki_wiki = wikipediaapi.Wikipedia('Wikipedia Searcher (thomaltcobble@gmail.com)', 'en')
    return wiki_wiki

def text_parse(request):
    wiki_name = json.loads(request.body.decode('utf-8'))
    return(wiki_name["body"])

@csrf_exempt
@require_http_methods(['POST'])
def wikipedia_search(request):
    text = text_parse(request)
    wiki_obj = wikipedia_init()
    page = wiki_obj.page(text)

    if(page.exists()):
        format_wiki = [{
            "title": page.title,
            "link": page.fullurl,
            "text": (page.summary)
        }]
        return JsonResponse({"body": format_wiki})
    else:
        return JsonResponse({"error: Unable to find"})
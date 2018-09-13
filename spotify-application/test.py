import requests
import config
import json

def recommended_playlist():
    client_id = 'client_id=' + config.client_id
    scope_split = config.scope.split()
    scope = ''
    for x in scope_split:
        scope += str(x) + '%20'
    scope = scope[:-3]
    url = 'https://accounts.spotify.com/authorize/?' + client_id + '&response_type=code' + '&redirect_uri=http%3A%2F%2Flocalhost%2F' + '&scope=' + scope
    print(url)
    response = requests.get(url)
    print(response.status_code)
    print(response.json())
recommended_playlist()
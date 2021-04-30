import requests


def get_user_data(token):
    headers = {'Authorization': 'token %s' % token}
    r = requests.get('https://api.github.com/user', headers=headers)
    r.raise_for_status()
    return r.json()

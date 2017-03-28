import requests


def get_server_response(url):
    """
    :param url: Queried address URL
    :return: Server time and response code
    """
    response = requests.request('GET', url)
    return response.elapsed.total_seconds(), response.status_code

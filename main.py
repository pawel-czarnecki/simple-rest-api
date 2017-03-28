from time import sleep
from reader import Reader
from database import Database
from helpers import get_server_response
from rest_api import RestApi


def main():
    reader = Reader('config.yml')
    database = Database('sample.db')
    database.query('CREATE TABLE IF NOT EXISTS server_response(time REAL, code INTEGER)')

    rest_api = RestApi('127.0.0.1', 8000)
    rest_api.start()

    while rest_api.is_running:
        for link in reader.get_branch('urls'):
            srv_response = get_server_response(link['url'])
            database.query('INSERT INTO server_response (time, code) VALUES({time}, {code})'.format(
                time=srv_response[0],
                code=srv_response[1])
            )
            sleep(float(link['delay']))

    rest_api.stop()

main()

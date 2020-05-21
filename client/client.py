import json
from argparse import ArgumentParser
import requests
from datetime import datetime

from constants import HELP_MESSAGE, WRONG_COMMAND, WRONG_COMMAND_ARGUMENTS, CREATE_HEAD_MESSAGE, CREATE_BODY_MESSAGE, \
    NOTE_DOES_NOT_EXIST, SUCCESSFUL_DELETE, SCRIPT_EXIT, SURE_EXIT


def get_script_execution_parser():
    parser = ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('-p', '--port', default=8000, type=int)

    return parser


class NotesCommandsManager:

    def __init__(self, host, port, protocol='http'):
        self.host = host
        self.port = port
        self.base_url = f'{protocol}://{host}:{port}/'

    @staticmethod
    def help():
        print(HELP_MESSAGE)

    @staticmethod
    def exit():
        confirm_answer = input(SURE_EXIT)
        if confirm_answer.lower() in ['yes', 'y', 'да', 'д']:
            print(SCRIPT_EXIT)
            exit(0)

    def create(self):
        data = {
            'name': input(CREATE_HEAD_MESSAGE),
            'body': input(CREATE_BODY_MESSAGE)
        }
        self._execute_request('POST', 'note', data=data)

    def show(self, note_id=None):
        if note_id is None:
            notes = self._execute_request('GET', 'notes')['value']
            print(f'Найдено {len(notes)} заметок')
            for note in notes:
                date = datetime.fromtimestamp(note['date'])
                date_str = date.strftime("%d.%m %H:%M")
                print('{:<3} {}  {}'.format(note['id'], date_str, note['name']))

        else:
            response = self._execute_request('GET', 'note', str(note_id))
            if response['status'] == 'fail':
                print(NOTE_DOES_NOT_EXIST)
            else:
                note = response['value']
                date = datetime.fromtimestamp(note['date'])
                date_str = date.strftime("%A, %d %B %Y %H:%M")
                print('Номер: {}\nСоздано: {}\n{}\n{}'.format(note['id'], date_str, note['name'], note['body']))

    def delete(self, note_id):
        response = self._execute_request('DELETE', 'note', str(note_id))
        if response['status'] == 'fail':
            print(NOTE_DOES_NOT_EXIST)
        else:
            print(SUCCESSFUL_DELETE)

    def _execute_request(self, method, *args, data=None):
        request_url = self.base_url + '/'.join(args) + '/'
        if method in ['GET', 'POST', 'PUT', 'DELETE']:
            try:
                return getattr(requests, method.lower())(request_url, json=data).json()
            except json.decoder.JSONDecodeError:
                print('Получен невалидный ответ от сервера')
                return {
                    'status': 'fail',
                    'value': None
                }
        else:
            raise NotImplementedError


def main():
    script_parser = get_script_execution_parser()
    script_args = script_parser.parse_args()

    print(f'Host: {script_args.host}, port: {script_args.port}')
    commands_manager = NotesCommandsManager(script_args.host, script_args.port)
    commands_manager.help()
    while True:
        try:
            print('Введите команду: ', end='')

            command_items = input().split()
            command = command_items[0]

            getattr(commands_manager, command)(*command_items[1:])

        except KeyboardInterrupt:
            commands_manager.exit()

        except (AttributeError, IndexError):
            print(WRONG_COMMAND)

        except TypeError:
            print(WRONG_COMMAND_ARGUMENTS)

        print()


if __name__ == '__main__':
    main()

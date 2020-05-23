import json
from argparse import ArgumentParser
import requests
from datetime import datetime
from client import consts
import net_consts


def get_script_execution_parser():
    parser = ArgumentParser()
    parser.add_argument('--host', default=net_consts.DEFAULT_HOST)
    parser.add_argument('-p', '--port', default=net_consts.DEFAULT_PORT, type=int)

    return parser


class NotesCommandsManager:

    def __init__(self, host, port, protocol=net_consts.DEFAULT_PROTOCOL):
        self.host = host
        self.port = port
        self.base_url = f'{protocol}://{host}:{port}/'

    @staticmethod
    def help():
        print(consts.HELP_MESSAGE)

    @staticmethod
    def exit():
        confirm_answer = input(consts.SURE_EXIT)
        if confirm_answer.lower() in consts.USER_POSITIVE_ANSWERS:
            print(consts.SCRIPT_EXIT)
            exit(0)

    def create(self):
        data = {
            'name': input(consts.CREATE_HEAD_MESSAGE),
            'body': input(consts.CREATE_BODY_MESSAGE)
        }
        self._execute_request('POST', net_consts.ONE_NOTE_PATH, data=data)

    def show(self, note_id=None):
        if note_id is None:
            notes = self._execute_request('GET', net_consts.MANY_NOTES_PATH)['value']
            print(consts.NOTES_FOUND_COUNT % len(notes))
            for note in notes:
                date = datetime.fromtimestamp(note['date'])
                date_str = date.strftime(consts.MANY_NOTES_DATE_FORMAT)
                print(consts.MANY_NOTES_FORMAT.format(
                    id=note['id'], date=date_str, name=note['name'])
                )

        else:
            response = self._execute_request('GET', net_consts.ONE_NOTE_PATH, str(note_id))
            if response['status'] == net_consts.RESPONSE_FAIL_STATUS:
                print(consts.NOTE_DOES_NOT_EXIST)
            else:
                note = response['value']
                date = datetime.fromtimestamp(note['date'])
                date_str = date.strftime(consts.ONE_NOTE_DATE_FORMAT)
                print(consts.ONE_NOTE_FORMAT.format(
                    id=note['id'], date=date_str, name=note['name'], body=note['body'])
                )

    def delete(self, note_id):
        response = self._execute_request('DELETE', net_consts.ONE_NOTE_PATH, str(note_id))
        if response['status'] == net_consts.RESPONSE_FAIL_STATUS:
            print(consts.NOTE_DOES_NOT_EXIST)
        else:
            print(consts.SUCCESSFUL_DELETE)

    def _execute_request(self, method, *args, data=None):
        request_url = self.base_url + '/'.join(args)
        if method in ['GET', 'POST', 'DELETE']:
            try:
                return getattr(requests, method.lower())(request_url, json=data).json()
            except json.decoder.JSONDecodeError:
                print(consts.RESPONSE_WRONG)
                return {
                    'status': net_consts.RESPONSE_FAIL_STATUS,
                    'value': None
                }
        else:
            raise NotImplementedError


def main():
    script_parser = get_script_execution_parser()
    script_args = script_parser.parse_args()

    print(consts.START_MESSAGE_FORMAT.format(host=script_args.host, port=script_args.port))
    commands_manager = NotesCommandsManager(script_args.host, script_args.port)
    commands_manager.help()
    while True:
        try:
            command_items = input(consts.ENTER_COMMAND).split()
            command = command_items[0]
            getattr(commands_manager, command)(*command_items[1:])

        except KeyboardInterrupt:
            commands_manager.exit()

        except (AttributeError, IndexError):
            print(consts.WRONG_COMMAND)

        except TypeError:
            print(consts.WRONG_COMMAND_ARGUMENTS)

        print()


if __name__ == '__main__':
    main()

from flask import Flask, jsonify, request
from flask.views import MethodView

from notes_manager import NotesManager
from functools import wraps
from time import time
from traceback import print_exc
from argparse import ArgumentParser
from net_consts import *

app = Flask(__name__)

notes_manager = NotesManager()


def request_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        in_time = time()
        request_data = request.get_json()
        response_failed = False
        response = None
        try:
            if request_data:
                response = func(*args, request_data, **kwargs)
            else:
                response = func(*args, **kwargs)
        except:
            print_exc()
            response_failed = True

        response_object = {
            'processing_time': round(time() - in_time, 3),
            'status': RESPONSE_FAIL_STATUS if response_failed else RESPONSE_SUCCESS_STATUS,
            'value': response
        }
        return jsonify(response_object)

    return wrapper


class NoteAPI(MethodView):
    @request_wrapper
    def get(self, note_id=None):
        if note_id is None:
            return notes_manager.get_all_notes()
        else:
            return notes_manager.get_note(int(note_id))

    @request_wrapper
    def post(self, note_data: dict):
        notes_manager.create_note(note_data)

    @request_wrapper
    def delete(self, note_id):
        notes_manager.delete_note(int(note_id))


note_view = NoteAPI.as_view('note_api')

app.add_url_rule(f'{MANY_NOTES_PATH}', view_func=note_view, methods=['GET'])
app.add_url_rule(f'{ONE_NOTE_PATH}', view_func=note_view, methods=['POST', 'PUT'])
app.add_url_rule(f'{ONE_NOTE_PATH}<int:note_id>/', view_func=note_view, methods=['GET', 'DELETE'])


def main():
    parser = ArgumentParser()
    parser.add_argument('--host', default=DEFAULT_HOST)
    parser.add_argument('--port', default=DEFAULT_PORT, type=int)
    command_line_args = parser.parse_args()
    host = command_line_args.host
    port = command_line_args.port
    app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    main()

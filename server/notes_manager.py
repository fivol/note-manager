from datetime import datetime
from database import NoteModel


def get_current_time():
    return datetime.now().timestamp()


class NotesStorage:

    @staticmethod
    def have_note(note_id: int):
        return bool(NoteModel.get_or_none(note_id))

    @staticmethod
    def delete(note_id: int):
        NoteModel.delete_by_id(note_id)

    @staticmethod
    def get(note_id: int):
        note = NoteModel.get_by_id(note_id)
        return note.__data__

    @staticmethod
    def create(note: dict):
        return NoteModel.create(**note)

    @staticmethod
    def get_all():
        return list(NoteModel.select(NoteModel.id, NoteModel.date, NoteModel.name).dicts())


class NotesManager:
    def __init__(self):
        self.storage = NotesStorage()

    def is_valid_note_id(self, note_id):
        return self.storage.have_note(note_id)

    def get_all_notes(self):
        return self.storage.get_all()

    def get_note(self, note_id):
        return self.storage.get(note_id)

    def create_note(self, note_data: dict):
        note_data['date'] = get_current_time()
        print(note_data)
        self.storage.create(note_data)

    def delete_note(self, note_id):
        self.storage.delete(note_id)

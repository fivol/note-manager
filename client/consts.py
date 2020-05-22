
# Запросы на получение данных от пользователя
CREATE_BODY_MESSAGE = "Напишите что-угодно и нажмите enter: "
CREATE_HEAD_MESSAGE = "Введите название заметки: "
UPDATE_MESSAGE = "Укажите новое содержание: "
ENTER_COMMAND = "Введите команду: "
SURE_EXIT = "Вы уверены, что хотие выйти? (да/нет): "
USER_POSITIVE_ANSWERS = ['y', 'yes', 'д', 'да']

# Информационные сообщения пользователю
NOTE_DOES_NOT_EXIST = "Заметки с таким номером не существует"
SUCCESSFUL_DELETE = "Заметка успешно удалена"
RESPONSE_WRONG = "Получен невалидный ответ от сервера"
SCRIPT_EXIT = "Выход из программы"
NOTES_FOUND_COUNT = 'Найдено %s заметок'
WRONG_COMMAND = "Введена некорректная команда"
WRONG_COMMAND_ARGUMENTS = "Неверные аргументы для команды"

HELP_MESSAGE = """Команды для взаимодействия с менеджером заметок:
1. exit - чтобы выйти из программы
2. help - показать это сообщение
3. create - создать новую заметку
4. show - посмотреть все существующие заметки
5. show <id> - показать заметку с определенным id
6. delete <id> - удалить заметку с указанным id
7. update <id> - обновить указанную заметку
"""

# Константы вывода данных
MANY_NOTES_DATE_FORMAT = "%d.%m %H:%M"
MANY_NOTES_FORMAT = '{id:<3} {date}  {name}'

ONE_NOTE_DATE_FORMAT = "%A, %d %B %Y %H:%M"
ONE_NOTE_FORMAT = 'Номер: {id}\nСоздано: {date}\n{name}\n{body}'


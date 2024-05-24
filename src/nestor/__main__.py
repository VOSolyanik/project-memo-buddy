import shlex
from typing import List, Tuple

from nestor.handlers.contacts import ContactsHandler
from nestor.handlers.notes import NotesHandler
from nestor.services.colorizer import Colorizer
from nestor.services.serializer import Serializer
from nestor.models.contacts_book import ContactsBook
from nestor.models.notes_book import NotesBook
from nestor.services.ui import CommandLineInterface

def parse_input(user_input: str) -> Tuple[str, List[str]]:
    parts = shlex.split(user_input)
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, *args


def main():
    # load ContactsBook and initialize contacts handler
    serializer = Serializer('data')
    ui = CommandLineInterface()
    storage = serializer.load_data()
    contacts_handler = ContactsHandler(storage.contacts_book)
    notes_handler = NotesHandler(storage.notes_book)

    ui.output(Colorizer.highlight("Welcome to the assistant bot!"))

    while True:
        user_input = ""
        try:
            user_input = ui.input(Colorizer.info("Enter a command: "))
        # handle Exit on Ctrl+C
        except KeyboardInterrupt:
            ui.output(Colorizer.highlight("\nGood bye!"))
            serializer.save_data(storage)
            break

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            ui.output(Colorizer.highlight("Good bye!"))
            serializer.save_data(storage)
            break
        elif command == "hello":
            ui.output(Colorizer.highlight("How can I help you?"))
        elif command == "help":
            #todo: Implement
            pass
        elif command in ContactsHandler.get_available_commands():
            ui.output(contacts_handler.handle(command, *args))
        elif command in NotesHandler.get_available_commands():
            ui.output(notes_handler.handle(command, *args))
        else:
            ui.output(Colorizer.error("Invalid command."))

if __name__ == "__main__":
    main()
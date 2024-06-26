import shlex
from typing import List, Tuple

from nestor.handlers.contacts import ContactsHandler
from nestor.handlers.notes import NotesHandler
from nestor.services.colorizer import Colorizer
from nestor.services.serializer import Serializer
from nestor.services.ui import CommandLineInterface

def parse_input(user_input: str) -> Tuple[str, List[str]]:
    parts = shlex.split(user_input)
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, *args

def main():
    serializer = Serializer('data')
    cli = CommandLineInterface()
    # load storage and initialize handlers
    storage = serializer.load_data()
    contacts_handler = ContactsHandler(storage.contacts_book, cli)
    notes_handler = NotesHandler(storage.notes_book, cli)

    cli.output(Colorizer.highlight("Welcome to the assistant bot!"))
    
    while True:
        user_input = ""
        try:
            user_input = cli.prompt(
                "Enter a command: ", 
                completion=[
                    "hello", "help", "close", "exit",
                    *ContactsHandler.get_available_commands(),
                    *NotesHandler.get_available_commands()
                ]
            )
        # handle Exit on Ctrl+C
        except KeyboardInterrupt:
            cli.output(Colorizer.highlight("\nGood bye!"))
            serializer.save_data(storage)
            break

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            cli.output(Colorizer.highlight("Good bye!"))
            serializer.save_data(storage)
            break
        elif command == "hello":
            cli.output(Colorizer.highlight("How can I help you?"))
        elif command == "help":
            if args:
                if args[0] in ContactsHandler.get_available_commands():
                    cli.output(contacts_handler.help(args[0]))
                elif args[0] in NotesHandler.get_available_commands():
                    cli.output(notes_handler.help(args[0]))
                else:
                    cli.output(Colorizer.error("Invalid command."))
            else:
                cli.output(contacts_handler.help())
                cli.output(notes_handler.help())
        elif command in ContactsHandler.get_available_commands():
            cli.output(contacts_handler.handle(command, *args))
        elif command in NotesHandler.get_available_commands():
            cli.output(notes_handler.handle(command, *args))
        else:
            cli.output(Colorizer.error("Invalid command."))

if __name__ == "__main__":
    main()
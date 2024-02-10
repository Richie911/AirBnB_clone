#!/usr/bin/python3
import cmd
import json
import shlex
from models import storage
from models.base_model import BaseModel
from shlex import split
import re

from models.engine.file_storage import FileStorage


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Command interpreter for HBNB program."""
    prompt = "(hbnb) "
    __model_list = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
        }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Handle the End-of-File (EOF) to exit the program."""
        print("")  # Print a new line before exiting
        return True

    def emptyline(self):
        """Do nothing on an empty line."""
        pass

    def do_create(self, arg):
        """Create a new instance, save it, and print the ID."""

        if len(arg) == 0:
            print("** class name missing **")
        elif arg not in HBNBCommand.__model_list:
            print("** class doesn't exist **")
        else:
            print(eval(arg)().id)
            storage.save()

    def do_show(self, arg):
        """Print the string representation of
        an instance based on class name and ID."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.__model_list:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        data = storage.all()

        if key not in data:
            print("** no instance found **")
            return
        print(f"[{class_name}] ({instance_id}) {data[key]}")

    def do_destroy(self, arg):
        """Deletes an instance based on class name and id."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.__model_list:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        print(key)
        if key.split(".")[0] not in HBNBCommand.__model_list:
            print("** no instance found **")
            return
        data = storage.all()
        del data[key]
        with open('file.json', 'w') as file:
            json.dump(data, file, indent=2)

    def do_all(self, arg):
        """Print all string representations of instances."""
        if arg not in HBNBCommand.__model_list:
            print("** class doesn't exist **")
            return
        data = storage.all()
        filtered = []
        for key, value in data.items():
            if key.startswith(arg):
                split_data = key.split(".")
                filtered.append(f"[{split_data[0]}] ({split_data[1]}) {value}")
        print(filtered)

    def do_update(self, arg):
        """Updates an instance based on class name and id."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.__model_list:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        data = storage.all()
        key = "{}.{}".format(class_name, instance_id)
        if key not in data:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        attribute_name = args[2]
        if len(args) < 4:
            print("** value missing **")
            return

        attribute_value = args[3]
        instance = data[key]

        instance[attribute_name] = attribute_value
        data[key] = instance
        with open('file.json', 'w') as file:
            json.dump(data, file, indent=2)


if __name__ == "__main__":
    HBNBCommand().cmdloop()

#!/usr/bin/env python
"""

Usage:
    amity create_room <room_type> (<room_name>)...
    amity add_person <firstname> <surname> <designation> [<wants_accommodation>]
    amity allocate_room <ID> <room_type>
    amity reallocate <person_identifier> <room_name>
    amity print_room <room_name>
    amity load_people <doc>
    amity print_allocations [filename] 
    amity print_unallocated [filename]
    amity save_state [--db=sqlite_database]
    amity load_state <load_file>
    amity (-i | --interactive)
    amity (-h | --help | --version)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    -d, --db=<opt>  Save state to database
"""

import sys
import cmd
import os
import pyfiglet
import colorama
from termcolor import *
from docopt import docopt, DocoptExit
from amity import Amity
from person import Person, Staff, Fellow
from room import Room, Livingspace, Office

colorama.init()


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


def yellow(string):
    return colored(string, 'yellow')


def cyan(string):
    return colored(string, 'cyan')


def green(string):
    return colored(string, 'green')


def blue(string):
    return colored(string, 'blue')


def red(string):
    return colored(string, 'red')


def intro():
    os.system("clear")
    pyfiglet.print_figlet("AMITY", 'slant')
    print('-' * 40)
    print(blue('Automated Space Allocation System'))
    print('-' * 40)
    print(blue('\nHere are the acceptable commands:'))
    print(cyan('~' * 40))
    print(yellow('''
    create_room <room_type> <room_name(s)>
    add_person <firstname> <surname> <designation> <Y/N>
    reallocate <ID> <room_name>
    print_room <room_name>
    load_people <filename>
    print_allocations <filename>
    print_unallocated <filename>
    save_state [--db=sqlite_database]
    load_state <load_file>
    '''))


class Facilities(cmd.Cmd):
    prompt = yellow('Amity>>> ')

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room (office | livingspace) <room_name>...
        """
        room_names = []
        for room in args["<room_name>"]:
            room = room.capitalize()
            room_names.append(room)
        room_type = "office" if args['office'] else "livingspace"
        print Amity().create_room(room_names, room_type)

    @docopt_cmd
    def do_add_person(self, args):
        """
        Usage: 
        add_person <firstname> <surname> <designation> [<wants_accommodation>]
        """
        firstname = args["<firstname>"].capitalize()
        surname = args['<surname>'].capitalize()
        designation = args['<designation>']
        resident = args['<wants_accommodation>'].upper() if args['<wants_accommodation>'] else 'N'
        print Amity().add_person(firstname, surname, designation, resident)

    @docopt_cmd
    def do_reallocate(self, args):
        """Usage: reallocate <person_identifier> <new_room_name>
        """

        ID = args['<person_identifier>']
        room_name = args['<new_room_name>'].capitalize()
        print Amity().reallocate(ID, room_name)

    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [<filename>]

        Options:
        -o, filename  Print to file
        """
        filename = args['<filename>'] if args['<filename>'] else None
        Amity().print_allocations(filename)

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [<filename>]
        """
        filename = args['<filename>'] if args['<filename>'] else None
        Amity().print_unallocated(filename)

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>
        """
        room_name = args['<room_name>'].capitalize()
        Amity().print_room(room_name)

    @docopt_cmd
    def do_load_people(self, args):
        """Usage: load_people <doc>
        """
        doc = args['<doc>']
        print Amity().load_people(doc)

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=sqlite_database]

        Options:
        -d,--db=sqlite_database  Save state to database 
        """
        savefile = args['--db']
        print Amity().save_state(savefile)

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state <load_file> 
        """
        load_file = args['<load_file>']
        print Amity().load_state(load_file)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print(green('Good Bye!'))
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    intro()
    Facilities().cmdloop()

print(opt)

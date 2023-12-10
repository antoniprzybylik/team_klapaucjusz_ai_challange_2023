#!/usr/bin/python3

"""
Εξερευνητής (Exereunetes)

Imagine some IT system you do not know written in
programming language you do not know and relying on
technologies you know nothing about. You have a
task of fixing some bug in this system or task of
adding functionallity to this system. How do you do
this?

Exereunetes tool can do this for you. It uses RAG technique
to make chat GPT 4 learn the system and solve your problem.
Just put the project's code in same directory as exereunetes.py
and run exereunetes!

In particular this program provides such functionallity:
- Adding functionalities to already existing code
- Generating documentation
- Describing already existing code and it's subsystems.

More precise description of how to use the program
is in README.md file.
"""

import argparse
from cmd_chat import cmd_chat
from cmd_apply import cmd_apply


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("prompt")
    parser.add_argument("-m", "--max-prompts",
                        type=int, default=1000)
    args = parser.parse_args()

    if args.command == "chat":
        print(cmd_chat(args.prompt, args.max_prompts))
    elif args.command == "apply":
        fp = open(args.prompt, "r")
        print(cmd_apply(fp.read(), args.max_prompts))
    else:
        print(f"exereunetes: {args.command}: Unknown command.")


if __name__ == "__main__":
    main()

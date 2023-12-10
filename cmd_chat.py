"""
cmd_chat.py

Imagine some IT system you do not know written in
programming language you do not know and relying on
technologies you know nothing about. You have a
task of fixing some bug in this system or task of
adding functionallity to this system. How do you do
this?

This program can do this for you. It uses RAG technique
to make chat GPT 4 learn the system and solve your problem.

In particular this program provides such functionallity:
- Adding functionalities to already existing code
- Generating documentation
- Describing already existing code and it's subsystems.
"""

import re
import os
from openai import OpenAI


with open("api_key.txt", "r") as fp:
    client = OpenAI(api_key=fp.read().rstrip())


basic_message = \
"Django-School-Management-System is a school " + \
"management system based on Django framework." + \
"The app is " +\
"meant to be used by school manager to manage " + \
"their school records such as: student data, " + \
"staff, results and finances. " + \
"It currently does not " + \
"allow students/staff to login. The system's code " + \
"should be compliant with isort and black linters. " + \
"The project's structure is as follows: \n" + \
"In the root directory of the project " + \
"(which is ./Django-School-Management-System/) there are present files " + \
"README.md and requirements.txt and directories " + \
"apps, school_app, static, templates.\n" + \
"Directory apps contains Django apps that make up " + \
"the components of the school management system.\n" + \
"Directory school_app is the main Django project directory.\n" + \
"Directory static stores static files for the application " + \
"such as JavaScript, CSS and images.\n" + \
"Directory templates contains the Django HTML template files.\n" + \
"The code of Django-School-Management-System is in " + \
"./Django-School-Management-System/ directory in current " + \
"working directory. The current working directory is " + \
"a root directory of another project's code and is not " + \
"a root directory of Django-School-Management-System's " + \
"code.\n\n" + \
"For example, if your task is to read README of the " + \
"project, read " + \
"file Django-Management-System/README.md. Do not read " + \
"files in current working directory (./)."


project_name = "Django-School-Management-System"


vm_definition = \
"GET_FILE(<filename>) - Retrieves " + \
"content of file <filename>. " + \
"<filename> is bare name, without any " + \
"quote marks.\n" + \
"FILE_SUMMARY(<filename>) - Summarizes " + \
"content of file <filename>. " + \
"<filename> is bare name, without any " + \
"quote marks.\n" + \
"LIST_DIRECTORY(<dirname>) - Lists " + \
"files in <dirname> directory. " + \
"<dirname> is bare name, without any " + \
"quote marks.\n" + \
"GREP(<pattern>) - Search for " + \
"<pattern> in every file in the " + \
"repository. " + \
"Pattern should not be in " + \
"quotation marks. If you enclose " + \
"pattern in quotation marks, " + \
"grep command fails.\n" + \
"GET_SIZE(<filename>) - Shows " + \
"size of file <filename> in bytes. " + \
"<filename> is bare name, without any " + \
"quote marks.\n"


def get_size(file):
    try:
        return str(os.path.getsize(file)) + " bytes\n"
    except:
        return "GET_SIZE: No such file.\n"


def summarize(filename):
    try:
        fp = open(filename, "r")
        content = fp.read()
    except:
        return "FILE_SUMMARY: No such file.\n"

    dialog = []
    dialog.append({"role": "system",
                   "content": "You are an element of " +
                   "Retrieval Augmented Generation (RAG) " +
                   "chain.\n" +
                   "Your task is to generate summaries of given files. " +
                   "Your summaries will then be embedded, they " +
                   "should be optimized for embedding.\n" +
                   "Files you will receive all come from " +
                   f"{project_name} project's " +
                   "repository.\n" +
                   basic_message + "\n"})
    dialog.append({"role": "user",
                   "content": "Summarize content of " +
                   f"file \"{filename}\":\n" +
                   f"{content}"})

    completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=dialog
    )

    return completion.choices[0].message.content + "\n"


def scan_dir(directory, pattern):
    response = ""

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = list(file.readlines())
                    for line_number, line in enumerate(lines,
                                                       start=1):
                        matches = re.findall(pattern, line)

                        if matches:
                            response += f"{file_path}:{line_number}\n"
            except:
                pass

    if len(response) == 0:
        return "GREP: Your pattern did not match any file.\n"
    else:
        return response


def interpret_cmd(command):
    if command[:15] == "LIST_DIRECTORY(":
        dir = command[15:-1]
        try:
            return command + "\n" + \
                ' '.join(os.listdir(dir)) + "\n\n"
        except:
            return command + "\n" + \
                command.split('(')[0] + ": No such directory.\n\n"
    elif command[:9] == "GET_FILE(":
        file = command[9:-1]

        try:
            fp = open(file, "r")
            if os.path.getsize(file) > 200000:
                return command + "\n" + \
                    command.split('(')[0] + ": File is too large.\n\n"
            return command + "\n" + \
                ''.join(fp.readlines()) + "\n\n"
        except:
            return command + "\n" + \
                command.split('(')[0] + ": No such file.\n\n"
    elif command[:9] == "GET_SIZE(":
        file = command[9:-1]
        try:
            return command + "\n" + \
                get_size(file) + "\n"
        except:
            return command + "\n" + \
                command.split('(')[0] + ": Error.\n\n"
    elif command[:13] == "FILE_SUMMARY(":
        file = command[13:-1]
        try:
            return command + "\n" + \
                summarize(file) + "\n"
        except:
            return command + "\n" + \
                command.split('(')[0] + ": Error.\n\n"
    elif command[:5] == "GREP(":
        pattern = command[5:-1]
        if pattern[0] == "\"" or \
           pattern[0] == "'":
            return command + "\n" + \
                command.split('(')[0] + ": Error: You should not enclose " + \
                                        "pattern in quotation marks.\n\n"

        try:
            return command + "\n" + \
                scan_dir('./', pattern) + "\n"
        except:
            return command + "\n" + \
                command.split('(')[0] + ": Error.\n\n"
    else:
        return command.split('(')[0] + ": Unknown command.\n\n"


def interpret(commands):
    info = ""
    for command in commands.split('\n'):
        info += interpret_cmd(command)

    return info


def can_you_do_this(task, info):
    dialog = []
    dialog.append({"role": "system",
                   "content": "You are an element of " +
                   "Retrieval Augmented Generation (RAG) " +
                   "chain.\n" +
                   "The chain must acquire information necessary" +
                   "for Chat GPT 4 to solve user specified " +
                   "problem " +
                   f"related to {project_name}.\n" +
                   basic_message + "\n" +
                   "Your task is to determine " +
                   "whether already acquired data is " +
                   "enought to solve the problem or do we " +
                   "need to acquire more data. " +
                   "Your response should be either YES or NO. " +
                   "Do not put any other text in your " +
                   "response.\n" +
                   "You should respond with YES if and only if " +
                   "you are 100% sure that you are able to write " +
                   "complete working " +
                   "example of code which solves the user's " +
                   "problem.\n" +
                   "\nDo not guess the solution by just " +
                   "filenames. Do not guess what code " +
                   "is in file based on it's name, always " +
                   "make sure.\n" +
                   "\nThe data will be in form of command " +
                   "history. It contains commands and their " +
                   "output. Commands present in the history: \n" +
                   vm_definition})
    dialog.append({"role": "user",
                   "content": "Can you solve problem: " +
                   f"\"{task}\"? You have this information " +
                   "acquired by commands in eariler part of RAG chain:\n" +
                   f"{info}"})

    completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=dialog
    )

    return completion.choices[0].message.content


def solve_problem(task, info):
    dialog = []
    dialog.append({"role": "system",
                   "content": "You are at the end of " +
                   "Retrieval Augmented Generation (RAG) chain. " +
                   "You must solve the problem basing on" +
                   "acquired data. Task you have to solve is " +
                   f"related to {project_name}.\n" +
                   basic_message + "\n"})
    dialog.append({"role": "user",
                   "content": "Solve this problem: " +
                   f"\"{task}\" given this information: " +
                   f"\"{info}\"."})

    completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=dialog
    )

    return completion.choices[0].message.content


def what_gpt_needs(task, info):
    dialog = []
    dialog.append({"role": "system",
                   "content": "You are an element of " +
                   "Retrieval Augmented Generation (RAG) " +
                   "chain. You have ability to call commands of " +
                   "special virtual machine in order to retrieve data " +
                   "you need. " +
                   "Output of command calls you request will be given to " +
                   "you in future prompts. " +
                   "Output of command calls you requested in previous " +
                   "interactions is given to you. " +
                   "You should use the data you requested in previous " +
                   "prompts the best way you can to choose " +
                   "commands of the virtual machine that will give " +
                   "you the data you need." +
                   "Your response should contain only commands of the " +
                   "virtual machine. It cannot contain any other text.\n" +
                   "Your task is to acquire information necessary" +
                   "for Chat GPT 4 to solve user specified problem " +
                   f"related to {project_name}.\n" +
                   basic_message + "\n" +
                   "The virtual machine you have ability to use " +
                   "has these commands:\n" +
                   vm_definition +
                   "\nRemember to ask only for files " +
                   "and directories you are sure exist. " +
                   "Do not hallucinate. Do not ask for files " +
                   "which does not exist.\n" +
                   "\nDo not repeat commands which " +
                   "were already executed and their output " +
                   "can be found in the data.\n" +
                   "\nNote that you can receive at most " +
                   "128000 tokens as input (you are gpt-4-1106-preview). " +
                   "In order to not reach the maximum number of tokens, " +
                   "you should not always use GET_FILE command. " +
                   "If you don't need whole content of some file, you " +
                   "should use FILE_SUMMARY command.\n" +
                   "\nYou may use GET_SIZE command to check size " +
                   "of files and avoid getting to big files which " +
                   "would crash the program.\n"})
    dialog.append({"role": "user",
                   "content": "This is the task you have to solve: " +
                   f"\"{task}\".\n" +
                   "This is the output of command calls " +
                   "requested by you in previous iterations:\n" +
                   f"{info}\n" +
                   "Feel free to call any command of the virtual machine " +
                   "you want."})

    completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=dialog
    )

    return completion.choices[0].message.content


def cmd_chat(task, max_prompts):
    info = ""
    prompt_no = 1
    while can_you_do_this(task, info) != "YES":
        if prompt_no + 1 > max_prompts:
            break

        print(f"\033[31;1m{prompt_no}.\033[0m " +
              "\033[32;1mI can't solve your problem.\033[0m")
        prompt_no += 1
        what_needs = what_gpt_needs(task, info)
        print(f"\033[31;1m{prompt_no}.\033[0m " +
              "\033[32;1mRequest information.\033[0m")
        prompt_no += 1
        print(what_needs)
        info += interpret(what_needs)
        print("---")
        print(info)
        print("---")

    print(f"\033[31;1m{prompt_no}.\033[0m "
          "\033[32;1mI can solve your problem.\033[0m")

    return solve_problem(task, info)

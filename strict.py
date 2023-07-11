import sys
import re
import time

with open(sys.argv[1], 'r') as f:
    content = f.read().split("\n")

var_list = {}
dogears = {}
array_list = {}

curr_line = 0
content_length = len(content) - 1
return_lines = []
uncaps = False
debug = False

def get_string(string):
    '''Just turns "Meow" into Meow'''
    return string[:-1][1:]


def sys_print(text):
    '''Print that does not mess up with sleep function'''
    print(text, end='', flush=True)


def move(num):
    '''Move curr_line by num'''
    global curr_line
    curr_line += num


def if_upper(text):
    '''If META UNCAPS is on, make command uncap'''
    global uncaps
    if uncaps:
        return text.upper()
    return text


def resolve(text):
    '''Smartly returns vars, strings, nums, and arrays'''
    global curr_line
    global var_list
    if text[0] == '"':
        return get_string(text)
    elif text.isnumeric():
        return int(text)
    elif text[0] == '$':
        var = text[1:]
        match if_upper(var):
            case "LINE":
                return curr_line
            case "TIME":
                return time.time()
            case "EMPTY":
                return ""
            case _:
                return ""
    elif text[0] == '[':
        regex_pattern = r'\[([^]]+)\]'
        matches = re.findall(regex_pattern, text)
        return array_list[matches[0]][resolve(matches[1])]
    else:
        try:
            return var_list[text]
        except:
            try:
                return array_list[text]
            except:
                print(f"No variable or array named {text}")
                quit(1)


def split_quotes(string):
    '''Uses regex to split each command line (includes quotes)'''
    regex_pattern = r'(?:(?<=\s)|(?<=^))([^"\s]+|".*?")(?:(?=\s)|(?=$))'
    matches = re.findall(regex_pattern, string)
    if len(matches) == 0:
        return [""]
    for i in range(len(matches)):
        matches[i] = matches[i].replace(r'\"', r'"')
    return matches


def reset_content():
    '''Just resets dogears and content length'''
    global dogears
    global content
    for i in range(len(content)):
        '''Remove indentation'''
        command = content[i].split(" ")
        while True:
            if len(command) == 0:
                break
            elif command[0] == "":
                command.pop(0)
            else:
                break
        content[i] = ' '.join([str(elem) for i, elem in enumerate(command)])

    for i in range(len(content)):
        command = content[i].split(" ")
        if command[0] == "DOGEAR":
            dogears[command[1]] = i


reset_content()

while curr_line <= content_length:
    command = split_quotes(content[curr_line])
    if debug:
        '''Do some debug stuff, yknow'''
        print(f"vars:{var_list}")
        print(f"Command:{command}")
        print(f"Arrays:{array_list}")
    match if_upper(command[0]):
        case "PLACE":
            '''Set a variable'''
            value = command[1]
            var_list[command[2]] = resolve(command[1])
            move(1)

        case "REPORT":
            '''Print out'''
            sys_print(resolve(command[1]))
            move(1)

        case "SAY":
            '''Report with a newline'''
            sys_print(str(resolve(command[1])) + "\n")
            move(1)

        case "DOGEAR":
            '''
            Sets a bookmark to set the curr_line back to after a goto.
            This language does not have functions, but this is similar.
            So ditto, ig.
            '''
            dogears[command[1]] = curr_line
            move(1)

        case "GOTO":
            '''Go to dogear'''
            return_lines.append(curr_line)
            name = resolve(command[1])
            if name.isnumeric():
                curr_line = command[1]
            else:
                try:
                    curr_line = dogears[name]
                except:
                    print(f"No dogear named {command[1]}")

        case "IF":
            '''Just an IF'''
            first = resolve(command[2])
            second = resolve(command[3])

            match if_upper(command[1]):
                case "EQ":
                    if first == second:
                        move(1)
                    else:
                        move(2)

                case "GR":
                    if first > second:
                        move(1)
                    else:
                        move(2)

                case "LS":
                    if first < second:
                        move(1)
                    else:
                        move(2)

                case "NE":
                    if first != second:
                        move(1)
                    else:
                        move(2)

                case _:
                    if resolve(command[1]) == resolve(command[2]):
                        move(1)
                    else:
                        move(2)

        case "INC":
            '''Increment value by 1'''
            if str(var_list[command[1]]).isnumeric():
                var_list[command[1]] = var_list[command[1]] + 1
            move(1)

        case "DEC":
            '''Decrement by 1'''
            if str(var_list[command[1]]).isnumeric():
                var_list[command[1]] = var_list[command[1]] - 1
            move(1)

        case "ADD":
            '''Add two numbers, put into a var'''
            try:
                var_list[command[3]] = resolve(command[1]) + resolve(command[2])
            except:
                print(f"Could not add {command[1]} to {command[2]}")
                quit(1)
            move(1)

        case "SUB":
            '''Subtract two numbers, put into a var'''
            try:
                var_list[command[3]] = resolve(command[1]) - resolve(command[2])
            except:
                print(f"Could not subtract {command[2]} from {command[1]}")
                quit(1)
            move(1)

        case "MUL":
            '''Multiply two numbers, put into a var'''
            try:
                var_list[command[3]] = resolve(command[1]) * resolve(command[2])
            except:
                print(f"Could not multiply {command[2]} and {command[1]}")
                quit(1)
            move(1)

        case "DIV":
            '''Divide two numbers, put into a var'''
            try:
                var_list[command[3]] = resolve(command[1]) / resolve(command[2])
            except:
                print(f"Could not divide {command[1]} by {command[2]}")
                quit(1)
            move(1)

        case "MOD":
            '''Modulo two numbers, put into a var'''
            try:
                var_list[command[3]] = resolve(command[1]) % resolve(command[2])
            except:
                print(f"Could not modulo {command[1]} by {command[2]}")
                quit(1)
            move(1)

        case "ROUND":
            '''Round a float and put into var'''
            var_list[command[2]] = round(resolve(command[1]))
            move(1)

        case "INPUT":
            '''Takes user input and put in var'''
            var_list[command[1]] = input()
            move(1)

        case "WAIT":
            '''Just a sleep command'''
            try:
                time.sleep(resolve(command[1]))
                move(1)
            except:
                print(f"{command[1]} could not be processed as time")
                quit()

        case "INCLUDE":
            '''Import file'''
            with open(resolve(command[1]), 'r') as f:
                content = content + ["END PROGRAM"] + f.read().split("\n")
            reset_content()
            content_length = len(content) - 1
            move(1)

        case "RETURN":
            '''Return back to previous goto'''
            curr_line = return_lines[-1] + 1
            return_lines.pop(-1)

        case "READ":
            '''Read a file, put into array'''
            with open(resolve(command[1])) as f:
                array_list[command[2]] = f.read().split("\n")
            move(1)

        case "MAKE":
            '''
            Kinda odd command. Essentially just makes something
            into either another variable type or makes a new thing.
            Maybe in the future I'll make custom types
            '''
            match if_upper(command[1]):
                case "ARRAY":
                    array_list[command[2]] = []

                case "INT":
                    var_list[command[2]] = int(var_list[command[2]])

                case _:
                    var_list[command[1]] = 0
            move(1)

        case "ARRAY":
            '''Change array stuff'''
            array = command[1]
            match if_upper(command[2]):
                case "ADD":
                    array_list[array].append(resolve(command[3]))

                case "DEL":
                    array_list[array].pop(resolve(command[3]))

                case "SET":
                    array_list[array][resolve(command[4])] = resolve(command[3])

                case "LIST":
                    array_list[array] = list(str(resolve(command[3])))

                case _:
                    pass
            move(1)

        case "LEN":
            '''Get length of value, put into var'''
            try:
                var_list[command[2]] = len((resolve(command[1])))
            except:
                try:
                    var_list[command[2]] = len(str(resolve(command[1])))
                except:
                    print(f"Could not get length of {command[1]}")
                    quit(1)
            move(1)

        case "DEL":
            '''Deletes multiple arrays or vars'''
            for i in range(1, len(command)):
                if command[i][0] == "[":
                    del array_list[command[i][1:][:-1]]
                else:
                    del var_list[command[i]]
            move(1)

        case "META":
            match if_upper(command[1]):
                case "DEBUG":
                    match if_upper(command[2]):
                        case "OFF":
                            debug = False

                        case _:
                            debug = True

                case "CAPS":
                    uncaps = False

                case "UNCAPS":
                    uncaps = True

                case _:
                    pass
            move(1)

        case "END":
            '''Terminate something'''
            match if_upper(command[1]):
                case "PROGRAM":
                    quit(0)

                case "DOGEAR":
                    '''Go to next dogear'''
                    while True:
                        if content[curr_line].split(" ")[0] != "DOGEAR":
                            move(1)
                        else:
                            break

                case _:
                    quit(0)
        case _:
            move(1)

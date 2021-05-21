# Todhri Angjelo, AM:3090, username:cse53090
# Mpoulotis Panagiotis, AM:4271, username:cse74271


import sys  # needed for reading the test files
import string  # for some library uses

min_value = -(pow(2, 32) - 1)
max_value = (pow(2, 32) - 1)

letters = string.ascii_letters

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# numerical symbols
num_symbols = ['+', '-', '*', '/', '=']

# relational symbols
rel_symbols = ['>', '<', '<=', '>=', '<>']

# declaration symbol
dec_symbol = ':='

# separation symbols
sep_symbols = [';', ':']

# grouping symbols
group_symbols = ['(', ')', '[', ']', '{', '}']

# comma symbol
comma_symbol = ','

# End of File symbol
EOF_symbol = '.'

# Comment symbol
cmt_symbol = '#'

# White character symbols
white_characters = [' ', '\t', '\n']

# States for Lexical Analysis
start_state = 0
word_state = 1
digit_state = 2
lesser_than_state = 3
greater_than_state = 4
colon_state = 5
comment_state = 6
final_state = 7
EOF_state = 8

lex_states = [start_state, word_state, digit_state, lesser_than_state, greater_than_state, colon_state,
              comment_state, final_state, EOF_state]

# Lex errors

Error_non_valid_symbol = "Non-valid symbol detected"
Error_letter_after_digit = "There's an alphabetic character after a numerical digit"
Error_colon = "There isn't a = after the : symbol  "
Error_out_of_bounds = "There's an out-of-bounds number "
Error_string_length = "There's a string with more than 30 characters "
Error_comments = "The EOF has been detected while a comment is open"

# All the reserved words Cimple implements
reserved = ['program', 'declare', 'if', 'else',
            'while', 'switchcase',
            'forcase', 'incase', 'default', 'case',
            'not', 'and', 'or',
            'function', 'procedure', 'call', 'return', 'in', 'inout',
            'input', 'print']

lex_result = []  # the result list of the lex()


# ----------------------------------------------------------------------------------------------------------------------
# File handling
# ----------------------------------------------------------------------------------------------------------------------
# Check if a cimple file is not given by the command file_line
if len(sys.argv) == 1:
    print("There's not a cimple file given")
    sys.exit()

# Check if there are more than one cimple files is given by the command file_line
if len(sys.argv) > 2:
    print("There are more than one cimple files given")
    sys.exit()

# Get the Cimple file from the command file_line
file = open(sys.argv[1], 'r')

file_line = 1  # first line of the file


# ----------------------------------------------------------------------------------------------------------------------
# Lexical Analysis
# ----------------------------------------------------------------------------------------------------------------------
# This will be used for printing the correct error when something is wrong
def printError(error, line):
    print('Error: ' + error + ' at line ' + str(line))
    sys.exit()


def lex():
    global file_line
    state = start_state  # start with the state 0: start state
    file_pos = 0  # a simple counter for the position of the file
    prod_word = ''  # produced word: the word the alphabetic characters create
    prod_num = ''  # produced number : the number the numerical characters create
    # will be later converted to int value so it can be checked

    token_type = ''  # the type of the token
    token_string = ''  # the string of the token

    result = []  # the result lex returns

    while state != final_state:  # while the character is not in a final state
        file_pos = file.tell()  # save the file's current position
        char = file.read(1)  # char reads the current character from the file

        # Start state analysis
        if state == start_state:

            # detected a white character
            if char in white_characters:
                # staying in the same state
                token_type = "white character"
                state = start_state
                if char == '\n':
                    file_line += 1  # changing file_line

            # detected an alphabetic character
            elif char in letters:
                token_type = "id"
                prod_word += char
                state = word_state  # moving to state 1: creating a word

            # detected a numerical digit
            elif char in digits:
                token_type = "number"
                prod_num += char
                state = digit_state  # moving to state 2: creating a number

            # detected a numerical symbol (+,-,*,/,=)
            elif char in num_symbols:
                token_string += char
                if char == '+':
                    token_type = "plus"
                elif char == '-':
                    token_type = "minus"
                elif char == '*':
                    token_type = "multiply"
                elif char == '/':
                    token_type = "divide"
                elif char == '=':
                    token_type = "equal"
                state = final_state
                file_pos += 1

            # detected a lesser than symbol
            elif char == '<':
                state = lesser_than_state  # moving to state 3: lesser than state
                token_type = "lesser than"
                token_string += char
                file_pos += 1

            # detected a greater than symbol
            elif char == '>':
                state = greater_than_state  # moving to state 4: greater than state
                token_type = "greater than"
                token_string += char
                file_pos += 1

            # detected a colon symbol
            elif char == ':':
                state = colon_state  # moving to state 5: colon (declaration) state
                token_type = "colon"
                token_string += char
                file_pos += 1

            # detected a left bracket symbol
            elif char == '{':
                state = final_state
                token_type = "left bracket"
                token_string += char
                file_pos += 1

            # detected a right bracket symbol
            elif char == '}':
                state = final_state
                token_type = "right bracket"
                token_string += char
                file_pos += 1

            # detected a hashtag (comment) symbol
            elif char == '#':
                state = comment_state  # moving to state 7: comment state
                token_type = "hashtag1"
                token_string += char

            # detected a comma symbol
            elif char == ',':
                state = final_state
                token_type = "comma"
                token_string += char
                file_pos += 1

            # detected a greek question mark symbol
            elif char == ';':
                state = final_state
                token_type = "question mark"
                token_string += char
                file_pos += 1

            # detected a left parenthesis symbol
            elif char == '(':
                state = final_state
                token_type = "left parenthesis"
                token_string += char
                file_pos += 1

            # detected a right parenthesis symbol
            elif char == ')':
                state = final_state
                token_type = "right parenthesis"
                token_string += char
                file_pos += 1

            # detected a left block symbol
            elif char == '[':
                state = final_state
                token_type = "left block"
                token_string += char
                file_pos += 1

            # detected a right block symbol
            elif char == ']':
                state = final_state
                token_type = "right block"
                token_string += char
                file_pos += 1

            # detected a dot symbol (EOF symbol)
            elif char == '.':
                state = EOF_state  # moving to state 9: EOF state
                token_type = "EOF symbol"
                token_string += char

            # Unacceptable characters
            else:
                print(char)
                printError(Error_non_valid_symbol, file_line)

        # word state analysis
        elif state == word_state:
            if char in letters or char in digits:
                prod_word += char
            else:
                token_string += prod_word
                state = final_state

            # The produced word exceeds 30 characters, so display error
            if len(prod_word) > 30:
                printError(Error_string_length, file_line)

        # Number state analysis
        elif state == digit_state:
            if char in digits:
                prod_num += char

            # detected an alphabetic character after a numerical digit
            elif char in letters:
                printError(Error_letter_after_digit, file_line)

            else:
                # the number is created, proceed to the final state
                token_string += prod_num
                state = final_state

            # convert the string of the produced number to an integer so it
            # can be checked for errors
            number = int(prod_num)

            # The number is out of bounds
            if (number < min_value) or (number > max_value):
                printError(Error_out_of_bounds, file_line)

        # Lesser than state analysis
        elif state == lesser_than_state:
            if char == '=':
                state = final_state
                token_type = "lesser equal"
                token_string += char
                file_pos += 1
            elif char == '>':
                state = final_state
                token_type = "not equal"
                token_string += char
                file_pos += 1
            else:
                state = final_state

        # Greater than state analysis
        elif state == greater_than_state:
            if char == '=':
                state = final_state
                token_type = "greater equal"
                token_string += char
                file_pos += 1
            else:
                state = final_state

        # Colon state analysis
        elif state == colon_state:
            if char == '=':
                state = final_state
                token_type = "declaration"
                token_string += char
                file_pos += 1
            else:
                printError(Error_colon, file_line)

        # Comment state
        elif state == comment_state:
            if char == '#':
                state = start_state
                token_type = "hashtag2"
                token_string = ''
            elif char == '.':
                printError(Error_comments, file_line)
            else:
                state = comment_state

        # EOF state analysis
        elif state == EOF_state:
            # We want to detect if there are characters after the EOF symbols has been detected
            # If there are, the following warning message will be displayed
            file_pos += 1
            file.seek(file_pos)
            char = file.read(1)
            if char:
                if char not in white_characters:
                    print("Warning: There's code after the EOF symbol was detected")
            state = final_state

    # If we reached this state, then a token has been detected
    if state == final_state:
        # Set the files position here for next call of lex()
        file.seek(file_pos)

        # Check if the word produced is in the reserved words Cimple implements
    if prod_word in reserved:
        token_type = prod_word

    # Declaring the return values of the lex function
    # Position 0:The token type
    result.append(token_type)
    # Position 1:The token string
    result.append(token_string)
    return result


# ----------------------------------------------------------------------------------------------------------------------
# Functions and variables used for the intermediate code phase
# ----------------------------------------------------------------------------------------------------------------------
quad_num = 0  # the number of quads created
quad_list = []  # the list of all quads
T_value = 0  # the number of the temporary variable used in "T_<T_value>"
T_value_list = []  # a list with all T_values
program_name = ""  # the name of the program, will be needed for .c and .int files as well as the block(name) function
function_flag = False  # true if there are functions/procedures in the cimple code.
# If there are, we don't need to create a C file
function_list = []  # a list with the ids of the program's functions
procedure_list = []  # same, but for procedures
variables = []


# Returns the number of the next quad to be created
def nextquad():
    global quad_num

    # The number of total quads is increased by 1 from genquad so we just have to return it
    return quad_num


# Creates a new quad and adds it to the quad_list
def genquad(op, x, y, z):
    global quad_num, quad_list

    quad = [op, x, y, z]  # give the values of current quad to this list

    quad_list.append(quad)  # append the list created to the list of all the quads
    quad_num += 1  # a new quad has been created so +1 to the total number of quads


# Creates and returns T_<T_value>
def newtemp():
    global T_value, T_value_list, symbol_list

    temp = "T_" + str(T_value)  # temp is now "T_<T_value>" for example "T_1" or "T_2"
    T_value += 1  # a new temporary variable has been created so +1 to the total number of temporary variables
    T_value_list.append(temp)

    # Since each time a new temporaty variable is created newtemp() is called,
    # we decided to add the entity here so we can save some code space
    offset = symbol_list[-1].frame_length
    ent_list = symbol_list[-1].entity_list
    add_entity("temp_var", temp, offset, "", ent_list)
    # The framelength of the current scope is the offset of the current entity increased by 4
    symbol_list[-1].frame_length = symbol_list[-1].entity_list[-1].offset + 4

    return temp


# Creates an empty list of quads
def emptylist():
    empty = []
    return empty


# Creates a list that only contains the x value
def makelist(x):
    x_list = emptylist()  # create a new empty list
    x_list.append(x)  # pass the x value to the new list

    return x_list


# Merges two lists
def merge(list1, list2):
    merged = list1 + list2

    return merged


# Fills the z value, when needed, the "destination"
def backpatch(list_given, z):  # list is a close resemblance to list(), so we named it list_given
    global quad_list, quad_num

    for i in range(quad_num):
        if i in list_given:  # searches the list given to find the number of quad indexed
            quad_list[i][3] = z  # completes the specific quad list by adding the z value


# ----------------------------------------------------------------------------------------------------------------------
# Symbol Array variables, classes and functions
# ----------------------------------------------------------------------------------------------------------------------
symbol_list = []  # the symbol array in list form
main_state_flag = False  # this flag let us know whether we are in the main part of the program
# or in a function or procedure
procedure_state_flag = False  # likewise for procedures
return_flag = False  # we have detected a return flag while analysing a function

# This flag combined with the procedure_state_flag will be used to check if we have a return statement inside a function
# Each time we are doing a function analysis, if the procedure_state_flag is true, this means we have the declaration of
# a function inside of a procedure. Since we may have more than 1 functions declared inside a procedure, this flag is
# an integer and not boolean
temp_flag = 0

# This is a list of all the Temporary variable entities, it is used to recover them, if they were declared in a scope
# that has now been deleted
Temp_vars = []


# We are using classes, because they are the C-equivalent to structs.
# We need to store multiple strings, integers etc, and using lists would be a complicated process
# Cimple's syntax does not have the float type only integers, so we don't need to include the int type
# in the following records-classes
# Record Entity
class Variable:
    def __init__(self, name, offset):
        self.name = name
        self.entity = "variable"
        self.offset = offset


class Function:
    def __init__(self, name):
        self.name = name
        self.entity = "function"
        self.start_quad = 0
        self.argument_list = []
        self.frame_length = 12


class Procedure:
    def __init__(self, name):
        self.name = name
        self.entity = "procedure"
        self.start_quad = 0
        self.argument_list = []
        self.frame_length = 12


class Parameter:
    def __init__(self, name, parmode, offset):
        self.name = name
        self.entity = "parameter"
        self.parmode = parmode
        self.offset = offset


class TempVariable:
    def __init__(self, name, offset):
        self.name = name
        self.entity = "temp_variable"
        self.offset = offset


# Record Scope
class Scope:
    def __init__(self, nesting_level):
        self.entity_list = []
        self.nesting_level = nesting_level
        # We added an extra parameter, frame_length, so we can pass it down
        # the necessary functions
        self.frame_length = 12


# Record Argument
class Argument:
    def __init__(self, parmode):
        self.parmode = parmode


# Adding a scope to the scope list
def add_scope(nest_level):
    global symbol_list
    scope = Scope(nest_level)
    # we don't have to add the offset yet

    # Nesting level handling
    if not symbol_list:
        # The symbol list is empty so we are in nesting level 0
        scope.nesting_level = 0
    else:
        # The nesting level is increased
        scope.nesting_level = symbol_list[-1].nesting_level + 1

    symbol_list.append(scope)
    return scope


# Deletes the last scope of the symbol list
def close_scope():
    global symbol_list
    del symbol_list[-1]


# Displays the scope in the symbol_list file
def display_scope(scope):
    result = "Nesting level: " + str(scope.nesting_level) + "\n"
    result = result + "Entities: \n"
    e_list = scope.entity_list

    if len(e_list) == 0:
        # There are not any entities
        result = result + "None"

    for entity in e_list:
        # Display the entities of the scope
        result = result + str(display_entity(entity, entity.entity))
        result = result + "\n"

    result = result + "Scope's framelength: " + str(scope.frame_length)
    return result


# Adding an entity to the entity list
def add_entity(ent_type, name, offset, parmode, ent_list):
    global Temp_vars
    # Entity - Variable
    if ent_type == "variable":
        entity = Variable(name, offset)

    # Entity - Function
    elif ent_type == "function":
        entity = Function(name)

    # Entity - Procedure
    elif ent_type == "procedure":
        entity = Procedure(name)

    # Entity - Parameter
    elif ent_type == "parameter":
        entity = Parameter(name, parmode, offset)

    # Entity - Temp_variable
    elif ent_type == "temp_var":
        entity = TempVariable(name, offset)
        Temp_vars.append(entity)

    # We excluded the constant entity, as it's not being added in the entity list
    else:
        print("Incorrect type of entity")
        sys.exit()

    ent_list.append(entity)
    return entity


# Displays the entities in the symbol_list file
def display_entity(entity, ent_type):
    result = ""
    # Entity - Variable
    if ent_type == "variable":
        result = "Var: " + str(entity.name) + " / " + str(entity.offset)

    # Entity - Function
    elif ent_type == "function":
        result = "Function: " + str(entity.name) + " | Starting quad : " + str(entity.start_quad)
        # We need to display the arguments as well
        result += " | Arguments: ("
        temp = ""
        for arg in entity.argument_list:
            temp = temp + str(display_argument(arg)) + ","
        temp = temp[:-1] + ""  # delete the last ","
        result += str(temp) + ") | Frame_length: " + str(entity.frame_length)

    # Entity - Procedure
    elif ent_type == "procedure":
        # Same as before
        result = "Procedure: " + str(entity.name) + " | Starting quad : " + str(entity.start_quad)
        # We need to display the arguments as well
        result += " | Arguments: ("
        temp = ""
        for arg in entity.argument_list:
            temp = temp + str(display_argument(arg)) + ","
        temp = temp[:-1] + ""  # delete the last ","
        result += str(temp) + ") | Frame_length: " + str(entity.frame_length)

    # Entity - Parameter
    elif ent_type == "parameter":
        result = "Par: " + str(entity.name) + " / " + str(entity.parmode) + " / " + str(entity.offset)

    # Entity - Temp_variable
    elif ent_type == "temp_variable":
        result = "Temp_Var: " + str(entity.name) + " / " + str(entity.offset)

    return result


# Adding an argument to the argument list of the function
def add_argument(parmode, argument_list):
    arg = Argument(parmode)
    argument_list.append(arg)
    return arg


# Displays the arguments in the symbol_list file
def display_argument(arg):
    return str(arg.parmode)


# Search the entity with the given name
def search_entity(name):
    global symbol_list, file_line, Temp_vars

    # searching all of the symbol list
    for i in symbol_list:
        # searching for the entity in each entity_list of the symbol list
        for entity in i.entity_list:
            if entity.name == name:
                # we found the entity we were searching
                return entity

    # searching all Temporary variables, in the case of a deleted scope
    for entity in Temp_vars:
        if entity.name == name:
            return entity

    # We didn't find the entity we were searching for
    printError("Could not find an entity with " + name + " name", file_line)


# Checks if the parameters list are the same
def param_check(func_name, par_list):
    global file_line
    func_entity = search_entity(func_name)
    func_pars = []  # the parameter list of the function
    for i in func_entity.argument_list:
        # We have the function's argument list that is provided by formalparlist
        func_pars.append(i.parmode)  # Adding each argument to the list

    if func_entity.entity == "function":
        # We need to check their length
        if len(func_pars) < len(par_list):
            printError("The function '" + func_name + "' requires less arguments ", file_line)

        elif len(func_pars) > len(par_list):
            printError("The function '" + func_name + "' requires more arguments ", file_line)

        else:
            # We need to check if the parameters of the function are the same format as the ones of the list given
            if func_pars != par_list:
                printError("Invalid format of arguments for '" + func_name + "' function", file_line)

    # Same but for procedures
    elif func_entity.entity == "procedure":
        # We need to check their length
        if len(func_pars) < len(par_list):
            printError("The procedure '" + func_name + "' requires less arguments ", file_line)

        elif len(func_pars) > len(par_list):
            printError("The procedure '" + func_name + "' requires more arguments ", file_line)

        else:
            # We need to check if the parameters of the function are the same format as the ones of the list given
            if func_pars != par_list:
                printError("Invalid format of arguments for the '" + func_name + "' procedure", file_line)

    else:
        printError(func_name + "is an invalid name for procedures/functions", file_line)


# ----------------------------------------------------------------------------------------------------------------------
# Functions and variables used for the conversion of the intermediate to the final code
# ----------------------------------------------------------------------------------------------------------------------
i_num = 0  # the number of parameters used, this will be multiplied by 4 each time


# Searches for the nesting level of the entity
def search_level(entity):
    global symbol_list
    level = 0

    # We need to find the nesting level of the variable
    for i in symbol_list:
        if entity in i.entity_list:
            level = i.nesting_level

    return level


# Moves the $t0 register to the address of the var
def gnvlcode(var):
    global mips_file, symbol_list
    current_level = symbol_list[-1].nesting_level

    entity = search_entity(var)
    var_level = search_level(entity)  # the nesting level of the variable

    # Now we will compute the difference with the current nesting level
    diff_level = current_level - var_level

    mips_file.write("\t" + "lw $t0, -4($sp) \n")  # stack of the parent

    # Loop till we get to the same nesting level
    for i in range(diff_level - 1):
        mips_file.write("\t" + "lw $t0, -4($t0) \n")

    mips_file.write("\t" + "addi $t0, $t0, -" + str(entity.offset) + "\n")


# Loads data from memory to v
def loadvr(v, r):
    global mips_file, symbol_list

    current_level = symbol_list[-1].nesting_level
    negative_flag = False  # will be set to true if we have a negative
    level = -1  # the nesting level of the v
    e_type = ""  # the entity type of the v
    offset = -1  # v's offset
    entity = None

    if "-" in v:
        # The variable v is a negative, but we don't want the '-' symbol for our analysis
        v = v[1:]
        negative_flag = True

    # Checking if the v is a variable and not a number
    if not v.isdigit():
        entity = search_entity(v)
        e_type = entity.entity
        # if we are calling a function
        if e_type == "function":
            offset = entity.frame_length
        else:
            offset = entity.offset

        level = search_level(entity)

    # v number check
    if v.isdigit():
        if negative_flag:
            mips_file.write("\t" + "li " + r + ", -" + str(v) + "\n")
        else:
            mips_file.write("\t" + "li " + r + ", " + str(v) + "\n")

    # v is a global variable, which means its level is 0 because that is the main part
    elif level == 0:
        mips_file.write("\t" + "lw " + r + ", -" + str(offset) + "($s0) \n")

    # v is in the same nesting level as the current function
    elif level == current_level:
        # v is a variable
        if e_type == "variable" or e_type == "temp_variable":
            mips_file.write("\t" + "lw " + r + ", -" + str(offset) + "($sp) \n")
        elif e_type == "parameter" and entity.parmode == "in":
            # Same as before
            mips_file.write("\t" + "lw " + r + ", -" + str(offset) + "($sp) \n")
        elif e_type == "parameter" and entity.parmode == "inout":
            mips_file.write("\t" + "lw t0, -" + str(offset) + "($sp) \n")
            mips_file.write("\t" + "lw " + r + ", ($t0) \n")

    # v is an earlier level
    elif current_level > level:
        gnvlcode(v)
        if e_type == "variable" or e_type == "temp_variable":
            mips_file.write("\t" + "lw " + r + ", ($t0) \n")
        elif e_type == "parameter" and entity.parmode == "in":
            mips_file.write("\t" + "lw " + r + ", ($t0) \n")
        elif e_type == "parameter" and entity.parmode == "inout":
            mips_file.write("\t" + "lw t0 , ($t0) \n")
            mips_file.write("\t" + "lw " + r + ", ($t0) \n")
    else:
        print("loadvr error with " + v)
        sys.exit()

    return


# Stores data from v to memory
def storerv(r, v):
    # This one will be similar to the loadvr but with no case for v being a number
    global mips_file, symbol_list
    current_level = symbol_list[-1].nesting_level
    # Same as before
    entity = search_entity(v)
    e_type = entity.entity
    offset = entity.offset

    level = search_level(entity)

    # v global variable
    if level == 0:
        mips_file.write("\t" + "sw " + r + ", -" + str(offset) + "($s0) \n")

    # v is in the same nesting level as the current function
    elif level == current_level:
        # v is a variable
        if e_type == "variable" or e_type == "temp_variable":
            mips_file.write("\t" + "sw " + r + ", -" + str(offset) + "($sp) \n")
        elif e_type == "parameter" and entity.parmode == "in":
            # Same as before
            mips_file.write("\t" + "sw " + r + ", -" + str(offset) + "($sp) \n")
        elif e_type == "parameter" and entity.parmode == "inout":
            mips_file.write("\t" + "lw t0, -" + str(offset) + "($sp) \n")
            mips_file.write("\t" + "sw " + r + ", ($t0) \n")

    # v is an earlier level
    elif current_level > level:
        gnvlcode(v)
        if e_type == "variable" or e_type == "temp_variable":
            mips_file.write("\t" + "sw " + r + ", ($t0) \n")
        elif e_type == "parameter" and entity.parmode == "in":
            mips_file.write("\t" + "sw " + r + ", ($t0) \n")
        elif e_type == "parameter" and entity.parmode == "inout":
            mips_file.write("\t" + "lw t0 , ($t0) \n")
            mips_file.write("\t" + "sw " + r + ", ($t0) \n")
    else:
        print("storerv error with " + v)
        sys.exit()

    return


# ----------------------------------------------------------------------------------------------------------------------
# C file handling
# ----------------------------------------------------------------------------------------------------------------------
def c_file_create():
    global program_name, quad_list, quad_num, T_value_list, T_value, variables

    variable_string = ""  # will be used for printing the variables
    relops = ["=", ">", "<", "<>", ">=", "<="]   # all the =,>,<,<>,>=,<= symbols
    temp_string = ""  # will be used for printing the temporary variables

    # Converting the variables list to a string 
    for i in range(len(variables)):
        variable_string += str(variables[i]) + ","  

    variable_string = variable_string[:-1] + ";"  # replace the last "," with ";"

    for i in range(T_value):
        temp_string += str(T_value_list[i]) + ","

    temp_string = temp_string[:-1] + ";"  # replace the last "," with ";"

    variable_string = variable_string[:-1] + ";"  # replace the last "," with ";"
    c_file = open(program_name + '.c', 'w')  # creates the .c file
    c_file.write("#include <stdio.h> \t// for the printf and scanf functions \n")  # will be need for the functions used
    c_file.write("\n \n")
    c_file.write("int main() \n" + "{\n")

    if len(variables) != 0:
        c_file.write("\t" + "int " + variable_string + "\n")  # writes all the variables declared

    if len(T_value_list) != 0:
        c_file.write("\t" + "int " + temp_string + "\n \n")  # writes all the variables declared

    for i in range(quad_num):
        # declaration statement
        if quad_list[i][0] == ":=":
            c_file.write("\t" + "L_" + str(i) + ": " + str(quad_list[i][3]) + " = " + str(quad_list[i][1]) + ";")
            c_file.write(" //(" + str(quad_list[i]) + ")" + "\n")

        # numerical operation statements
        elif (quad_list[i][0] == "+") or (quad_list[i][0] == "-") or (quad_list[i][0] == "*") or (quad_list[i][0] == "/"):
            c_file.write("\t" + "L_" + str(i) + ": " + str(quad_list[i][3]) + " = " + str(quad_list[i][1]) + " " + str(quad_list[i][0]) + " " + str(quad_list[i][2]) + ";")
            c_file.write(" //(" + str(quad_list[i]) + ")" + "\n")

        # if statements
        elif quad_list[i][0] in relops:

            if quad_list[i][0] == "=":  # equal in c is ==
                relop_id = "=="
            elif quad_list[i][0] == "<>":  # not equal in c is !=
                relop_id = "!="
            else:
                relop_id = str(quad_list[i][0])
            c_file.write("\t" + "L_" + str(i) + ": " + "if (" + str(quad_list[i][1]) + " " + relop_id + " " + str(quad_list[i][2]) + ") goto L_" + str(quad_list[i][3]) + ";")
            c_file.write(" //(" + str(quad_list[i]) + ")" + "\n")

        # jump statement
        elif quad_list[i][0] == "jump":
            c_file.write("\t" + "L_" + str(i) + ": " + "goto L_" + str(quad_list[i][3]) + ";")
            c_file.write(" //(" + str(quad_list[i]) + ")" + "\n")

        # end of program
        elif quad_list[i][0] == "halt":
            c_file.write("\t" + "L_" + str(i) + ": " + "return 0;")
            c_file.write(" //(" + str(quad_list[i]) + ")" + "\n")

        # return statement
        elif quad_list[i][0] == "retv":
            c_file.write("\t" + "L_" + str(i) + ": " + "return " + str(quad_list[i][1]) + ";")
            c_file.write(" //(" + str(quad_list[i]) + ")" + "\n")

        # input - scanf statement
        elif quad_list[i][0] == "inp":
            c_file.write("\t" + "L_" + str(i) + ": " + 'scanf("%d",&' + str(quad_list[i][1]) + ");")
            c_file.write(" //(" + str(quad_list[i]) + ")" + "\n")

        # output - printf statement
        elif quad_list[i][0] == "out":
            c_file.write("\t" + "L_" + str(i) + ": " + 'printf("%d",' + str(quad_list[i][1]) + ");")
            c_file.write(" //(" + str(quad_list[i]) + ")" + "\n")

        else:
            c_file.write("\t" + "//(" + str(quad_list[i]) + ")" + "\n")

    c_file.write("}")
    c_file.close()  # the file is completed


# ----------------------------------------------------------------------------------------------------------------------
# int file handling
# ----------------------------------------------------------------------------------------------------------------------
def int_file_create():
    global program_name, quad_list, quad_num

    int_file = open(program_name + '.int', 'w')  # creates the .int file

    for i in range(quad_num):
        int_file.write(str(i) + ": " + str(quad_list[i][0]) + " " + str(quad_list[i][1]) + " " + str(quad_list[i][2]) + " " + str(quad_list[i][3]) + "\n")

    int_file.close()  # the file is completed


# ----------------------------------------------------------------------------------------------------------------------
# txt file handling (for symbol array)
# ----------------------------------------------------------------------------------------------------------------------
def display_symbol_list():
    global symbol_list

    for scope in symbol_list:
        txt_file.write(display_scope(scope) + "\n\n")


# ----------------------------------------------------------------------------------------------------------------------
# asm file handling (final code)
# ----------------------------------------------------------------------------------------------------------------------
# In a way, this may resemble the .c code
def asm_file_create(start_quad, name):
    global mips_file, quad_list, program_name, i_num

    quad = quad_list[start_quad - 1]
    relop_list = ["=", ">", "<", "<>", ">=", "<="]   # all the =,>,<,<>,>=,<= symbols
    op_list = ["+", "-", "*", "/"]  # all the arithmetic operations symbols
    current_level = symbol_list[-1].nesting_level
    func_framelength = 0  # the framelength of the function/ procedure, if it exists
    func_level = -1

    # Find which function/procedure the name responds to if we are not in the main part of the program
    if name != program_name:
        func = search_entity(name)
        func_framelength = func.frame_length
        func_level = search_level(func)

    # Start of the function/procedure or main part
    if quad[0] == "begin_block":
        if name == program_name:
            mips_file.write("Lmain: \n")
            # the nesting level of the main part is 0, so its framelength is in the scope 0
            mips_file.write("\t" + "add  $sp, $sp, " + str(symbol_list[0].frame_length) + "\n")
            mips_file.write("\t" + "move  $s0, $sp \n")

        else:
            # Handling a function or procedure
            mips_file.write("L" + str(start_quad - 1) + ":\n")
            mips_file.write("\t" + "sw  $ra, ($sp) \n")

    # Jump to label
    elif quad[0] == "jump":
        mips_file.write("L" + str(start_quad - 1) + ":\n")
        mips_file.write("\t" + "j L" + str(quad[3]) + "\n")

    # Relational Operations
    elif quad[0] in relop_list:
        mips_file.write("L" + str(start_quad - 1) + ":\n")
        loadvr(quad[1], "$t1")
        loadvr(quad[2], "$t2")
        # Equal
        if quad[0] == "=":
            mips_file.write("\t" + "beq $t1, $t2, L" + str(quad[3]) + "\n")
        # Lesser than
        elif quad[0] == "<":
            mips_file.write("\t" + "blt $t1, $t2, L" + str(quad[3]) + "\n")
        # Greater than
        elif quad[0] == ">":
            mips_file.write("\t" + "bgt $t1, $t2, L" + str(quad[3]) + "\n")
        # Lesser equal
        elif quad[0] == "<=":
            mips_file.write("\t" + "ble $t1, $t2, L" + str(quad[3]) + "\n")
        # Greater equal
        elif quad[0] == ">=":
            mips_file.write("\t" + "bge $t1, $t2, L" + str(quad[3]) + "\n")
        # Not Equal
        elif quad[0] == "<>":
            mips_file.write("\t" + "bne $t1, $t2, L" + str(quad[3]) + "\n")

    # Declaration
    elif quad[0] == ":=":
        mips_file.write("L" + str(start_quad - 1) + ":\n")
        loadvr(quad[1], "$t1")
        storerv("$t1", quad[3])

    # Arithmetic Operations
    elif quad[0] in op_list:
        mips_file.write("L" + str(start_quad - 1) + ":\n")
        loadvr(quad[1], "$t1")
        loadvr(quad[2], "$t2")
        # Addition
        if quad[0] == "+":
            mips_file.write("\t" + "add $t1, $t1, $t2 \n")
        # Subtraction
        elif quad[0] == "-":
            mips_file.write("\t" + "sub $t1, $t1, $t2 \n")
        # Multiplication
        elif quad[0] == "*":
            mips_file.write("\t" + "mul $t1, $t1, $t2 \n")
        # Division
        elif quad[0] == "/":
            mips_file.write("\t" + "div $t1, $t1, $t2 \n")
        storerv("$t1", quad[3])

    # Output
    elif quad[0] == "out":
        mips_file.write("L" + str(start_quad - 1) + ":\n")
        mips_file.write("\t" + "li  $v0, 1 \n")
        loadvr(quad[1], "$a0")
        mips_file.write("\t" + "syscall\n")

    # Input
    elif quad[0] == "inp":
        mips_file.write("L" + str(start_quad - 1) + ":\n")
        mips_file.write("\t" + "li  $v0, 5 \n")
        mips_file.write("\t" + "syscall \n")
        storerv("$v0", quad[1])

    # Return
    elif quad[0] == "retv":
        mips_file.write("L" + str(start_quad - 1) + ":\n")
        loadvr(quad[1], "$t1")
        mips_file.write("\t" + "lw  $t0, -8($sp) \n")
        mips_file.write("\t" + "sw  $t1, ($t0) \n")

    # Parameter handling
    elif quad[0] == "par":
        mips_file.write("L" + str(start_quad - 1) + ":\n")

        # We need to find out the level,type and offset of the quad[1]
        v_entity = search_entity(quad[1])
        v_level = search_level(v_entity)  # the nesting level
        v_type = v_entity.entity  # the type
        v_offset = v_entity.offset  # the offset

        # First we will check if we are compiling the first parameter
        if i_num == 0:
            mips_file.write("\t" + "addi $fp, $sp " + str(func_framelength) + "\n")

            i_num = i_num + 1  # added a parameter

        # Now we need to check each case
        # CV case
        if quad[2] == "CV":
            loadvr(quad[1], "$t0")
            mips_file.write("\t" + "sw $t0, -" + str(12 + 4 * i_num) + "($fp) \n")

            i_num = i_num + 1  # added a parameter

        # REF case
        elif quad[2] == "REF":
            # quad[1] is in the same nesting level as the current function
            if v_level == current_level:
                if v_type == "variable" or v_type == "temp_variable":
                    mips_file.write("\t" + "addi $t0, $sp, -" + str(v_offset) + "\n")

                elif v_type == "parameter" and v_entity.parmode == "in":
                    mips_file.write("\t" + "addi $t0, $sp, -" + str(v_offset) + "\n")

                elif v_type == "parameter" and v_entity.parmode == "inout":
                    mips_file.write("\t" + "lw $t0, -" + str(v_offset) + "\n")

            # quad[1] is in a different nesting level as the current function
            else:
                if v_type == "variable" or v_type == "temp_variable":
                    gnvlcode(quad[1])

                elif v_type == "parameter" and v_entity.parmode == "in":
                    gnvlcode(quad[1])

                elif v_type == "parameter" and v_entity.parmode == "inout":
                    mips_file.write("\t" + "lw $t0, ($t0) \n")

            # This is needed for all REF cases
            mips_file.write("\t" + "sw $t0, -" + str(12 + 4 * i_num) + "($fp) \n")
            i_num = i_num + 1  # added a parameter

        # RET case
        elif quad[2] == "RET":
            mips_file.write("\t" + "addi $t0, $sp, -" + str(v_offset) + "\n")
            mips_file.write("\t" + "sw $t0, -8 ($fp) \n")
            i_num = i_num + 1  # added a parameter

    # Call handling
    elif quad[0] == "call":
        mips_file.write("L" + str(start_quad - 1) + ":\n")

        # Like the parameter handling
        # We need to find out the level, framelength and start_quad of the quad[1]
        # Important note, func is the one that calls quad[1], so f_entity is either
        # the child of func, or a sibling

        f_entity = search_entity(quad[1])
        f_level = search_level(f_entity)  # the nesting level
        f_framelength = f_entity.frame_length  # the framelength
        f_start_quad = f_entity.start_quad  # this will be used for calling it

        # Both functions have same nesting level
        # The have the same parent
        if func_level == f_level:
            mips_file.write("\t" + "lw  $t0, -4($sp) \n")
            mips_file.write("\t" + "sw  $t0, -4($sp) \n")

        else:
            # The func entity, calls the function/procedure f_entity
            mips_file.write("\t" + "sw  $sp, -4($sp) \n")

        # For both cases
        mips_file.write("\t" + "addi  $sp, $sp, " + str(f_framelength) + "\n")
        mips_file.write("\t" + "jal L" + str(f_start_quad) + "\n")
        mips_file.write("\t" + "addi  $sp, $sp, -" + str(f_framelength) + "\n")

    # Ending of the function, we return
    elif quad[0] == "end_block" and name != program_name:
        mips_file.write("L" + str(start_quad - 1) + ":\n")
        mips_file.write("\t" + "lw  $ra, ($sp) \n")
        mips_file.write("\t" + "jr  $ra \n")

    # Halt
    elif quad[0] == "halt":
        mips_file.write("L" + str(start_quad - 1) + ":\n")
        mips_file.write("\t" + "li $v0, 10 \n")
        mips_file.write("\t" + "syscall \n")


# ----------------------------------------------------------------------------------------------------------------------
# Syntax Analysis
# Guided by Cimple's grammar
# ----------------------------------------------------------------------------------------------------------------------
def syntax():
    global lex_result, function_flag, symbol_list
    global txt_file, mips_file

    # Creating first scope, scope 0
    add_scope(0)  # nesting level 0 and an empty entity list

    lex_result = lex()  # the result of the lex() is stored here and will be used for the analysis

    # Execute the program analysis
    program()

    print("Syntax Analysis completed successfully")

    int_file_create()

    if function_flag is False:  # if we don't have any functions or procedures we can create the C file
        c_file_create()

    txt_file.close()
    mips_file.close()
    return


# "program" is the starting symbol
def program():
    global lex_result, file_line, program_name  # the file line will be used for the error messages
    global txt_file, mips_file

    if lex_result[0] == 'program':
        # program token detected
        lex_result = lex()  # search for next token

        if lex_result[0] == 'id':

            program_name = lex_result[1]  # save the program's name
            lex_result = lex()  # search for next token

            txt_file = open(program_name + '.txt', 'w')  # creates the .txt file
            mips_file = open(program_name + '.asm', 'w')  # creates the .asm file
            mips_file.write("\t" + "j Lmain \n\n")
            block(program_name)

            if lex_result[0] == 'EOF symbol':
                # End of file reached
               
                return

            else:
                printError("The EOF symbol was not detected", file_line)

        else:
            printError("Program name is not given", file_line)
    else:
        printError("No 'program' key word detected at the start of the program ", file_line)


# a block with declarations , subprogram and statement
def block(name):
    global program_name, main_state_flag, quad_list, txt_file
    start_quad = 0  # this will be used for each function or the main part
    # check if there are declarations
    declarations()
    # check if there are subprograms
    subprograms()
    genquad("begin_block", name, "_", "_")

    if name != program_name:
        # Search for the specific function and save it to func
        func = search_entity(name)
        # The next_quad is the starting one for the function
        func.start_quad = nextquad()
        start_quad = func.start_quad
        # check if there are statements
        statements()
        genquad("end_block", name, "_", "_")
        # framelength handling
        func.frame_length = symbol_list[-1].frame_length + 4

        # Handling of the final code
        while quad_list[start_quad][0] != "end_block":
            asm_file_create(start_quad, name)
            start_quad = start_quad + 1  # increase it by 1 for the rest quads
        asm_file_create(start_quad, name)  # another one for the end_block quad

    elif name == program_name:
        start_quad = nextquad()
        # we are in the main part of the program
        main_state_flag = True
        # check if there are statements
        statements()
        genquad("halt", "_", "_", "_")
        genquad("end_block", program_name, "_", "_")

    display_symbol_list()

    if name != program_name:
        close_scope()  # we are done with the analysis of the functions so close its scope
        txt_file.write("--------------------------------------------------------------------------------------------\n")
        txt_file.write("Modified Symbol Array: \n\n")
    else:
        # Handling of the final code
        while quad_list[start_quad][0] != "end_block":
            asm_file_create(start_quad, name)
            start_quad = start_quad + 1  # increase it by 1 for the rest quads
        asm_file_create(start_quad, name)  # another one for the end_block quad


# declaration of variables , zero or more " declare " allowed
def declarations():
    global lex_result, file_line

    while lex_result[0] == 'declare':
        # declare token detected
        lex_result = lex()  # search for next token

        # check the varlist() if there are one or more words
        varlist()

        if lex_result[0] == 'question mark':
            lex_result = lex()  # search for next token

        else:
            printError("Declarations: ';' character was not detected", file_line)
    return


# a list of variables following the declaration keyword
def varlist():
    global lex_result, file_line, variables, symbol_list

    if lex_result[0] == 'id':
        # detected a variable name
        name = lex_result[1]

        # We need to check if there are duplicates
        if name not in variables:
            variables.append(name)
        else:
            printError("We have found a duplicate" + name, file_line)

        # Symbol Array - variable add
        offset = symbol_list[-1].frame_length
        ent_list = symbol_list[-1].entity_list
        add_entity("variable", name, offset, "", ent_list)

        # The framelength of the current scope is the offset of the current entity increased by 4
        symbol_list[-1].frame_length = symbol_list[-1].entity_list[-1].offset + 4

        lex_result = lex()  # search for next token
        while lex_result[0] == 'comma':
            # detected ',' symbol so there may be another or more variables
            lex_result = lex()  # search for next token

            if lex_result[0] == 'id':
                name = lex_result[1]

                # Same as before
                if name not in variables:
                    variables.append(name)
                else:
                    printError("We have found a duplicate" + name, file_line)

                offset = symbol_list[-1].frame_length
                ent_list = symbol_list[-1].entity_list
                add_entity("variable", name, offset, "", ent_list)

                # The framelength of the current scope is the offset of the current entity increased by 4
                symbol_list[-1].frame_length = symbol_list[-1].entity_list[-1].offset + 4

                lex_result = lex()  # search for next token

            else:
                printError("Varlist: There's not a variable after the ',' symbol ", file_line)

    return 


# zero or more subprograms allowed
def subprograms():
    global lex_result, function_flag

    while (lex_result[0] == 'procedure') or (lex_result[0] == 'function'):
        # detected a 'procedure' or 'function' keyword  proceed to subprogram analysis
        function_flag = True  # we don't need to create a C file
        subprogram()

    return


# a subprogram is a function or a procedure, followed by parameters and block
def subprogram():
    global lex_result, file_line, function_list, procedure_list, symbol_list
    global procedure_state_flag, temp_flag, return_flag

    # Procedure's analysis
    if lex_result[0] == 'procedure':
        # procedure token detected
        lex_result = lex()  # search for next token
        procedure_state_flag = True  # we are going to need it for later use

        if lex_result[0] == 'id':
            # procedure's name is given
            name = lex_result[1]  # save the name of the procedure
            lex_result = lex()  # search for next token

            ent_list = symbol_list[-1].entity_list

            # We need to check the entity list to find if we have a variable/function with the
            # same name in the same nesting level
            # Since the ent_list contains all the entities of the current nesting level, if there
            # is another entity with the same name, but in different nesting_level, this will
            # not affect us

            if name not in ent_list:
                procedure_list.append(name)
            else:
                printError("We found duplicate" + name + " as a procedure", file_line)

            # Symbol Array - function add
            add_entity("procedure", name, "", "", ent_list)

            if lex_result[0] == 'left parenthesis':
                lex_result = lex()  # search for next token

                # We are now compiling the procedure so we need to add +1 the nesting level
                nest_level = symbol_list[-1].nesting_level  # save the current nesting level
                add_scope(nest_level)  # creates the new scope for the function analysis

                formalparlist(name)  # inside parenthesis parameters analysis

                if lex_result[0] == 'right parenthesis':

                    lex_result = lex()  # search for next token  # search for next token

                    block(name)  # go back to block() to check the other functions
                    genquad("end_block", name, "_", "_")

                    # We are done with the procedure's analysis
                    procedure_state_flag = False

                    return
                else:
                    printError("Procedure: Right parenthesis not detected", file_line)
            else:
                printError("Procedure: Left parenthesis not detected", file_line)
        else:
            printError("Procedure's name was not detected ", file_line)

    # Function's analysis
    elif lex_result[0] == 'function':
        # function token detected
        lex_result = lex()  # search for next token

        if procedure_state_flag:
            # The function is declared inside of a procedure
            temp_flag = temp_flag + 1
            # We need to set it to false so we can avoid the possible error for the return statement
            procedure_state_flag = False

        if lex_result[0] == 'id':
            # function's name is given
            name = lex_result[1]  # save the name of the function
            lex_result = lex()  # search for next token

            ent_list = symbol_list[-1].entity_list

            # We need to check for duplicates, same as before
            if name not in ent_list:
                function_list.append(name)
            else:
                printError("We found duplicate" + name + " as a function", file_line)

            # Symbol Array - function add
            add_entity("function", name, "", "", ent_list)

            if lex_result[0] == 'left parenthesis':
                lex_result = lex()  # search for next token

                # We are now compiling the function so we need to add +1 the nesting level
                nest_level = symbol_list[-1].nesting_level  # saves the current nesting level
                add_scope(nest_level)  # creates the new scope for the function analysis

                formalparlist(name)  # inside parenthesis parameters analysis

                if lex_result[0] == 'right parenthesis':
                    lex_result = lex()  # search for next token

                    block(name)  # go back to block() to check the other functions

                    if not return_flag:
                        print("Return statement has not been found inside the function" + "'" + name + "'")
                        sys.exit()
                    else:
                        # We are setting it to False so the next function ( if there is one ) can be checked
                        return_flag = False

                    if temp_flag > 0:
                        # We are decreasing the number of functions declared inside the procedure
                        temp_flag = temp_flag - 1
                        if temp_flag == 0:
                            # Now that the function's analysis is finished, we return to the procedure's analysis
                            procedure_state_flag = True

                    return

                else:
                    printError("Function: Right parenthesis not detected", file_line)
            else:
                printError("Function: Left parenthesis not detected", file_line)
        else:
            printError("Function's name was not detected ", file_line)


# list of formal parameters
def formalparlist(func_name):
    global lex_result

    formalparitem(func_name)

    while lex_result[0] == 'comma':
        lex_result = lex()  # search for next token

        formalparitem(func_name)

    return


# a formal parameter (" in ": by value , " inout " by reference )
def formalparitem(func_name):
    global lex_result, file_line, symbol_list, function_list, procedure_list

    # We need to check if we have functions/procedures with the 'func_name' name
    if func_name not in function_list and func_name not in procedure_list:
        printError("The function/procedure with name '" + func_name + "' isn't declared", file_line)

    # Now we need to search for the entity - function/procedure in order to update their argument_list
    entity = search_entity(func_name)
    arg_list = entity.argument_list

    if lex_result[0] == 'in':
        # in token detected
        par = lex_result[0]

        argument = add_argument(par, arg_list)  # added the argument created

        lex_result = lex()  # search for next token

        if lex_result[0] == 'id':

            # Symbol Array - parameter add
            offset = symbol_list[-1].frame_length
            ent_list = symbol_list[-1].entity_list
            name = lex_result[1]
            add_entity("parameter", name, offset, argument.parmode, ent_list)
            # The framelength of the current scope is the offset of the current entity increased by 4
            symbol_list[-1].frame_length = symbol_list[-1].entity_list[-1].offset + 4

            lex_result = lex()  # search for next token

            return
        else:
            printError("Formalparitem: A value name was expected after 'in' statement ", file_line)

    elif lex_result[0] == 'inout':
        # inout token detected
        par = lex_result[0]

        argument = add_argument(par, arg_list)  # added the argument created

        lex_result = lex()  # search for next token

        if lex_result[0] == 'id':
            # Symbol Array - parameter add
            offset = symbol_list[-1].frame_length
            ent_list = symbol_list[-1].entity_list
            name = lex_result[1]
            add_entity("parameter", name, offset, argument.parmode, ent_list)
            # The framelength of the current scope is the offset of the current entity increased by 4
            symbol_list[-1].frame_length = symbol_list[-1].entity_list[-1].offset + 4

            lex_result = lex()  # search for next token

            return
        else:
            printError("Formalparitem: A value name was expected after 'inout' statement ", file_line)


# one or more statements
def statements():
    global lex_result, file_line

    if lex_result[0] == 'left bracket':
        lex_result = lex()  # search for next token
        statement()

        while lex_result[0] == 'question mark':
            lex_result = lex()  # search for next token

            statement()

        if lex_result[0] == 'right bracket':
            lex_result = lex()  # search for next token
            return

        else:
            printError("Statements: Right bracket wasn't detected", file_line)

    else:

        statement()

        if lex_result[0] == 'question mark':
            lex_result = lex()  # search for next token

            return
        else:
            printError("Statements: ';' character wasn't detected after statement", file_line)


# one statement
def statement():
    global lex_result

    if lex_result[0] == 'id':
        assignment_stat()

    elif lex_result[0] == 'if':
        # if token detected
        if_stat()

    elif lex_result[0] == 'while':
        # while token detected
        while_stat()

    elif lex_result[0] == 'switchcase':
        # switchcase token detected
        switchcase_stat()

    elif lex_result[0] == 'forcase':
        # forcase token detected
        forcase_stat()

    elif lex_result[0] == 'incase':
        # incase token detected
        incase_stat()

    elif lex_result[0] == 'call':
        # call token detected
        call_stat()

    elif lex_result[0] == 'return':
        # return token detected
        return_stat()

    elif lex_result[0] == 'input':
        # input token detected
        input_stat()

    elif lex_result[0] == 'print':
        # print token detected
        print_stat()

    elif lex_result[0] == "function" or lex_result[0] == "procedure":
        # a function or a procedure detected
        subprogram()

    return


# assignment statement
def assignment_stat():
    global lex_result, file_line, variables

    # S -> id := E {P1}
    if lex_result[0] == 'id':
        id_place = lex_result[1]

        # we need to check if the id responds to a declared variable
        if id_place not in variables:
            printError("'" + id_place + "' variable has not been declared", file_line)

        lex_result = lex()  # search for next token

        if lex_result[0] == 'declaration':
            lex_result = lex()  # search for next token

            E_place = expression()  # E

            genquad(":=", E_place, "_", id_place)  # {P1}

            return
        else:
            printError("Declaration symbol was not detected after assignment's name", file_line)
    else:
        printError("Assignment's name was not detected", file_line)


# if statement
def if_stat():
    global lex_result, file_line

    if lex_result[0] == 'if':
        # if token detected
        lex_result = lex()  # search for next token

        if lex_result[0] == 'left parenthesis':
            lex_result = lex()  # search for next token

            # S -> if B then {P1} S1 {P2} TAIL {P3}
            B_list = condition()  # B_list[0] = B.true and B_list[1] = B.false

            if lex_result[0] == 'right parenthesis':
                lex_result = lex()  # search for next token
                # {P1}
                backpatch(B_list[0], nextquad())

                statements()  # S1

                # {P2}
                ifList = makelist(nextquad())
                genquad("jump", "_", "_", "_")
                backpatch(B_list[1], nextquad())

                elsepart()  # TAIL
                # {P3}
                backpatch(ifList, nextquad())

                return

            else:
                printError("Right parenthesis was not detected after 'IF' statement", file_line)
        else:
            printError("Left parenthesis was not detected before 'IF' statement", file_line)
    else:
        printError("'IF' statement was not detected", file_line)


# else statement
def elsepart():
    global lex_result

    # TAIL -> else S2| TAIL -> e
    if lex_result[0] == 'else':
        # else token detected
        lex_result = lex()  # search for next token

        statements()  # S2

    return


# while statement
def while_stat():
    global lex_result, file_line

    # S -> while {P1} B do {P2} S1 {P3}
    if lex_result[0] == 'while':
        lex_result = lex()  # search for next token
        # {P1}
        B_quad = nextquad()

        if lex_result[0] == 'left parenthesis':
            lex_result = lex()  # search for next token

            B_list = condition()  # B_list[0] = B.true and B_list[1] = B.false

            if lex_result[0] == 'right parenthesis':
                lex_result = lex()  # search for next token
                # {P2}
                backpatch(B_list[0], nextquad())

                statements()  # S1
                # {P3}
                genquad("jump", "_", "_", B_quad)
                backpatch(B_list[1], nextquad())

                return
            else:
                printError("Right parenthesis was not detected after 'while' statement", file_line)
        else:
            printError("Left parenthesis was not detected before 'while' statement", file_line)
    else:
        printError("'while' statement was not detected", file_line)


# switch statement
def switchcase_stat():
    global lex_result, file_line

    # S -> switch {P1}
    #   ((cond): {P2} S1 break {P3})*
    #   default: S2 {P4}

    if lex_result[0] == 'switchcase':
        # switchcase token detected
        lex_result = lex()  # search for next token
        # {P1}:
        exitlist = emptylist()

        while lex_result[0] == 'case':
            # case token detected
            lex_result = lex()  # search for next token

            if lex_result[0] == 'left parenthesis':
                lex_result = lex()  # search for next token

                cond_list = condition()  # cond_list[0] = cond.true and cond_list[1] = cond.false

                if lex_result[0] == 'right parenthesis':
                    lex_result = lex()  # search for next token

                    # {P2}:
                    backpatch(cond_list[0], nextquad())
                    statements()

                    # {P3}:
                    e = makelist(nextquad())
                    genquad("jump", "_", "_", "_")
                    exitlist = merge(exitlist, e)
                    backpatch(cond_list[1], nextquad())

                else:
                    printError("Right parenthesis was not detected after 'switchcase' statement", file_line)

            else:
                printError("Left parenthesis was not detected before 'switchcase' statement", file_line)

        if lex_result[0] == 'default':
            # default token detected
            lex_result = lex()  # search for next token

            statements()

            # {P4}:
            backpatch(exitlist, nextquad())

            return
        else:
            printError("'default' statement was not detected after 'switchcase' statement ", file_line)
    else:
        printError("'switchcase' statement was not detected", file_line)


# forcase statement
def forcase_stat():
    global lex_result, file_line

    # forcase {P1}
    #       ( when (condition) do {P2}
    #            sequence {P3}
    #            end do )*
    # endforcase

    if lex_result[0] == 'forcase':
        # forcase token detected
        lex_result = lex()  # search for next token

        # {P1}:
        p1quad = nextquad()

        while lex_result[0] == 'case':
            lex_result = lex()  # search for next token

            if lex_result[0] == 'left parenthesis':
                lex_result = lex()  # search for next token

                cond_list = condition()  # cond_list[0] = cond.true and cond_list[1] = cond.false

                if lex_result[0] == 'right parenthesis':
                    lex_result = lex()  # search for next token

                    # {P2}:
                    backpatch(cond_list[0], nextquad())
                    statements()
                    # {P3}:
                    genquad("jump", "_", "_", p1quad)
                    backpatch(cond_list[1], nextquad())
                else:
                    printError("Right parenthesis was not detected after 'forcase' statement", file_line)

            else:
                printError("Left parenthesis was not detected before 'forcase' statement", file_line)

        if lex_result[0] == 'default':
            # default token detected
            lex_result = lex()  # search for next token

            statements()

            return
        else:
            printError("'default' statement was not detected after 'forcase' statement ", file_line)
    else:
        printError("'forcase' statement was not detected", file_line)


# incase statement
def incase_stat():
    global lex_result, file_line, symbol_list
    w = 0
    p1quad = ""
    # incase {P1}
    #       ( when (condition) do {P2}
    #            sequence {P3}
    #            end do )*
    # endincase {P4}

    if lex_result[0] == 'incase':
        # incase token detected
        # {P1}:
        w = newtemp()

        p1quad = nextquad()
        genquad(":=", 1, "_", w)
        lex_result = lex()  # search for next token

        while lex_result[0] == 'case':
            # case token detected
            lex_result = lex()  # search for next token

            if lex_result[0] == 'left parenthesis':
                lex_result = lex()  # search for next token

                cond_list = condition()  # cond_list[0] = cond.true and cond_list[1] = cond.false

                if lex_result[0] == 'right parenthesis':
                    lex_result = lex()  # search for next token

                    # {P2}:
                    backpatch(cond_list[0], nextquad())
                    genquad(":=", 0, "_", w)
                    statements()
                    # {P3}:
                    backpatch(cond_list[1], nextquad())
                else:
                    printError("Right parenthesis was not detected after 'incase' statement", file_line)
            else:
                printError("Left parenthesis was not detected before 'incase' statement", file_line)

    else:
        printError("'incase' statement was not detected", file_line)
    # {P4}:
    genquad(":=", w, 0, p1quad)
    return


# return statement
def return_stat():
    global lex_result, file_line, main_state_flag, procedure_state_flag, return_flag

    if lex_result[0] == 'return':
        # return token detected
        return_flag = True
        lex_result = lex()  # search for next token

        # We need to check if we detected this statement on
        # the main part of the program (main_state_flag)
        # or inside a procedure (procedure_state_flag)
        # both of them must not have the return statement
        if main_state_flag:
            printError("Return statement detected outside function", file_line)
        if procedure_state_flag:
            printError("Return statement detected inside a procedure", file_line)

        if lex_result[0] == 'left parenthesis':
            lex_result = lex()  # search for next token

            # S -> return (E) {P1}
            E_place = expression()

            if lex_result[0] == 'right parenthesis':
                lex_result = lex()  # search for next token

                genquad("retv", E_place, "_", "_")
                return
            else:
                printError("Right parenthesis was not detected after 'return' statement", file_line)

        else:
            printError("Left parenthesis was not detected before 'return' statement", file_line)


# call statement
def call_stat():
    global lex_result, file_line, function_flag, procedure_list

    if lex_result[0] == 'call':
        # call token detected
        lex_result = lex()  # search for next token
        function_flag = True

        if lex_result[0] == 'id':
            name = lex_result[1]
            lex_result = lex()  # search for next token

            # Checking if the name of the function/procedure has not been declared
            if name not in procedure_list:  # if False
                printError("Procedure" + "'" + name + "' has not been declared", file_line)

            if lex_result[0] == 'left parenthesis':
                lex_result = lex()  # search for next token

                par_list = actualparlist()

                # We need to check if we have the correct format of the parameters
                param_check(name, par_list)

                if lex_result[0] == 'right parenthesis':
                    lex_result = lex()  # search for next token

                    genquad("call", name, "_", "_")  # this is needed for both procedure or function

                    return
                else:
                    printError("Right parenthesis was not detected after 'call' statement", file_line)
            else:
                printError("Left parenthesis was not detected before 'call' statement", file_line)

        else:
            printError("Value name was not detected after 'call' statement", file_line)
    else:
        printError("'call' statement was not detected", file_line)

    return


# print statement
def print_stat():
    global lex_result, file_line

    if lex_result[0] == 'print':
        # print token detected
        lex_result = lex()  # search for next token

        if lex_result[0] == 'left parenthesis':
            lex_result = lex()  # search for next token

            # S -> print (E) {P1}
            E_place = expression()

            if lex_result[0] == 'right parenthesis':
                lex_result = lex()  # search for next token

                genquad("out", E_place, "_", "_")
            else:
                printError("Right parenthesis was not detected after 'print' statement", file_line)
        else:
            printError("Left parenthesis was not detected before 'call' statement", file_line)
    else:
        printError("'print' statement was not detected", file_line)
    return


# input statement
def input_stat():
    global lex_result, file_line, variables

    if lex_result[0] == 'input':
        # input token detected
        lex_result = lex()  # search for next token

        if lex_result[0] == 'left parenthesis':
            lex_result = lex()  # search for next token
            # S -> input (id) {P1}

            if lex_result[0] == 'id':
                id_place = lex_result[1]
                lex_result = lex()  # search for next token

                # We need to check that the variable is declared
                if id_place not in variables:
                    printError("The variable" + id_place + "has not been declared", file_line)

                if lex_result[0] == 'right parenthesis':
                    lex_result = lex()  # search for next token

                    genquad("inp", id_place, "_", "_")
                    return

                else:
                    printError("Right parenthesis was not detected after 'input' statement", file_line)
            else:
                printError("Value name was not detected after 'input' statement", file_line)
        else:
            printError("Left parenthesis was not detected before 'input' statement", file_line)
    else:
        printError("'input' statement was not detected", file_line)


# list of actual parameters
def actualparlist():
    global lex_result, file_line
    par_list = []  # list of parameters types
    par = actualparitem()  # search for a parameter and save its type
    par_list.append(par)  # add it to the list

    while lex_result[0] == 'comma':
        lex_result = lex()

        # Same as before for more than one parameters
        par = actualparitem()
        par_list.append(par)

    return par_list


# an actual parameter (" in ": by value , " inout " by reference )
def actualparitem():
    global lex_result, file_line

    result = ""  # the parameter type we will return if found

    if lex_result[0] == 'in':
        # in token detected
        result = lex_result[0]
        lex_result = lex()  # search for next token

        a_place = expression()  # in a
        genquad("par", a_place, "CV", "_")

    elif lex_result[0] == 'inout':
        # inout token detected
        result = lex_result[0]
        lex_result = lex()  # search for next token

        if lex_result[0] == 'id':
            b_place = lex_result[1]  # inout b
            lex_result = lex()  # search for next token
            genquad("par", b_place, "REF", "_")

        else:
            printError("Actualparitem: Value name was not detected after 'inout' statement", file_line)
    return result


# boolean expression
def condition():
    global lex_result

    # B -> Q1 {P1} (or {P2} Q2 {P3})*

    Q1_list = boolterm()

    # {P1}
    B_true = Q1_list[0]  # B.true = Q1.true
    B_false = Q1_list[1]  # B.false = Q1.false

    while lex_result[0] == 'or':
        # {P2}:
        backpatch(B_false, nextquad())
        lex_result = lex()  # search for next token

        # {P3}:
        Q2_list = boolterm()
        B_true = merge(B_true, Q2_list[0])
        B_false = Q2_list[1]  # B.false = Q2.false

    B_list = [B_true, B_false]
    return B_list


# term in boolean expression
def boolterm():
    global lex_result

    # Q -> R1 {P1} (and {P2} R2 {P3})*
    # {P1}:
    R1_list = boolfactor()

    Q_true = []
    Q_false = []

    Q_true = R1_list[0]  # Q.true = R1.true
    Q_false = R1_list[1]  # Q.false = R1.false

    while lex_result[0] == 'and':  # and token detected
        # {P2}:
        backpatch(Q_true, nextquad())
        lex_result = lex()  # search for next token

        R2_list = boolfactor()  # R2
        # {P3}:
        Q_false = merge(Q_false, R2_list[1])
        Q_true = R2_list[0]

    Q_list = [Q_true, Q_false]

    return Q_list


# factor in boolean expression
def boolfactor():
    global lex_result, file_line

    # R -> not (B) {P1}
    if lex_result[0] == 'not':
        # not statement detected
        lex_result = lex()  # search for next token

        if lex_result[0] == 'left block':
            lex_result = lex()  # search for next token

            B_list = condition()

            if lex_result[0] == 'right block':
                lex_result = lex()  # search for next token
                R_true = B_list[1]  # R.true = B.false
                R_false = B_list[0]  # R.false = B.true

                R_list = [R_true, R_false]  # save it to a list that we will return

                return R_list
            else:
                printError("Boolfactor: Right block was not detected after 'not' statement", file_line)
        else:
            printError("Boolfactor: Left block was not detected before 'not' statement", file_line)

    # not statement is not detected
    # R -> (B) {P1}
    elif lex_result[0] == 'left block':
        lex_result = lex()  # search for next token

        B_list = condition()

        if lex_result[0] == 'right block':
            lex_result = lex()  # search for next token

            R_true = B_list[0]  # R.true = B.true
            R_false = B_list[1]  # R.false = B.false

            R_list = [R_true, R_false]  # save it to a list that we will return

            return R_list

        else:
            printError("Boolfactor: Right block was not detected after boolfactor statement", file_line)
    else:
        # R -> E1 relop E2 {P1}

        E1_place = expression()

        relop = relational_op()

        E2_place = expression()

        R_true = makelist(nextquad())
        genquad(relop, E1_place, E2_place, "_")
        R_false = makelist(nextquad())
        genquad("jump", "_", "_", "_")
        R_list = [R_true, R_false]

        return R_list


# arithmetic expression
def expression():
    global lex_result, file_line, symbol_list

    symbol = optional_sign()

    # E -> T1 ( + T2 {P1}) * {P2}
    T1_place = term()

    # Checks if T1 is a negative number
    if symbol == "-":
        T1_place = "-" + T1_place

    while lex_result[0] == 'plus' or lex_result[0] == 'minus':
        symbol = lex_result[1]
        add_op()

        T2_place = term()

        # {P1}:
        w = newtemp()

        genquad(symbol, T1_place, T2_place, w)
        T1_place = w

    # {P2}:
    E_place = T1_place

    return E_place


# term in arithmetic expression       
def term():
    global lex_result, file_line, symbol_list

    # T -> F1 ( x F2 {P1}) * {P2}
    F1_place = factor()

    while lex_result[0] == 'multiply' or lex_result[0] == 'divide':
        symbol = lex_result[1]
        mul_op()

        F2_place = factor()
        # {P1}:
        w = newtemp()

        genquad(symbol, F1_place, F2_place, w)
        F1_place = w

    # {P2}:
    T_place = F1_place

    return T_place


# factor in arithmetic expression
def factor():
    global lex_result, file_line, procedure_list

    if lex_result[0] == 'number':
        F_place = lex_result[1]
        lex_result = lex()  # search for next token
        return F_place

    elif lex_result[0] == 'left parenthesis':
        lex_result = lex()  # search for next token

        F_place = expression()  # F.place = E.place

        if lex_result[0] == 'right parenthesis':
            lex_result = lex()  # search for next token

            return F_place
        else:
            printError("Factor: Right parenthesis was not detected after the number expression", file_line)

    elif lex_result[0] == 'id':
        F_place = lex_result[1]  # F.place = id.place

        # Check if the id responds to the name of a procedure
        if F_place in procedure_list:
            printError(F_place + " is a procedure, it cannot be called without the 'call' statement", file_line)

        idtail(F_place)

        return F_place

    else:
        printError("Factor: Number value or variable name was expected ", file_line)


# follows a function or procedure ( parenthesis and parameters )
def idtail(func_name):
    global lex_result, file_line, symbol_list

    lex_result = lex()  # search for next token

    if lex_result[0] == 'left parenthesis':
        lex_result = lex()  # search for next token

        par_list = actualparlist()

        # We need to check if we have the correct format of the parameters
        param_check(func_name, par_list)

        w = newtemp()

        genquad("par", w, "RET", "_")
        genquad("call", func_name, "_", "_")  # we are calling a function

        if lex_result[0] == 'right parenthesis':
            lex_result = lex()  # search for next token
        else:
            printError("Right parenthesis was not detected", file_line)

    return


# symbols "+" and " -" ( are optional )
def optional_sign():
    global lex_result

    symbol = lex_result[1]  # the '+' or '-' symbol if detected

    if (lex_result[0] == 'plus') or (lex_result[0] == 'minus'):
        # '+' or '-' tokens detected
        add_op()

    return symbol


# lexer rules : relational , arithmetic operations , multiplying operations
def relational_op():
    global lex_result, file_line

    relationals = ['equal', 'lesser than', 'lesser equal', 'not equal', 'greater than', 'greater equal']

    if lex_result[0] in relationals:  # '=','<','<=','<>','>','>='
        symbol = lex_result[1]  # save the symbol found
        lex_result = lex()  # search for next token

        return symbol
    else:
        printError("Relational operator was not detected", file_line)


# Add operator analysis
def add_op():
    global lex_result

    if (lex_result[0] == 'plus') or (lex_result[0] == 'minus'):  # + or -
        lex_result = lex()  # search for next token

        return


# Multiplier operator analysis
def mul_op():
    global lex_result

    if (lex_result[0] == 'multiply') or (lex_result[0] == 'divide'):  # * or /
        lex_result = lex()  # search for next token  

    return


# ----------------------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------------------

syntax()
# The file is no longer needed so close it
file.close()

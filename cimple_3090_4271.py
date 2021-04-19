# Todri Aggelos, AM:3090, username:cse53090
# Mpoulotis Panagiotis, AM:4271, username:cse74271

# Disclaimer: The code still needs some adjustments as it's currently in debugging state
# So this will be modified in later phases

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

'''
# All acceptable characters
acc_chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                        '0','1','2','3','4','5','6','7','8','9',
                        '+', '-', '*', '/','=',
                        '>','<','<=','>=','<>',':',
                        ':=','(',')','{','}','[',']',
                        ',','.','#',';',
                        ' ','\t','\n']
'''

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

# Errors

Error_non_valid_symbol = "Non-valid symbol detected"
Error_letter_after_digit = "There's an alphabetic character after a numerical digit"
Error_colon = "There isn't a = after the : symbol  "
Error_out_of_bounds = "There's an out-of-bounds number "
Error_string_length = "There's a string with more than 30 characters "
Error_brackets = "The EOF has been detected while a bracket is open"

# All the reserved words Cimple implements
reserved = ['program', 'declare', 'if', 'else',
            'while', 'switchcase',
            'forcase', 'incase', 'default', 'case',
            'not', 'and', 'or',
            'function', 'procedure', 'call', 'return', 'in', 'inout',
            'input', 'print']

# ----------------------------------------------------------------------------------------------------------------------------
# Functions and variables used for the intermediate code phase
# ----------------------------------------------------------------------------------------------------------------------------
quad_num = 0  # the number of quads created
quad_list = []  # the list of all quads
T_value = 0  # the number of the temporary variable used in "T_<T_value>"
program_name = ""
# name = ""  # the name of a procedure or function
function_flag = False  # true if there are functions/procedures in the cimple code.
# If there are, we don't need to create a C file
m_label = ""  # this value is given CV,REF,RET depending on the function's parameter


# Returns the number of the next quad to be created
def nextquad():
    global quad_num

    return quad_num


# Creates a new quad and adds it to the quad_list
def genquad(op, x, y, z):
    global quad_num, quad_list

    quad = [op, x, y, z]  # give the values of current quad to this list

    quad_list.append(quad)  # append the list created to the list of all the quads
    quad_num += 1  # a new quad has been created so +1 to the total number of quads
    print(quad)


# Creates and returns T_<T_value>
def newtemp():
    global T_value

    temp = "T_" + str(T_value)  # temp is now "T_<T_value>" for example "T_1" or "T_2"
    T_value += 1  # a new temporary variable has been created so +1 to the total number of temporary variables

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

    for i in range(quad_num-1):  # we want to start from 0, not 1
        if(i in list_given):  # searches the list given to find the number of quad indexed
            quad_list[i][3] = z  # completes the specific quad list by adding the z value


# ----------------------------------------------------------------------------------------------------------------------------
# File handling 
# ----------------------------------------------------------------------------------------------------------------------------
# Check if a cimple file is not given by the command file_line
if (len(sys.argv) == 1):
    print("There's not a cimple file given")
    sys.exit()

# Check if there are more than one cimple files is given by the command file_line
if (len(sys.argv) > 2):
    print("There are more than one cimple files given")
    sys.exit()

# Get the Cimple file from the command file_line
file = open(sys.argv[1], 'r')

file_line = 1  # first line of the file


# ----------------------------------------------------------------------------------------------------------------------------
# Lexical Analysis
# ----------------------------------------------------------------------------------------------------------------------------
# This will be used for printing the correct error when something
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

    while (state != final_state):  # while the character is not in a final state
        file_pos = file.tell()  # save the file's current position
        char = file.read(1)  # char reads the current character from the file

        # Start state analysis
        if (state == start_state):

            # detected a white character
            if (char in white_characters):
                # staying in the same state
                token_type = "white character"
                state = start_state
                if (char == '\n'):
                    file_line += 1  # changing file_line

            # detected an alphabetic character
            elif (char in letters):
                token_type = "id"
                prod_word += char
                state = word_state  # moving to state 1: creating a word

            # detected a numerical digit
            elif (char in digits):
                token_type = "number"
                prod_num += char
                state = digit_state  # moving to state 2: creating a number

            # detected a numerical symbol (+,-,*,/,=)
            elif (char in num_symbols):
                token_string += char
                if (char == '+'):
                    token_type = "plus"
                elif (char == '-'):
                    token_type = "minus"
                elif (char == '*'):
                    token_type = "multiply"
                elif (char == '/'):
                    token_type = "divide"
                elif (char == '='):
                    token_type = "equal"
                state = final_state
                file_pos += 1

            # detected a lesser than symbol
            elif (char == '<'):
                state = lesser_than_state  # moving to state 3: lesser than state
                token_type = "lesser than"
                token_string += char
                file_pos += 1

            # detected a greater than symbol
            elif (char == '>'):
                state = greater_than_state  # moving to state 4: greater than state
                token_type = "greater than"
                token_string += char
                file_pos += 1

            # detected a colon symbol
            elif (char == ':'):
                state = colon_state  # moving to state 5: colon (declaration) state
                token_type = "colon"
                token_string += char
                file_pos += 1

            # detected a left bracket symbol    
            elif (char == '{'):
                state = final_state
                token_type = "left bracket"
                token_string += char
                file_pos += 1

            # detected a right bracket symbol    
            elif (char == '}'):
                state = final_state
                token_type = "right bracket"
                token_string += char
                file_pos += 1

            # detected a hashtag (comment) symbol    
            elif (char == '#'):
                state = comment_state  # moving to state 7: comment state
                token_type = "hashtag1"
                token_string += char

            # detected a comma symbol
            elif (char == ','):
                state = final_state
                token_type = "comma"
                token_string += char
                file_pos += 1

            # detected a greek question mark symbol
            elif (char == ';'):
                state = final_state
                token_type = "question mark"
                token_string += char
                file_pos += 1

            # detected a left parethensis symbol
            elif (char == '('):
                state = final_state
                token_type = "left parethensis"
                token_string += char
                file_pos += 1

            # detected a right parethensis symbol
            elif (char == ')'):
                state = final_state
                token_type = "right parethensis"
                token_string += char
                file_pos += 1

            # detected a left block symbol
            elif (char == '['):
                state = final_state
                token_type = "left block"
                token_string += char
                file_pos += 1

            # detected a right block symbol
            elif (char == ']'):
                state = final_state
                token_type = "right block"
                token_string += char
                file_pos += 1

            # detected a dot symbol (EOF symbol)
            elif (char == '.'):
                state = EOF_state  # moving to state 9: EOF state
                token_type = "EOF symbol"
                token_string += char

                # Unacceptable characters
            else:
                print(char)
                printError(Error_non_valid_symbol, file_line)

                # word state analysis
        elif (state == word_state):
            if (char in letters or char in digits):
                prod_word += char
            else:
                token_string += prod_word
                state = final_state

            # The produced word exceeds 30 characters, so display error        
            if (len(prod_word) > 30):
                printError(Error_string_length, file_line)

        # Number state analysis    
        elif (state == digit_state):
            if (char in digits):
                prod_num += char

            # detected an alphabetic character after a numerical digit    
            elif (char in letters):
                printError(Error_letter_after_digit, file_line)

            else:
                # the number is created, proceed to the final state
                token_string += prod_num
                state = final_state

            # convert the string of the produced number to an integer so it
            # can be checked for errors
            number = int(prod_num)

            # The number is out of bounds
            if ((number < min_value) or (number > max_value)):
                printError(Error_out_of_bounds, file_line)

        # Lesser than state analysis
        elif (state == lesser_than_state):
            if (char == '='):
                state = final_state
                token_type = "lesser equal"
                token_string += char
                file_pos += 1
            elif (char == '>'):
                state = final_state
                token_type = "not equal"
                token_string += char
                file_pos += 1
            else:
                state = final_state

        # Greater than state analysis
        elif (state == greater_than_state):
            if (char == '='):
                state = final_state
                token_type = "greater equal"
                token_string += char
                file_pos += 1
            else:
                state = final_state

        # Colon state analysis
        elif (state == colon_state):
            if (char == '='):
                state = final_state
                token_type = "declaration"
                token_string += char
                file_pos += 1
            else:
                printError(Error_colon, file_line)

        # Comment state
        elif (state == comment_state):
            if (char == '#'):
                state = start_state
                token_type = "hashtag2"
                token_string = ''
            elif (char == '.'):
                printError(Error_brackets, file_line)
            else:
                state = comment_state

        # EOF state analysis
        elif (state == EOF_state):
            # We want to detect if there are characters after the EOF symbols has been detected
            # If there are the following warning message will be displayed
            file_pos += 1
            file.seek(file_pos)
            char = file.read(1)
            if (char):
                print("Warning: There's code after the EOF symbol was detected")
            state = final_state

    # If we reached this state, then a token has been detected
    if (state == final_state):
        # Set the files position here for next call of lex()
        file.seek(file_pos)

        # Check if the word produced is in the reserved words Cimple implements
    if (prod_word in reserved):
        token_type = prod_word

    # Declaring the return values of the lex function
    # Position 0:The token type 
    result.append(token_type)
    # Position 1:The token string 
    result.append(token_string)
    return result


''' Testing the lexical analysis
while(1):
        lexres = lex()
        if (lexres[0] == "EOF symbol"):
                break
        print(lexres)
'''


# ---------------------------------------------------------------------------------------------------------------------------
# Syntax Analysis
# Guided by Cimple's grammar
# ----------------------------------------------------------------------------------------------------------------------------

def syntax():
    global lex_result, function_flag
    lex_result = lex()  # the result of the lex() is stored here and will be used for the analysis

    # Execute the program analysis
    program()

    print("Syntax Analysis completed successfully")

    # int_file_create()

    # if(function_flag == False):
    #    c_file_create()

    return


# "program" is the starting symbol
def program():
    global lex_result, file_line, program_name  # the file line will be used for the error messages

    if (lex_result[0] == 'program'):
        # program token detected
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'id'):

            program_name = lex_result[1]  # save the program's name
            lex_result = lex()  # search for next token

            genquad("begin_block", program_name, "_", "_")
            block(program_name)

            if (lex_result[0] == 'EOF symbol'):
                # End of file reached
                genquad("halt", "_", "_", "_")
                genquad("end_block", program_name, "_", "_")
                return

            else:
                printError("The EOF symbol was not detected", file_line)

        else:
            printError("Program name is not given", file_line)
    else:
        printError("No 'program' key word detected at the start of the program ", file_line)


# a block with declarations , subprogram and statement
def block(name):
    global program_name

    # check if there are declarations
    declarations()

    # check if there are subprograms
    subprograms()

    if((name == "null") or (name == program_name)):
        # check if there are statements
        statements()
    else:
        genquad("begin_block", name, "_", "_")
        # check if there are statements
        statements()
        genquad("end_block", name, "_", "_")


# declaration of variables , zero or more " declare " allowed
def declarations():
    global lex_result, file_line, name

    while (lex_result[0] == 'declare'):
        # declare token detected
        lex_result = lex()  # search for next token

        # check the varlist() if there are one or more words
        varlist()

        if (lex_result[0] == 'question mark'):
            lex_result = lex()  # search for next token

            name = "null"
            block(name)  # go back to block() to check the other functions

        else:
            printError("Declarations: ';' character was not detected", file_line)
    return


# a list of variables following the declaration keyword
def varlist():
    global lex_result, file_line

    if (lex_result[0] == 'id'):
        # detected a variable name
        lex_result = lex()  # search for next token

        while (lex_result[0] == 'comma'):
            # detected ',' symbol so there may be another or more variables
            lex_result = lex()  # search for next token

            if (lex_result[0] == 'id'):
                lex_result = lex()  # search for next token

            else:

                printError("Varlist: There's not a variable after the ',' symbol ", file_line)

    return


# zero or more subprograms allowed
def subprograms():
    global lex_result, function_flag

    while ((lex_result[0] == 'procedure') or (lex_result[0] == 'function')):
        # detected a 'procedure' or 'function' keyword  proceed to subprogram analysis
        function_flag = True  # we don't need to create a C file
        subprogram()

    return


# a subprogram is a function or a procedure, followed by parameters and block
def subprogram():
    global lex_result, file_line, name

    # Procedure's analysis
    if (lex_result[0] == 'procedure'):
        # procedure token detected
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'id'):
            # procedure's name is given
            name = lex_result[1]  # save the name of the procedure
            lex_result = lex()  # search for next token

            if (lex_result[0] == 'left parethensis'):

                lex_result = lex()  # search for next token

                formalparlist()  # inside parethensis parameters analysis

                if (lex_result[0] == 'right parethensis'):

                    lex_result = lex()  # search for next token  # search for next token

                    block(name)  # go back to block() to check the other functions

                    return
                else:
                    printError("Procedure: Right parethensis not detected", file_line)
            else:
                printError("Procedure: Left parethensis not detected", file_line)
        else:
            printError("Procedure's name was not detected ", file_line)

    # Function's analysis
    elif (lex_result[0] == 'function'):
        # function token detected
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'id'):
            # function's name is given
            name = lex_result[1]  # save the name of the function
            lex_result = lex()  # search for next token

            if (lex_result[0] == 'left parethensis'):
                lex_result = lex()  # search for next token

                formalparlist()  # inside parethensis parameters analysis

                if (lex_result[0] == 'right parethensis'):
                    lex_result = lex()  # search for next token

                    block(name)  # go back to block() to check the other functions

                    return

                else:
                    printError("Function: Right parethensis not detected", file_line)
            else:
                printError("Function: Left parethensis not detected", file_line)
        else:
            printError("Function's name was not detected ", file_line)


# list of formal parameters
def formalparlist():
    global lex_result

    formalparitem()

    while (lex_result[0] == 'comma'):
        lex_result = lex()  # search for next token

        formalparitem()

    return


# a formal parameter (" in ": by value , " inout " by reference )
def formalparitem():
    global lex_result, file_line

    if (lex_result[0] == 'in'):
        # in token detected
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'id'):
            lex_result = lex()  # search for next token

            return
        else:
            printError("Formalparitem: A value name was espected after 'in' statement ", file_line)

    elif (lex_result[0] == 'inout'):
        # inout token detected
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'id'):
            lex_result = lex()  # search for next token

            return
        else:
            printError("Formalparitem: A value name was espected after 'inout' statement ", file_line)


# one or more statements
def statements():
    global lex_result, file_line

    if (lex_result[0] == 'left bracket'):
        lex_result = lex()  # search for next token
        statement()

        while (lex_result[0] == 'question mark'):
            lex_result = lex()  # search for next token

            statement()

        if (lex_result[0] == 'right bracket'):
            lex_result = lex()  # search for next token
            return

        else:
            printError("Statements: Right bracket wasn't detected", file_line)

    else:

        statement()

        if (lex_result[0] == 'question mark'):
            lex_result = lex()  # search for next token

            return
        elif (lex_result[0] == 'EOF symbol'):
            return
        else:
            printError("Statements: ';' character wasn't detected after statement", file_line)


# one statement
def statement():
    global lex_result

    if (lex_result[0] == 'id'):
        assignment_stat()

    elif (lex_result[0] == 'if'):
        # if token detected
        if_stat()

    elif (lex_result[0] == 'while'):
        # while token detected
        while_stat()

    elif (lex_result[0] == 'switchcase'):
        # switchcase token detected
        switchcase_stat()

    elif (lex_result[0] == 'forcase'):
        # forcase token detected
        forcase_stat()

    elif (lex_result[0] == 'incase'):
        # incase token detected
        incase_stat()

    elif (lex_result[0] == 'call'):
        # call token detected
        call_stat()

    elif (lex_result[0] == 'return'):
        # return token detected
        return_stat()

    elif (lex_result[0] == 'input'):
        # input token detected
        input_stat()

    elif (lex_result[0] == 'print'):
        # print token detected
        print_stat()

    return


# assignment statement
def assignment_stat():
    global lex_result, file_line

    if (lex_result[0] == 'id'):
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'declaration'):
            lex_result = lex()  # search for next token

            expression()

            return
        else:
            printError("Declaration symbol was not detected after assignment's name", file_line)
    else:
        printError("Assignment's name was not detected", file_line)


# if statement
def if_stat():
    global lex_result, file_line

    if (lex_result[0] == 'if'):
        # if token detected
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'left parethensis'):
            lex_result = lex()  # search for next token

            condition()

            if (lex_result[0] == 'right parethensis'):
                lex_result = lex()  # search for next token

                statements()
                elsepart()
                return

            else:
                printError("Right parethensis was not detected after 'IF' statement", file_line)
        else:
            printError("Left parethensis was not detected before 'IF' statement", file_line)
    else:
        printError("'IF' statement was not detected", file_line)


# else statement
def elsepart():
    global lex_result

    if (lex_result[0] == 'else'):
        # else token detected
        lex_result = lex()  # search for next token

        statements()

    return


# while statement
def while_stat():
    global lex_result, file_line

    if (lex_result[0] == 'while'):
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'left parethensis'):
            lex_result = lex()  # search for next token
            condition()

            if (lex_result[0] == 'right parethensis'):
                lex_result = lex()  # search for next token

                statements()

                return
            else:
                printError("Right parethensis was not detected after 'while' statement", file_line)
        else:
            printError("Left parethensis was not detected before 'while' statement", file_line)
    else:
        printError("'while' statement was not detected", file_line)


# switch statement
def switchcase_stat():
    global lex_result, file_line

    if (lex_result[0] == 'switchcase'):
        # switchcase token detected
        lex_result = lex()  # search for next token

        while (lex_result[0] == 'case'):
            # case token detected
            lex_result = lex()  # search for next token

            if (lex_result[0] == 'left parethensis'):
                lex_result = lex()  # search for next token

                condition()

                if (lex_result[0] == 'right parethensis'):
                    lex_result = lex()  # search for next token

                    statements()

                else:
                    printError("Right parethensis was not detected after 'switchcase' statement", file_line)

            else:
                printError("Left parethensis was not detected before 'switchcase' statement", file_line)

        if (lex_result[0] == 'default'):
            # default token detected
            lex_result = lex()  # search for next token

            statements()
            return
        else:
            printError("'default' statement was not detected after 'switchcase' statement ", file_line)
    else:
        printError("'switchcase' statement was not detected", file_line)


# forcase statement
def forcase_stat():
    global lex_result, file_line

    if (lex_result[0] == 'forcase'):
        # forcase token detected
        lex_result = lex()  # search for next token

        while (lex_result[0] == 'case'):
            lex_result = lex()  # search for next token

            if (lex_result[0] == 'left parethensis'):
                lex_result = lex()  # search for next token

                condition()

                if (lex_result[0] == 'right parethensis'):
                    lex_result = lex()  # search for next token

                    statements()

                else:
                    printError("Right parethensis was not detected after 'forcase' statement", file_line)

            else:
                printError("Left parethensis was not detected before 'forcase' statement", file_line)

        if (lex_result[0] == 'default'):
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
    global lex_result, file_line

    if (lex_result[0] == 'incase'):
        # incase token detected
        lex_result = lex()  # search for next token

        while (lex_result[0] == 'case'):
            # case token detected
            lex_result = lex()  # search for next token

            if (lex_result[0] == 'left parethensis'):
                lex_result = lex()  # search for next token

                condition()

                if (lex_result[0] == 'right parethensis'):
                    lex_result = lex()  # search for next token

                    statements()

                else:
                    printError("Right parethensis was not detected after 'incase' statement", file_line)
            else:
                printError("Left parethensis was not detected before 'incase' statement", file_line)

    else:
        printError("'incase' statement was not detected", file_line)
    return


# return statement
def return_stat():
    global lex_result, file_line

    if (lex_result[0] == 'return'):
        # return token detected
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'left parethensis'):
            lex_result = lex()  # search for next token

            expression()

            if (lex_result[0] == 'right parethensis'):
                lex_result = lex()  # search for next token

                return
            else:
                printError("Right parethensis was not detected after 'return' statement", file_line)

        else:
            printError("Left parethensis was not detected before 'return' statement", file_line)


# call statement
def call_stat():
    global lex_result, file_line, function_flag

    if (lex_result[0] == 'call'):
        # call token detected
        lex_result = lex()  # search for next token
        function_flag = True

        if (lex_result[0] == 'id'):
            lex_result = lex()  # search for next token

            if (lex_result[0] == 'left parethensis'):
                lex_result = lex()  # search for next token

                actualparlist()

                if (lex_result[0] == 'right parethensis'):
                    lex_result = lex()  # search for next token

                    return
                else:
                    printError("Right parethensis was not detected after 'call' statement", file_line)
            else:
                printError("Left parethensis was not detected before 'call' statement", file_line)

        else:
            printError("Value name was not detected after 'call' statement", file_line)
    else:
        printError("'call' statement was not detected", file_line)

    return


# print statement
def print_stat():
    global lex_result, file_line

    if (lex_result[0] == 'print'):
        # print token detected
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'left parethensis'):
            lex_result = lex()  # search for next token

            expression()

            if (lex_result[0] == 'right parethensis'):
                lex_result = lex()  # search for next token

            else:
                printError("Right parethensis was not detected after 'print' statement", file_line)
        else:
            printError("Left parethensis was not detected before 'call' statement", file_line)
    else:
        printError("'print' statement was not detected", file_line)
    return


# input statement
def input_stat():
    global lex_result, file_line

    if (lex_result[0] == 'input'):
        # input token detected
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'left parethensis'):
            lex_result = lex()  # search for next token

            if (lex_result[0] == 'id'):
                lex_result = lex()  # search for next token

                if (lex_result[0] == 'right parethensis'):
                    lex_result = lex()  # search for next token
                    return

                else:
                    printError("Right parethensis was not detected after 'input' statement", file_line)
            else:
                printError("Value name was not detected after 'input' statement", file_line)
        else:
            printError("Left parethensis was not detected before 'input' statement", file_line)
    else:
        printError("'input' statement was not detected", file_line)


# list of actual parameters
def actualparlist():
    global lex_result, file_line

    actualparitem()

    while (lex_result[0] == 'comma'):
        lex_result = lex()

        actualparitem()

    return


# an actual parameter (" in ": by value , " inout " by reference )
def actualparitem():
    global lex_result, file_line

    if (lex_result[0] == 'in'):
        # in token detected
        lex_result = lex()  # search for next token

        expression()

    elif (lex_result[0] == 'inout'):
        # inout token detected
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'id'):
            lex_result = lex()  # search for next token

        else:
            printError("Actualparitem: Value name was not detected after 'inout' statement", file_line)
    return


# boolean expression
def condition():
    global lex_result

    # B -> Q1 {P1} (or {P2} Q2 {P3})*

    Q1_list = boolterm()

    # {P1}
    B_true = Q1_list[0]  # B.true = Q1.true
    B_false = Q1_list[1]  # B.false = Q1.false

    while (lex_result[0] == 'or'):
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

    Q_true = R1_list[0]  # Q.true = R1.true
    Q_false = R1_list[1]  # Q.false = R1.false

    while (lex_result[0] == 'and'):  # and token detected
        # {P2}:
        backpatch(Q_true, nextquad())
        lex_result = lex()  # search for next token

        # {P3}:
        R2_list = boolfactor()
        Q_false = merge(Q_false, R2_list[1])
        Q_true = R2_list[0]

    Q_list = [Q_true, Q_false]

    return Q_list


# factor in boolean expression
def boolfactor():
    global lex_result, file_line

    # R -> not (B) {P1}
    if (lex_result[0] == 'not'):
        # not statement detected
        lex_result = lex()  # search for next token

        if (lex_result[0] == 'left block'):
            lex_result = lex()  # search for next token

            B_list = condition()

            if (lex_result[0] == 'right block'):
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
    elif (lex_result[0] == 'left block'):
        lex_result = lex()  # search for next token

        B_list = condition()

        if (lex_result[0] == 'right block'):
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
    global lex_result, file_line

    optional_sign()

    # E -> T1 ( + T2 {P1}) * {P2}
    T1_place = term()

    while (lex_result[0] == 'plus' or lex_result[0] == 'minus'):
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
    global lex_result, file_line

    # T -> F1 ( x F2 {P1}) * {P2}
    F1_place = factor()

    while (lex_result[0] == 'multiply' or lex_result[0] == 'divide'):
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
    global lex_result, file_line

    if (lex_result[0] == 'number'):
        F_place = lex_result[1]
        lex_result = lex()  # search for next token

        return F_place

    elif (lex_result[0] == 'left parethensis'):
        lex_result = lex()  # search for next token

        F_place = expression()  # F.place = E.place

        if (lex_result[0] == 'right parethensis'):
            lex_result = lex()  # search for next token

            return F_place
        else:
            printError("Factor: Right parethensis was not detected after the number expression", file_line)

    elif (lex_result[0] == 'id'):
        F_place = lex_result[1]  # F.place = id.place

        idtail()
        return F_place
    else:
        printError("Factor: Number value or variable name was expected ", file_line)


# follows a function of procedure ( parethensis and parameters )
def idtail():
    global lex_result, file_line

    lex_result = lex()  # search for next token

    if (lex_result[0] == 'left parethensis'):
        lex_result = lex()  # search for next token

        actualparlist()

        if (lex_result[0] == 'right parethensis'):
            lex_result = lex()  # search for next token

    return


# symbols "+" and " -" ( are optional )
def optional_sign():
    global lex_result

    symbol = lex_result[1]  # the '+' or '-' symbol if detected

    if ((lex_result[0] == 'plus') or (lex_result[0] == 'minus')):
        # '+' or '-' tokens detected
        add_op()

    return symbol


# lexer rules : relational , arithmetic operations , multiplying operations
def relational_op():
    global lex_result, file_line

    relationals = ['equal', 'lesser than', 'lesser equal', 'not equal', 'greater than', 'greater equal']

    if (lex_result[0] in relationals):  # '=','<','<=','<>','>','>='
        symbol = lex_result[1]  # save the symbol found
        lex_result = lex()  # search for next token

        return symbol
    else:
        printError("Relational operator was not detected", file_line)


# Add operator analysis
def add_op():
    global lex_result

    if ((lex_result[0] == 'plus') or (lex_result[0] == 'minus')):  # + or -
        lex_result = lex()  # search for next token

        return


# Multiplier operator analysis
def mul_op():
    global lex_result

    if ((lex_result[0] == 'multiply') or (lex_result[0] == 'divide')):  # * or /
        lex_result = lex()  # search for next token  

    return


syntax()
# The file is no longer needed so close it
file.close()


# ----------------------------------------------------------------------------------------------------------------------------
# C file handling
# ----------------------------------------------------------------------------------------------------------------------------
def c_file_create():
    global program_name

    variables = []  # the variables declared in the program
    variable_string = ""  # will be used for printing the variables
    relops = rel_symbols.append("=")  # all the =,>,<,<>,>=,<= symbols
    relop_id = ""  # this wil be used in its respective file.write()

    for i in quad_list:
        if(quad_list[i][0] == ":="):  # detected a variable
            variables.append(quad_list[i][3])  # add it to the list
            variable_string += quad_list[i][3] + ","  # convert the list to a string

    # for i in variables:
    #    variable_string += variables[i] + ","  # convert the list to a string

    variable_string = variable_string[:-1] + ";"  # replace the last "," with ";"

    c_file = open(program_name + '.c', 'w')  # creates the .c file
    c_file.write("#include <stdio.h> \t// for the printf and scanf functions \n")  # will be need for the functions used
    c_file.write("int main() \n" + "{\n")
    c_file.write("\t" + "int " + variable_string + "\n")  # writes all the variables declared

    for i in quad_list:
        # first line
        if(quad_list[i][0] == "begin_block"):
            c_file.write("\t" + "L_" + str(i) + ":")

        # declaration statement
        elif(quad_list[i][0] == ":="):
            c_file.write("\t" + "L_" + str(i) + ":" + str(quad_list[i][3]) + "=" + str(quad_list[i][1]) + ";" + " //(" + str(quad_list[i]) + ")")

        # numerical operation statements
        elif((quad_list[i][0] == "+") or (quad_list[i][0] == "-") or (quad_list[i][0] == "*") or (quad_list[i][0] == "/")):
            c_file.write("\t" + "L_" + str(i) + ":" + str(quad_list[i][3]) + "=" + str(quad_list[i][1]) + str(quad_list[i][0]) + str(quad_list[i][2]) + ";" + " //(" + str(quad_list[i]) + ")")

        # if statements
        elif (quad_list[i][0] in relops):

            if(quad_list[i][0] == "="):  # equal in c is ==
                relop_id = "=="
            elif(quad_list[i][0] == "<>"):  # not equal in c is !=
                relop_id = "!="
            else:
                relop_id = str(quad_list[i][0])
            c_file.write("\t" + "L_" + str(i) + ":" + "if (" + str(quad_list[i][1]) + relop_id + str(quad_list[i][2]) + ") goto L_" + str(quad_list[i][3]) + ";" + " //(" + str(quad_list[i]) + ")")

        # jump statement
        elif (quad_list[i][0] == "jump"):
            c_file.write("\t" + "L_" + str(i) + ":" + "goto L_" + str(quad_list[i][3]) + ";" + " //(" + str(quad_list[i]) + ")")

        # end of program
        elif (quad_list[i][0] == "halt"):
            c_file.write("\t" + "L_" + str(i) + ":" + "return 0;" + " //(" + str(quad_list[i]) + ")")

        # return statement
        elif (quad_list[i][0] == "retv"):
            c_file.write("\t" + "L_" + str(i) + ":" + "return " + str(quad_list[i][0]) + ";" + " //(" + str(quad_list[i]) + ")")

        # input - scanf statement
        elif (quad_list[i][0] == "inp"):
            c_file.write("\t" + "L_" + str(i) + ":" + "scanf(%d,&" + str(quad_list[i][1]) + "); //(" + str(quad_list[i]) + ")")

        # output - printf statement
        elif (quad_list[i][0] == "out"):
            c_file.write("\t" + "L_" + str(i) + ":" + "printf(%d," + str(quad_list[i][1]) + "); //(" + str(quad_list[i]) + ")")

        else:
            print("Something went wrong with the creation of the C file")
            sys.exit()

    c_file.write("}")
    c_file.close()  # the file is completed


# ----------------------------------------------------------------------------------------------------------------------------
# int file handling
# ----------------------------------------------------------------------------------------------------------------------------
def int_file_create():
    global program_name

    int_file = open(program_name + '.int', 'w')  # creates the .int file

    for i in quad_list:
        int_file.write(str(i) + ": " + str(quad_list[i][0]) + " " + str(quad_list[i][1]) + " " + str(quad_list[i][2]) + " " + str(quad_list[i][3]))

    int_file.close()  # the file is completed

#Todri Aggelos, AM:3090, username:cs03090
#Mpoulotis Panagiotis, AM:4271, username:cse74271

import sys          #needed for reading the test files
import string       #may be needed 

min_value = -(pow(2,32)-1)
max_value = (pow(2,32)-1)

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
                        
digits = ['0','1','2','3','4','5','6','7','8','9']

#numerical symbols
num_symbols = ['+', '-', '*', '/','=']

#relational symbols
rel_symbols =  ['>','<','<=','>=','<>']

#declaration symbol
dec_symbol = ':='

#separation symbols
sep_symbols = [';',':']

#grouping symbols 
group_symbols =['(', ')' ,'[',']','{','}' ]

#Comma symbol
comma_symbol = ','

#End of File symbol
EOF_symbol = '.'

#Comment symbol
cmt_symbol= '#'

#White character symbols
white_characters = [' ','\t','\n']

#All acceptable characters
acc_chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                        '0','1','2','3','4','5','6','7','8','9',
                        '+', '-', '*', '/','=',
                        '>','<','<=','>=','<>',
                        ':=', '(', ')' , '{','}','[',']'
                        ',','.','#',
                        ' ','\t','\n']

#States for Lexical Analysis
start_state = 0
letter_state = 1
digit_state = 2
lesser_than_state = 3
greater_than_state = 4
colon_state = 5
bracket_state = 6 
comment_state = 7
final_state = 8
EOF_state = 9

lex_states = [start_state,letter_state,digit_state,lesser_than_state,greater_than_state,colon_state,bracket_state,comment_state,final_state]

#Errors

Error_non_valid_symbol =  "Non-valid symbol detected"
Error_letter_after_digit= "There's an alphabetic character after a numerical digit"
Error_colon =             "There isn't a = after the : symbol  "
Error_out_of_bounds =     "There's an out-of-bounds number "
Error_string_length =     "There's a string with more than 30 characters "
Error_brackets=           "The EOF has been found while a bracket is open"  

#All the reserved words Cimple implements 
reserved = ['program' ,'declare','if','else',
                                        'while','switchcase',
                                        'forcase','incase','default','case',
                                        'not','and','or',
                                        'function','procedure','call','return','in','inout',
                                        'input','print']

                                        
 
#This will be used for printing the correct error when something 
def printError(Error,line):
    print('Error: '+ Error+' at line '+ str(line))
    sys.exit()

#Check if a cimple file is not given by the command line
if (len(sys.argv)==1):
    print("There's not a cimple file given")
    sys.exit()

#Check if there are more than one cimple files is given by the command line
if (len(sys.argv)>2):    
    print("There are more than one cimple files given")
    sys.exit()

#Get the Cimple file from the command line    
file = open(sys.argv[1],'r')

'''
#For testing reasons
n=1
char=''
tempchar=''
while (char!= EOF_symbol):
    char= file.read(n)
    tempchar = tempchar + char
char=''

'''

file_line = 1       #first line of the file

#Lexical Analysis
def lex():
    global file_line
    state = start_state         #start with the state 0: start state
    file_pos = 0;               #a simple counter for the position of the file 
    prod_word = ''              #produced word: the word the alphabetic characters create     
    prod_num  = ''              #produced number : the number the numerical characters create 
                                #will be later converted to int so it can be checked  
    Error=''                    #will be used for the error messages
    
    token_type   =''            #the type of the token
    token_string =''            #the string of the token
    
    result = []                 #the result lex returns
        
    while(state != final_state): #while the character is not in a final state  
        file_pos = file.tell()   #save the file's current position
        char = file.read(1)
        #print(file_pos)
        #Start state analysis
        if(state == start_state):   
            #Found a white character
            if(char in white_characters):
                #staying in the same state
                token_type = "white character"
                token_string += char
                if(char == '\n'):
                    file_line += 1 #changing line
            #Found an alphabetic character        
            elif(char in alphabet):
                token_type = "letter"
                prod_word += char 
                state = letter_state #moving to state 1: creating a letter
            #Found a numerical digit
            elif(char in digits):
                token_type = "number"
                prod_num += char 
                state = digit_state  #moving to state 2: creating a number
                
            #Found a numerical symbol (+,-,*,/,=)
            elif(char in num_symbols):
                state = final_state
                token_type = "numerical symbol" 
                token_string+= char 
            #Found a lesser than symbol
            elif(char =='<'):
                state = lesser_than_state #moving to state 3: lesser than state
                token_type = "lesser than"
                token_string += char
            #Found a greater than symbol
            elif(char =='>'):
                state = greater_than_state #moving to state 4: greater than state 
                token_type = "greater than"
                token_string += char
            #Found a colon symbol
            elif(char == ':'):
                state = colon_state #moving to state 5: colon (declaration) state
                token_type = "colon"
                token_string += char
            #Found a left bracket symbol    
            elif(char == '{'): 
                state = bracket_state #moving to state 6: bracket state
                token_type = "left bracket"
                token_string += char
            #Found a hashtag (comment) symbol    
            elif(char == '#'): 
                state = comment_state #moving to state 7: comment state
                token_type = "hashtag1"
                token_string += char
            #Found a comma symbol
            elif(char == ','):
                state = final_state
                token_type = "comma"            
                token_string += char
            #Found a left parenthesis symbol
            elif((char == '(') or (char == '[')):
                state = final_state
                token_type = "left parenthesis"
                token_string += char
            #Found a right parenthesis symbol
            elif((char == ')') or (char == ']')):
                state = final_state
                token_type = "right parenthesis"
                token_string += char
            #Found a dot symbol (EOF symbol)
            elif(char == '.'):
                state = EOF_state #moving to state 9: EOF state
                token_type = "EOF symbol"
                token_string += char 
                
        
        #Letter state analysis
        elif(state == letter_state):
            if(char in alphabet or char in digits):
                prod_word += char
                #print(prod_num)
            else:
                token_string += prod_word
                state = final_state
                
            if(len(prod_word) > 30):
                printError(Error_string_length,file_line)
                
        
        #Number state analysis    
        elif(state == digit_state):
            if(char in digits):
                prod_num += char
            #Found an alphabetic character after a numerical digit    
            elif(char in alphabet):
                printError(Error_letter_after_digit,file_line)
            else:
                token_string += prod_num 
                state = final_state
                
            #convert the string of the produced number to an integer so it
            #can be checked for errors    
            number = int(prod_num)
            
            #The number is out of bounds
            if((number < min_value) or (number > max_value)):
                printError(Error_out_of_bounds,file_line)
        
        #Lesser than state analysis
        elif(state == lesser_than_state):
            if(char == '='):
                state = final_state
                token_type = "lesser equal"
                token_string += char
            elif(char == '>'):
                state = final_state
                token_type = "not equal"
                token_string += char
            else:
                state = final_state
                 
        #Greater than state analysis
        elif(state == greater_than_state):
            if(char == '='):
                state = final_state
                token_type = "greater equal"
                token_string += char
            else:
                state = final_state
        
        #Colon state analysis
        elif(state == colon_state):
            if(char == '='):
                state = final_state
                token_type = "declaration"
                token_string += char
            else:    
                printError(Error_colon,file_line)
        
        #Bracket state analysis
        elif(state == bracket_state):
            if(char == '}'):
                state = start_state
                token_type = "right bracket"
                token_string += char
            elif(char == '.'):
                printError(Error_brackets,file_line)
            else:
                state = final_state

        #Comment state
        elif(state ==  comment_state):
            if(char == '#'):
                state = start_state
                token_type = "hashtag2"
                token_string += char
            #CHECK THIS    
            elif(char == '.'):
                printError(Error_brackets,file_line)
            else:
                state = final_state
        #EOF state analysis
        elif(state == EOF_state):    
            print("Hopefully, everything is fine")
            
        #Unacceptable characters
        if(char not in acc_chars):
            printError(Error_non_valid_symbol,file_line)    
            
    #If we reached this state, then a token has been found
    if(state == final_state):
        #Set the files position here for next call of lex()
        file.seek(file_pos) 
       
    #Check if the word produced is in the reserved words Cimple implements 
    if(prod_word in reserved ):
        #print("Here")
        token_type = prod_word
        
    #Declaring the return type of the lex function
    #Position 0:The token type 
    result.append(token_type)
    #Position 1:The token string 
    result.append(token_string)
    #Position 2:The file line
    result.append(file_line)            
    return result
        
lex_result = lex()
print(lex_result[0])
#print(file_line)

#---------------------------------------------------------------------------------------------------------------------------
#Syntax Analysis





#The file is no longer needed so close it
file.close()





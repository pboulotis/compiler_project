#
#Mpoulotis Panagiotis, AM:4271, username:cse74271

import sys          #needed for reading the test files
import string       #may be needed 

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
                        
digits = ['0','1','2','3','4','5','6','7','8','9']

#numerical symbols
num_symbols = ['+', '-', '*', '/']

#comparison symbols
com_symbols = ['=','>','<','<=','>=','<>']

#declaration symbol
dec_symbol = ':='

#separation symbols
sep_symbols = [';', '“','”', ':']

#grouping symbols 
group_symbols = ['[', ']', '(', ')' , '{' , '}']

#End of File symbol
EOF_symbol = '.'

#Comment symbol
cmt_symbol= '#'

#States for Lectical Analysis
start_state = 0
letter_state = 1
digit_state = 2
less_than_state = 3
greater_than_state = 4
colon_state = 5
bracket_state = 6 
comment_state = 7
final_state = 8

lex_states = [start_state,letter_state,digit_state,less_than_state,greater_than_state,colon_state,bracket_state,comment_state,final_state]

#Errors
Error_non_valid_symbol=-1
Error_letter_after_digit=-2
Error_colon=-3
Error_out_of_bounds=-4
Error_string_length=-5
Error_brackets=-6

#All the reserved words Cimple implements 
reserved = ['program' ,'declare','if','else',
                                        'while','switchcase',
                                        'forcase','incase','default','case',
                                        'not','and','or',
                                        'function','procedure','call','return','in','inout',
                                        'input','print']
 
#In order to create our transition diagram we need to check each state transition
#The following will be used as the identifiers of the position of the token in the state transition array
white_character = 0
letter=1
digit=2
plus=3
minus=4
multiply=5
divide=6
equal=7
less_than=8
greater_than=9
EOF=10
non_valid_symbol=11
comma=12
greek_question_mark=13
left_parenthesis=14
right_parenthesis=15
left_bracket=16
right_bracket=17
open_block=18
close_block=19
newline= 20                                                     
colon=21                                                        # : symbol
dot=22                                                          #End Of File identifier
hashtag=23

#Their relative tokens where tk=token
letter_tk=30
digit_tk=31
plus_tk=32
minus_tk=33
multiply_tk=34
divide_tk=35
equal_tk=36
lessthan_tk=37
greaterthan_tk=38
EOF_tk=39
comma_tk=41
greek_question_mark_tk=42
left_parenthesis_tk=43
right_parenthesis_tk=44
left_bracket_tk=45
right_bracket_tk=46
open_block_tk=47
close_block_tk=48
lessORequal_tk=49
greaterORequal_tk=50
colon_tk= 51
decl_tk= 52                                 #declaration token
not_equal_tk=53 
dot_tk=54


Transition_Diagram = [
                    #Start state transitions:
                    
                    [start_state,letter_state,digit_state,plus_tk,minus_tk, multiply_tk,divide_tk,equal_tk,less_than_state,greater_than_state
                    EOF_tk,Error_non_valid_symbol,comma_tk,greek_question_mark_tk,left_parenthesis_tk,right_parenthesis_tk,
                    left_bracket_tk,right_bracket_tk,open_block_tk,close_block_tk,start_state,colon_state,final_state,comment_state],
                    
                    #Letter state transitions:
                    
                    [letter_tk,letter_state,letter_state,letter_tk,letter_tk,letter_tk,letter_tk,letter_tk,letter_tk,
                    letter_tk,letter_tk,Error_non_valid_symbol,letter_tk,letter_tk,letter_tk,letter_tk,letter_tk,letter_tk,letter_tk,
                    letter_tk,letter_tk,letter_tk,letter_tk,letter_tk],

                    #Digit state transitions:
                    [digit_tk,Error_letter_after_digit, digit_state,digit_tk,digit_tk,digit_tk,
                    digit_tk,digit_tk,digit_tk,digit_tk,digit_tk,Error_non_valid_symbol,
                    digit_tk,digit_tk,digit_tk,digit_tk,digit_tk,digit_tk,digit_tk,digit_tk,
                    digit_tk,digit_tk,digit_tk,digit_tk],
                    
                    #Less than transitions:
       
                    [lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,
                     lessthan_tk,lessORequal_tk,lessthan_tk,not_equal_tk,lessthan_tk,Error_non_valid_symbol,
                     lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,
                     lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk],
                
                    #Greater than transitions:
                    [greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,
                     greaterthan_tk,greaterORequal_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,Error_non_valid_symbol,
                     greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,
                     greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk],
                     
                     
                    #Colon state transitions:
                    [Error_colon,Error_colon,Error_colon,Error_colon,Error_colon,Error_colon,
                     Error_colon,decl_tk,Error_colon,Error_colon,Error_colon,Error_non_valid_symbol,
                     Error_colon,Error_colon,Error_colon,Error_colon,Error_colon,Error_colon,Error_colon,Error_colon,
                     Error_colon,Error_colon,Error_colon,Error_colon]
                     
                    #Bracket state transitions: 
                    [bracket_state,bracket_state,bracket_state,bracket_state,bracket_state,bracket_state,
                     bracket_state,bracket_state,bracket_state,bracket_state,Error_brackets,bracket_state,
                     bracket_state,bracket_state,bracket_state,bracket_state,bracket_state,bracket_state,bracket_state,bracket_state,
                     katastasi_start,bracket_state,bracket_state,start_state]

                    ] 







 
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


#For testing reasons
n=1
char=''
tempchar=''
while (char!= EOF_symbol):
    char= file.read(n)
    tempchar = tempchar + char







#The file is no longer needed so close it
file.close()





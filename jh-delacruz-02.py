import string
import re


def get_ascii():
    # Get all 95 ascii characters
    ascii_characters = string.printable.strip()
    ascii_characters_list = list(ascii_characters)
    ascii_characters_list.append(' ')
    len(ascii_characters)
    len(ascii_characters_list)
    return ascii_characters_list


def clean_me_basic(user_inp):
    # Clean and return the input
    # Replaces all the tabs with one space
    user_inp = user_inp.replace('\t', ' ')
    # Removes any leading (spaces at the beginning) and trailing (spaces at the end)
    user_inp = user_inp.strip()
    # Removes more than 1 space
    user_inp = re.sub('\s+', " ", user_inp)

    return user_inp


def get_string(user_inp):
    # Get the string using the original input
    # Removes any leading (spaces, tabs at the beginning) and trailing (spaces,tabs at the end)
    user_inp = user_inp.strip()
    # Strip off the backslash
    user_inp = user_inp.replace('\\"','"')
    # Find the location of the first double quote
    loc_start = user_inp.find('"')
    # Find the location of the next double quote. This is with an assumption that the string has valid double quotes,
    loc_end = user_inp.find('"', loc_start+1)
    # Get the string from before start and end of double quotes
    string_input = user_inp[loc_start+1:loc_end]

    return string_input

def get_string_wo_comments(user_inp):
    # Removes the comments from the input
    # Find the location of the first #
    loc_start = user_inp.find('#')
    if (loc_start >= 0):
        # Get the string from before the #
        user_inp = user_inp[:loc_start]
        # Removes any leading (spaces, tabs at the beginning) and trailing (spaces,tabs at the end)
        user_inp = user_inp.strip()
    return user_inp


def check_invalid_chars(user_inp):
    # Check for invalid characters
    # Get ascii list
    ascii_list = get_ascii()
    not_ascii = ""
    msg = ""

    for word in user_inp:
        word_list = list(word)
        for c in word_list:
            if not c in ascii_list:
                not_ascii += "{0} ".format(c)

    # Return syntax error message
    if not_ascii != "":
        msg = "{0}".format(error_messages['SYNTAX_ERROR'])
        #if len(not_ascii) < 3:
           # msg += "The {0}{1}".format(not_ascii, error_messages['INVALID_ASCII'])
       # else:
           # msg += "The {0}{1}".format(not_ascii, error_messages['INVALID_ASCIIS'])
    return msg


if __name__ == '__main__':
    # Main program
    # All valid keyword list
    keyword_list = ['GIVEYOU!', 'GIVEYOU!!', 'PLUS', 'MINUS', 'TIMES', 'DIVBY', 'MODU']
    # Print keywords
    print_keywords = ['GIVEYOU!', 'GIVEYOU!!']
    # Operator keywords
    operator_keywords = ['PLUS', 'MINUS', 'TIMES', 'DIVBY', 'MODU']
    # Error messages
    error_messages = {'SYNTAX_ERROR': "Syntax is incorrect.", 'BEGIN_ERROR': 'Input the BEGIN keyword to start.',
                      'INVALID_KW': 'is not a valid keyword.', 'INVALID_ASCII': 'is not a valid ASCII character.',
                      'INVALID_ASCIIS': 'are not valid ASCII characters.',
                      'INVALID_STRING': 'The argument is not a valid string.',
                      'INVALID_INTEGER': 'Invalid integer', 'INT_ARG_ERROR':' needs 2 arguments.',
                      'STR_ARG_ERROR':'The argument needs to be enclosed in quotation marks.',
                      'DQUOTE_ERROR':'The internal quote(s) needs to be escaped with a backslash.'}
    # Successful messages
    success_messages = {'WELCOME': 'INTERPOL Compiler', 'BEGIN_WARNING': 'Input CREATE to begin.',
                        'END_WARNING': 'Input RUPTURE to END.', 'BEGIN': 'Starting program',
                        'BEGIN_INPUT': 'Input syntax to check.', 'END': 'Ending program.',
                        'SYNTAX_CORRECT': 'The syntax is correct.'}
    try:
        # Display welcome message
        print("{0}\n{1} {2}".format(success_messages['WELCOME'], success_messages['BEGIN_WARNING'],
                                    success_messages['END_WARNING']))
        user_input_orig = input('$ ')
        user_input = clean_me_basic(user_input_orig)

        # Check if CREATE keyword has been inputted
        while user_input != "CREATE":
            print("{0}".format(success_messages['BEGIN_WARNING']))
            user_input_orig = input('$ ')
            user_input = clean_me_basic(user_input_orig)

        # Display begin message if passed the above loop
        print("{0}".format(success_messages['BEGIN']))
        user_input_orig = input('$ ')
        user_input = clean_me_basic(user_input_orig)
        user_input = get_string_wo_comments(user_input)
        user_input_list = user_input.split(" ")

        # Check if RUPTURE keyword has been inputted
        while user_input != "RUPTURE":

            # Check for invalid characters
            error_msg = check_invalid_chars(user_input_list)
            if error_msg != "":
                print(error_msg)
            else:
                # Check if the expression is a comment and has a valid keyword
                if (user_input_list[0][:1] == "#" or user_input_list[0] == "CREATE"
                    or user_input_list[0] == ''):
                    # This will do nothing and proceed with the next input
                    pass
                # Check if the expression has a valid keyword
                elif user_input_list[0] in keyword_list:

                    # Check if the expression is an operation
                    if user_input_list[0] in operator_keywords:
                        if len(user_input_list) == 3:
                            try:
                                #print(success_messages['SYNTAX_CORRECT'])
                                answer = 0
                                operator = user_input_list[0]
                                operand_1 = int(user_input_list[1])
                                operand_2 = int(user_input_list[2])

                                # Perform arithmetic operation
                                if operator == 'PLUS':
                                    answer = operand_1 + operand_2
                                elif operator == 'MINUS':
                                    answer = operand_1 - operand_2
                                elif operator == 'TIMES':
                                    answer = operand_1 * operand_2
                                elif operator == 'DIVBY':
                                    answer = operand_1 // operand_2
                                elif operator == 'MODU':
                                    answer = operand_1 % operand_2

                                print(str(int(answer)))

                            except ValueError:
                                # Operand(s) is invalid integer
                                print("{0}".format(error_messages['SYNTAX_ERROR']))
                            except Exception as e:
                                # Other arithmetic exceptions like OverflowError, ZeroDivisionError, FloatingPointError
                                #print("Error: Division by zero")
                                print("Error: {0}".format(str(e).capitalize()))
                        else:
                            print(error_messages['SYNTAX_ERROR'])
                            #print("{0}{1}".format(user_input_list[0],(error_messages['INT_ARG_ERROR'])))

                    # Check if the expression is a print
                    elif user_input_list[0] in print_keywords and len(user_input_list) > 1:

                        # Split the KW and argument
                        kw_len = len(user_input_list[0]) + 1
                        arguments = user_input[kw_len:]
                        word = arguments[1:-1]
                        doubleq_err_count = 0

                        # Check if the argument has " in the beginning and end
                        if arguments[0:1] == '"' and arguments[-1] == '"':

                            # Get the string using the original input
                            print_output = get_string(user_input_orig)

                            # Check if string has double quotes
                            if '"' not in word:
                                #print(success_messages['SYNTAX_CORRECT'])
                                if user_input_list[0] == 'GIVEYOU!!':
                                    print("{0}\n".format(print_output))
                                else:
                                    print(print_output)
                            else:
                                # Check if it has unescaped double quotes inside
                                for match in re.finditer('"', word):
                                    s = int(match.start())
                                    e = int(match.end())
                                    escape_char = word[s-1:e-1]

                                    # Find if it has \ before the "
                                    if s == 0:
                                        doubleq_err_count += 1
                                    elif escape_char != "\\":
                                        doubleq_err_count += 1
                                    else:
                                        continue
                                # If argument is with or without unescaped double quotes
                                if doubleq_err_count == 0:
                                    #print(success_messages['SYNTAX_CORRECT'])
                                    if user_input_list[0] == 'GIVEYOU!!':
                                        print("{0}\n".format(print_output))
                                    else:
                                        print(print_output)

                                else:
                                    print("{0}".format(error_messages['SYNTAX_ERROR']))
                                          #error_messages['DQUOTE_ERROR']))
                        else:
                            print("{0}".format(error_messages['SYNTAX_ERROR']))
                                #,error_messages['STR_ARG_ERROR']))
                    else:
                        print(error_messages['SYNTAX_ERROR'])

                # Catch all
                else:
                    print("{0}".format(error_messages['SYNTAX_ERROR']))
                    #,user_input_list[0],error_messages['INVALID_KW']))

            user_input_orig = input('$ ')
            user_input = clean_me_basic(user_input_orig)
            user_input = get_string_wo_comments(user_input)
            user_input_list = user_input.split(" ")

        # Proceed to exit program
        print("{0}".format(success_messages['END']))
    except:
        # Proceed to exit program
        print("\n{0}".format(success_messages['END']))

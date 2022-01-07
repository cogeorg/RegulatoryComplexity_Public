# -------------------------------------------------------------------------------
# clean_input_string
# -------------------------------------------------------------------------------
def clean_input_string(input_string):
    input_string = re.sub('\(', " ", input_string)
    input_string = re.sub('\)', " ", input_string)
    input_string = re.sub('\n', " ", input_string)
    input_string = re.sub(';', " ", input_string)
    for i in range(0,100):
        input_string = re.sub("  ", " ", input_string)

    input_string = re.sub('"', "", input_string)

    return input_string
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
#
# MAIN
#
# -------------------------------------------------------------------------------
if __name__=="__main__":
    import sys
    import re
    #
    # VARIABLES
    #
    OPERATORS = {'==', '=', 'lt1', 'g1', 'IF', 'THEN', 'ELSE', 'AND', 'OR'}
    _operators = {}
    _operands = {}

    #
    # CODE
    #
    input_file_name = sys.argv[1]
    input_file = open(input_file_name, "r")

    input_string = ""
    for line in input_file.readlines():
        input_string += line

    # clean and tokenize input string
    input_string = clean_input_string(input_string)
    tokens = input_string.split(" ")

    # loop over all tokens and compute stats
    for token in tokens:
        if token in OPERATORS:
            try:
                _operators[token] += 1
            except KeyError:
                _operators[token] = 1
        else:
            try:
                _operands[token] += 1
            except KeyError:
                _operands[token] = 1

    # write out resulting dictionaries
    out_text = ""
    for entry in _operators.keys():
        out_text += entry + ";" + str(_operators[entry]) + ";OPERATOR\n"
    for entry in _operands.keys():
        out_text += entry + ";" + str(_operands[entry]) + ";OPERAND\n"

    out_text2 = ""
    for entry in sorted(_operators.keys()):
        out_text2 +=  str(_operators[entry]) + "\t" + entry + "\n"
    for entry in sorted(_operands.keys()):
        out_text2 += str(_operands[entry]) + "\t" + entry + "\n"

    output_folder = sys.argv[2]
    output_file_name = output_folder + input_file_name.split("/")[-1].strip(".txt") + ".csv"
    output_file = open(output_file_name, "w")
    output_file.write(out_text)
    output_file.close()

    print(out_text2)

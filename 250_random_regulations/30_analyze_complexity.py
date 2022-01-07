# -------------------------------------------------------------------------------
# clean_input_string
# -------------------------------------------------------------------------------


def clean_input_string(input_string):
    input_string = re.sub('\(', " ", input_string)
    input_string = re.sub('\)', " ", input_string)
    input_string = re.sub('\n', " ", input_string)
    for i in range(0, 100):
        input_string = re.sub("  ", " ", input_string)

    input_string = re.sub('"', "", input_string)

    return input_string
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
#
# MAIN
#
# -------------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    import re
    #
    # VARIABLES
    #
    OPERATORS = []
    OPERANDS = []
    out_text = ""
    num_operators = 0
    num_operands =0
    num_unique_operators = 0
    num_unique_operands = 0
    total_volume = 0
    potential_volume = 0

    #
    # CODE
    #
    input_file_name = sys.argv[1]
    input_file = open(input_file_name, "r")
    identifier = input_file_name.split("/")[-1].strip(".csv")

    input_string = ""
    for line in input_file.readlines():
        tokens = line.split(";")

        if tokens[2].strip("\n") == "OPERATOR":
            OPERATORS.append(tokens[0])
            num_operators += int(tokens[1])
        elif tokens[2].strip("\n") == "OPERAND":
            OPERANDS.append(tokens[0])
            num_operands += int(tokens[1])
        else:
            print("ERROR")

    num_unique_operands = len(list(OPERANDS))
    num_unique_operators = len(list(OPERATORS))
    total_volume = num_operators + num_operands
    potential_volume = 2 + num_unique_operands
    level = potential_volume / float(total_volume)

    out_text = identifier + ";"+ str(num_operands) + ";" + str(num_unique_operands) + ";" + str(num_operators) + ";" + str(num_unique_operators) + ";" + \
        str(total_volume) + ";" + str(potential_volume) + ";" + str(level) + "\n"
    if False:
        print(out_text)
    
    # output
    output_folder = sys.argv[2]
    output_file_name = output_folder + \
        "result_" + identifier + ".csv"
    output_file = open(output_file_name, "w")
    output_file.write(out_text)
    output_file.close()

# -------------------------------------------------------------------------------
# COLORS FOR DEBUGGING
# -------------------------------------------------------------------------------
class bcolors:
    # HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    # BOLD = '\033[1m'
    # UNDERLINE = '\033[4m'
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# generate_statements()
# -------------------------------------------------------------------------------
def generate_statements(H, node, depth, current_path):
    DEBUG = False

    num_succ = len(list(H.successors(node)))

    if DEBUG:
        print("    ", node, list(H.successors(node)))

    # if the node has successors, append it to the current path and continue iteration
    if num_succ > 0:
        depth += 1
        current_path.append(node)
        # if the node we are at has several successors, allow for the possibility of OR
        for succ in H.successors(node):
            current_path.append(succ)
            generate_statements(H, succ, depth, current_path[0:depth])
    else:  # otherwise, generate text for current path and return to previous level
        # depth += 1 @TODO: probably not needed
        current_path.append(node)
        all_paths.append(current_path)
        return
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# reset_edge_weights()
# -------------------------------------------------------------------------------
def reset_edge_weights(G):
    for u, v in G.edges():
        G[u][v]['weight'] = 1.0
    return G
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# get_random_successor()
# -------------------------------------------------------------------------------
def get_random_successor(G, node):
    join_operator = ""
    random_successor = -1

    # number of possible conditionals to pick from
    _num_successors = len(list(G.successors(node))) # - 1
    _found_successor = None

    if _num_successors > 0:
        # pick random successor (but make sure it wasn't picked before)
        _count = 0
        while True:
            _count += 1
            random_successor = random.randint(0, _num_successors-1)
            _found_successor = list(G.successors(node))[random_successor]

            if G[node][_found_successor]['weight'] == 1.0:
                # one of two things can happen here:
                # - either the connection is an AND, in which case the weights
                #   of all edges emanating from node are set to zero
                # - or the connection is an OR, in which case only one
                #   edge weight is set to zero
                if random.uniform(0,1.0) > probability_and:  # use AND
                    join_operator = "AND"
                    _all_succ = list(G.successors(node))
                    for _to_node in _all_succ:  # set all edges to zero
                        G[node][_to_node]['weight'] = 0.0
                else:  # use OR
                    join_operator = "OR"
                    # set weight to zero
                    G[node][_found_successor]['weight'] = 0.0
                break

            if _count > 1000:
                join_operator = "XXX"
                break  # we did not find an unused random successor
    else:  # there is no successor
        join_operator = "XXX"

    # and return it
    return [join_operator, _found_successor]
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# generate_conditions()
# -------------------------------------------------------------------------------
def generate_conditions(H, num_conditions, num_conditionals):
    out_text = ""
    join_operator = ""  # not used for ASSET_CLASS conditions
    # generate num_conditions ASSET_CLASS == "XXXX" conditions
    for i in range(0, num_conditions):
        [join_operator, asset_successor] = get_random_successor(H, "ASSET_CLASS")
        out_text += "    ASSET_CLASS == '" + asset_successor + "'"

        if False:
            out_text += "\n"
            out_text += "    << DEBUG: " + str(num_conditionals) + ";" + asset_successor + ";" + \
                str(list(G.successors(asset_successor))) + "\n"

        #
        # now include conditionals
        #
        # we want to have num_conditionals conditionals, but might find fewer, this variable keeps track
        _found_conditionals = 0
        j = 0
        while _found_conditionals < num_conditionals:
            [join_operator, random_succ_conditional] = get_random_successor(H, asset_successor)
            if join_operator != "XXX":  # only if a conditional was found create it here
                _found_conditionals += 1
                if j == 0:  # first join operator is always an AND
                    join_operator = "AND"
                # construct out_text if we have a condition
                [join_operator2, random_succ_conditional2] = get_random_successor(H, random_succ_conditional)
                out_text += " " + join_operator + " ("  # open the AND or OR conditionals
                out_text += random_succ_conditional + " == '" + \
                    random_succ_conditional2 + "'"  # ignore the join operator
                out_text += ")"  # close the AND or OR conditionals

            # if we cannot find a conditional, break after 1000 tries
            j += 1
            if j == 100:
                out_text += "\n"
                return out_text


        if i < num_conditions-1:  # add an OR before the next condition
            out_text += " OR"
        out_text += "\n"
    return out_text
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# get_num_occurences(condition, conditions)
# -------------------------------------------------------------------------------
def get_num_occurences(condition, conditions):
    DEBUG = False
    num_occurrences = 0

    for element in conditions:
        if element == condition:
            num_occurrences += 1

    if DEBUG:
        print("    <<< WITHIN GET_NUM_OCCURENCES:", num_occurrences, condition, conditions)

    return num_occurrences
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# sanitize_token(token)
# -------------------------------------------------------------------------------
def sanitize_token(token):
    _ret = token
    _ret = re.sub("\)", "", _ret)
    _ret = re.sub("\(", "", _ret)
    _ret = re.sub(" OR", "", _ret)
    return _ret
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# tokenizer(line)
# -------------------------------------------------------------------------------
def tokenizer(line):
    DEBUG = False
    _ret = []

    # @TODO: the below is not perfect because it doesn't catch all possible duplicate
    # conditions, but should be fine for now;
    tokens = re.findall("\'(.*?)\'",line)
    if DEBUG:
        print("    <<<", tokens)

    for token in tokens:
        token = sanitize_token(token)  # remove extra characters
        if "AND" not in line:
            _ret.append(token)

    return _ret
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# clean_lines1(out_text, conditions)
# -------------------------------------------------------------------------------
def clean_lines1(out_text, conditions):
    DEBUG = False

    lines = out_text.split("\n")
    out_text_clean = ""

    if DEBUG:
        print("    <<< WITHIN CLEAN_LINES1")

    for line in lines:
        if DEBUG:
            print("      ", line)

        #
        # FIRST FIX: replace those placeholders for less than, greater than with human-readable text
        #
        line = re.sub("== 'g1'","> 1.0",line)
        line = re.sub("== 'lt1'","<= 1.0",line)

        #
        # SECOND FIX: avoid duplications of conditions
        # this fix is a bit more intricate and we only solve it in a very rough form
        # now, i.e. by dropping ELSE IF statements that duplicate
        #
        if "ASSET_CLASS" in line:
            tokens = tokenizer(line)
            if "AND" in line:  # if it is a composite condition, always add the line
                out_text_clean += line + "\n"
            else:  # we need to check whether we had the condition before
                condition = re.sub(" OR","", tokens[0])
                if condition != "":
                    # check if condition already exists
                    num_occurrences = get_num_occurences(condition, conditions)
                    if num_occurrences == 0:
                        # if not, add it to conditions and append line
                        conditions.append(condition)
                        out_text_clean += line + "\n"
        else:  # these are all other lines, we simply add them
            out_text_clean += line + "\n"

    return out_text_clean
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# clean_lines2(out_text)
# this procedure fixes things arising from dropping
# -------------------------------------------------------------------------------
def clean_lines2(out_text):
    DEBUG = False

    if DEBUG:
        print("    <<< WITHIN CLEAN_LINES2")

    # REPLACE TEXT
    out_text = re.sub("ELSE IF \(\n\) THEN:", "", out_text)
    out_text = re.sub("IF \(\n\) THEN:", "", out_text)
    out_text = re.sub("\n\n(.*risk_weight = \d.\d)", "", out_text)
    out_text = re.sub("OR\n\) THEN:","\n) THEN:", out_text)

    if DEBUG:
        lines = out_text.split("\n")
        for line in lines:
            print("      ", line)

    return out_text
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# clean_lines3(out_text)
# this procedure fixes text issues and makes the output more human readable
# -------------------------------------------------------------------------------
def clean_lines3(out_text):
    DEBUG = False

    if DEBUG:
        print("    <<< WITHIN CLEAN_LINES3")

    # REPLACE TEXT
    out_text = re.sub("and deducted from is", "deducted from", out_text)
    out_text = re.sub("or deducted from is", "or deducted from", out_text)
    out_text = re.sub("and collateralized is", "collateralized by", out_text)
    out_text = re.sub("or collateralized is", "or collateralized by", out_text)
    out_text = re.sub("and guaranteed is", "guaranteed by", out_text)
    out_text = re.sub("or guaranteed is", "or guaranteed by", out_text)
    out_text = re.sub("and asset maturity", "with asset maturity", out_text)
    out_text = re.sub("or asset maturity", "or with asset maturity", out_text)
    out_text = re.sub("and issuer is", "issued by", out_text)
    out_text = re.sub("or issuer is", "or issued by", out_text)
    out_text = re.sub("and funding currency", "where the funding currency", out_text)
    out_text = re.sub("or funding currency", "or where the funding currency", out_text)
    out_text = re.sub("and cash collection is", "where the cash collection is", out_text)
    out_text = re.sub("or cash collection is", "or where the cash collection is", out_text)
    out_text = re.sub("and denomination is", "where the denomination is", out_text)
    out_text = re.sub("or denomination is", "or where the denomination is", out_text)
    out_text = re.sub("and guaranteed Country is", "where the guaranteeing country is", out_text)
    out_text = re.sub("or guaranteed Country is", "or where the guaranteeing country is", out_text)
    out_text = re.sub("and property occupied is", "where the property is occupied by", out_text)
    out_text = re.sub("or property occupied is", "or where the property is occupied by", out_text)
    out_text = re.sub("and loan security is", "where the loan security is", out_text)
    out_text = re.sub("or loan security is", "or where the loan security is", out_text)
    out_text = re.sub("and issuer owner is", "where the issuer owner is", out_text)
    out_text = re.sub("or issuer owner is", "or where the issuer owner is", out_text)

    out_text = re.sub("where the issuer owner is public sector", "where the issuer is the public sector", out_text)
    out_text = re.sub("Loans where the property is occupied by rented", "Loans collateralized with mortgages where the property is occupied by a tenant", out_text)

    if DEBUG:
        lines = out_text.split("\n")
        for line in lines:
            print("      ", line)

    return out_text
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# clean_lines4(out_text)
# this procedure fixes text issues and makes the output more human readable
# -------------------------------------------------------------------------------
def clean_lines4(out_text, all_paths):
    DEBUG = 0
    asset_classes = []

    # START
    if DEBUG > 0:
        print("    <<< WITHIN CLEAN_LINES4")

    # # create list of all asset_classes to check if one of them appears more than once
    # for path in all_paths:
    #     if DEBUG > 2:
    #         print("      ", path)
    #     asset_classes.append(path[1])
    #
    # asset_classes_consolidated = set(asset_classes)
    # if DEBUG > 2:
    #     print("      ", asset_classes_consolidated)
    #
    # # REPLACE TEXT
    # # loop over all consolidated asset classes and see if one of them occurs more than once in the text
    # replacements = []
    # for asset in asset_classes_consolidated:
    #     # make sure to replace asset with the correct string
    #     asset = replace_text_in_lines(asset)
    #     # then replace
    #     replacements.append(("r'^(.*?(" + asset + ".*?){1})" + asset + "'","r'Other " + asset + "'"))
    #
    # for replacement in replacements:
    #     print(replacement[0], replacement[1])
    #     out_text = re.sub(replacement[0], replacement[1], out_text)

    # END
    if DEBUG > 0:
        lines = out_text.split("\n")
        for line in lines:
            print("      ", line)

    return out_text
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# clean_output()
# -------------------------------------------------------------------------------
def clean_output(out_text):
    DEBUG = False
    out_text_clean = ""
    conditions = []  # list of conditions we already covered

    out_text_clean = clean_lines1(out_text, conditions)
    if DEBUG:
        print(bcolors.OKGREEN + "  <<< CONDITIONS USED TO CLEAN UP TEXT" + bcolors.ENDC)
        print("    ",conditions, "\n")

    out_text_clean = clean_lines2(out_text_clean)

    if DEBUG:
        print(bcolors.OKGREEN + "  <<< AFTER CLEANING OF OUT_TEXT" + bcolors.ENDC)
        lines = out_text.split("\n")
        for line in lines:
            print("    ", line)

    return out_text_clean
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# read_input_file(input_file_name, G)
# -------------------------------------------------------------------------------
def read_input_file(input_file_name, G):
    is_from = False         # used in generating graph representing cases

    input_file = open(input_file_name, 'r')

    for line in input_file.readlines():  # parse input file
        if line.strip() != "":
            if is_from:
                if "}" in line:  # stop adding links
                    is_from = False
                else:
                	items = line.strip().split(",")
                	# print(from_node, items)
                	to_node = items[0]
                	_weight = float(items[1])
                	# print from_node, items, "XXX", to_node, weight
                	to_node = re.sub(r',', "", to_node)
                	to_node = re.sub(r"'", "", to_node)
                	# print from_node, to_node, "XXXX", to_node.split(',')[0]
                	G.add_edge(from_node, to_node, weight=_weight)
            if "{" in line:  # we have a new from node
                is_from = True
                tokens = line.split("=")
                from_node = tokens[0].strip()
    input_file.close()
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# replace_text_in_lines(line)
# -------------------------------------------------------------------------------
def replace_text_in_lines(line):
    cleaned_line = line

    # cleaned_line = re.sub("", "", cleaned_line)
    cleaned_line = re.sub("cash", "Cash", cleaned_line)
    cleaned_line = re.sub("claim", "Claims", cleaned_line)
    cleaned_line = re.sub("loan", "Loans", cleaned_line)
    cleaned_line = re.sub("fixed_asset", "Fixed Asset", cleaned_line)
    cleaned_line = re.sub("real_estate", "Real Estate", cleaned_line)
    cleaned_line = re.sub("other_investment", "Other Investment", cleaned_line)
    cleaned_line = re.sub("capital_instrument", "Capital Instrument", cleaned_line)

    cleaned_line = re.sub("CASH_COLLECTION", "cash collection", cleaned_line)
    cleaned_line = re.sub("ISSUER_COUNTRY", "issuer country", cleaned_line)
    cleaned_line = re.sub("ISSUER_OWNER", "issuer owner", cleaned_line)
    cleaned_line = re.sub("ISSUER", "issuer", cleaned_line)
    cleaned_line = re.sub("DENOMINATION", "denomination", cleaned_line)
    cleaned_line = re.sub("FUNDING_CURRENCY", "funding currency", cleaned_line)
    cleaned_line = re.sub("COLLATERALIZED", "collateralized", cleaned_line)
    cleaned_line = re.sub("GUARANTEED_COUNTRY", "guaranteed Country", cleaned_line)
    cleaned_line = re.sub("GUARANTEED", "guaranteed", cleaned_line)
    cleaned_line = re.sub("ASSET_MATURITY", "asset maturity", cleaned_line)
    cleaned_line = re.sub("LOAN_SECURITY", "loan security", cleaned_line)
    cleaned_line = re.sub("PROPERTY_OCCUPIED", "property occupied", cleaned_line)
    cleaned_line = re.sub("DEDUCTED_FROM", "deducted from", cleaned_line)

    cleaned_line = re.sub("ASSET_CLASS ==","", cleaned_line)
    cleaned_line = re.sub("'","", cleaned_line)
    cleaned_line = re.sub("OR"," or ", cleaned_line)
    cleaned_line = re.sub("AND \("," and ", cleaned_line)
    cleaned_line = re.sub("\)"," ", cleaned_line)
    cleaned_line = re.sub("\("," ", cleaned_line)
    cleaned_line = re.sub(" == "," is ", cleaned_line)

    cleaned_line = re.sub("> 1.0"," more than one year", cleaned_line)
    cleaned_line = re.sub("<= 1.0"," less than one year", cleaned_line)


    # remove extra whitespaces
    cleaned_line = re.sub("     "," ", cleaned_line)
    cleaned_line = re.sub("    "," ", cleaned_line)
    cleaned_line = re.sub("   "," ", cleaned_line)
    cleaned_line = re.sub("  "," ", cleaned_line)
    return cleaned_line
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# gen_tex_output(out_text)
# -------------------------------------------------------------------------------
def gen_tex_output(out_text, all_paths):

    counter = 1  # used to number conditions
    tmp_output = ""

    tex_output = """
\\documentclass{article}
\\begin{document}
\\setlength{\\parindent}{0em}
\\begin{center}{\\bf Risk weights by category of on-balance-sheet asset}\\end{center}
~\\\\
~\\\\

"""
    lines = out_text.split("\n")

    tmp_output = ""
    for line in lines:
        # append lines to tmp_output, which can be cleaned further
        if "ASSET_CLASS" in line:
            # substitute text in lines
            tmp_output += "(" + str(counter) + ")" + replace_text_in_lines(line) + "\\\\\n"
            counter += 1
        if "ELSE:" in line:
            tmp_output += "All other assets:\\\\\n"
        if "risk_weight" in line:
            risk_weight = line.split(" = ")[1]
            tmp_output += "Risk weight = " + str(100*float(risk_weight)) + "%\\\\ \n\n"
            tmp_output += "~\\\\\n"

    tex_output += tmp_output
    tex_output += "\\end{document}\n"

    tex_output = clean_lines3(tex_output)
    tex_output = clean_lines4(tex_output, all_paths) # NOT DEBUGGED

    return tex_output
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
#
# MAIN
#
# -------------------------------------------------------------------------------
if __name__=="__main__":
    DEBUG_LEVEL = 5  # granularity of debugging, low means granular
    import sys
    import random
    import networkx as nx
    from random import randint
    from pathlib import Path
    import re


    #
    # VARIABLE DEFINITIONS
    #
    max_conditions = 6      # the maximum number of conditions inside an IF clause
    max_conditionals = 5    # the maximum number of additional conditionals combined by OR
    num_elseif = 4          # Basel I has 4, but maybe we want to construct more complicated structures
    global probability_and  # probability to get an AND (vs. OR)
    probability_and = 0.5   # TODO: at some point this should be changed to an environment class


    #
    # CODE
    #
    input_file_name = sys.argv[1]
    output_directory = sys.argv[2]
    out_text = ""
    out_text_tex = ""

    print(bcolors.OKGREEN + "<<< START" + bcolors.ENDC)
    #
    # generate graph reprepsenting possible cases in the regulation
    #
    G = nx.DiGraph()
    read_input_file(input_file_name, G)  # populate G

    if DEBUG_LEVEL < 2:
        for u,v,edata in G.edges(data=True):
        	print(u,v,edata)

    #
    # generate statements from network
    #
    current_path = []
    all_paths = []

    G = reset_edge_weights(G)  # TODO: generate weights from G graph
    if  DEBUG_LEVEL < 2:
        for u,v,edata in G.edges(data=True):
        	print("    ", u,v,edata)
        print("<<< AFTER reset_edge_weights(G)")

    # then, populate all paths from the graph recursively, starting at depth 0
    generate_statements(G, "ASSET_CLASS", 0, current_path)
    if DEBUG_LEVEL < 3:
        print("  <<< AFTER generate_statements(G, 'ASSET_CLASS', 0, [])")
        for path in all_paths:
        	print("    ", path)

    #
    # generate IF THEN ELSE clauses
    #
    out_text = "IF (\n"

    #
    # structure is always:
    # ASSET_CLASS == "" OR ASSET_CLASS == "" AND ()
    #
    # random number of possible conditions for ASSET_CLASS
    num_conditions = random.randint(1, max_conditions)
    # random number of conditionals within each condition, joint with AND with condition and with
    # OR among themselves
    num_conditionals = random.randint(0, max_conditionals)
    if DEBUG_LEVEL < 3:
        print("  <<< BEFORE generate_conditions(G, ", num_conditions, ",", num_conditionals,")")

    out_text += generate_conditions(G, num_conditions, num_conditionals)

    if DEBUG_LEVEL < 3:
        print("  <<< AFTER generate_conditions(G, num_conditions, num_conditionals)")

    out_text += ") THEN:\n"
    out_text += "    risk_weight = 0.0\n\n"

    #
    # NOW LOOP OVER ELSE IF STATEMENTS
    #
    for i in range(0,num_elseif):
        out_text += "ELSE IF (\n"  # same as above
        num_conditions = random.randint(1, max_conditions)  # these are random for every ELSE IF
        num_conditionals = random.randint(0, max_conditionals)
        out_text += generate_conditions(G, num_conditions, num_conditionals)
        out_text += ") THEN:\n"
        out_text += "    risk_weight = 0." + str(random.randint(0,9)) + "\n\n"

    #
    # AND CLOSE WITH ELSE STATEMENT
    #
    out_text += "ELSE:\n"
    out_text += "    risk_weight = 1.0\n"

    #
    # POST RUN CLEANUP
    #
    if DEBUG_LEVEL < 4:
        print(bcolors.OKGREEN + "  <<< CLEANING OUT_TEXT" + bcolors.ENDC)
        for line in out_text.split("\n"):
            print("    " + line)

    out_text = clean_output(out_text)

    #
    # CREATE LATEX OUTPUT
    #
    out_text_tex = gen_tex_output(out_text, all_paths)
    if DEBUG_LEVEL < 5:
        print(bcolors.OKGREEN + "  <<< CREATING LATEX OUT_TEXT" + bcolors.ENDC)
        for line in out_text_tex.split("\n"):
            print("    ", line)

    #
    # WRITE OUT FILES
    #
    _count = 0
    while True:
        _count += 1  # just to have a limit on the number of tries to write a file

        identifier = randint(0, 100000000000000)

        out_file_name = output_directory + re.sub('.txt', "", input_file_name) + \
            "-" + str(identifier) + ".gexf"
        txt_out_file_name = re.sub('.gexf', '.txt', out_file_name)
        tex_out_file_name = re.sub('.gexf', '.tex', out_file_name)

        _check_file = Path(out_file_name)
        if not _check_file.is_file():
            # file does not yet exist, write to it
            print(bcolors.OKGREEN + "  <<< WRITING TO:")
            print(bcolors.WARNING + "    " + out_file_name)
            print("    " + txt_out_file_name)
            print("    " + tex_out_file_name + bcolors.ENDC)
            # write graph
            nx.write_gexf(G, out_file_name)
            # write text file
            output_file = open(txt_out_file_name, "w")
            output_file.write(out_text)
            output_file.close()
            # write tex file
            output_file = open(tex_out_file_name, "w")
            output_file.write(out_text_tex)
            output_file.close()

            break
        if _count > 100:
            print(bcolors.ERROR + "  <<< ERROR: unable to write file", out_file_name + bcolors.ENDC)
            break

    print(bcolors.OKGREEN + ">>> END" + bcolors.ENDC)

# -------------------------------------------------------------------------------
# END
# -------------------------------------------------------------------------------

#!/usr/local/bin/python
import docker
import sys
import getopt
import re
import ast
# lists for comparison
expected_list = []
found_list = []
info_level = 1

# print message
def print_this(mystring, level):
    global info_level
    if info_level >= 2 and level == 2:
        print "DEBUG: " + str(mystring)
    elif info_level >= 1 and level == 1:
        print "INFO: " + str(mystring)

# read in parameters
def main(argv):
    global info_level
    image_name = ''
    inspect_file = ''
    usage = 'image_inspector.py -i <image_name> -f <inspect_file> [-d]'
    try:
        opts, args = getopt.getopt(argv,"hi:f:d",["iname=","fname"])
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        elif opt in ("-i", "--iname"):
            image_name = arg
        elif opt in ("-f", "--ifile"):
            inspect_file = arg
        elif opt == '-d':
            info_level = 2
    if not image_name:
        print usage
        sys.exit(2)
    elif not inspect_file:
        print usage
        sys.exit(2)
    else:
        print_this("Image name is: " + image_name, 2)
        print_this("Inspect file is: " + inspect_file, 2)
        docker_inspect(image_name, inspect_file)

# process the inspection
def docker_inspect(myimage, myfile):
    # connect to the docker daemon
    cli = docker.Client(base_url='unix://var/run/docker.sock', tls=True)
    # collect inspect data for image
    data_dict = cli.inspect_image(myimage)
    # read in the expected inspect data from text file into string
    expected_string = read_file(myfile)
    # convert the string to dictionary
    expected_dict = ast.literal_eval(expected_string)
    # inspect the dictionary objects
    inspect_dict(expected_dict, data_dict, 'Root')
    # compare the inspect data
    global expected_list
    global found_list
    compare_lists(expected_list, found_list)

# read in text file
def read_file(thisfile):
    mystring=""
    with open(thisfile) as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        # find 'key: value' pairs
        if re.match( r'(.*): (.*)', line, re.M|re.I):
            key = line.split(': ')[0]
            value = line.split(': ')[1]
            # any values not inside double quotes
            if not re.match( r'^"(.*)",$', value, re.M|re.I):
                # remove any ending comma
                new_value = value.rstrip(',')
                # check we are dealing with a value and not brackets
                if re.match( r'^[a-zA-Z0-9]*$', new_value, re.M|re.I):
                    # turn 'true' to 'True' and 'false' to 'False'
                    if new_value == "true":
                        new_value = "True"
                    elif new_value == "false":
                        new_value = "False"
                    elif new_value == "null":
                        new_value = "None"
                    new_value = "\"" + new_value + "\""
                    new_line = key + ": " + new_value + ","
                    mystring = mystring + new_line + '\n'
                else:
                    mystring = mystring + line + '\n'
            else:
                mystring = mystring + line + '\n'
        else:
            mystring = mystring + line + '\n'
    return mystring

# inspect dictionary
def inspect_dict(e, d, p):
    global expected_list
    global found_list
    print_this("Starting dictionary inspection...", 2)
    for k, v in e.iteritems():
        if k in d:
            if isinstance(v, dict) and v:
                p2 = p + "-" + k
                d2 = d[k]
                big_dictionary_inspection(e[k], d[k], p2)
                inspect_dict(v, d2, p2)
            elif isinstance(v, list):
                p2 = p + "-" + k
                d2 = d[k]
                inspect_array(v, d2, p2)
            else:
                print_this("Exp: " + str(p) + "-{0}={1}".format(k, v), 2)
                print_this("Fnd: " + str(p) + "-" + str(k) + "=" + str(d[k]), 2)
                expected_string = str(p) + "-{0}={1}".format(k, v)
                found_string = str(p) + "-" + str(k) + "=" + str(d[k])
                expected_list.append(expected_string)
                found_list.append(found_string)
        else:
            print_this("Skipping item: " + k + " this should have been reported as missing from the new docker images already!", 1)

# compare two dictionaries
def big_dictionary_inspection(de, dd, dp):
    print_this("Exp: dictionary size is: " + str(len(de)), 2)
    print_this("Fnd: dictionary size is: " + str(len(dd)), 2)
    if len(de) > len(dd):
        for k, v in de.iteritems():
            if not k in dd:
                print_this("WARNING - missing item in new docker image: " + str(dp) + "-" + str(k) + "-" + str(v), 1)
    elif len(de) < len(dd):
        for k, v in dd.iteritems():
            if not k in de:
                print_this("INFO - additional item found in new docker image: " + str(dp) + "-" + str(k) + "-" + str(v), 1)

# inspect array
def inspect_array(ae, ad, ap):
    print_this("Starting array inspection...", 2)
    print_this("Exp: array size is: " + str(len(ae)), 2)
    print_this("Fnd: array size is: " + str(len(ad)), 2)
    if len(ae) == len(ad):
        print_this("Array sizes match.", 2)
        big_array_inspection(ae, "Exp", ad, str(ap))
        big_array_inspection(ad, "Fnd", ae, str(ap))
    elif len(ae) > len(ad):
        print_this("Array size does not match, searching for extra array element...", 2)
        big_array_inspection(ae, "Exp", ad, str(ap))
    elif len(ae) < len(ad):
        print_this("Array size does not match, searching for extra array element...", 2)
        big_array_inspection(ad, "Fnd", ae, str(ap))

# compare two lists
def compare_lists(el, dl):
    print_this("Starting list comparison...", 2)
    for i in range(len(el)):
        if not el[i] == dl[i]:
            print_this("ERROR - values do not match:\n" + str(el[i]) + "\n" + str(dl[i]), 1)
        else:
            print_this("MATCH:\n" + str(el[i]) + "\n" + str(dl[i]), 2)

# inspect array bae for additional elements
def big_array_inspection(a1, stringI, a2, stringP):
    global expected_list
    global found_list
    a1_dict = {}
    a2_dict = {}
    for i in range(len(a1)):
        a1_dict[str(a1[i])] = ''
    for j in range(len(a2)):
        a2_dict[str(a2[j])] = ''  
    for k, v in a1_dict.iteritems():
        if k in a2_dict:
            print_this("Exp: " + stringP + "-" + k, 2)
            print_this("Fnd: " + stringP + "-" + k, 2)
            expected_string = stringP + "-" + k
            found_string = stringP + "-" + k
            expected_list.append(expected_string)
            found_list.append(found_string)
        else:
            if stringI == "Exp":
                print_this("WARNING - missing item in new docker image: " + stringP + "-" + k, 1) 
            elif stringI == "Fnd":
                print_this("WARNING - additional item found in new docker image: " + stringP + "-" + k, 1)

# start here
if __name__ == "__main__":
    main(sys.argv[1:])

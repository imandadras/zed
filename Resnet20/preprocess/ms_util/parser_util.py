def check_options(choice,options):
    if choice==None:
        return 
    if choice in options:
        return True
    else:
        print("Choice {} is not in the list:".format(choice))
        raise ValueError

def print_list(options):
    for l in options:
        print("\t- {}".format(l))
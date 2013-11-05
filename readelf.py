import os
import sys
import getopt
import os.path
import elfutils


def print_usage():
    print("usage: readelf exectuable")
    exit(2)


def print_dynamic(elf):
    dynamic = elf["dynamic"] 
    for entry in dynamic:
        tag = elfutils.dynamic_type[entry.keys()[0]]
        value = entry.values()[0]
        if isinstance(value, str):
            print "{:<20}{:<30}".format(tag, value)
        else:
            print "{:<20}{:<16}".format(tag, hex(value))

def print_symbol(elf):
    symtabs = elf["symtabs"]
    for symtab in symtabs:
        print "in", symtab
        print "{:<15}{:<10}{:<10}{:<10}{:<20}".format("addr", "type", "visiblity", "bind", "name")
        for symbol in symtabs[symtab]:
            value = hex(symbol["value"])
            name = symbol["name"]
            sym_type = elfutils.sym_type[symbol["type"]].split("_")[-1]
            bind_type = elfutils.sym_bind_type[symbol["bind"]].split("_")[-1] 
            vis_type =  elfutils.sym_vis_type[symbol["vis"]].split("_")[-1] 
            print "{:<15}{:<10}{:<10}{:<10}{:<20}".format(value, sym_type, vis_type, bind_type, name)
        print "\n"

def print_pheader(elf):
    pass
def print_sheader(elf):
    pass
def print_header(elf):
    pass

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dhlsS")
    except getopt.GetoptError, err:        
        print str(err)
        print_usage() 
    if len(args) == 0:
        print_usage()
    path = args[0]
    if not os.path.exists(path):
        print_usage()
    header = False
    dynamic = False
    pheader = False
    sheader =False
    symbol = False 
    for o, a in opts:
        if o == "--help":
            print_usage()
        elif o == "-d":
            dynamic = True
        elif o == "-h":  
            header = True
        elif o == "-l":
            pheader = True
        elif o == "-s":
            symbol = True
        elif o == "-S":
            sheader = True 
        else:
            assert False, "unhandled options"
    elf = elfutils.set_target(path)    
    if dynamic:
        print_dynamic(elf)
    if header:
        print_header(elf)
    if pheader:
        print_pheader(elf)
    if sheader:
        print_sheader(elf)
    if symbol:
        print_symbol(elf)
if __name__ == "__main__":
    main()

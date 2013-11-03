import getopt
import elfutils

if __name__ == "__main__":
    import sys
    if sys.argv < 2:
        print "error"
        exit(0)
    binfile = open(sys.argv[1], "r")
    elf = elfutils.set_target(binfile)
    symtabs = elf["symtabs"] 
    for symtab in symtabs:    
        print "in",symtab 
        for symbol in symtabs[symtab]: 
            print "{:<15}{:<40} {:<3}".format(hex(symbol["value"]), symbol["name"], elfutils.sym_vis_type[symbol["vis"]])
        print "\n"
    dynamic = elf["dynamic"]
    for entry in dynamic:
        d_tag = elfutils.dynamic_type[entry.keys()[0]] 
        value = entry.values()[0]
        if isinstance(value, str): 
            print "{:<20}{:<30}".format(d_tag, value)     
        else:
            print "{:<20}{:<15}".format(d_tag, hex(value))

#! /usr/bin/env python
import os
import sys 
import getopt 
import os.path
import elfutils
#import cProfile


def print_usage():
    print("usage: readelf.py [option] exectuable")
    print """Options are:
    -d Display the dynamic section (if present)
    -h Display the ELF file header
    -l Display the program headers
    -r Display the relocations (if present)
    -S Display the section's header
    -s Display the symbol table 
    """
    exit(2)


def print_dynamic(elf):
    dynamic = elf["dynamic"] 
    strtypes = [elfutils.DT_NEEDED, elfutils.DT_SONAME, elfutils.DT_RPATH]
    for entry in dynamic: 
        tag = entry.keys()[0]
        value = entry.values()[0]
        if tag in strtypes:
            tag = elfutils.dynamic_type[tag]
            print "{:<20}{:<30}".format(tag, value)
        elif tag == elfutils.DT_FLAGS: 
            tag = elfutils.dynamic_type[tag] 
            print "{:<20}{:<30}".format(tag, elfutils.DT_FLAGS_type[value])
        elif tag == elfutils.DT_FLAGS_1: 
            tag = elfutils.dynamic_type[tag] 
            print "{:<20}{:<30}".format(tag, elfutils.DT_FLAGS_1_type[value])
        else:
            tag = elfutils.dynamic_type[tag]
            print "{:<20}{:<16}".format(tag, hex(value))

def print_symbol(elf):
    symtabs = elf["symtabs"]
    of = "{:<15}{:<10}{:<10}{:<10}{:<20}"
    NAME, BIND, TYPE, VIS, INDEX, VALUE, SIZE = range(7)
    type_table = elfutils.sym_type 
    bind_type_table = elfutils.sym_bind_type
    vis_type_table = elfutils.sym_vis_type
    pdb.set_trace()
    for symtab in symtabs:
        print "in", symtab
        print of.format("addr", "type", "visiblity", "bind", "name")
        for symbol in symtabs[symtab]:
            value = hex(symbol[VALUE])
            name = symbol[NAME]
            sym_type = type_table[symbol[TYPE]].split("_")[-1] 
            bind_type = bind_type_table[symbol[BIND]].split("_")[-1] 
            vis_type =  vis_type_table[symbol[VIS]].split("_")[-1] 
            print of.format(value, sym_type, vis_type, bind_type, name)
        print "\n"

def print_pheader(elf):
    pheader = elf['programs']
    of = "{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<5}" 
    print of.format("Type", "Align", "Offset", "VirtAddr", "PhysAddr", "FileSize", "MemSize", "Flags")
    for entry in pheader:
        try:
            ptype = elfutils.ph_type[entry['type']].split("_")[-1]
        except:
            pdb.set_trace()
        flag = elfutils.ph_flags[entry['flags']]
        offset = hex(entry['offset'])
        virt = hex(entry['virt'])
        phys = hex(entry['phys'])
        filesize = hex(entry['filesize'])
        memsize = hex(entry['memsize'])
        align = hex(entry['align'])
        print of.format(ptype, align, offset, virt, phys, filesize, memsize, flag)
    if elf['interpreter']:
        print "INTERP: ", elf['interpreter']
    print "\n"

def print_sheader(elf):
    sections = elf['sections']
    of = "{:<20}{:<15}{:<10}{:<10}\n\t\t{:<10}{:<10}{:<10}{:<5}{:<5}{:<20}"
    print of.format("Name", "Type", "Addr", "Offset", "Size", "Link", "Info", "Align", "Entsize", "Flag",) 
    for entry in sections:
        name = entry['name']
        type = elfutils.sh_type[entry['type']]
        flag = elfutils.decide_shflags(entry['flag'])
        addr = hex(entry['addr'])
        offset = hex(entry['offset'])
        size = hex(entry['size'])
        link = hex(entry['link'])
        info = hex(entry['info'])
        align = hex(entry['align'])
        entsize = hex(entry['entsize'])
        print of.format(name, type, addr, offset, size, link, info, align, entsize,  flag)
    print "\n"

def print_header(elf):
    header = elf['elf_header']
    print "in elf header:"
    of = "{:<30}{:<20}"
    print of.format("file ident:", elfutils.elf_class_type[header['file_class']]) 
    print of.format("file encoding:", elfutils.elf_encoding[header['file_encoding']])
    print of.format("file version:", header['file_version'])
    print of.format("elf type:", elfutils.elf_type[header['e_type']])
    print of.format("elf machine type:", elfutils.elf_arch_type[header['e_machine']])
    print of.format("elf version:", header['e_version'])
    print of.format("elf entry:", hex(header['e_entry']))
    print of.format("program header offset:", hex(header['e_phoff']))
    print of.format("section header offset:", hex(header['e_shoff']))
    print of.format("elf flags:", header['e_flags'])
    print of.format("elf header size:", header['e_ehsize'])
    print of.format("program entry size:", header['e_phentsize'])
    print of.format("program entry number:", header['e_phnum'])
    print of.format("section entry size:", header['e_shentsize'])
    print of.format("section entry number:", header['e_shnum'])
    print of.format("index of .strtab:", header['e_shstrndx'])
    
def print_rela(elf):
    symtab = elf["symtabs"][".dynsym"] 
    rel_type = elfutils.rel_type
    if "rel" in elf:
        of = "{:<15}{:<20}{:<10}{:<10}" 
        for name, rel in elf["rel"].iteritems(): 
            print "in", name
            print of.format("offset", "type", "Sym.Index",  "Sym.Name") 
            for item in rel: 
                print of.format(hex(item[0]), rel_type[item[2]],
                        item[1], symtab[item[1]][0])
    if "rela" in elf:       
        of = "{:<10}{:<15}{:<10}{:<10}{:<10}" 
        for name, rela in elf["rela"].iteritems(): 
            print "in", name 
            print of.format("offset", "type", "Addend",
                    "Sym.Index", "Sym.Name") 
            for item in rela: 
                print of.format(hex(item[0]), rel_type[item[2]],
                        item[3], item[1], symtab[item[1]][0]) 

def print_dwarf_info(elf):
    pass


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dhlrsSw:")
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
    dwarf_info = False
    rela = False
    flags = 0
    for o, a in opts:
        if o == "--help":
            print_usage()
        elif o == "-d":
            dynamic = True
            flags |= elfutils.ELF_DYNAMIC
        elif o == "-h":  
            header = True
        elif o == "-l":
            pheader = True
        elif o == "-s":
            symbol = True
            flags |= elfutils.ELF_SYMBOL
        elif o == "-S":
            sheader = True 
        elif o == "-w":
            if a == "i":
                dwarf_info = True 
                flags |= elfutils.DWARF_INFO
        elif o == "-r":
            rela = True
            flags |= elfutils.ELF_RELA
        else:
            assert False, "unhandled options" 
    #cProfile.runctx("elfutils.set_target(path)", globals(), locals(), "readelf.trace")    
    elf = elfutils.set_target(path, flags)
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
    if rela: 
        print_rela(elf)
    if dwarf_info: 
        print_dwarf_info(elf)

if __name__ == "__main__":
    main()

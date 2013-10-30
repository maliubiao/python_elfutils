import cStringIO
from baseutils import strtoint

elf = {
    "elf_header": {},
    "sections": [],
    "programs": [], 
    "strtabs": {},
    "symtabs": {}
    }

section_header = {
        "index": 0,
        "name": "",
        "type": "",
        "address": 0,
        "offset": 0,
        "size": 0,
        "entsize": 0,
        "flags": "",
        "link": "",
        "info": "",
        "align": 0
        }

sh_type = {
        0: "SHT_NULL",
        1: "SHT_PROGBITS",
        2: "SHT_SYMTAB",
        3: "SHT_STRTAB",
        4: "SHT_RELA",
        5: "SHT_HASH",
        6: "SHT_DYNAMIC",
        7: "SHT_NOTE",
        8: "SHT_NOBITS",
        9: "SHT_REL",
        10: "SHT_SHLIB",
        11: "SHT_DYNSYM"
        }

sh_flags = {
        1: "SHF_WRITE",
        2: "SHF_ALLOC",
        4: "SHF_EXECINSTR"
        }

program_header = {
        "type": "",
        "offset": 0,
        "virtaddr": 0,
        "physaddr": 0,
        "filesize": 0,
        "memsize": 0,
        "flags": "",
        "align": 0
        }

ph_type = {
        0: "PT_NULL",
        1: "PT_LOAD",
        2: "PT_DYNMAIC",
        3: "PT_INTERP",
        4: "PT_NOTE",
        5: "PT_SHLIB",
        6: "PT_PHDR"
        }

ph_flags = {
        0: "NULL",
        1: "PF_X",
        2: "PF_W",
        3: "PF_W + PF_X",
        4: "PF_R",
        5: "PF_R + PF_X",
        6: "PF_R + PF_W",
        7: "PF_R + PF_W + PF_X"
        }

dynamic_type = {
        0: "DT_NULL",
        1: "DT_NEEDED",
        2: "DT_PLTRELSZ",
        3: "DT_PLTGOT",
        4: "DT_HASH",
        5: "DT_STRTAB",
        6: "DT_SYMTAB",
        7: "DT_RELA",
        8: "DT_RELASZ",
        9: "DT_RELAENT",
        10: "DT_STRSZ",
        11: "DT_SYMENT",
        12: "DT_INIT",
        13: "DT_FINI",
        14: "DT_SONAME",
        15: "DT_RPATH",
        16: "DT_SYMBOLIC",
        17: "DT_REL",
        18: "DT_RELSZ",
        19: "DT_RELENT",
        20: "DT_PLTREL",
        21: "DT_DEBUG",
        22: "DT_TEXTREL",
        23: "DT_JMPREL",
        24: "DT_BIND_NOW"
        }

rel_type = {
        0: "R_386_NONE",
        1: "R_386_32",
        2: "R_386_PC32",
        3: "R_386_GOT32",
        4: "R_386_PLT32",
        5: "R_386_COPY",
        6: "R_386_GLOB_DAT",
        7: "R_386_JMP_SLOT",
        8: "R_386_RELATIVE",
        9: "R_386_GOTOFF",
        10: "R_386_GOTPC"
        }

def read_header(buffer):
    buffer.seek(0)
    elf_header = elf['elf_header']
    elf_header["file_ident"] = buffer.read(4)
    assert elf_header["file_ident"] == "\x7fELF"
    elf_header["file_class"] = strtoint(buffer.read(1))
    elf_header["file_encoding"] = strtoint(buffer.read(1))
    elf_header["file_version"] = strtoint(buffer.read(1))
    #ignore 9 chars
    buffer.read(9) 
    elf_header["e_type"] = strtoint(buffer.read(2))
    elf_header["e_machine"] = strtoint(buffer.read(2))
    elf_header["e_version"] = strtoint(buffer.read(4))
    elf_header["e_entry"] = strtoint(buffer.read(8))
    elf_header["e_phoff"] = strtoint(buffer.read(8))
    elf_header["e_shoff"] = strtoint(buffer.read(8))
    elf_header["e_flags"] = strtoint(buffer.read(4))
    elf_header["e_ehsize"] = strtoint(buffer.read(2))
    elf_header["e_phentsize"] = strtoint(buffer.read(2))
    elf_header["e_phnum"] = strtoint(buffer.read(2))
    elf_header["e_shentsize"] = strtoint(buffer.read(2))
    elf_header["e_shnum"] = strtoint(buffer.read(2))
    elf_header["e_shstrndx"] = strtoint(buffer.read(2))

def read_section_header(buffer):
    elf_header = elf["elf_header"]
    sections = elf["sections"]
    e_shoff = elf_header["e_shoff"]
    buffer.seek(e_shoff)
    e_shnum = elf_header["e_shnum"]
    e_shentsize = elf_header["e_shentsize"] 
    for num in range(e_shnum):    
        sections.append({
            "name": strtoint(buffer.read(4)),
            "type": strtoint(buffer.read(4)),
            "flag": strtoint(buffer.read(8)),
            "addr": strtoint(buffer.read(8)),
            "offset": strtoint(buffer.read(8)),
            "size": strtoint(buffer.read(8)),
            "link": strtoint(buffer.read(4)),
            "info": strtoint(buffer.read(4)),
            "align": strtoint(buffer.read(8)),
            "entsize": strtoint(buffer.read(8))
        })


def read_program_header(buffer):
    elf_header = elf["elf_header"]
    programs = elf["programs"] 
    buffer.seek(elf_header["e_phoff"])
    e_phnum = elf_header["e_phnum"] 
    e_phentsize = elf_header["e_phentsize"]
    for num in range(e_phnum):
        programs.append({
            "type": strtoint(buffer.read(4)),
            "flag": strtoint(buffer.read(4)),
            "offset": strtoint(buffer.read(8)),
            "virt": strtoint(buffer.read(8)),
            "phys": strtoint(buffer.read(8)),
            "filesize": strtoint(buffer.read(8)),
            "memsize": strtoint(buffer.read(8)),
            "align": strtoint(buffer.read(8))
            })


def build_strtab(buffer, section):
    buffer.seek(section["offset"])        
    size = section["size"]
    strtabdata = buffer.read(size) 
    strtab = {}
    j = 0
    while j < size:
        if strtabdata[j] == "\x00":
            end = strtabdata.find("\x00", j+1) 
            if end == -1:
                break
            name = strtabdata[j+1:end]
            more = name.find(".", 1)
            if more > 0: 
                strtab[j+more+1] = name[more:]
            strtab[j+1] = name 
            j = end
            continue
        j += 1 
    return strtab

def search_sections(key, value):
    pocket = []
    sections = elf["sections"]
    for section in sections:
        if section[key] == value:
            pocket.append(section)
    return pocket

def read_strtab(buffer): 
    elf_header = elf["elf_header"] 
    sections = elf["sections"]
    strtab_sections = []
    for section in sections:
        if section["type"] == 3:
            strtab_sections.append(section) 
    shstrtab_section = None
    for section in strtab_sections:
        buffer.seek(section["offset"])
        if ".text" in buffer.read(section["size"]):
            shstrtab_section = section 
    if not shstrtab_section:
        print "error: where is .shstrtab?"
        return
    shstrtab = build_strtab(buffer, shstrtab_section)    
    for section in sections[1:]:
        section["name"] = shstrtab[section["name"]]
    for section in strtab_sections:    
        if section["name"] == ".shstrtab":
            continue
        strtab = build_strtab(buffer, section)
        elf["strtabs"][section["name"]] = strtab

def read_symtab(buffer):
    sections = elf["sections"]
    symtabs = elf["symtabs"]
    symtab_sections = []
    for section in sections:
        if section["type"] == 2:
            symtab_sections.append(section) 
        if section["type"] == 11:
            symtab_sections.append(section)
    for section in symtab_sections: 
        buffer.seek(section["offset"])
        extra = section["align"] - (section["entsize"] / section["align"]) 
        total = section["size"] / section["entsize"]
        symtab = []
        for entry in range(total): 
            name = strtoint(buffer.read(4))
            info = strtoint(buffer.read(1))
            _bind = info >> 4
            _type = info & 0xf
            symtab.append({
                "name": name,
                "bind": _bind,
                "type": _type,
                "vis": strtoint(buffer.read(1)),
                "index": strtoint(buffer.read(2)),
                "value": strtoint(buffer.read(8)),
                "size": strtoint(buffer.read(8))
                })
        symtabs[section["name"]] = symtab                     
    if ".symtab" in elf["symtabs"]:
        strtab = elf["strtabs"][".strtab"]
        for symbol in elf["symtabs"][".symtab"]:
            if symbol["name"]:
                symbol["name"] = strtab[symbol["name"]] 
        dynsym = elf["strtabs"][".dynstr"]
        for symbol in elf["symtabs"][".dynsym"]:
            if symbol["name"]:
                symbol["name"] = dynsym[symbol["name"]]

def read_rela(buffer):
    pass


if __name__ == "__main__":
    import sys
    if sys.argv < 2:
        print "error"
        exit(0)
    binfile = open(sys.argv[1], "r")
    read_header(binfile) 
    read_section_header(binfile)
    read_program_header(binfile)
    read_strtab(binfile) 
    read_symtab(binfile) 
    symtabs = elf["symtabs"] 
    for symtab in symtabs:    
        print "in",symtab 
        for symbol in symtabs[symtab]: 
            print hex(symbol["value"]),"\t",symbol["name"] 
        print "\n"

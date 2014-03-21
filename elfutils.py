import os 
import mmap 
import io 
import pdb
from cStringIO import StringIO
from baseutils import string_to_unsigned
from baseutils import string_to_signed

elf = None
_read = None

#options 
ELF_HEADER = 1 << 2
ELF_SYMBOL = 1 << 3
ELF_DYNAMIC = 1 << 4
ELF_RELA = 1 << 5
ELF_PSECTION = 1 << 6
DWARF_INFO = 1 << 10 


#types
ELF64 = 8
ELF32 = 4
ELF16 = 2
ELF8 = 1


Elf32_Ehdr = {
    "e_ident": ELF8,
    "e_type": ELF16,
    "e_machine": ELF16,
    "e_version": ELF32,
    "e_entry": ELF32,
    "e_phoff": ELF32,
    "e_shoff": ELF32,
    "e_flags": ELF32,
    "e_ehsize": ELF16,
    "e_phentsize": ELF16,
    "e_phnum": ELF16,
    "e_shentsize": ELF16,
    "e_shnum": ELF16,
    "e_shstrndx": ELF16
    }

Elf64_Ehdr = {
        "e_ident": ELF8,
        "e_type": ELF16,
        "e_machine": ELF16,
        "e_version": ELF32,
        "e_entry": ELF64,
        "e_phoff": ELF64,
        "e_shoff": ELF64,
        "e_flags": ELF32,
        "e_ehsize": ELF16,
        "e_phentsize": ELF16,
        "e_phnum": ELF16,
        "e_shentsize": ELF16,
        "e_shnum": ELF16,
        "e_shstrndx": ELF16
        }
        

Elf32_Shdr = {
        "sh_name": ELF32,
        "sh_type": ELF32,
        "sh_flags": ELF32,
        "sh_addr": ELF32,
        "sh_offset": ELF32,
        "sh_size": ELF32,
        "sh_link": ELF32,
        "sh_info": ELF32,
        "sh_addralign": ELF32,
        "sh_entsize": ELF32
        }

Elf64_Shdr = {
        "sh_name": ELF32,
        "sh_type": ELF32,
        "sh_flags": ELF64,
        "sh_addr": ELF64,
        "sh_offset": ELF64,
        "sh_size": ELF64,
        "sh_link": ELF32,
        "sh_info": ELF32,
        "sh_addralign": ELF64,
        "sh_entsize": ELF64
        }

Elf32_Phdr = {
        "p_type": ELF32,
        "p_offset": ELF32,
        "p_vaddr": ELF32,
        "p_paddr": ELF32,
        "p_filesz": ELF32,
        "p_memsz": ELF32,
        "p_flags": ELF32,
        "p_align": ELF32
        }

Elf64_Phdr = {
        "p_type": ELF32,
        "p_flags": ELF32,
        "p_offset": ELF64,
        "p_vaddr": ELF64,
        "p_paddr": ELF64,
        "p_filesz": ELF64,
        "p_memsz": ELF64,
        "p_align": ELF64
        }


HIGHBITMASK = 0b1111111
LOWBITSHIFT = 7
ELFSIG = "\x7fELF"

EM_NONE = 0
EM_386 = 3
EM_X86_64 = 62

elf_arch_type = {
        0: "EM_NONE",
        3: "EM_386",
        62: "EM_X86_64"
        }
        
ELFDATANONE = 0
ELFDATA2LSB = 1
ELFDATA2MSB = 2

elf_encoding = {
        0: "ELFDATANONE",
        1: "ELFDATA2LSB",
        2: "ELFDATA2MSB"
        }

ELFCLASSNONE = 0
ELFCLASS32 = 1
ELFCLASS64 = 2

elf_class_type = {
        0: "ELFCLASSNONE",
        1: "ELFCLASS32",
        2: "ELFCLASS64"
        }

ET_NONE = 0
ET_REL = 1
ET_EXEC = 2
ET_DYN = 3
ET_CORE = 4

elf_type = {
        0: "ET_NONE",
        1: "ET_REL",
        2: "ET_EXEC",
        3: "ET_DYN",
        4: "ET_CORE"
        }

SHT_NULL = 0
SHT_PROGBITS = 1
SHT_SYMTAB = 2
SHT_STRTAB = 3
SHT_RELA = 4
SHT_HASH = 5
SHT_DYNAMIC = 6
SHT_NOTE = 7
SHT_NOBITS = 8
SHT_REL = 9
SHT_SHLIB = 10
SHT_DYNSYM = 11
SHT_INIT_ARRAY = 14
SHT_FINI_ARRAY = 15
SHT_PREINIT_ARRAY = 16
SHT_GROUP = 17
SHT_SYMTAB_SHNDX = 18
SHT_LOOS = 0x60000000 
SHT_GNU_INCREMENTAL_INPUTS = 0x6fff4700
SHT_GNU_ATTRIBUTES = 0x6ffffff5
SHT_GNU_HASH = 0x6ffffff6
SHT_GNU_LIBLIST = 0x6ffffff7
SHT_GNU_verdef = 0x6ffffffd
SHT_GNU_verneed = 0x6ffffffe
SHT_GNU_versym = 0x6fffffff

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
        11: "SHT_DYNSYM",
        14: "SHT_INIT_ARRAY",
        15: "SHT_FINI_ARRAY",
        16: "SHT_PREINIT_ARRAY",
        17: "SHT_GROUP",
        18: "SHT_SYMTAB_SHNDX",
        0x60000000: "SHT_LOOS", 
        0x6fff4700: "SHT_GNU_INCREMENTAL_INPUTS",
        0x6ffffff5: "SHT_GNU_ATTRIBUTES",
        0x6ffffff6: "SHT_GNU_HASH",
        0x6ffffff7: "SHT_GNU_LIBLIST",
        0x6ffffffd: "SHT_GNU_verdef",
        0x6ffffffe: "SHT_GNU_verneed",
        0x6fffffff: "SHT_GNU_versym"
        }

SHF_NONE = 0
SHF_ALLOC = 1 << 0
SHF_EXECINSTR = 1<< 2
SHF_MERGE = 1 << 4
SHF_STRINGS = 1 << 5
SHF_INFO_LINK = 1 << 6
SHF_LINK_ORDER = 1 << 7
SHF_OS_NONCONFORMING = 1 << 8 
SHF_GROUP = 1 << 9 
SHF_TLS = 1 << 10
SHF_MASKOS = 0x0ff00000
SHF_MASKPROC = 0xf0000000
SHF_EXCLUDE = 0x80000000

sh_flags = {
        0: "SHF_NONE",
        1 << 0: "SHF_WRITE",
        1 << 1: "SHF_ALLOC",
        1 << 2: "SHF_EXECINSTR",
        1 << 4: "SHF_MERGE",
        1 << 5: "SHF_STRINGS",
        1 << 6: "SHF_INFO_LINK",
        1 << 7: "SHF_LINK_ORDER",
        1 << 8: "SHF_OS_NONCONFORMING",
        1 << 9: "SHF_GROUP",
        1 << 10: "SHF_TLS",
        0x0ff00000: "SHF_MASKOS",
        0xf0000000: "SHF_MASKPROC", 
        0x80000000: "SHF_EXCLUDE"
        }


def decide_shflags(flag):
    t = []
    for key in sh_flags:
        if flag & key:
            t.append(sh_flags[key])
    return "+".join(t)

PT_NULL = 0
PT_LOAD = 1
PT_DYNMAIC = 2
PT_INTERP = 3
PT_NOTE = 4
PT_SHLIB = 5
PT_PHDR = 6
PT_TLS = 7
PT_LOOS = 0x60000000
PT_HIOS = 0x6fffffff
PT_LOPROC = 0x70000000
PT_HIPROC = 0x7fffffff
PT_GNU_EH_FRAME = 0x6474e550
PT_GNU_STACK = 0x6474e551
PT_GNU_RELRO = 0x6474e552

ph_type = {
        0: "PT_NULL",
        1: "PT_LOAD",
        2: "PT_DYNMAIC",
        3: "PT_INTERP",
        4: "PT_NOTE",
        5: "PT_SHLIB",
        6: "PT_PHDR",
        7: "PT_TLS",
        0x60000000: "PT_LOOS",
        0x6fffffff: "PT_HIOS",
        0x70000000: "PT_LOPROC",
        0x7fffffff: "PT_HIPROC",
        0x6474e550: "PT_GNU_EH_FRAME",
        0x6474e551: "PT_GNU_STACK",
        0x6474e552: "PT_GNU_RELRO"
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

DT_NEEDED = 1
DT_SONAME = 14
DT_RPATH = 15
DT_FLAGS = 30
DT_FLAGS_1 = 0x6ffffffb

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
        24: "DT_BIND_NOW",
        25: "DT_INIT_ARRAY",
        26: "DT_FINI_ARRAY",
        27: "DT_INIT_ARRAYSZ",
        28: "DT_FINI_ARRAYSZ",
        29: "DT_RUNPATH",
        30: "DT_FLAGS",
        31: "DT_ENCODING",
        32: "DT_PREINIT_ARRAY",
        33: "DT_PREINIT_ARRAYSZ",
        0x6000000d: "DT_LOOS",
        0x6ffff000: "DT_HIOS",
        0x70000000: "DT_LOPROC",
        0x7fffffff: "DT_HIPROC",
        0x6ffffd00: "DT_VALRNGLO",
        0x6ffffdf5: "DT_GNU_PRELINKED",
        0x6ffffdf6: "DT_GNU_CONFLICTSZ",
        0x6ffffdf7: "DT_GNU_LIBLISTSZ",
        0x6ffffdf8: "DT_CHECKSUM",
        0x6ffffdf9: "DT_PLTPADSZ",
        0x6ffffdfa: "DT_MOVEENT",
        0x6ffffdfb: "DT_MOVESZ",
        0x6ffffdfc: "DT_FEATURE",
        0x6ffffdfd: "DT_POSFLAG_1",
        0x6ffffdfe: "DT_SYMINSZ",
        0x6ffffdff: "DT_SYMINENT", 
        0x6ffffe00: "DT_ADDRRNGLO",
        0x6ffffef5: "DT_GNU_HASH",
        0x6ffffef6: "DT_TLSDESC_PLT",
        0x6ffffef7: "DT_TLSDESC_GOT",
        0x6ffffef8: "DT_GNU_CONFLICT",
        0x6ffffef9: "DT_GNU_LIBLIST",
        0x6ffffefa: "DT_CONFIG",
        0x6ffffefb: "DT_DEPAUDIT",
        0x6ffffefc: "DT_AUDIT",
        0x6ffffefd: "DT_PLTPAD",
        0x6ffffefe: "DT_MOVETAB",
        0x6ffffeff: "DT_SYMINFO",
        0x6ffffff9: "DT_RELACOUNT",
        0x6ffffffa: "DT_RELCOUNT",
        0x6ffffffb: "DT_FLAGS_1",
        0x6ffffffc: "DT_VERDEF",
        0x6ffffffd: "DT_VERDEFNUM",
        0x6ffffffe: "DT_VERNEED",
        0x6fffffff: "DT_VERNEEDNUM",
        0x6ffffff0: "DT_VERSYM"
        }

DT_FLAGS_type = {
        1 << 0: "DF_ORIGIN",
        1 << 1: "DF_SYMBOLIC",
        1 << 2: "DF_TEXTREL",
        1 << 3: "DF_BIND_NOW",
        1 << 4: "DF_STATIC_TLS"
        }

DT_FLAGS_1_type = {
        0x1: "DT_1_NOW",
        0x2: "DT_1_GLOBAL",
        0x4: "DT_1_GROUP",
        0x8: "DT_1_NODELETE",
        0x10: "DT_1_LOADFLTR",
        0x20: "DT_1_INITFIRST",
        0x40: "DT_1_NOOPEN",
        0x80: "DT_1_ORIGIN",
        0x100: "DT_1_DIRECT",
        0x200: "DT_1_TRANS",
        0x400: "DT_1_INTERPOSE",
        0x800: "DT_1_NODEFLIB",
        0x1000: "DT_1_NODUMP",
        0x2000: "DT_1_CONLFAT"
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

sym_type = {
        0: "STT_NOTYPE",
        1: "STT_OBJECT",
        2: "STT_FUNC",
        3: "STT_SECTION",
        4: "STT_FILE",
        5: "STT_COMMON",
        6: "STT_TLS",
        8: "STT_RELC",
        9: "STT_SRELC",
        10: "STT_LOOS",
        12: "STT_HIOS",
        13: "STT_LOPROC",
        15: "STT_HIPROC"
        } 

sym_bind_type = {
        0: "STB_LOCAL", 
        1: "STB_GLOBAL",
        2: "STB_WEAK",
        10: "STB_UNIQUE"
        } 

sym_spec_index = {
        0: "SHN_UNDEF", 
        0xff00: "SHN_LOPROC",
        0xff1f: "SHN_HIPROC",
        0xfff1: "SHN_ABS",
        0xfff2: "SHN_COMMON",
        0xffff: "HIRESERVE"
        }

sym_vis_type = {
        0: "STV_DEFAULT",
        1: "STV_INTERNAL",
        2: "STV_HIDDEN",
        3: "STV_PROTECTED"
        } 

def print_mem_usage(position): 
    Mib = 1024
    pagesize = 4
    f = open("/proc/%d/statm" % os.getpid(), "r")
    mems = f.read().split(" ")
    print "in", position    
    print "VM: %dm PHYM: %dm" % (int(mems[0]) * pagesize / Mib,
            int(mems[1]) * pagesize / Mib)              
    f.close()

def read_header(buffer):
    buffer.seek(0)
    elf_header = elf['elf_header']
    elf_header["file_ident"] = _read(ELF32)
    assert elf_header["file_ident"] == ELFSIG
    file_class = string_to_unsigned(_read(ELF8)) 
    if file_class == ELFCLASS32:
        ehdr = Elf32_Ehdr
    elif file_class == ELFCLASS64:
        ehdr = Elf64_Ehdr
    else:
        raise Exception("Unknown ELFCLASS: %d", file_class)
    elf_header["file_class"] = file_class
    elf_header["file_encoding"] = string_to_unsigned(_read(ELF8))
    elf_header["file_version"] = string_to_unsigned(_read(ELF8)) 
    #ignore 9 bytes
    buffer.seek(9, io.SEEK_CUR)
    elf_header["e_type"] = string_to_unsigned(_read(ehdr["e_type"]))
    elf_header["e_machine"] = string_to_unsigned(_read(ehdr["e_machine"]))
    elf_header["e_version"] = string_to_unsigned(_read(ehdr["e_version"]))
    elf_header["e_entry"] = string_to_unsigned(_read(ehdr["e_entry"]))
    elf_header["e_phoff"] = string_to_unsigned(_read(ehdr["e_phoff"]))
    elf_header["e_shoff"] = string_to_unsigned(_read(ehdr["e_shoff"]))
    elf_header["e_flags"] = string_to_unsigned(_read(ehdr["e_flags"]))
    elf_header["e_ehsize"] = string_to_unsigned(_read(ehdr["e_ehsize"]))
    elf_header["e_phentsize"] = string_to_unsigned(_read(ehdr["e_phentsize"]))
    elf_header["e_phnum"] = string_to_unsigned(_read(ehdr["e_phnum"]))
    elf_header["e_shentsize"] = string_to_unsigned(_read(ehdr["e_shentsize"]))
    elf_header["e_shnum"] = string_to_unsigned(_read(ehdr["e_shnum"]))
    elf_header["e_shstrndx"] = string_to_unsigned(_read(ehdr["e_shstrndx"]))

def read_section_header(buffer):
    elf_header = elf["elf_header"]
    sections = elf["sections"]
    e_shoff = elf_header["e_shoff"]
    buffer.seek(e_shoff)
    e_shnum = elf_header["e_shnum"]
    e_shentsize = elf_header["e_shentsize"] 
    if elf_header["file_class"] == ELFCLASS32:
        shdr = Elf32_Shdr
    else:
        shdr = Elf64_Shdr 
    for num in range(e_shnum):    
        sections.append({
            "name": string_to_unsigned(_read(shdr["sh_name"])),
            "type": string_to_unsigned(_read(shdr["sh_type"])),
            "flag": string_to_unsigned(_read(shdr["sh_flags"])),
            "addr": string_to_unsigned(_read(shdr["sh_addr"])),
            "offset": string_to_unsigned(_read(shdr["sh_offset"])),
            "size": string_to_unsigned(_read(shdr["sh_size"])),
            "link": string_to_unsigned(_read(shdr["sh_link"])),
            "info": string_to_unsigned(_read(shdr["sh_info"])),
            "align": string_to_unsigned(_read(shdr["sh_addralign"])),
            "entsize": string_to_unsigned(_read(shdr["sh_entsize"]))
        })


def read_program_header(buffer):
    elf_header = elf["elf_header"]
    programs = elf["programs"] 
    buffer.seek(elf_header["e_phoff"])
    e_phnum = elf_header["e_phnum"] 
    e_phentsize = elf_header["e_phentsize"]
    if elf_header["file_class"] == ELFCLASS32:
        phdr = Elf32_Phdr
    else:
        phdr = Elf64_Phdr 
    elf_type = elf_header["file_class"]
    for num in range(e_phnum):
        p_type = string_to_unsigned(_read(phdr["p_type"])) 
        if elf_type == ELFCLASS64: 
            p_flags = string_to_unsigned(_read(phdr["p_flags"]))
        p_offset = string_to_unsigned(_read(phdr["p_offset"]))
        p_vaddr = string_to_unsigned(_read(phdr["p_vaddr"]))
        p_paddr = string_to_unsigned(_read(phdr["p_paddr"]))
        p_filesz = string_to_unsigned(_read(phdr["p_filesz"]))
        p_memsz = string_to_unsigned(_read(phdr["p_memsz"]))
        if elf_type == ELFCLASS32:
            p_flags = string_to_unsigned(_read(phdr["p_flags"]))
        p_align = string_to_unsigned(_read(phdr["p_align"]));
        entry = {
            "type": p_type,
            "flags": p_flags,
            "offset": p_offset,
            "virt": p_vaddr,
            "phys": p_paddr,
            "filesize": p_filesz,
            "memsize": p_memsz,
            "align": p_align
            }
        #INTERP
        if entry['type'] == PT_INTERP:
            mark = buffer.tell() 
            buffer.seek(entry['offset'])
            elf['interpreter'] = _read(entry['filesize']) 
            buffer.seek(mark)
        programs.append(entry)


def build_strtab(buffer, section): 
    buffer.seek(section["offset"])        
    size = section["size"] 
    data = _read(size) 
    strtab = {}
    j = 0
    strend = "\x00"
    while j < size:
        if data[j] != strend: 
            j += 1 
            continue 
        k = j + 1
        end = data.find(strend, k) 
        if end == -1: 
            break
        name = data[k:end]
        more = name.find(".", 1)
        if more > 0: 
            strtab[k+more] = name[more:]
        strtab[k] = name 
        j = end
    return strtab


def read_strtab(buffer): 
    elf_header = elf["elf_header"] 
    sections = elf["sections"]
    strtab_sections = []
    for section in sections:
        if section["type"] == SHT_STRTAB:
            strtab_sections.append(section) 
    shstrtab_section = None
    for section in strtab_sections:
        buffer.seek(section["offset"])
        if ".text" in _read(section["size"]):
            shstrtab_section = section 
    if not shstrtab_section:
        print "error: where is .shstrtab?"
        return
 
    shstrtab = build_strtab(buffer, shstrtab_section)    
    for section in sections[1:]:
        section["name"] = shstrtab[section["name"]]
    for section in strtab_sections:    
        name = section["name"]
        if name == ".shstrtab":
            continue
        strtab = build_strtab(buffer, section)
        elf["strtabs"][name] = strtab

def read_symtab(buffer): 
    sections = elf["sections"]
    symtabs = elf["symtabs"]
    symtab_sections = [] 
    try:
        strtab = elf["strtabs"][".strtab"]
    except:
        strtab = None
    dynsym = elf["strtabs"][".dynstr"]
    for section in sections:
        if section["type"] == SHT_SYMTAB:
            symtab_sections.append(section) 
        if section["type"] == SHT_DYNSYM:
            symtab_sections.append(section)
    #use local alias
    sym_read = _read
    elf_type = elf["elf_header"]["file_class"]
    for section in symtab_sections: 
        buffer.seek(section["offset"]) 
        extra = section["align"] - (section["entsize"] / section["align"]) 
        total = section["size"] / section["entsize"]
        symtab = []
        symtab_append = symtab.append 
        section_name = section["name"]
        for entry in range(total): 
            sym_name = string_to_unsigned(_read(ELF32)) 
            if not sym_name:
                sym_name = "unknown"
            elif section_name == ".symtab":
                try:
                    sym_name = strtab[sym_name]
                except KeyError:
                    pass
            elif section_name == ".dynsym": 
                try:
                    sym_name = dynsym[sym_name] 
                except KeyError:
                    pass
            if not sym_name:
                continue
            #name ,bind , type, vis, index, value, size
            if elf_type == ELFCLASS32:
                st_value = string_to_unsigned(sym_read(ELF32))
                st_size = string_to_unsigned(sym_read(ELF32))
                st_info = string_to_unsigned(sym_read(ELF8))
                st_other = string_to_unsigned(sym_read(ELF8))
                st_shndx = string_to_unsigned(sym_read(ELF16))
                symtab_append((sym_name, st_info >> 4,  st_info & 0xf,
                    st_other, st_shndx, st_value, st_size))
            else:
                st_info = string_to_unsigned(sym_read(ELF8)) 
                symtab_append((sym_name, st_info >> 4,
                    st_info & 0xf,
                    string_to_unsigned(sym_read(ELF8)), 
                    string_to_unsigned(sym_read(ELF16)), 
                    string_to_unsigned(sym_read(ELF64)), 
                    string_to_unsigned(sym_read(ELF64))
                    ))

        symtabs[section["name"]] = symtab                     
        #sym_data.close() 

def read_rela(buffer):
    sections = elf["sections"] 
    rel_list = []
    for section in sections:
        if section["type"] == SHT_REL:
            rel_list.append(section) 
    elf_type = elf["elf_header"]["file_class"]
    symtab = elf["symtabs"][".dynsym"]
    elf["rel"] = {}
    for rel in rel_list:
        r1_list = []
        buffer.seek(rel["offset"])
        if elf_type == ELFCLASS32:
            for i in range(rel["size"] / rel["entsize"]):
                r_offset = string_to_unsigned(_read(ELF32))
                r_info = string_to_unsigned(_read(ELF32))
                r1_list.append((r_offset, r_info >> 8, r_info & 0xff))
        else:
            for i in range(rel["size"] / rel["entsize"]):
                r_offset = string_to_unsigned(_read(ELF64))
                r_info = string_to_unsigned(_read(ELF64))
                r1_list.append((r_offset, r_info >> 32,
                    r_info & 0xffffffff))
        elf["rel"][rel["name"]] = r1_list
    if not elf["rel"]:
        del elf["rel"]
    
    rela_list = []
    for section in sections:
        if section["type"] == SHT_RELA:
            rela_list.append(section) 
    elf["rela"] = {}
    for rela in rela_list:
        r2_list = []
        buffer.seek(rela["offset"])
        if elf_type == ELFCLASS32:
            for i in range(rela["size"] / rela["entsize"]):
                r_offset = string_to_unsigned(_read(ELF32))
                r_info = string_to_unsigned(_read(ELF32))
                r_addend = string_to_signed(_read(ELF32))
                r2_list.append((r_offset, r_info >> 8,
                    r_info & 0xff, r_addend))
        else:
            for i in range(rela["size"] / rela["entsize"]):
                r_offset = string_to_unsigned(_read(ELF64))
                r_info = string_to_unsigned(_read(ELF64))
                r_addend = string_to_signed(_read(ELF64))
                r2_list.append((r_offset, r_info >> 32,
                    r_info & 0xffffffff, r_addend)) 
        elf["rela"][rela["name"]] = r2_list
    if not elf["rela"]:
        del elf["rela"]        
    

def read_dynamic(buffer): 
    sections = elf["sections"]
    dynamic = None
    for section in sections:
        if section["type"] == SHT_DYNAMIC:
            dynamic = section            
    dynamic_list = elf["dynamic"]
    buffer.seek(dynamic["offset"])
    total = dynamic["size"] / dynamic["entsize"] 
    if elf["elf_header"]["file_class"] == ELFCLASS32: 
        for entry in range(total):
            d_tag = string_to_signed(_read(ELF32))
            value = string_to_unsigned(_read(ELF32)) 
            dynamic_list.append({d_tag: value})    
            if not d_tag:
                break
    else:
        for entry in range(total):
            d_tag = string_to_signed(_read(ELF64))
            value = string_to_unsigned(_read(ELF64)) 
            dynamic_list.append({d_tag: value})    
            if not d_tag:
                break

    in_symtab = [DT_NEEDED, DT_SONAME, DT_RPATH]     
    strtabs = elf["strtabs"]
    strtab = {}
    dyntab = {}
    if ".strtab" in strtabs:
        strtab = strtabs[".strtab"]
    if ".dynstr" in strtabs: 
        dyntab = strtabs[".dynstr"]
    for entry in dynamic_list: 
        d_tag = entry.keys()[0]
        if d_tag in in_symtab:
            if not d_tag:
                continue
            value = entry[d_tag]
            if not value:
                continue 
            if value in strtab:
                name = strtab[value]
            elif value in dyntab:
                name = dyntab[value]
            entry[d_tag] = name 


def read_versym(buffer): 
    sections = elf["sections"]
    versym = None
    for section in sections: 
        if section["type"] == SHT_GNU_versym:
            versym = section            
            break     
    if not versym:
        raise Exception("No section gnu.version")
    #seek and read
    buffer.seek(versym["offset"])
    total = versym["size"] / versym["entsize"] 
    verlist = []
    for entry in range(total):
        verlist.append(string_to_unsigned(buffer.read(2)))
    return verlist 

def read_verneed(buffer): 
    sections = elf["sections"]
    verneed = None
    for section in sections: 
        if section["type"] == SHT_GNU_versym:
            verneed = section            
            break     
    if not verneed:
        raise Exception("No section gnu.version")
    buffer.seek(verneed["offset"])     
    total = versym["size"] / versym["entsize"]
    deflist = []
    pdb.set_trace()
    for entry in range(total):
        vn_version = string_to_unsigned(buffer.read(2))
        vn_cnt = string_to_unsigned(buffer.read(2))
        vn_file = string_to_unsigned(buffer.read(4)) 
        vn_aux = string_to_unsigned(buffer.read(4))
        vn_next = string_to_unsigned(buffer.read(4))
        deflist.append({
            "version": vn_version,
            "cnt": vn_cnt,
            "file": vn_file,
            "aux": vn_aux,
            "next": vn_next
            })

def read_section(buffer, name): 
    sections = elf["sections"]
    target = None
    for section in sections: 
        if section["name"] == name:
            target = section            
            break     
    if not target:
        raise Exception("No section %s" % target)
    buffer.seek(target["offset"])
    elf["target"] = buffer.read(target["size"])

def has_sections(debug_list, section_names):
    ret = True
    for d in debug_list:
        if d not in section_names:
            ret = False
            break 
    return ret

def get_sections(name_list, sections):
    ret_list = []
    section_names = [x["name"] for x in sections] 
    for name in name_list:
        ret_list.append(sections[section_names.index(name)])
    return ret_list


def read_debugabbr(buffer):
    sections = elf["sections"]
    debug_abbr = ".debug_abbrev"
    if debug_abbr not in sections:
        assert False, "where is the section .debug_abbrev?"
    debug_abbr = sections[".debug_abbrev"]
    buffer.seek(debug_abbr["offset"])
 
def set_target(path, flags, *args): 
    flags |= ELF_HEADER 
    if flags & ELF_RELA:
        flags |= ELF_SYMBOL
    if flags & ELF_DYNAMIC:
        flags |= ELF_SYMBOL
    global elf 
    global _read
    elf = {
        "elf_header": {},
        "sections": [],
        "programs": [], 
        "interpreter": "",
        "strtabs": {},
        "symtabs": {},
        "dynamic": [],
        "compile_units": [],
        "target": None
        } 
    f = open(path, "rb")
    buffer = mmap.mmap(f.fileno(), 0, mmap.MAP_PRIVATE, mmap.PROT_READ)
    _read = buffer.read
    if flags & ELF_HEADER:
        read_header(buffer) 
        read_section_header(buffer)
        read_program_header(buffer) 
        read_strtab(buffer) 
    if flags & ELF_SYMBOL: 
        read_symtab(buffer) 
    if flags & ELF_DYNAMIC: 
        read_dynamic(buffer) 
    if flags & ELF_RELA:
        read_rela(buffer)
    if flags & DWARF_INFO: 
        read_debuginfo(buffer) 
    if flags & ELF_PSECTION:
        read_section(buffer, args[1])
    buffer.close()
    f.close()
    return elf

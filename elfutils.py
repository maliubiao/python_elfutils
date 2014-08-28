#-*-encoding=utf-8-*-
import os 
import mmap 
import io 
import pdb
import dwarf
import struct
from cStringIO import StringIO 


"""
去掉baseutils
参考golang, elfutils重新设计接口
提高struct的使用效率
解释清楚ELF标准里每个的用途
完全支持elf标准里的各种计算 
支持读取与生成
支持dwarf调试信息的读取与生成
"""

elf = None 

#options 
ELF_HEADER = 1 << 2
ELF_SYMBOL = 1 << 3
ELF_DYNAMIC = 1 << 4
ELF_RELA = 1 << 5
ELF_PSECTION = 1 << 6
ELF_VERNEED = 1 << 7
DWARF_INFO = 1 << 10 


#types
ELF64 = 8
ELF32 = 4
ELF16 = 2
ELF8 = 1


def load_struct(buffer, d, fmt): 
    fmt_str = "".join([x[1] for x in fmt])
    size = struct.calcsize(fmt_str)
    raw = buffer.read(size) 
    if len(raw) != size:
        raise Exception("Truncated Stream")
    unpacked_raw = struct.unpack(fmt_str, raw)
    for i, m in enumerate(fmt): 
        d[m[0]] = unpacked_raw[i]


elf32_hdr_format = (
        ("e_type", "H"),
        ("e_machine", "H"),
        ("e_version", "I"),
        ("e_entry", "I"),
        ("e_phoff", "I"),
        ("e_shoff", "I"),
        ("e_flags", "I"),
        ("e_ehsize", "H"),
        ("e_phentsize", "H"),
        ("e_phnum", "H"),
        ("e_shentsize", "H"),
        ("e_shnum", "H"),
        ("e_shstrndx", "H")
        )

elf64_hdr_format = (
        ("e_type", "H"),
        ("e_machine", "H"),
        ("e_version", "I"),
        ("e_entry", "Q"),
        ("e_phoff", "Q"),
        ("e_shoff", "Q"),
        ("e_flags", "I"),
        ("e_ehsize", "H"),
        ("e_phentsize", "H"),
        ("e_phnum", "H"),
        ("e_shentsize", "H"),
        ("e_shnum", "H"),
        ("e_shstrndx", "H")
        )

elf32_shdr_format = (
        ("sh_name", "I"),
        ("sh_type", "I"),
        ("sh_flags", "I"),
        ("sh_addr", "I"),
        ("sh_offset", "I"),
        ("sh_size", "I"),
        ("sh_link", "I"),
        ("sh_info", "I"),
        ("sh_addralign", "I"),
        ("sh_entsize", "I")
        )

elf64_shdr_format = (
        ("sh_name", "I"),
        ("sh_type", "I"),
        ("sh_flags", "Q"),
        ("sh_addr", "Q"),
        ("sh_offset", "Q"),
        ("sh_size", "Q"),
        ("sh_link", "I"),
        ("sh_info", "I"),
        ("sh_addralign", "Q"),
        ("sh_entsize", "Q")
        ) 


elf32_phdr_format = (
        ("p_type", "I"), 
        ("p_offset", "I"),
        ("p_vaddr", "I"),
        ("p_paddr", "I"),
        ("p_filesz", "I"),
        ("p_memsz", "I"), 
        ("p_flags", "I"),
        ("p_align", "I") 
        ) 

elf64_phdr_format = (
        ("p_type", "I"),
        ("p_flags", "I"),
        ("p_offset", "Q"),
        ("p_vaddr", "Q"),
        ("p_paddr", "Q"),
        ("p_filesz", "Q"),
        ("p_memsz", "Q"),
        ("p_align", "Q")
        )

elf32_sym_format = (
        ("st_name", "I"),
        ("st_value", "I"),
        ("st_size", "I"),
        ("st_info", "B"),
        ("st_other", "B"),
        ("st_shndx", "H")
        )

elf64_sym_format = (
        ("st_name", "I"),
        ("st_info", "B"),
        ("st_other", "B"),
        ("st_shndx", "H"),
        ("st_value", "Q"),
        ("st_size", "Q")
        )

verdef_format = (
        ("vd_version", "H"),
        ("vd_flags", "H"),
        ("vd_ndx", "H"),
        ("vd_cnt", "H"),
        ("vd_hash", "I"),
        ("vd_aux", "I"),
        ("vd_next", "I")
        )

verdaux_format = (
        ("vda_name", "I"),
        ("vda_next", "I")
        )

verneed_format = (
        ("vn_version", "H"),
        ("vn_cnt", "H"),
        ("vn_file", "I"),
        ("vn_aux", "I"),
        ("vn_next", "I")
        )

vernaux_format = (
	("vna_hash", "I"),
	("vna_flags", "H"),
	("vna_other", "H"),
	("vna_name", "I"),
	("vna_next", "I")
	)

elf32_rel_format = (
        ("r_offset", "I"),
        ("r_info", "I") 
        )

elf64_rel_format = (
        ("r_offset", "Q"),
        ("r_info", "Q")
        ) 

elf32_rela_format = (
        ("r_offset", "I"),
        ("r_info", "I"),
        ("r_addend", "I")
        )

elf64_rela_format = (
        ("r_offset", "Q"),
        ("r_info", "Q"),
        ("r_addend", "Q")
        )

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


def read_header(elf, buffer):
    buffer.seek(0) 
    elf_header = elf['elf_header']
    elf_header["file_ident"] = buffer.read(ELF32)
    if elf_header["file_ident"] != ELFSIG:
        raise ValueError("This is not a ELF object")
    file_class = ord(buffer.read(ELF8))
    if file_class == ELFCLASS32:
        hdr_format = elf32_hdr_format
    elif file_class == ELFCLASS64:
        hdr_format = elf64_hdr_format
    else:
        raise ValueError("Unknown ELFCLASS: %d", file_class)
    elf_header["file_class"] = file_class
    elf_header["file_encoding"] = ord(buffer.read(ELF8))
    elf_header["file_version"] = ord(buffer.read(ELF8)) 
    #ignore 9 bytes
    buffer.seek(9, io.SEEK_CUR) 
    load_struct(buffer, elf_header, hdr_format) 
    

def read_section_header(elf, buffer): 
    elf_header = elf["elf_header"]
    sections = elf["sections"]
    e_shoff = elf_header["e_shoff"]
    buffer.seek(e_shoff)
    e_shnum = elf_header["e_shnum"] 
    if elf_header["file_class"] == ELFCLASS32:
        shdr_format = elf32_shdr_format
    elif elf_header["file_class"] == ELFCLASS64:
        shdr_format = elf64_shdr_format
    else:
        raise ValueError("Unknown ELFCLASS: %d", file_class) 
    for num in range(e_shnum):    
        section = {}
        load_struct(buffer, section, shdr_format)
        sections.append(section) 


def read_program_header(elf, buffer): 
    elf_header = elf["elf_header"]
    programs = elf["programs"] 
    buffer.seek(elf_header["e_phoff"])
    e_phnum = elf_header["e_phnum"] 
    if elf_header["file_class"] == ELFCLASS32:
        phdr_format = elf32_phdr_format
    elif elf_header["file_class"] == ELFCLASS64:
        phdr_format = elf64_phdr_format 
    else: 
        raise ValueError("Unknown ELFCLASS: %d", file_class) 
    elf_type = elf_header["file_class"]
    for num in range(e_phnum):
        entry = {}
        load_struct(buffer, entry, phdr_format)
        #INTERP
        if entry['p_type'] == PT_INTERP:
            mark = buffer.tell() 
            buffer.seek(entry['p_offset'])
            elf['interpreter'] = buffer.read(entry['p_filesz']) 
            buffer.seek(mark)
        programs.append(entry)


def build_strtab(buffer, section): 
    buffer.seek(section["sh_offset"])        
    size = section["sh_size"] 
    raw = buffer.read(size) 
    strtab = {}
    strend = "\x00"
    i = 0 
    while i < size:
        if raw[i] != strend: 
            i += 1 
            continue 
        j = i + 1
        end = raw.find(strend, j) 
        if end == -1: 
            break
        name = raw[j:end]
        more = name.find(".", 1)
        if more > 0: 
            strtab[j+more] = name[more:]
        strtab[j] = name 
        i = end
    return strtab


def read_strtab(elf, buffer): 
    elf_header = elf["elf_header"] 
    sections = elf["sections"]
    strtab_sections = []
    for section in sections:
        if section["sh_type"] == SHT_STRTAB:
            strtab_sections.append(section) 
    shstrtab_section = None
    for section in strtab_sections:
        buffer.seek(section["sh_offset"])
        if ".text" in buffer.read(section["sh_size"]):
            shstrtab_section = section 
    if not shstrtab_section:
        print "error: where is .shstrtab?"
        return
 
    shstrtab = build_strtab(buffer, shstrtab_section)    
    for section in sections[1:]:
        section["sh_name"] = shstrtab[section["sh_name"]]
    for section in strtab_sections:    
        name = section["sh_name"] 
        strtab = build_strtab(buffer, section)
        elf["strtabs"][name] = strtab


def read_symtab(elf, buffer): 
    sections = elf["sections"] 
    symtabs = elf["symtabs"]
    elf_header= elf["elf_header"]
    symtab_sections = [] 
    for section in sections:
        if section["sh_type"] == SHT_SYMTAB:
            symtab_sections.append(section) 
        if section["sh_type"] == SHT_DYNSYM:
            symtab_sections.append(section) 
    sym_read = buffer.read 
    if elf_header["file_class"] == ELFCLASS32:
        sym_format = elf32_sym_format
    elif elf_header["file_class"] == ELFCLASS64:
        sym_format = elf64_sym_format
    else: 
        raise ValueError("Unknown ELFCLASS: %d", file_class) 
    try:
        strtab = elf["strtabs"][".strtab"] 
        strtab_keys = sorted(strtab.keys(), reverse=True)
    except KeyError:
        pass
    try:
        dynsym = elf["strtabs"][".dynstr"] 
        dynsym_keys = sorted(dynsym.keys(), reverse=True)
    except KeyError:
        pass 
    for section in symtab_sections: 
        buffer.seek(section["sh_offset"]) 
        total = section["sh_size"] / section["sh_entsize"]
        symtab = [] 
        section_name = section["sh_name"]
        for entry in range(total): 
            sym = {} 
            load_struct(buffer, sym, sym_format)
            sym_name = sym["st_name"] 
            if not sym_name:
                sym["st_name"] = "unknown"
            elif section_name == ".symtab": 
                try:
                    sym["st_name"] = strtab[sym_name] 
                except KeyError as e:
                    #slow find
                    for i in strtab_keys:
                        if i < sym_name:
                            sym["st_name"] = strtab[i][sym_name-i:] 
                            break
            elif section_name == ".dynsym": 
                try:
                    sym["st_name"] = dynsym[sym_name] 
                except KeyError as e: 
                    #slow find
                    for i in dynsym_keys:
                        if i < sym_name: 
                            sym["st_name"] = dynsym[i][sym_name-i:] 
                            break
            sym["st_bind"] = sym["st_info"] >> 4 
            sym["st_type"] = sym["st_info"] & 0xf 
            symtab.append(sym) 
        symtabs[section["sh_name"]] = symtab                     

def read_rel(elf, buffer): 
    sections = elf["sections"] 
    rel_list = []
    for section in sections:
        if section["sh_type"] == SHT_REL:
            rel_list.append(section) 
    elf_type = elf["elf_header"]["file_class"]
    symtab = elf["symtabs"][".dynsym"]
    elf["rel"] = {}
    for rel in rel_list:
        r1_list = []
        buffer.seek(rel["sh_offset"]) 
        if elf_type == ELFCLASS32: 
            for i in range(rel["sh_size"] / rel["sh_entsize"]): 
                entry = {} 
                load_struct(buffer, entry, elf32_rel_format) 
                r_info = entry["r_info"]
                entry["r_symbol"] = r_info >> 8 
                entry["r_type"] = r_info & 0xff 
                r1_list.append(entry)
        else: 
            for i in range(rel["sh_size"] / rel["sh_entsize"]): 
                entry = {}
                load_struct(buffer, entry, elf64_rel_format) 
                r_info = entry["r_info"] 
                entry["r_symbol"] = r_info >> 32 
                entry["r_type"] = r_info & 0xffffffff
                r1_list.append(entry)
        elf["rel"][rel["sh_name"]] = r1_list 

def read_rela(elf, buffer): 
    sections = elf["sections"] 
    rela_list = []
    for section in sections:
        if section["sh_type"] == SHT_RELA:
            rela_list.append(section) 
    elf["rela"] = {}
    elf_type = elf["elf_header"]["file_class"]
    symtab = elf["symtabs"][".dynsym"] 
    for rela in rela_list:
        r2_list = []
        buffer.seek(rela["sh_offset"]) 
        if elf_type == ELFCLASS32: 
            for i in range(rela["sh_size"] / rela["sh_entsize"]):
                entry = {} 
                load_struct(buffer, entry, elf32_rela_format)
                r_info = entry["r_info"] 
                entry["r_symbol"] = r_info >> 8 
                entry["r_type"] = r_info & 0xff 
                r2_list.append(entry) 
        else:                    
            for i in range(rela["sh_size"] / rela["sh_entsize"]): 
                entry = {}
                load_struct(buffer, entry, elf64_rela_format)
                r_info = entry["r_info"] 
                entry["r_symbol"] = r_info >> 32
                entry["r_type"] = r_info & 0xffffffff 
                r2_list.append(entry)
        elf["rela"][rela["sh_name"]] = r2_list 



def read_dynamic(elf, buffer): 
    sections = elf["sections"]
    dynamic = None
    for section in sections:
        if section["sh_type"] == SHT_DYNAMIC:
            dynamic = section            
    dynamic_list = elf["dynamic"]
    buffer.seek(dynamic["sh_offset"])
    total = dynamic["sh_size"] / dynamic["sh_entsize"] 
    if elf["elf_header"]["file_class"] == ELFCLASS32: 
        for entry in range(total):
            dtag, value = struct.unpack("II", buffer.read(ELF64)) 
            dynamic_list.append({dtag: value})    
            if not dtag:
                break
    else:
        for entry in range(total):
            dtag, value = struct.unpack("QQ", buffer.read(2*ELF64)) 
            dynamic_list.append({dtag: value})    
            if not dtag:
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

def read_versym(elf, buffer): 
    sections = elf["sections"]
    versym = None
    for section in sections: 
        if section["sh_type"] == SHT_GNU_versym:
            versym = section            
            break     
    if not versym:
        elf["versym"] = []
        return
    #seek and read
    buffer.seek(versym["sh_offset"])
    total = versym["sh_size"] / versym["sh_entsize"] 
    verlist = []
    for entry in range(total):
        verlist.append(struct.unpack("H", buffer.read(2))[0])
    elf["versym"] = verlist


def read_verdef(elf, buffer):
    sections = elf["sections"]
    verdef = None
    for section in sections:
        if section["sh_type"] == SHT_GNU_verdef:
            verdef = section
            break
    if not verdef:
        elf["verdef"] = []
        return
    buffer.seek(verdef["sh_offset"])
    if not verdef["sh_size"]:
        #nothing here
        return
    symtab = elf["strtabs"][sections[verdef["sh_link"]]["sh_name"]] 
    deflist = [] 
    while True:
        entry = {}
        load_struct(buffer, entry, verdef_format)
        vs = []
        if entry["vd_aux"] != 0:
            while True:
                verdaux = {}
                load_struct(buffer, verdaux, verdaux_format)
                vs.append(verdaux)
                verdaux["vda_name"] = symtab[verdaux["vda_name"]]
                if verdaux["vda_next"] == 0:
                    break
        entry["verdaux"] = vs 
        deflist.append(entry)
        if entry["vd_next"] == 0:
            break
    elf["verdef"] = deflist 

def read_verneed(elf, buffer): 
    sections = elf["sections"]
    verneed = None
    for section in sections: 
        if section["sh_type"] == SHT_GNU_verneed:
            verneed = section            
            break     
    if not verneed:
        elf["verneed"] = []
        elf["verindex"] = {}
        return
    buffer.seek(verneed["sh_offset"])     
    if not verneed["sh_size"]:
        #nothing here
        return 
    symtab = elf["strtabs"][sections[verneed["sh_link"]]["sh_name"]] 
    deflist = [] 
    while True: 
        entry = {} 
        load_struct(buffer, entry, verneed_format)
        vs = [] 
        if entry["vn_aux"] != 0: 
            while True:
                vernaux = {}
                load_struct(buffer,  vernaux, vernaux_format) 
                vs.append(vernaux)
                vernaux["vna_name"] = symtab[vernaux["vna_name"]]
                if vernaux["vna_next"] == 0:
                    break
        entry["vernaux"] = vs
        entry["vn_file"] = symtab[entry["vn_file"]]
        deflist.append(entry) 
        if entry["vn_next"] == 0:
            break 
    elf["verneed"] = deflist
    verindex = {}
    if "verindex" in elf:
        verindex = elf["verindex"] 
    for i in deflist:
        for j in i["vernaux"]:
            verindex[j["vna_other"]] = j
    elf["verindex"] = verindex 

def read_section(buffer, name): 
    sections = elf["sections"]
    target = None
    for section in sections: 
        if section["sh_name"] == name:
            target = section            
            break     
    if not target:
        raise Exception("No section %s" % target)
    buffer.seek(target["sh_offset"])
    elf["target"] = buffer.read(target["sh_size"])

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


def read_debugabbr(elf, buffer):
    sections = elf["sections"]
    debug_abbr = ".debug_abbrev"
    if debug_abbr not in sections:
        raise ValueError("need .debug_abbrev?")
    debug_abbr = sections[".debug_abbrev"]
    buffer.seek(debug_abbr["offset"])
 
def readelf(path, flags, *args): 
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
    flags |= ELF_HEADER 
    if flags & ELF_RELA:
        flags |= ELF_SYMBOL
    if flags & ELF_DYNAMIC:
        flags |= ELF_SYMBOL 
    if flags & ELF_SYMBOL:
        flags |= ELF_VERNEED
    f = open(path, "rb")
    buffer = mmap.mmap(f.fileno(), 0, mmap.MAP_PRIVATE, mmap.PROT_READ) 
    if flags & ELF_HEADER:
        read_header(elf, buffer) 
        read_section_header(elf, buffer)
        read_program_header(elf, buffer) 
        read_strtab(elf, buffer) 
    if flags & ELF_SYMBOL: 
        read_symtab(elf, buffer) 
    if flags & ELF_DYNAMIC: 
        read_dynamic(elf, buffer) 
    if flags & ELF_RELA:
        read_rel(elf, buffer)
        read_rela(elf, buffer)
    if flags & DWARF_INFO: 
        dwarf.read_debuginfo(elf, buffer) 
    if flags & ELF_PSECTION:
        read_section(elf, buffer, args[1])
    if flags & ELF_VERNEED: 
        read_verdef(elf, buffer)
        read_verneed(elf, buffer)
        read_versym(elf, buffer)
    buffer.close()
    f.close()
    return elf

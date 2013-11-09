import os
import mmap 
from baseutils import strtoint

elf = None
_read = None

def print_mem_usage(position):
    Mib = 1024
    pagesize = 4
    f = open("/proc/%d/statm" % os.getpid(), "r")
    mems = f.read().split(" ")
    print "in", position    
    print "VM: %dm PHYM: %dm" % (int(mems[0]) * pagesize / Mib,
            int(mems[1]) * pagesize / Mib)              
    f.close()

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

elf_arch_type = {
        0: "EM_NONE",
        3: "EM_386",
        62: "EM_X86_64"
        }
        
elf_encoding = {
        0: "ELFDATANONE",
        1: "ELFDATA2LSB",
        2: "ELFDATA2MSB"
        }


elf_class_type = {
        0: "ELFCLASSNONE",
        1: "ELFCLASS32",
        2: "ELFCLASS64"
        }

elf_type = {
        0: "ET_NONE",
        1: "ET_REL",
        2: "ET_EXEC",
        3: "ET_DYN",
        4: "ET_CORE"
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
        11: "SHT_DYNSYM",
        14: "SHT_INIT_ARRAY",
        15: "SHT_FINI_ARRAY",
        16: "SHT_PREINIT_ARRAY",
        17: "SHT_GROUP",
        18: "SHT_SYMTAB_SHNDX",
        0x60000000: "SHT_LOOS",
        0x6fffffff: "SHT_HIOS",
        0x6fff4700: "SHT_GNU_INCREMENTAL_INPUTS",
        0x6ffffff5: "SHT_GNU_ATTRIBUTES",
        0x6ffffff6: "SHT_GNU_HASH",
        0x6ffffff7: "SHT_GNU_LIBLIST",
        0x6ffffffd: "SHT_GNU_verdef",
        0x6ffffffe: "SHT_GNU_verneed",
        0x6fffffff: "SHT_GNU_versym"
        }

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
        0x6ffffffb: "DT_RELCOUNT",
        0x6ffffffc: "DT_VERDEF",
        0x6ffffffd: "DT_VERDEFNUM",
        0x6ffffffe: "DT_VERNEED",
        0x6fffffff: "DT_VERNEEDNUM",
        0x6ffffff0: "DT_VERSYM"
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
        -6: "STB_UNIQUE"
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

#Tags
DW_TAG_array_type = 0x01
#DW_AT_name
#DW_AT_type
#DW_AT_bit_stride
#DW_AT_bit_size
#DW_AT_byte_size
#DW_ORD_col_major
#DW_ORD_row_major
#child -> DW_TAG_subrange_type, DW_TAG_enumeration_type
#DW_AT_allocated
#DW_AT_associated
#DW_AT_data_location 
DW_TAG_class_type = 0x02
DW_TAG_entry_point = 0x03
#DW_AT_name
#DW_AT_linkage_name
#DW_AT_external
#DW_AT_main_subprogram
#DW_AT_calling_convention
#-> DW_CC_normal, program, nocall
#DW_AT_prototyped
#DW_AT_elemental
#DW_AT_recursive
#DW_AT_pure
#DW_AT_recursive 
#DW_AT_type
#DW_AT_low_pc
#DW_AT_high_pc
#DW_AT_ranges
#DW_AT_entry_pc
#DW_AT_start_scope
#DW_AT_segment
#DW_AT_location
#DW_AT_address_class 
#children -> DW_TAG_unspecified_parameters
#children -> DW_TAG_common_inclusion -> DW_AT_common_reference
#children -> DW_TAG_thrown_type
#children -> DW_TAG_template_type_parameter
#DW_AT_return_addr
#DW_AT_frame_base
#DW_AT_static_link
#DW_AT_inline -> DW_INL_not_inlined, inlined, declared_not_inlined, declared_inlined
#inined subroutine -> DW_AT_call_file 
#inined subroutine -> DW_AT_call_line 
#inined subroutine -> DW_AT_call_column 
#inined subroutine -> DW_AT_const_value 
#inined subroutine -> DW_AT_const_expr 
#inined subroutine -> DW_AT_abstract_origin 
#inined subroutine -> DW_AT_trampoline 
#inined subroutine -> DW_AT_artificial

DW_TAG_enumeration_type = 0x04
DW_TAG_formal_parameter = 0x05
DW_TAG_imported_declaration = 0x08
DW_TAG_label = 0x0a
DW_TAG_lexical_block = 0x0b
DW_TAG_member = 0x0d
DW_TAG_pointer_type = 0x0f
DW_TAG_reference_type = 0x10
DW_TAG_compile_unit = 0x11
DW_TAG_string_type = 0x12
DW_TAG_structure_type = 0x13
DW_TAG_subroutine_type = 0x15
DW_TAG_typedef = 0x16
DW_TAG_union_type = 0x17
DW_TAG_unspecified_parameters = 0x18
DW_TAG_variant = 0x19
DW_TAG_common_block = 0x1a
DW_TAG_common_inclusion = 0x1b
DW_TAG_inheritance = 0x1c
DW_TAG_inlined_subroutine = 0x1d
DW_TAG_module = 0x1e
DW_TAG_ptr_to_member_type = 0x1f
DW_TAG_set_type = 0x20
DW_TAG_subrange_type = 0x21
DW_TAG_with_stmt = 0x22
DW_TAG_access_declaration = 0x23
DW_TAG_base_type = 0x24
DW_TAG_catch_block = 0x25
DW_TAG_const_type = 0x26
DW_TAG_constant = 0x27
DW_TAG_enumerator = 0x28
DW_TAG_file_type = 0x29
DW_TAG_friend = 0x2a
DW_TAG_namelist = 0x2b
DW_TAG_namelist_item = 0x2c
DW_TAG_packed_type = 0x2d
DW_TAG_subprogram = 0x2e
DW_TAG_template_type_parameter = 0x2f
DW_TAG_template_value_parameter = 0x30
DW_TAG_thrown_type = 0x31
DW_TAG_try_block = 0x32
DW_TAG_variant_part = 0x33
DW_TAG_variable = 0x34
DW_TAG_volatile_type = 0x35
DW_TAG_dwarf_procedure = 0x36
DW_TAG_restrict_type = 0x37
DW_TAG_interface_type = 0x38
DW_TAG_namespace = 0x39
DW_TAG_imported_module = 0x3a
DW_TAG_unspecified_type = 0x3b
DW_TAG__partial_unit = 0x3c
DW_TAG_imported_unit = 0x3d
DW_TAG_condition = 0x3f
DW_TAG_shared_type = 0x40
DW_TAG_type_unit = 0x41
DW_TAG_type_rvalue_reference_type = 0x42
DW_TAG_template_alias = 0x43
DW_TAG_lo_user = 0x4080
DW_TAG_hi_user = 0xffff

#has children ?
DW_CHILDREN_no = 0x00
DW_CHILDREN_yes = 0x01

#attributes
DW_AT_sibling = 0x01
DW_AT_location = 0x02
DW_AT_name = 0x03
DW_AT_ordering = 0x09
DW_AT_byte_size = 0x0b
DW_AT_bit_offset = 0x0c
DW_AT_bit_size = 0x0d
DW_AT_stmt_list = 0x10
DW_AT_low_pc = 0x11
DW_AT_high_pc = 0x12
DW_AT_language = 0x13
DW_AT_discr = 0x15
DW_AT_discr_value = 0x16
DW_AT_visibility = 0x17
DW_AT_import = 0x18
DW_AT_string_length = 0x19
DW_AT_common_reference = 0x1a
DW_AT_comp_dir = 0x1b
DW_AT_const_value = 0x1c
DW_AT_containing_type = 0x1d
DW_AT_default_value = 0x1e
DW_AT_inline = 0x20
DW_AT_is_optional = 0x21
DW_AT_lower_bound = 0x22
DW_AT_producer = 0x25
DW_AT_prototyped = 0x27
DW_AT_return_addr = 0x2a
DW_AT_start_scope = 0x2c
DW_AT_bit_stride = 0x2e
DW_AT_upper_bound = 0x2f
DW_AT_abstract_origin = 0x31
DW_AT_accessibility = 0x32
DW_AT_address_class = 0x33
DW_AT_artificial = 0x34
DW_AT_base_types = 0x35
DW_AT_calling_convention = 0x36
DW_AT_count = 0x37
DW_AT_data_member_location = 0x38
DW_AT_decl_column = 0x39
DW_AT_decl_file = 0x3a
DW_AT_decl_line = 0x3b
DW_AT_declaration = 0x3c
DW_AT_discr_list = 0x3d
DW_AT_encoding = 0x3e
DW_AT_external = 0x3f
DW_AT_frame_base = 0x40
DW_AT_friend = 0x41
DW_AT_identifier_case = 0x42
DW_AT_macro_info = 0x43
DW_AT_namelist_item = 0x44
DW_AT_priority = 0x45
DW_AT_segment = 0x46
DW_AT_specification = 0x47
DW_AT_static_link = 0x48
DW_AT_type = 0x49
DW_AT_use_location = 0x4a
DW_AT_virtuality = 0x4c
DW_AT_vtable_elem_location = 0x4d
DW_AT_allocated = 0x4e
DW_AT_associated = 0x4f
DW_AT_data_location = 0x50
DW_AT_byte_stride = 0x51
DW_AT_entry_pc = 0x52
DW_AT_use_UTF8 = 0x53
DW_AT_extension = 0x54
DW_AT_ranges = 0x55
DW_AT_trampoline = 0x56
DW_AT_call_column = 0x57
DW_AT_call_file = 0x58
DW_AT_call_line = 0x59
DW_AT_description = 0x5a
DW_AT_binary_scale = 0x5b
DW_AT_decimal_scale = 0x5c
DW_AT_small = 0x5d
DW_AT_decimal_sign = 0x5e
DW_AT_digit_count = 0x5f
DW_AT_picture_string = 0x60
DW_AT_mutable = 0x61
DW_AT_threads_scaled = 0x62
DW_AT_explicit = 0x63
DW_AT_object_pointer = 0x64
DW_AT_endiantity = 0x65
DW_AT_elemental = 0x66
DW_AT_pure = 0x67
DW_AT_recursive = 0x68
DW_AT_signature = 0x69
DW_AT_main_subprogram = 0x6a
DW_AT_data_bit_offset = 0x6b
DW_AT_const_expr = 0x6c
DW_AT_enum_class = 0x6d
DW_AT_linkage_name = 0x6e
DW_AT_lo_user = 0x2000
DW_AT_hi_user = 0x3fff

#format
DW_FORM_addr = 0x01
DW_FORM_block2 = 0x03
DW_FORM_block4 = 0x04
DW_FORM_data2 = 0x05
DW_FORM_data4 = 0x06
DW_FORM_data8 = 0x07
DW_FORM_string = 0x08
DW_FORM_block = 0x09
DW_FORM_block1 = 0x0a
DW_FORM_data1 = 0x0b
DW_FORM_flag = 0x0c
DW_FORM_sdata = 0x0d
DW_FORM_strp = 0x0e
DW_FORM_udata = 0x0f
DW_FORM_ref_addr = 0x10
DW_FORM_ref1 = 0x11
DW_FORM_ref2 = 0x12
DW_FORM_ref4 = 0x13
DW_FORM_ref8 = 0x14
DW_FORM_ref_udata = 0x15
DW_FORM_indirect = 0x16
DW_FORM_sec_offset = 0x17
DW_FORM_exprloc = 0x18
DW_FORM_flag_present = 0x19
DW_FORM_ref_sig8 = 0x20

def read_header(buffer):
    buffer.seek(0)
    elf_header = elf['elf_header']
    elf_header["file_ident"] = _read(4)
    assert elf_header["file_ident"] == "\x7fELF"
    elf_header["file_class"] = strtoint(_read(1))
    elf_header["file_encoding"] = strtoint(_read(1))
    elf_header["file_version"] = strtoint(_read(1))
    #ignore 9 chars
    _read(9) 
    elf_header["e_type"] = strtoint(_read(2))
    elf_header["e_machine"] = strtoint(_read(2))
    elf_header["e_version"] = strtoint(_read(4))
    elf_header["e_entry"] = strtoint(_read(8))
    elf_header["e_phoff"] = strtoint(_read(8))
    elf_header["e_shoff"] = strtoint(_read(8))
    elf_header["e_flags"] = strtoint(_read(4))
    elf_header["e_ehsize"] = strtoint(_read(2))
    elf_header["e_phentsize"] = strtoint(_read(2))
    elf_header["e_phnum"] = strtoint(_read(2))
    elf_header["e_shentsize"] = strtoint(_read(2))
    elf_header["e_shnum"] = strtoint(_read(2))
    elf_header["e_shstrndx"] = strtoint(_read(2))

def read_section_header(buffer):
    elf_header = elf["elf_header"]
    sections = elf["sections"]
    e_shoff = elf_header["e_shoff"]
    buffer.seek(e_shoff)
    e_shnum = elf_header["e_shnum"]
    e_shentsize = elf_header["e_shentsize"] 
    for num in range(e_shnum):    
        sections.append({
            "name": strtoint(_read(4)),
            "type": strtoint(_read(4)),
            "flag": strtoint(_read(8)),
            "addr": strtoint(_read(8)),
            "offset": strtoint(_read(8)),
            "size": strtoint(_read(8)),
            "link": strtoint(_read(4)),
            "info": strtoint(_read(4)),
            "align": strtoint(_read(8)),
            "entsize": strtoint(_read(8))
        })


def read_program_header(buffer):
    elf_header = elf["elf_header"]
    programs = elf["programs"] 
    buffer.seek(elf_header["e_phoff"])
    e_phnum = elf_header["e_phnum"] 
    e_phentsize = elf_header["e_phentsize"]
    for num in range(e_phnum):
        entry = {
            "type": strtoint(_read(4)),
            "flag": strtoint(_read(4)),
            "offset": strtoint(_read(8)),
            "virt": strtoint(_read(8)),
            "phys": strtoint(_read(8)),
            "filesize": strtoint(_read(8)),
            "memsize": strtoint(_read(8)),
            "align": strtoint(_read(8))
            }
        #INTERP
        if entry['type'] == 3:
            mark = buffer.tell() 
            buffer.seek(entry['offset'])
            elf['interpreter'] = _read(entry['filesize']) 
            buffer.seek(mark)
        programs.append(entry)


def build_strtab(buffer, section): 
    buffer.seek(section["offset"])        
    size = section["size"] 
    strtabdata = _read(size) 
    strtab = {}
    j = 0
    strend = "\x00"
    while j < size:
        if strtabdata[j] == strend:
            k = j + 1
            end = strtabdata.find(strend, k) 
            if end == -1: 
                break
            name = strtabdata[k:end]
            more = name.find(".", 1)
            if more > 0: 
                strtab[k+more] = name[more:]
            strtab[k] = name 
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
    strtab = elf["strtabs"][".strtab"]
    dynsym = elf["strtabs"][".dynstr"]
    for section in sections:
        if section["type"] == 2:
            symtab_sections.append(section) 
        if section["type"] == 11:
            symtab_sections.append(section)
    for section in symtab_sections: 
        flag = 0
        if section["name"] == ".symtab":
            flag = 1
        elif section["name"] == ".dynsym":
            flag = 2
        buffer.seek(section["offset"]) 
        sym_read = buffer.read 
        extra = section["align"] - (section["entsize"] / section["align"]) 
        total = section["size"] / section["entsize"]
        symtab = []
        symtab_append = symtab.append 
        for entry in range(total): 
            sym_name = strtoint(sym_read(4)) 
            if not sym_name:
                sym_name = "unknown"
            elif flag == 1:
                sym_name = strtab[sym_name]
            elif not flag == 2:
                sym_name = dynsym[sym_name]
            info = strtoint(sym_read(1)) 
            #name ,bind , type, vis, index, value, size
            symtab_append((sym_name, info >> 4,  info & 0xf,
                strtoint(sym_read(1)), 
                strtoint(sym_read(2)), 
                strtoint(sym_read(8)), 
                strtoint(sym_read(8))
                ))
        symtabs[section["name"]] = symtab                     
        #sym_data.close() 

def read_rela(buffer):
    sections = elf["sections"] 

def read_dynamic(buffer): 
    sections = elf["sections"]
    dynamic = None
    for section in sections:
        if section["type"] == 6:
            dynamic = section            
    dynamic_list = elf["dynamic"]
    buffer.seek(dynamic["offset"])
    total = dynamic["size"] / dynamic["entsize"] 
    for entry in range(total):
        d_tag = strtoint(_read(8))
        value = strtoint(_read(8)) 
        dynamic_list.append({d_tag: value})    
        if not d_tag:
            break
    in_symtab = [1, 14, 15]     
    strtab = elf["strtabs"][".strtab"]
    dyntab = elf["strtabs"][".dynstr"]
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


def read_debugabbr(buffer):
    sections = elf["sections"]
    debug_abbrev = ".debug_abbrev"
    if debug_abbrev not in sections:
        assert False, "where is the section .debug_abbrev" 
    debug_abbrev = sections[".debug_abbrev"]
    buffer.seek(debug_abbrev["offset"])

def read_debuginfo(buffer):
    sections = elf["sections"]
    debug_info = ".debug_info"
    if debug_info not in sections:
        assert False, "where is the section .debug_info?"
    debug_info = sections["debug_info"]
    buffer.seek(debug_info["offset"])
 
def set_target(path):
    global elf 
    global _read
    elf = {
        "elf_header": {},
        "sections": [],
        "programs": [], 
        "interpreter": "",
        "strtabs": {},
        "symtabs": {},
        "dynamic": []
        } 
    f = open(path, "r+b")
    buffer = mmap.mmap(f.fileno(), 0, mmap.MAP_PRIVATE, mmap.PROT_READ)
    _read = buffer.read
    read_header(buffer) 
    read_section_header(buffer)
    read_program_header(buffer)
    #print_mem_usage("after headers")
    read_strtab(buffer) 
    #print_mem_usage("after strtab")
    read_symtab(buffer) 
    #print_mem_usage("after symtab")
    read_dynamic(buffer) 
    buffer.close()
    f.close()
    return elf

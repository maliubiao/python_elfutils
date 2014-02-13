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


DW_TAG_array_type = 0x01 
DW_TAG_class_type = 0x02
DW_TAG_entry_point = 0x03 
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

TAG_types = {
        0x01: "DW_TAG_array_type",
        0x02: "DW_TAG_class_type",
        0x03: "DW_TAG_entry_point",
        0x04: "DW_TAG_enumeration_type",
        0x05: "DW_TAG_formal_parameter",
        0x08: "DW_TAG_imported_declaration",
        0x0a: "DW_TAG_label",
        0x0b: "DW_TAG_lexical_block",
        0x0d: "DW_TAG_member",
        0x0f: "DW_TAG_pointer_type",
        0x10: "DW_TAG_reference_type",
        0x11: "DW_TAG_compile_unit",
        0x12: "DW_TAG_string_type",
        0x13: "DW_TAG_structure_type",
        0x15: "DW_TAG_subroutine_type",
        0x16: "DW_TAG_typedef",
        0x17: "DW_TAG_union_type",
        0x18: "DW_TAG_unspecified_parameters",
        0x19: "DW_TAG_variant",
        0x1a: "DW_TAG_common_block",
        0x1b: "DW_TAG_common_inclusion",
        0x1c: "DW_TAG_inheritance",
        0x1d: "DW_TAG_inlined_subroutine",
        0x1e: "DW_TAG_module",
        0x1f: "DW_TAG_ptr_to_member_type",
        0x20: "DW_TAG_set_type",
        0x21: "DW_TAG_subrange_type",
        0x22: "DW_TAG_with_stmt",
        0x23: "DW_TAG_access_declaration",
        0x24: "DW_TAG_base_type",
        0x25: "DW_TAG_catch_block",
        0x26: "DW_TAG_const_type",
        0x27: "DW_TAG_constant",
        0x28: "DW_TAG_enumerator",
        0x29: "DW_TAG_file_type",
        0x2a: "DW_TAG_friend",
        0x2b: "DW_TAG_namelist",
        0x2c: "DW_TAG_namelist_item",
        0x2d: "DW_TAG_packed_type",
        0x2e: "DW_TAG_subprogram",
        0x2f: "DW_TAG_template_type_parameter",
        0x30: "DW_TAG_template_value_parameter",
        0x31: "DW_TAG_thrown_type",
        0x32: "DW_TAG_try_block",
        0x33: "DW_TAG_variant_part",
        0x34: "DW_TAG_variable",
        0x35: "DW_TAG_volatile_type",
        0x36: "DW_TAG_dwarf_procedure",
        0x37: "DW_TAG_restrict_type",
        0x38: "DW_TAG_interface_type",
        0x39: "DW_TAG_namespace",
        0x3a: "DW_TAG_imported_module",
        0x3b: "DW_TAG_unspecified_type",
        0x3c: "DW_TAG__partial_unit",
        0x3d: "DW_TAG_imported_unit",
        0x3f: "DW_TAG_condition",
        0x40: "DW_TAG_shared_type",
        0x41: "DW_TAG_type_unit",
        0x42: "DW_TAG_type_rvalue_reference_type",
        0x43: "DW_TAG_template_alias",
        0x4080: "DW_TAG_lo_user",
        0xffff: "DW_TAG_hi_user"
        }

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

AT_types = {
        0x01: "DW_AT_sibling",
        0x02: "DW_AT_location",
        0x03: "DW_AT_name",
        0x09: "DW_AT_ordering",
        0x0b: "DW_AT_byte_size",
        0x0c: "DW_AT_bit_offset",
        0x0d: "DW_AT_bit_size",
        0x10: "DW_AT_stmt_list",
        0x11: "DW_AT_low_pc",
        0x12: "DW_AT_high_pc",
        0x13: "DW_AT_language",
        0x15: "DW_AT_discr",
        0x16: "DW_AT_discr_value",
        0x17: "DW_AT_visibility",
        0x18: "DW_AT_import",
        0x19: "DW_AT_string_length",
        0x1a: "DW_AT_common_reference",
        0x1b: "DW_AT_comp_dir",
        0x1c: "DW_AT_const_value",
        0x1d: "DW_AT_containing_type",
        0x1e: "DW_AT_default_value",
        0x20: "DW_AT_inline",
        0x21: "DW_AT_is_optional",
        0x22: "DW_AT_lower_bound",
        0x25: "DW_AT_producer",
        0x27: "DW_AT_prototyped",
        0x2a: "DW_AT_return_addr",
        0x2c: "DW_AT_start_scope",
        0x2e: "DW_AT_bit_stride",
        0x2f: "DW_AT_upper_bound",
        0x31: "DW_AT_abstract_origin",
        0x32: "DW_AT_accessibility",
        0x33: "DW_AT_address_class",
        0x34: "DW_AT_artificial",
        0x35: "DW_AT_base_types",
        0x36: "DW_AT_calling_convention",
        0x37: "DW_AT_count",
        0x38: "DW_AT_data_member_location",
        0x39: "DW_AT_decl_column",
        0x3a: "DW_AT_decl_file",
        0x3b: "DW_AT_decl_line",
        0x3c: "DW_AT_declaration",
        0x3d: "DW_AT_discr_list",
        0x3e: "DW_AT_encoding",
        0x3f: "DW_AT_external",
        0x40: "DW_AT_frame_base",
        0x41: "DW_AT_friend",
        0x42: "DW_AT_identifier_case",
        0x43: "DW_AT_macro_info",
        0x44: "DW_AT_namelist_item",
        0x45: "DW_AT_priority",
        0x46: "DW_AT_segment",
        0x47: "DW_AT_specification",
        0x48: "DW_AT_static_link",
        0x49: "DW_AT_type",
        0x4a: "DW_AT_use_location",
        0x4c: "DW_AT_virtuality",
        0x4d: "DW_AT_vtable_elem_location",
        0x4e: "DW_AT_allocated",
        0x4f: "DW_AT_associated",
        0x50: "DW_AT_data_location",
        0x51: "DW_AT_byte_stride",
        0x52: "DW_AT_entry_pc",
        0x53: "DW_AT_use_UTF8",
        0x54: "DW_AT_extension",
        0x55: "DW_AT_ranges",
        0x56: "DW_AT_trampoline",
        0x57: "DW_AT_call_column",
        0x58: "DW_AT_call_file",
        0x59: "DW_AT_call_line",
        0x5a: "DW_AT_description",
        0x5b: "DW_AT_binary_scale",
        0x5c: "DW_AT_decimal_scale",
        0x5d: "DW_AT_small",
        0x5e: "DW_AT_decimal_sign",
        0x5f: "DW_AT_digit_count",
        0x60: "DW_AT_picture_string",
        0x61: "DW_AT_mutable",
        0x62: "DW_AT_threads_scaled",
        0x63: "DW_AT_explicit",
        0x64: "DW_AT_object_pointer",
        0x65: "DW_AT_endiantity",
        0x66: "DW_AT_elemental",
        0x67: "DW_AT_pure",
        0x68: "DW_AT_recursive",
        0x69: "DW_AT_signature",
        0x6a: "DW_AT_main_subprogram",
        0x6b: "DW_AT_data_bit_offset",
        0x6c: "DW_AT_const_expr",
        0x6d: "DW_AT_enum_class",
        0x6e: "DW_AT_linkage_name",
        0x2000: "DW_AT_lo_user",
        0x3fff: "DW_AT_hi_user"
        }
#format
#8c machine addr
DW_FORM_addr = 0x01 
#2c
DW_FORM_block2 = 0x03
#4c
DW_FORM_block4 = 0x04
#2c
DW_FORM_data2 = 0x05
#4c
DW_FORM_data4 = 0x06
#8c
DW_FORM_data8 = 0x07
#c_str
DW_FORM_string = 0x08
#unsigned LEB
DW_FORM_block = 0x09
#1c
DW_FORM_block1 = 0x0a
#1c
DW_FORM_data1 = 0x0b
#1c
DW_FORM_flag = 0x0c
#signed LEB
DW_FORM_sdata = 0x0d
#offset in .debug_str, 4c 32, 8c 64
DW_FORM_strp = 0x0e
#unsigned LEB
DW_FORM_udata = 0x0f
#offset in .debug_info
DW_FORM_ref_addr = 0x10
#1c
DW_FORM_ref1 = 0x11
#2c
DW_FORM_ref2 = 0x12
#4c
DW_FORM_ref4 = 0x13
#8c
DW_FORM_ref8 = 0x14
#unsigned LEB
DW_FORM_ref_udata = 0x15
#unsigned LEB
DW_FORM_indirect = 0x16
#4c 32, 8c 64
DW_FORM_sec_offset = 0x17
#unsigned LEB
DW_FORM_exprloc = 0x18
#1c
DW_FORM_flag_present = 0x19
#8c signature
DW_FORM_ref_sig8 = 0x20

FORM_types =  {
        0x01: "DW_FORM_addr",
        0x03: "DW_FORM_block2",
        0x04: "DW_FORM_block4",
        0x05: "DW_FORM_data2",
        0x06: "DW_FORM_data4",
        0x07: "DW_FORM_data8",
        0x08: "DW_FORM_string",
        0x09: "DW_FORM_block",
        0x0a: "DW_FORM_block1",
        0x0b: "DW_FORM_data1",
        0x0c: "DW_FORM_flag",
        0x0d: "DW_FORM_sdata",
        0x0e: "DW_FORM_strp",
        0x0f: "DW_FORM_udata",
        0x10: "DW_FORM_ref_addr",
        0x11: "DW_FORM_ref1",
        0x12: "DW_FORM_ref2",
        0x13: "DW_FORM_ref4",
        0x14: "DW_FORM_ref8",
        0x15: "DW_FORM_ref_udata",
        0x16: "DW_FORM_indirect",
        0x17: "DW_FORM_sec_offset",
        0x18: "DW_FORM_exprloc",
        0x19: "DW_FORM_flag_present",
        0x20: "DW_FORM_ref_sig8"
        }

attr_form_to_len = {
        0x01: 8,
        0x03: 2,
        0x04: 4,
        0x05: 2,
        0x06: 4,
        0x07: 8,
        0x08: 0xfff1,  #str
        0x09: 0xfff2,  #uleb
        0x0a: 1,
        0x0b: 1,
        0x0c: 1,
        0x0d: 0xfff3,  #sleb
        0x0e: 4,
        0x0f: 0xfff2,
        0x10: 4,
        0x11: 1,
        0x12: 2,
        0x13: 4,
        0x14: 8,
        0x15: 0xfff2,
        0x16: 0xfff2,
        0x17: 4,
        0x18: 0xfff2,
        0x19: 1,
        0x20: 8 
        }

#.debug_line standard ops
DW_LNS_copy = 0x01
DW_LNS_advance_pc = 0x02
DW_LNS_advance_line = 0x03
DW_LNS_set_file = 0x04
DW_LNS_set_column = 0x05
DW_LNS_negate_stmt = 0x06
DW_LNS_set_basic_block = 0x07
DW_LNS_const_add_pc = 0x08
DW_LNS_fixed_advance_pc = 0x09
DW_LNS_set_prologue_end = 0x0a
DW_LNS_set_epilogue_begin = 0x0b
DW_LNS_set_isa = 0x0c

LINE_STD_ops = {
        0x01: "DW_LNS_copy",
        0x02: "DW_LNS_advance_pc",
        0x03: "DW_LNS_advance_line",
        0x04: "DW_LNS_set_file",
        0x05: "DW_LNS_set_column",
        0x06: "DW_LNS_negate_stmt",
        0x07: "DW_LNS_set_basic_block",
        0x08: "DW_LNS_const_add_pc",
        0x09: "DW_LNS_fixed_advance_pc",
        0x0a: "DW_LNS_set_prologue_end",
        0x0b: "DW_LNS_set_epilogue_begin",
        0x0c : "DW_LNS_set_isa"
        }


#.debug_line ext ops
DW_LINE_end_sequence = 0x01
DW_LINE_set_address = 0x02
DW_LINE_define_file = 0x03
DW_LINE_set_discriminator = 0x04
DW_LINE_lo_user = 0x80
DW_LINE_hi_user = 0xff

LINE_EXT_ops = {
        0x01: "DW_LINE_end_sequence",
        0x02: "DW_LINE_set_address",
        0x03: "DW_LINE_define_file",
        0x04: "DW_LINE_set_discriminator",
        0x80: "DW_LINE_lo_user",
        0xff: "DW_LINE_hi_user"
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
    strtab = elf["strtabs"][".strtab"]
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
                sym_name = strtab[sym_name]
            elif section_name == ".dynsym": 
                sym_name = dynsym[sym_name] 
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

def decode_unsigned_leb(buffer):
    l = 0L
    while True: 
        part = ord(buffer.read(1)) 
        #stream end, high order is 0
        if not part & 0x80:
            l += part
            break 
        #remove the hight order 
        l = l << 7 + part & 0x7f
    return l 

def encode_unsigned_leb(integer):
    pc = StringIO()
    bits_count = 1 
    while True:
        if (integer >> bits_count) == 0:
            break
        bits_count += 1 
    last = bits_count - 7
    for i in range(0, bits_count -6, 7): 
        val = (integer & (0x7fL << i)) >> i 
        #set hight order 
        if (not bits_count % 7) and (i == last):
            pc.write(chr(val))
        else:
            pc.write(chr(val | 0x80))
    if bits_count % 7:
        pc.write(chr(integer >> (bits_count - bits_count % 7))) 
    final = pc.getvalue()
    pc.close()
    return final
    

def read_debuginfo(buffer):
    #sanity check
    sections = elf["sections"] 
    section_names = [x["name"] for x in sections]
    debug_sections = {}
    debug_list = [".debug_info", ".debug_abbrev", ".debug_str", ".debug_line"]
    for i in debug_list:
        if i not in section_names:
            raise Exception("where is section: %s" % i) 
    debug_info = sections[section_names.index(debug_list[0])] 
    debug_abbrev = sections[section_names.index(debug_list[1])]
    debug_str =sections[section_names.index(debug_list[2])]
    debug_line = sections[section_names.index(debug_list[3])] 
    #get CU addr list
    cu_addrs = []
    section_end = debug_info["offset"] + debug_info["size"] 
    buffer.seek(debug_info["offset"])
    while True:
        cur = buffer.tell()
        if cur >= section_end: 
            break
        cu_addrs.append(cur) 
        buffer.seek(string_to_unsigned(_read(ELF32)), 1) 
    #read CU header
    cus = [] 
    for cu_addr in cu_addrs:    
        buffer.seek(cu_addr) 
        unit_length = string_to_unsigned(_read(ELF32))
        version = string_to_unsigned(_read(ELF16)) 
        abbrev_offset = string_to_unsigned(_read(ELF32))
        addr_size = string_to_signed(_read(ELF8)) 
        cus.append({
            "length": unit_length,
            "version": version,
            "abbrev_offset": abbrev_offset,
            "addr_size": addr_size, 
            "data_formats": [],
            "data_offset": buffer.tell(),
            "data": {},
            }) 

    #read tag tree in a CU
    tree = [] 
    for cu in cus: 
        buffer.seek(cu["abbrev_offset"]+debug_abbrev["offset"]) 
        level = []
        cur = [[], [], tree] 
        levels = [level] 
        while True: 
            abbrev = decode_unsigned_leb(buffer) 
            #NULL entry, siblings end
            if not abbrev:
                #back to father, break if no father 
                if not cur[2]:
                    break
                level = cur[2] 
                continue
            tag_name = TAG_types[decode_unsigned_leb(buffer)] 
            children = string_to_unsigned(_read(1))
            #[[self], [children], father] 
            attrs = []
            cur[0].extend([abbrev, tag_name,  children, attrs]) 
            #read attrs
            while True:
                attr_type = decode_unsigned_leb(buffer)
                attr_form = decode_unsigned_leb(buffer)
                #attr list end
                if not (attr_type or attr_form): 
                    break 
                print AT_types[attr_type], FORM_types[attr_form] 
                attrs.append((attr_type, attr_form)) 
            level.append(cur)
            if children:
                #add children 
                level = cur[1] 
                levels.append(level)
                #remember father 
                cur = [[], [], cur] 
            else:
                cur = [[], [], []] 
        tree.append(levels) 
    pdb.set_trace()
    found_str = False
    strtab = None
    if not isinstance(debug_str, str):
        strtab = build_strtab(buffer, debug_str)        
        found_str = True
    for cu in cus:
        buffer.seek(cu["data_offset"])
        formats = cu["data_formats"]
        abbrev = decode_unsigned_leb(buffer)
        for df in formats:
            length = attr_form_to_len[df[1]] 
            value = None 
            if length < 0xfff1:
                value = string_to_unsigned(_read(length)) 
            #c string
            elif length == 0xfff1:
                strbuffer = StringIO()
                while True:
                    c = _read(ELF8)
                    if c=="\x00":
                        break
                    strbuffer.write(c) 
                value = strbuffer.getvalue()
                strbuffer.close()
            #uleb
            elif length == 0xfff2:
                value = decode_unsigned_leb(buffer)
            #sleb
            elif length == 0xfff3:
                value = decode_unsigned_leb(buffer)
            #in strtab
            if df[0] == DW_AT_name:
                if found_str and (df[1] == DW_FORM_strp):
                    value = strtab[value]
            cu["data"][df[0]] = value 
        """
        if 0x10 in cu["data"]: 
            read_debugline(buffer, debug_line["offset"], cu)
        """
    elf["compile_units"] = cus        

def read_debugline(buffer,debugline_offset, cu):
    buffer.seek(debugline_offset)
    buffer.seek(cu["data"][0x10], 1) 
    print hex(buffer.tell())
    unit_len = string_to_unsigned(_read(ELF32)) 
    stop_point = buffer.tell() + unit_len
    version = string_to_unsigned(_read(ELF16))
    header_len = string_to_unsigned(_read(ELF32))
    mini_ins_len = string_to_unsigned(_read(ELF8))
    #max_op_per_ins =string_to_unsigned(_read(ELF8))
    default_is_stmt = string_to_unsigned(_read(ELF8))
    line_base = string_to_unsigned(_read(ELF8))
    line_range = string_to_unsigned(_read(ELF8))
    op_base = string_to_unsigned(_read(ELF8))
    opargs_array = []
    opargs_array_len = op_base - 1
    start = 1
    while start <= opargs_array_len: 
        opargs_array.append(string_to_unsigned(_read(ELF8)))
        start += 1        
    str_buffer = StringIO()    
    while True:
        c = _read(ELF8) 
        if c == "\x00":
            back = buffer.tell()
            if _read(ELF8) == "\x00":
                break
            else:
                buffer.seek(back) 
        str_buffer.write(c)
    include_dirs = str_buffer.getvalue().split("\x00")
    str_buffer.close()
    file_names = []
    str_buffer = StringIO() 
    while True: 
        dir_index = 0
        mtime = 0
        file_len = 0 
        c = _read(ELF8)
        if c == "\x00":
            dir_index = string_to_unsigned(_read(ELF8)) 
            mtime = string_to_unsigned(_read(ELF8)) 
            file_len = string_to_unsigned(_read(ELF8)) 
            file_names.append((
                str_buffer.getvalue(),
                dir_index,
                mtime,
                file_len))
            str_buffer.truncate(0)
            back = buffer.tell()
            if _read(ELF8) == "\x00":
                break
            else:
                buffer.seek(back)
            continue
        str_buffer.write(c)
    str_buffer.close()
    #exec opcode
    reg_address = 0
    reg_line = 1
    reg_op_index = 0
    reg_file = 1
    reg_row  = 0
    is_stmt = default_is_stmt
    reg_column = 0
    reg_basic_block = False
    reg_prologue_end = False
    reg_epilogue_begin = False
    reg_discriminator = 0 
    reg_fixed = False
    reg_ext_end = 0
    oparg = 0 
    while True:
        if buffer.tell() == stop_point:
            break
        op = string_to_signed(_read(ELF8))   
        print "op", hex(op), op
        if op == DW_LNS_copy: 
            next = string_to_unsigned(_read(ELF8))
            if next == 1: 
                #sequences end, reset registers 
                reg_address = 0
                reg_line = 1
                reg_op_index = 0
                reg_file = 1
                reg_row  = 0
                is_stmt = default_is_stmt
                reg_column = 0
                reg_basic_block = False
                reg_prologue_end = False
                reg_epilogue_begin = False
                reg_discriminator = 0 
                reg_fixed = False
                reg_ext_end = 0 
            else: 
                op = next
                reg_row += 1
                reg_discriminator = 0
                reg_basic_block = False
                reg_prologue_end = False
                reg_epilogue_begin = False 
        if op > DW_LNS_set_isa:
            #special ops 
            operation_advance = (op - op_base) / line_range
            reg_address += operation_advance
            #reg_op_index += operation_advance
            reg_line += line_base + (op - op_base) % line_range 

        elif op == DW_LNS_advance_pc: 
            if reg_fixed:
                reg_address = string_to_unsigned(_read(ELF64)) 
                reg_fixed = False 
            else:
                reg_address += string_to_unsigned(_read(ELF16)) 
        elif op == DW_LNS_advance_line: 
            reg_line += string_to_unsigned(_read(ELF8)) 
        elif op == DW_LNS_set_file:
            reg_file = string_to_unsigned(_read(ELF8)) 
        elif op == DW_LNS_set_column:
            reg_column = string_to_unsigned(_read(ELF8)) 
        elif op == DW_LNS_negate_stmt:
            is_stmt = not is_stmt 
        elif op == DW_LNS_set_basic_block:
            reg_basic_block = True
        elif op == DW_LNS_const_add_pc:
            reg_address += (255 - op_base) / line_range 
        elif op == DW_LNS_fixed_advance_pc:
            reg_fixed = True
        elif op == DW_LINE_set_address:
            reg_address = string_to_unsigned(_read(ELF64)) 
        elif op == DW_LINE_define_file:
            pass 

        
def read_debugabbr(buffer):
    sections = elf["sections"]
    debug_abbr = ".debug_abbrev"
    if debug_abbr not in sections:
        assert False, "where is the section .debug_abbrev?"
    debug_abbr = sections[".debug_abbrev"]
    buffer.seek(debug_abbr["offset"])
 
def set_target(path, flags): 
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
        "compile_units": []
        } 
    f = open(path, "rb")
    buffer = mmap.mmap(f.fileno(), 0, mmap.MAP_PRIVATE, mmap.PROT_READ)
    _read = buffer.read
    if flags & ELF_HEADER:
        read_header(buffer) 
        read_section_header(buffer)
        read_program_header(buffer)
        #print_mem_usage("after headers")
        read_strtab(buffer) 
    if flags & ELF_SYMBOL: 
        #print_mem_usage("after strtab")
        read_symtab(buffer) 
    if flags & ELF_DYNAMIC:
        #print_mem_usage("after symtab")
        read_dynamic(buffer) 
    if flags & ELF_RELA:
        read_rela(buffer)
    if flags & DWARF_INFO: 
        read_debuginfo(buffer) 
    buffer.close()
    f.close()
    return elf

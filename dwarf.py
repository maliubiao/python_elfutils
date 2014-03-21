import elfutils

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

def decode_unsigned_leb(buffer):
    l = 0L 
    while True: 
        part = ord(buffer.read(1)) 
        #stream end, high order is 0
        if not part & 0x80:
            l = (l << 7) + part
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
    

def get_CU_offsets(buffer, debug_info): 
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
    return cu_addrs

def read_CU_headers(buffer, cu_addrs):
    cu_headers = [] 
    for cu_addr in cu_addrs:    
        buffer.seek(cu_addr) 
        unit_length = string_to_unsigned(_read(ELF32))
        version = string_to_unsigned(_read(ELF16)) 
        abbrev_offset = string_to_unsigned(_read(ELF32))
        addr_size = string_to_signed(_read(ELF8)) 
        cu_headers.append({
            "length": unit_length,
            "version": version,
            "abbrev_offset": abbrev_offset,
            "addr_size": addr_size, 
            "data_formats": [],
            "data_offset": buffer.tell(),
            "data": {},
            }) 
    return cu_headers

def read_CU_format_tree(buffer, cu_headers, debug_abbrev):
    for cu in cu_headers: 
        buffer.seek(cu["abbrev_offset"]+debug_abbrev["offset"]) 
        level = []
        cur = [[], [], []] 
        #tree depth
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
                #print AT_types[attr_type], FORM_types[attr_form] 
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
        cu["data_formats"] = levels
    return cu_headers

def read_by_formats(buffer, formats, strtab): 
    attrs_list = []
    for format in formats:
        length = attr_form_to_len[format[1]] 
        value = None 
        if length < 0xfff1:
            value = string_to_unsigned(_read(length)) 
        #c string
        elif length == 0xfff1:
            strbuffer = StringIO()
            while True:
                c = _read(ELF8)
                if c == "\x00":
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
        if format[0] == DW_AT_name:
            if format[1] == DW_FORM_strp:
                value = strtab[value]
        attrs_list.append((format[0], value))
    return attrs_list

def read_CU_data_tree(buffer, cu_headers, debug_str): 
    strtab = build_strtab(buffer, debug_str)        
    for cu in cu_headers:
        buffer.seek(cu["data_offset"])
        formats = cu["data_formats"]
        tree = formats[0][0] 
        nodes = [tree] 
        level = [] 
        i = 0                               
        while i < len(nodes): 
            #read attrs of this node 
            node = nodes[i]
            #read abbrev
            abbrev = decode_unsigned_leb(buffer) 
            #read formats
            pdb.set_trace()
            attrs_list = read_by_formats(buffer,  node[0][3], strtab) 
            #if children, iter over children 
            if node[1]: 
                level.append((nodes, i+i)) 
                nodes = node[1] 
                i = 0
                continue
            #next node in nodes
            i += 1 
            #if this is the last node, go upper
            if i == len(nodes):
                if not level:
                    break
                nodes, index = level.pop() 
                i = index 

def read_debuginfo(buffer):
    #sanity check
    sections = elf["sections"] 
    debug_list = [".debug_info", ".debug_abbrev",
            ".debug_str", ".debug_line"] 
    
    sections = get_sections(debug_list, sections)
    if len(sections) != len(debug_list):
        raise Exception("need section %s" % str(debug_list))

    debug_info, debug_abbrev, debug_str, debug_line = sections
    cu_addrs = get_CU_offsets(buffer, debug_info)
    cu_headers = read_CU_headers(buffer, cu_addrs)
    #read tag tree in a CU 
    read_CU_format_tree(buffer, cu_headers, debug_abbrev)
    read_CU_data_tree(buffer, cu_headers, debug_str)



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



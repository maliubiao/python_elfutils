python-elfutils
===============
#Demo 
```shell
python readelf.py --help 
usage: readelf.py [option] exectuable
Options are:
    -d Display the dynamic section (if present)
    -h Display the ELF file header
    -l Display the program headers
    -r Display the relocations (if present)
    -S Display the section's header
    -s Display the symbol table 
```		
```shell
python readelf.py -l baseutils.so
in elf header:
file ident:                   ELFCLASS64          
file encoding:                ELFDATA2LSB         
file version:                 1                   
elf type:                     ET_DYN              
elf machine type:             EM_X86_64           
elf version:                  1                   
elf entry:                    0x8d0               
program header offset:        0x40                
section header offset:        0x3af0              
elf flags:                    0                   
elf header size:              64                  
program entry size:           56                  
program entry number:         7                   
section entry size:           64                  
section entry number:         37                  
index of .strtab:             34  
```
```shell
python readelf.py -d baseutils.so
DT_NEEDED           libpython2.7.so.1.0           
DT_NEEDED           libpthread.so.0               
DT_NEEDED           libc.so.6                     
DT_INIT             0x828           
DT_FINI             0xaa0           
DT_INIT_ARRAY       0x200dc0        
DT_INIT_ARRAYSZ     0x8             
DT_FINI_ARRAY       0x200dc8        
DT_FINI_ARRAYSZ     0x8             
DT_HASH             0x1f0           
DT_GNU_HASH         0x290           
DT_STRTAB           0x4b0           
DT_SYMTAB           0x2d0           
DT_STRSZ            0x14a           
DT_SYMENT           0x18            
DT_PLTGOT           0x201000        
DT_PLTRELSZ         0xa8            
DT_PLTREL           0x7             
DT_JMPREL           0x780           
DT_RELA             0x648           
DT_RELASZ           0x138           
DT_RELAENT          0x18            
DT_VERNEED          0x628           
DT_VERNEEDNUM       0x1             
DT_VERSYM           0x5fa           
DT_RELACOUNT        0x6             
DT_NULL             0x0 
```
```shell
python readelf.py -l baseutils.so 
Type      Align     Offset    VirtAddr  PhysAddr  FileSize  MemSize   Flags
LOAD      0x200000  0x0       0x0       0x0       0xb9c     0xb9c     PF_R + PF_X
LOAD      0x200000  0xdc0     0x200dc0  0x200dc0  0x340     0x348     PF_R + PF_W
DYNMAIC   0x8       0xdd8     0x200dd8  0x200dd8  0x1f0     0x1f0     PF_R + PF_W
NOTE      0x4       0x1c8     0x1c8     0x1c8     0x24      0x24      PF_R 
FRAME     0x4       0xaf0     0xaf0     0xaf0     0x24      0x24      PF_R 
STACK     0x8       0x0       0x0       0x0       0x0       0x0       PF_R + PF_W
RELRO     0x1       0xdc0     0x200dc0  0x200dc0  0x240     0x240     PF_R 
``` 
```shell
python readelf.py -S baseutils.so
Name                Type           Addr      Offset    
		Size      Link      Info      AlignEntsizeFlag                
0                   SHT_NULL       0x0       0x0       
		0x0       0x0       0x0       0x0  0x0                      
.note.gnu.build-id  SHT_NOTE       0x1c8     0x1c8     
		0x24      0x0       0x0       0x4  0x0  SHF_ALLOC           
.hash               SHT_HASH       0x1f0     0x1f0     
		0x9c      0x4       0x0       0x8  0x4  SHF_ALLOC           
.gnu.hash           SHT_GNU_HASH   0x290     0x290     
		0x3c      0x4       0x0       0x8  0x0  SHF_ALLOC           
.dynsym             SHT_DYNSYM     0x2d0     0x2d0     
		0x1e0     0x5       0x2       0x8  0x18 SHF_ALLOC           
.dynstr             SHT_STRTAB     0x4b0     0x4b0     
		0x14a     0x0       0x0       0x1  0x0  SHF_ALLOC           
.gnu.version        SHT_GNU_versym 0x5fa     0x5fa     
		0x28      0x4       0x0       0x2  0x2  SHF_ALLOC           
.gnu.version_r      SHT_GNU_verneed0x628     0x628     
		0x20      0x5       0x1       0x8  0x0  SHF_ALLOC           
.rela.dyn           SHT_RELA       0x648     0x648     
		0x138     0x4       0x0       0x8  0x18 SHF_ALLOC           
.rela.plt           SHT_RELA       0x780     0x780     
		0xa8      0x4       0xb       0x8  0x18 SHF_ALLOC           
.init               SHT_PROGBITS   0x828     0x828     
		0x1a      0x0       0x0       0x4  0x0  SHF_ALLOC+SHF_EXECINSTR
.plt                SHT_PROGBITS   0x850     0x850     
		0x80      0x0       0x0       0x10 0x10 SHF_ALLOC+SHF_EXECINSTR
.text               SHT_PROGBITS   0x8d0     0x8d0     
		0x1d0     0x0       0x0       0x10 0x0  SHF_ALLOC+SHF_EXECINSTR
.fini               SHT_PROGBITS   0xaa0     0xaa0     
		0x9       0x0       0x0       0x4  0x0  SHF_ALLOC+SHF_EXECINSTR
.rodata             SHT_PROGBITS   0xaa9     0xaa9     
		0x47      0x0       0x0       0x1  0x1  SHF_ALLOC+SHF_MERGE+SHF_STRINGS
.eh_frame_hdr       SHT_PROGBITS   0xaf0     0xaf0     
		0x24      0x0       0x0       0x4  0x0  SHF_ALLOC           
.eh_frame           SHT_PROGBITS   0xb18     0xb18     
		0x84      0x0       0x0       0x8  0x0  SHF_ALLOC           
.init_array         SHT_INIT_ARRAY 0x200dc0  0xdc0     
		0x8       0x0       0x0       0x8  0x0  SHF_WRITE+SHF_ALLOC 
.fini_array         SHT_FINI_ARRAY 0x200dc8  0xdc8     
		0x8       0x0       0x0       0x8  0x0  SHF_WRITE+SHF_ALLOC 
.jcr                SHT_PROGBITS   0x200dd0  0xdd0     
		0x8       0x0       0x0       0x8  0x0  SHF_WRITE+SHF_ALLOC 
.dynamic            SHT_DYNAMIC    0x200dd8  0xdd8     
		0x1f0     0x5       0x0       0x8  0x10 SHF_WRITE+SHF_ALLOC 
.got                SHT_PROGBITS   0x200fc8  0xfc8     
		0x38      0x0       0x0       0x8  0x8  SHF_WRITE+SHF_ALLOC 
.got.plt            SHT_PROGBITS   0x201000  0x1000    
		0x50      0x0       0x0       0x8  0x8  SHF_WRITE+SHF_ALLOC 
.data               SHT_PROGBITS   0x201060  0x1060    
		0xa0      0x0       0x0       0x20 0x0  SHF_WRITE+SHF_ALLOC 
.bss                SHT_NOBITS     0x201100  0x1100    
		0x8       0x0       0x0       0x4  0x0  SHF_WRITE+SHF_ALLOC 
.comment            SHT_PROGBITS   0x0       0x1100    
		0x42      0x0       0x0       0x1  0x1  SHF_MERGE+SHF_STRINGS
.comment.SUSE.OPTs  SHT_PROGBITS   0x0       0x1142    
		0x6       0x0       0x0       0x1  0x1  SHF_MERGE+SHF_STRINGS
.debug_aranges      SHT_PROGBITS   0x0       0x1150    
		0xb0      0x0       0x0       0x10 0x0                      
.debug_info         SHT_PROGBITS   0x0       0x1200    
		0x14ed    0x0       0x0       0x1  0x0                      
.debug_abbrev       SHT_PROGBITS   0x0       0x26ed    
		0x23d     0x0       0x0       0x1  0x0                      
.debug_line         SHT_PROGBITS   0x0       0x292a    
		0x232     0x0       0x0       0x1  0x0                      
.debug_str          SHT_PROGBITS   0x0       0x2b5c    
		0xb0a     0x0       0x0       0x1  0x1  SHF_MERGE+SHF_STRINGS
.debug_loc          SHT_PROGBITS   0x0       0x3666    
		0x2aa     0x0       0x0       0x1  0x0                      
.debug_ranges       SHT_PROGBITS   0x0       0x3910    
		0x80      0x0       0x0       0x10 0x0                      
.shstrtab           SHT_STRTAB     0x0       0x3990    
		0x15e     0x0       0x0       0x1  0x0                      
.symtab             SHT_SYMTAB     0x0       0x4430    
		0x6d8     0x24      0x37      0x8  0x18                     
.strtab             SHT_STRTAB     0x0       0x4b08    
		0x26e     0x0       0x0       0x1  0x0           
```
```shell
python readelf.py -s baseutils.so
in .dynsym
addr           type      visiblity bind      name                
0x0            NOTYPE    DEFAULT   LOCAL     0                   
0x828          SECTION   DEFAULT   LOCAL     0                   
0x0            NOTYPE    DEFAULT   WEAK      _ITM_deregisterTMCloneTable
0x0            FUNC      DEFAULT   GLOBAL    Py_InitModule4_64   
0x0            FUNC      DEFAULT   GLOBAL    PyErr_SetString     
0x0            OBJECT    DEFAULT   GLOBAL    PyExc_TypeError     
0x0            NOTYPE    DEFAULT   WEAK      __gmon_start__      
0x0            FUNC      DEFAULT   GLOBAL    PyString_Size       
0x0            FUNC      DEFAULT   GLOBAL    PyArg_ParseTuple    
0x0            OBJECT    DEFAULT   GLOBAL    PyExc_AssertionError
0x0            FUNC      DEFAULT   GLOBAL    PyInt_FromLong      
0x0            NOTYPE    DEFAULT   WEAK      _Jv_RegisterClasses 
0x0            NOTYPE    DEFAULT   WEAK      _ITM_registerTMCloneTable
0x0            FUNC      DEFAULT   WEAK      __cxa_finalize      
0x201100       NOTYPE    DEFAULT   GLOBAL    _edata              
0xa80          FUNC      DEFAULT   GLOBAL    initbaseutils       
0x201108       NOTYPE    DEFAULT   GLOBAL    _end                
0x201100       NOTYPE    DEFAULT   GLOBAL    __bss_start         
0x828          FUNC      DEFAULT   GLOBAL    _init               
0xaa0          FUNC      DEFAULT   GLOBAL    _fini               


in .symtab
addr           type      visiblity bind      name                
0x0            NOTYPE    DEFAULT   LOCAL     0                   
0x1c8          SECTION   DEFAULT   LOCAL     0                   
0x1f0          SECTION   DEFAULT   LOCAL     0                   
0x290          SECTION   DEFAULT   LOCAL     0                   
0x2d0          SECTION   DEFAULT   LOCAL     0                   
0x4b0          SECTION   DEFAULT   LOCAL     0                   
0x5fa          SECTION   DEFAULT   LOCAL     0                   
0x628          SECTION   DEFAULT   LOCAL     0                   
0x648          SECTION   DEFAULT   LOCAL     0                   
0x780          SECTION   DEFAULT   LOCAL     0                   
0x828          SECTION   DEFAULT   LOCAL     0                   
0x850          SECTION   DEFAULT   LOCAL     0                   
0x8d0          SECTION   DEFAULT   LOCAL     0                   
0xaa0          SECTION   DEFAULT   LOCAL     0                   
0xaa9          SECTION   DEFAULT   LOCAL     0                   
0xaf0          SECTION   DEFAULT   LOCAL     0                   
0xb18          SECTION   DEFAULT   LOCAL     0                   
0x200dc0       SECTION   DEFAULT   LOCAL     0                   
0x200dc8       SECTION   DEFAULT   LOCAL     0                   
0x200dd0       SECTION   DEFAULT   LOCAL     0                   
0x200dd8       SECTION   DEFAULT   LOCAL     0                   
0x200fc8       SECTION   DEFAULT   LOCAL     0                   
0x201000       SECTION   DEFAULT   LOCAL     0                   
0x201060       SECTION   DEFAULT   LOCAL     0                   
0x201100       SECTION   DEFAULT   LOCAL     0                   
0x0            SECTION   DEFAULT   LOCAL     0                   
0x0            SECTION   DEFAULT   LOCAL     0                   
0x0            SECTION   DEFAULT   LOCAL     0                   
0x0            SECTION   DEFAULT   LOCAL     0                   
0x0            SECTION   DEFAULT   LOCAL     0                   
0x0            SECTION   DEFAULT   LOCAL     0                   
0x0            SECTION   DEFAULT   LOCAL     0                   
0x0            SECTION   DEFAULT   LOCAL     0                   
0x0            SECTION   DEFAULT   LOCAL     0                   
0x0            FILE      DEFAULT   LOCAL     crtstuff.c          
0x200dd0       OBJECT    DEFAULT   LOCAL     __JCR_LIST__        
0x8d0          FUNC      DEFAULT   LOCAL     deregister_tm_clones
0x900          FUNC      DEFAULT   LOCAL     register_tm_clones  
0x940          FUNC      DEFAULT   LOCAL     __do_global_dtors_aux
0x201100       OBJECT    DEFAULT   LOCAL     completed.6121      
0x200dc8       OBJECT    DEFAULT   LOCAL     __do_global_dtors_aux_fini_array_entry
0x980          FUNC      DEFAULT   LOCAL     frame_dummy         
0x200dc0       OBJECT    DEFAULT   LOCAL     __frame_dummy_init_array_entry
0x0            FILE      DEFAULT   LOCAL     baseutils.c         
0x9b0          FUNC      DEFAULT   LOCAL     baseutils_strtoint  
0x2010c0       OBJECT    DEFAULT   LOCAL     baseutils_methods   
0x201080       OBJECT    DEFAULT   LOCAL     baseutils_strtoint_doc
0x0            FILE      DEFAULT   LOCAL     crtstuff.c          
0xb98          OBJECT    DEFAULT   LOCAL     __FRAME_END__       
0x200dd0       OBJECT    DEFAULT   LOCAL     __JCR_END__         
0x0            FILE      DEFAULT   LOCAL     0                   
0x201060       OBJECT    DEFAULT   LOCAL     __dso_handle        
0x200dd8       OBJECT    DEFAULT   LOCAL     _DYNAMIC            
0x201100       OBJECT    DEFAULT   LOCAL     __TMC_END__         
0x201000       OBJECT    DEFAULT   LOCAL     _GLOBAL_OFFSET_TABLE_
0x0            NOTYPE    DEFAULT   WEAK      _ITM_deregisterTMCloneTable
0x0            FUNC      DEFAULT   GLOBAL    Py_InitModule4_64   
0x201100       NOTYPE    DEFAULT   GLOBAL    _edata              
0xaa0          FUNC      DEFAULT   GLOBAL    _fini               
0xa80          FUNC      DEFAULT   GLOBAL    initbaseutils       
0x0            FUNC      DEFAULT   GLOBAL    PyErr_SetString     
0x0            OBJECT    DEFAULT   GLOBAL    PyExc_TypeError     
0x0            NOTYPE    DEFAULT   WEAK      __gmon_start__      
0x0            FUNC      DEFAULT   GLOBAL    PyString_Size       
0x201108       NOTYPE    DEFAULT   GLOBAL    _end                
0x0            FUNC      DEFAULT   GLOBAL    PyArg_ParseTuple    
0x0            OBJECT    DEFAULT   GLOBAL    PyExc_AssertionError
0x201100       NOTYPE    DEFAULT   GLOBAL    __bss_start         
0x0            FUNC      DEFAULT   GLOBAL    PyInt_FromLong      
0x0            NOTYPE    DEFAULT   WEAK      _Jv_RegisterClasses 
0x0            NOTYPE    DEFAULT   WEAK      _ITM_registerTMCloneTable
0x0            FUNC      DEFAULT   WEAK      __cxa_finalize@@GLIBC_2.2.5
0x828          FUNC      DEFAULT   GLOBAL    _init         
``` 
```shell 
python readelf.py -r baseutils.so 
in .rela.plt
offset    type           Addend    Sym.Index Sym.Name  
0x202018  R_386_JMP_SLOT 0         2         PyDict_SetItemString
0x202020  R_386_JMP_SLOT 0         4         Py_InitModule4_64
0x202028  R_386_JMP_SLOT 0         5         PyErr_SetString
0x202030  R_386_JMP_SLOT 0         7         __gmon_start__
0x202038  R_386_JMP_SLOT 0         8         PyString_Size
0x202040  R_386_JMP_SLOT 0         9         PyArg_ParseTuple
0x202048  R_386_JMP_SLOT 0         11        PyDict_New
0x202050  R_386_JMP_SLOT 0         12        PyInt_FromLong
0x202058  R_386_JMP_SLOT 0         15        __cxa_finalize
in .rela.dyn
offset    type           Addend    Sym.Index Sym.Name  
0x201dc0  R_386_RELATIVE 2736      0         unknown   
0x201dc8  R_386_RELATIVE 2672      0         unknown   
0x202060  R_386_RELATIVE 2105440   0         unknown   
0x2020e0  R_386_RELATIVE 3572      0         unknown   
0x2020e8  R_386_RELATIVE 3216      0         unknown   
0x2020f8  R_386_RELATIVE 2105472   0         unknown   
0x202100  R_386_RELATIVE 3503      0         unknown   
0x202108  R_386_RELATIVE 3008      0         unknown   
0x202118  R_386_RELATIVE 2105504   0         unknown   
0x202120  R_386_RELATIVE 3601      0         unknown   
0x202128  R_386_RELATIVE 2784      0         unknown   
0x202138  R_386_RELATIVE 2105536   0         unknown   
0x201fc8  R_386_GLOB_DAT 0         3         _ITM_deregisterTMCloneTable
0x201fd0  R_386_GLOB_DAT 0         6         PyExc_TypeError
0x201fd8  R_386_GLOB_DAT 0         7         __gmon_start__
0x201fe0  R_386_GLOB_DAT 0         10        PyExc_AssertionError
0x201fe8  R_386_GLOB_DAT 0         13        _Jv_RegisterClasses
0x201ff0  R_386_GLOB_DAT 0         14        _ITM_registerTMCloneTable
0x201ff8  R_386_GLOB_DAT 0         15        __cxa_finalize
```
```shell	
python readelf.py -p baseutils.so .strtab

000000: 0x00 c r t s t u f f . c 0x00 _ _ J C R _ L I S T _ _ 0x00 d e r e g i s
000020: t e r _ t m _ c l o n e s 0x00 r e g i s t e r _ t m _ c l o n e s
000040: 0x00 _ _ d o _ g l o b a l _ d t o r s _ a u x 0x00 c o m p l e t e d
000060: . 6 1 2 1 0x00 _ _ d o _ g l o b a l _ d t o r s _ a u x _ f i n i
000080: _ a r r a y _ e n t r y 0x00 f r a m e _ d u m m y 0x00 _ _ f r a m e
0000a0: _ d u m m y _ i n i t _ a r r a y _ e n t r y 0x00 b a s e u t i l
0000c0: s . c 0x00 b a s e u t i l s _ g e t _ t y p e s _ l e n g t h 0x00 b
0000e0: a s e u t i l s _ s t r i n g _ t o _ s i g n e d 0x00 b a s e u t
000100: i l s _ s t r i n g _ t o _ u n s i g n e d 0x00 b a s e u t i l s
000120: _ m e t h o d s 0x00 b a s e u t i l s _ s t r i n g _ t o _ u n s
000140: i g n e d _ d o c 0x00 b a s e u t i l s _ s t r i n g _ t o _ s i
000160: g n e d _ d o c 0x00 b a s e u t i l s _ g e t _ t y p e s _ l e n
000180: g t h _ d o c 0x00 _ _ F R A M E _ E N D _ _ 0x00 _ _ J C R _ E N D _
0001a0: _ 0x00 _ _ d s o _ h a n d l e 0x00 _ D Y N A M I C 0x00 _ _ T M C _ E N
0001c0: D _ _ 0x00 _ G L O B A L _ O F F S E T _ T A B L E _ 0x00 P y D i c t
0001e0: _ S e t I t e m S t r i n g 0x00 _ I T M _ d e r e g i s t e r T M
000200: C l o n e T a b l e 0x00 P y _ I n i t M o d u l e 4 _ 6 4 0x00 _ e d
000220: a t a 0x00 _ f i n i 0x00 i n i t b a s e u t i l s 0x00 P y E r r _ S e
000240: t S t r i n g 0x00 P y E x c _ T y p e E r r o r 0x00 _ _ g m o n _ s
000260: t a r t _ _ 0x00 P y S t r i n g _ S i z e 0x00 _ e n d 0x00 P y A r g _
000280: P a r s e T u p l e 0x00 P y E x c _ A s s e r t i o n E r r o r 0x00
0002a0: _ _ b s s _ s t a r t 0x00 P y D i c t _ N e w 0x00 P y I n t _ F r o
0002c0: m L o n g 0x00 _ J v _ R e g i s t e r C l a s s e s 0x00 _ I T M _ r
0002e0: e g i s t e r T M C l o n e T a b l e 0x00 _ _ c x a _ f i n a l i
000300: z e @ @ G L I B C _ 2 . 2 . 5 0x00 _ i n i t 0x00
```

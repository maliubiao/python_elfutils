python-elfutils
===============
#Demo 
```shell
python readelf.py --help 
usage: readelf.py exectuable
Options are:
    -d Display the dynamic section (if present)
    -h Display the ELF file header
    -l Display the program headers
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

```

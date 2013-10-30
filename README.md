python-elfutils
===============
#Demo
```shell
python elf.py /usr/local/bin/nginx
in .dynsym 
0x0       getenv                        
0x0       sigprocmask                   
0x0       raise                         
0x0       empty                         
0x0       recv                          
0x0       localtime                     
0x0       abort                         
0x0       __errno_location              
0x0       srandom                       
0x0       unlink                        
0x0       strncmp                       
0x0       _ITM_deregisterTMCloneTable   
0x0       localtime_r                   
0x0       mkdir                         
0x0       sendmsg                       
0x0       writev 
...
in .symtab
...
0x403440  ngx_set_env                   
0x4034bc  ngx_set_cpu_affinity          
0x403624  ngx_set_priority              
0x4036a9  ngx_set_user                  
0x4037ce  ngx_set_worker_processes      
0x40383a  ngx_core_module_init_conf     
0x403b6d  ngx_write_stderr              
0x403b98  ngx_core_module_create_conf   
0x68dd58  ngx_show_version              
0x68dd60  ngx_show_help                 
0x68dd68  ngx_show_configure            
0x68dd70  ngx_prefix                    
0x68dd80  ngx_conf_file                 
0x68dd88  ngx_conf_params               
0x68dd78  ngx_signal                    
0x68dd90  ngx_os_environ                
0x67f560  ngx_core_module_ctx           
0x67f580  ngx_core_commands             
0x67f900  ngx_debug_points              
0x0       ngx_log.c       

import elfutils
import pprint

elf = elfutils.readelf("/bin/ls", elfutils.ELF_HEADER)
pprint.pprint(elf)

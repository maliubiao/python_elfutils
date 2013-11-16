from baseutils import string_to_unsigned
from struct import unpack

src = [string_to_unsigned("\x7f"*i) for i in [2,4,8]]
dst = [ unpack("H", "\x7f"*2),
        unpack("I", "\x7f"*4),
        unpack("Q", "\x7f"*8)]

for m, n in zip(src, dst): 
    if m != n[0]:
        print m, n[0]
        print "test failed"
        exit(0)

print "test passed"




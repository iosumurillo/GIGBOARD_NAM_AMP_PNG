import lzma, os, subprocess

with open("scratch/Update_patched.img", "rb") as f:
    patched = f.read()

pos = patched.rfind(b"\xfd7zXZ")
dec = lzma.LZMADecompressor()
rootfs = dec.decompress(patched[pos:])

with open("scratch/test_rootfs.bin", "wb") as f:
    f.write(rootfs)

cmd = 'debugfs -R "dump /usr/Evil/Evil scratch/extracted_evil_patched" scratch/test_rootfs.bin'
subprocess.run(cmd, shell=True, check=True)

with open("scratch/extracted_evil_patched", "rb") as f:
    evil_patched = f.read()

print("extracted evil_patched len:", len(evil_patched))

off1 = 0x2190255
off2 = 0x2180c1a

with open("scratch/NAM_A2_direct_v1_exact.png", "rb") as f:
    v1_png = f.read()

with open("scratch/NAM_A2_direct_v2_exact.png", "rb") as f:
    v2_png = f.read()

slice1 = evil_patched[off1:off1+len(v1_png)]
slice2 = evil_patched[off2:off2+len(v2_png)]

print("Is off1 equal to NAM_A2_direct_v1_exact.png?", slice1 == v1_png)
print("Is off2 equal to NAM_A2_direct_v2_exact.png?", slice2 == v2_png)


ntfs=open("C:/Users/wkd58/OneDrive/바탕 화면/BoB/02. 심화교육/강의/강대명 멘토/ntfs.dd","rb+")
ntfs.seek(11)
bps=ntfs.read(2)
spc=ntfs.read(1)
bps=(int.from_bytes(bps, 'little'))
spc=(int.from_bytes(spc, 'little'))
cluster_size=bps*spc
ntfs.seek(0x30)
mft_start=ntfs.read(8)
mft_start=(int.from_bytes(mft_start, 'little'))
mft_start=mft_start*cluster_size
ntfs.seek(mft_start)            # go to mft table


ntfs.read(4)
fix_offset=ntfs.read(2)
fix_offset=(int.from_bytes(fix_offset, 'little'))
ntfs.seek(mft_start+fix_offset)
fix_sig=ntfs.read(2)
fix1=ntfs.read(2)
fix2=ntfs.read(2)

ntfs.seek(mft_start+510)
fix_target=ntfs.read(2)
if fix_sig==fix_target:
    ntfs.seek(mft_start + 510)
    print("fixup_array 수정 전:", fix_target)
    ntfs.write(fix1)
    print("fixup_array 수정 후:", fix1)
ntfs.seek(mft_start+1022)
fix_target=ntfs.read(2)

if fix_sig==fix_target:
    ntfs.seek(mft_start + 1022)
    print("fixup_array 수정 전:", fix_target)
    ntfs.write(fix2)
    print("fixup_array 수정 후:", fix2)

ntfs.seek(mft_start)
ntfs.read(20)
attribute=ntfs.read(2)
attribute=(int.from_bytes(attribute, 'little'))          #read first attribute offset
attribute_offset=mft_start+attribute
ntfs.seek(attribute_offset)
skip=0
real_address=0
while(True):
    attribute_name=ntfs.read(1)
    attribute_name = hex(int.from_bytes(attribute_name, "little"))
    ntfs.read(3)
    skip = ntfs.read(1)
    skip = (int.from_bytes(skip, "little"))
    if attribute_name == '0x80':
        ntfs.read(3)
        check_resident=ntfs.read(1)
        if check_resident==b'\x01':
            ntfs.seek(attribute_offset+32)
            runlist_offset=ntfs.read(2)
            runlist_offset = (int.from_bytes(runlist_offset, "little"))
            ntfs.seek(attribute_offset+runlist_offset)
            while(True):
                runlist=ntfs.read(1)
                if runlist==b'\x00':
                    break
                runlist = hex(int.from_bytes(runlist, "little"))
                size = runlist[2]
                length = runlist[3]
                length=ntfs.read(int(length))
                offset_size=ntfs.read(int(size))
                length = hex(int.from_bytes(length, "little"))
                offset_size = (int.from_bytes(offset_size, "little"))
                real_address = real_address + offset_size
                print("len size: ", int(length,16))
                print("offset size: ", int(real_address))
            break

    attribute_offset=attribute_offset+skip
    ntfs.seek(attribute_offset)
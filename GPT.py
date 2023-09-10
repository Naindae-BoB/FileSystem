def convert(string):
    string_list=list(string)
    string_len=len(string_list)
    for i in range(0,len(string_list),2):
        string_list[i],string_list[i+1],string_list[string_len-i-2],string_list[string_len-i-1]=string_list[string_len-i-2],string_list[string_len-i-1],string_list[i],string_list[i+1]
        if i==8:
            break
    string=''.join(string_list)
    return string

gpt=open("C:/Users/wkd58/OneDrive/바탕 화면/BoB/02. 심화교육/강의/강대명 멘토/gpt_128.dd","rb")
gpt.seek(0x3ff)  # 파일 포인터를 400바이트 위치로 이동
byte_cnt=0      #count byte
part_row=0      #count partition row
part_cnt=1      #count partition
guid=""
byte = gpt.read(1)  # 바이트 단위로 읽기
try:
    while byte:
        if byte_cnt==16:
            if part_row%8==0:           #if first partition row, print guid
                guid=guid.upper()
                print(guid, end=' ')
            if part_row%8==2:           #if third partition row, print partition offset, size and file system type
                flba = convert(guid[0:16])              #store high 16 bits in flba
                llba = convert(guid[16:32])             #store low 16 bits in llba
                converted_string1 = ""
                converted_string2 = ""
                for i in range(0, len(flba), 2):                                #make 0xaa 0xaa 0xaa
                    converted_string1 += "0x" + flba[i:i + 2] + ""
                for i in range(0, len(llba), 2):
                    converted_string2 += "0x" + llba[i:i + 2] + ""

                hex_string_no_space = converted_string1.replace('0x', '').replace(' ', '')      #make str to hex
                decimal_value = int(hex_string_no_space, 16)
                hex_flba = hex(decimal_value)
                hex_string_no_space = converted_string2.replace('0x', '').replace(' ', '')
                decimal_value = int(hex_string_no_space, 16)
                hex_llba = hex(decimal_value)

                hex_flba = int(hex_flba, 16)
                hex_llba = int(hex_llba, 16)
                partion_off=hex(hex_flba * 512)
                print(" partion{} offset:".format(part_cnt),partion_off,end='')         #print partition offset

                size = hex_llba - hex_flba +1
                print(" Size:{}MB".format(size*512/1024/1024), end=' ')          #print partition size
                current_position = gpt.tell()                                           #store current position gpt
                partion_off = int(partion_off, 16)
                gpt.seek(partion_off)                                                   #move for partition offset
                gpt.read(3)
                file_type=gpt.read(4)                                                   #store file system type

                print("File System Type:",file_type.decode())
                gpt.seek(current_position)
                part_cnt += 1

            byte = gpt.read(1)
            guid=""
            formatted_hex = format(byte[0], "02x")
            guid += formatted_hex
            byte_cnt=0
            byte_cnt+=1
            part_row+=1

            if part_row==48:            #if end of partition, break
                break

        else:
            byte = gpt.read(1)          #if not 0,2 line, just read and plus byte_cnt
            formatted_hex = format(byte[0], "02x")
            guid+=formatted_hex
            byte_cnt+=1
finally:
    gpt.close()
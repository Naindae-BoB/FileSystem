gpt=open("C:/Users/wkd58/OneDrive/바탕 화면/BoB/02. 심화교육/강의/강대명 멘토/mbr_128.dd","rb")
gpt.seek(0x1c2)
i=0
while 1:
    bytes=gpt.read(1)   #1개를 읽어 07인지 05인지 00인지 판단

    if b'\x00' in bytes:    #00이면 중단
        break
    if b'\x07' in bytes:
        print("File System Type:",hex(int.from_bytes(bytes, 'big')),end='  ')   #07일때만 출력, 05일땐 출력 안함

    gpt.read(3)                                                                 #파일시스템타입 출력 후 뒤에 3바이트 버림
    partition=gpt.read(4)                   #get start offset                   파티션의 시작 오프셋을 얻어옴
    current_postition=gpt.tell()                                                #돌아올 현재 위치 저장
    size = gpt.read(4)                      #get partition size                 파티션의 사이즈를 읽음
    gpt.seek(current_postition)                                                 #다시 파티션 오프셋을 얻는 위치로 돌아옴


    partition = partition[::-1]                                                         #리틀엔디안 to 빅엔디안
    partition_value = hex(int.from_bytes(partition, 'big'))
    partition_value = int(partition_value, 16)
    partition_Start = (int(partition_value) * 512)                                     #파티션 시작 offset을 partition_Start에 저장

    if i>=1:                                                                        #만약 ebr을 한번 지나왔으면 ebr의 첫 base에 파티션 주소를 더해 상대위치를 찾음
        partition_Start=int(partition_Start)+int(ebr_Base)
    if b'\x07' in bytes:                                                            #만약 07이면 파티션이니 파티션의 시작주소를 출력함

        print("Partition Offset:",hex(partition_Start), end='  ')                   #파티션이니 저장된 사이즈를 mb로 변환 후 출력
        size = size[::-1]
        size = int.from_bytes(size, 'big') * 512 / 1024 / 1024
        print("Size: {}MB".format(size))
    if b'\x05' in bytes:                                                            #만약 05면 ebr이니 해당 위치로 이동
        gpt.seek(partition_Start)
        if i==0:                                                                   #첫번째 ebr이면 ebr의 base로 설정
            ebr_Base=partition_Start
        else:                                                                       #첫번째가 아니면 mbr_base로 파티션을 찾을때 ebr의 시작 주소 + mbr 상대위치로 찾아줌
            mbr_Base=partition_Start
        bytes = gpt.read(450)  # move ebr
        bytes = gpt.read(1)    # read file system

        print("File System Type:",hex(int.from_bytes(bytes, 'big')),end='  ')                           #05에서 다음 ebr로 왔으니 파일시스템 출력
        gpt.read(3)
        partition = gpt.read(4)
        current_postition = gpt.tell()                                                      #파티션 위치와 사이즈정보가 있는 위치 저징
        size = gpt.read(4)  # get partition size
        gpt.seek(current_postition)
        partition = partition[::-1]
        partition_value = hex(int.from_bytes(partition, 'big'))
        partition_value = int(partition_value, 16)

        partition_Start = (int(partition_value) * 512)
        if i==0:
            partition_Start=int(ebr_Base) + int(partition_Start)                #첫 ebr이면 ebr의 base에 파티션 오프셋을 더해줌
        else:
            partition_Start = int(mbr_Base) + int(partition_Start)              #첫 ebr이 아니면 첫 ebr이 아닌 해당 ebr의 시작주소와 파티션 오프셋을 더해줌
        print("Partition Offset:", hex(partition_Start),end='  ')               #오프셋과 사이즈를 출력
        size = size[::-1]
        size = int.from_bytes(size, 'big') * 512 / 1024 / 1024                  
        print("Size: {}MB".format(size))
        i=i+1                                                               #첫 ebr인지 판단을 위해 i+1을 해줌

    if b'\x05' and b'\x07' not in bytes:
        break
    gpt.read(8)                             #8바이트를 읽어 다음 파일 시스템을 읽어옴
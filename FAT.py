fat=open("C:/Users/wkd58/OneDrive/바탕 화면/BoB/02. 심화교육/강의/강대명 멘토/fat32.dd","rb")
start_cluster = int(input("시작할 클러스터를 입력해 주세용: "))
fat.seek(11)
BPS=fat.read(2)
fat.read(1)
RSC=fat.read(2)

BPS=hex(int.from_bytes(BPS, 'little'))
RSC=hex(int.from_bytes(RSC, 'little'))
BPS = int(BPS, 16)
RSC = int(RSC, 16)
fat_start=BPS*RSC
print(start_cluster,end='')
print("->",end='')
fat.seek(fat_start)
fat.read(8)
i=0
while 1:
    if i==0:
        i=i+1
        fat.seek(fat_start+4*start_cluster)
        current_cluster = fat.read(4)
        big_current_cluster=hex(int.from_bytes(current_cluster, 'big'))
        if big_current_cluster[-2:]== '00':          #ff ff ff 0f와 ff 00 00 00을 구분
            little_current_cluster = hex(int.from_bytes(current_cluster, 'little'))
            start_cluster=current_cluster            #다음 클러스터로 이동 후 ff ff ff 0f면 종료하자
        else:
            print('0')
            break
    else:
        i = i + 1
        start_cluster=start_cluster[::-1]
        start_cluster_value = hex(int.from_bytes(start_cluster, 'big'))
        start_cluster_value = int(start_cluster_value, 16)
        print(start_cluster_value,end='')
        if i%19==0:
            print("\n")
        fat.seek(fat_start + 4 * start_cluster_value)    #주소변환
        current_cluster = fat.read(4)
        big_current_cluster = hex(int.from_bytes(current_cluster, 'big'))
        if big_current_cluster[-2:] == '00':  # ff ff ff 0f와 ff 00 00 00을 구분
            little_current_cluster = hex(int.from_bytes(current_cluster, 'little'))
            start_cluster = current_cluster  # 다음 클러스터로 이동 후 ff ff ff 0f면 종료하자
            print("->", end='')
        else:
            break
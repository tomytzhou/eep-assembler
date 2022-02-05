OPS = {
    'MOV': 0x0,
    'ADD': 0x2,
    'SUB': 0x4,
    'ADC': 0x6,
    'LDR': 0x8,
    'STR': 0xA,
    'JMP': 0xC,
    'JNE': 0xD,
    'JCS': 0xE,
    'JMI': 0xF
}
R = {
    "R0": 0x0,
    "R1": 0x1,
    "R2": 0x2,
    "R3": 0x3,
}


def findval(x):
    if x[0:2] == '0b':
        return int(x[2:], 2)
    elif x[0:2] == '0x':
        return int(x[2:], 16)
    else:
        return int(x)


f = open('assembly.txt', 'r')
a = []
for line in f:
    al = []
    for i in line.split():
        al.append(i.strip(',#'))
    a.append(al)
f.close()

f = open('assembly.ram', 'w')

pc = 0
for j in a:
    opc = OPS[j[0]]
    if j[0][0] != 'J':
        rs = R[j[1]] * 0x4
        if j[2][0] != 'R':
            opc += 0x1
            imm = findval(j[2])
        else:
            rs += R[j[2]]
            imm = 0x0
    else:
        rs = 0x0
        imm = findval(j[1])
    i = opc * 0x1000 + rs * 0x100 + imm
    print(hex(pc), hex(i))
    f.write(hex(pc))
    f.write(' ')
    f.write(hex(i))
    f.write('\n')
    pc += 1
f.close()

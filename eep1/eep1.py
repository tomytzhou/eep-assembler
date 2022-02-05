OPS = {
    'MOV': 0x0,
    'ADD': 0x1,
    'SUB': 0x2,
    'ADC': 0x3,
    'LDR': 0x8,
    'STR': 0xA,
    'JMP': 0x0,
    'JNE': 0x2,
    'JCS': 0x4,
    'JMI': 0x6
}


def findval(x):
    if x[0:2] == '0b':
        return int(x[2:], 2)
    elif x[0:2] == '0x':
        return int(x[2:], 16)
    else:
        return int(x)


def find_twos_compl(x, l):
    if x[0] == '-':
        x = findval(x[1:]) ^ int('1'*l, 2)
        return x + 1
    else:
        return findval(x)


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
        a = int(j[1][1]) * 0x2
        if j[2][0] != 'R':
            a += 0x1
            imm = find_twos_compl(j[2], 8)
        else:
            imm = int(j[2][1]) * 0x20 + (find_twos_compl(j[3], 5) if len(j) == 4 else 0)
        i = opc * 0x1000 + a * 0x100 + imm
    else:
        imm = findval(j[1])
        i = 0xF000 + opc * 0x100 + imm
    print(hex(pc), hex(i))
    f.write(hex(pc))
    f.write(' ')
    f.write(hex(i))
    f.write('\n')
    pc += 1
f.close()

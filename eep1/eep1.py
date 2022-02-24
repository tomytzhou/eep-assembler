OPS = {
    'MOV': 0x0,
    'ADD': 0x1,
    'SUB': 0x2,
    'ADC': 0x3,
    'LDR': 0x8,
    'STR': 0xA,
    'JMP': 0xC0,
    'JNE': 0xC2,
    'JCS': 0xC4,
    'JMI': 0xC6,
    'JEQ': 0xC3,
    'JCC': 0xC5,
    'JPL': 0xC7,
    'JGE': 0xC8,
    'JLT': 0xC9,
    'JGT': 0xCA,
    'JLE': 0xCB,
    'JHI': 0xCC,
    'JLS': 0xCD,
    'JSR': 0xCE,
    'RET': 0xCF,
    'SBC': 0X4,
    'AND': 0x5,
    'XOR': 0x6,
    'LSL': 0x7,
}

def rcheck(r):
    if r[0] == 'R' and 0 <= int(r[1]) <= 7:
        return True
    else:
        return False

def assemble(j):
    if j[0] == '0':
        return 0
    if j[0] not in OPS:
        return -1
    opc = OPS[j[0]]
    if j[0] == 'RET':
        return opc << 8
    elif j[0][0] != 'J':
        if rcheck(j[1]):
            a = int(j[1][1]) * 0x2
        else:
            return -2
        j[2] = j[2].strip('[]')
        if j[2][0] != 'R':
            a += 0x1
            if -128 < findval(j[2]) < 255:
                imm = find_twos_compl(j[2], 8)
            else:
                return -3
        else:
            if len(j) == 3:
                j.append('0')
            j[3] = j[3].strip(']')
            if -16 < findval(j[3]) < 15:
                if rcheck(j[2]):
                    imm = int(j[2][1]) * 0x20 + (find_twos_compl(j[3], 5))
                else:
                    return -4
            else:
                return -5
        return opc * 0x1000 + a * 0x100 + imm
    else:
        imm = addr[j[1]] if j[1] in addr else findval(j[1])
        if 0 <= imm < 255:
            return opc * 0x100 + imm
        else:
            return -2

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

def erreport(i, pc):
    if i == -1:
        print('Invalid OPC on line ', pc)
    if i == -2:
        print('Invalid Ra value on line ', pc)
    if i == -3:
        print('Invalid Imm8 value on line ', pc)
    if i == -4:
        print('Invalid Rb value on line ', pc)
    if i == -5:
        print('Invalid Imms5 value on line ', pc)


f = open('assembly.txt', 'r')
a = []
global addr
addr = {}
pc = 0
for line in f:
    al = []
    line = line.replace(',', ' ')
    for i in line.split():
        if i[-1] == ':':
            addr[i[:-1]] = pc
        elif i[0] != '/':
            al.append(i.strip('#'))
    a.append(al)
    pc += 1
f.close()

f = open('assembly.ram', 'w')

pc = 0
for j in a:
    i = assemble(j)
    if i < 0:
        erreport(i, pc)
    else:
        print(hex(pc), hex(i))
        l = hex(pc) + ' ' + hex(i) + '\n'
        f.write(l)
    pc += 1
f.close()

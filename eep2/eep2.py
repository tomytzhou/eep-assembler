OPCALU = {
    'MOV': 0x0,
    'ADD': 0x1,
    'SUB': 0x2,
    'ADC': 0x3,
    'LDR': 0x8,
    'STR': 0xA,
    'SBC': 0X4,
    'AND': 0x5,
    'XOR': 0x6,
    'CMP': 0xD,
    'SWP': 0xE,
    'ORR': 0xF,
    'LDRB': 0x9,
    'STRB': 0xB,
}

OPCJMP = {
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
    'EXT': 0xC1,
}

OPCSFT = {
    'LSR': 0x0,
    'ASR': 0x1,
    'LSL': 0x10,
    'ROR': 0x11,
    'RRX': 0x0,
}

def rcheck(r):
    if r[0] == 'R' and 0 <= int(r[1]) <= 7:
        return True
    else:
        return False

def assemble(j, BA):
    if len(j) == 0:
        return 0
    if len(j) == 1:
        return find_twos_compl(j[0], 16)
    if j[0] == 'RET':
        return 0xCF00
    if j[0] == 'DCW' or j[0] == '=':
        return find_twos_compl(j[1], 16)
    if j[0] in OPCALU or j[0] in OPCSFT:
        opc = OPCALU[j[0]] if j[0] in OPCALU else 7
        if rcheck(j[1]):
            a = int(j[1][1]) * 0x2
        else:
            return -2
        j[2] = j[2].strip('[]')
        if j[2][0] != 'R':
            a += 0x1
            if j[2] in addr:
                imm = addr[j[2]]
            elif -128 <= findval(j[2]) <= 255:
                imm = find_twos_compl(j[2], 8)
            else:
                return -3
        else:
            if len(j) == 3:
                j.append('0')
            j[3] = j[3].strip(']')
            if -16 <= findval(j[3]) <= 15:
                if rcheck(j[2]):
                    imm = int(j[2][1]) * 0x20 + (find_twos_compl(j[3], 5))
                else:
                    return -4
            else:
                return -5
        if BA and (j[0] == 'LDR' or j[0] == 'STR') and imm % 2 != 0:
            return -6
        if not BA and (j[0] == 'LDRB' or j[0] == 'STRB'):
            return -1 
        return opc * 0x1000 + a * 0x100 + imm + (OPCSFT[j[0]] << 4 if j[0] in OPCSFT else 0)
    elif j[0] in OPCJMP:
        opc = OPCJMP[j[0]]
        imm = addr[j[1]] if j[1] in addr else findval(j[1])
        if 0 <= imm <= 255:
            return opc * 0x100 + imm
        else:
            return -2
    else:
        return -1

def findval(x):
    x=x.strip('#')
    if x[0:2] == '0b':
        return int(x[2:], 2)
    elif x[0:2] == '0x':
        return int(x[2:], 16)
    else:
        return int(x)


def find_twos_compl(x, l):
    x=x.strip('#')
    if x[0] == '-':
        x = findval(x[1:]) ^ int('1'*l, 2)
        return x + 1
    else:
        return findval(x)

def erreport(i, pc):
    pc += 1 #Remove this line for line to be aligned with RAM address
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
    if i == -6:
        print('Invalid word address for LDR/STR on line', pc)


f = open('assembly.txt', 'r')
a = []
addr = {}
pc = 0
for line in f:
    al = []
    line = line.replace(',', ' ')
    for i in line.split():
        if i[-1] == ':':
            addr[i[:-1]] = pc
            if pc > 255:
                print("Warning: Symbolic address is bigger than 255")
        elif i[0] == '/':
            break
        else:
            al.append(i)
    a.append(al)
    pc += 1
f.close()

f = open('assembly.ram', 'w')

BYTE_ADDRESSING = False #Change bool to True for byte addressing challenge

pc = 0
for j in a:
    i = assemble(j, BYTE_ADDRESSING)
    if i < 0:
        erreport(i, pc)
    else:
        print(hex(pc), hex(i), j)
        l = hex(pc) + ' ' + hex(i) + '\n'
        f.write(l)
    pc += 1
f.close()

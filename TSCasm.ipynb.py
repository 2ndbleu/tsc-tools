# %% [markdown]
# ## Utility Functions

# %%
directives = ['.BSC', '.BSS', '.END', '.ORG'] # '.EQU'
insts = {
# I-type
    'BNE': ['I', 0, 's', 't', 'l'],
    'BEQ': ['I', 1, 's', 't', 'l'],
    'BGZ': ['I', 2, 's', 'l'],
    'BLZ': ['I', 3, 's', 'l'],
    'ADI': ['I', 4, 't', 's', 'i8'],
    'ORI': ['I', 5, 't', 's', 'u8'],
    'LHI': ['I', 6, 't', 'u8'],
    'LWD': ['I', 7, 't', 's', 'i8'],
    'SWD': ['I', 8, 't', 's', 'i8'],

# J-type
    'JMP': ['J', 9, 'j'],
    'JAL': ['J', 10, 'j'],

# R-type
    'ADD': ['R', 0, 'd', 's', 't'],
    'SUB': ['R', 1, 'd', 's', 't'],
    'AND': ['R', 2, 'd', 's', 't'],
    'ORR': ['R', 3, 'd', 's', 't'],
    'NOT': ['R', 4, 'd', 's'],
    'TCP': ['R', 5, 'd', 's'],
    'SHL': ['R', 6, 'd', 's'],
    'SHR': ['R', 7, 'd', 's'],
    'JPR': ['R', 25, 's'],
    'JRL': ['R', 26, 's'],
    'RWD': ['R', 27, 'd'],
    'WWD': ['R', 28, 's'],
    'HLT': ['R', 29],
    'ENI': ['R', 30, 's'],
    'DSI': ['R', 31, 's'],
}

def check_name(name: str):
    if len(name) <= 0:
        return False
    elif name[0].isdigit():
        return False
    elif name in directives:
        return False
    else:
        return True
    
def parse_int(s: str):
    if len(s) <= 0:
        raise ValueError("parse_int(): Empty String!")
    # support x86 hexadecimal
    if s[-1] == 'h':
        return int(s[:-1], base=16)
    # literal
    if s[0] == '0':
        if len(s) == 1:
            return 0
        elif s[1] == 'b':
            return int(s[2:], base=2)
        elif s[1] == 'o':
            return int(s[2:], base=8)
        elif s[1] == 'x':
            return int(s[2:], base=16)
        elif s[1].isdigit():
            return int(s[1:], base=8)
        else:
            raise ValueError("parse_int(): Unsupported Literal!")
    elif (s[0] in ['+', '-']) and s[1] == '0':
        if len(s) == 2:
            return 0
        elif s[2] == 'b':
            return int(s[0]+s[3:], base=2)
        elif s[2] == 'o':
            return int(s[0]+s[3:], base=8)
        elif s[2] == 'x':
            return int(s[0]+s[3:], base=16)
        elif s[2].isdigit():
            return int(s[0]+s[2:], base=8)
        else:
            raise ValueError("parse_int(): Unsupported Literal!")
    # decimal
    return int(s)

# %% [markdown]
# ## Assembly Code (`CPU_TB.v`)

# %%
asm = """
.ORG    0
    JMP    ENTRY
VAR1    .BSC 0x0001
VAR2    .BSC 0xFFFF
STACK   .BSS 32
ENTRY:
    LHI     $0, 0
    WWD     $0          ; TEST #1-1 : LHI (= 0x0000)
    LHI     $1, 0
    WWD     $1          ; TEST #1-2 : LHI (= 0x0000)
    LHI     $2, 0
    WWD     $2          ; TEST #1-3 : LHI (= 0x0000)
    LHI     $3, 0
    WWD     $3          ; TEST #1-4 : LHI (= 0x0000)
    ADI     $0, $1, 1
    WWD     $0          ; TEST #2-1 : ADI (= 0x0001)
    ADI     $0, $0, 1
    WWD     $0          ; TEST #2-2 : ADI (= 0x0002)
    ORI     $1, $2, 1
    WWD     $1          ; TEST #3-1 : ORI (= 0x0001)
    ORI     $1, $1, 2
    WWD     $1          ; TEST #3-2 : ORI (= 0x0003)
    ORI     $1, $1, 3
    WWD     $1          ; TEST #3-3 : ORI (= 0x0003)
    ADD     $3, $0, $2
    WWD     $3          ; TEST #4-1 : ADD (= 0x0002)
    ADD     $3, $1, $2
    WWD     $3          ; TEST #4-2 : ADD (= 0x0003)
    ADD     $3, $0, $1
    WWD     $3          ; TEST #4-3 : ADD (= 0x0005)
    SUB     $3, $0, $2
    WWD     $3          ; TEST #5-1 : SUB (= 0x0002)
    SUB     $3, $2, $0
    WWD     $3          ; TEST #5-2 : SUB (= 0xFFFE)
    SUB     $3, $1, $2
    WWD     $3          ; TEST #5-3 : SUB (= 0x0003)
    SUB     $3, $2, $1
    WWD     $3          ; TEST #5-4 : SUB (= 0xFFFD)
    SUB     $3, $0, $1
    WWD     $3          ; TEST #5-5 : SUB (= 0xFFFF)
    SUB     $3, $1, $0
    WWD     $3          ; TEST #5-6 : SUB (= 0x0001)
    AND     $3, $0, $2
    WWD     $3          ; TEST #6-1 : AND (= 0x0000)
    AND     $3, $1, $2
    WWD     $3          ; TEST #6-2 : AND (= 0x0000)
    AND     $3, $0, $1
    WWD     $3          ; TEST #6-3 : AND (= 0x0002)
    ORR     $3, $0, $2
    WWD     $3          ; TEST #7-1 : ORR (= 0x0002)
    ORR     $3, $1, $2
    WWD     $3          ; TEST #7-2 : ORR (= 0x0003)
    ORR     $3, $0, $1
    WWD     $3          ; TEST #7-3 : ORR (= 0x0003)
    NOT     $3, $0
    WWD     $3          ; TEST #8-1 : NOT (= 0xFFFD)
    NOT     $3, $1
    WWD     $3          ; TEST #8-2 : NOT (= 0xFFFC)
    NOT     $3, $2
    WWD     $3          ; TEST #8-3 : NOT (= 0xFFFF)
    TCP     $3, $0
    WWD     $3          ; TEST #9-1 : TCP (= 0xFFFE)
    TCP     $3, $1
    WWD     $3          ; TEST #9-2 : TCP (= 0xFFFD)
    TCP     $3, $2
    WWD     $3          ; TEST #9-3 : TCP (= 0x0000)
    SHL     $3, $0
    WWD     $3          ; TEST #10-1 : SHL (= 0x0004)
    SHL     $3, $1
    WWD     $3          ; TEST #10-2 : SHL (= 0x0006)
    SHL     $3, $2
    WWD     $3          ; TEST #10-3 : SHL (= 0x0000)
    SHR     $3, $0
    WWD     $3          ; TEST #11-1 : SHR (= 0x0001)
    SHR     $3, $1
    WWD     $3          ; TEST #11-2 : SHR (= 0x0001)
    SHR     $3, $2
    WWD     $3          ; TEST #11-3 : SHR (= 0x0000)
    LWD     $0, $2, VAR1
    WWD     $0          ; TEST #12-1 : LWD (= 0x0001)
    LWD     $1, $2, VAR2
    WWD     $1          ; TEST #12-2 : LWD (= 0xFFFF)
    SWD     $1, $2, VAR1
    SWD     $0, $2, VAR2
    LWD     $0, $2, VAR1
    WWD     $0          ; TEST #13-1 : WWD (= 0xFFFF)
    LWD     $1, $2, VAR2
    WWD     $1          ; TEST #13-2 : WWD (= 0x0001)
    JMP     JMP0
JMP0:
    WWD     $0          ; TEST #14-1 : JMP (= 0xFFFF)
    JMP     JMP1
    HLT
JMP1:
    WWD     $1          ; TEST #14-2 : JMP (= 0x0001)
    BNE     $2, $3, BNE1
    JMP     BNE2
BNE1:
    HLT
BNE2:
    WWD     $0          ; TEST #15-1 : BNE (= 0xFFFF)
    BNE     $1, $2, BNE3
    HLT
BNE3:
    WWD     $1          ; TEST #15-2 : BNE (= 0x0001)
    BEQ     $1, $2, BEQ1
    JMP     BEQ2
BEQ1:
    HLT
BEQ2:
    WWD     $0          ; TEST #16-1 : BEQ (= 0xFFFF)
    BEQ     $2, $3, BEQ3
    HLT
BEQ3:
    WWD     $1          ; TEST #16-2 : BEQ (= 0x0001)
    BGZ     $0, BGZ1
    JMP     BGZ2
BGZ1:
    HLT
BGZ2:
    WWD     $0          ; TEST #17-1 : BGZ (= 0xFFFF)
    BGZ     $1, BGZ3
    HLT
BGZ3:
    WWD     $1          ; TEST #17-2 : BGZ (= 0x0001)
    BGZ     $2, BGZ4
    JMP     BGZ5
BGZ4:
    HLT
BGZ5:
    WWD     $0          ; TEST #17-3 : BGZ (= 0xFFFF)
    BLZ     $0, BLZ1
    HLT
BLZ1:
    WWD     $1          ; TEST #18-1 : BLZ (= 0x0001)
    BLZ     $1, BLZ2
    JMP     BLZ3
BLZ2:
    HLT
BLZ3:
    WWD     $0          ; TEST #18-2 : BLZ (= 0xFFFF)
    BLZ     $2, BLZ4
    JMP     BLZ5
BLZ4:
    HLT
BLZ5:
    WWD     $1          ; TEST #18-3 : BLZ (= 0x0001)
    JAL     SIMPLE1
    WWD     $0          ; TEST #19-1 : JAL & JPR (= 0xFFFF)
    JAL     SIMPLE2
    HLT
    WWD     $1          ; TEST #19-2 : JAL & JPR (= 0x0001)
    LHI     $3, 0
    ORI     $3, $3, STACK
    LHI     $0, 0
    ADI     $0, $0, 5
    JAL     FIB
    WWD     $0          ; TEST #19-3 : JAL & JPR (= 0x0008)
    JMP     PREFIB1
PREFIB2:
    ADI     $1, $2, 0
    JRL     $1
    WWD     $0          ; TEST #20 : JAL & JRL & JPR (= 0x0022)
    JMP     PRELOOP
SIMPLE2:
    ADI     $2, $2, 1
SIMPLE1:
    JPR     $2
    HLT
PREFIB1:
    JAL     PREFIB2
FIB:
    ADI     $1, $0, -1
    BGZ     $1, FIBRECUR
    LHI     $0, 0
    ORI     $0, $0, 1
    JPR     $2
    HLT
FIBRECUR:
    SWD     $2, $3, 0
    SWD     $0, $3, 1
    ADI     $3, $3, 2
    ADI     $0, $0, -2
    JAL     FIB
    LWD     $1, $3, -1
    SWD     $0, $3, -1
    ADI     $0, $1, -1
    JAL     FIB
    LWD     $1, $3, -1
    LWD     $2, $3, -2
    ADD     $0, $0, $1
    ADI     $3, $3, -2
    JPR     $2
    HLT
PRELOOP:
    LHI     $3, 1
    LHI     $0, 0
    ADI     $2, $1, 16
LOOP:
    LWD     $0, $2, 0
    ADD     $1, $1, $0
    ADI     $2, $2, 1
    LHI     $0, 0
    ADI     $0, $0, 23
    AND     $2, $2, $0
    ADI     $3, $3, -1
    BGZ     $3, LOOP
    WWD     $1          ; TEST #21-1 : ADI & BGZ (= 0x002D)
    LHI     $0, 0
    WWD     $2          ; TEST #21-2 : ADI & BGZ (= 0x0015)
    ADI     $1, $0, 24
    ADI     $0, $0, 8
    LHI     $2, 0
SETZERO:
    SWD     $2, $1, 0
    ADI     $1, $1, 1
    ADI     $0, $0, -1
    BGZ     $0, SETZERO
    ORI     $3, $2, STACK
    ADI     $0, $2, 5
    ADI     $1, $2, 24
    JAL     FIBDP
    WWD     $0          ; TEST #22 : JAL & SWD & LWD & JPR (= 0x0008)
    HLT                 ; FINISHED
FIBDP:
    SWD     $2, $3, 0
    SWD     $1, $3, 1
    SWD     $0, $3, 2
    ADI     $3, $3, 4
    ADI     $2, $0, -2
    ADD     $1, $1, $0
    LWD     $0, $1, 0
    BGZ     $0, DPEND
    LHI     $0, 0
    ADI     $0, $0, 1
    BLZ     $2, SETDP
    ADI     $0, $2, 1
    LWD     $1, $3, -3
    JAL     FIBDP
    SWD     $0, $3, -1
    LWD     $0, $3, -2
    LWD     $1, $3, -3
    ADI     $0, $0, -2
    JAL     FIBDP
    LWD     $1, $3, -1
    ADD     $0, $0, $1
SETDP:
    LWD     $2, $3, -2
    LWD     $1, $3, -3
    ADD     $1, $1, $2
    SWD     $0, $1, 0
DPEND:
    LWD     $2, $3, -4
    ADI     $3, $3, -4
    JPR     $2
    HLT
TESTEND:
    HLT                 ; FINISHED
.END
"""

# %% [markdown]
# ## Parser

# %%
tokens = []
n_lines = 0
n_token = 0

for line in asm.splitlines():
    # remove comments
    code = line.strip().split(';')[0].split()
    if len(code) <= 0:
        pass
    else:
        cstr = ' '.join(code)
        n_lines += 1
        # Label
        if ':' in cstr:
            i = cstr.index(':')
            if not check_name(cstr[:i]):
                print("LABEL NAME ERROR!")
                break
            else:
                __code = ('l', cstr[:i])
                tokens.append(__code)
                n_token += 1
                if (i+1) >= len(cstr):
                    continue
                cstr = cstr[i+1:].strip()
                code = cstr.split()
        # Directive
        if '.' in cstr:
            try:
                if code[0][0] == '.':
                    dir = code[0]
                    __code = ('d', dir, *[i.strip() for i in ' '.join(code[1:]).split(',')])
                elif code[1][0] == '.':
                    dir = code[1]
                    __code = ('D', dir, *[i.strip() for i in ' '.join(code[2:]).split(',')], code[0])
                tokens.append(__code)
                n_token += 1
                continue
            except:
                if code[0] == '.END':
                    __code = ('d', '.END')
                    tokens.append(__code)
                    n_token += 1
                    continue
                pass
        # Inst str
        if len(code) == 1:
            __code = ('i', code[0])
        else:
            __code = ('i', code[0], *[i.strip() for i in ' '.join(code[1:]).split(',')])
        tokens.append(__code)
        n_token += 1

print(len(tokens), f"## {n_lines} non-empty lines: {n_token} tokens")

# %%
for token in tokens:
    print(token)

# %% [markdown]
# ## Pass-1&2

# %%
# Pass 1
addr = 0; labels = dict()

for token in tokens:
    match token[0]:
        case 'd':
            match token[1]:
                case '.BSC':
                    addr += len(token) - 2
                case '.BSS':
                    if (sz := parse_int(token[2])) > 0:
                        addr += sz
                case '.END':
                    break
                case '.ORG':
                    if (org := parse_int(token[2])) >= addr:
                        addr = org
                    else:
                        print("[Pass 1] Warning: section start is before than previous section data end")
                        addr = org
                case _:
                    pass
        case 'D':
            labels[token[-1]] = addr
            match token[1]:
                case '.BSC':
                    addr += len(token) - 3
                case '.BSS':
                    if (sz := parse_int(token[2])) > 0:
                        addr += sz
                case '.END':
                    break
                case '.ORG':
                    if (org := parse_int(token[2])) >= addr:
                        addr = org
                    else:
                        print("[Pass 1] Warning: section start is before than previous section data end")
                        addr = org
                case _:
                    pass
        case 'l':
            labels[token[1]] = addr
        case 'i':
            addr += 1
        case _:
            pass

print("[Pass 1]")
print("Resolved Symbols:", labels)

# Pass 2
addr = 0; binary = []

for token in tokens:
    match token[0]:
        case 'd':
            match token[1]:
                case '.BSC':
                    for word in token[2:]:
                        try:
                            binary.append((addr, (parse_int(word) & 0xffff)))
                            addr += 1
                        except:
                            try:
                                if word in labels.keys():
                                    binary.append((addr, (labels[word] & 0xffff)))
                                    addr += 1
                            except:
                                raise ValueError("[Pass 2] Error: Invalid Label Name!")
                case '.BSS':
                    if (sz := parse_int(token[2])) > 0:
                        for _ in range(sz):
                            binary.append((addr, 0))
                            addr += 1
                case '.END':
                    break
                case '.ORG':
                    addr = org
                case _:
                    pass
        case 'D':
            match token[1]:
                case '.BSC':
                    for word in token[2:-1]:
                        try:
                            binary.append((addr, (parse_int(word) & 0xffff)))
                            addr += 1
                        except:
                            try:
                                if word in labels.keys():
                                    binary.append((addr, (labels[word] & 0xffff)))
                                    addr += 1
                            except:
                                raise ValueError("[Pass 2] Error: Invalid Label Name!")
                case '.BSS':
                    if (sz := parse_int(token[2])) > 0:
                        for _ in range(sz):
                            binary.append((addr, 0))
                            addr += 1
                case '.END':
                    break
                case '.ORG':
                    addr = org
                case _:
                    pass
        case 'l':
            pass
        case 'i':
            op = insts[token[1]]
            word = 0x0000
            match op[0]:
                case 'I':
                    word |= op[1] << 12
                    for i, operand in enumerate(op):
                        if i < 2:
                            pass
                        match operand:
                            case 's':
                                if token[i][0] == '$':
                                    regno = int(token[i][1:])
                                    if regno not in range(4):
                                        raise ValueError("[Pass 2] Error: Invalid Register #!")
                                    word |= regno << 10
                            case 't':
                                if token[i][0] == '$':
                                    regno = int(token[i][1:])
                                    if regno not in range(4):
                                        raise ValueError("[Pass 2] Error: Invalid Register #!")
                                    word |= regno << 8
                            case 'i8':
                                try:
                                    imm = parse_int(token[i])
                                except:
                                    try:
                                        if token[i] in labels.keys():
                                            imm = labels[token[i]]
                                    except:
                                        raise ValueError("[Pass 2] Error: Invalid Immediate or Offset!")
                                if imm not in range(-128, 128):
                                    raise ValueError("[Pass 2] Error: Immediate Out of Range!")
                                word |= imm & 0xff
                            case 'u8':
                                try:
                                    imm = parse_int(token[i])
                                except:
                                    try:
                                        if token[i] in labels.keys():
                                            imm = labels[token[i]]
                                    except:
                                        raise ValueError("[Pass 2] Error: Invalid Immediate or Offset!")
                                if imm not in range(0, 256):
                                    raise ValueError("[Pass 2] Error: Immediate Out of Range!")
                                word |= imm & 0xff
                            case 'l':
                                try:
                                    imm = parse_int(token[i])
                                except:
                                    try:
                                        if token[i] in labels.keys():
                                            imm = labels[token[i]] - (addr + 1)
                                    except:
                                        raise ValueError("[Pass 2] Error: Invalid Offset!")
                                if imm not in range(-128, 128):
                                    raise ValueError("[Pass 2] Error: Immediate Out of Range!")
                                word |= imm & 0xff
                            case _:
                                pass
                case 'J':
                    word |= op[1] << 12
                    try:
                        target = parse_int(token[2])
                        if (target ^ addr) & 0xf000 != 0:
                            raise ValueError("[Pass 2] Error: Invalid Jump Target!")
                        offset = target & 0x0fff
                    except:
                        try:
                            if token[2] in labels.keys():
                                target = labels[token[2]]
                                if (target ^ addr) & 0xf000 != 0:
                                    raise ValueError("[Pass 2] Error: Invalid Jump Target!")
                                offset = target & 0x0fff
                        except:
                            raise ValueError("[Pass 2] Error: Invalid Immediate or Offset!")
                    word |= offset
                case 'R':
                    word |= 15 << 12
                    word |= op[1]
                    for i, operand in enumerate(op):
                        if i < 2:
                            pass
                        match operand:
                            case 's':
                                if token[i][0] == '$':
                                    regno = int(token[i][1:])
                                    if regno not in range(4):
                                        raise ValueError("[Pass 2] Error: Invalid Register #!")
                                    word |= regno << 10
                            case 't':
                                if token[i][0] == '$':
                                    regno = int(token[i][1:])
                                    if regno not in range(4):
                                        raise ValueError("[Pass 2] Error: Invalid Register #!")
                                    word |= regno << 8
                            case 'd':
                                if token[i][0] == '$':
                                    regno = int(token[i][1:])
                                    if regno not in range(4):
                                        raise ValueError("[Pass 2] Error: Invalid Register #!")
                                    word |= regno << 6
                            case _:
                                pass
                case _:
                    pass
            binary.append((addr, (word & 0xffff)))
            addr += 1
        case _:
            pass

print("[Pass 2]")
print(f"Finished at 0x{addr:x}")

# %%
print(len(binary))

# %%
for addr, word in binary:
    print(f"{addr:04x}: {word:04x}")

# %%
for addr, word in binary:
    print(f"				memory[16'h{addr:x}] <= 16'h{word:x};")

# %%
print('[', end='')
for i, d in enumerate(binary):
    addr, data = d
    print(f"(0x{addr:x}, 0x{data:x}), ", end='')
    if (i & 0x3) == 0x3:
        print()
print(']')



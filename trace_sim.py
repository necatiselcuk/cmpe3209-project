#!/usr/bin/env python3
# Necati Selcuk, 5001240039, G2 - data address trace generator
# Runs main_rars.s (RV32IM subset used by the program) with the same memory
# layout as RARS 1.6 and writes every data load/store to trace.csv.
# Usage: python trace_sim.py [main_rars.s] [trace.csv]

import sys, csv

TEXT_BASE = 0x00400000
DATA_BASE = 0x10010000
SP_INIT = 0x7FFFEFFC
GP_INIT = 0x10008000
MASK = 0xFFFFFFFF

REGS = {'zero': 0, 'ra': 1, 'sp': 2, 'gp': 3, 'tp': 4, 't0': 5, 't1': 6, 't2': 7,
        's0': 8, 'fp': 8, 's1': 9, 'a0': 10, 'a1': 11, 'a2': 12, 'a3': 13, 'a4': 14,
        'a5': 15, 'a6': 16, 'a7': 17, 's2': 18, 's3': 19, 's4': 20, 's5': 21,
        's6': 22, 's7': 23, 's8': 24, 's9': 25, 's10': 26, 's11': 27, 't3': 28,
        't4': 29, 't5': 30, 't6': 31}
for i in range(32):
    REGS['x%d' % i] = i

# C source line for each RARS address range (tutanak 2a table)
C_LINES = [
    (0x00400000, 0x00400008, 'start'),
    (0x0040000C, 0x0040001C, '13-14'), (0x00400020, 0x00400070, '15-19'),
    (0x00400074, 0x00400084, '20'), (0x00400088, 0x0040009C, '23-24'),
    (0x004000A0, 0x004000B4, '25'), (0x004000B8, 0x004000B8, '26'),
    (0x004000BC, 0x004000CC, '27'), (0x004000D0, 0x004000DC, '29-30'),
    (0x004000E0, 0x004000E8, '31'), (0x004000EC, 0x004000EC, '32'),
    (0x004000F0, 0x004000F4, '35'), (0x00400164, 0x00400178, '35'),
    (0x004000F8, 0x00400114, '36'), (0x00400118, 0x00400160, '37'),
    (0x0040017C, 0x00400180, '41'), (0x00400210, 0x00400224, '41'),
    (0x00400184, 0x0040019C, '42'), (0x004001A0, 0x004001D4, '43'),
    (0x004001D8, 0x004001FC, '44'), (0x00400200, 0x0040020C, '45'),
    (0x00400228, 0x0040024C, '47'), (0x00400250, 0x00400254, '50'),
    (0x004002E4, 0x004002F8, '50'), (0x00400258, 0x00400288, '51'),
    (0x0040028C, 0x004002C4, '52'), (0x004002C8, 0x004002E0, '53'),
    (0x004002FC, 0x00400310, '56-57'),
]


def c_line(pc):
    for lo, hi, ln in C_LINES:
        if lo <= pc <= hi:
            return ln
    return '?'


def s32(v):
    v &= MASK
    return v - (1 << 32) if v & 0x80000000 else v


def parse(path):
    """Return (instructions, labels, data_bytes)."""
    labels, insts, data = {}, [], bytearray()
    section, pc = None, TEXT_BASE
    for raw in open(path, encoding='utf-8'):
        line = raw.split('#')[0].strip()
        if not line:
            continue
        if line in ('.data', '.text'):
            section = line
            continue
        if line.endswith(':'):
            name = line[:-1]
            labels[name] = DATA_BASE + len(data) if section == '.data' else pc
            continue
        parts = line.replace(',', ' ').split()
        op, args = parts[0], parts[1:]
        if section == '.data':
            if op == '.word':
                for a in args:
                    data += (int(a, 0) & MASK).to_bytes(4, 'little')
            elif op == '.space':
                data += bytes(int(args[0], 0))
            continue
        if op.startswith('.'):
            continue
        insts.append((pc, op, args))
        pc += 8 if op == 'la' else 4          # la = auipc + addi
    return insts, labels, data


def run(path):
    insts, labels, data = parse(path)
    by_pc = {pc: (op, args) for pc, op, args in insts}
    mem = {}
    for i, b in enumerate(data):
        mem[DATA_BASE + i] = b
    x = [0] * 32
    x[2], x[3] = SP_INIT, GP_INIT
    pc, icount, trace = TEXT_BASE, 0, []

    def rd_mem(a):
        return int.from_bytes(bytes(mem.get(a + i, 0) for i in range(4)), 'little')

    def wr_mem(a, v):
        for i, b in enumerate((v & MASK).to_bytes(4, 'little')):
            mem[a + i] = b

    def R(n):
        return x[REGS[n]]

    def W(n, v):
        r = REGS[n]
        if r:
            x[r] = v & MASK

    def memop(arg):                       # "-20(s0)"
        off, base = arg.split('(')
        return (s32(int(off, 0)) + R(base[:-1])) & MASK

    def target(a):
        return labels[a] if a in labels else int(a, 0)

    while True:
        op, a = by_pc[pc]
        nxt = pc + 4
        icount += 1
        if op == 'lw':
            addr = memop(a[1])
            W(a[0], rd_mem(addr))
            trace.append(('R', addr, pc))
        elif op == 'sw':
            addr = memop(a[1])
            wr_mem(addr, R(a[0]))
            trace.append(('W', addr, pc))
        elif op == 'addi':
            W(a[0], R(a[1]) + s32(int(a[2], 0)))
        elif op == 'ori':
            W(a[0], R(a[1]) | (int(a[2], 0) & MASK))
        elif op == 'add':
            W(a[0], R(a[1]) + R(a[2]))
        elif op == 'sub':
            W(a[0], R(a[1]) - R(a[2]))
        elif op == 'mul':
            W(a[0], R(a[1]) * R(a[2]))
        elif op == 'mulh':
            W(a[0], (s32(R(a[1])) * s32(R(a[2]))) >> 32)
        elif op == 'mulhu':
            W(a[0], (R(a[1]) * R(a[2])) >> 32)
        elif op == 'slli':
            W(a[0], R(a[1]) << int(a[2], 0))
        elif op == 'srli':
            W(a[0], R(a[1]) >> int(a[2], 0))
        elif op == 'srai':
            W(a[0], s32(R(a[1])) >> int(a[2], 0))
        elif op == 'lui':
            W(a[0], int(a[1], 0) << 12)
        elif op == 'li':
            W(a[0], int(a[1], 0))
        elif op == 'mv':
            W(a[0], R(a[1]))
        elif op == 'la':
            icount += 1                       # second instruction (addi)
            W(a[0], labels[a[1]])
            nxt = pc + 8
        elif op in ('beq', 'bge', 'bgt', 'ble'):
            u, v = s32(R(a[0])), s32(R(a[1]))
            if {'beq': u == v, 'bge': u >= v, 'bgt': u > v, 'ble': u <= v}[op]:
                nxt = target(a[2])
        elif op == 'j':
            nxt = target(a[0])
        elif op == 'jal':
            W(a[0], pc + 4)
            nxt = target(a[1])
        elif op == 'jr':
            nxt = R(a[0])
        elif op == 'ecall':
            if R('a7') == 10:
                break
        else:
            raise ValueError('unsupported instruction: %s at 0x%08X' % (op, pc))
        pc = nxt

    return trace, icount, rd_mem, labels


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else 'main_rars.s'
    out = sys.argv[2] if len(sys.argv) > 2 else 'trace.csv'
    trace, icount, rd_mem, labels = run(src)
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        # column format required by the submission form (tutanak 4a)
        w.writerow(['sira', 'RW', 'adres_hex', 'boyut', 'c_satiri', 'stack_mi'])
        for i, (rw, addr, pc) in enumerate(trace, 1):
            stack = 1 if addr >= 0x7F000000 else 0
            w.writerow([i, rw, '0x%08X' % addr, 4, c_line(pc), stack])

    b = labels['bucket']
    print('dynamic instructions:', icount)
    print('data references    :', len(trace),
          '(R %d, W %d)' % (sum(t[0] == 'R' for t in trace), sum(t[0] == 'W' for t in trace)))
    g0 = labels['grades']
    print('stack references   :', sum(t[1] >= 0x7F000000 for t in trace))
    print('grades[] references:', sum(g0 <= t[1] < g0 + 4 * 38 for t in trace))
    print('bucket             :', [rd_mem(b + 4 * i) for i in range(5)])
    for n in ('mean', 'below_count', 'pass_count'):
        print('%-19s: %d' % (n, s32(rd_mem(labels[n]))))
    print('grades[0..5]       :', [rd_mem(labels['grades'] + 4 * i) for i in range(6)])


if __name__ == '__main__':
    main()

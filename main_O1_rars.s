# Necati Selcuk, 5001240039, G2 - Exam grade distribution (-O1, for step 5a)
# RARS-adapted version of asm_O1.s
# Source: RISC-V (32-bits) gcc 16.1.0 (godbolt.org), -O1 -march=rv32im -mabi=ilp32
# Same changes as main_rars.s (program logic unchanged):
#   1. Added .data / .text sections; '.zero n' -> '.space n'
#   2. Added a startup block that calls main and then exits (ecall 10)
#   3. 'lla' -> 'la'
#   4. 'li rd, <large constant with low 12 bits = 0>' -> 'lui rd, <upper 20 bits>'
#   5. 'call f' -> 'jal ra, f'
#   6. .LANCHOR0 (= grades) offsets written with data labels:
#      .LANCHOR0+152 -> pass_count, .LANCHOR0+180 -> below_count

        .data
SID:
        .word   1240039
grades:
        .space  152
pass_count:
        .word   0
bucket:
        .space  20
mean:
        .word   0
below_count:
        .word   0

        .text
_start:
        jal     ra, main
        li      a7, 10
        ecall

bucket_of:
        mv      a5,a0
        li      a4,49
        ble     a0,a4,.L3
        li      a4,64
        li      a0,1
        ble     a5,a4,.L1
        li      a4,74
        li      a0,2
        ble     a5,a4,.L1
        li      a0,84
        sgt     a0,a5,a0
        addi    a0,a0,3
        ret
.L3:
        li      a0,0
.L1:
        ret
mark:
        blt     a0,a1,.L9
        ret
.L9:
        ori     a0,a0,256
        ret
main:
        addi    sp,sp,-48
        sw      ra,44(sp)
        sw      s0,40(sp)
        sw      s1,36(sp)
        sw      s2,32(sp)
        sw      s3,28(sp)
        sw      s4,24(sp)
        sw      s5,20(sp)
        sw      s6,16(sp)
        sw      s7,12(sp)
        sw      s8,8(sp)
        sw      s9,4(sp)
        la     s0,grades
        la     s3,pass_count
        mv      a2,s0
        lui     a3,0x12f
        addi    a3,a3,-1049
        lui     a7,0x196
        addi    a7,a7,1549
        lui     a6,0x3c6ef
        addi    a6,a6,863
        lui     a0,0x446f8
        addi    a0,a0,1623
        li      t1,101
.L11:
        mul     a3,a3,a7
        add     a3,a3,a6
        srli    a4,a3,16
        mulhu   a5,a4,a0
        sub     a1,a4,a5
        srli    a1,a1,1
        add     a5,a5,a1
        srli    a5,a5,6
        mul     a5,a5,t1
        sub     a4,a4,a5
        sw      a4,0(a2)
        addi    a2,a2,4
        bne     a2,s3,.L11
        lw      s6,pass_count
        la     s1,grades
        li      s8,0
        li      s4,0
        mv      s5,s1
        li      s7,58
        li      s9,1
        j       .L13
.L12:
        slli    a0,a0,2
        add     a0,s5,a0
        sw      a5,156(a0)
        add     s4,s4,s2
        addi    s1,s1,4
        beq     s1,s3,.L23
.L13:
        lw      s2,0(s1)
        mv      a0,s2
        jal     ra,bucket_of
        slli    a5,a0,2
        add     a5,s5,a5
        lw      a5,156(a5)
        addi    a5,a5,1
        ble     s2,s7,.L12
        addi    s6,s6,1
        mv      s8,s9
        j       .L12
.L23:
        beq     s8,zero,.L14
        sw      s6,pass_count,a5
.L14:
        lui     a1,0x6bca2
        addi    a1,a1,-1293
        mulh    a1,s4,a1
        srai    a1,a1,4
        srai    s4,s4,31
        sub     a1,a1,s4
        la     a5,grades
        sw      a1,176(a5)
        lw      a2,180(a5)
        li      a0,0
        li      a6,1
        j       .L16
.L25:
        ori     a3,a5,256
        beq     a5,a3,.L15
        addi    a2,a2,1
        mv      a5,a3
        mv      a0,a6
.L15:
        sw      a5,0(a4)
        addi    s0,s0,4
        beq     s0,s3,.L24
.L16:
        mv      a4,s0
        lw      a5,0(s0)
        ble     a1,a5,.L15
        j       .L25
.L24:
        beq     a0,zero,.L17
        sw      a2,below_count,a5
.L17:
        li      a0,0
        lw      ra,44(sp)
        lw      s0,40(sp)
        lw      s1,36(sp)
        lw      s2,32(sp)
        lw      s3,28(sp)
        lw      s4,24(sp)
        lw      s5,20(sp)
        lw      s6,16(sp)
        lw      s7,12(sp)
        lw      s8,8(sp)
        lw      s9,4(sp)
        addi    sp,sp,48
        jr      ra

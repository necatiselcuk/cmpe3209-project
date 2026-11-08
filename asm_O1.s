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
        lla     s0,.LANCHOR0
        lla     s3,.LANCHOR0+152
        mv      a2,s0
        li      a3,1241088
        addi    a3,a3,-1049
        li      a7,1662976
        addi    a7,a7,1549
        li      a6,1013903360
        addi    a6,a6,863
        li      a0,1148157952
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
        lw      s6,.LANCHOR0+152
        lla     s1,.LANCHOR0
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
        call    bucket_of
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
        sw      s6,.LANCHOR0+152,a5
.L14:
        li      a1,1808408576
        addi    a1,a1,-1293
        mulh    a1,s4,a1
        srai    a1,a1,4
        srai    s4,s4,31
        sub     a1,a1,s4
        lla     a5,.LANCHOR0
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
        sw      a2,.LANCHOR0+180,a5
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
SID:
        .word   1240039
        .set    .LANCHOR0,. + 0
grades:
        .zero   152
pass_count:
        .zero   4
bucket:
        .zero   20
mean:
        .zero   4
below_count:
        .zero   4
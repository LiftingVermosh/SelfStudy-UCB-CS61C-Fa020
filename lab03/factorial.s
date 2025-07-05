.globl factorial

.data
n: .word 8

.text
main:
    la t0, n
    lw a0, 0(t0)
    jal ra, factorial

    addi a1, a0, 0
    addi a0, x0, 1
    ecall # Print Result

    addi a1, x0, '\n'
    addi a0, x0, 11
    ecall # Print newline

    addi a0, x0, 10
    ecall # Exit

factorial:
    li   t0, 1              # Init t0 to 1 (this will hold the result)
    beq  a0, x0, factorial_return # 

    # Save current n (a0) and return address (ra) to stack
    addi sp, sp, -8
    sw   a0, 0(sp)          # store n on stack
    sw   ra, 4(sp)          # store return address

    # recursive case: factorial(n) = n * factorial(n-1)
    addi a0, a0, -1         # n -= 1
    jal  ra, factorial      # recursive call to factorial(n-1)

    # restore n from stack
    lw   a0, 0(sp)          # restore current n
    mul  a1, t0, a1         # a0 = n * factorial(n-1)
    lw   ra, 4(sp)          # restore ra
    addi sp, sp, 8          # relese stack pointer

factorial_return:
    ret                     # return to caller
.globl relu

.text
# ======================================================================
# FUNCTION: Performs an inplace element-wise ReLU on an array of ints
# Arguments:
#   a0 (int*) is the pointer to the array
#   a1 (int)  is the # of elements in the array
# Returns:
#   None
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 78.
# ======================================================================
relu:
    # Prologue: save registers on stack
    addi sp, sp, -16
    sw t0, 0(sp)
    sw t1, 4(sp)
    sw t2, 8(sp)
    sw t3, 12(sp)

    # Initialize counter and check element count
    li t0, 0               # t0 = counter
    mv t1, a1              # t1 = number of elements
    mv t3, a0              # t3 = temporary pointer (preserve a0)
    blez t1, err_return    # if t1 <= 0, jump to error

loop_start:
    bge t0, t1, loop_end   # if counter >= elements, end loop
    lw t2, 0(t3)           # load current element
    bgez t2, no_set        # if t2 >= 0, skip setting to zero
    li t2, 0               # set t2 to 0 (ReLU operation)

no_set:
    sw t2, 0(t3)           # store result back
    addi t3, t3, 4         # move pointer to next element
    addi t0, t0, 1         # increment counter
    j loop_start           # jump to loop start

loop_end:
    # Epilogue: restore registers
    lw t0, 0(sp)
    lw t1, 4(sp)
    lw t2, 8(sp)
    lw t3, 12(sp)
    addi sp, sp, 16
    ret

err_return:
    # Error handling: exit with code 78
    li a1, 78
    jal exit2          # Jump to exit2 (from utils.s)
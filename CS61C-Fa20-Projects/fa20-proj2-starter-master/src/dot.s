.globl dot

.text
# =======================================================
# FUNCTION: Dot product of 2 int vectors
# Arguments:
#   a0 (int*) is the pointer to the start of v0
#   a1 (int*) is the pointer to the start of v1
#   a2 (int)  is the length of the vectors
#   a3 (int)  is the stride of v0
#   a4 (int)  is the stride of v1
# Returns:
#   a0 (int)  is the dot product of v0 and v1
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 75.
# - If the stride of either vector is less than 1,
#   this function terminates the program with error code 76.
# =======================================================
dot:
    # Prologue: Save only necessary registers (7 registers)
    addi sp, sp, -28
    sw t0, 0(sp)
    sw t1, 4(sp)
    sw t2, 8(sp)
    sw t3, 12(sp)
    sw t4, 16(sp)
    sw t5, 20(sp)
    sw t6, 24(sp)

    # Parameter checks
    li t0, 1
    blt a2, t0, length_error_return
    blt a3, t0, stride_error_return
    blt a4, t0, stride_error_return

    # Initialize variables
    li t0, 0           # t0 = loop counter i
    li t1, 0           # t1 = accumulator for dot product
    mv t2, a0          # t2 = current pointer for v0
    mv t3, a1          # t3 = current pointer for v1
    slli t4, a3, 2     # t4 = byte stride for v0 (stride * 4)
    slli t5, a4, 2     # t5 = byte stride for v1 (stride * 4)

loop_start:
    # Check if loop counter i >= length (a2)
    bge t0, a2, loop_end

    # Load elements from v0 and v1
    lw t6, 0(t2)       # Load v0 element
    lw a0, 0(t3)       # Load v1 element (temporary use a0, but we restore later)
    mul t6, t6, a0     # Multiply elements
    add t1, t1, t6     # Accumulate to sum

    # Increment pointers by byte strides
    add t2, t2, t4     # v0 pointer += byte stride v0
    add t3, t3, t5     # v1 pointer += byte stride v1

    # Increment loop counter
    addi t0, t0, 1
    j loop_start

loop_end:
    # Move result to a0 for return
    mv a0, t1

    # Epilogue: Restore registers
    lw t0, 0(sp)
    lw t1, 4(sp)
    lw t2, 8(sp)
    lw t3, 12(sp)
    lw t4, 16(sp)
    lw t5, 20(sp)
    lw t6, 24(sp)
    addi sp, sp, 28
    ret

length_error_return:
    # Restore all registers for consistency
    lw t0, 0(sp)
    lw t1, 4(sp)
    lw t2, 8(sp)
    lw t3, 12(sp)
    lw t4, 16(sp)
    lw t5, 20(sp)
    lw t6, 24(sp)
    addi sp, sp, 28
    li a1, 75          # Error code for length error
    jal exit2          # Jump to exit2 (from utils.s)

stride_error_return:
    # Restore all registers for consistency
    lw t0, 0(sp)
    lw t1, 4(sp)
    lw t2, 8(sp)
    lw t3, 12(sp)
    lw t4, 16(sp)
    lw t5, 20(sp)
    lw t6, 24(sp)
    addi sp, sp, 28
    li a1, 76          # Error code for length error
    jal exit2          # Jump to exit2 (from utils.s)
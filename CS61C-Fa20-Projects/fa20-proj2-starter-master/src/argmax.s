.globl argmax

.text
# =================================================================
# FUNCTION: Given a int vector, return the index of the largest
#	element. If there are multiple, return the one
#	with the smallest index.
# Arguments:
# 	a0 (int*) is the pointer to the start of the vector
#	a1 (int)  is the # of elements in the vector
# Returns:
#	a0 (int)  is the first index of the largest element
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 77.
# =================================================================
argmax:
    # Prologue：Store regsiters on the stack
    addi sp, sp, -24
    sw t0, 0(sp)
    sw t1, 4(sp)
    sw t2, 8(sp)
    sw t3, 12(sp)
    sw t4, 16(sp)
    sw t5, 20(sp)
    
    # Param check
    li t0, 1
    blt a1, t0, err_return

    # Initialize the loop variables
    li t0, 0        # Reset the index to 0
    mv t1, a1
    mv t3, a0
    lw t4, 0(t3)    # Use the first element as the initial largest element
    mv t5, t0       # Use the first index as the initial largest index


loop_start:

    # Load the current element at index t0
    slli t2, t0, 2
    add t2, t3, t2
    lw t2, 0(t2)



    # Compare with the largest element
    bge t4, t2, loop_continue
    mv t5, t0           # Update the largest index
    mv t4, t2           # Update the largest element

loop_continue:

    # Increment the index
    addi t0, t0, 1
    # Check whether we have reached the end of the vector
    blt t0, t1, loop_start

loop_end:
    # Epilogue:Save the index of the largest element to a0
    mv a0, t5

    # Restore registers from the stack
    lw t0, 0(sp)
    lw t1, 4(sp)
    lw t2, 8(sp)
    lw t3, 12(sp)
    lw t4, 16(sp)
    lw t5, 20(sp)
    addi sp, sp, 24

    ret

err_return:    

    # Restore registers from the stack
    lw t0, 0(sp)
    lw t1, 4(sp)
    lw t2, 8(sp)
    lw t3, 12(sp)
    lw t4, 16(sp)
    lw t5, 20(sp)
    addi sp, sp, 24

    # Error return: terminate the program with error code 77
    li a1, 77
    jal exit2          # Jump to exit2 (from utils.s)
.globl simple_fn naive_pow inc_arr

.data
failure_message: .asciiz "Test failed for some reason.\n"
success_message: .asciiz "Sanity checks passed! Make sure there are no CC violations.\n"
array:
    .word 1 2 3 4 5
exp_inc_array_result:
    .word 2 3 4 5 6

.text
main:
    # We test our program by loading a bunch of random values
    # into a few saved registers - if any of these are modified
    # after these functions return, then we know calling
    # convention was broken by one of these functions
    li s0, 2623
    li s1, 2910
    # ... skipping middle registers so the file isn't too long
    # If we wanted to be rigorous, we would add checks for
    # s2-s20 as well
    li s11, 134
    # Now, we call some functions
    # simple_fn: should return 1
    jal simple_fn # Shorthand for "jal ra, simple_fn"
    li t0, 1
    bne a0, t0, failure
    # naive_pow: should return 2 ** 7 = 128
    li a0, 2
    li a1, 7
    jal naive_pow
    li t0, 128
    bne a0, t0, failure
    # inc_arr: increments "array" in place
    la a0, array
    li a1, 5
    jal inc_arr
    jal check_arr # Verifies inc_arr and jumps to "failure" on failure
    # Check the values in the saved registers for sanity
    li t0, 2623
    li t1, 2910
    li t2, 134
    bne s0, t0, failure
    bne s1, t1, failure
    bne s11, t2, failure
    # If none of those branches were hit, print a message and exit normally
    li a0, 4
    la a1, success_message
    ecall
    li a0, 10
    ecall

# Just a simple function. Returns 1.
#
# FIXME Fix the reported error in this function (you can delete lines
# if necessary, as long as the function still returns 1 in a0).
simple_fn:
    # The next line is commented out here to fix the CC error
    # mv a0, t0
    li a0, 1
    ret

# Computes a0 to the power of a1.
# This is analogous to the following C pseudocode:
#
# uint32_t naive_pow(uint32_t a0, uint32_t a1) {
#     uint32_t s0 = 1;
#     while (a1 != 0) {
#         s0 *= a0;
#         a1 -= 1;
#     }
#     return s0;
# }
#
# FIXME There's a CC error with this function!
# The big all-caps comments should give you a hint about what's
# missing. Another hint: what does the "s" in "s0" stand for?
naive_pow:
    # BEGIN PROLOGUE
    # Using reg s0 without saving it is a CC violation,
    # So we need to save it on the stack.
    # END PROLOGUE
    # FIXME Add code to save the value of s0 on the stack
    addi sp, sp, -4
    sw s0, 0(sp)
    # Now we can use s0 to store the result
    li s0, 1
naive_pow_loop:
    beq a1, zero, naive_pow_end
    mul s0, s0, a0
    addi a1, a1, -1
    j naive_pow_loop
naive_pow_end:
    mv a0, s0
    # BEGIN EPILOGUE
    # FIXME Add code to restore the value of s0 from the stack
    # END EPILOGUE
    lw s0, 0(sp)
    addi sp, sp, 4
    # Now we can return the result in a0
    ret

# Increments the elements of an array in-place.
# a0 holds the address of the start of the array, and a1 holds
# the number of elements it contains.
#
# This function calls the "helper_fn" function, which takes in an
# address as argument and increments the 32-bit value stored there.
inc_arr:
    # BEGIN PROLOGUE
    # FIXME What other registers need to be saved?
    # Using s0, s1 without saving them is a CC violation,
    # so we need to save them on the stack.
    # We also need to save ra, since we will call helper_fn
    # Normaliy say, t series registers (t0, t1) don't need to be saved
    # because they are temporary registers and can be overwritten
    # by the function.
    # but here we need to preserve t0 because we use it
    # as a counter in the loop.
    # in other words, t0 is used across function calls
    addi sp, sp, -12
    sw ra, 0(sp)
    sw s0, 4(sp) # Save s0
    sw s1, 8(sp) # Save s1
    # END PROLOGUE
    mv s0, a0 # Copy start of array to saved register
    mv s1, a1 # Copy length of array to saved register
    li t0, 0 # Initialize counter to 0
inc_arr_loop:
    beq t0, s1, inc_arr_end
    slli t1, t0, 2 # Convert array index to byte offset
    add a0, s0, t1 # Add offset to start of array
    # Prepare to call helper_fn
    #
    # FIXME Add code to preserve the value in t0 before we call helper_fn
    # Hint: What does the "t" in "t0" stand for?
    # Also ask yourself this: why don't we need to preserve t1?
    #
    addi sp sp -4
    sw t0, 0(sp) # Save t0 on the stack
    jal helper_fn
    lw t0, 0(sp) # Restore t0 from the stack
    addi sp, sp, 4 
    # Finished call for helper_fn
    addi t0, t0, 1 # Increment counter
    j inc_arr_loop
inc_arr_end:
    # BEGIN EPILOGUE
    lw ra, 0(sp)
    lw s0, 4(sp) # Restore s0
    lw s1, 8(sp) # Restore s1
    addi sp, sp, 12 # Restore stack pointer
    # END EPILOGUE
    ret

# This helper function adds 1 to the value at the memory address in a0.
# It doesn't return anything.
# C pseudocode for what it does: "*a0 = *a0 + 1"
#
# FIXME This function also violates calling convention, but it might not
# be reported by the Venus CC checker (try and figure out why).
# You should fix the bug anyway by filling in the prologue and epilogue
# as appropriate.
helper_fn:
    # BEGIN PROLOGUE
    # Using s0 without saving it is a CC violation,
    # so we need to save it on the stack.
    # END PROLOGUE
    addi sp, sp, -4
    sw s0, 4(sp) # Save s0
    lw t1, 0(a0)
    addi s0, t1, 1
    sw s0, 0(a0)
    # BEGIN EPILOGUE
    # Restore the saved registers
    lw s0, 0(sp) # Restore s0
    addi sp, sp, 4 # Restore stack pointer
    # END EPILOGUE
    ret

# YOU CAN IGNORE EVERYTHING BELOW THIS COMMENT

# Checks the result of inc_arr, which should contain 2 3 4 5 6 after
# one call.
# You can safely ignore this function; it has no errors.
check_arr:
    la t0, exp_inc_array_result
    la t1, array
    addi t2, t1, 20 # Last element is 5*4 bytes off
check_arr_loop:
    beq t1, t2, check_arr_end
    lw t3, 0(t0)
    lw t4, 0(t1)
    bne t3, t4, failure
    addi t0, t0, 4
    addi t1, t1, 4
    j check_arr_loop
check_arr_end:
    ret
    

# This isn't really a function - it just prints a message, then
# terminates the program on failure. Think of it like an exception.
failure:
    li a0, 4 # String print ecall
    la a1, failure_message
    ecall
    li a0, 10 # Exit ecall
    ecall
    

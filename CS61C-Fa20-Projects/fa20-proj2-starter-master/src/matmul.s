.globl matmul

.text
# =======================================================
# FUNCTION: Matrix Multiplication of 2 integer matrices
# 	d = matmul(m0, m1)
# Arguments:
# 	a0 (int*)  is the pointer to the start of m0 
#	a1 (int)   is the # of rows (height) of m0
#	a2 (int)   is the # of columns (width) of m0
#	a3 (int*)  is the pointer to the start of m1
# 	a4 (int)   is the # of rows (height) of m1
#	a5 (int)   is the # of columns (width) of m1
#	a6 (int*)  is the pointer to the the start of d
# Returns:
#	None (void), sets d = matmul(m0, m1)
# Exceptions:
#   Make sure to check in top to bottom order!
#   - If the dimensions of m0 do not make sense,
#     this function terminates the program with exit code 72.
#   - If the dimensions of m1 do not make sense,
#     this function terminates the program with exit code 73.
#   - If the dimensions of m0 and m1 don't match,
#     this function terminates the program with exit code 74.
#   - If the pointer to d is null,
#     this function terminates the program with exit code 75.
# =======================================================
matmul:
    # Prologue: Save registers and return address
    addi sp, sp, -44
    sw ra, 40(sp)    # Save return address
    sw s0, 36(sp)
    sw s1, 32(sp)
    sw s2, 28(sp)
    sw s3, 24(sp)
    sw s4, 20(sp)
    sw s5, 16(sp)
    sw s6, 12(sp)
    sw s7, 8(sp)
    sw s8, 4(sp)
    sw s9, 0(sp)

    # Move arguments to saved registers
    mv s0, a0        # s0 = m0 base pointer
    mv s1, a3        # s1 = m1 base pointer
    mv s2, a6        # s2 = d base pointer
    mv s3, a1        # s3 = m0 rows
    mv s4, a2        # s4 = m0 columns
    mv s5, a5        # s5 = m1 columns

    # Error checks
    li t0, 1
    blt s3, t0, error_m0_null    # Check m0 rows >= 1
    blt s4, t0, error_m0_null    # Check m0 columns >= 1
    blt a4, t0, error_m1_null    # Check m1 rows >= 1 (a4 still valid)
    blt s5, t0, error_m1_null    # Check m1 columns >= 1
    bne s4, a4, error_m0_m1_dim  # Check m0 columns == m1 rows
    beqz s2, error_d_null        # Check d pointer not null

    # Initialize row index i = 0
    li s6, 0          # s6 = i

outer_loop:
    bge s6, s3, outer_loop_end   # If i >= m0 rows, break
    # Compute m0 row i pointer: s8 = m0 + i * m0_cols * 4
    mul t0, s6, s4    # i * m0_cols
    slli t0, t0, 2    # Multiply by 4 (bytes per int)
    add s8, s0, t0    # s8 = address of row i in m0

    # Compute d row i pointer: s9 = d + i * m1_cols * 4
    mul t0, s6, s5    # i * m1_cols
    slli t0, t0, 2    # Multiply by 4
    add s9, s2, t0    # s9 = address of row i in d

    # Initialize column index j = 0
    li s7, 0          # s7 = j

inner_loop:
    bge s7, s5, inner_loop_end   # If j >= m1 columns, break
    # Compute m1 column j start address: t1 = m1 + j * 4
    slli t1, s7, 2    # j * 4
    add t1, s1, t1    # t1 = address of column j in m1

    # Set up arguments for dot function
    mv a0, s8         # a0 = pointer to m0 row i
    mv a1, t1         # a1 = pointer to m1 column j
    mv a2, s4         # a2 = vector length (inner dimension, m0 columns)
    li a3, 1          # a3 = stride for v0 (contiguous)
    mv a4, s5         # a4 = stride for v1 (skip m1 columns per element)
    jal dot           # Call dot function, result in a0

    # Compute d[i][j] address: t0 = d_row_i + j * 4
    slli t0, s7, 2    # j * 4
    add t0, s9, t0    # t0 = address of d[i][j]
    sw a0, 0(t0)      # Store dot product result to d[i][j]

    # Increment j
    addi s7, s7, 1
    j inner_loop

inner_loop_end:
    # Increment i
    addi s6, s6, 1
    j outer_loop

outer_loop_end:
    # Epilogue: Restore registers and return
    lw s9, 0(sp)
    lw s8, 4(sp)
    lw s7, 8(sp)
    lw s6, 12(sp)
    lw s5, 16(sp)
    lw s4, 20(sp)
    lw s3, 24(sp)
    lw s2, 28(sp)
    lw s1, 32(sp)
    lw s0, 36(sp)
    lw ra, 40(sp)
    addi sp, sp, 44
    ret

error_m0_null:
    # Restore registers and exit with code 72
    lw s9, 0(sp)
    lw s8, 4(sp)
    lw s7, 8(sp)
    lw s6, 12(sp)
    lw s5, 16(sp)
    lw s4, 20(sp)
    lw s3, 24(sp)
    lw s2, 28(sp)
    lw s1, 32(sp)
    lw s0, 36(sp)
    lw ra, 40(sp)
    addi sp, sp, 44
    li a1, 72
    jal exit2

error_m1_null:
    # Restore registers and exit with code 73
    lw s9, 0(sp)
    lw s8, 4(sp)
    lw s7, 8(sp)
    lw s6, 12(sp)
    lw s5, 16(sp)
    lw s4, 20(sp)
    lw s3, 24(sp)
    lw s2, 28(sp)
    lw s1, 32(sp)
    lw s0, 36(sp)
    lw ra, 40(sp)
    addi sp, sp, 44
    li a1, 73
    jal exit2

error_m0_m1_dim:
    # Restore registers and exit with code 74
    lw s9, 0(sp)
    lw s8, 4(sp)
    lw s7, 8(sp)
    lw s6, 12(sp)
    lw s5, 16(sp)
    lw s4, 20(sp)
    lw s3, 24(sp)
    lw s2, 28(sp)
    lw s1, 32(sp)
    lw s0, 36(sp)
    lw ra, 40(sp)
    addi sp, sp, 44
    li a1, 74
    jal exit2

error_d_null:
    # Restore registers and exit with code 75
    lw s9, 0(sp)
    lw s8, 4(sp)
    lw s7, 8(sp)
    lw s6, 12(sp)
    lw s5, 16(sp)
    lw s4, 20(sp)
    lw s3, 24(sp)
    lw s2, 28(sp)
    lw s1, 32(sp)
    lw s0, 36(sp)
    lw ra, 40(sp)
    addi sp, sp, 44
    li a1, 75
    jal exit2

.globl classify

.text
classify:
    # =====================================
    # COMMAND LINE ARGUMENTS
    # =====================================
    # Prologue: Save registers
    addi sp, sp, -60
    sw ra, 56(sp)
    sw s0, 52(sp)   # print_classification flag
    sw s1, 48(sp)   # argv pointer
    sw s2, 44(sp)   # m0 pointer
    sw s3, 40(sp)   # m0 rows
    sw s4, 36(sp)   # m0 columns
    sw s5, 32(sp)   # m1 pointer
    sw s6, 28(sp)   # m1 rows
    sw s7, 24(sp)   # m1 columns
    sw s8, 20(sp)   # input pointer
    sw s9, 16(sp)   # input rows
    sw s10, 12(sp)  # input columns
    sw s11, 8(sp)   # intermediate output pointer
    sw t0, 4(sp)    # final output pointer
    sw t1, 0(sp)    # classification result

    # Check command line arguments (argc should be 5: program + 4 args)
    li t2, 5
    bne a0, t2, arg_error
    mv s0, a2        # s0 = print_classification flag
    mv s1, a1        # s1 = argv

    # =====================================
    # LOAD MATRICES (使用正确的 read_matrix)
    # =====================================
    # Load pretrained m0
    lw a0, 4(s1)     # a0 = M0_PATH (argv[1])
    addi sp, sp, -8  # Allocate space for row/col pointers
    mv a1, sp        # a1 = pointer to row output
    addi a2, sp, 4   # a2 = pointer to col output
    jal read_matrix
    mv s2, a0        # s2 = m0 pointer
    lw s3, 0(sp)     # s3 = m0 rows
    lw s4, 4(sp)     # s4 = m0 columns

    # Load pretrained m1
    lw a0, 8(s1)     # a0 = M1_PATH (argv[2])
    mv a1, sp        # a1 = pointer to row output
    addi a2, sp, 4   # a2 = pointer to col output
    jal read_matrix
    mv s5, a0        # s5 = m1 pointer
    lw s6, 0(sp)     # s6 = m1 rows
    lw s7, 4(sp)     # s7 = m1 columns

    # Load input matrix
    lw a0, 12(s1)    # a0 = INPUT_PATH (argv[3])
    mv a1, sp        # a1 = pointer to row output
    addi a2, sp, 4   # a2 = pointer to col output
    jal read_matrix
    mv s8, a0        # s8 = input pointer
    lw s9, 0(sp)     # s9 = input rows
    lw s10, 4(sp)    # s10 = input columns
    addi sp, sp, 8   # Deallocate stack space

    # =====================================
    # RUN LAYERS
    # =====================================
    # 1. LINEAR LAYER: m0 * input
    # Check dimensions: m0 columns must equal input rows
    bne s4, s9, dimension_error

    # Allocate memory for intermediate output (m0 * input)
    mul t2, s3, s10   # output size: m0_rows * input_cols
    slli a0, t2, 2    # bytes: elements * 4
    jal malloc
    beqz a0, malloc_error
    mv s11, a0        # s11 = intermediate output pointer

    # Perform matmul: m0 * input
    mv a0, s2         # a0 = m0 pointer
    mv a1, s3         # a1 = m0 rows
    mv a2, s4         # a2 = m0 columns
    mv a3, s8         # a3 = input pointer
    mv a4, s9         # a4 = input rows
    mv a5, s10        # a5 = input columns
    mv a6, s11        # a6 = output pointer
    jal matmul

    # 2. NONLINEAR LAYER: ReLU(intermediate output)
    mul t2, s3, s10   # number of elements in intermediate output
    mv a0, s11        # a0 = pointer to intermediate output
    mv a1, t2         # a1 = number of elements
    jal relu          # ReLU in-place

    # 3. LINEAR LAYER: m1 * ReLU output
    # Check dimensions: m1 columns must equal ReLU output rows
    bne s7, s3, dimension_error

    # Allocate memory for final output (m1 * ReLU_output)
    mul t2, s6, s10   # output size: m1_rows * input_cols
    slli a0, t2, 2    # bytes: elements * 4
    jal malloc
    beqz a0, malloc_error
    sw a0, 4(sp)      # Store final output pointer in stack slot

    # Perform matmul: m1 * ReLU_output
    mv a0, s5         # a0 = m1 pointer
    mv a1, s6         # a1 = m1 rows
    mv a2, s7         # a2 = m1 columns
    mv a3, s11        # a3 = ReLU output pointer
    mv a4, s3         # a4 = ReLU output rows
    mv a5, s10        # a5 = ReLU output columns
    lw a6, 4(sp)      # a6 = final output pointer
    jal matmul

    # Free intermediate output
    mv a0, s11
    jal free

    # =====================================
    # WRITE OUTPUT
    # =====================================
    lw a0, 16(s1)     # a0 = OUTPUT_PATH (argv[4])
    lw a1, 4(sp)      # a1 = final output pointer
    mv a2, s6         # a2 = output rows (m1_rows)
    mv a3, s10        # a3 = output columns (input_cols)
    jal write_matrix

    # =====================================
    # CALCULATE CLASSIFICATION/LABEL
    # =====================================
    mul t2, s6, s10   # number of elements in final output
    lw a0, 4(sp)      # a0 = pointer to final output
    mv a1, t2         # a1 = number of elements
    jal argmax        # a0 = classification index
    sw a0, 0(sp)      # Store classification result

    # =====================================
    # PRINT CLASSIFICATION (if needed)
    # =====================================
    bnez s0, skip_print
    lw a1, 0(sp)      # a1 = classification index to print
    jal print_int
    li a1, '\n'
    jal print_char

skip_print:
    # Free final output
    lw a0, 4(sp)
    jal free

    # Set return value
    lw a0, 0(sp)      # a0 = classification index

    # Epilogue: Restore registers
    lw t1, 0(sp)
    lw t0, 4(sp)
    lw s11, 8(sp)
    lw s10, 12(sp)
    lw s9, 16(sp)
    lw s8, 20(sp)
    lw s7, 24(sp)
    lw s6, 28(sp)
    lw s5, 32(sp)
    lw s4, 36(sp)
    lw s3, 40(sp)
    lw s2, 44(sp)
    lw s1, 48(sp)
    lw s0, 52(sp)
    lw ra, 56(sp)
    addi sp, sp, 60
    ret

arg_error:
    # Restore stack and exit
    lw t1, 0(sp)
    lw t0, 4(sp)
    lw s11, 8(sp)
    lw s10, 12(sp)
    lw s9, 16(sp)
    lw s8, 20(sp)
    lw s7, 24(sp)
    lw s6, 28(sp)
    lw s5, 32(sp)
    lw s4, 36(sp)
    lw s3, 40(sp)
    lw s2, 44(sp)
    lw s1, 48(sp)
    lw s0, 52(sp)
    lw ra, 56(sp)
    addi sp, sp, 60
    li a1, 89
    jal exit2

malloc_error:
    # Restore stack and exit
    lw t1, 0(sp)
    lw t0, 4(sp)
    lw s11, 8(sp)
    lw s10, 12(sp)
    lw s9, 16(sp)
    lw s8, 20(sp)
    lw s7, 24(sp)
    lw s6, 28(sp)
    lw s5, 32(sp)
    lw s4, 36(sp)
    lw s3, 40(sp)
    lw s2, 44(sp)
    lw s1, 48(sp)
    lw s0, 52(sp)
    lw ra, 56(sp)
    addi sp, sp, 60
    li a1, 88
    jal exit2

dimension_error:
    # Restore stack and exit
    lw t1, 0(sp)
    lw t0, 4(sp)
    lw s11, 8(sp)
    lw s10, 12(sp)
    lw s9, 16(sp)
    lw s8, 20(sp)
    lw s7, 24(sp)
    lw s6, 28(sp)
    lw s5, 32(sp)
    lw s4, 36(sp)
    lw s3, 40(sp)
    lw s2, 44(sp)
    lw s1, 48(sp)
    lw s0, 52(sp)
    lw ra, 56(sp)
    addi sp, sp, 60
    li a1, 74
    jal exit2

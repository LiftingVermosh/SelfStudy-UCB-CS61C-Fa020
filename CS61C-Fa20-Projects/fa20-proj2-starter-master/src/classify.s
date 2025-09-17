.globl classify

.text
classify:
    # =====================================
    # COMMAND LINE ARGUMENTS
    # =====================================
    # Prologue: Save registers
    addi sp, sp, -60
    sw ra, 56(sp)
    sw t0, 52(sp)
    sw t1, 48(sp)
    sw s0, 44(sp)   # print_classification flag
    sw s1, 40(sp)   # argv pointer
    sw s2, 36(sp)   # m0 pointer
    sw s3, 32(sp)   # m0 rows
    sw s4, 28(sp)   # m0 columns
    sw s5, 24(sp)   # m1 pointer
    sw s6, 20(sp)   # m1 rows
    sw s7, 16(sp)   # m1 columns
    sw s8, 12(sp)   # input pointer
    sw s9, 8(sp)    # input rows
    sw s10, 4(sp)   # input columns
    sw s11, 0(sp)   # output pointer (after matmul)

    # Check command line arguments
    li t0, 5
    bne a0, t0, arg_error
    mv s0, a2        # s0 = print_classification flag
    mv s1, a1        # s1 = argv

    # =====================================
    # LOAD MATRICES
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
    mul t0, s3, s10   # output rows: m0_rows * input_cols
    slli a0, t0, 2    # bytes: elements * 4
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
    mul t0, s3, s10   # number of elements in intermediate output
    mv a0, s11        # a0 = pointer to intermediate output
    mv a1, t0         # a1 = number of elements
    jal relu          # ReLU in-place

    # 3. LINEAR LAYER: m1 * ReLU output
    bne s7, s3, dimension_error

    # Allocate memory for final output (m1 * ReLU_output)
    mul t0, s6, s10   # output rows: m1_rows * input_cols
    slli a0, t0, 2    # bytes: elements * 4
    jal malloc
    beqz a0, malloc_error
    mv t1, a0         # t1 = final output pointer

    # Perform matmul: m1 * ReLU_output
    mv a0, s5         # a0 = m1 pointer
    mv a1, s6         # a1 = m1 rows
    mv a2, s7         # a2 = m1 columns
    mv a3, s11        # a3 = ReLU output pointer (shape: s3 x s10)
    mv a4, s3         # a4 = ReLU output rows (s3)
    mv a5, s10        # a5 = ReLU output columns (s10)
    mv a6, t1         # a6 = final output pointer
    jal matmul

    # Free intermediate output (s11) after use
    mv a0, s11
    jal free

    # =====================================
    # CALCULATE CLASSIFICATION/LABEL
    # =====================================
    mul t2, s6, s10   # number of elements in final output
    mv a0, t1         # a0 = pointer to final output
    mv a1, t2         # a1 = number of elements
    jal argmax        # a0 = classification index

    # Save classification result
    mv t3, a0         # t3 = classification index

    # Free final output memory
    mv a0, t1
    jal free

    # =====================================
    # WRITE OUTPUT
    # =====================================
    lw a0, 16(s1)     # OUTPUT_PATH (argv[4])

    # Write output matrix to file
    lw a0, 16(s1)     # a0 = OUTPUT_PATH
    mv a1, t1         # a1 = final output pointer
    mv a2, s6         # a2 = output rows (m1_rows)
    mv a3, s10        # a3 = output columns (input_cols)
    jal write_matrix

    # free final output
    mv a0, t1
    jal free

    # =====================================
    # PRINT CLASSIFICATION (if needed)
    # =====================================
    # Now print classification if print_classification flag is zero
    bnez s0, skip_print
    mv a1, t3         # a1 = classification index to print
    jal print_int
    li a1, '\n'
    jal print_char
skip_print:
    # Set return value
    mv a0, t3         # a0 = classification index

    # Epilogue: Restore registers
    lw s11, 0(sp)
    lw s10, 4(sp)
    lw s9, 8(sp)
    lw s8, 12(sp)
    lw s7, 16(sp)
    lw s6, 20(sp)
    lw s5, 24(sp)
    lw s4, 28(sp)
    lw s3, 32(sp)
    lw s2, 36(sp)
    lw s1, 40(sp)
    lw s0, 44(sp)
    lw ra, 48(sp)
    addi sp, sp, 52
    ret

arg_error:
    li a1, 89
    jal exit2

malloc_error:
    li a1, 88
    jal exit2

dimension_error:
    li a1, 74
    jal exit2

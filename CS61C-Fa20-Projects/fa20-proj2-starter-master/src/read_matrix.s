.globl read_matrix

.text
# ==============================================================================
# FUNCTION: Allocates memory and reads in a binary file as a matrix of integers
#
# FILE FORMAT:
#   The first 8 bytes are two 4 byte ints representing the # of rows and columns
#   in the matrix. Every 4 bytes afterwards is an element of the matrix in
#   row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is a pointer to an integer, we will set it to the number of rows
#   a2 (int*)  is a pointer to an integer, we will set it to the number of columns
# Returns:
#   a0 (int*)  is the pointer to the matrix in memory
# Exceptions:
# - If malloc returns an error,
#   this function terminates the program with error code 88.
# - If you receive an fopen error or eof, 
#   this function terminates the program with error code 90.
# - If you receive an fread error or eof,
#   this function terminates the program with error code 91.
# - If you receive an fclose error or eof,
#   this function terminates the program with error code 92.
# ==============================================================================
read_matrix:

    # Prologue: Save registers
    addi sp, sp, -28
    sw ra, 24(sp)
    sw s0, 20(sp)   # File descriptor
    sw s1, 16(sp)   # Number of rows
    sw s2, 12(sp)   # Number of columns  
    sw s3, 8(sp)    # Matrix data pointer
    sw s4, 4(sp)    # Header buffer pointer
    sw s5, 0(sp)    # Number of elements

    # Save output parameter pointers
    mv t0, a1       # Save rows pointer
    mv t1, a2       # Save columns pointer
    sw t0, 28(sp)   # Store rows pointer on stack
    sw t1, 32(sp)   # Store columns pointer on stack

    # Open the file
    mv a1, a0       # a1 = filename pointer
    li a2, 0        # a2 = read mode (0)
    jal fopen       # fopen(a1: filename, a2: mode)
    blt a0, x0, error_fopen  # Check for fopen error
    mv s0, a0       # s0 = file descriptor

    # Allocate memory for file header (8 bytes)
    li a0, 8        # a0 = 8 bytes for header
    jal malloc      # malloc(a0: size)
    blt a0, x0, error_malloc  # Check for malloc error
    mv s4, a0       # s4 = header buffer pointer

    # Read the file header (8 bytes)
    mv a1, s0       # a1 = file descriptor
    mv a2, s4       # a2 = buffer pointer
    li a3, 8        # a3 = 8 bytes to read
    jal fread       # fread(a1: fd, a2: buffer, a3: size)
    li t0, 8
    blt a0, t0, error_fread  # Check if read 8 bytes successfully

    # Extract matrix dimensions from header
    lw s1, 0(s4)    # s1 = number of rows (first 4 bytes)
    lw s2, 4(s4)    # s2 = number of columns (next 4 bytes)

    # Free header buffer memory
    mv a0, s4       # a0 = header buffer pointer
    jal free        # free(a0: pointer)

    # Calculate matrix data size (number of elements * 4 bytes)
    mul s5, s1, s2  # s5 = rows * columns (number of elements)
    slli a0, s5, 2  # a0 = number of elements * 4 (bytes)
    jal malloc      # malloc(a0: size)
    blt a0, x0, error_malloc  # Check for malloc error
    mv s3, a0       # s3 = matrix data pointer

    # Read matrix data (file pointer is now at byte 8, after header)
    mv a1, s0       # a1 = file descriptor
    mv a2, s3       # a2 = matrix data buffer
    slli a3, s5, 2  # a3 = number of bytes to read (elements * 4)
    jal fread       # fread(a1: fd, a2: buffer, a3: size)
    slli t1, s5, 2  # t1 = expected bytes (elements * 4)
    blt a0, t1, error_fread  # Check if read all data successfully

    # Close the file
    mv a1, s0       # a1 = file descriptor
    jal fclose      # fclose(a1: fd)
    blt a0, x0, error_fclose  # Check for fclose error

    # Set output parameters
    lw t0, 28(sp)   # t0 = rows pointer
    sw s1, 0(t0)    # Store number of rows
    lw t1, 32(sp)   # t1 = columns pointer
    sw s2, 0(t1)    # Store number of columns

    # Return matrix data pointer
    mv a0, s3       # a0 = matrix data pointer

read_matrix_end:
    # Epilogue: Restore registers
    lw s5, 0(sp)
    lw s4, 4(sp)
    lw s3, 8(sp)
    lw s2, 12(sp)
    lw s1, 16(sp)
    lw s0, 20(sp)
    lw ra, 24(sp)
    addi sp, sp, 28
    ret

error_fopen:
    # Epilogue for fopen error
    lw s5, 0(sp)
    lw s4, 4(sp)
    lw s3, 8(sp)
    lw s2, 12(sp)
    lw s1, 16(sp)
    lw s0, 20(sp)
    lw ra, 24(sp)
    addi sp, sp, 28
    li a1, 90       # Error code 90 for fopen error
    jal exit2       # exit2(a1: error_code)

error_malloc:
    # Epilogue for malloc error
    lw s5, 0(sp)
    lw s4, 4(sp)
    lw s3, 8(sp)
    lw s2, 12(sp)
    lw s1, 16(sp)
    lw s0, 20(sp)
    lw ra, 24(sp)
    addi sp, sp, 28
    li a1, 88       # Error code 88 for malloc error
    jal exit2       # exit2(a1: error_code)

error_fread:
    # Epilogue for fread error
    lw s5, 0(sp)
    lw s4, 4(sp)
    lw s3, 8(sp)
    lw s2, 12(sp)
    lw s1, 16(sp)
    lw s0, 20(sp)
    lw ra, 24(sp)
    addi sp, sp, 28
    li a1, 91       # Error code 91 for fread error
    jal exit2       # exit2(a1: error_code)

error_fclose:
    # Epilogue for fclose error
    lw s5, 0(sp)
    lw s4, 4(sp)
    lw s3, 8(sp)
    lw s2, 12(sp)
    lw s1, 16(sp)
    lw s0, 20(sp)
    lw ra, 24(sp)
    addi sp, sp, 28
    li a1, 92       # Error code 92 for fclose error
    jal exit2       # exit2(a1: error_code)

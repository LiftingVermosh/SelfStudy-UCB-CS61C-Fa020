.globl write_matrix

.text
# ==============================================================================
# FUNCTION: Writes a matrix of integers into a binary file
# FILE FORMAT:
#   The first 8 bytes of the file will be two 4 byte ints representing the
#   numbers of rows and columns respectively. Every 4 bytes thereafter is an
#   element of the matrix in row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is the pointer to the start of the matrix in memory
#   a2 (int)   is the number of rows in the matrix
#   a3 (int)   is the number of columns in the matrix
# Returns:
#   None
# Exceptions:
# - If you receive an fopen error or eof,
#   this function terminates the program with error code 93.
# - If you receive an fwrite error or eof,
#   this function terminates the program with error code 94.
# - If you receive an fclose error or eof,
#   this function terminates the program with error code 95.
# ==============================================================================
write_matrix:

    # Prologue: Save registers
    addi sp, sp, -28
    sw ra, 24(sp)
    sw s0, 20(sp)   # File descriptor
    sw s1, 16(sp)   # Matrix data pointer
    sw s2, 12(sp)   # Number of rows
    sw s3, 8(sp)    # Number of columns
    sw s4, 4(sp)    # Header buffer pointer
    sw s5, 0(sp)    # Number of elements

    # Save arguments
    mv s1, a1       # s1 = matrix data pointer
    mv s2, a2       # s2 = number of rows
    mv s3, a3       # s3 = number of columns

    # Open the file with write mode
    mv a1, a0       # a1 = filename pointer
    li a2, 1        # a2 = write mode (1)
    jal fopen       # fopen(a1: filename, a2: mode)
    blt a0, x0, error_fopen  # Check for fopen error
    mv s0, a0       # s0 = file descriptor

    # Allocate memory for file header (8 bytes)
    li a0, 8        # a0 = 8 bytes for header
    jal malloc      # malloc(a0: size)
    blt a0, x0, error_malloc  # Check for malloc error
    mv s4, a0       # s4 = header buffer pointer

    # Store row and column counts in header
    sw s2, 0(s4)    # Store row count at offset 0
    sw s3, 4(s4)    # Store column count at offset 4

    # Write file header (8 bytes)
    mv a1, s0       # a1 = file descriptor
    mv a2, s4       # a2 = header buffer
    li a3, 2        # a3 = 2 items (row and column)
    li a4, 4        # a4 = 4 bytes per item
    jal fwrite      # fwrite(a1: fd, a2: buffer, a3: count, a4: size)
    li t0, 2
    blt a0, t0, error_fwrite  # Check if wrote 2 items successfully

    # Free header buffer memory
    mv a0, s4       # a0 = header buffer pointer
    jal free        # free(a0: pointer)

    # Calculate number of matrix elements
    mul s5, s2, s3  # s5 = rows * columns (number of elements)

    # Write matrix data
    mv a1, s0       # a1 = file descriptor
    mv a2, s1       # a2 = matrix data pointer
    mv a3, s5       # a3 = number of elements to write
    li a4, 4        # a4 = 4 bytes per element
    jal fwrite      # fwrite(a1: fd, a2: buffer, a3: count, a4: size)
    blt a0, s5, error_fwrite  # Check if wrote all elements successfully

    # Flush the file (optional but good practice)
    mv a1, s0       # a1 = file descriptor
    jal fflush      # fflush(a1: fd)
    # Note: fflush error is not critical for this assignment

    # Close the file
    mv a1, s0       # a1 = file descriptor
    jal fclose      # fclose(a1: fd)
    blt a0, x0, error_fclose  # Check for fclose error

write_matrix_end:
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
    li a1, 93       # Error code 93 for fopen error
    jal exit2       # exit2(a1: error_code)

error_malloc:
    # Close file if malloc failed after fopen
    mv a1, s0
    jal fclose
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

error_fwrite:
    # Close file if fwrite failed
    mv a1, s0
    jal fclose
    # Epilogue for fwrite error
    lw s5, 0(sp)
    lw s4, 4(sp)
    lw s3, 8(sp)
    lw s2, 12(sp)
    lw s1, 16(sp)
    lw s0, 20(sp)
    lw ra, 24(sp)
    addi sp, sp, 28
    li a1, 94       # Error code 94 for fwrite error
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
    li a1, 95       # Error code 95 for fclose error
    jal exit2       # exit2(a1: error_code)

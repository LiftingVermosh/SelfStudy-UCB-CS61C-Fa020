#!/usr/bin/env python3
# create_reference_files.py

import struct
import os

def create_binary_file(filename, rows, cols, data):
    """Create a binary file with the given matrix data"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'wb') as f:
        # Write header (rows and columns as 4-byte integers)
        f.write(struct.pack('<ii', rows, cols))
        
        # Write matrix data as 4-byte integers
        for value in data:
            f.write(struct.pack('<i', value))

# Create reference files for various test cases
create_binary_file("outputs/test_write_matrix/reference_simple.bin", 2, 2, [1, 2, 3, 4])
create_binary_file("outputs/test_write_matrix/reference_1x1.bin", 1, 1, [42])
create_binary_file("outputs/test_write_matrix/reference_2x3.bin", 2, 3, [1, 2, 3, 4, 5, 6])
create_binary_file("outputs/test_write_matrix/reference_3x4.bin", 3, 4, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
create_binary_file("outputs/test_write_matrix/reference_negative.bin", 2, 2, [-1, -2, -3, -4])
create_binary_file("outputs/test_write_matrix/reference_zeros.bin", 2, 2, [0, 0, 0, 0])
create_binary_file("outputs/test_write_matrix/reference_max_values.bin", 2, 2, [2147483647, -2147483648, 2147483647, -2147483648])
create_binary_file("outputs/test_write_matrix/reference_single_row.bin", 1, 3, [1, 2, 3])
create_binary_file("outputs/test_write_matrix/reference_single_column.bin", 3, 1, [1, 2, 3])

print("Reference files created successfully!")

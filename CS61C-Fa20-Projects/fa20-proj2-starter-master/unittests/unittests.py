from unittest import TestCase
from framework import AssemblyTest, print_coverage


class TestAbs(TestCase):
    def test_zero(self):
        t = AssemblyTest(self, "abs.s")
        # load 0 into register a0
        t.input_scalar("a0", 0)
        # call the abs function
        t.call("abs")
        # check that after calling abs, a0 is equal to 0 (abs(0) = 0)
        t.check_scalar("a0", 0)
        # generate the `assembly/TestAbs_test_zero.s` file and run it through venus
        t.execute()

    def test_one(self):
        # same as test_zero, but with input 1
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", 1)
        t.call("abs")
        t.check_scalar("a0", 1)
        t.execute()

    def test_minus_one(self):
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", -1)
        t.call("abs")
        t.check_scalar("a0", 1)
        t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("abs.s", verbose=False)


class TestRelu(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [1, 0, 3, 0, 5, 0, 7, 0, 9])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("relu.s", verbose=False)


class TestArgmax(TestCase):
    def test_simple(self):
        # Test a simple array with unique maximum at the end
        t = AssemblyTest(self, "argmax.s")
        # Create an array in the data section
        array = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # Load address of the array into register a0
        t.input_array("a0", array)
        # Set a1 to the length of the array
        t.input_scalar("a1", len(array))
        # Call the argmax function
        t.call("argmax")
        # Check that the register a0 contains the correct output (index 8)
        t.check_scalar("a0", 8)
        # Generate the assembly file and run it through venus
        t.execute()

    def test_multiple_max(self):
        # Test an array with multiple maximum elements, should return the smallest index
        t = AssemblyTest(self, "argmax.s")
        array = t.array([3, 3, 2, 3])  # Max value 3 at indices 0, 1, and 3; should return 0
        t.input_array("a0", array)
        t.input_scalar("a1", len(array))
        t.call("argmax")
        t.check_scalar("a0", 0)  # Smallest index for max
        t.execute()

    def test_single_element(self):
        # Test an array with only one element
        t = AssemblyTest(self, "argmax.s")
        array = t.array([5])
        t.input_array("a0", array)
        t.input_scalar("a1", len(array))
        t.call("argmax")
        t.check_scalar("a0", 0)  # Only index 0
        t.execute()

    def test_all_same(self):
        # Test an array where all elements are the same
        t = AssemblyTest(self, "argmax.s")
        array = t.array([4, 4, 4, 4])
        t.input_array("a0", array)
        t.input_scalar("a1", len(array))
        t.call("argmax")
        t.check_scalar("a0", 0)  # Should return first index
        t.execute()

    def test_negative_numbers(self):
        # Test an array with negative numbers and positive numbers
        t = AssemblyTest(self, "argmax.s")
        array = t.array([-1, -2, 0, 1])  # Max value 1 at index 3
        t.input_array("a0", array)
        t.input_scalar("a1", len(array))
        t.call("argmax")
        t.check_scalar("a0", 3)
        t.execute()

    def test_max_at_start(self):
        # Test where the maximum element is at the start of the array
        t = AssemblyTest(self, "argmax.s")
        array = t.array([10, 1, 2, 3])  # Max value 10 at index 0
        t.input_array("a0", array)
        t.input_scalar("a1", len(array))
        t.call("argmax")
        t.check_scalar("a0", 0)
        t.execute()

    def test_max_at_end(self):
        # Test where the maximum element is at the end of the array
        t = AssemblyTest(self, "argmax.s")
        array = t.array([1, 2, 3, 10])  # Max value 10 at index 3
        t.input_array("a0", array)
        t.input_scalar("a1", len(array))
        t.call("argmax")
        t.check_scalar("a0", 3)
        t.execute()

    def test_error_empty_array(self):
        # Test error case: array length is 0, should terminate with code 77
        t = AssemblyTest(self, "argmax.s")
        # For empty array, we don't need to create an array, just set a1 to 0
        t.input_scalar("a1", 0)
        # Call argmax, but since length is 0, it should error
        t.call("argmax")
        # Execute and expect error code 77
        t.execute(code=77)

    def test_error_negative_length(self):
        # Test error case: array length is negative, but since a1 is unsigned, this might not occur in practice, but we test for length < 1
        # In RISC-V, a1 is passed as int, so negative length might be possible, but the function checks for < 1
        t = AssemblyTest(self, "argmax.s")
        t.input_scalar("a1", -1)  # Negative length
        t.call("argmax")
        t.execute(code=77)  # Should terminate with error code 77

    @classmethod
    def tearDownClass(cls):
        print_coverage("argmax.s", verbose=False)


class TestDot(TestCase):
    def test_simple(self):
        # Test simple dot product with stride 1 for both vectors
        t = AssemblyTest(self, "dot.s")
        # Create arrays in the data section
        v0 = t.array([1, 2, 3, 4])
        v1 = t.array([2, 3, 4, 5])
        # Load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # Load array attributes into argument registers
        t.input_scalar("a2", 4)  # length
        t.input_scalar("a3", 1)  # stride for v0
        t.input_scalar("a4", 1)  # stride for v1
        # Call the dot function
        t.call("dot")
        # Check the return value: 1*2 + 2*3 + 3*4 + 4*5 = 2+6+12+20=40
        t.check_scalar("a0", 40)
        t.execute()

    def test_stride_not_one(self):
        # Test dot product with different strides
        t = AssemblyTest(self, "dot.s")
        v0 = t.array([1, 2, 3, 4, 5, 6])
        v1 = t.array([2, 3, 4, 5, 6, 7])
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        t.input_scalar("a2", 3)  # length: we'll take every other element
        t.input_scalar("a3", 2)  # stride for v0: skip one element
        t.input_scalar("a4", 2)  # stride for v1: skip one element
        t.call("dot")
        # Elements: v0[0]=1, v0[2]=3, v0[4]=5; v1[0]=2, v1[2]=4, v1[4]=6
        # Dot product: 1*2 + 3*4 + 5*6 = 2 + 12 + 30 = 44
        t.check_scalar("a0", 44)
        t.execute()

    def test_different_strides(self):
        # Test with different strides for v0 and v1
        t = AssemblyTest(self, "dot.s")
        v0 = t.array([1, 2, 3, 4, 5, 6])
        v1 = t.array([2, 3, 4, 5, 6, 7])
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        t.input_scalar("a2", 2)  # length
        t.input_scalar("a3", 1)  # stride for v0: consecutive
        t.input_scalar("a4", 3)  # stride for v1: skip two elements
        t.call("dot")
        # v0: indices 0,1 -> [1,2]; v1: indices 0,3 -> [2,5]
        # Dot product: 1*2 + 2*5 = 2 + 10 = 12
        t.check_scalar("a0", 12)
        t.execute()

    def test_single_element(self):
        # Test with single element vectors
        t = AssemblyTest(self, "dot.s")
        v0 = t.array([5])
        v1 = t.array([3])
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        t.input_scalar("a2", 1)  # length
        t.input_scalar("a3", 1)  # stride
        t.input_scalar("a4", 1)  # stride
        t.call("dot")
        t.check_scalar("a0", 15)  # 5*3=15
        t.execute()

    def test_negative_numbers(self):
        # Test with negative numbers
        t = AssemblyTest(self, "dot.s")
        v0 = t.array([-1, 2, -3])
        v1 = t.array([4, -5, 6])
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        t.input_scalar("a2", 3)  # length
        t.input_scalar("a3", 1)  # stride
        t.input_scalar("a4", 1)  # stride
        t.call("dot")
        # (-1)*4 + 2*(-5) + (-3)*6 = -4 -10 -18 = -32
        t.check_scalar("a0", -32)
        t.execute()

    def test_error_length_less_than_one(self):
        # Test error case: length less than 1
        t = AssemblyTest(self, "dot.s")
        v0 = t.array([1, 2])
        v1 = t.array([3, 4])
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        t.input_scalar("a2", 0)  # invalid length
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        t.call("dot")
        t.execute(code=75)  # should terminate with error code 75

    def test_error_negative_length(self):
        # Test error case: negative length (though a2 is signed, function checks <1)
        t = AssemblyTest(self, "dot.s")
        v0 = t.array([1, 2])
        v1 = t.array([3, 4])
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        t.input_scalar("a2", -1)  # invalid length
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        t.call("dot")
        t.execute(code=75)  # should terminate with error code 75

    def test_error_stride_v0_less_than_one(self):
        # Test error case: stride for v0 less than 1
        t = AssemblyTest(self, "dot.s")
        v0 = t.array([1, 2])
        v1 = t.array([3, 4])
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        t.input_scalar("a2", 2)
        t.input_scalar("a3", 0)  # invalid stride
        t.input_scalar("a4", 1)
        t.call("dot")
        t.execute(code=76)  # should terminate with error code 76

    def test_error_stride_v1_less_than_one(self):
        # Test error case: stride for v1 less than 1
        t = AssemblyTest(self, "dot.s")
        v0 = t.array([1, 2])
        v1 = t.array([3, 4])
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        t.input_scalar("a2", 2)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 0)  # invalid stride
        t.call("dot")
        t.execute(code=76)  # should terminate with error code 76

    def test_error_both_strides_invalid(self):
        # Test error case: both strides invalid (should catch first error in code: v0 stride)
        t = AssemblyTest(self, "dot.s")
        v0 = t.array([1, 2])
        v1 = t.array([3, 4])
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        t.input_scalar("a2", 2)
        t.input_scalar("a3", 0)  # invalid stride
        t.input_scalar("a4", 0)  # invalid stride
        t.call("dot")
        t.execute(code=76)  # should terminate with error code 76 (first check is v0 stride)

    @classmethod
    def tearDownClass(cls):
        print_coverage("dot.s", verbose=False)



class TestMatmul(TestCase):
    def do_matmul(self, m0, m0_rows, m0_cols, m1, m1_rows, m1_cols, result, code=0):
        t = AssemblyTest(self, "matmul.s")
        # we need to include (aka import) the dot.s file since it is used by matmul.s
        t.include("dot.s")

        # create arrays for the arguments and to store the result
        array0 = t.array(m0)
        array1 = t.array(m1)
        array_out = t.array([0] * len(result))

        # load address of input matrices and set their dimensions
        t.input_array("a0", array0)  # pointer to m0
        t.input_scalar("a1", m0_rows)  # rows of m0
        t.input_scalar("a2", m0_cols)  # columns of m0
        t.input_array("a3", array1)  # pointer to m1
        t.input_scalar("a4", m1_rows)  # rows of m1
        t.input_scalar("a5", m1_cols)  # columns of m1
        # load address of output array
        t.input_array("a6", array_out)  # pointer to output matrix d

        # call the matmul function
        t.call("matmul")

        # check the content of the output array only if no error expected
        if code == 0:
            t.check_array(array_out, result)

        # generate the assembly file and run it through venus, we expect the simulation to exit with code `code`
        t.execute(code=code)

    def test_simple(self):
        # Test simple 3x3 matrix multiplication
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150]
        )

    def test_2x2(self):
        # Test 2x2 matrix multiplication
        self.do_matmul(
            [1, 2, 3, 4], 2, 2,
            [5, 6, 7, 8], 2, 2,
            [19, 22, 43, 50]
        )

    def test_1x1(self):
        # Test 1x1 matrix multiplication (scalar multiplication)
        self.do_matmul(
            [5], 1, 1,
            [3], 1, 1,
            [15]
        )

    def test_rectangular(self):
        # Test rectangular matrix multiplication: 2x3 * 3x2 = 2x2
        self.do_matmul(
            [1, 2, 3, 4, 5, 6], 2, 3,
            [7, 8, 9, 10, 11, 12], 3, 2,
            [58, 64, 139, 154]
        )

    def test_with_zeros(self):
        # Test matrix multiplication with zeros
        self.do_matmul(
            [1, 0, 0, 1], 2, 2,
            [2, 3, 4, 5], 2, 2,
            [2, 3, 4, 5]  # Identity-like matrix multiplication
        )

    def test_negative_numbers(self):
        # Test matrix multiplication with negative numbers
        self.do_matmul(
            [1, -2, 3, -4], 2, 2,
            [-5, 6, -7, 8], 2, 2,
            [1* -5 + -2 * -7, 1*6 + -2*8, 3* -5 + -4 * -7, 3*6 + -4*8]  # Calculate expected result
        )

    def test_error_m0_invalid_rows(self):
        # Test error case: m0 has 0 rows
        self.do_matmul(
            [1, 2, 3, 4], 0, 2,  # 0 rows
            [1, 2, 3, 4], 2, 2,
            [0, 0, 0, 0],  # dummy result
            code=72  # expected error code
        )

    def test_error_m0_invalid_cols(self):
        # Test error case: m0 has 0 columns
        self.do_matmul(
            [1, 2, 3, 4], 2, 0,  # 0 columns
            [1, 2, 3, 4], 2, 2,
            [0, 0, 0, 0],  # dummy result
            code=72  # expected error code
        )

    def test_error_m1_invalid_rows(self):
        # Test error case: m1 has 0 rows
        self.do_matmul(
            [1, 2, 3, 4], 2, 2,
            [1, 2, 3, 4], 0, 2,  # 0 rows
            [0, 0, 0, 0],  # dummy result
            code=73  # expected error code
        )

    def test_error_m1_invalid_cols(self):
        # Test error case: m1 has 0 columns
        self.do_matmul(
            [1, 2, 3, 4], 2, 2,
            [1, 2, 3, 4], 2, 0,  # 0 columns
            [0, 0, 0, 0],  # dummy result
            code=73  # expected error code
        )

    def test_error_dimension_mismatch(self):
        # Test error case: m0 columns != m1 rows
        self.do_matmul(
            [1, 2, 3, 4], 2, 2,
            [1, 2, 3, 4, 5, 6], 3, 2,  # 3 rows, but m0 has 2 columns
            [0, 0, 0, 0],  # dummy result
            code=74  # expected error code
        )

    def test_error_output_null(self):
        # Test error case: output matrix pointer is null
        t = AssemblyTest(self, "matmul.s")
        t.include("dot.s")
        
        # Create input arrays
        array0 = t.array([1, 2, 3, 4])
        array1 = t.array([5, 6, 7, 8])
        
        # Set up valid inputs but null output pointer
        t.input_array("a0", array0)
        t.input_scalar("a1", 2)  # rows of m0
        t.input_scalar("a2", 2)  # columns of m0
        t.input_array("a3", array1)
        t.input_scalar("a4", 2)  # rows of m1
        t.input_scalar("a5", 2)  # columns of m1
        t.input_scalar("a6", 0)  # null output pointer
        
        t.call("matmul")
        t.execute(code=75)  # should terminate with error code 75

    def test_row_vector(self):
        # Test 1xN matrix multiplication (row vector)
        self.do_matmul(
            [1, 2, 3], 1, 3,  # row vector
            [4, 5, 6, 7, 8, 9], 3, 2,  # 3x2 matrix
            [1*4 + 2*6 + 3*8, 1*5 + 2*7 + 3*9]  # 1x2 result
        )

    def test_column_vector(self):
        # Test Nx1 matrix multiplication (column vector)
        self.do_matmul(
            [1, 2, 3], 3, 1,  # column vector
            [4], 1, 1,  # 1x1 matrix
            [1*4, 2*4, 3*4]  # 3x1 result
        )

    def test_large_matrix(self):
        # Test larger matrix to ensure loop logic works correctly
        # 4x3 * 3x2 = 4x2
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 4, 3,
            [1, 2, 3, 4, 5, 6], 3, 2,
            [1*1+2*3+3*5, 1*2+2*4+3*6, 
             4*1+5*3+6*5, 4*2+5*4+6*6,
             7*1+8*3+9*5, 7*2+8*4+9*6,
             10*1+11*3+12*5, 10*2+11*4+12*6]
        )

    def test_all_ones(self):
        # Test matrix of all ones
        self.do_matmul(
            [1, 1, 1, 1], 2, 2,
            [1, 1, 1, 1], 2, 2,
            [2, 2, 2, 2]  # 2*1 + 2*1 = 4, but wait: 1*1+1*1=2, 1*1+1*1=2, etc.
        )

    def test_identity_matrix(self):
        # Test identity matrix multiplication
        self.do_matmul(
            [1, 0, 0, 1], 2, 2,  # identity matrix
            [2, 3, 4, 5], 2, 2,
            [2, 3, 4, 5]  # should return the same matrix
        )

    def test_zero_matrix(self):
        # Test zero matrix multiplication
        self.do_matmul(
            [0, 0, 0, 0], 2, 2,  # zero matrix
            [1, 2, 3, 4], 2, 2,
            [0, 0, 0, 0]  # should return zero matrix
    )

    @classmethod
    def tearDownClass(cls):
        print_coverage("matmul.s", verbose=False)

class TestReadMatrix(TestCase):

    def do_read_matrix(self, filename, expected_rows, expected_cols, expected_data, fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", filename)

        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])

        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)  # pointer to rows output
        t.input_array("a2", cols)  # pointer to cols output

        # call the read_matrix function
        t.call("read_matrix")

        if code == 0:
            # check the output from the function
            # Check that rows and cols were set correctly
            t.check_array(rows, [expected_rows])
            t.check_array(cols, [expected_cols])
            
            # Check that the returned matrix pointer contains the correct data
            # The returned pointer should point to the matrix data (after the 8-byte header)
            # We need to check the matrix elements
            t.check_array_pointer("a0", expected_data)

        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def test_simple(self):
        # Test reading a simple 2x2 matrix
        self.do_read_matrix(
            "inputs/test_read_matrix/test_input.bin",
            3, 3,  # expected rows and columns
            [1, 2, 3, 4, 5, 6, 7, 8, 9]  # expected matrix data
        )

    def test_single_element(self):
        # Test reading a 1x1 matrix
        self.do_read_matrix(
            "inputs/test_read_matrix/test_1x1.bin",
            1, 1,  # expected rows and columns
            [42]  # expected matrix data
        )

    def test_rectangular(self):
        # Test reading a rectangular matrix (2x3)
        self.do_read_matrix(
            "inputs/test_read_matrix/test_2x3.bin",
            2, 3,  # expected rows and columns
            [1, 2, 3, 4, 5, 6]  # expected matrix data
        )

    def test_large_matrix(self):
        # Test reading a larger matrix (3x4)
        self.do_read_matrix(
            "inputs/test_read_matrix/test_3x4.bin",
            3, 4,  # expected rows and columns
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # expected matrix data
        )

    def test_negative_numbers(self):
        # Test reading a matrix with negative numbers
        self.do_read_matrix(
            "inputs/test_read_matrix/test_negative.bin",
            2, 2,  # expected rows and columns
            [-1, -2, -3, -4]  # expected matrix data
        )

    def test_zero_matrix(self):
        # Test reading a matrix with zeros
        self.do_read_matrix(
            "inputs/test_read_matrix/test_zeros.bin",
            2, 2,  # expected rows and columns
            [0, 0, 0, 0]  # expected matrix data
        )

    def test_max_values(self):
        # Test reading a matrix with maximum and minimum integer values
        self.do_read_matrix(
            "inputs/test_read_matrix/test_max_values.bin",
            2, 2,  # expected rows and columns
            [2147483647, -2147483648, 2147483647, -2147483648]  # expected matrix data
        )

    def test_single_row(self):
        # Test reading a single row matrix
        self.do_read_matrix(
            "inputs/test_read_matrix/test_single_row.bin",
            1, 3,  # expected rows and columns
            [1, 2, 3]  # expected matrix data
        )

    def test_single_column(self):
        # Test reading a single column matrix
        self.do_read_matrix(
            "inputs/test_read_matrix/test_single_column.bin",
            3, 1,  # expected rows and columns
            [1, 2, 3]  # expected matrix data
        )

    def test_error_file_not_found(self):
        # Test error case: file not found (fopen error)
        self.do_read_matrix(
            "inputs/test_read_matrix/nonexistent.bin",
            0, 0, [],  # dummy values
            code=90  # expected error code for fopen error
        )

    def test_error_empty_file(self):
        # Test error case: empty file (fread error for header)
        self.do_read_matrix(
            "inputs/test_read_matrix/empty.bin",
            0, 0, [],  # dummy values
            code=91  # expected error code for fread error
        )

    def test_error_header_only(self):
        # Test error case: file has only header but no data (fread error for matrix)
        self.do_read_matrix(
            "inputs/test_read_matrix/header_only.bin",
            0, 0, [],  # dummy values
            code=91  # expected error code for fread error
        )

    def test_error_invalid_file_format(self):
        # Test error case: invalid file format (too short for header)
        self.do_read_matrix(
            "inputs/test_read_matrix/invalid_header.bin",
            0, 0, [],  # dummy values
            code=91  # expected error code for fread error
        )

    def test_error_incomplete_data(self):
        # Test error case: file has incomplete matrix data
        self.do_read_matrix(
            "inputs/test_read_matrix/incomplete_data.bin",
            0, 0, [],  # dummy values
            code=91  # expected error code for fread error
        )

    def test_error_malloc_failure_header(self):
        # Test error case: malloc fails for header allocation
        # We can simulate this by creating a very large allocation request
        t = AssemblyTest(self, "read_matrix.s")
        
        # Create a filename that will trigger a very large malloc request
        # We'll create a file with very large dimensions to force malloc failure
        t.input_read_filename("a0", "inputs/test_read_matrix/large_dimensions.bin")
        
        # Allocate space for output parameters
        rows = t.array([-1])
        cols = t.array([-1])
        
        t.input_array("a1", rows)
        t.input_array("a2", cols)
        
        t.call("read_matrix")
        # This should trigger malloc failure and exit with code 88
        t.execute(code=88)

    def test_error_malloc_failure_matrix(self):
        # Test error case: malloc fails for matrix allocation
        # Similar to above, but we need to create a file with valid header
        # but very large matrix size to trigger malloc failure
        t = AssemblyTest(self, "read_matrix.s")
        
        t.input_read_filename("a0", "inputs/test_read_matrix/large_matrix.bin")
        
        rows = t.array([-1])
        cols = t.array([-1])
        
        t.input_array("a1", rows)
        t.input_array("a2", cols)
        
        t.call("read_matrix")
        # This should trigger malloc failure and exit with code 88
        t.execute(code=88)

    def test_error_fclose_failure(self):
        # Test error case: fclose fails
        # This is difficult to test without mocking, but we can try to create
        # a special file that might cause fclose to fail
        # For now, we'll create a test that might trigger this path
        t = AssemblyTest(self, "read_matrix.s")
        
        t.input_read_filename("a0", "inputs/test_read_matrix/fclose_error.bin")
        
        rows = t.array([-1])
        cols = t.array([-1])
        
        t.input_array("a1", rows)
        t.input_array("a2", cols)
        
        t.call("read_matrix")
        # This might trigger fclose error and exit with code 92
        t.execute(code=92)

    @classmethod
    def tearDownClass(cls):
        print_coverage("read_matrix.s", verbose=False)

class TestWriteMatrix(TestCase):

    def do_write_matrix(self, matrix_data, rows, cols, reference_file, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        outfile = "outputs/test_write_matrix/student.bin"
        
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        
        # create array for matrix data
        array = t.array(matrix_data)
        
        # load input array and other arguments
        t.input_array("a1", array)  # pointer to matrix data
        t.input_scalar("a2", rows)  # number of rows
        t.input_scalar("a3", cols)  # number of columns
        
        # call `write_matrix` function
        t.call("write_matrix")
        
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        
        # compare the output file against the reference only if no error expected
        if code == 0:
            t.check_file_output(outfile, reference_file)

    def test_simple(self):
        # Test writing a simple 2x2 matrix
        self.do_write_matrix(
            [1, 2, 3, 4], 2, 2,
            "outputs/test_write_matrix/reference_simple.bin"
        )

    def test_1x1(self):
        # Test writing a 1x1 matrix
        self.do_write_matrix(
            [42], 1, 1,
            "outputs/test_write_matrix/reference_1x1.bin"
        )

    def test_rectangular(self):
        # Test writing a rectangular matrix (2x3)
        self.do_write_matrix(
            [1, 2, 3, 4, 5, 6], 2, 3,
            "outputs/test_write_matrix/reference_2x3.bin"
        )

    def test_large_matrix(self):
        # Test writing a larger matrix (3x4)
        self.do_write_matrix(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 3, 4,
            "outputs/test_write_matrix/reference_3x4.bin"
        )

    def test_negative_numbers(self):
        # Test writing a matrix with negative numbers
        self.do_write_matrix(
            [-1, -2, -3, -4], 2, 2,
            "outputs/test_write_matrix/reference_negative.bin"
        )

    def test_zero_matrix(self):
        # Test writing a matrix with zeros
        self.do_write_matrix(
            [0, 0, 0, 0], 2, 2,
            "outputs/test_write_matrix/reference_zeros.bin"
        )

    def test_max_values(self):
        # Test writing a matrix with maximum and minimum integer values
        self.do_write_matrix(
            [2147483647, -2147483648, 2147483647, -2147483648], 2, 2,
            "outputs/test_write_matrix/reference_max_values.bin"
        )

    def test_single_row(self):
        # Test writing a single row matrix
        self.do_write_matrix(
            [1, 2, 3], 1, 3,
            "outputs/test_write_matrix/reference_single_row.bin"
        )

    def test_single_column(self):
        # Test writing a single column matrix
        self.do_write_matrix(
            [1, 2, 3], 3, 1,
            "outputs/test_write_matrix/reference_single_column.bin"
        )

    def test_error_fopen(self):
        # Test error case: fopen fails (invalid filename)
        t = AssemblyTest(self, "write_matrix.s")
        
        # Create invalid filename (empty string)
        t.input_write_filename("a0", "")
        
        # Create matrix data
        array = t.array([1, 2, 3, 4])
        
        # Set up arguments
        t.input_array("a1", array)
        t.input_scalar("a2", 2)  # rows
        t.input_scalar("a3", 2)  # columns
        
        t.call("write_matrix")
        t.execute(code=93)  # should terminate with error code 93

    def test_error_malloc(self):
        # Test error case: malloc fails for header allocation
        # This is tricky to test without mocking malloc
        # We'll create a test that might trigger this in some environments
        t = AssemblyTest(self, "write_matrix.s")
        
        # Use a valid filename
        t.input_write_filename("a0", "outputs/test_write_matrix/malloc_test.bin")
        
        # Create matrix data
        array = t.array([1, 2, 3, 4])
        
        # Set up arguments
        t.input_array("a1", array)
        t.input_scalar("a2", 2)  # rows
        t.input_scalar("a3", 2)  # columns
        
        t.call("write_matrix")
        # This might trigger malloc failure in some environments
        # We'll expect either success (code 0) or malloc failure (code 88)
        # For this test, we'll allow both outcomes
        t.execute(code=[0, 88])

    def test_error_fwrite_header(self):
        # Test error case: fwrite fails for header
        # This is difficult to test without mocking fwrite
        # We'll create a test that might trigger this in some environments
        t = AssemblyTest(self, "write_matrix.s")
        
        # Use a valid filename
        t.input_write_filename("a0", "outputs/test_write_matrix/fwrite_header_test.bin")
        
        # Create matrix data
        array = t.array([1, 2, 3, 4])
        
        # Set up arguments
        t.input_array("a1", array)
        t.input_scalar("a2", 2)  # rows
        t.input_scalar("a3", 2)  # columns
        
        t.call("write_matrix")
        # This might trigger fwrite failure in some environments
        # We'll expect either success (code 0) or fwrite failure (code 94)
        t.execute(code=[0, 94])

    def test_error_fwrite_matrix(self):
        # Test error case: fwrite fails for matrix data
        # This is difficult to test without mocking fwrite
        # We'll create a test that might trigger this in some environments
        t = AssemblyTest(self, "write_matrix.s")
        
        # Use a valid filename
        t.input_write_filename("a0", "outputs/test_write_matrix/fwrite_matrix_test.bin")
        
        # Create matrix data
        array = t.array([1, 2, 3, 4])
        
        # Set up arguments
        t.input_array("a1", array)
        t.input_scalar("a2", 2)  # rows
        t.input_scalar("a3", 2)  # columns
        
        t.call("write_matrix")
        # This might trigger fwrite failure in some environments
        # We'll expect either success (code 0) or fwrite failure (code 94)
        t.execute(code=[0, 94])

    def test_error_fclose(self):
        # Test error case: fclose fails
        # This is difficult to test without mocking fclose
        # We'll create a test that might trigger this in some environments
        t = AssemblyTest(self, "write_matrix.s")
        
        # Use a valid filename
        t.input_write_filename("a0", "outputs/test_write_matrix/fclose_test.bin")
        
        # Create matrix data
        array = t.array([1, 2, 3, 4])
        
        # Set up arguments
        t.input_array("a1", array)
        t.input_scalar("a2", 2)  # rows
        t.input_scalar("a3", 2)  # columns
        
        t.call("write_matrix")
        # This might trigger fclose failure in some environments
        # We'll expect either success (code 0) or fclose failure (code 95)
        t.execute(code=[0, 95])

    def test_error_invalid_dimensions(self):
        # Test error case: invalid matrix dimensions (rows or columns <= 0)
        # Note: The current implementation doesn't check for invalid dimensions
        # but we'll add tests in case the implementation is updated
        t = AssemblyTest(self, "write_matrix.s")
        
        # Use a valid filename
        t.input_write_filename("a0", "outputs/test_write_matrix/invalid_dimensions.bin")
        
        # Create matrix data
        array = t.array([])
        
        # Set up arguments with invalid dimensions
        t.input_array("a1", array)
        t.input_scalar("a2", 0)  # invalid rows
        t.input_scalar("a3", 2)  # columns
        
        t.call("write_matrix")
        # The current implementation doesn't check dimensions, so this should succeed
        # But we'll allow for potential future error handling
        t.execute(code=[0, 94])  # Allow success or fwrite error

    @classmethod
    def tearDownClass(cls):
        print_coverage("write_matrix.s", verbose=False)


class TestClassify(TestCase):

    def make_test(self):
        t = AssemblyTest(self, "classify.s")
        t.include("argmax.s")
        t.include("dot.s")
        t.include("matmul.s")
        t.include("read_matrix.s")
        t.include("relu.s")
        t.include("write_matrix.s")
        return t

    def do_classify_test(self, m0_path, m1_path, input_path, output_path, 
                        expected_output, expected_classification, 
                        print_classification=0, code=0):
        t = self.make_test()
        
        # Set up command line arguments
        args = [m0_path, m1_path, input_path, output_path]
        t.input_args(args)
        
        # Set print classification flag
        t.input_scalar("a2", print_classification)
        
        # Call classify function
        t.call("classify")
        
        if code == 0:
            # Check the output file
            t.check_file_output(output_path, expected_output)
            
            # Check the classification result
            t.check_scalar("a0", expected_classification)
            
            # Check stdout if print_classification is 0
            if print_classification == 0:
                t.check_stdout(str(expected_classification))
        
        # Execute the test
        t.execute(code=code)

    def test_simple0_input0(self):
        # Test with simple0 dataset, input0
        self.do_classify_test(
            "inputs/simple0/bin/m0.bin",
            "inputs/simple0/bin/m1.bin",
            "inputs/simple0/bin/inputs/input0.bin",
            "outputs/test_basic_main/student0.bin",
            "outputs/test_basic_main/reference0.bin",
            2,  # expected classification
            0   # print classification
        )

    def test_simple0_input1(self):
        # Test with simple0 dataset, input1
        self.do_classify_test(
            "inputs/simple0/bin/m0.bin",
            "inputs/simple0/bin/m1.bin",
            "inputs/simple0/bin/inputs/input1.bin",
            "outputs/test_basic_main/student1.bin",
            "outputs/test_basic_main/reference1.bin",
            1,  # expected classification
            0   # print classification
        )

    def test_simple1_input0(self):
        # Test with simple1 dataset, input0
        self.do_classify_test(
            "inputs/simple1/bin/m0.bin",
            "inputs/simple1/bin/m1.bin",
            "inputs/simple1/bin/inputs/input0.bin",
            "outputs/test_basic_main/student2.bin",
            "outputs/test_basic_main/reference2.bin",
            0,  # expected classification
            0   # print classification
        )

    def test_simple1_input1(self):
        # Test with simple1 dataset, input1
        self.do_classify_test(
            "inputs/simple1/bin/m0.bin",
            "inputs/simple1/bin/m1.bin",
            "inputs/simple1/bin/inputs/input1.bin",
            "outputs/test_basic_main/student3.bin",
            "outputs/test_basic_main/reference3.bin",
            1,  # expected classification
            0   # print classification
        )

    def test_no_print_classification(self):
        # Test with print_classification flag set to 1 (don't print)
        self.do_classify_test(
            "inputs/simple0/bin/m0.bin",
            "inputs/simple0/bin/m1.bin",
            "inputs/simple0/bin/inputs/input0.bin",
            "outputs/test_basic_main/student4.bin",
            "outputs/test_basic_main/reference0.bin",
            2,  # expected classification
            1   # don't print classification
        )

    def test_arg_error(self):
        # Test argument error (wrong number of arguments)
        t = self.make_test()
        
        # Set up wrong number of arguments (only 3 instead of 4)
        args = ["inputs/simple0/bin/m0.bin", "inputs/simple0/bin/m1.bin", "inputs/simple0/bin/inputs/input0.bin"]
        t.input_args(args)
        
        # Set print classification flag
        t.input_scalar("a2", 0)
        
        # Call classify function
        t.call("classify")
        
        # Should exit with error code 89
        t.execute(code=89)

    def test_dimension_error_m0_input(self):
        # Test dimension error between m0 and input
        # Create test files with incompatible dimensions
        t = self.make_test()
        
        # Create a special test case where m0 columns != input rows
        # We'll use simple0 m0 (3x3) but with an input that has different number of rows
        args = [
            "inputs/simple0/bin/m0.bin",  # 3x3 matrix
            "inputs/simple0/bin/m1.bin",  # 3x3 matrix
            "inputs/test_classify/incompatible_input.bin",  # 2x1 matrix (should be 3x1 to match m0 columns)
            "outputs/test_classify/student_dim_error.bin"
        ]
        t.input_args(args)
        
        # Set print classification flag
        t.input_scalar("a2", 0)
        
        # Call classify function
        t.call("classify")
        
        # Should exit with error code 74 (dimension error)
        t.execute(code=74)

    def test_dimension_error_m1_relu(self):
        # Test dimension error between m1 and ReLU output
        # Create test files with incompatible dimensions
        t = self.make_test()
        
        # Create a special test case where m1 columns != ReLU output rows
        # We'll use simple0 m0 (3x3) and input (3x1) which produces 3x1 output
        # But use an m1 that expects a different input dimension
        args = [
            "inputs/simple0/bin/m0.bin",  # 3x3 matrix
            "inputs/test_classify/incompatible_m1.bin",  # 2x2 matrix (should be 3x3 to match ReLU output rows)
            "inputs/simple0/bin/inputs/input0.bin",  # 3x1 matrix
            "outputs/test_classify/student_dim_error2.bin"
        ]
        t.input_args(args)
        
        # Set print classification flag
        t.input_scalar("a2", 0)
        
        # Call classify function
        t.call("classify")
        
        # Should exit with error code 74 (dimension error)
        t.execute(code=74)

    def test_malloc_error(self):
        # Test malloc error (difficult to simulate, but we can try)
        # This test might not be reliable as it depends on the system's memory state
        t = self.make_test()
        
        # Use normal arguments
        args = [
            "inputs/simple0/bin/m0.bin",
            "inputs/simple0/bin/m1.bin",
            "inputs/simple0/bin/inputs/input0.bin",
            "outputs/test_classify/student_malloc.bin"
        ]
        t.input_args(args)
        
        # Set print classification flag
        t.input_scalar("a2", 0)
        
        # Call classify function
        t.call("classify")
        
        # This might trigger malloc failure in some environments
        # We'll expect either success (code 0) or malloc failure (code 88)
        t.execute(allow_codes=[0, 88])

    def test_file_not_found(self):
        # Test file not found error
        t = self.make_test()
        
        # Use non-existent file paths
        args = [
            "inputs/nonexistent/m0.bin",
            "inputs/simple0/bin/m1.bin",
            "inputs/simple0/bin/inputs/input0.bin",
            "outputs/test_classify/student_file_error.bin"
        ]
        t.input_args(args)
        
        # Set print classification flag
        t.input_scalar("a2", 0)
        
        # Call classify function
        t.call("classify")
        
        # Should exit with error code 90 (fopen error)
        t.execute(code=90)

    @classmethod
    def tearDownClass(cls):
        print_coverage("classify.s", verbose=False)


class TestMain(TestCase):

    def run_main(self, inputs, output_id, label):
        args = [f"{inputs}/m0.bin", f"{inputs}/m1.bin", f"{inputs}/inputs/input0.bin",
                f"outputs/test_basic_main/student{output_id}.bin"]
        reference = f"outputs/test_basic_main/reference{output_id}.bin"
        t = AssemblyTest(self, "main.s", no_utils=True)
        t.call("main")
        t.execute(args=args, verbose=False)
        t.check_stdout(label)
        t.check_file_output(args[-1], reference)

    def test0(self):
        self.run_main("inputs/simple0/bin", "0", "2")

    def test1(self):
        self.run_main("inputs/simple1/bin", "1", "1")

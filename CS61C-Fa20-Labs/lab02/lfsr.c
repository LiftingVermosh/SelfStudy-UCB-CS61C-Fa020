#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "lfsr.h"

void lfsr_calculate(uint16_t *reg) {
    /* YOUR CODE HERE */
    // Calculate the new bit using the polynomial x^16 + x^15 + x^13 + x^4 + 1
    // [Remark]: Must be Primitive Polynomial
    uint16_t new_bit = ((*reg >> 12) ^ (*reg >> 3) ^ (*reg >> 1) ^ (*reg >> 0)) + 1;
    // Shift the register to the right and insert the new bit at the leftmost position
    *reg = (*reg >> 1) | (new_bit << 15);
    return;
}


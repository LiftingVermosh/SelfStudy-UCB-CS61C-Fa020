#include <stdio.h>
#include "bit_ops.h"

// Return the nth bit of x.
// Assume 0 <= n <= 31
unsigned get_bit(unsigned x,
                 unsigned n) {
    // YOUR CODE HERE
    // To get the nth bit, we right shift x by n and then mask with 1
    return (x >> n) & 1;
}
// Set the nth bit of the value of x to v.
// Assume 0 <= n <= 31, and v is 0 or 1
void set_bit(unsigned * x,
             unsigned n,
             unsigned v) {
    // YOUR CODE HERE
    if(v){
        // If v is 1, we set the nth bit to 1
        *x |= (1 << n);
    } else {
        // If v is 0, we clear the nth bit
        *x &= ~(1 << n);
    }
    return;
}
// Flip the nth bit of the value of x.
// Assume 0 <= n <= 31
void flip_bit(unsigned * x,
              unsigned n) {
    // YOUR CODE HERE
    // To flip the nth bit, we left shift 1 by n and then use bitwise XOR with x
    *x ^= (1 << n);
    return; 
}


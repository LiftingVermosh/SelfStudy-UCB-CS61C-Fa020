#include <stdio.h>

int main(int argc, char *argv[]) {
    int i;
    int count = 0;
    int *p = &count;

    for (i = 0; i < 10; i++) {
        (*p)++; // Do you understand this line of code and all the other permutations of the operators? ;)
        /*
        The line (*p)++; combines pointer dereferencing and the increment operator:
          - p is a pointer variable
          - *p dereferences the pointer to access the value it points to
          - (*p)++ performs a post-increment on the dereferenced value
          - The parentheses are necessary because *p++ would have a different meaning.  
        (*p)++; 这行代码包含指针和操作符的组合。让我们分解它的含义：
          - p 是一个指针变量
          - *p 解引用这个指针，获取它指向的值
          - (*p)++ 对解引用的值进行后置递增操作
          - 括号是必须的，因为 *p++ 会有不同的含义。
        */
    }

    printf("Thanks for waddling through this program. Have a nice day.");
    return 0;
}
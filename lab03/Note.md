# Lab 03

## cc_test.c

程序的大体架构如下：

```c

main
├─ 初始化寄存器
├─ 调用 simple_fn() → 检查返回值
├─ 调用 naive_pow(2,7) → 检查返回值
├─ 调用 inc_arr(array,5)
│   ├─ 遍历数组
│   └─ 对每个元素调用 helper_fn()
│       └─ 递增元素值
├─ 调用 check_arr() → 验证数组
└─ 检查寄存器 → 输出结果

.globl:声明了可链接的函数/全局变量，包括
  simp_fn(), naive_pow(), inc_arr()

.data:存放已初始化的全局/静态变量
  success/failure_message:成功/失败信息的字符串
  array/exp_inc_array_result:整型数组

.text:程序段
  main:
    s0 = 2623 -> s1 = 2910 -> s11 = 134 -> call simple_fn(), ra = pc + offset(simple_fn) 
    -> t0 = 1 -> if(a0 != t0) goto failure -> a0 = 2 -> a1 = 7 
    -> call naive_pow, ra = pc + offset(naive_pow) 
    -> if(a0 != t0) goto failure  -> load address a0(array) 
    -> a1 = 5 -> call inc_arr(), ra = pc + offset(inc_arr) 
    -> call check_arr(), ra = pc + offset(check_arr) 
    -> t0 = 2623 -> t1 = 2910 -> t2 = 134
    -> if(s0 != t0) goto failure
    -> if(s1 != t1) goto failure
    -> if(s11 != t2) goto failure
    -> a0 = 4 -> load address a1(success_message)
    -> ecall (Environment Call:Print String) -> a0 = 10
    -> ecall (Environment Call:Exit)
  
  simple_fn:
    a0 = t0 -> a0 = 1 -> jump register ra (equals ret)

  naive_pow:
    s0 = 1 -> (no ret, into label 'naive_pow_loop') 
    -> if(a1 == 0) goto naivee_pow_end -> s0 *= a0 
    -> a1 -= 1 -> (no ret, into label 'naive_pow_end')
    -> a0 = s0 -> jump register ra

  inc_arr:
    sp -= 4 -> save word ra(sp + 0) -> s0 = a0 -> s1 = a1 
    -> t0 = 0 -> (no ret, into label 'inc_arr_loop') -> if (t0 == s1) goto inc_arr_end 
    -> Shift Left Logical Immediate t1 = t0 <<< 2 -> a0 = s0 + t1
    -> call helper_fn, ra = pc + offset(helper_fn) -> t0 += 1
    -> jump inc_arr_loop

  inc_arr_end：
    load word ra(sp + 0) -> sp += 4 -> jump register ra

  helper_fn:
    load word t1(a0 + 0) -> s0 = t1 + 1 -> save word s0(a0 + 0) 
    -> jump register ra

  check_arr:
    load address t0(exp_inc_array_result) -> load address t1(array)
    -> t2 = t1 + 20 -> (no ret, into label 'check_arr_loop') 
    -> if(t1 == t2) goto check_arr_end -> load word t3(t0 + 0)
    -> load word t4(t1 + 0) -> if(t3 != t4) goto failure -> t0 += 4
    -> t1 += 4 -> jump check_arr_loop

  check_arr_end:
    jump register ra

  failure:
    a0 = 4 -> load address a1(failure_message) -> ecall(Environmnet Call:Print String) -> a0 =10 -> ecall(Environment Call:Exit)

.globl simple_fn, naive_pow, inc_arr  # 声明为全局函数，可被其他文件链接

.data
    failure_message: .asciiz "Test failed for some reason.\n"      // 失败提示字符串
    success_message: .asciiz "Sanity checks passed!...\n"          // 成功提示字符串
    array: .word 1, 2, 3, 4, 5                                    // 初始数组
    exp_inc_array_result: .word 2, 3, 4, 5, 6                     // 预期递增后的数组

// Disassembly
main:
    // 初始化测试寄存器（检查调用约定是否被破坏）
    s0 = 2623; s1 = 2910; ...; s11 = 134;

    // 测试函数1：simple_fn() 应返回1
    a0 = simple_fn();
    if (a0 != 1) goto failure;

    // 测试函数2：naive_pow(2, 7) 应返回128
    a0 = 2; a1 = 7;
    a0 = naive_pow(a0, a1);
    if (a0 != 128) goto failure;

    // 测试函数3：inc_arr(array, 5) 递增数组
    a0 = &array; a1 = 5;
    inc_arr(a0, a1);
    check_arr();  // 验证数组是否变为[2,3,4,5,6]

    // 检查寄存器是否被意外修改（调用约定保护）
    if (s0 != 2623 || s1 != 2910 || s11 != 134) goto failure;

    // 成功输出并退出
    print_string(success_message);
    exit(0);

    int simple_fn() {
      a0 = 1;  // 直接返回1（注：原代码有冗余操作 `mv a0, t0` 需删除）
      return;
    }

    uint32_t naive_pow(uint32_t a0, uint32_t a1) {
      // 问题：未保存调用者保存的s0（违反调用约定）
      s0 = 1;              // 临时变量
      while (a1 != 0) {
          s0 *= a0;
          a1--;
      }
      a0 = s0;             // 结果存入a0
      return;
    }

    void inc_arr(uint32_t *a0, uint32_t a1) {
      // 保存ra和s0-s1（被调用者保存寄存器）
      push(ra);
      s0 = a0;  // 数组起始地址
      s1 = a1;  // 数组长度

      for (t0 = 0; t0 < a1; t0++) {
        uint32_t *elem_addr = s0 + t0*4;  // 计算元素地址
        helper_fn(elem_addr);             // 调用辅助函数递增
        // 问题：未保存临时寄存器t0（可能被helper_fn破坏）
      }

      pop(ra);
      return;
    }

    void helper_fn(uint32_t *a0) {
      // 问题：未保存s0（被调用者保存寄存器）
      t1 = *a0;       // 读取内存
      s0 = t1 + 1;    // 递增（错误使用s0）
      *a0 = s0;       // 写回内存
      return;
    }

    void check_arr() {
      uint32_t *expected = &exp_inc_array_result;
      uint32_t *actual = &array;
      for (; actual < &array[5]; expected++, actual++) {
          if (*expected != *actual) goto failure;
      }
      return;
    }

    void failure() {
      print_string(failure_message);
      exit(1);  // 非正常退出
    }
```
# 获取操作系统类型
UNAME_S := $(shell uname -s)

# 定义系统相关变量
ifeq ($(OS),Windows_NT)
    # Windows 系统 - 但优先使用 MinGW 工具链
    EXE_SUFFIX := .exe
    # 统一使用 rm 命令（MinGW 提供）
    RM := rm -f
    # 不再需要路径转换
else
    # Linux/macOS 系统
    EXE_SUFFIX :=
    RM := rm -f
endif

# 定义编译器和链接器
CC = gcc
LD = gcc

# 编译选项
CFLAGS = -ggdb -Wall -std=c99
LDFLAGS = 

# Valgrind 配置
ifeq ($(UNAME_S), Darwin)
    MEMCHECK = valgrind --tool=memcheck --leak-check=full --track-origins=yes --dsymutil=yes
endif

ifeq ($(UNAME_S), Linux)
    MEMCHECK = valgrind --tool=memcheck --leak-check=full --track-origins=yes
endif

# 目标文件定义
BIT_OPS_OBJS = bit_ops.o test_bit_ops.o
BIT_OPS_PROG = bit_ops$(EXE_SUFFIX)

LFSR_OBJS = lfsr.o test_lfsr.o
LFSR_PROG = lfsr$(EXE_SUFFIX)

VECTOR_OBJS = vector.o vector-test.o
VECTOR_PROG = vector-test$(EXE_SUFFIX)

BINARIES = $(VECTOR_PROG) $(BIT_OPS_PROG) $(LFSR_PROG)

# 默认目标：编译并运行所有程序
all: $(BINARIES)
	@echo "Running all binaries..."
	@for prog in $(BINARIES); do \
	    echo "Running $$prog..."; \
	    ./$$prog; \
	done
	@$(MAKE) clean

# 构建规则
$(BIT_OPS_PROG): $(BIT_OPS_OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

$(LFSR_PROG): $(LFSR_OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

$(VECTOR_PROG): $(VECTOR_OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# 依赖关系
lfsr.o: lfsr.c lfsr.h
test_lfsr.o: test_lfsr.c lfsr.h

bit_ops.o: bit_ops.c bit_ops.h
test_bit_ops.o: test_bit_ops.c bit_ops.h

vector.o: vector.c vector.h
vector-test.o: vector-test.c vector.h

# 通用编译规则
%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@

# 内存检查目标
vector-memcheck: $(VECTOR_PROG)
	$(MEMCHECK) ./$(VECTOR_PROG)

# 清理目标
clean:
	@echo "Cleaning up..."
	@$(RM) $(BINARIES) core *.o *~ "#"*"#" Makefile.bak *.dSYM

# 伪目标声明
.PHONY: all clean vector-memcheck
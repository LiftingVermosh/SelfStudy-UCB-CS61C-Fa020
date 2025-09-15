# Compiler
CC = gcc

# Target
TARGET = test.exe

# Source
SOURCES = ll_cycle.c test_ll_cycle.c

# Define Target files
OBJECTS = $(SOURCES:.c=.o)

# Compile Flag
CFLAGS = -Wall -g

# Compile Target
all: $(TARGET)

# Linked Target
$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -o $@

# Compile Rule
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Run Target
run: $(TARGET)
	./$(TARGET)
	$(MAKE) clean

# Clean
clean:
	rm -f $(OBJECTS) $(TARGET)

# Custom target to compile, run, and clean
build-run-clean: all run clean
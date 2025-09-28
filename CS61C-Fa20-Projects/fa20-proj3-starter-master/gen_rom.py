# ROM 编码器，用于生成指令 ROM

import sys

# ===================== 配置部分 =====================

# ImmSel 枚举
IMM_R   = 0b000
IMM_I   = 0b001
IMM_S   = 0b010
IMM_B   = 0b011
IMM_U   = 0b100
IMM_J   = 0b101
IMM_CSR = 0b110 

# ALU 操作枚举
ALU_ADD     = 0b0000
ALU_SUB     = 0b0001
ALU_AND     = 0b0010
ALU_OR      = 0b0011
ALU_XOR     = 0b0100
ALU_SLL     = 0b0101
ALU_SRL     = 0b0110
ALU_SRA     = 0b0111
ALU_SLT     = 0b1000
ALU_SLTU    = 0b1001
ALU_COPY_B  = 0b1010
ALU_MUL     = 0b1011
ALU_MULH    = 0b1100
ALU_MULHSU  = 0b1101
ALU_MULHU   = 0b1110


# 生成全零 ROM(无操作)
rom_size = 1 << 17
rom = [0] * rom_size

# 控制信号编码函数
def encode_ctrl(BranchType, RegWEn, ImmSel, BrUn, ASel, BSel,
                ALUSel, MemRW, WBSel, CSRSel, CSRWen):
    """
    打包 19 位控制信号 (已修正以匹配 Logisim 电路)
    bit 18: CSRWen
    bit 17: CSRSel
    bit 15-16: WBSel (2位)
    bit 14: MemRW
    bit 10-13: ALUSel (4位)
    bit 9:  BSel
    bit 8:  ASel
    bit 7:  BrUn
    bit 4-6: ImmSel (3位)
    bit 3:  RegWEn
    bit 0-2: BranchType (3位)
    """
    value = (CSRWen << 18) | (CSRSel << 17) | (WBSel << 15) | (MemRW << 14) | \
            (ALUSel << 10) | (BSel << 9) | (ASel << 8) | (BrUn << 7) | \
            (ImmSel << 4) | (RegWEn << 3) | (BranchType << 0)
    return value


# 规则表(此处增加更多指令映射)
# key: (opcode, funct3, funct7)
# value: encode_ctrl(...) 返回值
instr_rules = {
    # R-type ALU
    (0x33, 0b000, 0x00): encode_ctrl(0,1,IMM_R,0,0,0,ALU_ADD,0,0b00,0,0),  # ADD
    (0x33, 0b000, 0x20): encode_ctrl(0,1,IMM_R,0,0,0,ALU_SUB,0,0b00,0,0),  # SUB
    (0x33, 0b001, 0x00): encode_ctrl(0,1,IMM_R,0,0,0,ALU_SLL,0,0b00,0,0),  # SLL
    (0x33, 0b010, 0x00): encode_ctrl(0,1,IMM_R,0,0,0,ALU_SLT,0,0b00,0,0),  # SLT
    (0x33, 0b011, 0x00): encode_ctrl(0,1,IMM_R,1,0,0,ALU_SLTU,0,0b00,0,0), # SLTU
    (0x33, 0b100, 0x00): encode_ctrl(0,1,IMM_R,0,0,0,ALU_XOR,0,0b00,0,0),  # XOR
    (0x33, 0b101, 0x00): encode_ctrl(0,1,IMM_R,0,0,0,ALU_SRL,0,0b00,0,0),  # SRL
    (0x33, 0b101, 0x20): encode_ctrl(0,1,IMM_R,0,0,0,ALU_SRA,0,0b00,0,0),  # SRA
    (0x33, 0b110, 0x00): encode_ctrl(0,1,IMM_R,0,0,0,ALU_OR,0,0b00,0,0),   # OR
    (0x33, 0b111, 0x00): encode_ctrl(0,1,IMM_R,0,0,0,ALU_AND,0,0b00,0,0),  # AND
    # RV32M Multiply instructions
    (0x33, 0b000, 0x01): encode_ctrl(0,1,IMM_R,0,0,0,ALU_MUL,0,0b00,0,0),     # MUL
    (0x33, 0b001, 0x01): encode_ctrl(0,1,IMM_R,0,0,0,ALU_MULH,0,0b00,0,0),    # MULH (signed*signed)
    (0x33, 0b010, 0x01): encode_ctrl(0,1,IMM_R,1,0,0,ALU_MULHSU,0,0b00,0,0),  # MULHSU (signed*unsigned)
    (0x33, 0b011, 0x01): encode_ctrl(0,1,IMM_R,1,0,0,ALU_MULHU,0,0b00,0,0),   # MULHU (unsigned*unsigned)


    # I-type ALU
    (0x13, 0b000, 0x00): encode_ctrl(0,1,IMM_I,0,0,1,ALU_ADD,0,0b00,0,0),  # ADDI
    (0x13, 0b010, 0x00): encode_ctrl(0,1,IMM_I,0,0,1,ALU_SLT,0,0b00,0,0),  # SLTI
    (0x13, 0b011, 0x00): encode_ctrl(0,1,IMM_I,1,0,1,ALU_SLTU,0,0b00,0,0), # SLTIU
    (0x13, 0b100, 0x00): encode_ctrl(0,1,IMM_I,0,0,1,ALU_XOR,0,0b00,0,0),  # XORI
    (0x13, 0b110, 0x00): encode_ctrl(0,1,IMM_I,0,0,1,ALU_OR,0,0b00,0,0),   # ORI
    (0x13, 0b111, 0x00): encode_ctrl(0,1,IMM_I,0,0,1,ALU_AND,0,0b00,0,0),  # ANDI
    (0x13, 0b001, 0x00): encode_ctrl(0,1,IMM_I,0,0,1,ALU_SLL,0,0b00,0,0),  # SLLI
    (0x13, 0b101, 0x00): encode_ctrl(0,1,IMM_I,0,0,1,ALU_SRL,0,0b00,0,0),  # SRLI
    (0x13, 0b101, 0x20): encode_ctrl(0,1,IMM_I,0,0,1,ALU_SRA,0,0b00,0,0),  # SRAI

    # Load
    (0x03, 0b000, 0x00): encode_ctrl(0,1,IMM_I,0,0,1,ALU_ADD,0,0b01,0,0),  # LB
    (0x03, 0b001, 0x00): encode_ctrl(0,1,IMM_I,0,0,1,ALU_ADD,0,0b01,0,0),  # LH
    (0x03, 0b010, 0x00): encode_ctrl(0,1,IMM_I,0,0,1,ALU_ADD,0,0b01,0,0),  # LW
    (0x03, 0b100, 0x00): encode_ctrl(0,1,IMM_I,0,0,1,ALU_ADD,0,0b01,0,0),  # LBU
    (0x03, 0b101, 0x00): encode_ctrl(0,1,IMM_I,0,0,1,ALU_ADD,0,0b01,0,0),  # LHU

    # Store
    (0x23, 0b000, 0x00): encode_ctrl(0,0,IMM_S,0,0,1,ALU_ADD,1,0b00,0,0),  # SB
    (0x23, 0b001, 0x00): encode_ctrl(0,0,IMM_S,0,0,1,ALU_ADD,1,0b00,0,0),  # SH
    (0x23, 0b010, 0x00): encode_ctrl(0,0,IMM_S,0,0,1,ALU_ADD,1,0b00,0,0),  # SW

    # Branch
    (0x63, 0b000, 0x00): encode_ctrl(2,0,IMM_B,0,0,0,ALU_SUB,0,0b00,0,0),  # BEQ
    (0x63, 0b001, 0x00): encode_ctrl(3,0,IMM_B,0,0,0,ALU_SUB,0,0b00,0,0),  # BNE
    (0x63, 0b100, 0x00): encode_ctrl(4,0,IMM_B,0,0,0,ALU_SLT,0,0b00,0,0),  # BLT
    (0x63, 0b101, 0x00): encode_ctrl(5,0,IMM_B,0,0,0,ALU_SLT,0,0b00,0,0),  # BGE
    (0x63, 0b110, 0x00): encode_ctrl(6,0,IMM_B,1,0,0,ALU_SLTU,0,0b00,0,0), # BLTU
    (0x63, 0b111, 0x00): encode_ctrl(7,0,IMM_B,1,0,0,ALU_SLTU,0,0b00,0,0), # BGEU

    # Jumps
    (0x6F, 0b000, 0x00): encode_ctrl(1,1,IMM_J,0,1,1,ALU_ADD,0,0b10,0,0),  # JAL
    (0x67, 0b000, 0x00): encode_ctrl(1,1,IMM_I,0,0,1,ALU_ADD,0,0b10,0,0),  # JALR

    # LUI/AUIPC
    (0x37, 0b000, 0x00): encode_ctrl(0,1,IMM_U,0,0,1,ALU_ADD,0,0b00,0,0),  # LUI
    (0x17, 0b000, 0x00): encode_ctrl(0,1,IMM_U,0,1,1,ALU_ADD,0,0b00,0,0),  # AUIPC

    # CSR/system - 新增指令
    (0x73, 0b000, 0x00): encode_ctrl(0,0,IMM_I,0,0,0,ALU_ADD,0,0b00,0,0),  # ECALL
    (0x73, 0b000, 0x01): encode_ctrl(0,0,IMM_I,0,0,0,ALU_ADD,0,0b00,0,0),  # EBREAK
    (0x73, 0b001, 0x00): encode_ctrl(0,1,IMM_CSR,0,0,0,ALU_COPY_B,0,0b11,1,1), # CSRRW
    (0x73, 0b010, 0x00): encode_ctrl(0,1,IMM_CSR,0,0,0,ALU_COPY_B,0,0b11,1,0), # CSRRS
    (0x73, 0b011, 0x00): encode_ctrl(0,1,IMM_CSR,0,0,0,ALU_COPY_B,0,0b11,1,0), # CSRRC
    (0x73, 0b101, 0x00): encode_ctrl(0,1,IMM_CSR,0,0,0,ALU_COPY_B,0,0b11,1,1), # CSRRWI
    (0x73, 0b110, 0x00): encode_ctrl(0,1,IMM_CSR,0,0,0,ALU_COPY_B,0,0b11,1,0), # CSRRSI
    (0x73, 0b111, 0x00): encode_ctrl(0,1,IMM_CSR,0,0,0,ALU_COPY_B,0,0b11,1,0), # CSRRCI
}



# ===================== 主程序 =====================

if len(sys.argv) != 3:
    print("用法: python gen_rom.py 指令输入文件.txt 输出.hex")
    print("输入文件每行为: opcode funct3 funct7 (十进制或0x十六进制)")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# 读取输入文件
with open(input_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 3:
            opcode_str = parts[0]
            funct3_str = parts[1]
            funct7_str = parts[2]
            # 转换字符串为整数
            try:
                opcode = int(opcode_str, 0)
                funct3 = int(funct3_str, 0)
                funct7 = int(funct7_str, 0)
            except ValueError:
                print(f"数值转换错误: {line}")
                continue
        else:
            print(f"格式错误: {line}")
            continue

        key = (opcode, funct3, funct7)
        if key not in instr_rules:
            print(f"警告: 找不到规则 {key}, 该指令将输出全零")
            continue

        addr = (funct7 << 10) | (funct3 << 7) | opcode
        rom[addr] = instr_rules[key]

# 写出 hex 文件(Logisim 每行一个16进制数)
with open(output_file, "w") as f:
    for val in rom:
        f.write(f"{val:05x}\n")  # 17 位 => 至多 0x1FFFF，用5位hex
print(f"已生成 {output_file} ，共 {rom_size} 行")

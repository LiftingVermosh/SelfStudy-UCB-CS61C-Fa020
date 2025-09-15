/************************************************************************
**
** NAME:        gameoflife.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Justin Yokota - Starter Code
**				YOUR NAME HERE
**
**
** DATE:        2020-08-23
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "imageloader.h"

//Determines what color the cell at the given row/col should be. This function allocates space for a new Color.
//Note that you will need to read the eight neighbors of the cell in question. The grid "wraps", so we treat the top row as adjacent to the bottom row
//and the left column as adjacent to the right column.
// 决定给定行/列的单元格应具有什么颜色。此函数为新 Color 分配空间。
// 请注意，您需要读取单元格周围的八个邻居。网格“包裹”，因此我们将顶行视为与底行邻接，左列视为与右列邻接。
Color *evaluateOneCell(Image *image, int row, int col, uint32_t rule)
{
	//YOUR CODE HERE
	const int BITS = 32;
	int rules[BITS];
	// Initialize all rules to 0 to avoid uninitialized values
	for (int i = 0; i < BITS; i++) {
		rules[i] = 0;
	}
	int loc = 0;
	while (rule > 0) {
		rules[loc++] = rule & 1;
		rule = rule >> 1;
	}
	uint32_t numNeighbors = 0;
	uint32_t height = image->rows;
	uint32_t width = image->cols;
	Color *cell = malloc(sizeof(Color));
	if (cell == NULL) {
		return NULL;
	}
	for (int i = -1; i <= 1; i++) {
		for (int j = -1; j <= 1; j++) {
			if (i == 0 && j == 0) continue;
			int neighborRow = (row + i + height) % height;
			int neighborCol = (col + j + width) % width;
			if (image->image[neighborRow][neighborCol].R == 255 && 
				image->image[neighborRow][neighborCol].G == 255 && 
				image->image[neighborRow][neighborCol].B == 255) {
				numNeighbors++;
			}
		}
	}
	if (rules[numNeighbors] == 1) {
		cell->R = 255;
		cell->G = 255;
		cell->B = 255;
	} else {
		cell->R = 0;
		cell->G = 0;
		cell->B = 0;
	}
	return cell;
}

//The main body of Life; given an image and a rule, computes one iteration of the Game of Life.
//You should be able to copy most of this from steganography.c
// Life 的主体；给定图像和规则，计算一轮游戏的下一个迭代。
// 你应该能够从 steganography.c 复制大部分代码。
Image *life(Image *image, uint32_t rule)
{
	//YOUR CODE HERE
	uint32_t rows = image->rows;
	uint32_t cols = image->cols;
	Image *new_image = malloc(sizeof(Image));
	if (new_image == NULL) {
		return NULL;
	}
	new_image->rows = rows;
	new_image->cols = cols;
	new_image->image = malloc(rows * sizeof(Color*));
	if (new_image->image == NULL) {
		free(new_image);
		return NULL;
	}
	// 循环遍历确定当前位置的下一个状态
	for (int i = 0; i < rows; ++i) {
		new_image->image[i] = malloc(cols * sizeof(Color));
		if (new_image->image[i] == NULL) {
			for (int j = 0; j < i; j++) {
				free(new_image->image[j]);
			}
			free(new_image->image);
			free(new_image);
			return NULL;
		}
		for (int j = 0; j < cols; ++j) {
			Color *new_Color = evaluateOneCell(image, i, j, rule);
			if (new_Color == NULL) {
				for (int k = 0; k <= i; k++) {
					free(new_image->image[k]);
				}
				free(new_image->image);
				free(new_image);
				return NULL;
			}
			new_image->image[i][j] = *new_Color;
			free(new_Color);
		}
	}
	return new_image;
}

/*
Loads a .ppm from a file, computes the next iteration of the game of life, then prints to stdout the new image.

argc stores the number of arguments.
argv stores a list of arguments. Here is the expected input:
argv[0] will store the name of the program (this happens automatically).
argv[1] should contain a filename, containing a .ppm.
argv[2] should contain a hexadecimal number (such as 0x1808). Note that this will be a string.
You may find the function strtol useful for this conversion.
If the input is not correct, a malloc fails, or any other error occurs, you should exit with code -1.
Otherwise, you should return from main with code 0.
Make sure to free all memory before returning!

You may find it useful to copy the code from steganography.c, to start.
*/
int main(int argc, char **argv)
{
	//YOUR CODE HERE
	if (argc != 3) {
		printf("Usage: ./gameoflife filename rule\n");
		printf("filename is an ASCII PPM file (type P3) with maximum value 255.\n");
		printf("rule is a hex number beginning with 0x; Life is 0x1808.\n");
		return -1;
	}
	Image *image = readData(argv[1]);
	if (image == NULL) {
		printf("Error loading image.\n");
		return -1;
	}
	uint32_t rule = strtol(argv[2], NULL, 16);
	Image *new_image = life(image, rule);
	if (new_image == NULL) {
		printf("Error computing new image.\n");
		freeImage(image);
		return -1;
	}
	writeData(new_image);
	freeImage(image);
	freeImage(new_image);
	return 0;
}

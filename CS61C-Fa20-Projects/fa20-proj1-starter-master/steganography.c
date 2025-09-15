/************************************************************************
**
** NAME:        steganography.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Dan Garcia  -  University of California at Berkeley
**              Copyright (C) Dan Garcia, 2020. All rights reserved.
**				Justin Yokota - Starter Code
**				YOUR NAME HERE
**
** DATE:        2020-08-23
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "imageloader.h"

//Determines what color the cell at the given row/col should be. This should not affect Image, and should allocate space for a new Color.
Color *evaluateOnePixel(Image *image, int row, int col)
{
	//YOUR CODE HERE
	Color base_Color = image->image[row][col];
	Color *new_Color = malloc(sizeof(Color));
	uint8_t LSB = base_Color.B & 1;   		// B Channel的最低位
	// 根据LSB的值，设置R、G、B的值
	new_Color->R = LSB * 255;
	new_Color->G = LSB * 255;
	new_Color->B = LSB * 255;
	return new_Color;
}

//Given an image, creates a new image extracting the LSB of the B channel.
Image *steganography(Image *image)
{
	//YOUR CODE HERE
	uint32_t rows = image->rows;
	uint32_t cols = image->cols;
	Image *new_image = malloc(sizeof(Image));
	new_image->rows = rows;
	new_image->cols = cols;
	new_image->image = malloc(rows * sizeof(Color*));
	// 循环遍历确定当前位置的LSB值
	for(int i = 0; i < rows; ++i){
		new_image->image[i] = malloc(cols * sizeof(Color));
		for(int j = 0; j < cols; ++j){
			Color *new_Color = evaluateOnePixel(image, i, j);
			new_image->image[i][j] = *new_Color;
			free(new_Color);
		}
	}
	return new_image;
}

/*
Loads a file of ppm P3 format from a file, and prints to stdout (e.g. with printf) a new image, 
where each pixel is black if the LSB of the B channel is 0, 
and white if the LSB of the B channel is 1.

argc stores the number of arguments.
argv stores a list of arguments. Here is the expected input:
argv[0] will store the name of the program (this happens automatically).
argv[1] should contain a filename, containing a file of ppm P3 format (not necessarily with .ppm file extension).
If the input is not correct, a malloc fails, or any other error occurs, you should exit with code -1.
Otherwise, you should return from main with code 0.
Make sure to free all memory before returning!
*/
int main(int argc, char **argv)
{
	//YOUR CODE HERE
	if(argc != 2){
		printf("错误：无效的命令行参数 %s \n", argv[0]);
		return -1;
	}
	Image *image = readData(argv[1]);
	if(image == NULL){
		printf("错误：无法读取文件 %s\n", argv[1]);
		return -1;
	}
	Image *new_image = steganography(image);
	if(new_image == NULL){
		printf("错误：无法创建新图像 \n");
		return -1;
	}
	writeData(new_image);
	freeImage(new_image);
	freeImage(image);
	return 0;
}

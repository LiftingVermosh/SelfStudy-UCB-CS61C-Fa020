/************************************************************************
**
** NAME:        imageloader.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Dan Garcia  -  University of California at Berkeley
**              Copyright (C) Dan Garcia, 2020. All rights reserved.
**              Justin Yokota - Starter Code
**				YOUR NAME HERE
**
**
** DATE:        2020-08-15
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include "imageloader.h"

// 跳过可能存在的注释
void skip_comments(FILE *file){
	char c;
	// 对输入进行鉴别，如果是 '#' 则跳过注释行
	while((c = fgetc(file)) == '#'){
		while((c = fgetc(file)) != '\n' && c != EOF)
			;
	}
	// 将指针指向当前读取的最后字符
	ungetc(c, file);
}

//Opens a .ppm P3 image file, and constructs an Image object. 
//You may find the function fscanf useful.
//Make sure that you close the file with fclose before returning.
Image *readData(char *filename) 
{
	//YOUR CODE HERE
	
	// 创建一个 Image 对象
	Image *cur_image = malloc(sizeof(Image));
	if(cur_image == NULL) {
		fprintf(stderr, "无法为图像分配内存\n");
		return NULL;
	}
	
	// 打开文件
	FILE *file = fopen(filename, "r");
	if(file == NULL) {
		fprintf(stderr, "无法读取文件 %s\n", filename);
		return NULL;
	}
	
	// 魔数校验
	char magic[3];
	fscanf(file, "%s", magic);
	if(strcmp(magic, "P3") != 0) {
		fprintf(stderr, "文件 %s 不是有效的 PPM3 图像\n", filename);
		fclose(file);
		return NULL;
	}

	// 读取图像尺寸
	skip_comments(file); 	// 跳过可能存在的注释
	if(fscanf(file, "%u %u", &cur_image->rows, &cur_image->cols) != 2){
		fprintf(stderr, "无法读取图像尺寸\n");
		fclose(file);
		return NULL;
	}
	
	// 读取图像颜色最大值
	skip_comments(file); 	// 跳过可能存在的注释
	uint32_t max_val;
	fscanf(file, "%u", &max_val);
	if(max_val > 255) {
		fprintf(stderr, "图像数据值超过 255,当前值: %u\n", max_val);
		fclose(file);
		return NULL;
	}

	// 读取图像数据
	cur_image->image = malloc(cur_image->rows * sizeof(Color*));
	if(cur_image->image == NULL) {
		fprintf(stderr, "无法为图像行数据分配内存\n");
		fclose(file);
		free(cur_image);
		return NULL;
	}
	for(int i = 0; i < cur_image->rows; i++) {
		cur_image->image[i] = malloc(cur_image->cols * sizeof(Color));
		if(cur_image->image[i] == NULL) {
			fprintf(stderr, "无法为图像列数据分配内存\n");
			free(cur_image->image);
			fclose(file);
			free(cur_image);
			return NULL;
		}
		for(int j = 0; j < cur_image->cols; j++) {
			if(fscanf(file, "%hhu %hhu %hhu", &cur_image->image[i][j].R, &cur_image->image[i][j].G, &cur_image->image[i][j].B) != 3){
				fprintf(stderr, "无法读取图像数据\n");
				fclose(file);
				return NULL;
			}
		}
	}

	// 关闭文件
	fclose(file);
	// printf("成功读取图像 %s\n", filename);
	return cur_image;
}

//Given an image, prints to stdout (e.g. with printf) a .ppm P3 file with the image's data.
void writeData(Image *image)
{
	//YOUR CODE HERE
// 文件输出
	// 打开文件
	// FILE *file = fopen("output.ppm", "w");
	// if(file == NULL) {
	// 	error("无法打开文件 output.ppm");
	// 	return;
	// }
	// // 写入魔数
	// fprintf(file, "P3\n");

	// // 写入图像尺寸
	// fprintf(file, "%u %u\n", image->rows, image->cols);

	// // 写入图像颜色最大值
	// fprintf(file, "255\n");

	// // 写入图像数据
	// for(int i = 0; i < image->rows; i++) {
	// 	for(int j = 0; j < image->cols; j++) {
	// 		fprintf(file, "%u %u %u ", image->image[i][j].R, image->image[i][j].G, image->image[i][j].B);
	// 	}
	// 	fprintf(file, "\n");
	// }

	// // 关闭文件
	// fclose(file);
	// printf("成功写入图像 output.ppm\n");
	
// 标准输出
    printf("P3\n");
    printf("%u %u\n", image->rows, image->cols);
    printf("255\n");
    for (int i = 0; i < image->rows; i++) {
        for (int j = 0; j < image->cols - 1; j++) {
            printf("%3d %3d %3d   ", image->image[i][j].R, image->image[i][j].G, image->image[i][j].B);
        }
        printf("%3d %3d %3d\n", image->image[i][image->cols - 1].R, image->image[i][image->cols - 1].G, image->image[i][image->cols - 1].B);
    }
}

//Frees an image
void freeImage(Image *image)
{
	//YOUR CODE HERE
	for(int i = 0; i < image->rows; i++) {
		free(image->image[i]);
	}
	free(image->image);
	free(image);
	// printf("成功释放图像内存\n");
}
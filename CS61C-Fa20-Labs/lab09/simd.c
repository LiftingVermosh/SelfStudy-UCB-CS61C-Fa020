#include <time.h>
#include <stdio.h>
#include <x86intrin.h>
#include "simd.h"

long long int sum(int vals[NUM_ELEMS]) {
	clock_t start = clock();

	long long int sum = 0;
	for(unsigned int w = 0; w < OUTER_ITERATIONS; w++) {
		for(unsigned int i = 0; i < NUM_ELEMS; i++) {
			if(vals[i] >= 128) {
				sum += vals[i];
			}
		}
	}
	clock_t end = clock();
	printf("Time taken: %.26f s\n", (double)(end - start) / CLOCKS_PER_SEC);
	return sum;
}

long long int sum_unrolled(int vals[NUM_ELEMS]) {
	clock_t start = clock();
	long long int sum = 0;

	for(unsigned int w = 0; w < OUTER_ITERATIONS; w++) {
		for(unsigned int i = 0; i < NUM_ELEMS / 4 * 4; i += 4) {
			if(vals[i] >= 128) sum += vals[i];
			if(vals[i + 1] >= 128) sum += vals[i + 1];
			if(vals[i + 2] >= 128) sum += vals[i + 2];
			if(vals[i + 3] >= 128) sum += vals[i + 3];
		}

		//This is what we call the TAIL CASE
		//For when NUM_ELEMS isn't a multiple of 4
		//NONTRIVIAL FACT: NUM_ELEMS / 4 * 4 is the largest multiple of 4 less than NUM_ELEMS
		for(unsigned int i = NUM_ELEMS / 4 * 4; i < NUM_ELEMS; i++) {
			if (vals[i] >= 128) {
				sum += vals[i];
			}
		}
	}
	clock_t end = clock();
	printf("Time taken: %.26f s\n", (double)(end - start) / CLOCKS_PER_SEC);
	return sum;
}

long long int sum_simd(int vals[NUM_ELEMS]) {
	clock_t start = clock();
	__m128i _127 = _mm_set1_epi32(127);		// This is a vector with 127s in it... Why might you need this?
	long long int result = 0;				   // This is where you should put your final result!
	/* DO NOT DO NOT DO NOT DO NOT WRITE ANYTHING ABOVE THIS LINE. */

	for(unsigned int w = 0; w < OUTER_ITERATIONS; w++) {
		/* YOUR CODE GOES HERE */
		__m128i ans = _mm_set_epi32(0, 0, 0, 0);
		for(unsigned int i = 0; i < NUM_ELEMS / 4 * 4; i += 4) {
			// TODO: 实现向量化计算
			// 提取4个元素
			__m128i v1 = _mm_loadu_si128((__m128i*)(vals + i));
			// 并与127进行比较
			__m128i v2 = _mm_cmpgt_epi32(v1, _127);
			// 与原始值进行与操作
			__m128i v3 = _mm_and_si128(v1, v2);
			// 将结果加到ans中
			ans = _mm_add_epi32(ans, v3);
		}
		result += _mm_extract_epi32(ans, 0) + _mm_extract_epi32(ans, 1) + _mm_extract_epi32(ans, 2) + _mm_extract_epi32(ans, 3);
		/* You'll need a tail case. */
		for(unsigned int i = NUM_ELEMS / 4 * 4; i < NUM_ELEMS; i++) {
			if (vals[i] >= 128) {
				result += vals[i];
			}
		}
	}
	clock_t end = clock();
	printf("Time taken: %.26f s\n", (double)(end - start) / CLOCKS_PER_SEC);
	return result;
}

long long int sum_simd_unrolled(int vals[NUM_ELEMS]) {
	clock_t start = clock();
	__m128i _127 = _mm_set1_epi32(127);
	long long int result = 0;
	for(unsigned int w = 0; w < OUTER_ITERATIONS; w++) {
		/* COPY AND PASTE YOUR sum_simd() HERE */
		/* MODIFY IT BY UNROLLING IT */
		__m128i sum1 = _mm_set_epi32(0, 0, 0, 0);
		__m128i sum2 = _mm_set_epi32(0, 0, 0, 0);
		for(unsigned int i = 0; i < NUM_ELEMS / 4 * 4; i += 8) {
			// TODO: 修改以下代码，实现循环展开
            __m128i v1 = _mm_loadu_si128((__m128i*)(vals + i));
            // 与127进行比较
            __m128i cmp1 = _mm_cmpgt_epi32(v1, _127);
            __m128i masked1 = _mm_and_si128(v1, cmp1);
            sum1 = _mm_add_epi32(sum1, masked1);
            // 对第二组数据进行处理
            __m128i v2 = _mm_loadu_si128((__m128i*)(vals + i + 4));
            __m128i cmp2 = _mm_cmpgt_epi32(v2, _127);
            __m128i masked2 = _mm_and_si128(v2, cmp2);
            sum2 = _mm_add_epi32(sum2, masked2);
        }
        // Combine the two accumulators into one SIMD register
        __m128i total_sum = _mm_add_epi32(sum1, sum2);
        // Extract the sum from the SIMD register by storing to an array and summing
        int sum_arr[4];
        _mm_storeu_si128((__m128i*)sum_arr, total_sum);
        result += sum_arr[0] + sum_arr[1] + sum_arr[2] + sum_arr[3];
		/* You'll need 1 or maybe 2 tail cases here. */
		for(unsigned int i = NUM_ELEMS / 4 * 4; i < NUM_ELEMS; i++) {
			if (vals[i] >= 128) {
				result += vals[i];
			}
		}
	}
	clock_t end = clock();
	printf("Time taken: %.26f s\n", (double)(end - start) / CLOCKS_PER_SEC);
	return result;
}
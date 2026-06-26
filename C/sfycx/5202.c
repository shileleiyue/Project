#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    char bin[10000];
    char hex[2500]; // 十六进制长度最多是二进制长度的1/4
    int n;
    scanf("%d", &n);
    while (n--) {
        scanf("%s", bin);
        int len = strlen(bin);
        int hex_index = 0;

        // 从右向左处理二进制，每4位转换为1位十六进制
        for (int i = len - 1; i >= 0; i -= 4) {
            int value = 0;
            for (int j = 0; j < 4 && (i - j) >= 0; j++) {
                if (bin[i - j] == '1') {
                    value += (1 << j); // 二进制位权重
                }
            }
            if (value < 10) {
                hex[hex_index++] = '0' + value; // 数字字符
            } else {
                hex[hex_index++] = 'A' + (value - 10); // 字母字符
            }
        }
        hex[hex_index] = '\0';

        // 反转十六进制字符串
        for (int i = 0; i < hex_index / 2; i++) {
            char temp = hex[i];
            hex[i] = hex[hex_index - i - 1];
            hex[hex_index - i - 1] = temp;
        }

        printf("%s\n", hex);
    }
    return 0;
}
// 题目描述
// 置换加密算法是最简单的加密算法，就是将一个字母表中的字符置换成另一个字母表中的字符，这种密方法，已经存在2000多年的历史了。
// 输入
// 第1行是原文字母表，第2行是替换用的字母表。剩下的便是原文。
// 输出
// 输出的第1行是替换用的字母表，第2行是原文字母表。接下来是将替换后得到的密文字符串。
// 注意：每行最多64个字符（包括结束符）。所有的字符都在原文字母表中。
// 样例输入 复制
// abcdefghijklmnopqrstuvwxyz
// zyxwvutsrqponmlkjihgfedcba
// Shar's Birthday:
// The birthday is October 6th, but the party will be Saturday,
// October 5.  It's my 24th birthday and the first one in some 
// years for which I've been employed.  Plus, I have new clothes.
// So I have cause to celebrate.  More importantly, though, 
// we've cleaned the house!  The address is 506-D Albert Street.
// Extra enticement for CS geeks:  there are several systems in
// the house, and the party is conveniently scheduled for 3 hours
// after the second CSC programming contest ends (not to mention,
// within easy walking distance)!
// 样例输出 复制
// zyxwvutsrqponmlkjihgfedcba
// abcdefghijklmnopqrstuvwxyz
// Sszi'h Brigswzb:
// Tsv yrigswzb rh Oxglyvi 6gs, yfg gsv kzigb droo yv Szgfiwzb,
// Oxglyvi 5.  Ig'h nb 24gs yrigswzb zmw gsv urihg lmv rm hlnv 
// bvzih uli dsrxs I'ev yvvm vnkolbvw.  Pofh, I szev mvd xolgsvh.
// Sl I szev xzfhv gl xvovyizgv.  Mliv rnkligzmgob, gslfts, 
// dv'ev xovzmvw gsv slfhv!  Tsv zwwivhh rh 506-D Aoyvig Sgivvg.
// Ecgiz vmgrxvnvmg uli CS tvvph:  gsviv ziv hvevizo hbhgvnh rm
// gsv slfhv, zmw gsv kzigb rh xlmevmrvmgob hxsvwfovw uli 3 slfih
// zugvi gsv hvxlmw CSC kiltiznnrmt xlmgvhg vmwh (mlg gl nvmgrlm,
// drgsrm vzhb dzoprmt wrhgzmxv)!

#include <stdio.h>
#include <string.h>

int main() {
    char original[256], target[256];
    char map[256];
    int has[256] = {0};
    
    // 读取原文字母表和替换字母表
    if (fgets(original, sizeof(original), stdin) == NULL) return 1;
    if (fgets(target, sizeof(target), stdin) == NULL) return 1;
    
    // 去除行末的换行符
    original[strcspn(original, "\n")] = '\0';
    target[strcspn(target, "\n")] = '\0';
    
    // 构建字符映射表
    int len = strlen(original);
    for (int i = 0; i < len; i++) {
        char idx = original[i];
        map[idx] = target[i];
        has[idx] = 1;
    }
    
    // 按题目要求先输出两个字母表
    printf("%s\n", target);
    printf("%s\n", original);
    
    // 逐行处理原文并输出密文
    char line[256];
    while (fgets(line, sizeof(line), stdin) != NULL) {
        for (int i = 0; line[i] != '\0'; i++) {
            if (line[i] == '\n') {
                putchar('\n');
                break;
            }
            char c = line[i];
            if (has[c]) {
                putchar(map[c]);
            } else {
                putchar(c);
            }
        }
    }
    
    return 0;
}
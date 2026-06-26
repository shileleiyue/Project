// 题目描述
// Stan和Ollie在玩一个猜数游戏。先由Stan想出一个1到10之间的数，Ollie猜这个数可能是几。Ollie每猜一个数，Stan回答这个数比原数高、低，还是正确，对应的回答为“too high”，“ too low”，“right on”。猜数正确后，此轮游戏结束。每次游戏结束，Ollie判断是不是Stan说谎。如果是，则输出“Stan is dishonest”，否则，输出“Stan may be honest”。
// 输入
// 请在这里写输入格式。例如：输入在一行中给出2个绝对值不超过1000的整数A和B。有多组数据，输入一个整数n（1 <= n <= 10）。接下来的一行是（too high，too low，right on）中的一个。如果是right on，则这组输入结束。如果n=0，表示这是最后一组数据。
// 输出
// Stan没有说谎，则输出“Stan may be honest”，否则输出“Stan is dishonest”。
// 样例输入 复制
// 10
// too high
// 3
// too low
// 4
// too high
// 2
// right on
// 5
// too low
// 7
// too high
// 6
// right on
// 0
// 样例输出 复制
// Stan is dishonest
// Stan may be honest

#include<stdio.h>
#include<string.h>

int main(){
    int n;
    char ans[10];
    while (scanf("%d", &n) && n != 0) {
        int low = 0, high = 11;
        getchar();
        while (1) {
            fgets(ans, sizeof(ans), stdin);
            ans[strcspn(ans, "\n")] = '\0';
            if (strcmp(ans, "too low") == 0) {
                if (n > low) low = n;
            } else if (strcmp(ans, "too high") == 0) {
                if (n < high) high = n;
            } else if (strcmp(ans, "right on") == 0) {
                if (n > low && n < high)
                    printf("Stan may be honest\n");
                else
                    printf("Stan is dishonest\n");
                break;
            }
            scanf("%d", &n);
            getchar();
        }
    }
}
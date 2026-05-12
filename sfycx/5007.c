// 题目描述
// 如果一个数从左往右读和从右往左读都是一样的话，那么我们就称它是一个回文数。例如，75457就是一个回文数。
// 当然，这种性质要取决于这个数是在什么进制下。例如，17在十进制下不是一个回文数，但在二进制下（10001）则是一个回文数。
// 题目要求你来验证给定的数在2~16进制中的哪些进制下是否是回文数。
// 输入
// 输入文件包含了若干个十进制整数n，0 < n < 50000，每个整数占一行。0表示结束。
// 输出
// 如果整数i在某些进制下是回文数，则输出“Number i is palindrom in basis”，然后分别输出这些进制，其中i是给定的整数。如果在2~16进制下都不是回文数，则输出“Number i is not palindrom”。



#include<stdio.h>
#include<math.h>
int is_palindrome(int n,int base){
    int digits[20], count=0;
    while(n>0){
        digits[count++]=n%base;
        n/=base;
    }
    for(int i=0;i<count/2;i++){
        if(digits[i]!=digits[count-1-i]){
            return 0;
        }
    }
    return 1;
}
int main(){
    int n;
    while(scanf("%d",&n)!=EOF){
        if(n==0){
            break;
        }
        int found=0;
        printf("Number %d is palindrom in basis", n);
        for(int base=2;base<=16;base++){
            if(is_palindrome(n,base)){
                printf(" %d", base);
                found=1;
            }
        }
        if(!found){
            printf(" not");
        }
        printf(".\n");
    }
    return 0;
}
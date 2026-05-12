// 题目描述
// 字符串S由字母字符组成，它的“D-对字符串”为S中相隔D个位置的两个字符组成的有序对。如果S所有的“D-对字符串”都不相同，则称S是“D-唯一的”。如果S对所有可能的D值都是“D-唯一的”，则称S是一个“令人惊讶的字符串”。
// 例如，字符串ZGBG，它的“0-对字符串”为ZG、GB和BG，由于这三个字符串都不相同，因此ZGBG是“0-唯一的”。同样，它的“1-对字符串”为ZB和GG，不相同，也是“1-唯一的”。最后，它的“2-对字符串”只有一个，就是ZG，因此ZGBG也是“2-唯一的”。
// 因此，ZGBG是一个“令人惊讶的字符串”。
// 输入
// 输入文件中包含了若干个非空字符串，由大写字母字符组成，长度最长为79个字符。每个字符串占一行。输入文件的最后一行为“*”字符，代表输入结束。
// 输出
// 输入文件中包含了若干个非空字符串，由大写字母字符组成，长度最长为79个字符。每个字符串占一行。输入文件的最后一行为“*”字符，代表输入结束。
// ZGBG is surprising.
// X is surprising.
// EE is surprising.
// AAB is surprising.
// AABA is surprising.
// AABB is NOT surprising.
// BCBABCC is NOT surprising.

#include<stdio.h>
#include<string.h>
int main(){
    char str[80];
    while(scanf("%s",str)!=EOF){
        if(strcmp(str,"*")==0){
            break;
        }
        int len=strlen(str);
        int surprising=1;
        for(int d=1;d<len;d++){
            char pairs[80][3]; // 存储D-对字符串
            int pair_count=0;
            for(int i=0;i+d<len;i++){
                char pair[3];
                pair[0]=str[i];
                pair[1]=str[i+d];
                pair[2]='\0';
                // 检查是否已经存在相同的D-对字符串
                int exists=0;
                for(int j=0;j<pair_count;j++){
                    if(strcmp(pairs[j],pair)==0){
                        exists=1;
                        break;
                    }
                }
                if(exists){
                    surprising=0;
                    break;
                }else{
                    strcpy(pairs[pair_count++],pair);
                }
            }
            if(!surprising){
                break;
            }
        }
        if(surprising){
            printf("%s is surprising.\n",str);
        }else{
            printf("%s is NOT surprising.\n",str);
        }
    }
    return 0;
}
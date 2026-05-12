// 输入
// 输入包括多组测试数据。每组数据包括一行，给出2到15个两两不同且小于10000的正整数。每一行最后一个数是0，表示这一行的结束后，这个数不属于那2到15个给定的正整数。输入的最后一行只包括一个整数-1,这行表示输入数据的结束，不用进行处理。
// 输出
// 对每组输入数据，输出一行，给出有多少个数对满足其中一个数是另一个数的两倍。
#include<stdio.h>
#include<math.h>
int main(){
    int nums[15];
    while(scanf("%d",&nums[0])!=EOF){
        if(nums[0]==-1){
            break;
        }
        int count=0;
        int i=1;
        while(scanf("%d",&nums[i])!=EOF){
            if(nums[i]==0){
                break;
            }
            i++;
        }
        for(int j=0;j<i;j++){
            for(int k=j+1;k<i;k++){
                if(nums[j]==2*nums[k]||nums[k]==2*nums[j]){
                    count++;
                }
            }
        }
        printf("%d\n",count);
    }
    return 0;
}
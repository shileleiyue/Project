#include<stdio.h>
int main(){
    int a,sum,t,temp[5],   i;
    while (scanf("%d",&a)!=EOF)
    {
        sum=0;
        for(i=0;i<5;i++)
            scanf("%d",temp[i]);
        for(i=0;i<5;i++)
            if(temp[i]<a)
                sum+=temp[i];
        printf("%d\n",sum);
    }
    return 0;
}
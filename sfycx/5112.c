#include<stdio.h>
#include<string.h>
#include<math.h>

int sr(long x,int r){
    char num[20];
    sprintf(num,"%ld",x);   
    int len=strlen(num);
        int sum=0;
        for(int i=0;i<len;i++)
        {
            sum=sum+(num[i]-'0')*pow(r,len-i-1);
        }
    return sum;
}
int maxchar(long x,long y,long z){
    char num[20];
    sprintf(num,"%ld",x);   
    int len=strlen(num);
    int max=0;
    for(int i=0;i<len;i++)
        {
            if(num[i]-'0'>max){
                max=num[i]-'0';
            }
        }
    sprintf(num,"%ld",y);   
    len=strlen(num);
    for(int i=0;i<len;i++)
        {
            if(num[i]-'0'>max){
                max=num[i]-'0';
            }
        }
    sprintf(num,"%ld",z);   
    len=strlen(num);
    for(int i=0;i<len;i++)
        {
            if(num[i]-'0'>max){
                max=num[i]-'0';
            }
        }
    return max;
}

int main()
{
    int t;
    scanf("%d",&t);
    for(int i=0;i<t;i++)
    {
        int found=0;
        long r,p,q;
        scanf("%ld %ld %ld",&p,&q,&r);
        for (int i = maxchar(p,q,r)+1; i <= 64 ; i++)
        {
            if(sr(r,i)==sr(q,i)*sr(p,i)){
                printf("%d\n",i);
                found++;
                break;
            }
        }
        if(found==0){
            printf("0\n");
        }
    }
    return 0;
}
#include<stdio.h>
#include<string.h>
#include<ctype.h>
#include<math.h>
int main()
{
    char num[32];

    while(scanf("%s",num)!=EOF)
    {
        int len=strlen(num);
        int sum=0;
        for(int i=0;i<len;i++)
        {
            sum=sum+(num[i]-'0')*pow(8,len-i-1);
        }
        printf("%d\n",sum);
    }
    return 0;
}
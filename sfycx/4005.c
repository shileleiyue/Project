#include<stdio.h>
#include<string.h>
int main()
{
    int n,len,sum;
    char m[1001];
    scanf("%d",&n);
    for (int i = 0; i < n; i++)
    {
        scanf("%s",m);
        len = strlen(m);
        sum=0;
        for (int j = 0; j < len; j++)
        {
            if(m[j]==m[j+1])
            {
                sum++;
            }
            else
            {
                printf("%d%c",sum+1,m[j]);
                sum=0;
            }
            if(j==len-1)
            {
                printf("\n");
            }
        }
        
    }
    
    return 0;
}
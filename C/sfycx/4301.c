#include<stdio.h>
#include<string.h>

int main()
{
    int n,len;
    char line[110];
    scanf("%d",&n);
    getchar();
    for(int i=0;i<n;i++)
    {
        fgets(line, sizeof(line), stdin);
        line[strcspn(line, "\n")] = '\0';
        len = strlen(line);
        for(int j=0;j<len;j++)
        {
            if(j==0)
            {
                printf("%c",line[j]-'a'+'A');
            }
            if((line[j]==' '&&((line[j+1] >= 'a' && line[j+1] <= 'z') || (line[j+1] >= 'A' && line[j+1] <= 'Z'))))
            {
                printf("%c",line[j+1]-'a'+'A');
            }
        }
        printf("\n");
    }
    return 0;
}
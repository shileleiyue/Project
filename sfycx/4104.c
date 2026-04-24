#include<stdio.h>
#include<string.h>
int main(){
    int len,t;
    char str[21];
    while (scanf("%s",str)!=EOF)
    {
        t=0;
        len = strlen(str);
        for (int i = 0; i < len; i++)
        {
            switch (str[i])
            {
                case 'B':
                case 'F':
                case 'P':
                case 'V':
                    if (t!=1)
                    {
                        printf("1");
                        t=1;
                    }break;
                case 'C':
                case 'G':
                case 'J':
                case 'K':
                case 'Q':
                case 'S':
                case 'X':
                case 'Z':
                    if (t!=2)
                    {
                        printf("2");
                        t=2;
                            
                    }
                    break;
                case 'D':
                case 'T':
                    if (t!=3)
                    {
                        printf("3");
                        t=3;
                    }break;
                case 'L':
                    if (t!=4)
                    {
                        printf("4");
                        t=4;
                    }break;
                case 'M':
                case 'N':
                    if (t!=5)
                    {
                        printf("5");
                        t=5;
                    }break;
                case 'R':
                    if (t!=6)
                    {
                        printf("6");
                        t=6;
                    }break;
                case 'A':
                case 'E':
                case 'I':
                case 'O':
                case 'U':
                case 'H':
                case 'W': 
                case 'Y':
                    t=0;
                    break;
            }
            if (i==len-1)
            {
                printf("\n");
            }   
        }
    }
    return 0;
}
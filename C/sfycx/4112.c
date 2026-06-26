#include <stdio.h>
#include <string.h>

int main()
{
    int n, q;
    char number[100000][16];
    int count[100000] = {0};
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
    {
        scanf("%s", number[i]);
        int p = 0;
        int len = strlen(number[i]);
        for (int j = 0; j < len; j++)
        {
            switch (number[i][j])
            {
            case '-':
                break;
            case 'A':
            case 'B':
            case 'C':
            {
                number[i][p] = '2';
                p++;
                break;
            }
            case 'D':
            case 'E':
            case 'F':
            {
                number[i][p] = '3';
                p++;
                break;
            }
            case 'G':
            case 'H':
            case 'I':
            {
                number[i][p] = '4';
                p++;
                break;
            }
            case 'J':
            case 'K':
            case 'L':
            {
                number[i][p] = '5';
                p++;
                break;
            }
            case 'M':
            case 'N':
            case 'O':
            {
                number[i][p] = '6';
                p++;
                break;
            }
            case 'P':
            case 'R':
            case 'S':
            {
                number[i][p] = '7';
                p++;
                break;
            }
            case 'T':
            case 'U':
            case 'V':
            {
                number[i][p] = '8';
                p++;
                break;
            }
            case 'W':
            case 'X':
            case 'Y':
            {
                number[i][p] = '9';
                p++;
                break;
            default:
                number[i][p] = number[i][j];
                p++;
            }
            }
        }
        number[i][p] = '\0';
    }
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (strcmp(number[j], number[j+1]) > 0) {
                char temp[16];
                strcpy(temp, number[j]);
                strcpy(number[j], number[j+1]);
                strcpy(number[j+1], temp);
            }
        }
    }
    for (int i = 0; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if (strcmp(number[i], number[j]) == 0)
            {
                number[j][0] = '\0';
                count[i]++;
            }
        }
        if (count[i] > 0&& number[i][0] != '\0')
        {
            for (int k = 0; k < 7; k++)
            {
                printf("%c", number[i][k]);
                if (k == 2)
                {
                    printf("-");
                }
            }
            printf(" %d\n", count[i] + 1);
            q = 1;
        }
    }
    if (q == 0)
    {
        printf("No duplicates.\n");
    }
    return 0;
}
#include<stdio.h>
#include<string.h>

typedef struct {
        char name[20];
        int score;
}stu;

int main(){
    int i=0,j,k;
    stu st[100]={0},stu_temp;
    while (i<100 && scanf("%s %d",st[i].name,&st[i].score)!=EOF)i++;
    for (j = 0; j < i-1; j++) {
        for (k = 0; k < i-1-j; k++) {
            if (st[k].score < st[k+1].score) {
                stu_temp = st[k];
                st[k] = st[k+1];
                st[k+1] = stu_temp;
            }
        }
    }
    for(j=0;j<i;j++)
        printf("%s %d\n",st[j].name,st[j].score);
    return 0;
}
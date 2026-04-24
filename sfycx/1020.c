#include<stdio.h>
#include<string.h>

//结构体
typedef struct {
        char name[20];
        int score;
}stu;

//主函数
int main(){
    int i=0,j,k,p=0,q=0,m=0,n=0;
    //char;
    //long;
    //float;
    stu st[100]={0},stu_temp;//
    while (i<100 && scanf("%s %d",st[i].name,&st[i].score)!=EOF)i++;
    for (j=0; j<i; j++) {
        if(st[p].score<st[j].score)p=j;
        if(st[q].score>st[j].score)q=j;
    }
    for (j=0; j<i; j++) {
        if(st[p].score==st[j].score)m=j;
        if(st[q].score==st[j].score)n=j;
    }
    if(m==p)printf("Max is %d,name has ",st[p].score);
    else printf("Max is %d,name have ",st[p].score);
    for (j=0;j<=m;j++){
        if (st[p].score==st[j].score){
            if(j<=m&&j!=p)printf(",");
            printf("%s",st[j].name);
        }
    }
    printf("\n");
    if(n==q)printf("Min is %d,name has ",st[q].score);
    else printf("Min is %d,name have ",st[q].score);
    for (j=0;j<=n;j++){
        if (st[q].score==st[j].score){
            if(j<=n&&j!=q)printf(",");
            printf("%s",st[j].name);
        }
    }  

    return 0;
}
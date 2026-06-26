// 输入包含一些三角形的描述，每个描述占一行，包括了三个整数a，b和c，表示对应的直角三角形的三个边。三个数字当中有一个等于-1（表示未知的边），其余两个都是正数（表示已知的边）。如果a=b=c=0表示输入结束。
// 输出:对于每个输入的三角形，首先要输出三角形的序号，如输出样例所示。如果不能构成直角三角形，输出“Impossible.”。否则，输出为“s = L”，其中s是未知边的名称（a，b或c），L为其长度，精确到小数点后三位。每个测试数据后输出一个空行。
#include<stdio.h>
#include<math.h>
int main(){
    double a,b,c;
    int t=1;
    while(scanf("%lf %lf %lf",&a,&b,&c)!=EOF){
        if(a==0&&b==0&&c==0){
            break;
        }
        if(a==-1){
            printf("Triangle #%d\n",t);
            if(b<c){
                double l=sqrt(c*c-b*b);
                printf("a = %.3lf\n\n",l);
            }else{
                printf("Impossible.\n\n");
            }
        }else if(b==-1){
            printf("Triangle #%d\n",t);
            if(a<c){
                double l=sqrt(c*c-a*a);
                printf("b = %.3lf\n\n",l);
            }else{
                printf("Impossible.\n\n");
            }
        }else if(c==-1){
            printf("Triangle #%d\n",t);
            double l=sqrt(a*a+b*b);
            printf("c = %.3lf\n\n",l);
        }
        t++;
    }
    return 0;
}
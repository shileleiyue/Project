#include <stdio.h>
#include <string.h>

int main() {
    char token[100];
    int cur_len = 0;
    int first_word = 1;

    while (scanf("%s", token) != EOF) {
        if (strcmp(token, "<br>") == 0) {
            printf("\n");
            cur_len = 0;
            first_word = 1;
        } 
        else if (strcmp(token, "<hr>") == 0) {
            if (cur_len > 0) {
                printf("\n");
            }
            for (int i = 0; i < 80; i++) {
                printf(".");
            }
            printf("\n");
            cur_len = 0;
            first_word = 1;
        } 
        else {
            int word_len = strlen(token);
            if (cur_len == 0) {
                printf("%s", token);
                cur_len = word_len;
                first_word = 0;
            } 
            else {
                if (cur_len + 1 + word_len <= 80) {
                    printf(" %s", token);
                    cur_len += 1 + word_len;
                } 
                else {
                    printf("\n%s", token);
                    cur_len = word_len;
                }
            }
        }
    }
    printf("\n");

    return 0;
}
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]){
    if (argc != 3){
        printf("usage:\n  %s source_file target_file\n", argv[0]);
        return -1;
    }
    FILE *src, *dst;
    src = fopen(argv[1],"rb");
    dst = fopen(argv[2],"wb");
    if (NULL == src || NULL == dst){
        printf("open file error!");
        return 1;
    }
    char buffer;
    fread(&buffer, 1, 1, src);
    while (feof(src) == 0){
        fwrite(&buffer, 1, 1, dst);
        fread(&buffer, 1, 1, src);
    }
}
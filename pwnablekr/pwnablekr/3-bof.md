# bof

## 문제

> Nana told me that buffer overflow is one of the most common software vulnerability.  
> Is that true?
>
> Download : [http://pwnable.kr/bin/bof](http://pwnable.kr/bin/bof)  
> Download : [http://pwnable.kr/bin/bof.c](http://pwnable.kr/bin/bof.c)
>
> Running at : nc pwnable.kr 9000

## 소스

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
    char overflowme[32];
    printf("overflow me : ");
    gets(overflowme);    // smash me!
    if(key == 0xcafebabe){
        system("/bin/sh");
    }
    else{
        printf("Nah..\n");
    }
}
int main(int argc, char* argv[]){
    func(0xdeadbeef);
    return 0;
}
```

## 취약점
* [버퍼 오버플로우 취약점](/system/Overflow.md) 

## 힌트
* [GDB](/tools/gdb.md)를 적극 활용 할 것
* [스택의 구조와 변수의 위치](/system.md)를 잘 확인할 것

## 공략




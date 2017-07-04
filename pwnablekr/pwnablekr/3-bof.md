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

* [버퍼 오버플로우 취약점](/system/overflow.md)

## 힌트

* [GDB](/tools/gdb.md)를 적극 활용 할 것
* [스택의 구조와 변수의 위치](/system.md)를 잘 확인할 것

## 공략

* 입력받은 인자가 0xcafebabe와 일치할 경우 쉘을 실행함.

* 별 다른 입력이 없을 경우 0xdeadbeef가 key에 들어가기에 Nah.... 가 출력됨.

```c
gets(overflowme);
if(key == 0xcafebabe){
    system("/bin/sh");
}
else{
    printf("Nah..\n");
}
```

* gdb로 main 함수를 보게 되면 0xdeadbeef를 인자로 받고 func함수를 호출함.

![](/assets/main.PNG)

* func 함수로 보면 0x64f에서 입력받은 값을 ebp-0x2c 버퍼에 받고 gets 함수를 통해 overflowme에 저장함.
* 아래 0x654에 CMP가 보이는데 이 부분이 소스의 IF부분으로 입력받은 값\(ebp+0x8\)과 0xcafebabe를 비교함.

* 값이 같지 않으면 JNE\(Jump Not Equal\)에 의해서 x66b로 이동 후 Nah.. 를 출력함.

* 값이 같을 경우,  system 함수 호출 후 /bin/sh 실행 후 종료함.

![](/assets/func.PNG)

cafebabe와 값을 일치하기 위해서는 overflowme라는 char형\(32 bytes\) 변수를 넘어서 할당되지 않은 부분에 데이터를 입력해야 함.

overflowme 변수를 꽉 채워도 ebp-0xc 부분까지만 채워지므로 ebp+0x8까지가 SFP\(EBP\), RET, Dummy 값을 합한 공간으로 20bytes임을 확인할 수 있음.

이를 토대로 char형 32bytes, SFP\(EBP\), RET, Dummy 값의 20bytes를 합친 52bytes에 쓰레기 값을 대입해준 다음에 0xcafebabe를 입력해주면 값을 일치시킬 수 있음.

> 위의 복잡한 용어를 제외하고 단순히 메모리 주소로 계산해도 
>
> ebp-0x2c\(overflow 배열의 시작주소\)부터 ebp+0x8\(key 주소\)까지 
>
> 0x2c\(44\) + 0x8\(8\) = 52라는 계산이 나온다.




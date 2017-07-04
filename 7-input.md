# input

## 문제

> Mom? how can I pass my input to a computer program?
>
> ssh input2@pwnable.kr -p2222 \(pw:guest\)

## 소스

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(int argc, char* argv[], char* envp[]){
    printf("Welcome to pwnable.kr\n");
    printf("Let's see if you know how to give input to program\n");
    printf("Just give me correct inputs then you will get the flag :)\n");

    // argv
    if(argc != 100) return 0;
    if(strcmp(argv['A'],"\x00")) return 0;
    if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
    printf("Stage 1 clear!\n");    

    // stdio
    char buf[4];
    read(0, buf, 4);
    if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
    read(2, buf, 4);
        if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
    printf("Stage 2 clear!\n");

    // env
    if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
    printf("Stage 3 clear!\n");

    // file
    FILE* fp = fopen("\x0a", "r");
    if(!fp) return 0;
    if( fread(buf, 4, 1, fp)!=1 ) return 0;
    if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
    fclose(fp);
    printf("Stage 4 clear!\n");    

    // network
    int sd, cd;
    struct sockaddr_in saddr, caddr;
    sd = socket(AF_INET, SOCK_STREAM, 0);
    if(sd == -1){
        printf("socket error, tell admin\n");
        return 0;
    }
    saddr.sin_family = AF_INET;
    saddr.sin_addr.s_addr = INADDR_ANY;
    saddr.sin_port = htons( atoi(argv['C']) );
    if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
        printf("bind error, use another port\n");
            return 1;
    }
    listen(sd, 1);
    int c = sizeof(struct sockaddr_in);
    cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
    if(cd < 0){
        printf("accept error, tell admin\n");
        return 0;
    }
    if( recv(cd, buf, 4, 0) != 4 ) return 0;
    if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
    printf("Stage 5 clear!\n");

    // here's your flag
    system("/bin/cat flag");    
    return 0;
}
```

## 취약점

## 힌트

* stage 1:
* stage 2:
* stage 3:
* stage 4:
* stage 5:
* script 작성시 홈폴더에는 저장이 안되므로
	mkdir /tmp/임의디렉토리명
으로 디렉토리를 만들어서 스크립트를 짭니다.
* 마지막에 임의디렉토리에는 flag 파일이 없는 것을 고려하여야 합니다.
* 힌트 사이트 : [https://werewblog.wordpress.com/2016/01/11/pwnable-kr-input/](https://werewblog.wordpress.com/2016/01/11/pwnable-kr-input/)

## 공략

```c
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

void main(void) {
	// for stage1
	char *argv[101]={"/home/input2/input", [1 ... 99] = "A", NULL};
	argv['A'] = "\x00";
	argv['B'] = "\x20\x0a\x0d";

	// for stage2
	int pipe2stdin[2] = {-1,-1};
	int pipe2stderr[2] = {-1,-1};
	pid_t childpid;

	// for stage3
	char *env[2] = {"\xde\xad\xbe\xef=\xca\xfe\xba\xbe", NULL};
 
	// for stage4
	FILE* fp = fopen("\x0a", "w");

	// for stage5
	int cd;
	struct sockaddr_in saddr;
	argv['C'] = "7777";
	

	// source
	// for stage4
	fwrite("\x00\x00\x00\x00", 1, 4, fp);
	fclose(fp);
	// for stage2
	if ( pipe(pipe2stdin) < 0 || pipe(pipe2stderr) < 0){
	    perror("Cannot create the pipe");
	    exit(1);
	}
 
	if ( ( childpid = fork() ) < 0 ){
	    perror("Cannot fork");
	    exit(1);
	}
 
	if ( childpid == 0 ){
	    /* Child process */
	    close(pipe2stdin[0]); close(pipe2stderr[0]); // Close pipes for reading
	    write(pipe2stdin[1],"\x00\x0a\x00\xff",4);
	    write(pipe2stderr[1],"\x00\x0a\x02\xff",4);
	    
	    // for stage 5
	    saddr.sin_addr.s_addr = inet_addr("127.0.0.1");
	    saddr.sin_family = AF_INET;
	    saddr.sin_port = htons(7777);
		printf("socket()\n");
	    cd = socket(AF_INET, SOCK_STREAM, 0);
	    if(-1 == cd)
	    {
		printf("socket error!\n");
		exit(0);
	    }
		printf("sleep()\n");
	    sleep(1);
		printf("connect()\n");
	    if(-1==connect(cd, (struct sockaddr *)&saddr, sizeof(saddr)))
	    {
		printf("connect error!\n");
		exit(0);
	    }
		printf("send()\n");
	    send(cd, "\xde\xad\xbe\xef", 4, 0);
		printf("close(sd)\n");
	    close(cd);
	}
	else {
	    /* Parent process */
	    close(pipe2stdin[1]); close(pipe2stderr[1]);   // Close pipes for writing
	    dup2(pipe2stdin[0],0); dup2(pipe2stderr[0],2); // Map to stdin and stderr
	    close(pipe2stdin[0]); close(pipe2stderr[1]);   // Close write end (the fd has been copied before)
	    // for stage 1, 3
	    execve("/home/input2/input", argv, env);  // Execute the program
	}
}
```




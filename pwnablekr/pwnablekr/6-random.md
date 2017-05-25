# random

## 문제

> Daddy, teach me how to use random value in programming!
>
>
>
> ssh random@pwnable.kr -p2222 \(pw:guest\)

## 소스

```c
#include <stdio.h>

int main(){
	unsigned int random;
	random = rand();	// random value!

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




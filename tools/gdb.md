### 인텔 문법으로 변환

* `gdb) set disas(embly-flavor) intel  `

* 영구 변환
  * `$ cat set disas(embly-flavor) intel > ~/.gdbinit    `

### 명령어

* list

* run

* break \[func\|point\]

* next

* info \[register\|\]
  * info register : 레지스터 보기
  * i r \[레지스터\] : 특정 레지스터 보기

* x/\[옵션\] \[메모리위치\|레지스터\]
  예\)  `x/4xb $ebp`   `x/1xw 0x8048384  `
  * 형식
    * o 8진법
    * x 16진법
    * u 부호가 없는 표준 10진법
    * t 2진법
  * 크기
    * b 단일 바이트
    * h 2바이트의 하프 워드
    * w 4바이트의 워드
    * g 8바이트의 자이언트




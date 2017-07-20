### 인텔 문법으로 변환

* `gdb) set disas(embly-flavor) intel`

* 영구 변환

  * \`$ cat set disas\(embly-flavor\) intel &gt; ~/.gdbinit
    \`

### 명령어

* list

* run

* break \[func\|point\]

* next

* info \[register\]

  * info register : [레지스터 ](/system/assembly-lang.md)보기
  * i r \[레지스터\] : 특정 레지스터 보기
  * 변수보기
    * info variable : 전역/static 변수 보기
    * info locals : 지역변수 보기(현재 스택 프레임에서)
    * info args : 인수 보기(현재 스택 프레임에서)
    * info symbol [주소] : 주소의 symbol 보기

* x/\[옵션\] \[메모리위치\|레지스터\]  
  예\)  `x/4xb $ebp`, `x/1xw 0x8048384`

  * 형식
    * o 8진법
    * x 16진법
    * u 부호가 없는 표준 10진법
    * t 2진법
  * 크기
    * b 단일 바이트
    * h 2바이트의 하프 워드
    * w 4바이트의 워드[^1]
    * g 8바이트의 자이언트

[^1]: word : 컴퓨터에서 기본적으로 읽는 데이터 크기


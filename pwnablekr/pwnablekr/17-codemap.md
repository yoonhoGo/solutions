# codemap

## 문제

> I have a binary that has a lot information inside heap.
>
> How fast can you reverse-engineer this?
>
> \(hint: see the information inside EAX,EBX when 0x403E65 is executed\)
>
> download: http://pwnable.kr/bin/codemap.exe         ssh codemap@pwnable.kr -p2222 \(pw:guest\)

## 힌트

> 0x403E65에 BP,  codemap프로그램 사용, IDA사용 \(전 이걸로 풀어서...\) 또는 win 32debuger 사용  
>
> https://github.com/c0demap/codemap 에서 다운로드 한다 
>
> BP에 자원기준으로 저장된다. 쿼리를 날려서 문제에 대한 답을 가져오면 된다.




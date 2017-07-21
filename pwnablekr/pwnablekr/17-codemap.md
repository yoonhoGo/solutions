# codemap

## 문제

> I have a binary that has a lot information inside heap.
>
> How fast can you reverse-engineer this?
>
> \(hint: see the information inside EAX,EBX when 0x403E65 is executed\)
>
> download: [http://pwnable.kr/bin/codemap.exe](http://pwnable.kr/bin/codemap.exe)

ssh codemap@pwnable.kr -p2222 \(pw:guest\)

## 힌트

> 0x403E65에 BP,  codemap프로그램 사용, IDA사용 \(전 이걸로 풀어서...\) 또는 win 32debuger 사용
>
> [https://github.com/c0demap/codemap](https://github.com/c0demap/codemap) 에서 다운로드 한다
>
> BP에 자원기준으로 저장된다. 쿼리를 날려서 문제에 대한 답을 가져오면 된다.

## 참고

> Codemap은 IDA 플러그인으로 제공되는 "실행 추적 시각화"를위한 이진 분석 도구입니다.
>
> Intel PIN 또는 QEMU와 같은 DBI \(Dynamic Binary Instrumentation\) 기반 도구와 달리 Codemap은 프로그램의 제어 흐름이 추적 점을 통과하는 동안 레지스터 / 메모리 정보를 생성하기 위해 '추적 점'을 사용합니다.
>
> 자세한 내용은 https://github.com/c0demap/codemap 참고 바람






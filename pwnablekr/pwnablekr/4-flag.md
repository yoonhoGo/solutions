# flag

## 문제

```
Papa brought me a packed present! let's open it.

Download : http://pwnable.kr/bin/flag

This is reversing task. all you need is binary
```

## 취약점

* 바이너리 파일의 패킹 여부 확인 후 언패킹

## 공략

* 링크의 파일을 다운받아 IDA Pro로 연다.

![](/assets/ida.png)

* 파일을 여는 과정에서 64비트의 리눅스 실행파일\(ELF\)인 것을 알 수 있다.

* 해당 바이너리 파일에서 사용된 스트링을 보기 위해서 String window를 연다.

![](/assets/ida2.png)

* 총 세개의 스트링이 있는데 이 중 upx.sf.net 이라는게 눈에 띄어서 인터넷 주소창에 그대로 입력해 보았다.

![](/assets/upx.png)

* 실행파일을 패킹하는 툴중 하나인 [UPX](https://goyunho.gitbooks.io/solutions/content/tools/upx.html) 사이트로 이동된걸 보아 바이너리 파일이 UPX라는 패킹툴로 패킹되었다는 사실을 알 수 있다.
* UPX는 패킹기능과 언패킹 기능을 모두 제공하고 있다고 한다.
* [https://github.com/upx/upx/releases/latest](https://github.com/upx/upx/releases/latest) 이 곳에서 UPX툴을 다운받아 패킹된 flag 파일을 언패킹한다.

![](/assets/upx2.png)

* 언패킹 명령어는 upx -d \[언패킹 할 파일이름\] 이다.

* 언패킹 된 flag 파일을 다시 IDA Pro로 연다.

* String windows를 열면 flag를 알 수 있다.




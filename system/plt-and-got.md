# 흐름을 그림으로 간단히 보기
출처 : [http://cfile28.uf.tistory.com](http://cfile28.uf.tistory.com)
### GOT를 처음 참조할 때
![](http://cfile28.uf.tistory.com/image/2117054757A5D63420BD21)
### GOT에 주소가 저장된 후
![](http://cfile21.uf.tistory.com/image/21717E4D57A5D7DC281CEB)

---

# PLT와 GOT 자세히 알기

출처 : [https://bpsecblog.wordpress.com/2016/03/07/about\_got\_plt\_1/](https://bpsecblog.wordpress.com/2016/03/07/about_got_plt_1/)

### Dynamic Linking 과정을 추적해 PLT와 GOT를 이해해보자 :\)

---

## PLT and GOT

시스템 해킹을 공부하시는 분들이라면 PLT와 GOT에 대해 알고 있을 것입니다. 이제 막 시스템 해킹 공부를 시작한 분들도 한 번 쯤 들어보셨을 겁니다.

* **PLT \(Procedure Linkage Table\)**  
  : 외부 프로시저를 연결해주는 테이블. PLT를 통해 다른 라이브러리에 있는 프로시저를 호출해 사용할 수 있다.

* **GOT \(Global Offset Table\)**  
  : PLT가 참조하는 테이블. 프로시저들의 주소가 들어있다.

PLT와 GOT에 대해서는 대부분 이렇게 알고 있을 것입니다.

> ” 함수를 호출하면\(PLT를 호출하면\) GOT로 점프하는데 GOT에는 함수의 실제 주소가 쓰여있다.  
> 첫 번째 호출이라면 GOT는 함수의 주소를 가지고 있지 않고 ‘어떤 과정’을 거쳐 주소를 알아낸다.  
> 두 번째 호출 부터는 첫 번째 호출 때 알아낸 주소로 바로 점프한다. “

‘당연히 그렇겠거니-‘ 할 수도 있지만, 조금 더 의문을 가져봅시다. 함수의 주소로 바로 점프하면 되지 않을까? 왜 PLT와 GOT를 두고 사용하는 것일까? GOT가 함수의 주소를 알아내는 ‘어떤 과정’이라는 것은 무엇일까?

##### 1. STATIC LINK와 DYNAMIC LINK – GOT와 PLT는 왜 사용할까요?

PLT와 GOT를 왜 사용하는지 알기 위해서는 먼저 링커\(Linker\)를 알아야 합니다.

어떤 코드를 작성한다고 생각해봅시다.  예를들어, 소스 안에는 printf 함수를 호출하는 코드가 있고 include 한 헤더파일에는 printf의 선언이 있습니다. 소스파일을 실행파일로 만들기 위해서 ‘컴파일\(compile\)’이라는 과정을 거쳐야겠죠.

![](https://bpsecblog.files.wordpress.com/2016/02/gote1848be185aaplt-1-e18480e185b3e18485e185b5e186b72.png?w=1000 "got와plt-1-그림2")

\[그림 1\] GNU C 컴파일 과정

컴파일을 통해 오프젝트 파일이 생성됩니다. 하지만 오브젝트 파일은 그 자체로 실행이 가능하지는 않습니다. printf의 구현 코드를 모르기 때문이죠. printf를 호출 했을 때 어떤 코드를 실행해야 하는지, 우리가 작성한 코드만 가지고서는 아무것도 알 수 없습니다.

오브젝트 파일을 실행 가능하게 만들기 위해서는 printf의 실행 코드를 찾아서 오브젝트 파일과 연결시켜야 합니다. printf의 실행 코드는 printf의 구현 코드를 컴파일한 오브젝트 파일로, 이런 오브젝트 파일들이 모여있는 곳을 **라이브러리\(Library\)**라고 하죠.

![](https://bpsecblog.files.wordpress.com/2016/02/gote1848be185aaplt-1-e18480e185b3e18485e185b5e186b711.png?w=1000 "got와plt-1-그림1")

\[그림 2\] 소스파일이 실행파일이 되기까지

이렇게 라이브러리 등 **필요한 오브젝트 파일들을 연결시키는 작업을 링킹\(Linking\)**이라고 합니다.  
이렇게 링크 과정까지 마치면 최종적인 실행파일이 생깁니다.

---

## 링크

링크를 하는 방법에는 Static과 Dynamic 방식이 있습니다.

![](https://bpsecblog.files.wordpress.com/2016/02/gote1848be185aaplt-1-e18480e185b3e18485e185b5e186b73.png?w=459&h=450 "got와plt-1-그림3")

\[그림 3\] Static Link 방식을 통한 실행파일 생성

**Static Link 방식은 파일 생성시 라이브러리 내용을 포함한 실행 파일을 만듭니다.**

![](https://bpsecblog.files.wordpress.com/2016/03/e18489e185b3e1848fe185b3e18485e185b5e186abe18489e185a3e186ba-2016-03-08-e1848be185a9e18492e185ae-5-04-58.png?w=1000 "스크린샷 2016-03-08 오후 5.04.58")

\[그림 4\] Static Compile

gcc 옵션 중 static 옵션을 적용하면 Static Link 방식으로 컴파일 됩니다.

실행 파일 안에 모든 코드가 포함되기 때문에 라이브러리 연동 과정이 따로 필요 없고, 한 번 생성한 파일에 대해서 필요한 라이브러리를 따로 관리하지 않아도 되기 때문에 편하다는 장점이 있습니다. 하지만 파일 크기가 커지는 단점이 있고 동일한 라이브러리를 사용하더라도 해당 라이브러리를 사용하는 모든 프로그램들은 라이브러리의 내용을 메모리에 매핑 시켜야 합니다.

![](https://bpsecblog.files.wordpress.com/2016/02/gote1848be185aaplt-1-e18480e185b3e18485e185b5e186b74.png?w=566&h=435 "got와plt-1-그림4")

\[그림 5\] dynamic linking

**Dynamic Link 방식은 공유라이브러리를 사용합니다. **라이브러리를 하나의 메모리 공간에 매핑하고 여러 프로그램에서 공유하여 사용하는 것이죠.

실행파일 안에 라이브러리 코드를 포함하지 않으므로, Static Link 방식을 사용해 컴파일 했을 때에 비해 파일 크기가 훨씬 작아집니다. 실행시에도 상대적으로 적은 메모리를 차지하겠죠. 또한 라이브러리를 따로 업데이트 할 수 있기 때문에 유연한 방법입니다. 하지만 실행파일이 라이브러리에 의존해야 하기 때문에 라이브러리가 없으면 실행할 수 없습니다.

![](https://bpsecblog.files.wordpress.com/2016/02/gote1848be185aaplt-1-e18480e185b3e18485e185b5e186b76.png?w=1000 "got와plt-1-그림6")

\[그림 6\] Dynamic Compile

아무런 옵션도 주지 않는다면, 자동으로 Dynamic Link 방식으로 컴파일 합니다.

---

## 그래서..??

Dynamic Link 방식으로 컴파일 했을 때 PLT와 GOT를 사용하게 되는데, 이유가 슬슬 짐작이 가시나요?

Static Link 방식으로 컴파일 하면 라이브러리가 프로그램 내부에 있기 때문에 함수의 주소를 알아오는 과정이 필요하지 않지만, Dynamic Link 방식으로 컴파일 하면 라이브러리가 프로그램 외부에 있기 때문에 함수의 주소를 알아오는 과정이 필요한 것입니다.

![](https://bpsecblog.files.wordpress.com/2016/02/gote1848be185aaplt-1-e18480e185b3e18485e185b5e186b77.png?w=1000 "got와plt-1-그림7")

\[그림 7\] PLT와 GOT의 호출관계

Dynamic Link 방식으로 프로그램이 만들어지면 함수를 호출 할 때 PLT를 참조하게 됩니다. PLT에서는 GOT로 점프를 하는데, GOT에 라이브러리에 존재하는 실제 함수의 주소가 쓰여있어서 이 함수를 호출하게 됩니다.

그런데 이 때, 첫 호출이냐 아니냐에 따라 동작 과정이 조금 달라집니다.

두 번째 호출이라면 GOT에 실제 함수의 주소가 쓰여있지만, 첫 번째 호출이라면 GOT에 실제 함수의 주소가 쓰여있지 않습니다.

그래서**첫 호출 시에는 Linker가 dl\_resolve라는 함수를 사용해 필요한 함수의 주소를 알아오고, GOT에 그 주소를 써준 후 해당 함수를 호출합니다.**

![](https://bpsecblog.files.wordpress.com/2016/02/gote1848be185aaplt-1-e18480e185b3e18485e185b5e186b78.png?w=1000 "got와plt-1-그림8")

\[그림 8\] gdb로 열어본 Static compile 된 프로그램

함수 호출 전과 후의 주소가 같고, 처음부터 putchar함수의 주소를 가리키고 있습니다.putchar함수의 주소 또한 프로그램의 text영역 안에 있는 것으로 보입니다.

![](https://bpsecblog.files.wordpress.com/2016/02/gote1848be185aaplt-1-e18480e185b3e18485e185b5e186b79.png?w=1000 "got와plt-1-그림9")

\[그림 9\] gdb로 열어본 Dynamic compile 된 프로그램

함수 호출 전과 후의 주소가 다르고, 두 번째 호출부터 putchar함수의 주소를 가리키고 있습니다. putchar함수의 주소 또한 프로그램의 내부에 있는 주소로는 보이지 않습니다.


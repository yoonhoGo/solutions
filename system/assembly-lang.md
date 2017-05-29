# 레지스터

### 범용 레지스터[^1]

| 이름 | 설명 |
| :---: | :--- |
| AX\(Accumulator Register\) | 산술연산 명령에서 상수/변수 값을 저장하거나 함수의 리턴 값이 저장되는 용도 |
| BX\(Base Register\) | DS 세그먼트에 대한 포인터를 주로 저장하고 ESI나 EDI와 결합하여 인덱스에 사용. BX는 메모리 주소 지정을 확장하기 위해 인덱스로 사용될 수 있는 유일한 범용 레지스터 |
| CX\(Counter Register\) | 반복 명령어 사용시 반복 카운터로 사용. CX에 반복할 횟수를 지정해 놓고 반복 작업을 수행 |
| DX\(Data Register\) | 입출력 포인터 값을 저장할때 사용 |
| SI\(Source Index\) | 데이터 복사, 조작 시 Source Data\(원본\) 주소가 저장. SI 레지스터가 가리키는 주소의 데이터를 DI 레지스터가 가리키는 주소로 복사하는 용도로 많이 사용 |
| DI\(Destination Index\) | 복사 작업 시 Destination\(목적지, 사본\)의 주소가 저장.주로 SI 레지스터가 가리키는 주소의 데이터가 복사 됨. |
| SP\(Stack Pointer\) | 하나의 스택 프레임의 끝 지점 주소가 저장. PUSH, POP 명령어에 따라서 SP의 값이 nByte\(거의 항상 4바이트\)씩 변한다. |
| BP\(Base Pointer\) | 스택 프레임의 시작 지점 주소가 저장. 스택 프레임이 소멸 되지 않는 동안 BP의 값은 변하지 않음. 현재의 스택 프레임이소멸되면 이전에 사용하던 스택 프레임을 가리킴. |

### 명령 포인터 레지스터

\(E\)IP\(\(Extended\) Instruction Pointer\) : 다음에 실행해야 할 명령어가 존재하는 메모리 주소가 저장된다. 현재 명령어를 실행 완료한 후에 IP 레지스터에 저장되어 있는 주소에 위치한 명령어를 실행하게 된다. 실행 전 IP 레지스터에는 다음 실행해야 할 명령어가 존재하는 주소의 값이 저장된다.

### 세그먼트 레지스터

CS\(Code Segment\) : 코드 영역의 시작 주소를 저장

DS\(Data Segment\) : 데이터 영역의 시작 주소를 저장

ES\(Extra Segment\) : 비디오 영역의 시작 주소를 저장

FS : 기타영역의 시작 주소를 저장

SS\(Stack Segment\) : 스택 영역의 시작 주소를 저장

# 참고 자료

* [http://securityfactory.tistory.com/182](http://securityfactory.tistory.com/182)

---

# ARM 프로세스 asm
[ARM infomation center > 4.0 버전 한국어 문서](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0204ik/index.html)

---
[^1]: 레지스터 이름 앞에 E가 붙으면 32bit\(Extended\), R은 64bit

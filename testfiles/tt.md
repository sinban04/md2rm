* BFL Porting on Debian
  * ppt2x 쪽에서 이상한 문법 에러 디버깅
  * 3rd Party Xerces library debian 기반 빌드용으로 변경
    * Xerces 가 바라보는 uncv library 관련 에러 발생
    * Debian 기반에서 빌드한 후, 문제없이 동작
* TA 와 CWM(CCOPOD) 분석
  * 프로세스 형태
    * TA 는 user application 으로 일반적으로 하나의 단일 프로세스로 구성 (background process 들 제외)
    * CWM 의 경우, system daemon 으로 부팅 순간부터 항상 background 에서 동작 (init daemon)
  * TA 가 client 코드를 통해 CWM 과 통신(IPC)
    * Unix domain socket 을 이용하여 IPC 통신
  * TA 가 system service 에 대해 필요한 부분은 client 을 통해 CWM 에게 요청
    * CWM 은 해당 요청을 SingletonManagerFactory 를 통해 system service 요청 및 관리
      * InputService
      * BaseWindowService
      * ShadowService
      * CDSService
  * TA 프로세스는 5가지 APart 를 가짐
    * 에 따라 세 가지 queue 유지 (-100, 0, 100)
      * PostTask() 를 통해 온 task 들을 갖고 있는 queue
      * schedulePaint() 를 통해, widget 들이 RenderContext 의invalidated widget list 에 추가됨
    * EventManager 코드를 통해서 epoll 로 FD polling 함
* TA 의 Event Handling
  * Input_Libinput 을 통해, mouse, keyboard 같은 서비스를 받아옴 (from /dev/input/)
    * Linux 에서는 /dev/input/ 를 통해 user-level 에 input event 제공
  * Input_Libinput 을 통해 InputService 를 SingletonManagerFactory 가 받음 (CWM 과 같은 프로세스)
    * CWM 코드를 통해, TA 에게 이벤트 전달
* Poo-version TA 구조
  * *AA* 와 같은 구조로, 가장 빠른 시간안에 구현 가능한 방법으로 진행
  * 크게 세 부분으로 구성
    * TA 부분: 실질적인 Office 관련 코드가 동작
    * CCOPOD 부분: TA 와 platform 사이에서 통신 및 Document 들을 관리
    * TTT.js 부분: **Poo 와의 Glue** 를 담당하며, 모든 플랫폼 관련 부분들을 담당
      * Graphic, Window, UI 와 관련된 모든 서비스들을 제공 및 관리
  * Platform-dependent issue
    * System call 사용 부분은 Library Wrapper 를 사용해서 platform decoupling 진행
    * 3rd party library 들은 Poo 에서 새로 빌드하여 사용가능
    * AOS 코드 (e.g., twk) 는 Poo 로의 포팅 필요
  * Process Model (2가지 안)
    * 2 process: TA 프로세스와 CCOPOD 프로세스와 TTT.js 를 담당하는 프로세스로 구성
    * 3 process: TA 프로세스와 CCOPOD 과 TTT.js 를 담당하는 프로세스로 구성
  * IPC
    * Poo 에서 제공하는 pipe 를 통해서 IPC 사용
  * AOS-coupling issue
    * TMF (media framework) 나 Registry 는 AOS 에 strongly-coupling 되어있어서, Poo 에서 새로 구현 필요

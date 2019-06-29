# 19 d.

## TA for Poo

### Base library build

* 컴파일 진행 방향
  * 1안) AOS-Linux(POSIX)-Poo(awin)
    * AOS 코드 중 Linux(POSIX) 쪽 코드로 빌드
    * Poo 에서 컴파일 할 때에는 awin 으로 POSIX 컴파일처럼 구현
  * 2안) AOS-Linux(POSIX) & AOS-Poo
    * AOS 코드 중 Poo 관련 코드가 있는 부분으로 빌드
  * Base 를 빌드하는 과정에서 \*\_win.h 이나 win/ 디렉토리가 있어서, 2안으로 해보려고 함
    * 2안으로 진행하던 중, Poo 를 참조하는 곳과 POSIX 를 참조하는 곳이 겹치게 됨
    * Linux 에 tight-coupled 된 부분들이 많아서 불가
  * Base 의 build_config.h 를 OS_WIN 으로 설정하지 않고, OS_LINUX 로 설정하고 진행
* 이전의 Base 의 dependency tree 는 linking 하는 타겟 기준임
  * Base library 를 컴파일 하는 과정에서 직접 소스 컴파일로 여러 third_party 및 다른 타켓 사용
* Stack trace compile error (se/debug/stack_trace_posix.cc)
  * 리눅스 헤더(ffff.h)가 존재하지 않음
    * 해당 헤더(ffff.h)가 GNULib 코드이며, backtrace 할 때 사용됨
    * 현재 GNULib 이 몇몇 Platform 에서는 지원되지 않음: [awin 포함][1]
* 파일 (file stat)관련 compile error (file_posix.cc)
  * GNU file stat 관련 구현체가 없는 이슈 (이전 민규씨가 겪으셨던 이슈)
  * sys/stat.h 는 Linux 가 사용하는 GNU C Library 안에 들어있는 파일 중 하나
  * [awin 에서는 struct stat64 구조체를 제공하지 않고 있음][2]
    * `fstat64()` 함수가 `struct stat64` 를 사용
    * fstat64() 함수가 fstat() 함수와 같은 기능을 하는 함수이므로 [대체해도 문제가 되지 않을 것으로 보임][3]
  * `fstat64, stat64, lstat64` 를 `fstat, stat, lstat` 으로 변경하여 해결
* kevent_loop error
  * 리눅스 매크로로 인해 (ab 은 리눅스가 아니므로), 문법적인 에러가 발생
    * Linux 매크로에 awin 매크로도 함께 추가하여 해결
* `evli` 를 찾지 못해서 에러 발생
  * sys/event.h 가 kqueue 라이브러리에서 온 듯한데, 이 kqueue 가 Freebsd 커널 코드에서부터 온 듯함
    * `kqueue` 타겟이 외부에서 온 것이라기보다는 AOS 의 kqueue 타겟을 사용하는 것으로 보임
* GCC 관련 매크로는 Clang 컴파일러를 사용해도 컴파일러 안에서 잘 설정됨
  * `CCOPODPILER_GCC, __GNUC__`
* `wchar_t` size issue
  * 시스템에서 정의한 wchar_t 의 사이즈에 따라 wchar_t 이 UTF-16, UTF-32 로 나뉨
    * Poo 는 UTF-16 을 사용하고, Linux 에서는 UTF-32 를 사용
  * awin 은 POSIX 와 같은 환경을 제공하지만, Poo 이기 때문에 UTF-16 사용
  * `WCHAR_T_IS_UTF_16` 과 `WCHAR_T_IS_UTF_32` 매크로 설정 시점에 wchar_t 값을 판단함
    * 각 매크로 정의에 따라 wchar_t 를 그대로 사용할 지, uint16_t 를 사용할지 결정
    * 그러므로 그냥 WCHAR_T_IS_UTF32 매크로로 설정해도 uint16_t 로 설정되기 때문에 문제 없을 것으로 판단
  * WCHAR_T_IS_UTF32 매크로 설정함으로써 해결
* sys/prctl.h not found error
  * 이후 대체하기 위해 무시하고 넘어감
* `pthread_key` assign 에러
  * Base 코드에서 사용하는 PlatformThreadLocalStorage::TLSKey 가 se::subtle::Atomic32 와 맞지 않아 에러 발생
    * pthread_key_t 값에 대해서, 일반적인 Linux 에서는 int 값을 사용
    * awin 에서는 pthraed_key_t 를 awin 에서 만든 pthread_key 라는 클래스로 정의
    * Base 코드에서는 int 로 가정하고 se::subtle::Atomic32 (int) 를 사용
* Linking error
  * /usr/bin/ld 의 '-z' linking option 이 ld.exe 에는 존재하지 않음
    * '-z' 관련 옵션들은 ELF emulation 관련 옵션들임
  * `-z,now -z,relro -z,noexecstack` 옵션 제거
* `strlcpy() strlcat()` 등 함수 중복
  * common/linux/include.h 에서 정의한 strlcpy, strlcat 두 함수가 /usr/include/string.h 정의와 겹침
  * include/fls.h 에서 정의한 fls() 함수가, /usr/include/strings.h 의 정의가 겹침
  * Linux kernel 에는 해당 함수들이 포함되어 있지만, 해당 함수를 포함해야하는 아키텍처에만 사용되는 듯함
    * `__HAVE_ARCH_STRLCPY` 매크로로 확인 후에 사용됨
  * 현재 Linux 와 AOS 의 /usr/include/string.h 에는 해당 함수들이 존재하지 않음
    * awin 기반에서는 해당 함수가 `__BSD_VISIBLE` 매크로와 함께 정의되어 있음 (위 함수들 모두)
  * 해당 부분 주석처리
* Linux container 설치 이슈
  * zone_util.c (src/common/)
  * Linux container 라이브러리 자체를 설치해야하는 이슈라서, 추후 해결 필요
* `kqueue` target compilation error
  * kqueue 는 Linux-dependent 한 부분들이 많아서, 전체적으로 추후 해결 필요
* 현재 진행 상황
  * Fundamental 한 이슈들을 제외하고, se 라이브러리 및 관련 의존적인 target 들 컴파일 완료
  * `undefined referend to functionA()...` 이런식으로 에러 뜨는 중



[1]:https://www.gnu.org/software/gnulib/manual/html_node/ffff_002eh.html
[2]:https://ab.com/faq.html#faq.programming.stat64
[3]:https://www.mkssoftware.com/docs/man3/stat.3.asp

# 0612 Wd.

## TA for Poo

### Base library build

* Fork from tos/master
  * tos/master 에서 v5.0.1 태그로 코드 fork
  * Submodule 들도 함께 받은 뒤에 통채로 fork
    * Submodule command 가 각 cmake 에 정의되어 있으며, 각 submodule 마다 특정 commit 을 사용하도록 되어있음
    * Submodule 들의 git 정보도 제거하고 AOS 의 하나의 소스코드 형태로 만듬
* AOS 의 ccLists.txt 파일들이 가독성이 떨어져서 해석하는데 시간이 좀 소요됨
  * ccLists.txt 작성 시 가독성을 그다지 고려하지 않음
  * FIXME, TODO, temporary code, 등 수정중이었던 코드들이 많음
  * cc 문법의 잘못된 사용으로 의미없는 코드가 존재하거나, 잘못사용하고 있는 경우들 존재
  * ccLists.txt 파일들 내에서 linking 하는 라이브러리 이름들이, 다른 곳에서 만든 것인지 외부 라이브러리인지 판단 필요
* Base-related library dependency tree (cmake target 별로 기록)
  * 직접 Linking 하고 있는 것들을 기록하고, dependency 는 따로 표시함
    * AOS 에서 개발하지 않고, 외부에서 가져온 라이브러리들은 ext 로 표시
  * se
    * modp_b64_host
    * frame
      * {cfg_gen_list}(dep)
        * cfg_en.list
    * common
      * ssl (ext)
      * crypto (ext)
      * elf (ext)
      * util (ext) - 아마도 Linux 의 [libutil][1] 라이브러리 인듯?
      * lxc (ext)
      * {frame}(dep)
    * se_static_host
    * allocator_extension_thunks_host
    * dynamic_annotations_host
    * symbolize_host
    * xdg_mime_host
    * event (ext) - [libevent][2]
    * xml2 (ext) - [libxml2][3]
    * kqueue
      * Ws2_32 (Win32 일 때) (ext)
      * Threads::Threads (ext)
  * se_prefs
    * se_static
  * se_i18n
    * dynamic_annotations
    * se
    * icui18n (ext)
    * icudata (ext)
    * icuio (ext)
  * symbolize_host
  * ${LIBRARY}_host, ${LIBRARY} 이런 식으로 두 가지 target 을 갖는 패턴 존재함
    * 하나는 target, 하나는 host 에 대응하는 것인 듯하나, 어떤 사용법인지는 잘 모르겠음
* Build plan
  * awin 32bit 에서 빌드 진행 & 최소한으로 필요한 라이브러리만 빌드하는 식으로 진행
    * awin 64bit 에서는 system data type 에 대해서 다른 정의가 있음
  * cc 를 포함해서 AOS 의 전체 빌드 과정이 하드코딩된 부분들이 많아서 cc 를 대대적으로 수정하고 새로 짜야함
    * 플랫폼 호환성을 고려하지 않고 일단 Poo 에서 될 수 있도록만 수정
  * Prerequisite (ab package installer 로 설치)
    * `cmake, automake, make, cli, python`
    * 가장 기본적으로 소스를 빌드하기 위한 prerequisite 들 (gitlab project README 에 정리)
  * Base 에서 target 하나씩 주석 풀어가면서 빌드 진행
    * Dependent library 들을 하나씩 빌드하고 설치해가면서 진행
    * `libxml2, `
* awin 매크로(\__CYGWIN__)를 통한 플랫폼 환경 설정
  * AOS 빌드 시, Poo 의 ab 환경이라는 것 인식 (Win32 로 설정)
* Symbolize 라이브러리 빌드 에러 디버깅
  * ELF 매크로(\__ELF__) 의 설정이 되지 않아 소스가 제대로 빌드 되지 않음
    * ELF object format 을 사용하는 target 에 대해서 매크로가 정의됨
      * awin 의 output 이 ELF 가 아닌 exe 이기 때문에 설정 안되는 것으로 보임
  * 일단 symbolize_host 타겟은 빌드 안하고 무시하고 넘어감
* Unrecognized flag error
  * 일단 컴파일러는 gcc 와 cli 둘 간의 에러 내용이 다르기 때문에 cli 을 사용하기로 함 (cli 5.0.1)
  * Compilation flag 제거
* se/win/le.h 에서 문법 에러 해결
  * 원래 매크로 안에 에러를 발생시키는 부분이 '\\\\' 였으나 '\\' 로 변경
* MessagePump compile error
  * 헤더 파일에서는 Poo 와 관련된 코드를 사용하나, 소스 파일에서는 Unix 쪽 소스를 사용해서 생기는 에러
    * 사용될 소스가 매크로에 의해서 결정되는데, 매크로 기준이 다르다 보니 다른 소스가 사용됨
      * 헤더에서는 Poo, 소스에서는 POSIX 계열
    * 두 기준이 달라서, 잘 우회하기가 힘듬 (여러 다른 소스에서도 이런식으로 사용 중: twk, view, event, ...)
    * 확인 결과, USE_X11 매크로를 사용하기 때문에 POSIX 소스가 컴파일 된 것으로 확인
      * Base 에서 USE_X11 매크로가 사용된 것이 꼭 필요한 것인지, 원래 Fork 된 크로미움 코드에도 사용했는지 판단할 수가 없음
  * 올바르게 Poo 플랫폼 대상으로 빌드되게 하는 것이 어떤 방향인지 판단하기가 힘듬
* 현재 까지 완료
  * `se_static_host, allocator_extension_thunks_host, dynamic_annotations_host, xdg_mime_host`

[1]:https://www.daemon-systems.org/man/libutil.3.html
[2]:https://libevent.org/
[3]:http://www.xmlsoft.org/

# isdpt-notice-bot
~~나만 못봤어 공지사항~~

세종대학교 정보보호학과 홈페이지 공지사항 크롤링 후 알림 알려주는 디스코드 봇

> 세종대학교 정보보호학과 홈페이지 \
> http://home.sejong.ac.kr/~isdpt/

## Bot Permissions - 필수 권한
* 채널 보기 - View Channel
* 메시지 보내기 - Send Messages
* 링크 첨부 - Embed Links
* 메시지 관리 - Manage Messages
* 메시지 기록 보기 - Read Message History

## Installation
1. run.sh 스크립트를 `. ./run.sh`로 실행하면서 봇의 토큰을 인자로 넣어준다. \
`. ./run.sh asdf-bcde` \
\
(저렇게 실행하는 이유는 `run.sh` 내부에서 history 기록을 지움으로써 **history에 토큰이 남지 않게** 하는게 목적인데, 더 좋은 다른 방법이 있을 수 있다.)

## 사용법
의도된 사용 방법은 다음과 같다.

우선 해당 봇은 공지사항 전용 채널, 채용공고 전용 채널을 따로 만들어야 한다.

### 공지사항
* 봇하고 관리자만 채팅 칠 수 있는 채널 생성
  * 봇은 위에 말한 권한 추가
  * 외부인은 메시지 보기만 가능하게( 최소 권한 : View channel, Read message history )
  * 어드민이 채널에서 최초로 `!notice` 명령을 치면됨

### 채용공고
* 봇하고 관리자만 채팅 칠 수 있는 채널 생성
  * 봇은 위에 말한 권한 추가
  * 외부인은 메시지 보기만 가능하게( 최소 권한 : View channel, Read message history )
  * 어드민이 채널에서 최초로 `!job_opening` 명령을 치면됨


## TODO
* ~다른 게시판 크롤링 객체도 추가~
* ~`!notice` 에서 오류나면 채널 id가 클래스 변수에 고정되서 에러날 가능성이 있음, 클래스 변수에서 빼낼 수 있는 명령도 추가~
* ~봇도 `run` 내부에서 메시지 보낼때 채널이 존재하는지 확인하는 루틴 추가~
* 한번에 특정 채널 권한을 봇 전용 공간으로 만들 수 있게하는 명령어 제작( 채널에 Manage Roles, Manage Channels 추가되어야 할 듯 )
* selenium 사용해보기( 필요하다면 추가 )

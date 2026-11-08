# Slackbot 처음 만들기: 토큰부터 Socket Mode까지

테스트 업무에는 데이터 생성, 계정 초기화, 테스트 실행, 결과 확인 같은 반복 작업이 많습니다. Slackbot은 이런 절차를 찾고 반복하는 시간을 줄이는 데 유용합니다. 처음 설정할 때 헷갈리는 부분만 정리했습니다.

## 토큰 두 개를 구분하자

Slackbot에는 Bot Token(`xoxb-`)과 App-Level Token(`xapp-`)이 있습니다. Bot Token은 워크스페이스 안에서 메시지를 보내고 채널에 참여하는 권한이고, App-Level Token은 Socket Mode 같은 앱 전체 기능에 사용합니다. Socket Mode용 앱 토큰에는 `connections:write`, 예제의 멘션 수신과 답장용 봇 토큰에는 `app_mentions:read`와 `chat:write`가 필요합니다. scope와 토큰 종류는 [Slack 공식 문서](https://api.slack.com/scopes)에서 확인할 수 있으며, scope를 바꾸면 워크스페이스 재설치가 필요할 수 있습니다. 토큰은 코드에 넣지 말고 환경 변수로 읽으세요.

## Socket Mode를 선택한 이유

인터랙티브 메시지를 쓰려면 Slack이 사내 PC로 요청을 보내야 하는데, 보안상 직접 인바운드를 열기 어려울 때가 있습니다. Socket Mode는 공인 HTTP 엔드포인트 없이 아웃바운드 연결로 동작합니다. 대신 봇을 사용할 채널에 초대해야 메시지를 보낼 수 있습니다.

## 첫 실행

Bolt for Python으로 `app_mention` 이벤트를 처리하는 예제를 실행합니다. `Bolt app is running!`이 보이면 연결된 것입니다. 이벤트 핸들러가 없으면 터미널에 처리 방법이 제안되므로 로그를 보며 필요한 이벤트를 추가할 수 있습니다.

## 운영 팁

토큰은 비밀 관리 도구에 보관하고, 파괴적인 명령에는 확인 절차와 실행 이력을 남기세요. 채널 권한을 바꾼 뒤에는 재설치가 필요할 수 있습니다.

원문: [Slackbot 구축부터 활용까지 - 환경 설정하기](https://kimkitae.github.io/posts/setup-slackbot-initialization/)

업무 자동화 봇을 검토 중이라면 [iam@kimkitae.me](mailto:iam@kimkitae.me?subject=KFlowLabs%20Slackbot%20inquiry)로 문의해 주세요. 실제 토큰이나 채널 ID는 보내지 마세요.

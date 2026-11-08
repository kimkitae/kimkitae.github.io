# Slackbot 버튼 하나가 실제 업무를 실행할 때

Slackbot의 첫 실행은 어렵지 않습니다. 토큰 두 개를 발급하고 이벤트 하나를 처리하면 됩니다. 어려운 부분은 그다음입니다. 채널에 보이는 버튼은 권한이 아니고, Slack이 이벤트를 받았다는 사실은 작업이 끝났다는 뜻이 아닙니다.

## 토큰 두 개를 구분하자

- **Bot Token**(`xoxb-`): 워크스페이스 안에서 메시지를 보내고 채널에 참여하는 권한입니다. 예제의 멘션 수신과 답장에는 `app_mentions:read`, `chat:write`가 필요합니다.
- **App-Level Token**(`xapp-`): Socket Mode 연결 같은 앱 전체 기능에 사용합니다. `connections:write`가 필요합니다.

버튼과 모달을 쓰면 Interactivity를 켜야 하고, 그때 필요한 scope는 기능에 따라 다르므로 [Slack scope 문서](https://api.slack.com/scopes)에서 확인해야 합니다. scope를 바꾼 뒤에는 워크스페이스 재설치가 필요할 수 있습니다. 토큰은 코드에 넣지 말고 환경 변수나 비밀 관리 도구에서 읽으세요.

## Socket Mode는 연결 방식만 바꾼다

인터랙티브 메시지를 쓰려면 Slack이 사내 PC로 요청을 보내야 하는데, 보안상 인바운드를 열기 어려울 때가 있습니다. Socket Mode는 공인 HTTP 엔드포인트 없이 아웃바운드 WebSocket으로 동작합니다. 대신 연결 방식이 바뀔 뿐, 클릭한 사람이 그 업무를 실행할 권한이 있는지와 같은 요청이 두 번 실행돼도 되는지는 서버가 판단해야 합니다.

## ack는 완료가 아니다

Bolt 문서에 따르면 actions, commands, shortcuts, options, view submissions에는 ack가 필요하고, 보통 3초 안에 보내야 합니다. 이 3초는 작업을 끝내라는 시간이 아니라 요청을 받았다고 알려 주는 시간입니다. ack가 늦으면 사용자에게 오류가 보이고, 사용자가 다시 눌러 같은 작업을 두 번 시작할 수 있습니다([인터랙션 응답 문서](https://docs.slack.dev/interactivity/handling-user-interaction/)). HTTP Events API의 자동 전달 재시도는 별도 규칙이며 버튼 action에 그대로 적용하면 안 됩니다. Socket Mode의 전송 계층 수신 확인과도 구분해야 합니다.

서버는 클릭 하나를 다음 상태로 처리합니다. 실제 payload 필드 이름은 이벤트 종류와 Slack 버전에 따라 다르므로 구현 전에 문서를 확인하세요.

| 순서 | 상태 | 서버가 하는 일 |
|---|---|---|
| 1. 수신 | actor, channel, message `ts`, action id, target | 같은 작업을 식별할 operation id를 정한다. 예: 버튼 value에 서버가 발급한 ID |
| 2. 접수 | 3초 기한 | `ack()`로 접수만 알린다 |
| 3. 권한 | actor와 action/target | actor 허용 여부와 target/action 권한을 함께 확인한다 |
| 4. 중복 전달 | 같은 operation id | 새 실행 없이 기존 상태를 보여 준다 |
| 5. 더블클릭 | 같은 operation id | 4와 같은 경로로 묶는다 |
| 6. 의도적 재실행 | 새 operation id | 새 작업으로 접수한다 |
| 7. 실행·장애 | 작업 레코드, 큐, 워커 | 결과를 내구성 있게 저장하고 하류 작업을 멱등하게 만든다 |
| 8. 완료 | 결과 | `chat.update`로 같은 메시지를 갱신한다 |

중복 전달과 더블클릭은 같은 operation id로 묶지만, 나중의 의도적 재실행은 새 operation id여야 합니다. `SET NX`와 TTL 잠금만으로 exactly-once를 보장할 수는 없습니다. TTL 만료, 워커 크래시, 큐 전달 유실, 서로 다른 두 권한자가 같은 대상에 실행하는 경우가 남으므로 작업 결과 저장과 하류 멱등성, 상태 대조가 함께 필요합니다. 멱등 키의 범위는 워크스페이스·action·target을 포함해야 하며 actor만으로는 부족합니다. 이벤트는 SDK가 처리하므로 `app_mention` 핸들러에 수동 ack를 넣을 필요는 없지만, 버튼 action 핸들러는 ack를 명시해야 합니다.

## 버튼 노출과 실행 권한은 다르다

| 단계 | Slack이 보는 것 | 서버가 보장할 것 |
|---|---|---|
| 클릭 | action payload 도착 | 3초 안에 ack |
| 권한 | 누가 눌렀는지 | 그 사용자가 그 action과 target을 실행할 권한 |
| 중복 | 사용자 재클릭·더블클릭 가능 | 같은 operation id를 한 작업으로 묶는다. 크래시·TTL 만료·동시 실행은 별도 보장 필요 |
| 실행 | 아무것도 보이지 않음 | 작업 ID와 진행 상태 기록 |
| 완료 | 메시지 갱신 | 성공·실패를 사용자가 확인 |

버튼을 숨기는 것만으로는 부족합니다. 사용자는 다시 누르거나 오래된 메시지의 버튼을 누를 수 있으므로, 실행할 때마다 현재 권한을 확인해야 합니다. 원문에는 이런 승인 절차를 운영에 구현했다는 기록이 없습니다. 승인된 실행자와 대상별 실행 권한을 정하는 것은 지금의 설계 권고입니다.

## 상태를 보이게 만들기

오래 걸리는 작업은 작업 ID, 진행 상태(접수·실행 중·완료·실패), 실패 이유를 남겨야 합니다. `chat.update`로 같은 메시지를 갱신하면 채널이 지저분해지지 않고 실패도 같은 위치에서 확인할 수 있습니다. 작업 ID를 응답에 넣으면 문의가 왔을 때 로그를 바로 찾을 수 있습니다.

## 정리

토큰과 Socket Mode는 시작일 뿐입니다. 버튼이 상태를 바꾸는 순간 ack와 실행을 분리하고, 서버에서 권한을 확인하고, 중복 실행을 막고, 결과를 같은 메시지에 남기는 구조가 필요합니다.

원문: [Slackbot 구축부터 활용까지 - 환경 설정하기](https://kimkitae.github.io/posts/setup-slackbot-initialization/)

업무 자동화 봇을 검토 중이라면 [iam@kimkitae.me](mailto:iam@kimkitae.me?subject=KFlowLabs%20Slackbot%20inquiry)로 문의해 주세요. 실제 토큰이나 채널 ID는 보내지 마세요.

---
title: SlackBot 구축부터 활용까지 - 환경 설정하기
author: KimKitae
date: 2024-09-25 12:00:00 +9000
categories: [Automation, SlackBot]
tags: [SlackBot]
pin: true
---

많은 기업들이 Slack을 이용하여 업무를 진행하고 있습니다. Slack은 다양한 앱과 통합 기능을 지원하여 팀의 커뮤니케이션과 협업을 더욱 효율적으로 만들어 줍니다. 그중에서도 Slackbot은 업무 프로세스를 자동화하고 편의성을 높이는 데 큰 역할을 합니다.

저는 지난 5년 동안 Slackbot을 구축하고 운영해왔습니다. 그 경험을 통해 업무 효율성이 크게 향상되는 것을 느꼈지만, 주변에서는 Slackbot을 만드는 것을 어렵게 생각하는 분들이 많았습니다. 그래서 이번 블로그 시리즈를 통해 Slackbot의 최초 설정부터 간단한 사용 예제까지, 누구나 따라 할 수 있도록 단계별로 정리해보려고 합니다.

---

# SlackBot이란 무엇인가?

Slackbot은 다음과 같은 특징을 갖고 있습니다:
- **자동화:** 반복적인 업무를 자동으로 처리하여 시간을 절약합니다.
- **실시간 대응:** 즉각적인 반응으로 업무 흐름을 원활하게 유지합니다.
- **커스터마이징:** 팀의 필요에 따라 기능을 자유롭게 확장할 수 있습니다.

# 업무 효율성에 미치는 영향
Slackbot은 업무 프로세스의 자동화를 통해 팀의 생산성을 향상시킵니다. 제 개인적인 경험을 공유하자면, 테스트 업무를 수행하는 데 있어 Slackbot을 적극 활용했습니다.

## 업무에서의 Slackbot 활용

업무 중에는 데이터의 생성, 변경, 삭제, 테스트 수행, 결과 확인 등 반복적인 작업이 자주 필요했습니다. 초기에는 이러한 작업을 수동으로 처리했기 때문에 시간이 많이 소요되었고, 빈도가 낮은 작업의 경우 절차를 잊어버려 다시 가이드를 찾아야 했습니다. 또한 타 부서에서 방법을 물어오면 매번 답변해드려야 하는 번거로움도 많았습니다.

이를 개선하기 위해 Slackbot을 도입하여 다음과 같은 기능을 구현했습니다:

- **데이터 생성 및 관리 자동화:** Modal View를 이용하여 GUI를 통해 사용자가 필요한 기능 선택, 정보 입력하여 쉽게 데이터를 생성 및 관리 할 수 있도록 하였습니다.
- **테스트 수행 명령어:** Slack에서 바로 명령어를 이용하여 테스트를 수행하거나, Message를 분석하여, 필요한 테스트가 자동 수행되도록 하였습니다.
- **결과 알림:** 테스트 완료 후 결과를 자동으로 요약하여 각 채널로 전달했습니다.

이후에는 이 Slackbot을 본부 내 모든 사람들이 사용할 수 있도록 서비스화했습니다. **그 결과:**

- **시간 절약:** 자동화된 프로세스로 작업 시간이 단축됩니다.
- **팀 협업 강화:** 모든 팀원이 동일한 도구와 프로세스를 사용하여 일관성을 유지합니다.
- **신속한 의사소통:** 실시간 알림과 응답으로 어붐 흐름이 빨라집니다.
- **절차 간소화:** 복잡한 절차 없이도 필요한 작업을 즉시 수행할 수 있었습니다.
- **업무 효율성 향상:** 반복적인 수작업이 줄어들어 중요한 업무에 더 많은 시간을 투자할 수 있었습니다.

실제 업무에서 Slackbot을 통해 다양한 기능을 제공하였습니다. **일부 예를 들어:**

- **본인 인증 횟수 초기화:** 간단한 명령으로 인증 시도 횟수를 초기화하여 테스트를 원활하게 진행할 수 있었습니다.
- **계정 고유 식별 값 검색:** 계정의 고유 식별 값을 빠르게 조회하여 작업 효율을 높였습니다.
- **포인트 충전 및 계정 관리:** Slackbot을 통해 포인트를 충전하거나 계정을 생성/삭제하는 등의 계정 관리가 간편해졌습니다.
- **주문 처리 자동화:** 사용자 측의 주문 완료부터 사장님 측의 주문 수락까지의 프로세스를 자동화하여 업무 시간을 절약했습니다.
- **테스트 자동화 수행:** 리그레션 테스트와 자동화 테스트를 실행하고 결과를 채널에 공유하여 팀원들과 실시간으로 협업했습니다.

이러한 기능들을 통해 팀원들은 복잡한 절차 없이 필요한 작업을 즉시 수행할 수 있었고, 중요한 업무에 더 많은 시간을 투자할 수 있었습니다. 결과적으로 Slackbot은 업무 효율성을 크게 향상시키는 도구로 자리매김하였습니다.

---

# Slackbot 생성하기

1. [Your Apps](https://api.slack.com/apps)에 접속하여 `Create New App`을 선택, `From a manifest` 또는 `From scratch`를 선택하여 생성 합니다.
![Slackbot 신규 생성](https://github.com/user-attachments/assets/aaaba703-759b-4fd7-a65b-c52cdf49c5bd)
![Create an app](https://github.com/user-attachments/assets/8b233de9-34e6-4915-b4df-92a950f5dba7)
- manifest 파일에 익숙하시다면 `From a manifest`, 직접적인 UI를 통해 설정을 하실려면 `From scratch` 를 선택합니다.

2. `App-Level Token`을 생성하며, 필요한 권한을 추가 합니다. 이후 생성된 Token 값을 메모해 둡니다.
 
![App-Level Token](https://github.com/user-attachments/assets/aec07586-9552-4b29-b63f-0a2e14f56c4e)

---

# 상세 설정 하기
Slack은 Web API, Events API, Socket Mode 등 다양한 API를 제공합니다.

기존에는 웹 서버 형태로 Real Time Messaging(RTM)을 이용하여 Slackbot을 운영해보았습니다. 하지만 **인터랙티브 메시지(Interactive Message)**를 사용하기 위해서는 Slack을 통해 사용자의 요청이 사내 구동 PC로 전달되어야 했습니다. 그러나 보안상의 이유로 사내망으로의 직접적인 요청 전달이 불가능하였습니다.

이러한 문제를 해결하기 위해 Socket Mode로 전환하였습니다. Socket Mode를 사용하면 Public HTTP Request URL을 노출하지 않고도 사내망의 PC와 연결할 수 있어, 보안을 유지하면서도 필요한 기능을 구현할 수 있었습니다.

저의 예제에서는 보안성과 편의성을 고려하여 Socket Mode를 이용하도록 하겠습니다.

1. **Socket Mode** 를 활성화 합니다. (각 Features 상세 설정 내용은 다음 포스트에 정리하겠습니다.)
![Socket mode 활성화](https://github.com/user-attachments/assets/4a35d4be-4982-47f0-8cad-be2d701b36f3)
- Interactivity & Shortcuts - 상호작용이 가능한 Components, Shortcuts, Modal 기능 활성화
- Slash Commands - `/`를 이용한 커맨드 호출 기능 활성화
- Event Subscriptions - 특정 형태의 이벤트 구독 기능 활성화 

![Event Subscriptions 설정](https://github.com/user-attachments/assets/108f694c-fc20-4fcd-bad6-1fbe9eb51816)
- 이번 예제를 위해 `app_mention` 권한 추가 합니다. 해당 권한은 Slack 채널에서 @bot 호출에 대한 Event를 인지 할 수 있도록 해줍니다. (`app_home_opened`는 Bot의 홈 화면 진입 시 발생하는 이벤트 입니다.)


2. `Install App`을 통해 워크스페이스 Bot을 설치하여 `Bot Token` 을 확인합니다.
![Install Bot](https://github.com/user-attachments/assets/3ddefd96-b83c-4257-bd99-3c54c746cc07)


![Bot Token](https://github.com/user-attachments/assets/6d607fe3-5563-4a55-9b8d-6d902a7bb144)

- #### Bot Token 생성 전 필요한 설정을 모두 완료 후 워크스페이스에 설치해주시면 됩니다.
- #### Bot Token 생성 후 권한에 변화가 있을 때마다 `Reinstall to` 를 이용해 워크스페이스 재 설치가 필요 합니다. 
![Select Channel](https://github.com/user-attachments/assets/965301d8-46b8-469b-9050-abb03fe6491e)


![Invited Bot](https://github.com/user-attachments/assets/2d0463c9-91ad-423d-a236-f65f5b5070e0)
- 메세지 전달와 같은 동작을 위해선 해당 채널에 봇이 초대 되어 있어야 합니다.
---

# Slackbot 실행하기
[Bolt for Python](https://api.slack.com/tools/bolt-python) 프레임워크를 이용하게 되면 보다 쉽게 Slack App 구현이 가능합니다. Python 외에는 JavaScript, Java를 지원 합니다.

`Bolt for Python`를 이용하여 실행 예제를 만들어보도록 합니다.


개발 환경은 `python 3.12.0` 버전이며 설치 필요한 모듈은 아래와 같습니다.
```zsh
pip install slack-bolt
pip install aiohttp
```

`main.py`파일 생성하여 아래의 코드를 붙여넣습니다.
```python
import asyncio
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler

#Bot Token은 xoxb- 로 시작하며 App Token은 xapp-1로 시작
SLACK_BOT_TOKEN="xoxb-..."
APP_TOKEN="xapp-1-..."

# 비동기 Slack 앱
app = AsyncApp(token=SLACK_BOT_TOKEN)


# 'app_mention' 이벤트를 처리하는 비동기 핸들러
@app.event("app_mention")
async def handle_app_mention(event, say):
    await say(f"Hello, <@{event['user']}>!")  # 비동기 핸들러에서는 await 사용


# 비동기 SocketModeHandler 시작
async def main():
    handler = AsyncSocketModeHandler(app, APP_TOKEN)
    await handler.start_async()

if __name__ == "__main__":
    asyncio.run(main())  # 비동기 메인 함수 실행
```

- 아래의 명령어를 통해 위 코드를 실행 합니다.
```zsh
python main.py
```
- `Bolt app is running!`이 보였다면 Slackbot이 정상적으로 실행되고 있는 상태 입니다.

![Terminal](https://github.com/user-attachments/assets/949998b4-0a77-45c2-8207-780823c10796)

- `@app.event`의 `app_mention` 이벤트 발생 시 `handle_app_mention`함수가 수행이 됩니다.
![](https://github.com/user-attachments/assets/4c911819-9836-453e-a25c-de03a321b155)

- `@app.event`를 이용하여 `message`, `app_home_opened` 등 다양한 이벤트들에 대한 동작을 정의할 수 있습니다. 

- 터미널을 통해 아래와 같이 로그를 볼 수 있어, 이벤트가 발생했는데 정의되지 않은 부분에 대해서 제안까지 제공하고 있습니다.

```python
Unhandled request ({'type': 'event_callback', 'event': {'type': 'message'}})
---
[Suggestion] You can handle this type of event with the following listener function:

@app.event("message")
async def handle_message_events(body, logger):
    logger.info(body)

Unhandled request ({'type': 'event_callback', 'event': {'type': 'message'}})
---
[Suggestion] You can handle this type of event with the following listener function:

@app.event("message")
async def handle_message_events(body, logger):
    logger.info(body)
```
---

[Slackbot-sample](https://github.com/kimkitae/slackbot-sample) 를 사용하면 Docker를 통해 간단히 Slackbot을 실행해 볼 수 있습니다. 복잡한 설정 없이 명령어 몇 개만 입력하면 바로 실행할 수 있도록 준비된 예제가 포함되어 있어, 처음 사용하시는 분들도 쉽게 따라 하실 수 있습니다.(향후 추가되는 블로그 내용 내 예제들도 지속적으로 추가 예정)

위의 예제 코드를 보면 비동기(asyncio) 방식을 사용하여 Slackbot을 구현하였습니다. 왜 동기 방식이 아닌 비동기 방식으로 구현했는지, 그리고 이러한 선택이 어떤 이점을 가져오는지 설명해드리겠습니다.

**비동기 프로그래밍을 선택한 이유**
1. **효율적인 I/O 처리**
Slackbot은 여러 사용자의 메시지와 이벤트를 실시간으로 처리해야 합니다. 동기 방식으로 구현할 경우 하나의 요청을 처리하는 동안 다른 요청은 대기해야 하므로 응답 속도가 느려질 수 있습니다. 반면에 비동기 프로그래밍을 사용하면 동시에 여러 요청을 효율적으로 처리할 수 있어 성능이 향상됩니다.

2. **서버 자원 최적화**
비동기 방식은 이벤트 루프를 통해 비차단식(non-blocking)으로 작업을 처리합니다. 이를 통해 서버의 CPU 및 메모리 사용량을 최적화할 수 있으며, 더 적은 자원으로 더 많은 요청을 처리할 수 있습니다.

3. **향후 확장성 고려**
프로젝트 규모가 커지거나 처리해야 할 요청이 많아질 경우 비동기 방식은 확장성 측면에서 유리합니다. 초기부터 비동기 구조로 설계하면 추후 기능 추가나 성능 개선이 용이합니다.


비동기 방식은 이벤트 루프라는 메커니즘을 통해 작업을 동시에 처리할 수 있도록 도와줍니다. 비차단식(non-blocking) 이라는 개념은, `어떤 작업이 끝날 때까지 기다리지 않고 바로 다른 작업을 처리`할 수 있다는 의미입니다.

쉽게 설명하면, 서버가 요청을 처리할 때 비동기 방식은 이렇게 동작합니다:

- 일반적으로 요청이 들어오면, 서버는 그 요청을 처리하는 동안 다른 일을 못 하고 기다려야 합니다.
- 하지만 비동기 방식에서는 요청이 처리되는 동안 기다릴 필요 없이 다른 요청을 바로 처리할 수 있습니다.

예를 들어:

- 서버가 파일을 읽거나 외부 서비스에 데이터를 요청할 때, 그 작업이 끝날 때까지 기다리지 않고 바로 다른 작업을 진행할 수 있습니다.

이 방식 덕분에 서버는 CPU와 메모리를 효율적으로 사용할 수 있으며, 더 적은 자원으로도 더 많은 요청을 동시에 처리할 수 있게 됩니다.

*비유하자면, 일반 방식은 한 번에 한 가지 일만 처리하는 사람이고, 비동기 방식은 여러 가지 일을 동시에 조율하는 사람과 비슷합니다.*

### Slackbot에서 사용되는 토큰(Token) 종류
Slackbot에서는 두 가지 종류의 토큰을 사용합니다:

-  **Bot Token**
    - 설명: Bot Token은 Slack 앱 내에 설치된 봇이 Slack 워크스페이스에서 동작하기 위한 권한을 정의하는 토큰입니다.
    - 역할: 봇은 사용자가 설치한 Slack 워크스페이스 내에서 메시지를 보내거나 채널에 참여하고, 이벤트를 구독하는 등 Slack의 다양한 기능을 활용할 수 있습니다. 이 때 Bot Token은 해당 봇이 이러한 작업을 수행하는 데 필요한 권한을 제공합니다.

    - 용도:
        - 메시지 보내기/받기
        - 채널 참여
        - 사용자의 명령을 받아 처리하기
        - 앱과 상호작용하기 위한 권한

    - 예시: 사용자가 Slack에서 /weather 명령어를 입력하면, 날씨 정보를 제공하는 봇이 해당 명령을 처리하는데 필요한 권한을 Bot Token을 통해 얻게 됩니다.

- **App-Level Token**
    - 설명: App-Level Token은 Slack 앱이 설치된 여러 인스턴스(혹은 모든 인스턴스)에 대해 플랫폼 기능을 사용할 수 있도록 하는 토큰입니다. 이 토큰은 Bot Token과 달리 특정 봇의 역할과는 관련이 없으며, 앱 전체의 기능과 관련된 토큰입니다.
    - 역할: App-Level Token은 특히 Slack의 Event Subscriptions API와 같은 기능에서 앱이 설치된 워크스페이스에 대한 글로벌 권한을 허용하는 데 사용됩니다.
        - 예를 들어, 앱이 워크스페이스 전체에 대한 이벤트를 관리하거나, 앱 자체의 설정을 변경할 때 필요한 권한을 제공합니다.
    - 용도:
        - 앱 구성 관리: 앱 설정이나 구성 정보를 읽거나 쓸 수 있는 권한
        - 연결 관리: 다양한 워크스페이스에 대해 연결 설정을 변경하거나 관리하는 권한
        - 이벤트 권한: 여러 워크스페이스에 걸쳐 이벤트를 구독하고 처리하는 데 사용

- **차이점**
    - Bot Token은 봇이 워크스페이스 내에서 작동하기 위해 필요한 권한을 제공하며, 특정 봇의 동작에 초점을 맞춥니다.
    - App-Level Token은 앱 전체가 Slack 플랫폼 기능을 사용하기 위한 권한을 제공하며, 워크스페이스나 설치 인스턴스 간의 관리와 관련된 전역적인 권한을 제공합니다.

---
이번 포스트에서는 Slackbot의 생성부터 기본적인 실행까지의 과정을 살펴보았습니다. 다음 포스트에서는 각 Features의 상세 설정과 복잡한 기능 구현에 대해 다뤄보겠습니다. 감사합니다.

연관링크 - [SlackBot 내 LLM을 통한 자동 스크립트 생성](https://kimkitae.github.io/posts/quick-start-rag-and-llm-for-automation/)
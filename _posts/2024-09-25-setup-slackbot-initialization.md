---
title: Slackbot 구축부터 활용까지 - 환경 설정하기
author: KimKitae
date: 2024-09-25 12:00:00 +0900
last_modified_at: 2026-11-08
description: Slack 앱 생성, Socket Mode 설정, Bolt for Python으로 첫 봇을 실행하는 과정과 토큰 관리 주의점을 정리합니다.
categories: [Automation, SlackBot]
tags: [SlackBot]
translation_url: /en/posts/setup-slackbot-initialization/
pin: true
---

Slackbot은 반복 업무를 줄이는 데 효과적이지만, 처음 설정할 때 필요한 단계가 많아 어렵게 느껴질 수 있습니다. 이 글은 앱 생성부터 첫 실행까지를 한 번에 정리합니다. 운영 환경의 토큰은 절대 코드에 넣지 말고, 환경 변수나 비밀 관리 도구를 사용하세요.

![Slack 앱 생성, 토큰 발급, Socket Mode 연결, Bolt 실행으로 이어지는 설정 흐름](/assets/img/posts/renewal/setup-slackbot-initialization.svg)

*그림 1. Slackbot을 처음 만들 때 거치는 설정 순서. Bot Token과 App-Level Token의 역할이 다릅니다.*

## Slackbot이 유용한 이유

테스트 업무에서는 데이터 생성, 계정 초기화, 테스트 실행, 결과 확인 같은 반복 작업이 자주 생깁니다. 처음에는 수동으로 처리했지만, 빈도가 낮은 작업은 절차를 잊어버리기 쉽고, 다른 팀에서 방법을 물어올 때마다 같은 설명을 반복해야 했습니다.

Slackbot으로 Modal View를 제공하면 필요한 값을 폼으로 입력받아 안전하게 작업을 실행할 수 있습니다. 명령어로 테스트를 실행하고, 결과를 채널에 요약해 공유하는 것도 가능합니다. 핵심은 “사람이 하던 절차를 없애는 것”이 아니라 “절차를 찾고 반복하는 시간을 줄이는 것”입니다.

## 앱 생성과 토큰

1. [Slack API](https://api.slack.com/apps)에서 `Create New App`을 선택합니다.
2. `From scratch`로 만들거나, manifest 파일이 있다면 `From a manifest`를 사용합니다.
3. `App-Level Token`을 생성하고 `connections:write` scope를 추가합니다. 이 토큰은 `xapp-`로 시작합니다.
4. `Install App`으로 워크스페이스에 설치한 뒤 `Bot Token`(`xoxb-`)을 확인합니다. 예제의 `app_mention` 이벤트와 답장을 위해 Bot Token에는 `app_mentions:read`와 `chat:write`가 필요합니다.

Bot Token은 워크스페이스 안에서 봇이 메시지를 보내고 채널에 참여하는 권한입니다. App-Level Token은 앱 전체 수준에서 Socket Mode 같은 기능을 사용하기 위한 토큰입니다. 두 토큰을 같은 것으로 취급하면 권한 오류가 나기 쉽습니다. scope를 바꾼 뒤에는 워크스페이스에 다시 설치해야 할 수 있습니다. 공식 문서는 [Socket Mode](https://api.slack.com/apis/socket-mode), [토큰 종류](https://api.slack.com/authentication/token-types), [`connections:write`](https://api.slack.com/scopes/connections:write), [`app_mentions:read`](https://api.slack.com/scopes/app_mentions:read), [`chat:write`](https://api.slack.com/scopes/chat:write)에서 확인할 수 있습니다.

토큰을 코드에 직접 쓰지 말고 다음처럼 환경 변수로 읽습니다.

```python
import os

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
```

## Socket Mode를 선택한 이유

예전에는 웹 서버를 열고 RTM으로 봇을 운영했습니다. 하지만 인터랙티브 메시지를 사용하려면 Slack의 요청이 사내 PC로 들어와야 하고, 보안 정책상 외부에서 사내망으로 직접 요청을 보내는 것이 어려웠습니다.

Socket Mode는 공인 HTTP 엔드포인트를 열지 않고도 Slack과 연결할 수 있습니다. 사내망에서 아웃바운드 연결을 허용할 수 있다면, 별도의 리버스 프록시 없이 봇을 운영할 수 있다는 장점이 있습니다.

앱 설정에서 다음 기능을 활성화합니다.

- **Socket Mode**: 앱과 Slack의 WebSocket 연결
- **Interactivity & Shortcuts**: 버튼, 모달, 단축키
- **Slash Commands**: `/` 명령어
- **Event Subscriptions**: `app_mention` 등 이벤트 구독

메시지를 보내려는 채널에는 봇을 초대해야 합니다. 이 단계를 빠뜨리면 “not_in_channel” 오류가 납니다.

## Bolt for Python으로 실행하기

Bolt는 Slack 앱 개발을 단순화하는 프레임워크입니다. Python 3.12 환경에서 `slack-bolt`와 `aiohttp`를 설치한 뒤, 아래 예제를 실행합니다.

```bash
pip install slack-bolt aiohttp
```

```python
import asyncio
import os
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_mention")
async def handle_app_mention(event, say):
    await say(f"Hello, <@{event['user']}>!")

async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()

if __name__ == "__main__":
    asyncio.run(main())
```

`Bolt app is running!`이 보이면 연결된 것입니다. 채널에서 봇을 멘션해 응답이 오는지 확인합니다. 이벤트가 발생했는데 핸들러가 없으면 Bolt가 터미널에 처리 방법을 제안해 주므로, 로그를 보며 필요한 이벤트를 추가할 수 있습니다.

## 비동기 실행과 운영 팁

Slackbot은 여러 사용자의 이벤트를 동시에 처리합니다. 동기 방식으로 작성하면 한 요청이 끝날 때까지 다른 요청이 기다려야 합니다. `AsyncApp`과 `AsyncSocketModeHandler`를 사용하면 I/O 대기 중 다른 이벤트를 처리할 수 있어, 적은 자원으로도 응답성을 유지하기 쉽습니다.

운영에서는 다음을 권합니다.

- 토큰은 환경 변수 또는 비밀 관리 도구에 보관
- 봇이 실행할 수 있는 명령의 범위를 명시
- 파괴적인 작업은 확인 절차를 두고, 실행 이력을 남김
- 채널 초대와 권한 변경 후에는 재설치 필요 여부 확인

예제 저장소는 [slackbot-sample](https://github.com/kimkitae/slackbot-sample)에 있습니다. Docker로 실행하는 방법도 포함되어 있지만, 저장소의 최신 README를 기준으로 확인하세요. 이 글은 초기 설정에 집중했고, Modal View와 각 이벤트의 상세 구현은 다음 글에서 다룰 수 있습니다.

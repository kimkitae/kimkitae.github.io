---
title: Mobile MCP로 시작하는 모바일 테스트 자동화 - Cursor와 Claude Desktop 연결하기
author: KimKitae
date: 2025-07-15 12:00:00 +0900
last_modified_at: 2026-11-08
description: MCP 기반 모바일 자동화 도구를 Cursor와 Claude Desktop에 연결하고, 시뮬레이터·에뮬레이터에서 확인하는 과정을 정리합니다.
categories: [Automation, MobileTest]
tags: [Mobile-MCP, MCP, Cursor, Claude, Appium, 모바일테스트]
translation_url: /en/posts/mobile-mcp-setup-guide/
pin: true
---

MCP(Model Context Protocol)는 AI 도구가 외부 시스템과 도구를 호출할 수 있게 해 주는 규약입니다. 이 글은 MCP 기반 모바일 자동화 서버를 Cursor와 Claude Desktop에 연결하고, iOS 시뮬레이터와 Android 에뮬레이터에서 동작을 확인하는 과정을 정리합니다. 자연어로 테스트를 실행할 수 있다는 가능성은 흥미롭지만, 아직 안정성과 재현성을 검증 중인 영역이라는 점을 전제로 읽어 주세요.

![AI 클라이언트, MCP 서버, iOS/Android 단말 사이의 연결 구조](/assets/img/posts/renewal/mobile-mcp-setup-guide.svg)

*그림 1. Cursor나 Claude Desktop이 MCP 서버를 통해 단말의 접근성 정보와 조작 명령을 주고받는 구조.*

## MCP가 하는 일

MCP 서버는 AI 클라이언트에 도구 목록을 제공하고, 클라이언트가 도구를 호출하면 실제 작업을 수행합니다. 모바일 자동화에서는 화면의 접근성 스냅샷을 읽고, 요소를 나열하고, 탭·입력·스크린샷 같은 동작을 실행하는 도구가 제공됩니다. Appium처럼 세션과 셀렉터를 직접 관리하지 않아도 된다는 점이 장점입니다.

반대로 모든 앱에서 동일하게 동작한다고 가정하면 안 됩니다. 접근성 레이블이 없거나 WebView가 많은 화면에서는 요소 식별이 어려울 수 있고, 좌표 기반 탭은 해상도에 민감합니다. 자동화의 재현성이 필요한 회귀 테스트에는 아직 보조 수단으로 쓰는 편이 안전합니다.

## 사전 준비

- **Node.js**: 서버 실행에 필요합니다. LTS 버전을 권장합니다.
- **Xcode Command Line Tools**: iOS 시뮬레이터와 빌드 도구.
- **Android Studio + Platform Tools**: `adb`와 에뮬레이터.
- **AI 클라이언트**: Cursor 또는 Claude Desktop.

```bash
node --version
xcode-select -p
adb version
```

패키지 이름과 CLI 옵션은 배포 상태에 따라 달라질 수 있습니다. 설치 전에 [Mobile MCP 저장소](https://github.com/mobile-next/mobile-mcp)와 npm 패키지 페이지의 현재 안내를 확인하고, 설치 후 실제로 해석된 버전을 기록하세요. 아래 설정은 `@latest`를 사용하지만, 그 값이 가리키는 버전은 시점에 따라 달라지므로 재현성이 필요하면 실행 환경에서 확인한 버전을 별도로 남기는 편이 좋습니다. MCP 자체의 규약은 [공식 문서](https://modelcontextprotocol.io/)에서 확인할 수 있습니다.

## Cursor 설정

Cursor는 사용자 설정 디렉터리의 `mcp.json`에서 MCP 서버를 등록합니다.

```bash
mkdir -p ~/.cursor
```

```json
{
  "mcpServers": {
    "mobile-mcp": {
      "command": "npx",
      "args": ["-y", "@mobilenext/mobile-mcp@latest"]
    }
  }
}
```

저장 후 Cursor를 완전히 종료했다가 다시 실행합니다. 서버가 목록에 보이지 않으면 명령을 터미널에서 직접 실행해 오류 메시지를 확인하세요.

## Claude Desktop 설정

macOS 기준 설정 파일은 `~/Library/Application Support/Claude/claude_desktop_config.json`입니다. 같은 형식으로 서버를 추가합니다.

```json
{
  "mcpServers": {
    "mobile-mcp": {
      "command": "npx",
      "args": ["-y", "@mobilenext/mobile-mcp@latest"]
    }
  }
}
```

저장 후 Claude Desktop을 재시작합니다. 기존 설정이 있다면 `mcpServers` 객체를 합치는 방식으로 편집하고, JSON 문법 오류가 없는지 확인하세요.

## 단말 연결

iOS 시뮬레이터는 `xcrun simctl`로 확인하고 부팅합니다.

```bash
xcrun simctl list devices
xcrun simctl boot "iPhone 16"
open -a Simulator
```

Android 에뮬레이터는 다음처럼 실행합니다.

```bash
emulator -list-avds
emulator -avd Pixel_7_API_34
adb devices
```

실제 단말을 사용할 때는 iOS의 경우 신뢰 설정, Android의 경우 USB 디버깅을 활성화해야 합니다. 회사 정책상 허용된 테스트 단말만 사용하세요.

## 실제 확인 예시

연결이 되면 AI 클라이언트에 다음과 같이 요청할 수 있습니다.

```text
사용 가능한 모바일 디바이스와 실행 중인 시뮬레이터를 확인해줘.
현재 화면의 UI 요소를 나열하고, 설정 앱의 "일반" 메뉴로 이동해줘.
```

응답에 표시되는 기기 이름과 화면 요소가 실제와 맞는지 확인하세요. 자동화를 신뢰하기 전에 수동으로 같은 동작을 재현해 보고, 실패했을 때 어떤 정보가 남는지 확인하는 것이 중요합니다. 자연어 명령은 편리하지만, 같은 명령이 항상 같은 결과를 내는지는 별개의 문제입니다.

## 한계와 정리

이 방식은 탐색적 테스트, 빠른 화면 확인, 반복 입력에는 유용합니다. 반면 결제·인증처럼 보안이 중요한 흐름이나 정밀한 회귀 검증에는 아직 부족합니다. 운영에 도입한다면 도구 호출 로그, 실패 스크린샷, 재현 가능한 시나리오를 남기는 구조를 먼저 만들고, Appium이나 네이티브 테스트와 역할을 나누는 편이 현실적입니다. 이 글의 패키지 이름과 명령은 작성 시점의 정보를 바탕으로 한 예시이며, 설치 전 최신 문서를 확인해야 합니다.

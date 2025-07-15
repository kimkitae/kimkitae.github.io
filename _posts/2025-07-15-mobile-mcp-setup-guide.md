---
title: Mobile-MCP로 시작하는 모바일 테스트 자동화 - Cursor와 Claude Desktop 연결하기
author: KimKitae
date: 2025-07-15 12:00:00 +9000
categories: [Automation, MobileTest]
tags: [Mobile-MCP, MCP, Cursor, Claude, Appium, 모바일테스트]
pin: true
---

최근 AI 기술의 발전으로 개발 생산성이 크게 향상되고 있습니다. 특히 MCP(Model Context Protocol)의 등장으로 Claude, Cursor 같은 AI 도구들이 외부 시스템과 직접 연동할 수 있게 되었습니다. 오늘은 Mobile Next MCP를 이용해서 모바일 앱 테스트를 자동화하는 방법을 초보자도 쉽게 따라할 수 있도록 단계별로 설명해드리겠습니다.

---

# Mobile Next MCP란 무엇인가?

Mobile Next MCP Server는 MCP(Model Context Protocol)를 기반으로 한 차세대 모바일 테스트 자동화 도구입니다. 기존의 복잡한 프레임워크 대신 **접근성 스냅샷(accessibility snapshots)**을 활용하여 AI와 모바일 디바이스를 연결해주는 혁신적인 도구입니다.

## Mobile Next MCP의 주요 특징

- **AI 친화적**: Claude, Cursor 같은 AI 도구와 자연스럽게 연동
- **플랫폼 독립적**: iOS와 Android 모두 하나의 인터페이스로 지원
- **빠르고 가벼움**: 네이티브 접근성 트리를 활용하여 빠른 실행
- **시각적 분석**: 화면에 실제로 렌더링된 내용을 분석하여 적절한 동작 결정
- **구조화된 데이터**: 화면에 보이는 모든 정보를 체계적으로 추출 가능
- **자연어 명령**: 복잡한 코드 대신 자연어로 테스트 시나리오 작성

---

# 사전 준비사항

Mobile Next MCP를 사용하기 전에 다음 도구들이 설치되어 있어야 합니다.

## 1. 필수 소프트웨어 설치

### Node.js 설치
```bash
# Node.js 최신 LTS 버전 설치 (공식 웹사이트에서 다운로드)
node --version  # 설치 확인
```

### iOS 개발 도구 설치 (iOS 테스트용)
```bash
# Xcode command line tools 설치
xcode-select --install

# 설치 확인
xcode-select -p
```

### Android 개발 도구 설치 (Android 테스트용)
```bash
# Android Studio 설치 후 Platform Tools 설정
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools

# ADB 설치 확인
adb version
```

## 2. AI 도구 설치

- **Cursor**: [공식 웹사이트](https://cursor.sh)에서 다운로드
- **Claude Desktop**: [Anthropic 웹사이트](https://claude.ai/download)에서 다운로드

---

# Mobile Next MCP 설치하기

## 1. NPM을 통한 설치

```bash
# Mobile Next MCP 설치
npm install -g @mobilenext/mobile-mcp@latest
```

## 2. 설치 확인

```bash
# 설치 확인 (실행 테스트)
npx @mobilenext/mobile-mcp@latest --help
```

---

# Cursor에서 Mobile Next MCP 설정하기

## 1. MCP 서버 설정 파일 생성

Cursor에서 Mobile Next MCP를 사용하려면 설정 파일을 만들어야 합니다.

### macOS/Linux의 경우:
```bash
# 설정 디렉토리 생성
mkdir -p ~/.cursor

# 설정 파일 생성
touch ~/.cursor/mcp.json
```

### Windows의 경우:
```bash
# 설정 디렉토리 생성
mkdir %USERPROFILE%\.cursor

# 설정 파일 생성
type nul > %USERPROFILE%\.cursor\mcp.json
```

## 2. mcp.json 파일 설정

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

## 3. Cursor 재시작

설정 파일을 저장한 후 Cursor를 완전히 종료하고 다시 실행합니다.

---

# Claude Desktop에서 Mobile Next MCP 설정하기

## 1. Claude Desktop 설정 파일 위치

### macOS:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Windows:
```
%APPDATA%\Claude\claude_desktop_config.json
```

## 2. 설정 파일 편집

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

## 3. Claude Desktop 재시작

설정을 저장한 후 Claude Desktop을 재시작합니다.

---

# 디바이스 연결 및 준비

## 1. iOS 시뮬레이터 설정

```bash
# 사용 가능한 시뮬레이터 목록 확인
xcrun simctl list

# 시뮬레이터 부팅
xcrun simctl boot "iPhone 16"

# 시뮬레이터 앱에서 확인
open -a Simulator
```

## 2. Android 에뮬레이터 설정

```bash
# 에뮬레이터 목록 확인
emulator -list-avds

# 에뮬레이터 실행
emulator -avd Pixel_7_API_34

# 또는 Android Studio에서 직접 실행
```

## 3. 실제 디바이스 연결

### iOS 디바이스:
- USB로 Mac에 연결
- "이 컴퓨터를 신뢰하시겠습니까?" 승인
- Xcode에서 디바이스 인식 확인

### Android 디바이스:
```bash
# USB 디버깅 활성화 후 연결
adb devices

# 디바이스가 목록에 나타나는지 확인
```

---

# 실제 사용 예제

## 1. 디바이스 연결 확인

먼저 연결 가능한 디바이스가 있는지 확인해봅시다.

```
사용 가능한 모바일 디바이스나 시뮬레이터를 확인해줘
```

AI 응답 예시:
- iPhone 16 시뮬레이터 (연결됨)
- Galaxy S24 (USB 연결됨)
- Pixel 7 에뮬레이터 (실행 중)

## 2. 앱 실행하기

```
iPhone 시뮬레이터에서 설정 앱을 실행해줘
```

## 3. 화면 스크린샷 및 정보 확인

```
현재 화면의 스크린샷을 찍고, 화면에 있는 모든 UI 요소들을 나열해줘
```

## 4. 기본 자동화 시나리오

```
다음 단계를 실행해줘:
1. 설정 앱 실행
2. "일반" 메뉴 탭하기
3. "정보" 메뉴 탭하기
4. 디바이스 모델명 확인
5. 스크린샷 저장
```

## 5. 앱 스토어 검색 시나리오

```
앱 스토어에서 다음 작업을 진행해줘:
1. 앱 스토어 앱 실행
2. 검색 탭으로 이동
3. "Instagram" 검색
4. 첫 번째 검색 결과 정보 확인
5. 각 단계별로 스크린샷 저장
```

---

# Mobile Next MCP의 핵심 명령어들

## 디바이스 관리 명령어
- `mobile_list_apps`: 설치된 모든 앱 목록 확인
- `mobile_launch_app`: 특정 앱 실행 (Bundle ID/Package Name 사용)
- `mobile_terminate_app`: 실행 중인 앱 종료
- `mobile_get_screen_size`: 화면 크기 정보 확인

## 상호작용 명령어
- `mobile_list_elements_on_screen`: 화면의 모든 UI 요소 목록
- `mobile_element_tap`: 접근성 레이블로 요소 탭하기
- `mobile_tap`: 특정 좌표 탭하기
- `mobile_type_text`: 텍스트 입력하기

## 정보 수집 명령어
- `mobile_take_screenshot`: 스크린샷 촬영
- `mobile_get_source`: UI 구조를 XML 형식으로 가져오기

---

# 고급 활용 팁

## 1. 조건부 테스트 실행

```
만약 로그인이 되어 있지 않다면 먼저 로그인을 진행하고,
로그인이 되어 있다면 바로 메인 화면에서 원하는 작업을 시작해줘
```

## 2. 반복 작업 자동화

```
다음 작업을 3번 반복해줘:
1. 앱 새로고침
2. 5초 대기
3. 로딩이 완료되었는지 확인
4. 결과 스크린샷 저장
```

## 3. 크로스 플랫폼 비교 테스트

```
iOS와 Android에서 같은 앱의 동일한 기능을 테스트하고 비교해줘:
1. 로그인 플로우의 차이점
2. UI 레이아웃 비교
3. 성능 차이 분석
```

## 4. 접근성 테스트

```
현재 화면의 접근성을 확인해줘:
1. 모든 버튼에 적절한 레이블이 있는지 확인
2. 텍스트 크기가 적절한지 확인
3. 색상 대비가 충분한지 확인
```

---

# 문제 해결 가이드

## 자주 발생하는 문제들

### 1. 디바이스 연결 실패
```bash
# iOS 시뮬레이터 재시작
xcrun simctl shutdown all
xcrun simctl boot "iPhone 16"

# Android 디바이스 재연결
adb kill-server
adb start-server
adb devices
```

### 2. MCP 서버 연결 오류
- 설정 파일 경로 재확인
- JSON 문법 오류 검사
- Node.js 버전 확인 (최신 LTS 권장)

### 3. 앱 실행 실패
- Bundle ID (iOS) 또는 Package Name (Android) 정확성 확인
- 앱이 실제로 설치되어 있는지 확인
- 디바이스 권한 설정 확인

### 4. 요소 인식 실패
- 앱이 완전히 로드될 때까지 대기
- 접근성 설정 활성화 확인
- 스크린샷을 통한 시각적 확인

---

# Mobile Next MCP의 장점

## 기존 방식 대비 개선점

### 1. **단순함과 효율성**
- 복잡한 테스트 프레임워크 학습 불필요
- 자연어로 테스트 시나리오 작성 가능
- 빠른 프로토타이핑과 테스트 가능

### 2. **플랫폼 통합성**
- iOS와 Android를 하나의 인터페이스로 제어
- 크로스 플랫폼 테스트의 일관성 보장
- 플랫폼별 특수한 지식 불필요

### 3. **AI 친화적 설계**
- LLM이 이해하기 쉬운 구조화된 데이터 제공
- 컴퓨터 비전 모델 없이도 정확한 제어 가능
- 자연어 명령의 정확한 해석과 실행

---

# 마무리

Mobile Next MCP는 모바일 테스트 자동화의 새로운 패러다임을 제시합니다. 복잡한 코드나 테스트 프레임워크 학습 없이도, 단순히 자연어 명령으로 정교한 모바일 앱 테스트를 수행할 수 있습니다.

## 이 기술이 가져오는 변화

- **개발 시간 단축**: 테스트 케이스 작성과 실행 시간이 대폭 줄어듭니다
- **접근성 향상**: 개발자가 아닌 QA 팀이나 기획자도 쉽게 테스트를 만들 수 있습니다
- **품질 일관성**: 자동화를 통해 사람의 실수를 줄이고 일관된 테스트 품질을 유지합니다
- **비용 효율성**: 복잡한 테스트 인프라 구축 없이도 고품질 테스트 가능

Mobile Next MCP는 여전히 발전하고 있는 기술이지만, 모바일 앱 개발과 테스트의 미래를 바꿀 큰 잠재력을 가지고 있습니다. 지금부터 차근차근 익혀두시면 향후 업무 효율성을 크게 높일 수 있을 것입니다.

다음 포스트에서는 Mobile Next MCP를 활용한 실제 프로젝트 사례와 더 고급스러운 활용법에 대해 다뤄보겠습니다.

---

## 참고 자료

- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [Mobile Next MCP GitHub](https://github.com/mobilenext/mobile-mcp)
- [Cursor MCP 설정 가이드](https://cursor.sh/docs)
- [Claude Desktop MCP 설정](https://docs.anthropic.com/claude/docs/desktop-mcp)
- [Apidog Mobile Next MCP 가이드](https://apidog.com/blog/mobile-next-mcp-server/)
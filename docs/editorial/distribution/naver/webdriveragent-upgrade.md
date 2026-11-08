# 오래된 iOS 자동화 글을 읽을 때 주의할 점

2021년 iOS 14.4 환경에서 Appium 전체를 올리지 않고 WebDriverAgent만 교체해야 했던 경험이 있습니다. 이 글은 그 기록입니다. 지금 같은 문제를 겪는다면 아래 명령을 그대로 따르기보다 현재 공식 문서를 먼저 확인하세요.

## 당시 상황

iOS 업데이트 후 기존 WebDriverAgent가 동작하지 않았고, 프로젝트 때문에 Appium 버전은 유지해야 했습니다. 빌드 중 Carthage 래퍼가 실패해서, 기존 폴더의 Carthage 관련 파일을 보관했다가 새 WebDriverAgent 폴더에 다시 넣고 의존성을 받는 방식으로 해결했습니다.

## 지금 다시 한다면

현재 Appium의 XCUITest 드라이버가 WebDriverAgent 빌드를 관리합니다. 폴더를 직접 교체하는 방식은 권장되지 않습니다. [appium-xcuitest-driver 공식 문서](https://appium.github.io/appium-xcuitest-driver/)에서 Appium과 드라이버 버전, iOS와 Xcode 호환성을 확인하고, `appium driver doctor xcuitest` 같은 진단 도구로 환경을 점검하세요. 해결되지 않으면 드라이버 로그와 빌드 로그를 함께 확인해야 합니다.

## 오래된 글을 읽는 방법

자동화 글은 작성 시점의 버전에 크게 의존합니다. “그때는 이렇게 했다”와 “지금도 이렇게 해야 한다”를 구분하는 것이 중요합니다.

원문: [iOS 14+ WebDriverAgent 업데이트 기록](https://kimkitae.github.io/posts/webdriveragent-upgrade/)

iOS 자동화 환경 문제로 막혀 있다면 [iam@kimkitae.me](mailto:iam@kimkitae.me?subject=KFlowLabs%20iOS%20automation%20inquiry)로 문의해 주세요. 사용 중인 Xcode, Appium, 단말 버전을 함께 알려 주세요.

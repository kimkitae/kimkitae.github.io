# Espresso로 Android 화면 테스트 시작하기

Espresso는 Android 앱 내부에서 UI 동작을 검증하는 네이티브 테스트 프레임워크입니다. Appium처럼 외부에서 화면을 제어하는 방식과 달리, 앱 소스와 함께 빌드되어 더 빠르고 안정적인 경우가 많습니다.

## 연습할 흐름

Android Studio에서 앱을 빌드하고, 에뮬레이터나 단말에서 Espresso 테스트를 실행합니다. `onView`로 요소를 찾고, `perform`으로 클릭이나 입력을 하고, `check`로 상태를 검증합니다. 이 기본 흐름을 익히면 화면별 페이지 오브젝트를 나누는 방법도 이해하기 쉬워집니다.

## 저장소

[PracticeAutomationEspressoAndroid](https://github.com/kimkitae/PracticeAutomationEspressoAndroid)에 최소 예제가 있습니다. Android Studio, SDK Manager, 에뮬레이터가 준비된 상태를 가정하며, 자세한 설치는 README를 참고하세요. 작성 당시 버전을 기준으로 하므로 최신 Gradle과 Android SDK에서는 의존성 버전을 확인해야 합니다.

## Appium과 무엇이 다른가

Espresso는 앱 내부 접근이 가능해 테스트가 참조하는 식별자가 소스에 드러나고, 변경을 더 일찍 알아채기 쉽습니다. 대신 개발 프로세스와 함께 관리해야 하고, 접근 권한이 있는 사람만 작성할 수 있습니다. 두 도구를 경쟁 관계로 보기보다 역할을 나누는 편이 좋습니다.

원문: [Espresso Android 연습 프로젝트](https://kimkitae.github.io/posts/automation2/)

Android 자동화 구조를 검토 중이라면 [iam@kimkitae.me](mailto:iam@kimkitae.me?subject=KFlowLabs%20Espresso%20practice%20inquiry)로 문의해 주세요.

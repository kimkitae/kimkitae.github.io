# 테스트용 SMS 인증번호, 사람을 찾지 않고 확인하는 방법

테스트 자동화에서 SMS 인증번호를 확인하려면 테스트폰을 찾아가거나, 단말을 가진 동료에게 요청해야 합니다. 이 과정을 줄이기 위해 Android 수신 앱과 FastAPI·Redis 서버, Slack 알림, 최근 인증번호 조회 API를 만들었습니다. 원문은 테스트 유심폰을 공유하는 편의를 강조했고, 승인 단말·발신자 제한·내부망 접근 제어는 원문에 구현 기록이 없어 지금 공개한다면 먼저 갖춰야 할 경계입니다.

## 왜 한곳에 모았나

여러 시나리오가 같은 번호를 쓰면 누가 언제 코드를 받았는지 공유가 어렵습니다. 반대로 번호마다 담당자를 두면 인증이 필요할 때 사람을 기다려야 합니다. 그래서 수신 사실과 코드를 짧은 시간 동안만 한 화면에서 볼 수 있게 했습니다.

## 구조

테스트 단말의 Android 앱이 문자를 감지해 내부 서버로 보냅니다. 서버는 FastAPI와 Redis로 구성했고, 인증번호를 10분 TTL로 유지합니다. 웹 화면은 WebSocket으로 갱신되고, Slack 알림과 자동화 API가 최근 인증번호를 전달합니다. 단말 설명, 관리자, Slack 채널은 앱에서 입력하고 웹에서 확인했습니다. WebSocket 세션은 최대 30분으로 관리했습니다.

## 권한과 주의점

일반 SMS 수신과 SMS Retriever는 동작이 다르고, 스토어 배포 앱은 Google Play의 SMS 권한 정책을 별도로 확인해야 합니다. 원문의 `SmsMessage.createFromPdu((byte[]) pdu)` 단일 인자 메서드는 API 23에서 deprecated 되었고, 지금은 `createFromPdu(byte[] pdu, String format)`을 사용해야 합니다. 자세한 내용은 [SmsMessage 공식 문서](https://developer.android.com/reference/android/telephony/SmsMessage)에 있습니다.

발신 번호 허용 목록과 Slack 채널 ID를 설정값으로 분리하고, 로그에 인증번호나 문자 전문을 남기지 않는 것은 현재 권고입니다. 원문에는 이런 통제를 구현했다는 기록이 없습니다.

원문: [SMS 인증문자 관리 페이지 개발 및 운영하기](https://kimkitae.github.io/posts/sms-management-system/)

테스트 인증 흐름을 자동화하고 있다면 [iam@kimkitae.me](mailto:iam@kimkitae.me?subject=KFlowLabs%20SMS%20automation%20inquiry)로 문의해 주세요. 실제 전화번호, 토큰, 고객 문자 내용은 보내지 마세요.

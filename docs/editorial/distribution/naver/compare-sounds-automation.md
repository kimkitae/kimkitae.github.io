# 알림음이 났는지 자동으로 확인하는 방법

알림음은 화면에 흔적을 남기지 않습니다. 그래서 “소리가 났는가”를 자동으로 확인하려면 소리를 직접 기록해야 합니다. 오디오 지문(fingerprint)은 이 문제를 다루는 한 가지 방법입니다.

## 먼저 바로잡을 점

예전 글에서 Docker Hub의 `appbaseio/dejavu`를 오디오 지문 도구로 소개했는데, 그것은 Elasticsearch 데이터 뷰어입니다. 오디오 지문에는 [`worldveil/dejavu`](https://github.com/worldveil/dejavu)를 사용해야 합니다. 원문 환경은 docker-compose로 PostgreSQL을 실행하고 `songs`, `fingerprints` 테이블을 사용했습니다.

## 소리를 먼저 녹음해야 한다

Android의 `adb shell screenrecord`는 영상만 기록하고 오디오는 포함하지 않습니다. Appium의 Android 화면 녹화도 같습니다. 따라서 마이크 입력이나 오디오가 활성화된 별도 녹음기로 알림음 구간을 함께 기록해야 합니다. 원문에는 당시 어떤 녹음 경로를 사용했는지 명시되어 있지 않습니다.

기록한 파일에 오디오 스트림이 있을 때만 추출 단계를 적용할 수 있습니다.

```bash
ffmpeg -i notification.mp4 -vn -acodec pcm_s16le notification.wav
```

## 현실적인 주의점

주변 소음, 마이크 위치, 볼륨에 따라 결과가 달라집니다. 특정 환경에서 잘 맞았다는 관찰은 성능 보장이 아닙니다. 또한 소리가 났다는 사실과 알림이 사용자에게 올바르게 전달됐다는 것은 다릅니다. 기준 음원을 여러 환경에서 지문화하고, 매칭 점수 임계값을 고정하지 말고 모니터링해야 합니다. UI 검증과 함께 사용해야 합니다.

원문: [알림음 확인 자동화 - 오디오 지문으로 소리 매칭하기](https://kimkitae.github.io/posts/compare-sounds-automation/)

알림음이나 미디어 검증 자동화를 검토 중이라면 [iam@kimkitae.me](mailto:iam@kimkitae.me?subject=KFlowLabs%20audio%20automation%20inquiry)로 문의해 주세요. 사용 중인 도구와 버전, 재현 절차를 함께 보내 주시면 도움이 됩니다.

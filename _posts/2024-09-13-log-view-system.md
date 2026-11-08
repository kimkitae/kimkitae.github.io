---
title: 간단한 LogViewer 구현 및 운영하기
author: KimKitae
date: 2024-09-15 12:00:00 +0900
last_modified_at: 2026-11-08
description: FastAPI, Kafka, Redis, MariaDB를 조합해 여러 자동화 도구의 로그를 한곳에서 보는 내부 LogViewer를 만든 경험을 정리합니다.
categories: [Automation, TestPlatform]
tags: [TestPlatform]
translation_url: /en/posts/log-view-system/
pin: false
---

자동화 도구가 여러 개로 늘어나면 “지금 어디서 실패했는지”를 확인하는 일이 병목이 됩니다. New Relic, Datadog, Grafana 같은 도구가 이미 있지만, 간단한 로그 한 줄을 보려고 전체 관측 시스템을 붙이는 것은 과할 때가 있습니다. 이 글은 기존 API 서버에 Kafka와 Redis를 더해 작은 LogViewer를 만든 경험을 정리합니다.

![자동화 도구에서 API 서버, Kafka, MariaDB, Redis Pub/Sub, WebSocket을 거쳐 웹 UI로 이어지는 로그 흐름](/assets/img/posts/renewal/log-view-system.svg)

*그림 1. 로그 수집과 실시간 표시를 분리한 구조. 저장은 MariaDB, 실시간 전달은 Redis Pub/Sub이 담당합니다.*

## 왜 Kafka를 넣었나

처음에는 API 서버가 로그를 받아 바로 DB에 쓰는 구조를 생각했습니다. 하지만 로그 발생량이 늘면 DB 쓰기가 요청 처리 속도를 떨어뜨릴 수 있습니다. 그래서 API 서버는 로그를 Kafka 토픽에 넣고, 별도 컨슈머가 DB 저장과 실시간 전달을 맡도록 분리했습니다.

Kafka를 선택한 이유는 확장성과 병목 우려, 그리고 평소 관심 있던 기술을 이 프로젝트에 적용해 보려는 것이었습니다. 지금의 조언은 별개입니다. 로그량이 크지 않은 내부 도구라면 더 단순한 큐가 맞을 수 있으니, 도구를 문제 크기와 운영 인력에 맞추는 편이 좋습니다.

## 구성 요소

- **클라이언트**: 자동화 도구가 `LogEntry` 형태로 로그를 전송합니다.
- **API 서버(FastAPI)**: 서비스 이름을 Redis 집합에 저장하고, 로그를 Kafka `log` 토픽으로 보냅니다.
- **Kafka consumer**: 메시지를 MariaDB에 저장하고 Redis `log` 채널에 발행합니다.
- **WebSocket**: Redis 채널을 구독해 연결된 브라우저로 로그를 전달합니다.
- **Web UI**: 서비스, 태그, 레벨로 필터링하고 실시간 업데이트를 일시정지할 수 있습니다.

## FastAPI 수명주기

예전 글에서는 `@app.on_event("startup")`을 사용했습니다. 최근 FastAPI에서는 `lifespan` 컨텍스트를 사용하는 방식이 권장됩니다. 연결 객체를 앱 상태에 보관하고, 종료 시 정리하는 흐름을 한곳에 모을 수 있어 테스트하기도 쉽습니다.

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    app.state.redis = await create_redis()
    app.state.kafka = await create_kafka()
    try:
        yield
    finally:
        await app.state.kafka.close()
        await app.state.redis.close()
```

기존 코드를 그대로 붙여 넣기보다, 현재 프레임워크 버전의 권장 패턴으로 옮기는 것이 좋습니다.

## 로그 저장과 실시간 전달

로그 저장 API는 최소한의 검증만 하고 Kafka로 넘깁니다. 서비스 이름은 필터 목록을 만들기 위해 Redis에 모읍니다. 컨슈머는 토픽별로 분기해 `log` 토픽이면 DB 저장과 Redis 발행을 함께 수행합니다.

```python
async for message in consumer:
    data = json.loads(message.value.decode("utf-8"))
    await save_log(data)
    await redis.publish("log", json.dumps(data))
```

실시간 화면은 Redis Pub/Sub을 구독하다가 메시지가 오면 WebSocket으로 전달합니다. 브라우저가 새로고침되면 DB에서 최근 로그를 가져와 초기 화면을 채우고, 이후에는 실시간 스트림을 받습니다. 이 구조 덕분에 모든 로그를 매번 DB에서 조회하지 않아도 됩니다.

## 운영에서 먼저 정할 것

무엇보다 먼저 정할 것은 로그에 무엇을 남기지 않을지입니다. 인증번호, 토큰, 주문 상세처럼 민감한 값은 로그 뷰어에 보내기 전에 클라이언트 단계에서 마스킹하는 것이 좋습니다. 서비스별 보관 기간을 두어 오래된 로그를 정리하는 정책도 함께 필요합니다.

UI는 단순하게 유지하는 편이 좋습니다. 서비스 선택, 태그·레벨 필터, 일시정지, 페이지네이션, 연결 상태 표시 정도면 충분합니다. 기능을 더 넣기보다 “로그가 안 보일 때 원인을 알 수 있는가”를 기준으로 삼을 만합니다. WebSocket이 끊겼을 때 재연결 상태를 보여 주고, DB 조회 실패를 사용자에게 명시적으로 알리는 처리도 같은 기준에 포함됩니다.

## 정리

이 LogViewer는 완전한 관측 플랫폼이 아니라, 작은 내부 도구의 로그를 빠르게 확인하기 위한 장치입니다. 규모가 커지면 결국 전문 로그 수집 시스템으로 옮겨야 합니다. 그 전까지는 API 호출 한 줄로 로그를 남기고 한 화면에서 볼 수 있다는 것만으로도 커뮤니케이션 비용이 줄어듭니다. 이 글의 코드는 당시 구현을 설명하기 위한 축약 예시이며, 현재 라이브러리 버전에 맞춰 검증한 코드는 아닙니다.

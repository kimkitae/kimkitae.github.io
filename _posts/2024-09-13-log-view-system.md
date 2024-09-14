---
title: 간단한 LogViewer 구현 및 운영하기
author: KimKitae
date: 2024-09-15 12:00:00 +9000
categories: [Automation, TestPlatform]
tags: [Testing, TestPlatform]
pin: true
---

# 간단한 로그 뷰어 시스템 구현하기

여러 가지 자동화 도구를 개발하고 운영하다 보면 간단한 로그 확인이 필요할 때가 있습니다. 물론 뉴렐릭(New Relic), 데이터독(Datadog), 그라파나(Grafana)와 같은 훌륭한 로그 수집 및 모니터링 도구들이 이미 존재하지만, 단순한 로그 메시지를 확인하기에는 기능이 과도하거나 설정이 복잡할 수 있습니다. 그래서 기존에 운영 중인 API 서버를 활용하여 간단한 로그 뷰어 시스템을 구현해보았습니다.

서비스 규모가 커지면 단일 방식으로 로그 데이터를 전송할 경우 병목현상이 발생할 수 있다는 우려가 있었습니다. 이를 해결하고 확장성을 고려하기 위해 비동기 메시징 시스템인 Kafka를 도입했습니다. Kafka를 통해 메시지를 비동기로 전달함으로써 서버를 추가하거나 부하를 분산시켜 모든 요청을 효율적으로 처리할 수 있도록 설계했습니다. 또한, Kafka는 평소에 관심이 있던 기술이어서 이번 프로젝트에 적용해보았습니다.

이 글에서는 이전에 작성한 [SMS 인증문자 관리 페이지 개발 및 운영하기](https://kimkitae.github.io/posts/sms-management-system/)와 같은 Web Server 구성에 비동기 메시지 전달을 위한 Kafka와 로그 내역 저장을 위한 MariaDB를 추가 사용하여 시스템을 구성하는 방법을 소개하겠습니다.

## 시스템 아키텍처
시스템 아키텍처를 이해하기 쉽도록 간단한 플로우를 설명해 드리겠습니다.

1. **클라이언트 (서비스 애플리케이션)**:
   - 다양한 자동화 도구나 서비스에서 로그를 남길 때, `LogEntry` 형태의 데이터를 API 서버로 전송합니다.

2. **API 서버 (FastAPI)**:
   - 클라이언트로부터 받은 로그 데이터를 처리합니다.
     - **Redis**:
       - `sadd` 명령어를 사용하여 서비스명을 Redis에 저장하여 서비스 목록을 관리합니다.
     - **Kafka Producer**:
       - 로그 데이터를 Kafka의 `'log'` 토픽으로 전송합니다.

3. **Kafka**:
   - 메시지 브로커로서, `'log'` 토픽으로 전달된 로그 메시지를 저장하고 관리합니다.

4. **Kafka Consumer**:
   - 초기 서버 구동 시 `'log'` 토픽을 구독합니다.
   - 새로운 메시지가 도착하면 다음을 수행합니다:
     - **데이터베이스 (MariaDB)**:
       - 로그 데이터를 비동기로 데이터베이스에 저장합니다.
     - **Redis Publish**:
       - 로그 데이터를 Redis의 `'log'` 채널에 발행하여 실시간으로 웹 클라이언트에 전송합니다.

5. **Redis Pub/Sub 시스템**:
   - **Publish**:
     - Kafka Consumer로부터 받은 로그 데이터를 `'log'` 채널에 발행합니다.
   - **Subscribe**:
     - WebSocket 매니저가 `'log'` 채널을 구독하여 실시간 로그 데이터를 수신합니다.

6. **WebSocket 매니저 (FastAPI)**:
   - 웹 클라이언트와의 WebSocket 연결을 관리합니다.
   - Redis로부터 수신한 로그 데이터를 연결된 모든 웹 클라이언트에 전송합니다.

7. **웹 클라이언트 (Web UI)**:
   - WebSocket을 통해 실시간 로그 데이터를 수신합니다.
   - 사용자에게 로그 데이터를 표시하며, 서비스명, 태그, 로그 레벨 등에 따라 필터링할 수 있습니다.
   - 일시정지 및 재개 기능을 통해 실시간 업데이트를 제어할 수 있습니다.

**전체 흐름 요약**:

- **로그 발생**: 서비스 애플리케이션에서 로그가 발생하면 API 서버로 로그 데이터를 전송합니다.
- **로그 전달**: API 서버는 로그 데이터를 Kafka를 통해 비동기로 전달합니다.
- **로그 처리**: Kafka Consumer는 로그 데이터를 데이터베이스에 저장하고, Redis를 통해 웹 클라이언트에 실시간으로 전달합니다.
- **로그 표시**: 웹 클라이언트는 WebSocket을 통해 수신한 로그 데이터를 사용자에게 표시합니다.

![플로우 다이얼그램](https://github.com/user-attachments/assets/50756ef1-3923-4192-b24e-05c856126939)


--


## Backend 구현하기

### 1. 웹 서버 초기화 시 필요한 연결 설정

FastAPI의 `startup` 이벤트를 이용하여 Web Server가 실행 될 때 Redis와 Kafka에 연결하고, 필요한 Kafka 토픽을 구독합니다.

```python
@app.on_event("startup")
async def run_startup_event():
    if IS_REDIS_CONNECT:
        send_log("info", "Redis 연결 시작", "Redis")
        # Redis 연결 객체 생성 및 초기화
        app.state.redis_driver = await RedisDriver.create()
        await app.state.redis_driver.startup_event()

@app.on_event("startup")
async def start_kafka():
    if IS_KAFKA_CONNECT:
        try:
            # Kafka 매니저 생성 및 초기화
            app.state.kafka_manager = await KafkaManager.create()
            await app.state.kafka_manager.get_producer()
            app.state.consumers = {}

            # 구독할 Kafka 토픽 목록
            topics = ['log', 'sms', 'chatbot', 'automation']
            for topic in topics:
                await app.state.kafka_manager.get_consumer(app, topic, app.state.redis_driver)

            send_log("info", "Kafka 연결 완료", "Kafka")
        except Exception as e:
            send_log("error", f"Kafka 연결 실패: {e}", "Kafka")
            raise
```

- **Redis 연결**: Redis는 세션 관리 및 Pub/Sub 기능을 위해 사용됩니다.
- **Kafka 연결**: Kafka는 로그 메시지의 비동기 전송을 위해 사용됩니다.
  - **Producer**: 메시지를 특정 토픽으로 보내는 역할을 합니다.
  - **Consumer**: 특정 토픽을 구독하여 메시지를 받는 역할을 합니다.

### 2. 로그 저장 API 구현

API로 부터 로그 데이터를 받아 Kafka로 전달하고, Redis에 서비스명을 저장합니다.

```python
@router.post("/set", name="Log 저장", description="Log 내역 데이터를 저장합니다.")
async def save_log(
    request: Request,
    log_entry: LogEntry,
    _redis: RedisDriver = Depends(get_redis_driver),
    _kafka: KafkaManager = Depends(get_kafka_driver),
    db: AsyncSession = Depends(get_db),
    render: Callable = Depends(response_type("all_testcases.html", templates))
):
    try:
        timestamp = datetime.now(pytz.utc)
        formatted_timestamp = await format_kst_time()

        log_data = {
            "service_name": log_entry.service_name,
            "level": log_entry.level,
            "message": log_entry.message,
            "tag": log_entry.tag,
            "timestamp": formatted_timestamp
        }
        # Redis에 서비스명 저장
        await _redis.sadd("services", log_entry.service_name)
        log_key = f"{log_entry.service_name}_{timestamp}"
        log_data_str = json.dumps(log_data)
        # Kafka로 로그 데이터 전송
        await _kafka.send(key=log_key, value=log_data_str, topic='log')
        return {"message": "Log saved successfully"}
    except Exception as e:
        send_log("error", f"Log set Error: {e}", "Log API")
        raise HTTPException(status_code=500, detail=str(e))
```


- **LogEntry 모델**: 로그 데이터는 다음과 같은 필드로 구성됩니다.

```python
class LogEntry(BaseModel):
    service_name: str = Field(..., example="AuthService")
    level: str = Field(..., example="ERROR")
    message: str = Field(..., example="Failed to authenticate user.")
    tag: str = Field(..., example="auth")
    timestamp: datetime = Field(default_factory=datetime.now, example="2024-03-24T13:01:00")
```

- **Redis의 `sadd` 명령어**: 해당 서비스명을 Redis의 집합(set)에 저장하여 서비스 목록을 관리합니다.
- **Kafka로 메시지 전송**: 로그 데이터를 Kafka의 'log' 토픽으로 전송합니다.

### 3. Kafka 프로듀서 구현

Kafka 프로듀서를 통해 로그 데이터를 Kafka로 전송합니다.

```python
async def send(self, key: str, value: str, topic: str):
    try:
        # 메시지를 UTF-8로 인코딩
        encoded_key = key.encode('utf-8')
        encoded_value = value.encode('utf-8')
        # Kafka로 메시지 전송
        await self.producer.send(topic=topic, key=encoded_key, value=encoded_value)
    except Exception as e:
        send_log("error", f"Failed to send message to Kafka: {e}", "Kafka")
```

- **Kafka Producer**: 메시지를 Kafka 토픽으로 보내는 역할을 합니다.

### 4. Kafka 컨슈머 처리

Kafka 컨슈머를 통해 수신한 메시지를 처리하고, 데이터베이스에 저장하며, Redis를 통해 실시간으로 웹에 전송합니다.

```python
async def consume_messages(self, topic_name, redis, consumer):
    async for message in consumer:
        decoded_message = message.value.decode('utf-8')
        decoded_data = json.loads(decoded_message)
        if topic_name == 'log':
            # 비동기로 DB에 로그 데이터 저장
            async for db_session in get_db():
                await create_log(db=db_session, log_data=decoded_data)
            # Redis를 통해 실시간으로 웹에 로그 데이터 전송
            await redis.publish("log", json.dumps(decoded_data))
        elif topic_name == 'sms':
            pass  # 기타 토픽 처리 로직
        else:
            print(f"Received message from {topic_name}: {decoded_data}")
```

- **데이터베이스 저장**: 수신한 로그 데이터를 비동기로 데이터베이스에 저장합니다.

```python
async def create_log(db: AsyncSession, log_data: dict) -> Log:
    new_log = Log(**log_data)
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log
```

- **Redis Publish**: Redis의 `publish` 기능을 사용하여 실시간으로 Web UI로 로그 데이터를 전송합니다.

```python
async def publish(self, client_type: str, data):
    # Redis 채널에 데이터 발행
    await self.redis_client.publish(client_type, data)
```

- **Redis Publish/Subscribe**: Redis의 Pub/Sub 기능을 이용하여 메시지를 발행하고 구독합니다.

### 5. WebSocket을 통한 실시간 로그 전송

Web UI와 WebSocket으로 연결하여 실시간 로그 데이터를 전송합니다.

```python
@router.websocket("/ws")
async def log_web_websocket(websocket: WebSocket):
    manager = await get_log_web_socket_manager()
    client_id = None
    try:
        # 클라이언트 연결 관리
        client_id = await manager.connect(websocket, "log-web")
        # 실시간 로그 처리
        await manager.handle_log_web(client_id)
    except WebSocketDisconnect:
        send_log("WARNING", f"WebSocket 연결 종료: {client_id}", "Log API")
    except Exception as e:
        if isinstance(e, websockets.exceptions.ConnectionClosedOK):
            send_log("INFO", f"WebSocket 연결 정상 종료: {client_id}", "Log API")
        else:
            import traceback
            error_message = f"로그 WebSocket 오류: {str(e)}\n{traceback.format_exc()}"
            send_log("ERROR", error_message, "Log API")
            await asyncio.sleep(5)  # 5초 대기 후 재시도
    finally:
        if client_id:
            await manager.disconnect(client_id)
            await manager.remove_client_data(client_id)
```

- **WebSocket 연결**: 클라이언트와의 WebSocket 연결을 관리합니다.

### 5-1. Redis 구독 및 메시지 전송

Redis의 `subscribe`를 이용하여 'log' 채널을 구독하고, 새로운 메시지가 들어오면 WebSocket을 통해 클라이언트에 전송합니다.

```python
async def handle_log_web(self, client_id: str):
    websocket = self.active_connections[client_id]['websocket']
    pubsub = None
    try:
        # Redis에서 'log' 채널 구독
        pubsub = await self.redis.subscribe("log")
        while True:
            # Redis에서 메시지 수신
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and message['type'] == 'message':
                data = json.loads(message['data'])
                # WebSocket을 통해 클라이언트에 메시지 전송
                await websocket.send_json(data)
                self.active_connections[client_id]['last_activity'] = datetime.now()
            await asyncio.sleep(0.1)
    except websockets.exceptions.ConnectionClosedOK:
        pass
    except Exception as e:
        await asyncio.sleep(5)  # 5초 대기 후 재시도
    finally:
        if pubsub:
            # Redis 구독 해제
            await self.redis.unsubscribe(pubsub, "log")
        await self.disconnect(client_id)
        await self.remove_client_data(client_id)
```

- **Redis Pub/Sub**: Redis의 Publish/Subscribe 기능을 이용하여 실시간으로 메시지를 전달합니다.

## Web UI 구현하기

웹 UI는 사용자가 로그를 실시간으로 확인할 수 있도록 간단하게 구성되었습니다.

![Log Viewer](https://github.com/user-attachments/assets/b34b3cfe-7a0e-475a-8d58-8f84924220c1)

- **서비스명 선택**: 서비스명을 선택하여 해당 서비스의 로그를 확인할 수 있습니다.
- **태그 필터링**: 특정 태그를 선택하여 로그를 필터링할 수 있습니다.
- **로그 레벨 필터링**: 로그 레벨(예: INFO, ERROR 등)을 선택하여 필터링할 수 있습니다.
- **실시간 일시정지/재개**: 실시간 로그 업데이트를 일시정지하거나 재개할 수 있습니다.
- **페이지 이동**: 페이지네이션을 통해 이전 로그를 확인할 수 있습니다.
- **WebSocket 연결 상태**: WebSocket의 연결 상태를 표시합니다.

### 1. 실시간 로그 업데이트

Redis로부터 메시지를 수신하면 `onmessage` 이벤트를 통해 화면을 업데이트합니다.

```javascript
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.type === "ping") {
        socket.send(JSON.stringify({ type: "pong" }));
        return;
    }

    const selectedLogLevels = Array.from(document.querySelectorAll('.log-filter:checked')).map(cb => cb.value);
    if (!isPaused) {
        if (data.level && (selectedLogLevels.includes(data.level.toUpperCase()) || selectedLogLevels.includes('ALL'))) {
            if (data.service_name == currentServiceName && (selectedTags.includes('전체선택') || selectedTags.includes(data.tag))) {
                addLogs([data]);
            }
        }
    }
};
```

- **필터 적용**: 선택된 로그 레벨과 태그에 따라 로그를 필터링합니다.
- **일시정지 기능**: 실시간 업데이트를 일시정지할 수 있습니다.

### 2. 로그 불러오기 및 필터 적용

일시정지를 해제하거나 태그 필터를 변경할 때, 선택된 서비스명의 로그 내역을 데이터베이스로부터 다시 가져옵니다.

```javascript
function fetchLogsForService(serviceName) {
    if (!serviceName) {
        console.error('서비스 이름이 없습니다.');
        return;
    }

    let tagQuery = '';
    if (!selectedTags.includes('전체선택') && selectedTags.length > 0) {
        tagQuery = `&tags=${selectedTags.join(',')}`;
    }

    const url = `/log/get/${serviceName}?page=${currentPage}${tagQuery}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data && Array.isArray(data.logs)) {
                totalLogs = data.total;
                const selectedLogLevels = Array.from(document.querySelectorAll('.log-filter:checked')).map(cb => cb.value);

                const filteredLogs = data.logs.filter(log => {
                    return (selectedLogLevels.includes(log.level.toUpperCase()) || selectedLogLevels.includes('ALL'));
                });
                displayLogs(filteredLogs);
                updatePaginationButtons();
            } else {
                displayError('로그 데이터 형식이 올바르지 않습니다.');
            }
        })
        .catch(error => {
            displayError('로그를 가져오는데 실패했습니다. 잠시 후 다시 시도해주세요.');
        });
}
```

- **데이터베이스 조회 최소화**: Redis를 통해 실시간 로그를 받기 때문에 데이터베이스 조회를 최소화합니다. 단 새로고침 할 경우에만 DB로부터 해당 서비스의 로그 내역으로 가져온 뒤 다시 Redis로 부터 업데이트를 받습니다.
- **필터링 적용**: 선택된 필터에 따라 로그를 화면에 표시합니다.

## 마무리

여기까지 백엔드의 초기 설정부터 로그가 저장되고, 웹 UI에서 실시간으로 로그를 확인하는 과정을 간략하게 설명해보았습니다. 사내 시스템에서 남는 리소스를 활용하여 다양한 사이드 프로젝트의 웹 서비스를 도커로 운영하고 있습니다. 일부 서비스는 요청에 따라 해당 장비에서 대신 구동해드리고 있어, 이 로그 뷰어를 통해 각 담당자들이 간단하게 로그 메시지를 확인할 수 있게 되었습니다. 이를 통해 불필요한 커뮤니케이션 비용을 줄일 수 있습니다. 간단히 API 호출만 하면 되기 때문에 누구나 쉽게 사용할 수 있습니다.
이 시스템을 통해 각 서비스의 로그를 중앙에서 관리하고, 실시간으로 모니터링할 수 있게 되었습니다. 이를 통해 개발 및 운영 과정에서의 효율성을 높이고, 빠르게 문제를 파악하여 대응할 수 있습니다.

이미 훌륭한 로그 수집 서비스들이 많이 존재하지만, 간단하게 로그 메시지만 수집하고 확인하고 싶은 경우에 이와 같은 방법으로 직접 구현하여 활용할 수 있습니다.

## 추가 설명

위 코드에서 사용된 주요 개념들을 간단히 설명하겠습니다.

- **Redis Publish/Subscribe**:
  - **Publish**: 특정 채널에 메시지를 발행합니다.
  - **Subscribe**: 특정 채널을 구독하여 메시지를 수신합니다.
  - 실시간 통신이 필요한 경우에 많이 사용됩니다.

- **Kafka Producer/Consumer**:
  - **Producer**: 메시지를 Kafka의 특정 토픽으로 전송합니다.
  - **Consumer**: Kafka의 특정 토픽을 구독하여 메시지를 수신합니다.
  - 대용량의 데이터를 비동기로 처리할 때 유용합니다.

- **WebSocket**:
  - 클라이언트와 서버 간에 실시간 양방향 통신을 가능하게 하는 프로토콜입니다.
  - 실시간 업데이트가 필요한 웹 애플리케이션에서 많이 사용됩니다.

- **FastAPI**:
  - Python으로 웹 애플리케이션을 개발할 때 사용되는 프레임워크입니다.
  - 비동기 처리를 지원하며, 높은 성능을 자랑합니다.


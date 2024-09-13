---
title: SMS 인증문자 관리 페이지 개발 및 운영하기
author: KimKitae
date: 2024-09-12 12:00:00 +9000
categories: [Automation, TestPlatform]
tags: [Testing, TestPlatform]
pin: true
---

테스트 자동화를 진행할 때, SMS 인증번호를 확인하는 과정이 번거롭고 비효율적일 수 있습니다. 테스트폰을 직접 찾아서 확인하거나, 다른 사람이 소지한 테스트폰에 요청하는 과정이 필요한 경우도 있습니다. 이러한 문제를 해결하기 위해 SMS 수신 내용을 자동으로 처리하고, 인증번호를 Slack 채널로 전달하는 안드로이드 앱을 구현하였습니다.

최초 구현 시 Android 단말에선 `SMS Receiver`를 이용하여 수신 받은 문자 내용을 읽어올수 있어 이를 이용하여, 인증문자 수신 수 인증번호를 추출하여 특정 Slack 채널로 전달 할 수 있도록 `Àndroid SMS Receiver Application` 을 구현하였습니다.

```
@Override
    public void onReceive(Context context, Intent intent) {
        Bundle bundle = intent.getExtras();
        if (bundle != null) {
            Object[] pdus = (Object[]) bundle.get("pdus");
            if (pdus != null) {
                for (Object pdu : pdus) {
                    SmsMessage smsMessage = SmsMessage.createFromPdu((byte[]) pdu);
                    String sender = smsMessage.getDisplayOriginatingAddress();
                    String messageBody = smsMessage.getMessageBody();

                    // 특정 번호로부터의 SMS인지 확인
                    if (sender.equals("+821012345678")) { // 특정 번호를 여기서 설정
                        String verificationCode = extractVerificationCode(messageBody);
                        if (verificationCode != null) {
                            sendToChannel(context, verificationCode); // 특정 슬랙 채널로 수신번호 전달
                        }
                    }
                }
            }
        }
    }

    private String extractVerificationCode(String message) {
        // 인증번호 4자리 숫자 추출
        Pattern pattern = Pattern.compile("\\b\\d{4}\\b");
        Matcher matcher = pattern.matcher(message);
        if (matcher.find()) {
            return matcher.group(0);
        }
        return null;
    }
```

앱을 통한 SMS 수신 관리 외에도, 테스트 단말들이 늘어남에 따라 인증문자를 한 곳에서 통합 관리할 수 있는 웹 페이지를 구축하게 되었습니다. 이를 위해 웹 서버와 기존 Android Application의 개선 작업을 진행했습니다.

- Web Server: fastapi와 redis를 활용하여 도커화된 서버로 구축. WebSocket 통신을 통해 - Android 클라이언트와 실시간으로 통신.
- 데이터 관리: 인증번호는 저장하지 않고 Redis에 10분간 TTL(Time-To-Live) 설정하여 유지.



>시스템 아키텍처

![시스템 아키텍처](https://github.com/user-attachments/assets/b1c39cd4-073d-4063-a336-7214823744f9)

## WebServer

> 최종 UI 화면

![인증문자 통합 관리 페이지](https://github.com/user-attachments/assets/e8e1a5e6-5e7c-4815-bdf8-bc2125b642e9)


1. Web Server는 JavaScript로 UI를 구현하고, WebSocket 이벤트를 통해 실시간으로 화면을 업데이트합니다.
  
> WebSocket 이벤트를 통해 화면을 업데이트 합니다.

```
socket.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            console.log('수신된 데이터:', data);

            if (data.type === "sms_update" || data.type === "device_update") {
                updateUIWithDeviceDetails(data.device);
                if (data.type === "sms_update") {
                    showNotification(data.device.phone_number, data.device.code);
                }
            } else if (data.type === "connection_status") {
                updateDeviceStatus(data.identifier, data.is_connected);
            } else if (data.type === "device_deleted") {
                removeDeviceFromUI(data.phone_number);
            } else if (data.type === "ping") {
                socket.send(JSON.stringify({ type: "pong" }));
            } else if (data.type === "error") {
                console.error('WebSocket error message:', data.message);
            } else {
                console.warn('Unknown data type received:', data);
            }
        } catch (error) {
            console.error('Error processing WebSocket message:', error);
        }
    };
```

>화면 영역 업데이트

```
deviceContainer.innerHTML = `
    <div class="device-header"><h3>${device.phone_number || 'Unknown'}</h3></div>
    <div class="device-info">
        <p>인증번호: <span>${device.code || '-'}</span></p>
        <p>메시지: <span>${device.message || '-'}</span></p>
        <p>최근 수신 시간: <span class="received-time" data-original-time="${device.timestamp || ''}">${formattedTime}</span></p>
        <p>메모: <span>${device.phone_memo || '-'}</span></p>
        <p>관리자: <span>${device.phone_assigned || '-'}</span></p>
        <p>등록 Slack 채널: <span>${device.slack_channel || '-'}</span></p>
        <p class="connection-status ${isConnected ? 'connected' : 'disconnected'}">
            연결 상태: ${isConnected ? '연결됨' : '연결 끊김'}
        </p>
    </div>`;
```

> 단말 등록, SMS 문자 데이터 전송을 위한 Class

```
class SmsEntry(BaseModel):
    phone_number: str = Field(..., example="01000000000")
    code: str = Field(..., example="1234")
    message: str = Field(..., example="Failed to authenticate user.")
    timestamp: datetime = Field(default_factory=datetime.now, example="2024-03-24T13:01:00")

class RegisterEntry(BaseModel):
    phone_number: str = Field(..., example="01000000000")
    phone_memo: str = Field(..., example="메모")
    phone_assigned: str = Field(..., example="홍길동")
    slack_channel: str = Field(..., example="C03ERR0****")
```

> 단말번호를 기준으로 Redis에 리스트 형태로 저장

```
@router.post("/register", name="서버에 단말 등록", description="단말을 서버에 등록합니다.")
async def register_device(sms_entry: RegisterEntry):
    _redis = await RedisDriver.create()
    _kafka = await KafkaManager.create()
    _websockets = await WebSocketManager.create()

    try:
        device_info = {
            "phone_number": sms_entry.phone_number,
            "phone_memo": sms_entry.phone_memo,
            "phone_assigned": sms_entry.phone_assigned,
            "slack_channel": sms_entry.slack_channel
        }

        await _redis.sadd("registered_devices", sms_entry.phone_number)
        await _redis.hset(f"device:{sms_entry.phone_number}", mapping=device_info)

        send_log("debug", f"{sms_entry.phone_number} 단말 정보 등록 {device_info}", "SMS API")

        message = {
            "type": "device_update",
            "device": device_info
        }
        await _redis.publish("sms-web", json.dumps(message))
        await _websockets.broadcast_connection_status(sms_entry.phone_number, True)

        return {"message": "ok"}
    except Exception as e:
        send_log("ERROR", f"{device_info} 단말 등록 실패: {e}", "SMS API")
        raise HTTPException(status_code=500, detail=str(e))
```

> Redis: 단말번호를 기준으로 SMS 인증번호를 10분간 저장하며, 만료 시 삭제. 
> 
> Slack API: 특정 Slack 채널로 인증문자 전송.

```
@router.post("/send", name="Sms 서버로 전송", description="단말의 클라이언트에서 해당 서버로 SMS를 전송합니다.")
async def send_code(sms_entry: SmsEntry):
    _redis = await RedisDriver.create()
    _websocket_manager = await get_sms_web_socket_manager()


    try:

        timestamp = datetime.now(pytz.utc)
        seoul_timezone = pytz.timezone('Asia/Seoul')
        timestamp_kst = timestamp.astimezone(seoul_timezone)

        formatted_timestamp = timestamp_kst.strftime('%Y-%m-%d %H:%M:%S')
        kor_time = await format_kst_time()
        sms_data = {
            "phone_number": sms_entry.phone_number,
            "code": sms_entry.code,
            "message": sms_entry.message,
            "timestamp": formatted_timestamp
        }

        await _redis.set_key(key=sms_entry.phone_number, value=json.dumps(sms_data), ttl=300)
        await _redis.set_key(f"sms:{sms_entry.phone_number}", value=str(sms_entry.code), ttl=300)
        await _websocket_manager.send_sms_update(sms_entry.phone_number, sms_data)

        device_info = await _redis.hgetall(f"device:{sms_entry.phone_number}")
        slack_channel = device_info.get("slack_channel", "")
        if slack_channel and len(slack_channel) == 11 and slack_channel.startswith("C"):
            await SlackApp.post_message({
                'channel': slack_channel,
                'blocks': [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*인증번호 수신 알림*"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*단말번호:*\n{sms_entry.phone_number}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*인증번호:*\n{sms_entry.code}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*수신 시간:*\n{kor_time}"
                            }
                        ]
                    }
                ]
            })


        send_log("debug", f"SMS 전달 Phone - {sms_entry.phone_number} Code - {sms_entry.code} Message - {sms_entry.message} Channel - {slack_channel}", "SMS - Slack")
        return {"message": "SMS 전달 successfully"}
    except Exception as e:
        send_log("ERROR", f"Error: {e}", "SMS API")
        raise HTTPException(status_code=500, detail=str(e))
```

> 슬랙 채널에 인증문자 알림

![Slack 메세지 발송](https://github.com/user-attachments/assets/fc758acd-43a9-411b-9d5a-054e7002416d)

>인증번호를 자동화 테스트에서도 활용할 수 있도록 API를 추가하여 최근 10분 내의 인증번호를 조회할 수 있게 추가 API 구현

```
@router.get("/get/{phone_number}", name="해당 번호의 SMS code 가져오기", description="해당 번호의 최근 수신된 인증번호와 관련 정보를 가져옵니다.")
async def get_code(phone_number: str):
    _redis =  await RedisDriver.create()
    try:
        data_json = await _redis.get_key(f"sms:{phone_number}")

        logging.info(f"get phone number data_json: {data_json}")
        if data_json is None:
            return {"message": f"{phone_number} 에 대한 정보가 없습니다."}

        data = json.loads(data_json)

        return data

    except Exception as e:
        send_log("ERROR", f"Error: {e}", "SMS API")
        raise HTTPException(status_code=500, detail=str(e))
```

1. `WebSocket` 통신이다 보니 세션관리가 필요하여 Redis를 통해 세션관리를 하며, 연결 해제를 위한 여러 조건을 두어 불필요한 세션을 정리 할수 있도록 합니다. 사용 특성 상 즉시 수신문자 확인 후 종료할 것이라 생각하여 최대 세션 유지 시간은 30분으로 잡았고, 웹 브라우저 새로고침, 종료 시에도 즉시 세션정리 되도록 하였습니다. 그리하여 Client에서 인증문자 수신 시 활성화되어 있는 모든 세션에 신규 문자 알림을 띄우도록 하여 페이지를 통해서 바로바로 확인 할 수 있습니다. 

> 동시 문자 수신 알림 기능 확인

![문자 수신 알림](https://github.com/user-attachments/assets/68d5cc07-2a70-4283-ae95-ba02401cb9af)


## Android Client

![Android SMS Receiver Application](https://github.com/user-attachments/assets/3d720f1d-9933-47b2-8708-346281823831)

   
앱은 단말의 설명, 관리자 정보, Slack 채널 등을 입력할 수 있는 UI를 제공하며, 서버 연결 상태를 확인하고 SMS 수신을 처리합니다. 주요 기능은 다음과 같습니다:

### 버전별 SMS Receiver:

Android O (API 26) 미만: Telephony.Sms.Intents.SMS_RECEIVED_ACTION만 감지.
Android O 이상: SmsRetriever.SMS_RETRIEVED_ACTION도 감지. 이는 SMS Retriever API를 사용하여 SMS를 자동으로 읽기 위한 것입니다.
WebSocket을 통한 실시간 데이터 전송: 특정 이벤트 발생 시마다 WebSocket을 통해 데이터를 서버로 전달.


> Receiver 의 경우 OS 버전에 따라 아래와 같이 나뉘어 집니다.
```
 private fun registerSmsReceiver() {
        smsReceiver = SmsReceiver()
        val intentFilter = IntentFilter().apply {
            addAction(Telephony.Sms.Intents.SMS_RECEIVED_ACTION)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                addAction(SmsRetriever.SMS_RETRIEVED_ACTION)
            }
        }
        registerReceiver(smsReceiver, intentFilter)
    }
```
> 버전별 동작 차이
>  1. Android O (Oreo, API 26) 미만: Telephony.Sms.Intents.SMS_RECEIVED_ACTION만 감지합니다. 이 액션은 일반적인 SMS 수신 시에 트리거됩니다. 
> 2. Android O (Oreo, API 26) 이상: SmsRetriever.SMS_RETRIEVED_ACTION도 감지합니다. 이 액션은 SMS Retriever API를 사용하여 SMS를 자동으로 읽어올 때 필요합니다. 이 API는 보안과 사용자 경험을 개선하기 위해 Google이 제공하는 기능으로, 앱이 SMS 수신 권한 없이도 인증 코드가 포함된 SMS를 읽을 수 있게 해줍니다.


>특정 이벤트 발생 시마다 WebSocket으로 데이터를 전달 합니다.

```
override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val action = intent?.getStringExtra("action") ?: "connect"
        phoneNumber = intent?.getStringExtra("phoneNumber") ?: retrievePhoneNumber()
        Log.d("WebSocketService", "onStartCommand called with action: $action, phone number: $phoneNumber")

        when (action) {
            "connect" -> {
                phoneMemo = intent?.getStringExtra("memo") ?: "-"
                phoneAssigned = intent?.getStringExtra("manager") ?: "-"
                slackChannel = intent?.getStringExtra("slackChannel") ?: "-"
                Log.d("WebSocketService", "Connecting with memo: $phoneMemo, manager: $phoneAssigned, slack: $slackChannel")
                registerDeviceAndConnect()
            }
            "disconnect" -> {
                disconnectWebSocket()
                stopSelf()
            }
            "delete" -> {
                deleteDevice(phoneNumber)
                stopSelf()
            }
            "send_sms" -> {
                intent?.getStringExtra("json_data")?.let { jsonData ->
                    sendSmsData(jsonData)
                }
            }
        }

        return START_STICKY
    }
```

## 배포 및 운영
간단하게 구현 및 운영하기 위해 내부 장비를 이용하게 하다보니 배포 시스템도 간소화 해봅니다.
1. Jenkins를 통해 매 5분 단위로 특정 브렌치를 pull하여 커밋 내역을 조회하여, 커밋 내역 변경 확인 시마다 잡이 수행되도록 합니다.
   1. Web-Server : Docker Build, Docker-compose로 배포
   2. Client : Gradle 빌드하여 APK 생성
2. Web-Server를 통해 APK 다운로드 가능하도록 컴포넌트 생성

단말에 앱 설치 후, Web UI 또는 Slack 알림을 통해 인증번호를 쉽게 관리 가능합니다.

이제, 인증문자 통합 관리 페이지를 통해 테스트 자동화에서 SMS 인증번호를 쉽게 관리하고 공유할 수 있습니다. 유심폰을 보유하고 있으나 서랍속에만 넣어놓고 있다면 누구나 해당 앱을 설치하여 테스트 번호를 공유 할 수있고 자동화 코드에서도 인증번호를 손쉽게 활용할 수 있습니다.


---
title: 끊임없이 작동하는 테스터(소프트웨어와 하드웨어의 만남)
author: KimKitae
date: 2024-07-31 15:52:00 +9000
categories: [Automation, Testing]
tags: [Testing]
pin: true
---

노션을 정리하다가 3~4년 전 DeliveryHero Korea 소속 일 때 아르헨티나와 우루과이 국가의 Automation Engineer들과 대화를 나누며 소프트웨어뿐만 아니라 하드웨어를 활용해 절대 멈추지 않는 소프트웨어 테스터를 만들어보자는 아이디어 작성건이 있어 재미로 그때 작성했던 내용을 공유해봅니다.

[Making Automation Tester who never be tired. -  KimKitae](https://kimkitae.notion.site/Making-Automation-Tester-who-never-be-tired-6e6f163cc1564e929909847d2a4716eb)

---

## 절대 지치지 않는 테스터 만들기
백엔드에서는 매일 두 번 이상 배포를 진행하며, 배포마다 주문부터 결제 완료까지의 모든 결제 수단을 확인해야 합니다. 각 PG사에서 제공하는 화면의 가상 키보드는 암호화되어 있고, 매 화면 랜딩 시마다 숫자 배열이 랜덤으로 바뀝니다. 화면 캡처 보호 기능이 적용된 경우, 일반적인 캡처 시 해당 영역이 검은색으로만 표시됩니다. 따라서, GPU가 화면에 그리기 위해 메모리에 저장한 정보를 추출해야 합니다.


이때 테스트 프레임워크는 높은 CPU와 메모리 자원을 소비합니다. (우리 시스템은 3GHz 8코어 Intel XeonE5, 64GB 메모리를 사용합니다) 시스템 모니터링에서 CPU 90% 이상, 메모리 200GB(Swap) 이상 사용률을 확인할 수 있습니다.

## 구현해보기
알리익스프레스에서 판매하는 XY 플로터 기성제품(아두이노 및 커스터마이징 가능한 제품)을 구매하고, 아두이노 또는 라즈베리파이에 카메라 모듈을 연결합니다.


Appium으로 앱 실행 및 오브젝트 확인:
- Appium을 사용하여 앱을 실행하고, 특정 오브젝트가 있는지 확인합니다.

라즈베리파이에서 카메라를 이용해 화면 확인:
- 라즈베리파이에 연결된 카메라를 이용하여 실시간으로 화면을 캡처하고, 오브젝트를 식별합니다.

```
from flask import Flask, request, jsonify
import serial
import time

app = Flask(__name__)

# 시리얼 포트 설정
ser = serial.Serial('/dev/ttyUSB0', 9600)

@app.route('/click', methods=['POST'])
def click():
    data = request.get_json()
    x = data['x']
    y = data['y']
    
    # 좌표를 아두이노로 전송
    ser.write(f"{x},{y}\n".encode())
    
    # 로봇팔이 동작을 완료할 때까지 대기
    time.sleep(2)  # 로봇팔이 동작하는 데 걸리는 시간 (필요에 따라 조정)
    
    return jsonify({"status": "clicked"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

아두이노 로봇팔로 좌표 전달:
- 라즈베리파이가 식별한 오브젝트의 좌표를 아두이노 로봇팔로 전달합니다.

```
#include <Servo.h>

Servo servoX;
Servo servoY;

void setup() {
    Serial.begin(9600);
    servoX.attach(9); // X 축 서보 핀
    servoY.attach(10); // Y 축 서보 핀
}

void loop() {
    if (Serial.available() > 0) {
        String coords = Serial.readStringUntil('\n');
        int commaIndex = coords.indexOf(',');
        int x = coords.substring(0, commaIndex).toInt();
        int y = coords.substring(commaIndex + 1).toInt();

        // 좌표에 따라 서보 위치 설정
        servoX.write(x);
        servoY.write(y);

        // 클릭 동작 (예: 서보를 특정 위치로 이동 후 원위치)
        delay(500);  // 클릭 유지 시간
        servoX.write(90); // 원위치로 복귀
        servoY.write(90); // 원위치로 복귀
    }
}
```

로봇팔로 오브젝트 클릭:
- 아두이노 로봇팔이 전달받은 좌표를 따라 움직여 오브젝트를 클릭합니다.

Appium에서 클릭 확인:
- Appium을 통해 오브젝트가 정상적으로 클릭되었는지 확인합니다.

---

이와 같이 하드웨어만 만들어놓고 소프트웨어 구현을 마무리하지는 못했지만, 시간이 된다면 마무리하고 싶습니다. 또한, 단말의 다양한 사이즈에 사용할 수 있는 크기의 XY 플로터를 만들어 1개의 단말에 1개의 플로터를 연결하여 24/7 내내 각 BDD 형태로 시나리오를 계속 동작하게 하고자 합니다. (주로 비즈니스 로직 동작 여부를 체크)

관심이 있거나, 혹시 이런 프로젝트를 진행하고 계신 분들은 언제든지 많은 조언 부탁드립니다. 같이 한 번 완성해보아요!
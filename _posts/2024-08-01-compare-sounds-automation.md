---
title: 알림음 확인 자동화 (Sound 자동화)
author: KimKitae
date: 2024-08-01 14:00:00 +9000
categories: [Automation, Testing]
tags: [Testing]
pin: false
---

## 시작하기
Shazam이나 네이버 노래 검색 기능과 유사한 Dejavu라는 Docker 서비스를 이용하여, 소리 매칭을 통해 알림음 자동화 검증을 진행하기로 합니다. 

## Dejavu 사용하기
[dejavu](https://hub.docker.com/r/appbaseio/dejavu/)는 오디오 데이터를 지문(fingerprint)으로 변환하여 데이터베이스에 저장하고, 이후 오디오 파일과 매칭시켜 식별할 수 있는 도구입니다.

Docker Compose를 사용하면 로컬 환경에 쉽게 설치하고 실행할 수 있습니다.

```
docker-compose build
docker-compose up -d
```
위 명령어를 실행하면 postgres를 포함한 여러 컨테이너가 실행됩니다. 다음으로, 검증의 기준이 될 사운드 파일을 데이터베이스에 적재합니다.

```
dejavu=# \dt
            List of relations
 Schema |     Name     | Type  |  Owner   
--------+--------------+-------+----------
 public | fingerprints | table | postgres
 public | songs        | table | postgres
(2 rows)
```
```
dejavu=# select * from fingerprints limit 5;
          hash          | song_id | offset |        date_created        |       date_modified        
------------------------+---------+--------+----------------------------+----------------------------
 \g567abrb567h89ef971n29 |       1 |    137 | 2021-01-20 14:22:55.20012 | 2021-01-20 14:22:55.20013
```
이렇게 하면 사운드 파일이 데이터베이스에 적재된 것을 확인할 수 있습니다.

## 오디오 특성화 (Fingerprint 생성)
간단한 함수를 통해 디렉토리 내 음악 파일들을 오디오 특성화하여 데이터베이스에 저장할 수 있습니다.

```
from dejavu import Dejavu

djv.fingerprint_directory("test_sound/", [".mp3"], 3)
```
## 오디오 인식
오디오 인식을 위해서는 음악 파일 또는 마이크 입력을 사용하는 두 가지 방법이 있습니다.

- 파일 인식

```
$ python dejavu.py --recognize file notification.wav
```

```
from dejavu.logic.recognizer.file_recognizer import FileRecognizer

song = djv.recognize(FileRecognizer, "notification.wav")
```

- 마이크 인식

```
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer

song = djv.recognize(MicrophoneRecognizer, seconds=10)  # 기본값은 10초
```

```
$ python dejavu.py --recognize mic 10
```

이렇게 Python 코드를 통해 구현하거나 간단한 명령어로 오디오 인식을 수행할 수 있습니다.

## 테스트하기
요구사항에 따라 시나리오 내에서 해당 알림음이 정상적으로 송출되는지를 확인하기 위해 아래 단계를 진행합니다.

- **시나리오 작성** : Appium을 이용하여 시나리오를 작성합니다.
- **알림음 송출 전 스크린 녹화 시작** : 알림음이 송출되기 전 단계에서 단말의 `Screen Recording`을 시작합니다.
- **알림음 송출 후 스크린 녹화 종료** : 알림음 송출 이후 `Screen Recording`을 종료를 하게 되면 단말 내 특정 폴더 내 저장됩니다. 이후 `ADB pull` 을 통해 생성된 파일을 가져옵니다.
- **파일 형식 변환** : 녹화된 `MP4` 파일을 `MP3` 또는 필요한 형식으로 변환합니다.
- **사운드 매칭 수행** : `python dejavu.py --fingerprint ./test_sound/ notification.mp3` 명령어를 사용하여, 이전에 생성된 파일과 비교합니다.
이후 `Return` 값을 통해 매칭되는 파일이 있는지 확인할 수 있습니다. 

실제로, 집에서 TV가 켜져 있고 가족들이 대화를 나누는 환경에서도 녹음된 알림음 소리 파일이 정확히 서버 파일과 매칭될 정도로 정확도가 높았습니다.


**파일변환** 은 아래의 Python 코드로 변환이 가능합니다.

```
# 모듈 설치: !pip install moviepy
from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_file_path, audio_file_path):
    # mp4 등 비디오 파일 불러오기
    video = VideoFileClip(video_file_path)
    
    # 오디오를 추출하여 mp3 파일로 저장
    video.audio.write_audiofile(audio_file_path)

video_file = 'your_video.mp4'  # 변환하고 싶은 비디오 파일의 경로
audio_file = 'output_audio.mp3'  # 저장할 오디오 파일의 경로, 이름 지정

extract_audio_from_video(video_file, audio_file)
``` 

## 결론
이 과정을 통해 앱에서 특정 구간에 지정된 알림음이 정확히 송출되는지를 자동으로 검증할 수 있었습니다. 이 방법은 환경 소음이 있는 상황에서도 정확하게 동작할 만큼 신뢰도가 높았습니다. 
사운드 관련 간단하게 자동화를 해야 한다면 위의 방법으로도 해보시길 추천드립니다.
---
title: 윈도우 노트북에 Ubuntu 설치하기(맥에서 부팅 이미지 만들팅)
author: KimKitae
date: 2024-10-10 12:00:00 +9000
categories: [server]
tags: [ubuntu]
pin: false
---

최근 LG그램 노트북에 Ubuntu 설치를 하면서 그 과정을 남겨 봅니다.

# 부팅 이미지 다운로드
[부팅 이미지 다운로드](https://ubuntu.com/download/server)를 통해 `Desktop`또는 `Server` 버전을 다운로드 할 수 있다`

# 부팅 이미지 만들기

## USB 초기화
`디스크 유틸리티` 를 통해 USB를 초기화 합니다.
Format 유형은 `MS-DOS(FAT32)`로 설정합니다.

![디스크 유틸리티](https://image.kimkitae.com/images/ubuntu%2Finitialize_usb.png?quality=50)

## ISO 파일 USB 드라이브로 변환
`hdiutil`를 통해 ISO 파일을 USB 드라이브에 UDRW(UDIF read/write image)형태로 변환합니다.

![명령어](https://image.kimkitae.com/images/ubuntu%2Fiso-convert.png?quality=50)

이후 `dmg`확장자로 생성되기 때문에 `iso`확장자로 변경합니다.

## 부팅 이미지 생성
`diskutil list` 명령어를 통해 USB 드라이브를 확인합니다.
![명령어](https://image.kimkitae.com/images/ubuntu%2Fdiskutil-list.png?quality=50)

USB의 드라이브 명을 확인 후 `diskutil unmountDisk /dev/disk4(USB 드라이브 명)` 명령어를 통해 마운트를 해제합니다.

마운트 해제가 안되었을 경우 `dd: /dev/disk4: Resource busy` 에러가 발생합니다.
이 경우 `diskutil unmountDisk force /dev/disk4` 명령어를 통해 강제로 마운트를 해제합니다.

```bash
sudo dd if=./ubuntu.iso of=/dev/disk4 bs=1m
```
명령어를 통해 부팅 이미지를 USB 드라이브에 복사합니다.

```bash
2127+1 records in
3104+1 records out
269271888 bytes transferred in 592.194854 secs (592845 bytes/sec)
```
완료되기 까지의 수십분의 시간이 소요 됩니다.

`diskutil list`명령어를 통해 해당 파티션의 구조가 바뀐것을 확인 하실 수 있습니다.
`diskutil eject /dev/disk4` 를 통해 안전하게 USB 드라이브를 해제 합니다.

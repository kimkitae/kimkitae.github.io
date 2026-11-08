# 맥에서 Ubuntu 부팅 USB 만들기, dd 전에 꼭 확인할 것

맥에서 Ubuntu 부팅 USB를 만들 때 `dd`를 사용합니다. `dd`는 지정한 디스크를 그대로 덮어쓰기 때문에, 대상이 USB가 아니면 데이터를 되돌릴 수 없습니다. 명령보다 확인 절차가 먼저입니다.

## 준비

Ubuntu ISO를 내려받고, 4GB 이상 USB를 `MS-DOS(FAT32)`로 포맷합니다. 터미널에서 `hdiutil convert`로 ISO를 UDRW 이미지로 변환한 뒤 `.dmg` 확장자를 `dd`에서 사용할 이름으로 바꿉니다.

## 가장 중요한 단계

`diskutil list`로 전체 디스크와 USB 식별자를 확인합니다. USB는 보통 `external, physical`로 표시됩니다. 용량과 이름을 함께 보고, 내장 디스크(`/dev/disk0` 등)를 절대 지정하지 마세요. 예시의 `/dev/diskN`은 실제 값으로 바꿔야 합니다.

## 마운트 해제와 기록

`diskutil unmountDisk /dev/diskN`으로 마운트를 해제합니다. `Resource busy`가 나면 사용 중인 프로세스를 확인하고, 필요하면 force 옵션을 사용합니다. 그래도 안 되면 재부팅 후 다시 시도하는 편이 안전합니다. 대상이 USB임을 다시 확인한 뒤 `sudo dd if=./ubuntu.img of=/dev/rdiskN bs=4m status=progress`로 기록합니다.

## 검증

기록이 끝나면 `diskutil eject`로 안전하게 꺼내고, 가능하면 대상 노트북에서 부팅해 설치 화면이 뜨는지 확인합니다. 부팅이 안 되면 ISO 무결성, USB 상태, 보안 부팅 설정을 차례로 점검하세요.

원문: [맥에서 Ubuntu 부팅 USB 만들기](https://kimkitae.github.io/posts/making-booting-image-ubuntu-on-mac/)

설치나 서버 구성에서 막혔다면 [iam@kimkitae.me](mailto:iam@kimkitae.me?subject=KFlowLabs%20Ubuntu%20USB%20inquiry)로 문의해 주세요. 디스크 번호나 내부 호스트 정보는 공개 가능한 예시로 바꿔서 보내 주세요.

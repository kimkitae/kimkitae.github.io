# Ubuntu 네트워크 설정, SSH 끊기기 전에 할 일

Netplan으로 서버 네트워크를 바꾸다가 SSH가 끊기면 복구가 어렵습니다. 설정 문법뿐 아니라 적용 전 복구 절차를 준비하는 것이 중요합니다.

## 인터페이스 확인

`ip a`로 유선과 무선 인터페이스 이름을 확인합니다. Netplan에서는 인터페이스 이름이 키가 됩니다. 예시의 `enp3s0`, `wlp0s20f3`은 환경마다 다르므로 실제 값으로 바꿔야 합니다.

## 올바른 YAML 구조

유선 DHCP는 `ethernets` 아래에 인터페이스 이름을 두고 `dhcp4: true`를 넣습니다. 무선은 `wifis` 아래에 인터페이스 이름을 두고, 그 아래에 `access-points`를 넣습니다. `wlan0` 아래에 실제 인터페이스 이름을 넣는 구조는 올바르지 않습니다. networkd에서 `wifis`를 쓰려면 `wpasupplicant` 패키지가 필요하며 서버 이미지에는 없을 수 있으니 `dpkg -l wpasupplicant`로 확인하세요. 고정 IP는 `dhcp4: false`, `addresses`, `routes`, `nameservers`를 사용합니다.

## 적용 전 검증

`sudo netplan generate`로 문법을 확인하고, `sudo netplan try`로 먼저 적용합니다. 확인 응답이 없으면 이전 설정으로 되돌아갑니다. 정상 동작을 확인한 뒤 `sudo netplan apply`를 실행하세요. 원격 서버라면 콘솔이나 물리 키보드 접근 수단을 미리 준비해야 합니다.

## 복구

접속이 끊겼다면 콘솔에서 백업 파일을 되돌리고 `netplan apply`를 다시 실행합니다. 클라우드라면 직렬 콘솔이나 복구 모드 사용 가능 여부를 미리 확인하세요.

원문: [Ubuntu 서버 네트워크 설정하기(DHCP, 고정 IP)](https://kimkitae.github.io/posts/setting-network-setting/)

네트워크 설정이나 서버 자동화에서 막혔다면 [kimkitae@kflowlabs.com](mailto:kimkitae@kflowlabs.com?subject=KFlowLabs%20Netplan%20inquiry)로 문의해 주세요. 실제 IP, SSID, 비밀번호는 보내지 마세요.

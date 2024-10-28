---
title: Ubuntu 서버 네트워크 설정하기(DHCP, 고정 IP)
author: KimKitae
date: 2024-10-28 12:00:00 +9000
categories: [server]
tags: [ubuntu]
pin: false
---

Ubuntu 서버의 네트워크 설정을 설명합니다.

# 네트워크 인터페이스 조회
```bash
ip a
```

```bash
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever
3: wlp0s20f3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether  brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.102/24 metric 600 brd 192.168.0.255 scope global dynamic wlp0s20f3
       valid_lft 6770sec preferred_lft 6770sec
    inet6 /64 scope link
       valid_lft forever preferred_lft forever
4: enx00e04c680040: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether  brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.136/24 brd 192.168.0.255 scope global enx00e04c680040
       valid_lft forever preferred_lft forever
    inet6 /64 scope link
       valid_lft forever preferred_lft forever
```
현재의 네트워크 인터페이스가 노출됩니다. 
- wlp0s20f3 : 무선 인터페이스
- enx00e04c680040 : 유선 인터페이스

아직 ip 주소가 할당 되지 않아 네트워크 설정이 필요 합니다.

# 네트워크 설정
## Netplan에 자동 DHCP 등록 방법
Netplan 설정 파일 경로:
- **/etc/netplan/** 디렉토리에서 설정 파일을 찾을 수 있습니다. 일반적으로 .yaml 확장자를 갖습니다.

```bash
network:
  version: 2
  renderer: networkd
  ethernets:
    enx00e04c680040:  # 유선 네트워크 인터페이스
      dhcp4: true

  wifis:
    wlan0:  # 무선 네트워크 인터페이스
      wlp0s20f3: true
      access-points:
        "WiFi_SSID":  # 연결할 WiFi 네트워크 이름(SSID)
          password: "WiFi_Password"  # WiFi 비밀번호
```

`sudo netplan apply` 명령어를 통해 설정을 적용합니다.

## Netplan 내 수동 고정 IP 등록 방법

DHCP 대신 수동으로 고정 IP를 설정하는 경우, 다음과 같은 방법으로 설정할 수 있습니다.
```bash
network:
  version: 2
  renderer: networkd
  ethernets:
    enp3s0:
      dhcp4: false
      addresses:
        - 192.168.0.100/24
      routes:
        - to: 0.0.0.0/0
          via: 192.168.0.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```
`sudo netplan apply` 명령어를 통해 설정을 적용합니다.

## DHCP 수동 등록 방법
시스템에서 DHCP 클라이언트를 직접 실행하여 네트워크 인터페이스가 DHCP 서버로부터 IP를 할당받도록 할 수 있습니다.
```bash
sudo dhclient <인터페이스 이름>
```
`dhclient` 명령어를 통해 수동으로 DHCP 서버로부터 IP를 할당받을 수 있습니다.
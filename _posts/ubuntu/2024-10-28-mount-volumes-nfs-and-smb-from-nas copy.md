---
title: NAS와 Ubuntu 서버 간 네트워크 볼륨 마운트하기(NFS, SMB)
author: KimKitae
date: 2024-10-28 12:00:00 +9000
categories: [server]
tags: [ubuntu, nas]
pin: false
---

`DS920+` 네트워크 스토리지를 이용하여 Ubuntu 서버에 네트워크 볼륨으로 마운트하는 방법을 설명합니다.
네트워크 볼륨 마운트 시 2가지 프로토콜 `NFS`, `SMB`를 사용 할 수 있습니다.

# NFS
## NAS 설정
1. `DSM` 접속하여, `제어판` 진입, `NFS 서비스 활성화` 클릭
![NFS 설정](https://image.kimkitae.com/images/ubuntu%2Fnas-nfs-panel.png?quality=50)

2. `공유 폴더` 진입, 공유 하고자 하는 폴더 선택 후 `편집` 버튼 클릭, `NFS 권한` 탭 진입
![NFS 설정](https://image.kimkitae.com/images/ubuntu%2Fnas-folder-nfs-setting.png?quality=50)
- **호스트이름 또는 IP** : 해당 폴더로 마운트 하고자 하는 클라이언트의 IP를 입력합니다. (특정 IP 대역에 있는 클라이언트만 접근 가능하도록 설정 가능)
- **권한** : 해당 폴더에 접근 할 수 있는 권한을 설정합니다.
- **Squash** : 폴더 내 파일 권한을 설정합니다. (`Admin에 모든 사용자 매핑` 선택 시 폴더 내 파일 권한이 모두 동일하게 설정됩니다.)
- **암호화** : 폴더 내 파일 암호화 여부를 설정합니다.
- **비동기 활성화** : 체크하여 비동기 통신을 활성화 합니다.

## Ubuntu 서버 설정
### NFS 패키지 설치
먼저, NFS를 마운트하려면 nfs-common 패키지가 설치되어 있어야 합니다.
```bash
sudo apt update
sudo apt install nfs-common
```

### 마운트할 디렉터리 만들기
NFS 공유를 마운트할 디렉터리를 만들어야 합니다. 예를 들어, `/mnt/nfs_share` 디렉터리를 생성합니다:
```bash
sudo mkdir -p /mnt/nfs_share
```

### NFS 마운트 명령 실행 (임시 사용)
다음 명령을 사용하여 NFS 서버의 공유 디렉터리를 마운트합니다. 여기서는 NFS 서버의 IP 주소가 192.168.0.180이고, 마운트할 NFS 디렉터리가 /volume1/shared라고 가정합니다:
```bash
sudo mount -t nfs 192.168.0.180:/volume1/shared /mnt/nfs_share
```
### NFS 자동 마운트 설정
#### fstab 파일 수정
/etc/fstab 파일을 수정하여 NFS 마운트를 설정합니다:
```bash
sudo vim /etc/fstab
```
#### fstab 파일에 NFS 마운트 설정 추가
/etc/fstab 파일의 마지막 줄에 NFS 서버와 마운트할 디렉터리 정보를 추가합니다. 아래는 예시입니다:
```bash
192.168.0.180:/volume1/shared /mnt/nfs_share nfs defaults 0 0
```
- **192.168.0.180:/volume1/shared**: NFS 서버 IP와 공유 폴더 경로
- **/mnt/nfs_share**: 로컬에서 마운트할 디렉터리
- **nfs**: 파일 시스템 유형
- **defaults**: 기본 마운트 옵션
- **0 0**: 덤프와 파일 시스템 체크 옵션(일반적으로 0으로 설정)
#### 마운트 실행
fstab 파일을 수정한 후, 다음 명령을 사용하여 fstab 파일에 추가된 설정을 반영하고 NFS를 마운트합니다:
```bash
sudo mount -a
```

---
# SMB
## NAS 설정
1. `DSM` 접속하여, `제어판` 진입, `SMB 서비스 활성화` 클릭
![SMB 설정](https://image.kimkitae.com/images/ubuntu%2Fnas-smb-panel.png?quality=50)

## Ubuntu 서버 설정
### 필수 패키지 설치
SMB 파일 시스템을 마운트하려면 cifs-utils 패키지를 설치해야 합니다:
```bash
sudo apt update
sudo apt install cifs-utils
```
### 마운트할 디렉터리 만들기
SMB 공유를 마운트할 디렉터리를 생성합니다. 예를 들어 /mnt/smb_share라는 디렉터리를 생성합니다:
```bash
sudo mkdir -p /mnt/smb_share
```

### SMB 마운트 명령 실행(임시 사용)
SMB 공유를 마운트하려면 다음 명령을 사용합니다:
```bash
sudo mount -t cifs -o username=your_username,password=your_password,iocharset=utf8 //192.168.0.180/volume1/shared /mnt/smb_share
```

- **username=사용자이름,password=비밀번호**: SMB 공유에 접근할 때 사용할 사용자 이름과 비밀번호
- **//192.168.0.180/shared_folder**: SMB 서버의 IP 주소와 공유 폴더 이름
- **/mnt/smb_share**: 로컬 마운트 포인트

### SMB 자동 마운트 설정
#### fstab 파일 수정
/etc/fstab 파일을 수정하여 SMB 마운트를 설정합니다:
```bash
sudo vim /etc/fstab
```
#### fstab 파일에 SMB 마운트 설정 추가
fstab 파일의 마지막 줄에 다음과 같은 형식으로 SMB 공유 설정을 추가합니다:
```bash
//192.168.0.180/shared_folder /mnt/smb_share cifs username=사용자이름,password=비밀번호,iocharset=utf8,uid=1000,gid=1000,file_mode=0775,dir_mode=0775 0 0
```
- **192.168.0.180:/volume1/shared**: NFS 서버 IP와 공유 폴더 경로
- **/mnt/nfs_share**: 로컬에서 마운트할 디렉터리
- **nfs**: 파일 시스템 유형
- **defaults**: 기본 마운트 옵션
- **0 0**: 덤프와 파일 시스템 체크 옵션(일반적으로 0으로 설정)

- **//192.168.0.180/shared_folder**: SMB 서버의 IP 주소와 공유 폴더 이름
- **/mnt/smb_share**: 로컬 마운트 포인트
- **cifs**: 파일 시스템 유형
- **username=사용자이름,password=비밀번호**: SMB 접근을 위한 사용자 이름과 비밀번호
- **uid=1000,gid=1000**: 로컬 사용자의 UID와 GID
- **file_mode=0775,dir_mode=0775**: 파일과 디렉터리의 권한 설정

#### 마운트 실행
fstab 파일을 수정한 후, 다음 명령을 사용하여 fstab 파일에 추가된 설정을 반영하고 NFS를 마운트합니다:
```bash
sudo mount -a
```

---

## 네트워크 볼륨 연결 해제
```bash
sudo umount /mnt/nfs_share
sudo umount /mnt/smb_share
```
- `umount`명령어를 사용하여 연결 해제 하고자 하는 디렉터리를 입력합니다.
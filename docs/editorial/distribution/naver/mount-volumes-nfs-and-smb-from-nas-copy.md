# NAS 마운트, NFS와 SMB를 헷갈리지 않는 방법

NAS 공유 폴더를 Ubuntu 서버에 마운트할 때 NFS와 SMB는 설정 방식이 다릅니다. 먼저 사용할 프로토콜을 정하고 해당 절만 따라가는 것이 좋습니다. 아래 IP와 경로는 예시입니다.

## NFS

NAS에서 NFS 서비스를 켜고 공유 폴더 권한에 클라이언트 IP를 등록합니다. Ubuntu에는 `nfs-common`을 설치하고, 마운트 지점을 만든 뒤 임시 마운트로 확인합니다. 경로는 `서버:/볼륨/경로` 형식입니다. 정상이면 `/etc/fstab`에 `_netdev` 옵션과 함께 등록하고 `mount -a`로 검증합니다.

## SMB

SMB는 `cifs-utils`가 필요하고 경로는 `//서버/공유이름` 형식입니다. NFS처럼 `서버:/경로`를 쓰면 안 됩니다. 가장 중요한 차이는 자격 증명입니다. `/etc/fstab`에 `password=...`를 직접 쓰면 파일을 읽을 수 있는 사용자에게 비밀번호가 노출됩니다. 대신 root 소유, `0600` 권한의 credentials 파일을 사용하세요.

## 확인과 해제

임시 마운트로 먼저 확인하고, fstab 등록 후 `mount -a`와 재부팅으로 자동 마운트를 검증합니다. 해제는 `umount`로 합니다. 연결이 안 되면 NAS의 프로토콜 활성화, 클라이언트 IP 허용, 방화벽, 자격 증명 파일 권한을 차례로 확인하세요.

원문: [NAS와 Ubuntu 서버 간 네트워크 볼륨 마운트하기(NFS, SMB)](https://kimkitae.github.io/posts/mount-volumes-nfs-and-smb-from-nas-copy/)

NAS 마운트나 자격 증명 관리에서 막혔다면 [kimkitae@kflowlabs.com](mailto:kimkitae@kflowlabs.com?subject=KFlowLabs%20NAS%20mount%20inquiry)로 문의해 주세요. 실제 IP, 계정, 비밀번호는 보내지 마세요.

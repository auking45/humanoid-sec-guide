# 오픈소스 보안 스캐너 (`run_open_source_scanners.sh`)

이 스크립트는 로봇 시스템 내부에 존재하는 설정 취약점, 패키지(공급망) 취약점, 네트워크 서비스 취약점을 3가지 오픈소스 도구(Lynis, Syft/Grype, Nmap)를 활용하여 한 번에 종합적으로 스캔하는 도구입니다.

## 사전 요구사항

- **실행 환경**: 이 스크립트는 외부 호스트 PC가 아닌 **점검 대상 로봇 장비(x86 또는 NVIDIA 보드) 내부로 복사한 후 직접 실행**해야 합니다.
- 인터넷 연결 (도구 설치 및 취약점 DB 업데이트를 위해 필요)
- 루트(root) 또는 `sudo` 권한

## 사용법

제공된 `scanner_manager.sh` 헬퍼 스크립트를 사용하여 로봇 장비로 스크립트를 배포하고, 스캔 완료 후 결과 리포트 폴더를 쉽게 회수할 수 있습니다.

```bash
# 1. 로봇의 계정과 IP를 입력하여 스캐너 스크립트 배포 (기본 경로: ~/humanoid_sec_scanner)
chmod +x scanner_manager.sh
./scanner_manager.sh deploy robot_user@192.168.1.100
```

배포가 완료되면 로봇에 접속하여 스캐너를 실행합니다.

```bash
ssh robot_user@192.168.1.100
cd ~/humanoid_sec_scanner
sudo ./run_open_source_scanners.sh
exit
```

### 옵션 (CLI Arguments)

특정 스캐너만 개별적으로 실행할 수도 있습니다.

- `--all` : 모든 스캐너를 실행합니다. (기본값)
- `--lynis` : Lynis를 이용해 OS 및 시스템 설정 취약점만 스캔합니다.
- `--grype` : Syft와 Grype를 이용해 SBOM을 생성하고 패키지/라이브러리 취약점(CVE)만 스캔합니다.
- `--nmap` : Nmap과 vulners 스크립트를 이용해 로컬호스트에 열려있는 네트워크 포트와 서비스 취약점만 스캔합니다.

## 결과 확인

실행이 완료되면 스크립트가 실행된 디렉토리 하위에 `scan_reports_YYYYMMDD_HHMMSS` 형태의 폴더가 생성되며, 그 안에 각 도구의 상세 분석 리포트(`.txt`, `.json`)가 저장됩니다. 이 결과 파일들을 호스트 PC로 가져와 분석에 활용할 수 있습니다.

# 로봇 시스템 보안 설정 스크립트 (`robot_sec_setup.sh`)

이 스크립트는 설정 파일(`config.json`)을 기반으로 원격 리눅스 서버를 초기화하고 관리하는 포괄적인 도구임. 보안과 사용 편의성에 중점을 두었으며, SSH 키 기반 인증, 방화벽, 서비스 비활성화 등의 보안 설정을 자동화함.

## 주요 특징

- **설정 파일 기반 관리**: `config.json` 파일에 서버의 목표 상태를 선언적으로 기술하여, 일관성 있고 재사용 가능한 서버 관리가 가능함.
- **자동화된 사용자 설정**: 설정 파일에 명시된 모든 개발자 계정의 생성 및 SSH 키 설정을 자동화함.
- **강화된 보안**: 비밀번호 기반의 SSH 로그인을 비활성화하고, 방화벽을 설정하며, 불필요한 서비스를 끄고, 감사 데몬(`auditd`)을 설정하여 보안을 강화함.
- **중앙화된 키 관리**: 필요한 모든 SSH 키를 스크립트 위치를 기준으로 `.keys` 하위 디렉토리에 자동으로 생성하고 저장하여, 전체 설정을 다른 곳으로 쉽게 이식 가능하게 함.
- **위치 독립적인 실행**: 스크립트가 어떤 디렉토리에서 실행되더라도 문제없이 동작함.

## 사전 요구사항

- `ssh`, `ssh-keygen`이 설치된 로컬 PC.
- `jq`가 설치된 로컬 PC (`sudo apt-get install jq`).
- `sudo` 권한과 비밀번호 기반 SSH 접속이 활성화된 초기 사용자 계정(예: `admin`)이 있는, 새로 설치된 원격 Ubuntu/Debian 기반 서버.

## 파일 구조

스크립트를 실행하면, 스크립트와 동일한 위치에 `.keys` 디렉토리가 생성됨. 이를 통해 프로젝트와 관련 자격 증명을 깔끔하게 정리하여 관리할 수 있음.

```
.
├── robot_sec_setup.sh
├── GUIDE.md
├── GUIDE.ko.md
├── config.json.example
└── .keys/
    ├── id_rsa_rpc_admin
    ├── id_rsa_rpc_admin.pub
    ├── id_rsa_rpc_dev-user-1
    └── id_rsa_rpc_dev-user-1.pub
```

## 핵심 사용법: 설정 파일 기반 워크플로우

이 프로젝트의 모든 작업은 `config.json` 파일을 중심으로 이루어짐.

1.  **설정 파일 준비**: `config.json.example` 파일을 `config.json`으로 복사함.
    ```bash
    cp config.json.example config.json
    ```
2.  **설정 파일 수정**: `config.json` 파일을 열어 자신의 서버 환경에 맞게 `ip`, `admin_user`, `users` 등의 값을 수정함.
3.  **명령어 순차 실행**: 아래 `명령어` 섹션에 설명된 명령어들을 순서대로 실행하여 서버를 설정함.

## 명령어

모든 명령어는 별도의 인자 없이 실행되며, `config.json` 파일에서 모든 설정을 읽어옴.

### 1. `setup-admin`

이 명령어는 새 서버에 대해 **가장 먼저 실행해야 하는** 명령어이며, 초기 보안 강화를 수행함.

- **주요 기능**:
  1.  관리자 사용자를 위한 로컬 SSH 키 페어를 생성함 (`.keys/id_rsa_rpc_admin`).
  2.  생성된 공개키를 원격 서버의 관리자 계정에 복사함.
  3.  서버의 SSH 설정을 수정하여 비밀번호 로그인을 비활성화하고, 관리자 계정만 키로 접속하도록 제한함.
- **사용법**:
  ```bash
  ./robot_sec_setup.sh setup-admin
  ```
  _`ssh-copy-id`가 동작할 수 있도록 관리자 사용자의 비밀번호를 한 번 입력해야 함._

### 2. `add-dev`

`setup-admin` 완료 후, `config.json`의 `users` 목록에 있는 모든 개발자 계정을 서버에 추가함.

- **주요 기능**:
  1.  `users` 목록의 각 사용자에 대해 SSH 키 페어를 생성함.
  2.  각 사용자를 원격 서버에 생성하고, `sudo` 그룹에 추가하며, SSH 키를 배포함.
  3.  SSH 설정의 `AllowUsers` 목록에 새 개발자들을 추가하여 접속을 허용함.
- **사용법**:
  ```bash
  ./robot_sec_setup.sh add-dev
  ```

### 3. `setup-firewall`

`config.json`의 `security.firewall` 설정에 따라 방화벽을 구성함.

- **주요 기능**:
  1.  `enabled`가 `true`일 경우에만 실행됨.
  2.  `ufw`를 설치하고, 기본적으로 모든 수신을 차단함.
  3.  SSH 접속은 항상 허용하며, `allow_ports` 목록에 있는 모든 포트를 추가로 허용함.
- **사용법**:
  ```bash
  ./robot_sec_setup.sh setup-firewall
  ```

### 4. `harden-services`

`config.json`의 `security.harden_services` 설정에 따라 불필요한 네트워크 서비스를 비활성화함.

- **주요 기능**:
  1.  `enabled`가 `true`일 경우에만 실행됨.
  2.  `disable` 목록에 있는 모든 서비스를 찾아 중지하고 비활성화함.
- **사용법**:
  ```bash
  ./robot_sec_setup.sh harden-services
  ```

### 5. `setup-auditd`

`config.json`의 `security.auditd` 설정에 따라 감사 데몬을 설치하고 설정함.

- **주요 기능**:
  1.  `enabled`가 `true`일 경우에만 실행됨.
  2.  `auditd`를 설치하고, 주요 시스템 파일 및 이벤트에 대한 감사 규칙을 적용함.
- **사용법**:
  ```bash
  ./robot_sec_setup.sh setup-auditd
  ```

### 6. `harden-usb`

`config.json`의 `security.usb_hardening` 설정에 따라 USB 저장 장치를 차단함.

- **주요 기능**:
  1. `block_storage`가 `true`일 경우에만 실행됨.
  2. `usb-storage` 커널 모듈을 블랙리스트에 추가하여 USB 저장 장치 사용을 막음.
- **사용법**:
  ```bash
  ./robot_sec_setup.sh harden-usb
  ```

## 설정 옵션

스크립트는 `config.json` 파일을 통해 모든 설정을 관리함. `config.json.example` 파일을 복사하여 자신만의 설정 파일을 만들 수 있음.

- **커맨드라인 옵션**:
  - `--config <파일경로>`: 사용할 설정 파일을 지정함 (기본값: `config.json`).

## 검증 스크립트 (`verify_robot_sec_setup.py`)

설정 스크립트와 함께, `config.json`에 명시된 상태를 서버가 충족하는지 자동으로 확인하는 Python 기반의 검증 도구가 제공됨.

### 사전 요구사항

- 로컬 PC에 Python 3와 `pip`가 설치되어 있어야 함.

### 설치

`requirements.txt` 파일을 사용하여 필요한 Python 라이브러리를 설치함. 이를 통해 올바른 버전의 의존성을 보장할 수 있음.

```bash
# 스크립트 디렉토리로 이동
cd /home/auking45/repos/robot/rpc/

# 의존성 설치
pip install -r requirements.txt
```

### 사용법

`config.json` 파일을 사용하여 서버의 모든 설정을 검증함.

```bash
# 기본 config.json을 사용하여 검증 실행
./verify_robot_sec_setup.py

# 다른 설정 파일을 사용하여 검증 실행
./verify_robot_sec_setup.py --config my-server.json

# 검증 결과를 JSON 파일로 저장
./verify_robot_sec_setup.py --output results.json
```

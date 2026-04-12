# 휴머노이드 보안 점검 도구 (`humanoid_sec_auditor.py`)

이 스크립트는 로봇의 현재 시스템 상태가 **'휴머노이드 특화 보안 요구사항(Specific Requirements)'**을 충족하는지 자동으로 검사하는 도구입니다.
플러그인 아키텍처로 설계되어 있어, 메인 소스 코드를 수정하지 않고도 새로운 점검 항목을 손쉽게 추가할 수 있습니다.

## 주요 특징

- **플러그인 아키텍처**: `checks/` 디렉토리에 있는 점검 모듈을 동적으로 로드합니다.
- **다국어 지원 (i18n)**: 터미널 출력 및 보고서 생성 시 한국어(`ko`)와 영어(`en`)를 지원합니다. (`messages.json` 활용)
- **다양한 출력 포맷**: CI/CD 연동을 위한 JSON 출력과 가시성이 좋은 Markdown 보고서 출력을 모두 지원합니다.

## 사전 요구사항

- **실행 환경**: 이 스크립트는 외부 호스트 PC가 아닌 **점검 대상 로봇 장비(x86 또는 NVIDIA 보드) 내부로 복사한 후 직접 실행**해야 합니다.
- Python 3.6 이상
- 루트(root) 또는 `sudo` 권한 (일부 보안 설정 및 시스템 데몬 상태를 점검하기 위해 필요함)

## 사용법

제공된 `audit_manager.sh` 헬퍼 스크립트를 사용하여 로봇 장비로 파일을 쉽게 배포하고, 점검 완료 후 결과를 회수할 수 있습니다.

```bash
# 1. 로봇의 계정과 IP를 입력하여 스크립트 배포 (기본 설치 경로: ~/humanoid_sec_audit)
chmod +x audit_manager.sh
./audit_manager.sh deploy robot_user@192.168.1.100
```

배포가 완료되면 로봇에 SSH로 접속하여 점검을 수행합니다.

```bash
ssh robot_user@192.168.1.100
cd ~/humanoid_sec_audit
```

스크립트는 기본적으로 한국어(`ko`)로 터미널에 점검 결과를 출력합니다.

```bash
# 기본 점검 실행 (터미널 출력)
sudo ./humanoid_sec_auditor.py
```

### 옵션 (CLI Arguments)

- `--output <파일경로>`: 점검 결과를 머신 리더블(Machine-readable)한 JSON 파일로 저장합니다.
- `--report <파일경로>`: 점검 결과를 사람이 읽기 좋은 Markdown 표 형태로 저장합니다.
- `--lang <en|ko>`: 출력 언어를 설정합니다. 기본값은 `ko`입니다.

**사용 예시:**

```bash
# 영문으로 점검을 수행하고 Markdown 보고서와 JSON 파일을 동시에 생성
sudo ./humanoid_sec_auditor.py --lang en --report audit_report.md --output results.json
```

## 새로운 점검 항목 추가하기 (플러그인 작성법)

새로운 보안 요구사항(예: `SYS-22` AppArmor 점검)을 추가하려면 다음 두 단계를 거치면 됩니다.

### 1. `messages.json`에 메시지 추가

`messages.json` 파일의 `ko`와 `en` 블록에 각각 점검 항목의 이름과 성공/실패 메시지를 추가합니다.
키(Key) 이름은 반드시 `{check_id}_name`, `{check_id}_pass`, `{check_id}_fail` 형태를 따라야 합니다.

```json
"ko": {
    ...
    "SYS-22_name": "AppArmor 강제 모드 점검",
    "SYS-22_pass": "AppArmor가 활성화되어 있습니다.",
    "SYS-22_fail": "AppArmor가 비활성화되어 있습니다."
}
```

### 2. `checks/` 디렉토리에 점검 클래스 추가

`checks/` 디렉토리 안의 파일(예: `sys_checks.py`)에 `SecurityCheck`를 상속받는 클래스를 추가합니다.
별도의 `import` 없이 `SecurityCheck`와 번역 함수 `_()`를 바로 사용할 수 있습니다.

```python
# checks/sys_checks.py 에 클래스 추가

class CheckSYS22(SecurityCheck):
    check_id = "SYS-22"

    def audit(self):
        # 쉘 명령어 실행 결과를 받아옴
        success, out = self.run_cmd("aa-status | grep 'apparmor module is loaded'")

        if success:
            # 성공 시: True와 성공 메시지 반환
            return True, _("SYS-22_pass")
        else:
            # 실패 시: False와 실패 메시지 반환
            return False, _("SYS-22_fail")
```

이제 메인 스크립트를 다시 실행하면 새로 추가한 `SYS-22` 항목이 자동으로 로딩되어 점검 목록에 포함됩니다!

# 기기별 스킬 사본 관리

## 현재 상태

이 저장소의 기존 플러그인 안에 있는 스킬 5개는 해당 위치가 정본입니다. 같은 파일을 별도 skills 폴더에 복제하지 않습니다. catalog.json에서 이름과 정본 위치를 연결합니다.

hanbook은 현재 Windows PC에서 가져온 후보입니다. 다른 PC의 버전과 비교하기 전에는 최종 정본으로 확정하지 않습니다. 원본 내용은 변경하지 않았으며 출처는 provenance/hanbook.json에 기록합니다. 루트와 scripts 폴더의 서로 다른 analyze_pdf.py도 보존했습니다. SKILL.md는 scripts 안의 파일을 지정합니다.

앞서 만든 별도 skill-central 폴더는 초기 초안입니다. 이후 관리는 이 claude-skills 저장소에서 합니다.

## 준비

Python 3.10 이상과 Git이 필요합니다. 관리 도구는 Python 표준 라이브러리만 사용합니다. 스킬 실행에 필요한 OCR, 글꼴, Node 등의 설치와 각 운영체제에서의 스킬 실행 호환성은 별도 사항입니다.

각 PC에서 이 저장소를 내려받습니다.

```text
git clone https://github.com/qwerewqwerew/claude-skills.git
cd claude-skills
```

관리 기능이 main에 병합되기 전에는 기능 브랜치로 전환합니다.

```text
git switch feat/central-skill-management
```

profiles/example.json을 해당 PC 이름의 JSON 파일로 복사하고 skills 목록에 catalog.json의 스킬 이름을 적습니다. 예시 프로필은 실제 PC의 설치 상태를 나타내지 않습니다. hanbook-candidate.json은 후보 검토용입니다.

대상 앱에서 실제로 읽는 스킬 폴더를 확인하여 --target에 직접 지정합니다. 경로를 추측하여 자동 설치하지 않습니다. 플러그인으로 이미 설치된 동일 스킬이 있다면 중복 설치하지 않습니다. 계정 동기화 폴더와 공급자 관리 캐시는 설치 대상으로 사용하지 않습니다.

## Windows 사용 예시

저장소 폴더에서 실행합니다. 아래 테스트 경로는 앱에 등록된 실제 경로가 아닙니다.

```powershell
python tools/manage.py --profile profiles/example.json --target ../skill-test
python tools/manage.py --profile profiles/example.json --target ../skill-test --apply
```

첫 명령은 예정 작업만 표시합니다. 두 번째 명령이 실제로 사본을 설치합니다. installers/install.ps1도 같은 인수를 전달하는 실행 진입점입니다.

## macOS와 Linux 사용 예시

```sh
python3 tools/manage.py --profile profiles/example.json --target ../skill-test
sh installers/install.sh --profile profiles/example.json --target ../skill-test --apply
```

hanbook 후보를 테스트하려면 profiles/hanbook-candidate.json과 --allow-candidates를 명시합니다.

## 업데이트와 충돌

1. 중앙 저장소 안의 정본을 수정하고 검토 후 커밋·푸시합니다.
2. 다른 PC는 로컬 변경을 정리한 뒤 git pull --ff-only로 받습니다.
3. 해당 PC 프로필로 예정 작업을 확인하고 --apply를 실행합니다.
4. 사본의 SHA-256 파일 목록을 정본과 비교하여 일치 여부를 검사합니다.

관리 도구로 설치한 사본만 업데이트합니다. 기존 비관리 스킬, 로컬 수정, 링크·정션이 있으면 중단합니다. 기존 사본을 채택하려면 먼저 비교하고, 별도로 보존한 뒤 설치 대상에서 옮겨야 합니다. 자동 삭제·덮어쓰기 옵션은 없습니다.

업데이트 직전 사본은 설치 폴더의 상위 폴더에 skill-central-backup-임의번호/스킬명으로 보관됩니다. 실행 중 교체 오류가 나면 이미 교체한 사본을 되돌립니다. 전원 종료나 프로세스 강제 종료 시에는 자동 복구가 보장되지 않으므로 백업과 설치 상태를 먼저 확인합니다. 동일 대상에 여러 설치 작업을 동시에 실행하지 않습니다.

프로필에서 뺀 스킬은 자동 삭제하지 않습니다. 실제 사용 중지와 앱 새로고침은 별도로 확인합니다.

## 정본 확정

다른 PC의 동명 스킬과 파일 내용을 비교하여 선택한 버전 하나를 저장소에 반영합니다. hanbook을 확정할 때 catalog.json의 status를 selected로 바꾸고 출처 기록을 갱신합니다. 공개 저장소이므로 개인 경로, 계정 설정, 메모리 수집본은 추가하지 않습니다.

## 검증 범위

Windows에서 미리보기, 신규 설치, 반복 실행, 업데이트·백업, 기존 설치 보호, 로컬 수정 보호, 전체 사전 검사, 경로 입력 검사, 후보 제한, 실행 중 오류 복구를 자동 시험합니다.

macOS·Linux 실제 기기 시험과 각 앱에서의 스킬 인식은 별도 확인이 필요합니다. 공통 Python 구현을 사용한다는 사실만으로 모든 운영체제·스킬의 정상 실행을 보장하지 않습니다.

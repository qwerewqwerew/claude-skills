# 작업 계획

`~/.claude/skills/`의 로컬 스킬 4종을 GitHub 플러그인 마켓플레이스로 배포하기까지의 단계다.
**공개 배포로 진행.** 1~6단계 완료, 7단계(푸시) 진행 중.

## 완료

### 준비 (`0549ff9`)

- 작업본 생성 (`~/Desktop/claude-skills`) — 원본 `~/.claude/skills/`는 미변경
- 스킬 4종을 플러그인 2개 구조로 이관 (`node_modules` 제외로 2.9M → 412K)
- `.claude-plugin/marketplace.json`, `README.md`, `LICENSE`, `.gitignore` 작성
- `git init` + 무수정 베이스라인 커밋

### 1. 경로 이식 (`c95db69`)

하드코딩된 `~/.claude/skills/…` 5곳을 `${CLAUDE_PLUGIN_ROOT}` 기준으로 교체했다.
플러그인 설치 경로가 `~/.claude/plugins/cache/<마켓>/<플러그인>/<버전>/`이라 종전
경로로는 동작하지 않았다.

검증 — `grep -rn "\.claude/skills" plugins` 0건.

### 2. 테마 산출물 저장 위치 (`c95db69`)

`fig_tokens.py`가 생성 테마를 `stitch-ppt/references/themes/` 안에 쓰고 있었다. 플러그인
캐시는 버전별 디렉터리라 업데이트하면 사용자가 만든 테마가 함께 지워진다.

- 출력을 `~/.claude/ppt-themes/`로 옮기고 `PPT_THEME_DIR`로 바꿀 수 있게 했다
- `stitch-ppt`가 내장 테마와 그 폴더를 **함께** 조회하도록 테마 선택 절을 고쳤다
  (같은 id면 추출 테마 우선)
- 두 SKILL.md의 인계 절차에서 "복사해 옮긴다"를 "그 자리에 둔다"로 바꿨다

검증 — 모듈 로드 시 `THEME_OUT_DIR`이 `~/.claude/ppt-themes`로,
`PPT_THEME_DIR=/tmp/xyz`를 주면 `/tmp/xyz`로 해석됨을 확인.

### 3. Node 부트스트랩 (`c95db69`)

`npm install` "최초 1회" 안내를 재실행 안전한 형태로 교체했다.

```bash
[ -d "$SKILL/scripts/node_modules" ] || npm ci --prefix "$SKILL/scripts"
```

`SKILL.md`, `references/fig-extract.md`, "자주 생기는 문제" 항목 모두 같은 명령으로 통일.

### 4. 테마 파일 중복 제거 (`c95db69`)

`kiwik.md`, `kiwik-card.md`가 두 스킬에 바이트 단위로 동일하게 있었다. `stitch-ppt`를
정본으로 두고 `extract-token`의 사본(811줄)을 삭제했다.

`fig_tokens.py`의 골격 참조는 형제 스킬 상대경로(`ROOT.parent / "stitch-ppt" / …`)로
바꿨다. 로컬 개발본과 설치된 플러그인 양쪽에서 같은 위치라 환경변수가 필요 없다.

검증 — 골격 파일이 실제로 해석·존재하고, 전 스크립트 문법 검사 통과.

### 5. 사이트 종속성 분리와 참조 정리 (`ba6eec4`)

`hands-on-manual`의 description이 배포본에 없는 `notion-lesson`·`ncs-curriculum`으로
넘기라고 안내하던 문장을 제거했다.

공개 배포로 정해져 사이트 종속 부분을 **발행 프로필** 구조로 분리했다.
`wordpress-md-block-rules.md` 224줄은 특정 사이트의 자식 테마 패턴, 변환기 내부 함수명,
호스팅 구성, 서버 PHP 절대경로까지 담고 있어 공개 레포에 둘 내용이 아니다.

- 프로필 문서를 `~/.claude/manual-profiles/<사이트>.md`로 옮겼다. `MANUAL_PROFILE_DIR`로
  위치를 바꿀 수 있으며, 2단계의 테마 폴더와 같은 구조다
- SKILL.md의 콜아웃·코드·제목 규칙을 표준 마크다운 기준으로 일반화했다
- 프로필이 없으면 마크다운만 내고 **사이트 마크업을 추측하지 않는다**
- `references/publish-profile-template.md`를 추가했다 (접속 정보·자격증명을 적지 말라는
  주의 포함)

### 6. 로컬 설치 검증 (통과)

원본 스킬 4개를 비활성화하고 로컬 디렉터리를 마켓으로 등록해 실제로 설치했다.

| 확인 항목 | 결과 |
|---|---|
| 플러그인 2개 설치 | 성공 |
| 스킬 4개 인식 | `extract-token`, `stitch-ppt`, `stitch-ppt-54`, `hands-on-manual` |
| 설치본에 하드코딩 경로 | 0건 |
| 골격 파일 해석 (4단계) | 버전 디렉터리 안에서 정상 해석 |
| 테마 출력 위치 (2단계) | `~/.claude/ppt-themes`, 스킬 폴더 밖 확인 |
| `CLAUDE_PLUGIN_ROOT` 전개 (1단계) | 스크립트 2종 모두 존재 확인 |
| `npm ci` 부트스트랩 (3단계) | 의존성 설치 성공, 재실행 시 건너뜀 |
| `fig_decode.mjs` 모듈 로드 | 성공 |
| pptx 조립 end-to-end | 3장, 12192000×6858000 EMU (16:9) |

설치 경로가 `~/.claude/plugins/cache/claude-skills/ppt-kit/<버전>/`으로 확인돼,
1·2단계가 필요했던 이유가 실증됐다.

검증 후 플러그인·마켓을 제거하고 원본 스킬을 복구했다.

검증 중 `marketplace.json`의 `hands-on-manual` 설명이 5단계 변경을 반영하지 못한 것을
발견해 고쳤다(`b26dc16`).

### 7. 히스토리 정리와 공개 푸시 (완료)

**푸시 직전 문제 하나를 발견했다.** 5단계에서 사이트 종속 내용을 HEAD에서 지웠지만,
무수정 베이스라인 커밋에는 그대로 남아 있었다. 히스토리를 푸시하면 공개된다.

파일 하나만 제거하는 것으로는 부족했다 — 호스팅 구성과 서버 절대경로가
`SKILL.md` 본문에도 있었고, 초기 커밋들을 손보면 "무수정 이관"이라고 적힌 커밋이
실제로는 수정된 것이 되어 이력이 사실과 어긋난다.

그래서 **한 커밋으로 정리해서 공개했다.** 단계별 상세 히스토리(7커밋)는
`~/Desktop/claude-skills.history-backup`에 로컬로 보존돼 있다.

전 히스토리 스캔으로 사이트 고유명 · 호스팅명 · 서버 경로 · 변환기 내부 함수명 ·
자격증명 패턴 모두 0건을 확인한 뒤 푸시했다.

**공개 주소** — https://github.com/qwerewqwerew/claude-skills

```
/plugin marketplace add qwerewqwerew/claude-skills
/plugin install ppt-kit@claude-skills
/plugin install hands-on-manual@claude-skills
```

원격 설치 재검증 결과 — 스킬 4개 인식, 하드코딩 경로 0건, 골격 해석 정상,
출력 위치 `~/.claude/ppt-themes`, `npm ci` 부트스트랩 성공, 디코더 로드 성공,
pptx 조립 3장 16:9 정상. 검증 후 플러그인·마켓을 제거하고 원본 스킬을 복구했다.

## 남은 결정

**원본 로컬 스킬 처리** — `~/.claude/skills/`를 남기면 설치한 플러그인 스킬과 이름이 겹친다.
지금은 원본을 그대로 두고 플러그인은 설치하지 않은 상태다. 플러그인 쪽으로 옮겨 쓸지,
로컬 원본을 계속 쓸지 정하면 된다.

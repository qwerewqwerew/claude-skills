# 작업 계획

`~/.claude/skills/`의 로컬 스킬 4종을 GitHub 플러그인 마켓플레이스로 배포하기까지의 단계다.
**공개 배포로 진행.** 1~8단계 완료.

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

### 8. claude.ai 최신본(2026-08-26) 반영과 `session-to-prompt` 추가

`hands-on-manual.skill` · `session-to-prompt.skill` 두 내려받기 원본을 레포에 병합했다.
내려받기 원본은 코알라코딩 워드프레스 전용으로 쓰여 있어, 5단계에서 정한 **발행 프로필**
구조를 다시 얹어 일반화했다. 원본 `.skill` 묶음은 사이트 종속 참조(서버 경로·자식 테마·
변환기 함수명)를 그대로 담고 있어 `.gitignore`에 `*.skill`을 넣어 커밋 대상에서 뺐다.

**`hands-on-manual`에 새로 들어온 것** (561 → 597줄)

- 핵심 원칙 2 재작성 — 손동작을 잘게 쪼개는 것 자체가 목적이 아니고, 작업 흐름을 먼저 세운 뒤
  처음 다루는 사람이 막히는 자리만 쪼갠다
- 핵심 원칙 13 신설 — 산출물 고정 금지. 다 따라 하면 무엇이 몇 개 남는지, 무엇이 완성인지를
  못박지 않는다(읽는 사람마다 목표가 다르다)
- 산출 구조 재편 — 도입부·오리엔테이션 단락과 제목 아래 방향 단락을 없애고, 설명을 손동작
  뒤 결과 설명 자리로 몰았다. 도입 박스를 지운 뒤 줄글로 옮겨 붙는 "도입부 잔재" 4갈래 금지
- `삭제 지시 완전 이행` 섹션 신설 — 빼라는 지시를 받고 일부를 남기는 것은 불이행이다.
  지적 누적에서도 2스트라이크로 센다
- 검증 체크리스트 31~33 신설(도입부 잔재·제목 다음 층·설명 소실), 상황 중립 예외로 휘발성
  정보의 확인일·출처 URL 표기 추가
- `style-diction-rules.md` 269 → 308줄 (16절 산출물 고정 표기 치환표 신설)

**일반화한 자리** — 콜아웃·코드·탭을 사이트 전용 HTML 클래스로 적던 지시는
표준 마크다운(`> [!TAG]`, 펜스, `<details>`)으로, "워드프레스 등록(코알라코딩)" 섹션은
"발행 프로필"로, 특정 제품명이 박힌 예시(Runway·Chrome·토스·`/clear`)는 중립 표현으로 바꿨다.

**`session-to-prompt` 신규 플러그인** — 대화 세션 로그에서 최초 지시·중간 수정 지시·통하지
않은 지시·합격 기준·매번 바뀐 값을 뽑아 여섯 블록 배포용 프롬프트 `.md` 한 벌로 조립한다.
사이트 종속 내용이 없어 원본 그대로 옮겼다(`SKILL.md` + references 3종).
`marketplace.json`·`README.md`에 플러그인 항목을 추가했다.

**설치 검증(통과)** — 이미 user 스코프로 쓰는 설치본을 건드리지 않으려고, `marketplace.json`의
이름을 잠시 `claude-skills-local`로 바꿔 **local 스코프**로 따로 설치해 확인한 뒤 되돌렸다.

| 확인 항목 | 결과 |
|---|---|
| 마켓 매니페스트·플러그인 3개 검증 | `claude plugin validate` 통과 |
| 스킬 인식 | 5개 (`session-to-prompt` 신규 포함) |
| 설치본 = 작업본 | `diff -r` 차이 0 (커밋 전 변경까지 반영) |
| 설치본 하드코딩 경로 | 0건 |
| 설치본 사이트 종속 참조 | 0건 |
| 골격 파일 해석·테마 출력 위치 | 4·2단계 회귀 없음 |
| 코드펜스 짝 맞춤 | 스킬 문서 18개 정상 |

`hands-on-manual`의 호출 비용이 ~46.6k tok으로 다른 스킬(3.8k~7.3k)보다 크다. 검증 체크리스트나
치환표를 호출 시점이 아니라 필요할 때 읽는 구조로 빼면 줄일 수 있다.

## 정해진 것

**원본 로컬 스킬 처리 — 플러그인 쪽으로 옮겼다.** `~/.claude/skills/`를 비우고,
`ppt-kit`·`hands-on-manual`을 GitHub 마켓(`claude-skills`)에서 user 스코프로 설치해 쓴다.
이름이 겹칠 일이 없어졌다.

이후 스킬을 고칠 때는 이 레포를 고쳐 푸시하고 `/plugin update`로 받는다. claude.ai 쪽에서
먼저 고친 것이 있으면 `.skill`로 내려받아 8단계처럼 병합한다.

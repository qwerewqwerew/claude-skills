# claude-skills

한국어 실무용 [Claude Code](https://claude.com/claude-code) 스킬 모음입니다. 플러그인 3개로 배포합니다.

## 설치

```
/plugin marketplace add qwerewqwerew/claude-skills
/plugin install ppt-kit@claude-skills
/plugin install hands-on-manual@claude-skills
/plugin install session-to-prompt@claude-skills
```

## 플러그인

### `ppt-kit`

Figma 디자인 → 한국어 PPT 템플릿 파이프라인. 스킬 3개가 한 묶음으로 물려 있어 함께 설치됩니다.

| 스킬 | 역할 |
|---|---|
| `extract-token` | `.fig`/`.deck` 로컬 사본에서 색·타이포·간격·변수 등 디자인 토큰을 추출한다 |
| `stitch-ppt` | 16:9 PPT 템플릿을 만든다. 테마 교체 가능 |
| `stitch-ppt-54` | 5:4 오렌지/차콜 비즈니스 PPT를 만든다. 테마 고정 |

**사전 요구사항**

```bash
pip install python-pptx Pillow
```

Node 의존성은 `extract-token`이 처음 실행될 때 자동으로 설치합니다(`npm ci`). Node 18 이상이 필요합니다.

### `hands-on-manual`

강사 없이 혼자 따라 하는 실습 매뉴얼을 작성하는 스킬입니다. 별도 런타임 의존성이 없습니다.

기본 산출물은 마크다운 한 벌입니다. 특정 사이트(워드프레스·노션 등)에 올리는 것까지 맡기려면
**발행 프로필**을 하나 만들어 `~/.claude/manual-profiles/<사이트>.md`에 둡니다. 작성 서식은
`references/publish-profile-template.md`에 있습니다. 프로필이 없으면 마크다운만 내고 끝냅니다.

### `session-to-prompt`

잘 풀린 작업 하나의 대화 로그를 골라, 다른 사람이 아무 AI 서비스에나 그대로 붙여넣으면 같은
결과가 나오는 **배포용 프롬프트**로 바꾸는 스킬입니다. 별도 런타임 의존성이 없습니다.

로그에서 최초 지시·중간 수정 지시·통하지 않은 지시·합격 기준·매번 바뀐 값 다섯 가지를 뽑아
`[역할] [목표] [입력값] [수행 절차] [출력 형식] [제약]` 여섯 블록으로 압축하고, 파일 경로나
확장 기능 호출처럼 특정 도구에서만 되는 표현을 일반 문장으로 바꿉니다. 산출물은 사용 안내와
변수표, 확인 항목이 붙은 `prompt-<작업슬러그>-v1.md` 한 벌입니다.

## 라이선스

[MIT](LICENSE)

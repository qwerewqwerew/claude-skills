# 슬라이드 원형과 프롬프트 조립 (디자인 무관)

이 문서는 **디자인이 바뀌어도 변하지 않는 것**만 정의한다. 각 원형이 담아야 할
내용 구조, 구성안에서 쓰는 **슬롯 이름**, 그리고 프롬프트를 잇는 규칙이다.
색·폰트·장식·문구 표현은 테마 파일(`themes/<테마>.md`)이 정한다.

---

# 1부 — 슬라이드 원형 9종

원형은 두 갈래다.

- **텍스트형 5종** — 그림 소재가 필요 없다. Stitch 생성 결과를 그대로 쓴다.
- **이미지형 4종** — 사진·로고 같은 **실제 이미지 소재가 필요하다.**
  사용자에게 이미지를 받아 3단계에서 얹는 절차가 따로 있다.
  반드시 `image-slides.md`를 함께 읽는다.

**이미지형은 제공받은 콘텐츠에 이미지가 포함돼 있을 때만 고른다.** 사용자가 사진·로고를
첨부했거나 가진 이미지를 명시했을 때가 그 경우다. 이미지가 없으면 구성안은 텍스트형
5종만으로 짠다. 이미지형을 먼저 배치해 놓고 사용자에게 이미지를 구해 오라고 하지 않는다.

원형을 늘리거나 줄이려면 이 문서와 테마 파일 5절을 함께 고쳐야 한다.
웬만하면 원형은 그대로 두고 표현만 바꾼다.

## 슬롯 이름표 (구성안 → 프롬프트 대입에 그대로 사용)

### 텍스트형 5종

| 원형 | 필수 슬롯 | 선택 슬롯 |
|---|---|---|
| cover | `{부제}` `{주제목}` | — |
| divider | `{섹션문구}` | `{섹션라벨}` |
| card-grid | `{제목}` `{리드문단}` `{카드수}` `{카드N제목}` `{카드N본문}` (N=3~4) | `{섹션라벨}` |
| split-panel | `{제목}` `{항목수}` `{항목N제목}` `{항목N본문}` (N=3~4) | `{부제}` `{섹션라벨}` |
| closing | `{감사문구}` | `{안내문구}` `{섹션라벨}` |

`{섹션라벨}`은 슬라이드 상단에 놓이는 짧은 분류 문구다(예: `문제`, `시장 규모`).
테마가 이 슬롯을 쓰지 않으면 무시된다 — 테마 5절 블록에 `{섹션라벨}`이 없으면
구성안에 값이 있어도 프롬프트에 들어가지 않는다. cover는 이 슬롯을 쓰지 않는다.

### 이미지형 4종 — 사용자 이미지 필요

| 원형 | 필요한 이미지 | 필수 슬롯 | 선택 슬롯 |
|---|---|---|---|
| photo-highlight | 사진 1장 | `{헤드라인}` `{강조단어}` `{사진묘사}` | `{캡션}` `{섹션라벨}` |
| image-full | 사진 1장(상단 전폭) | `{헤드라인}` `{사진묘사}` | `{캡션}` `{섹션라벨}` |
| image-compare | 사진 2장(좌·우 대비) | `{제목}` `{좌사진묘사}` `{우사진묘사}` `{좌캡션}` `{우캡션}` | `{섹션라벨}` |
| logo-grid | 로고 N장 | `{제목}` `{항목수}` | `{마무리문구}` `{섹션라벨}` |

`{사진묘사}` 계열 슬롯은 **Stitch가 자리를 잡을 때 쓰는 설명**이다. 화면에 글자로
찍히지 않는다. 사용자 이미지를 얹을 때도 이 설명이 있어야 플레이스홀더 크기·방향이
내용에 맞게 나온다.

슬롯 이름은 고정이다. 그래서 구성안을 한 번 만들어 두면 프롬프트를 다시 조립하거나
디자인을 손본 뒤에도 같은 내용을 그대로 쓸 수 있다.

## 원형별 구조

### 텍스트형

**cover — 표지**
발표 전체의 첫 화면. 제목 2행(부제 + 주제목)과 시각 모티프.
본문 텍스트·목록·아이콘을 넣지 않는다. 사진 없이 만들어지므로 소재가 필요 없다.

**divider — 섹션 디바이더**
장 구분용. 대형 타이포 1~2행만. 다른 내용은 넣지 않는다.
본문 2~3장마다 하나씩 끼워 호흡을 만든다.

**card-grid — 카드 그리드**
상단에 제목 + 리드 문단, 하단에 동일한 크기의 카드 3~4장.
카드 하나 = 아이콘 + 짧은 제목 + 2~3줄 본문. 병렬 항목을 나열할 때 쓴다.

**split-panel — 좌우 분할 리스트**
화면을 좌/우로 나눠 한쪽은 제목 영역, 다른 쪽은 항목 3개를 세로로 쌓은 패널.
항목에 순서·단계 성격이 있을 때 card-grid보다 낫다.

**closing — 마무리**
감사·질문 유도 문구만. 짧은 텍스트에 강조색 전면 배경으로 덱을 닫는다.

### 이미지형

**photo-highlight — 사진 + 강조 문장**
사진 1장이 화면 절반을 차지하고, 반대편에 짧은 헤드라인 1개.
헤드라인 안의 `{강조단어}`를 테마가 정한 방식으로 강조한다. 선언형 슬라이드.

**image-full — 상단 전폭 이미지**
화면 위쪽 72%를 이미지가 가로로 꽉 채우고, 아래 28% 밴드에 헤드라인과 캡션이
들어간다. 장면 전환, 사례 제시, 분위기 환기용.
※ 글자가 이미지 위에 얹히지 않으므로 사진이 어두워도 가독성은 유지된다.
   다만 가로로 긴 사진이라야 잘리는 부분이 적다.

**image-compare — 이미지 2장 대비**
좌우에 이미지 2장을 같은 크기로 놓고 각각 캡션을 단다.
before/after, 기존/개선, 사례 A/B 비교에 쓴다.

**logo-grid — 로고/항목 그리드**
제목 1행 + 로고의 균등 그리드(3열 내외). 파트너사·사용 기술·고객사 목록 등.
로고는 저작권이 있는 자산이므로 반드시 사용자에게 받는다(임의 생성 금지).

## 구성 흐름 기본형

cover → divider → 본문(card-grid / split-panel / photo-highlight) → divider →
본문 → image-full 또는 logo-grid → closing

10장 내외 기준. 이미지형은 소재를 구해야 하므로 덱 전체의 1/3을 넘기지 않는 편이
진행이 빠르다. 테마 파일 맨 위의 "권장 흐름"도 함께 참고한다.

---

# 2부 — 프롬프트 조립

완성 프롬프트 = **BASE BLOCK** + **STYLE BLOCK** + **원형 블록**
세 조각을 이 순서로 이어 붙인 것이다. 이미지형 원형이면 맨 뒤에
**PLACEHOLDER BLOCK**을 하나 더 붙인다.

- BASE BLOCK: 이 문서에 있는 고정 문단. 모든 프롬프트가 공유한다.
- STYLE BLOCK: 색·폰트·장식 언어. 테마 파일 4절에 있다.
- 원형 블록: 슬라이드 유형별 레이아웃 지시. 같은 파일 5절에 9종이 있다.
- PLACEHOLDER BLOCK: 이미지 자리를 빈 회색 사각형으로 만드는 지시.
  `image-slides.md`에 있다. 앞의 이미지 묘사를 덮어써야 하므로 **반드시 맨 뒤**에 온다.

## 조립 규칙

1. **줄바꿈 없는 한 문단으로 만든다.** 조각을 이을 때 모든 줄바꿈·빈 줄을
   공백 하나로 치환한다. 사용자가 한 번에 복사해 Stitch 입력창에 붙여넣어야 한다.
2. `{슬롯}` 자리에는 구성안의 **한국어 원문을 큰따옴표 안에 그대로** 넣는다.
   번역하지 않는다. 슬롯 이름은 1부의 표를 따른다.
3. 프롬프트 본문 지시는 영문으로 쓴다. Stitch는 영문 지시에서 가장 안정적이다.
4. 한 프롬프트 = 한 슬라이드. 여러 슬라이드를 한 프롬프트에 묶지 않는다.
5. 카드·항목 수가 다르면 개수만 바꾸고 구조 설명은 유지한다.
6. **완성된 프롬프트 전문을 채팅창에 나열하지 않는다.** 도구에 직접 넘기거나
   md 문서로 저장한다(SKILL.md 2단계 참조).

## BASE BLOCK (모든 프롬프트의 첫 단락, 디자인과 무관하게 고정)

```
Design a single 16:9 presentation slide, landscape 1280x720, as one full-width
web page section with no browser chrome, no scrolling. This is a static
presentation slide, NOT an app screen or dashboard: absolutely no global
navigation bar (GNB), no top header bar, no menu bar, no sidebar, no left/right
navigation rail, no tab bar, no toolbar, and no footer of any kind (no footer
bar, no page-number strip, no logo/copyright line at the bottom). No interactive
UI controls at all: no buttons, no call-to-action buttons, no input fields, no
form elements. The slide content fills the entire 1280x720 frame edge to edge.
```

이 문단은 "슬라이드처럼 보이게 하는" 최소 조건이다. 디자인을 손봐도 건드리지 않고,
STYLE BLOCK에 같은 내용을 다시 적지도 않는다(중복되면 서로 어긋나기 쉽다).

## DESIGN.md 조립

Stitch 프로젝트 설정에 등록할 DESIGN.md는 **테마 파일 6절을 그대로 쓰되**, 아래 공통
Rules 항목을 반드시 포함시킨다. 6절에는 이미 포함돼 있으므로 보통은 그대로 복사하면 된다.

```
## Rules
- every screen is a 16:9 landscape presentation slide, 1280x720
- this is a static slide, NOT an app screen or dashboard
- no browser UI
- NEVER add buttons, call-to-action buttons, input fields, or any interactive form controls
- NEVER add a global navigation bar (GNB), top header bar, or menu bar
- NEVER add a sidebar, left/right navigation rail, tab bar, or toolbar
- NEVER add a footer of any kind: no footer bar, no page-number strip, no logo/copyright line at the bottom
- slide content fills the whole 1280x720 frame edge to edge
- Korean text must render in the Korean font declared above
```

## 자주 쓰는 변형

- 차트가 필요한 슬라이드: card-grid 블록에 "a simple bar chart in the accent
  color" 정도의 한 문장만 추가한다. 복잡한 수치는 Stitch보다 3단계 pptx에서
  텍스트 상자로 얹는 편이 정확하다.
- 사진·로고가 들어가는 슬라이드: Stitch에게 그리게 하지 않는다. PLACEHOLDER
  BLOCK으로 자리만 비우고 사용자 이미지를 3단계에서 얹는다 → `image-slides.md`.
- 한국어가 깨지는 경우: 같은 프롬프트를 영문 텍스트로 다시 생성하고,
  3단계에서 pptx 텍스트 상자로 한국어를 얹는다.

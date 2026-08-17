# 디자인: kiwik — PPT.fig 추출 테마 (그린)

이 스킬의 디자인은 이 파일 하나다. 색·폰트·장식·슬라이드별 레이아웃 문구가
모두 여기에 있고, 디자인 변경은 전부 이 파일 안에서 끝낸다.

- **한 줄 성격**: 흰 배경 + 딥그린 강조. 여백이 넓고 장식이 거의 없는 SaaS IR·회사 소개.
- **출처**: 사용자 제공 로컬 사본 `PPT.fig` / `PPT1.fig` (fig-kiwi v106, 노드 287개)와
  그 파일에서 내보낸 프레임 렌더 `#01`~`#10`.
  색은 파일에 들어 있던 **이름 붙은 컬러 스타일 25개 중 활성(visible) 항목**을 그대로 옮겼고,
  2절 타이포 위계와 2.5절 여백·간격은 **`PPT1.fig`의 노드 287개를 직접 재서 뽑은 실측값**이며,
  5절 레이아웃은 **렌더 이미지에서 실제 설계 언어를 읽어 다시 쓴 것**이다.
  근거 없이 바꾸지 않는다. 바꿔야 하면 2·2.5·3·4·5·6절의 해당 값을 함께 고치고,
  무엇을 바꿨는지 사용자에게 알린다.
- **권장 흐름**: cover → divider(질문형) → 본문 2~3장 → divider → 본문 → closing.
  이미지를 받았으면 마지막 본문 자리에 logo-grid(팀·고객사)를 넣는다.
  **이미지가 없으면 이미지형 4종은 쓰지 않는다.**

### 소스의 이름 있는 토큰 (활성 항목)

`styleType: "FILL"` 노드는 전부 25개다. 그중 `visible: true`인 10개가 아래 표이고,
나머지 15개는 꺼져 있다. **참조**는 `#01`~`#10` 노드가 그 스타일을 실제로 가리킨 횟수다.

| 이름표 (파일 그대로) | 값 | 참조 | 배정한 슬롯 |
|---|---|---|---|
| `Primary / Default` | #2C846A | **23회** | Primary — 표지 배경, 아이콘 타일, 원, 수치, 인물 이름 |
| `Primary/Teal` | #2D9F7A | 1회 | 동심원 **바깥**(671px) |
| `Primary / Dark` | #1E6B52 | 1회 | 동심원 **중간**(484px) |
| `Primary/Darkest` | #0E3327 | 1회 | 동심원 **안쪽**(256px) |
| `Neutral / White` | #FFFFFF | **27회** | 배경, 그린 면 위 글자 |
| `Neutral/Black` | #000000 | **26회** | TextStrong |
| `Neutral / Gray Light` | #A3A3A3 | 9회 | 상단 라벨·캡션 |
| `Neutral / Gray Medium` | #737373 | 7회 | TextBody |
| `Accent / Gold` | #CB862E | **0회** | 스와치만 있고 어디에도 안 쓰였다 |
| `Accent / Brown` | #B07553 | **0회** | 위와 같음 |

역할 배정은 추정이 아니라 참조된 노드를 그대로 읽은 것이다. 동심원 3단의 순서
(바깥 Teal → 중간 Dark → 안쪽 Darkest)도 `#08`의 671 / 484 / 256px 원에 각각
그 스타일이 붙어 있어 확인된다.

**Accent 2색은 파일 어디에서도 쓰이지 않았다.** 스와치로만 존재한다. 1절에 남겨는
두지만 기본 레이아웃에서 쓰지 않는 이유가 이것이다.

꺼져 있는 15개는 `Neutral/Neutral50~800`(머티리얼 회색 계단, `#FAFAFA`·`#E0E0E0` 등)과
남색 계열(`#304258`·`#6E7885`·`#F2F3F2`), 주황 `#F48120`이다. 앞의 회색 계단은
`#11`~`#14` 계열이 쓰는 팔레트다. 1절 `Placeholder #E0E0E0`은 이 꺼진 스타일
`Neutral/Neutral300`과 같은 값이라 새로 지어낸 값이 아니다.

### 보라 `#3B00B7`의 정체 — 이전 판 정정

이전 판에는 "보라는 `#04`·`#05` 차트 이미지의 선 색으로만 나타난다"고 적혀 있었는데
**틀렸다.** 실제로는 `#01`~`#10`의 강조 요소 **26개 전부**가 로컬 fill로 보라를 들고 있다:
표지 배경(`#01` 프레임), 아이콘 타일 4개, 원 2개, 수치 텍스트, 라인 아이콘, 인물 이름.
`#08`의 동심원도 보라 계단(`#4F09E3` / `#32009D` / `#18004A`)이다.

그런데 **그 26개 전부가 동시에 그린 스타일을 참조한다.** 로컬 fill과 스타일 값이
어긋나는 노드가 정확히 이 26개이고, 나머지 69개는 일치한다. 즉 파일은 원래 보라 덱이었고
**스타일 정의를 그린으로 바꿔 리컬러한 상태**다 — 렌더는 그린으로 나오고, 노드에 남은
보라는 갱신되지 않은 캐시값이다.

따라서 **그린이 맞다.** 다만 예외가 있다: 스타일 참조가 없는 대형 헤드라인 3개
(`Meet Our Team`, `Our product because of`, `Money raised by our SaaS`)는 리컬러에서
빠져 여전히 보라로 남아 있다. 이 스킬은 헤드라인 강조구를 그린으로 통일하므로
이 3개는 누락으로 보고 따르지 않는다.

## 1. 색상 토큰

| 토큰 | 값 | 용도 | 근거 |
|---|---|---|---|
| Primary | #2C846A | 헤드라인 강조구, 아이콘, 수치, 표지 배경 | `Primary / Default` 23회 |
| PrimaryLite | #2D9F7A | 중첩 도형 **바깥쪽**(671px), 밝은 그린 면 | `Primary/Teal` 1회 |
| PrimaryDark | #1E6B52 | 중첩 도형 **중간**(484px) | `Primary / Dark` 1회 |
| PrimaryDarkest | #0E3327 | 중첩 도형 **안쪽**(256px) | `Primary/Darkest` 1회 |
| Accent | #CB862E | 보조 강조(선택적) | 스와치만 존재, **참조 0회** |
| Neutral800 | #000000 | 헤드라인·카드 제목 | `Neutral/Black` 26회 |
| Neutral500 | #737373 | 본문 | `Neutral / Gray Medium` 7회 |
| Neutral400 | #A3A3A3 | 상단 라벨, 캡션, 마무리 문구 | `Neutral / Gray Light` 9회 |
| Background | #FFFFFF | 표지·마무리를 뺀 모든 슬라이드 배경 | 면적 77% |
| White | #FFFFFF | 그린 배경 위 텍스트 | `Neutral / White` 27회 |
| Placeholder | #E0E0E0 | 이미지 자리 | 꺼진 스타일 `Neutral/Neutral300` |

**면적 기준으로는 흰색 77%, 나머지 전부 합쳐 23%**다. 그린이 차지하는 면적은 6% 남짓인데
표지 배경 1장과 도형 몇 개에 몰려 있다. 넓게 칠하는 색이 아니라 **점으로 찍는 색**이다.

## 2. 타이포그래피

`PPT1.fig`의 TEXT 노드 100개를 전부 읽어 뽑은 값이다. 원본 프레임은 **1920×720이 아니라
1920×1080**이므로, 아래 표의 1280 값은 원본 크기에 **×0.667**을 적용한 것이다.
소스 폰트는 전부 Noto Sans 하나이고 두께만 4단(Black / Bold / Regular / Thin) 쓴다.
Inter Semi Bold 1개, Noto Sans Thin 1개(`{` 장식 글리프)는 예외라 무시한다.

- 라틴: Noto Sans / 한글: **항상 Noto Sans KR** (소스가 뭐든 고정)
- 혼용 스택: `"Noto Sans", "Noto Sans KR", sans-serif`
- 라운드 21.3px — 아이콘 타일에만 쓴다

### 2-1. 위계 표 (역할 → 크기·두께)

| 계층 | 역할 | 원본(1920) | 1280 기준 | 두께 | 행간(소스) | 색 |
|---|---|---|---|---|---|---|
| D1 | 대형 수치 (`$1M`) | 143.6 | **96** | Black 900 | 1.2 | Primary #2C846A |
| D2 | 섹션·디바이더 헤드라인 | 96 | **64** | Black 900 | 1.2 | #000000 + 강조구 #2C846A |
| H1 | 표지 제목 | 90.3 | **60** | Bold 700 | 1.0 | White |
| H1 | 그린 도형 안 대형 수치 | 88~89 | **59** | Bold 700 | 1.0 | White |
| H2 | 서술형 헤드라인 (`#04`) | 81.7 | **54** | Bold 700 | 1.0 | #000000 |
| H2 | 지표 수치 (75.9 / 73.8) | 74~76 | **50** | Bold 700 | 1.0 | Primary / White |
| H3 | 원 안 수치 (`$37`) | 62.2 | **41** | Bold 700 | 1.0 | #000000 |
| H3 | 인물 이름 | 52.2 | **35** | Bold 700 | 1.0 | Primary |
| H4 | 그린 면 위 라벨 (`Revenue`) | 45~47 | **30** | Regular 400 | 1.0 | White |
| H4 | 2×2 항목 제목 | 42.1 | **28** | Bold 700 | 1.0 | #000000 |
| H4 | 보조 강조 수치 (`25,000`) | 42.8 | **29** | Bold 700 | 1.0 | Primary |
| H5 | 3열 항목 제목 | 40 | **27** | Bold 700 | 1.0 | #000000 |
| **L** | **상단 섹션 라벨 (대문자)** | 33.9 | **23** | Bold 700 | 1.0 | #A3A3A3 |
| B1 | 항목 제목 / 캡션 굵게 | 32.4 | **22** | Bold 700 | 1.0 | #000000 |
| B1 | 항목 본문 | 32.4 | **22** | Regular 400 | 1.0 | #737373 |
| B2 | 본문 문단 | 30.4 | **20** | Regular 400 | 1.0 | #000000 |
| B2 | 표지 부제 | 37.0 | **25** | Regular 400 | 1.0 | White |
| B3 | 인물 직함 | 27.5 | **18** | Bold 700 | 1.0 | #000000 |
| B3 | 인물 설명 / 작은 본문 | 24.4 | **16** | Regular 400 | 1.0 | #000000 |
| C | 캡션 (`In Yearly Subscriptions`) | 21.7~23.8 | **15** | Regular 400 | 1.0 | #000000 / White |
| C | 리드 보조문 | 22.3 | **15** | Bold 700 | 1.0 | #737373 |

**한 슬라이드에 쓰는 계층은 3개까지.** 원본 10장이 전부 그렇다 —
라벨(L) + 헤드라인(D2/H2) + 본문(B1/B2)이 기본 세트이고, 수치 슬라이드만
여기에 D1/H2 수치 한 계층을 더한다.

### 2-2. 자간·행간

- **자간은 전부 0이다.** `#01`~`#10`의 TEXT 노드 중 letterSpacing이 0이 아닌 것은 하나도 없다.
  상단 라벨도 자간 0 — 이전 판에서 "wide-tracked"라고 쓴 건 렌더를 눈으로 보고 짐작한 것이라
  근거가 없어 걷어냈다. 대문자 + 굵기 + 회색만으로 라벨을 구분한다.
- **행간은 소스가 대형 헤드라인만 1.2, 나머지는 전부 1.0(100%)이다.**
  1.0을 슬라이드에 그대로 쓰면 붙어서 못 읽으므로 스킬 공통 규칙대로 **본문은 1.4로 올린다.**
  대형 헤드라인(D1·D2)만 소스 값 **1.2**를 유지한다 — 64px 이상에서 1.4는 줄 사이가 벌어져
  덩어리감이 깨진다.
- 문단 간격 6px(원본) → 1280 기준 **4px**. 사실상 문단 사이를 붙여 쓰고
  줄바꿈으로만 나눈다.

### 2-3. 소스 안의 다른 계열 (`#11`~`#14`)

같은 파일에 IT 서비스 소개용 프레임 4장이 더 붙어 있는데 설계가 다르다:
제목 34 / 본문 32(1280 기준 23 / 21), **자간 −4%**, **행간 1.8**, 회색조 텍스트(#424242).
빽빽한 설명문 슬라이드용이다. 이 스킬의 기본 위계는 `#01`~`#10`을 따르고,
설명이 긴 슬라이드가 필요할 때만 이 계열(자간 −4%, 행간 1.8, 본문 21px)을 빌려 쓴다.

## 2.5. 여백·간격 토큰 (spacing)

`#01`~`#10`에는 오토레이아웃이 없다. 전부 절대 좌표라서 아래 값은 노드 위치를
직접 재서 뽑은 것이다(원본 1920×1080 → **×0.667**로 1280 환산).
오토레이아웃(패딩 74/52, 간격 10·16·24·58)은 `#11`~`#14` 계열에만 있으므로
기본 위계에는 쓰지 않는다.

**기본 단위는 17px(원본 26px)이다.** 주요 간격이 전부 이 값의 배수로 떨어진다:
17 / 35 / 69 / 139 / 230.

### 2.5-1. 슬라이드 그리드

| 항목 | 원본 | 1280 기준 | 비고 |
|---|---|---|---|
| 상단 여백 (라벨 top) | 104 | **69** | 10장 전부 동일. 가장 확실한 값 |
| 좌우 여백 | 113 | **75** | 좌측 정렬 슬라이드의 기준선 |
| 하단 여백 | 104 | **69** | 상단과 대칭 |
| 라벨 → 헤드라인 | 26 | **17** | 기본 단위 1배 |
| 헤드라인 블록 하단 | 292 | **195** | 여기부터가 콘텐츠 영역 |
| 헤드라인 → 콘텐츠 (넓게) | 345 | **230** | 3열·인물처럼 아래쪽에 몰아 놓을 때 |
| 헤드라인 → 콘텐츠 (좁게) | 111 | **74** | 2×2처럼 위에서부터 채울 때 |

### 2.5-2. 반복 간격

| 항목 | 원본 | 1280 기준 |
|---|---|---|
| 3열 열 피치 / 거터 | 597~614 / 296 | **398~409 / 197** |
| 2×2 열 피치 | 921 | **614** |
| 2×2 행 피치 | 270 | **180** |
| 세로 지표 리스트 행 피치 (`#04`) | 185 | **123** |
| 항목 제목 → 본문 | 0~15 | **0~10** (거의 붙임) |
| 이름 → 직함 | 2 | **1** (붙임) |
| 직함 → 설명 | 22 | **15** |
| 수치 → 캡션 | 0 | **0** (행상자만으로 띄움) |
| 표지 제목 → 부제 | 52 | **35** |
| 문단 간격 | 6 | **4** |

간격이 대체로 **0에 가깝게 붙어 있다**는 게 이 덱의 성격이다. 항목 안은 붙이고,
항목 사이(거터 197 / 행 피치 180)와 헤드라인 아래(230)에서만 크게 띄운다.
카드가 없으니 **여백 자체가 그룹 경계** 역할을 한다.

### 2.5-3. 요소 크기

| 요소 | 원본 | 1280 기준 |
|---|---|---|
| 아이콘 타일 (라운드 사각) | 125 | **83** (라운드 21.34 → **14**) |
| 타일 안 흰 글리프 | 62~90 | **41~60** (타일의 50~70%) |
| 라인 아이콘 | 133~161 | **89~107** |
| 인물 원형 사진 | 301 | **201** |
| 동심원 3단 | 671 / 484 / 256 | **447 / 323 / 171** (1 : 0.72 : 0.38) |
| 원 안 수치용 원 | 384 / 314 / 157 | **256 / 209 / 105** |
| 우측 풀블리드 이미지 | 874×1080 | **583×720** (폭의 45.5%) |
| 본문 영역 이미지·차트 | 1025×652, 1066×678 | **683×435, 711×452** |

## 3. 장식 언어

원본은 장식이 거의 없다. **여백과 타이포 대비가 곧 디자인**이다.

- 슬라이드 상단에 **회색(#A3A3A3) 대문자 라벨** 한 줄 — 이 덱의 가장 뚜렷한 서명이다
- 그 아래 **대형 헤드라인을 두 색으로 나눈다**: 일부는 검정, 강조구는 그린
- **카드 배경·테두리·그림자·그라디언트를 쓰지 않는다.** 내용은 흰 바탕에 직접 놓인다
- 아이콘은 두 가지: **그린 라인 아이콘**, 또는 **그린 라운드 사각 타일 + 흰 글리프**
- 수치는 **그린 큰 숫자**, 또는 **채운 그린 원 + 흰 글자**에 담는다.
  **외곽선 원은 소스에 없다** — `#01`~`#10` 전체에 스트로크가 단 하나도 없다
- 규모 비교는 **크기가 다른 원을 겹쳐** 표현한다 (`#08`: 671 / 484 / 256px)
- 모서리 원, 점선 두들, 세로 룰, 블러 글로우는 **쓰지 않는다**

실측으로 확인한 사실이다. `#01`~`#10`에는 **스트로크 0개, 이펙트 0개, 그라디언트 0개,
불투명도 1 미만 0개**다. 파일 안의 블러 글로우 11개와 반투명 레이어 6개는 전부
`#11`~`#14` 계열에 있다. 장식 금지 규칙은 취향이 아니라 소스 그대로다.

## 4. STYLE BLOCK

```
Style: clean minimal business pitch deck with very generous whitespace. Colors:
primary deep green #2C846A, light green #2D9F7A, dark green #1E6B52, darkest green
#0E3327, near-black text #000000, body gray #737373, label gray #A3A3A3, white
background #FFFFFF. Typography: Noto Sans for Latin text and "Noto Sans KR" for
Korean text, in only three weights - black 900 for display headlines, bold 700 for
titles and labels, regular 400 for body. Letter-spacing is exactly 0 everywhere,
never tracked out. A small uppercase gray 23px bold label sits above a very large
900-weight headline around 64px whose key phrase is green and the rest near-black,
with body text at 20-22px. Line-height 1.2 on headlines and 1.4 on body. At most
three type sizes per slide. Spacing is built on a 17px unit: 69px slide margins on all
four sides, 17px between the label and the headline, a large 230px gap under the headline
block, 197px gutters between columns and 180px between grid rows, while text inside one
item stays tightly stacked with almost no gap. Absolutely no card backgrounds, no boxes, no borders, no drop
shadows, no gradients, no blurred glows and no decorative corner shapes: content
sits directly on the plain white slide. Icons are simple green line icons or green
rounded-square tiles with a white glyph.
```

## 5. 원형 블록 9종

### 5-1. 텍스트형 5종

#### cover
```
Cover slide. Background solid flat green #2C846A with no gradient, no glow and no
decoration at all. All content is centered horizontally and vertically: a very
large bold white heading "{주제목}", and below it two short centered white lines at
a much smaller size "{부제}". Generous empty space above and below the text block.
Nothing else on the slide.
```

#### divider
```
Section divider slide on plain #FFFFFF. Centered at the top, a small uppercase
bold 23px gray #A3A3A3 label "{섹션라벨}". Below it, centered, a very large 900-weight
display heading around 64px with letter-spacing 0 and line-height 1.2, in two colors, the opening words in near-black #000000
and the key phrase in green #2C846A: "{섹션문구}". Nothing else on the slide, with
large empty space below. No boxes, no glows, no decorative shapes.
```

#### card-grid
```
Content slide on plain #FFFFFF with generous margins. Top left: a small uppercase
bold 23px gray #A3A3A3 label "{섹션라벨}"; directly under it a very large 900-weight
headline around 64px with letter-spacing 0 in two colors, part in near-black
#000000 and the key phrase in green #2C846A: "{제목}"; under the headline one short gray #737373 line "{리드문단}".
Leave a large empty gap, then a row of {카드수} equal columns placed directly on the
white background with NO card background, NO border, NO rounded box and NO shadow.
Each column has a green #2C846A outline line icon at the top, then a bold near-black
title, then two or three lines of small gray #737373 body text. Column contents:
{카드목록}. Keep the columns in the lower half of the slide with wide gutters
between them.
```

**카드 4장일 때는 아래 변형을 쓴다.** 원본 `#06`이 이 형태다. 한 줄에 4개를 늘어놓는
대신 2행 2열로 두고, 아이콘을 라인 대신 타일로 바꾼다.

```
Content slide on plain #FFFFFF with generous margins. Top left: a small uppercase
bold 23px gray #A3A3A3 label "{섹션라벨}"; directly under it a very large 900-weight
headline around 64px with letter-spacing 0 in two colors, part in near-black
#000000 and the key phrase in green #2C846A: "{제목}". Below, four items arranged in a 2x2 grid on the plain white
background with NO card background, NO border and NO shadow. Each item is a
horizontal pair: on the left a green #2C846A rounded-square tile 83px with a 14px corner
radius and a
simple white line glyph inside, on the right a bold near-black title followed by two
or three lines of gray #737373 body text. Item contents: {카드목록}. Wide spacing
between the two columns and the two rows.
```

#### split-panel
```
Content slide on plain #FFFFFF. Centered at the top, a small uppercase bold 23px
gray #A3A3A3 label "{섹션라벨}". Below it a large bold centered headline in two
colors, the key phrase in green #2C846A and the rest in near-black #000000:
"{제목}"; under it one short centered gray #737373 line "{부제}". In the lower half,
{항목수} large figures spread evenly across the full width, each with a bold value
and a small near-black caption underneath. Vary how each figure is presented: the
first value sits inside a solid green #2C846A filled circle in white text, the second
is a plain large green #2C846A numeral with no container, the third sits under a
simple green line icon. Circles are always solid filled - never draw an outline or
stroked circle, the source has no strokes at all. Item contents: {항목목록}. No panel,
no card, no gradient, no border.
```

#### closing
```
Closing slide on plain #FFFFFF, everything centered. At the top, a small uppercase
bold 23px gray #A3A3A3 label "{섹션라벨}". Below it a very large bold centered
headline in two colors, the opening words in near-black #000000 and the key phrase in
green #2C846A: "{감사문구}". Below that, centered bold body text at a much smaller
size, beginning in near-black #000000 and trailing off in gray #A3A3A3:
"{안내문구}". Large empty space in the bottom half. No background color, no
decoration.
```

### 5-2. 이미지형 4종 — 사용자 첨부 이미지 필요

이 4종은 `references/image-slides.md`의 절차를 함께 따른다. 프롬프트 맨 뒤에
PLACEHOLDER BLOCK을 붙여 이미지 자리를 빈 회색 사각형으로 만들고, 실제 이미지는
3단계 pptx 조립에서 얹는다. **아래 블록의 이미지 묘사는 자리 크기와 방향을
정하기 위한 것이며, 글자는 이미지 영역 밖에만 둔다.**

원본 `#09`는 인물 사진을 **원형으로 크롭**해 썼지만, PLACEHOLDER BLOCK이 원형 크롭을
금지하고(그래야 3단계에서 이미지를 정확히 얹을 수 있다) 조립 스크립트에도 원형 크롭
기능이 없다. 원형이 필요하면 **미리 원형으로 크롭한 투명 배경 PNG**를 받아
`"fit": "contain"`으로 얹는다.

#### photo-highlight
```
Statement slide on plain #FFFFFF. Right side: one image area showing {사진묘사}, a
plain rectangle filling the right 45% of the slide, flush with the top, right and
bottom edges. Left side with generous margins: a small uppercase bold 23px gray
#A3A3A3 label "{섹션라벨}"; below it a large bold two-line headline where the first
line is near-black #000000 and the second line is green #2C846A, with "{강조단어}"
as the green part: "{헤드라인}". Below the headline, after a large gap, a short
bulleted list in near-black at small size: "{캡션}". All text stays in the left half
and never overlaps the image area. No highlight box, no underline, no vertical rule.
```

#### image-full
```
Content slide on plain #FFFFFF. The top 72% of the slide is one wide image area
showing {사진묘사}, spanning the full width from the left edge to the right edge. The
bottom 28% is plain white, containing on the left a small uppercase bold 23px gray
#A3A3A3 label "{섹션라벨}" with a large bold headline under it in two colors,
near-black #000000 and green #2C846A: "{헤드라인}", and on the right a small gray
#737373 caption "{캡션}". No text appears over the image area. No borders.
```

#### image-compare
```
Comparison slide on plain #FFFFFF. Top left: a small uppercase bold 23px gray
#A3A3A3 label "{섹션라벨}"; under it a large bold headline in two colors, near-black
#000000 and green #2C846A: "{제목}". Below the headline, two equal image areas side
by side with a wide gap between them: the left one shows {좌사진묘사}, the right one
shows {우사진묘사}. Under each image area a short bold caption in green #2C846A:
left "{좌캡션}", right "{우캡션}". No text appears over the image areas. No borders,
no shadows.
```

#### logo-grid
```
Content slide on plain #FFFFFF, everything centered. At the top, a small uppercase
bold 23px gray #A3A3A3 label "{섹션라벨}". Below it a large bold centered headline
in two colors, near-black #000000 and green #2C846A: "{제목}". Below, a row of
{항목수} evenly spaced image areas of equal size across the full width. Under each
image area, centered: a bold green #2C846A name line, then a small bold near-black
role line, then two lines of small near-black description. At the very bottom,
centered small gray #A3A3A3 text "{마무리문구}". No text appears over the image
areas. No decoration.
```

## 6. DESIGN.md 본문

```markdown
# DESIGN.md — Kiwik Green Pitch Deck

## Colors
- primary: #2C846A        # headline key phrase, icons, figures, cover background
- primaryLite: #2D9F7A    # outer ring of nested shapes
- primaryDark: #1E6B52    # middle ring of nested shapes
- primaryDarkest: #0E3327 # inner ring of nested shapes
- neutral800: #000000     # headlines and item titles
- neutral500: #737373     # body text
- neutral400: #A3A3A3     # top labels, captions, closing notes
- background: #FFFFFF
- white: #FFFFFF
- placeholder: #E0E0E0

## Typography
- label: "Noto Sans KR", Noto Sans, sans-serif; weight 700; uppercase; letter-spacing .1em; color #A3A3A3
- headings: "Noto Sans KR", Noto Sans, sans-serif; weight 700; letter-spacing 0; two-tone (near-black + green)
- body: "Noto Sans KR", Noto Sans, sans-serif; weight 400; line-height 1.4
- letter-spacing: 0 on every level, no exceptions
- scale (1280x720): display figure 96px/900, section & divider headline 64px/900,
  cover title 60px/700, statement headline 54px/700, figure 50px/700, name 35px/700,
  item title 27-28px/700, top label 23px/700 uppercase, item title & body 22px,
  paragraph 20px/400, role 18px/700, small body 16px/400, caption 15px/400
- line-height: 1.2 on display and headline levels, 1.4 on body and captions
- at most three type levels on one slide

## Spacing (1280x720, base unit 17px)
- slide margins: 69px top, bottom, left and right
- label to headline: 17px
- headline block to content: 230px when content sits low, 74px when content starts high
- column gutter: 197px; column pitch 398px (3-up), 614px (2x2)
- grid row pitch: 180px; vertical figure list row pitch: 123px
- inside one item text is tight: title to body 0-10px, name to role 1px, role to description 15px
- cover title to subtitle: 35px; paragraph spacing 4px
- whitespace, not boxes, marks every group boundary

## Sizes
- icon tile 83px, corner radius 14px, white glyph 41-60px inside
- line icon 89-107px
- circular portrait 201px
- nested scale circles 447 / 323 / 171px (1 : 0.72 : 0.38)
- figure circles 256 / 209 / 105px
- full-bleed side image 583x720 (45.5% of the width); inline image or chart about 683x435

## Components
- Section label: small uppercase bold 23px gray line above every headline
- Headline: very large bold, split into a near-black part and a green key phrase
- Item column: no background, no border, no shadow — green line icon, bold near-black
  title, small gray body, placed directly on the white slide
- Icon tile: green rounded square 83px, corner radius 14px, with a 41-60px white line glyph (2x2 layouts)
- Figure: large bold green numeral, optionally inside a solid green filled circle with
  white text. Never an outline circle - the source has no strokes anywhere
- Nested scale diagram: concentric circles from #2D9F7A outward to #0E3327 inward,
  each labelled in white

## Decoration
- none. Whitespace and type contrast carry the design.
- never add corner circles, dashed doodles, vertical rules, blurred glows or gradients

## Rules
- every screen is a 16:9 landscape presentation slide, 1280x720
- this is a static slide, NOT an app screen or dashboard
- no browser UI
- NEVER add buttons, call-to-action buttons, input fields, or any interactive form controls
- NEVER add a global navigation bar (GNB), top header bar, or menu bar
- NEVER add a sidebar, left/right navigation rail, tab bar, or toolbar
- NEVER add a footer of any kind: no footer bar, no page-number strip, no logo/copyright line at the bottom
- slide content fills the whole 1280x720 frame edge to edge
- Korean text must render in "Noto Sans KR"
```

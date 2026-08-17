# 디자인: kiwik-card — ppt.fig 추출 테마 (그린 · 카드형)

이 스킬의 디자인은 이 파일 하나다. 색·폰트·장식·슬라이드별 레이아웃 문구가
모두 여기에 있고, 디자인 변경은 전부 이 파일 안에서 끝낸다.

- **한 줄 성격**: 흰 배경 + 딥그린 강조 + **1px 회색 테두리 카드**. 여백보다
  테두리로 그룹을 나누는 조밀한 분석·리서치 덱.
- **출처**: 사용자 제공 로컬 사본 `ppt.fig` (fig-kiwi v106, 노드 312개,
  최상위 프레임 11장 · 전부 1280×720). 색·타이포·간격·라운드는 노드를 직접 재서
  뽑은 실측값이고, 토큰 정리 결정(4배수 통일·라운드 12 통합·대비 보정)은
  `design-tokens.md`에 근거가 있다.
- **`kiwik.md`와의 관계**: 색 팔레트는 같은 계열이지만 **레이아웃 언어가 다르다.**
  `kiwik`은 카드·테두리를 일절 쓰지 않고 여백으로만 그룹을 나누며 헤드라인이
  64px로 크다. `kiwik-card`는 테두리 카드를 기본 그릇으로 쓰고 헤드라인이 44px로
  작으며 한 슬라이드에 담는 정보량이 많다. **둘을 섞지 않는다.**
- **권장 흐름**: cover → divider → 본문 2~3장 → divider → 본문 → closing.

### 원본에서 확인한 사실

- 변수·공유 스타일이 **0개다.** 아래 토큰 이름은 사용 빈도와 역할로 유도한 것이며,
  값은 파일에서 그대로 읽었으므로 정확하다.
- `effects` 0건 — **그림자·블러를 쓰지 않는다.** 깊이는 테두리로만 표현한다.
- `layoutGrids` 0건 — 그리드를 걸지 않고 오토레이아웃으로 잡았다.
- 내장 이미지 0개 — 원본은 사진 없는 순수 텍스트 덱이다.
- 알파가 1.0이 아닌 색이 **하나도 없다.** 반투명을 쓰지 않는다.

## 1. 색상 토큰

| 토큰 | 값 | 용도 | 근거 |
|---|---|---|---|
| Primary | #2C846A | 강조 수치, 아이콘 타일, 표지 배경 | 32회 (글자 24 + 배경 8) |
| PrimaryLite | #2D9F7A | 밝은 그린 면, 번호 강조 | 2회 |
| PrimaryDark | #1E6B52 | 중간 단계 그린 | 1회 |
| PrimaryDarkest | #0E3327 | 인용문 글자, 가장 어두운 그린 | 4회 |
| Neutral800 | #000000 | 제목, 표 헤더, 카드 제목 | 45회 |
| Neutral500 | #737373 | 본문, 캡션, 보조 라벨 | 63회 + 대비 보정분 20회 |
| Neutral400 | #A3A3A3 | **테두리 전용** | 선 47회 |
| Background | #FFFFFF | 슬라이드 배경 | |
| Surface | #FFFFFF | 카드 배경 — 배경과 같은 흰색이고 **테두리로만 구분한다** | 16회 |
| White | #FFFFFF | 그린 면 위 글자 | 10회 |
| Placeholder | #E0E0E0 | 이미지 자리 | |

**`Neutral400`(#A3A3A3)은 글자에 쓰지 않는다.** 흰 배경 대비 2.52:1로 본문
기준(4.5:1)에 미달한다. 원본은 캡션·URL 등 글자 20곳에 썼으나 전부 `Neutral500`
(#737373, 4.74:1)로 올렸다. 테두리는 대비 기준을 받지 않으므로 그대로 둔다.

`Primary`(#2C846A)도 4.55:1로 여유가 거의 없다. **더 밝은 그린으로 바꾸면
바로 미달한다.**

## 2. 타이포그래피

- 라틴: Inter / 한글: **항상 Noto Sans KR** (소스가 뭐든 고정)
- 혼용 스택: `"Inter", "Noto Sans KR", sans-serif`
- 두께는 Regular / Medium / Bold 세 단. 표지 헤드라인만 Black.
- **자간은 전부 0이다.** 168개 TEXT 노드 중 0이 아닌 것은 하나뿐이라 무시한다.

### 2-1. 위계 표 (역할 → 크기·두께)

| 계층 | 역할 | 1280 기준 | 두께 | 행간 | 색 |
|---|---|---|---|---|---|
| D1 | 표지 헤드라인 | **64** | Black 900 | 1.2 | White |
| D2 | 디바이더 헤드라인 | **60** | Bold 700 | 1.2 | White |
| H1 | 슬라이드 제목 | **44** | Bold 700 | 1.0 | #000000 (강조구 Primary) |
| H2 | 섹션 번호 | **34** | Bold 700 | 1.0 | Primary / Neutral500 |
| H2 | 인용문 | **28** | Medium 500 | 1.0 | #0E3327 |
| H3 | 대상 이름 | **23** | Bold 700 | 1.0 | #000000 |
| **L** | **상단 섹션 라벨 (대문자)** | **23** | Bold 700 | 1.0 | Neutral500 |
| H4 | 카드 소제목 | **20** | Bold 700 | 1.0 | #000000 |
| B1 | 표 헤더·강조 본문 | **17** | Bold 700 | 1.0 | #000000 |
| B1 | 본문·표 내용 | **17** | Regular 400 | 1.0 | Neutral500 |
| B1 | 강조 수치 | **17** | Bold 700 | 1.0 | Primary |
| B2 | 여러 줄 본문·불릿 | **16** | Regular 400 | **1.5** | Neutral500 |
| B3 | 작은 본문 | **15** | Regular 400 | 1.5 | Neutral500 |
| C | 머리말·꼬리말 (대문자) | **15** | Medium 500 | 1.0 | Neutral500 |
| C | 출처·연도 캡션 | **13** | Regular 400 | 1.4 | Neutral500 |

`kiwik`과 달리 **한 슬라이드에 4~5개 계층이 함께 온다.** 라벨 + 제목 + 카드
소제목 + 본문이 기본 세트다. 정보 밀도가 높은 덱이라 계층을 줄이지 않는다.

### 2-2. 행간 규칙

원본은 네 값을 쓴다: 1.0 · 1.2 · 1.4 · 1.5.

- **1.0은 한 줄 전용이다.** 원본에서 1.0을 쓴 146건이 전부 한 줄이었다.
  여러 줄에 쓰면 줄이 붙는다.
- **여러 줄이 들어갈 수 있는 자리에는 1.5를 쓴다.** 원본도 불릿·설명문에 1.5를 썼다.
- 60px 이상 대형 헤드라인만 1.2.
- 13px 캡션은 1.4.

### 2-3. 대문자 라벨

영문 라벨 3종(상단 섹션 라벨 23px, 머리말·꼬리말 15px, 기준 라벨 14px)이 전부
대문자다. **대문자 변환이 이 덱의 가장 뚜렷한 서명이다.** 자간은 넓히지 않는다.

## 2.5. 여백·간격 토큰 (spacing)

원본은 오토레이아웃을 쓴다(124프레임). 아래는 그 값을 **4의 배수로 통일한** 결과다.
원본의 17배수 계열(17·34)과 비4배수 값(14·69·51)을 흡수했다.

**기본 단위는 4px이고 실제로 쓰는 값은 8 / 12 / 16 / 20 / 24 / 28 / 32다.**

### 2.5-1. 슬라이드 그리드

| 항목 | 값 | 비고 |
|---|---|---|
| 슬라이드 | **1280 × 720** | 16:9. 원본 11장 전부 동일 |
| 상하좌우 여백 | **68** | 원본 69 → 4배수 스냅 |
| 콘텐츠 영역 | **1144 × 584** | 1280 − 68×2 |
| 열 수 | **3열** | |
| 열 폭 | **360** | 1144 = 360×3 + 32×2 로 정확히 떨어진다 |
| 거터 | **32** | |

**마진 68은 임의로 고른 값이 아니다.** 4배수 후보 64/68/72 중 68만 열 폭이
360이라는 정수로 떨어진다. 다른 값을 쓰면 소수점이 생긴다.

### 2.5-2. 반복 간격

| 항목 | 값 |
|---|---|
| 라벨 → 제목 | **16** |
| 제목 → 콘텐츠 | **32** |
| 카드 안쪽 여백 (4방향) | **16** |
| 카드 안 요소 사이 | **8** |
| 칩·배지 안쪽 상하 여백 | **12** |
| 카드 사이 세로 간격 | **16** |
| 묶음 사이 간격 | **32** |
| 표 행 사이 | **8** |

간격이 전반적으로 **작고 촘촘하다.** `kiwik`이 197~230px 단위로 크게 띄우는 것과
정반대다. 이 덱은 **테두리가 그룹 경계**라서 여백으로 나눌 필요가 없다.

### 2.5-3. 요소 크기

| 요소 | 값 |
|---|---|
| 아이콘 타일 (라운드 사각) | **68 × 68** (라운드 12) |
| 칩·배지 높이 | **48** (상하 여백 12 + 내용 20) |
| 작은 배지 | **85 × 22** (라운드 4) |
| 3열 카드 | **360 × 320** |
| 가로 전폭 카드 | **1144 × 81** 또는 **1144 × 130** |

## 3. 장식 언어

**테두리가 이 덱의 디자인이다.** `kiwik`이 여백으로 하는 일을 여기서는 선이 한다.

- 카드는 **흰 배경 + 1px #A3A3A3 테두리 + 라운드 12**다. 배경색으로 구분하지 않는다.
- 테두리 정렬은 **INSIDE**로 고정한다(원본 49회 중 49회).
- **그림자·블러·그라디언트를 쓰지 않는다.** 원본 `effects` 0건이다.
  깊이가 필요하면 테두리를 2px로 굵히는 것이 유일한 수단이다.
- 슬라이드 상단에 **회색 대문자 라벨** 한 줄 — `kiwik`과 공통되는 서명이다.
- 아이콘은 **그린 라운드 사각 타일 68px + 흰 글리프**.
- 수치는 **그린 큰 숫자**로 쓴다. 점수는 `26 / 30` 형태로 분모를 함께 적는다.
- 반투명·모서리 장식·점선·세로 룰·블러 글로우는 쓰지 않는다.

## 4. STYLE BLOCK

```
Style: dense analytical research deck on a white background, where thin outlined
cards - not whitespace - separate every group. Colors: primary deep green #2C846A,
light green #2D9F7A, dark green #1E6B52, darkest green #0E3327, near-black text
#000000, body gray #737373, border gray #A3A3A3, white background #FFFFFF.
Typography: Inter for Latin text and "Noto Sans KR" for Korean text, in regular
400, medium 500 and bold 700 only. Letter-spacing is exactly 0 everywhere, never
tracked out. A small uppercase bold 23px gray #737373 label sits above a bold 44px
near-black slide title whose key phrase is green, with card titles at 20px bold and
body text at 17px. Line-height 1.0 on single lines and 1.5 wherever text can wrap.
Spacing is built on a 4px unit: 68px slide margins on all four sides, a three-column
grid of 360px columns with 32px gutters, 16px padding inside every card, 8px between
elements inside a card and 32px between groups. Every card is a plain white rectangle
with a 1px #A3A3A3 border drawn inside the shape and a 12px corner radius. Absolutely
no drop shadows, no gradients, no blurred glows, no translucency and no decorative
corner shapes: depth comes only from the thin border. Icons are green #2C846A
rounded-square tiles 68px with a 12px corner radius and a white glyph inside.
```

## 5. 원형 블록 9종

### 5-1. 텍스트형 5종

#### cover
```
Cover slide. Background solid flat green #2C846A with no gradient, no glow and no
decoration at all. Left aligned with 68px margins: a small uppercase bold 17px white
label "{섹션라벨}" near the top, then in the vertical middle a very large 64px
black-weight white heading with line-height 1.2 "{주제목}", and under it one 24px
medium white line "{부제}". At the bottom left a small uppercase medium 15px white
line "{하단문구}". No cards, no borders, no shapes on this slide.
```

#### divider
```
Section divider slide. Background solid flat green #2C846A, no gradient and no
decoration. Everything left aligned with 68px margins. At the top, a small uppercase
bold 23px white label "{섹션라벨}". In the vertical middle, a very large 60px bold
white heading with line-height 1.2 "{섹션문구}", and under it two short 20px medium
white lines "{보조문구}". Nothing else on the slide. No cards, no borders.
```

#### card-grid
```
Content slide on plain #FFFFFF with 68px margins. Top left: a small uppercase bold
23px gray #737373 label "{섹션라벨}"; 16px under it a bold 44px near-black #000000
title whose key phrase is green #2C846A: "{제목}". Leave a 32px gap, then a row of
{카드수} equal columns 360px wide with 32px gutters. Each column is a white
rectangle with a 1px #A3A3A3 border drawn inside the shape and a 12px corner radius,
with 16px padding inside. Inside each card, stacked with 8px gaps: a green #2C846A
rounded-square tile 68px with a 12px corner radius and a white line glyph, then a
bold 20px near-black title, then two or three lines of 16px gray #737373 body text
with line-height 1.5. Column contents: {카드목록}. No drop shadow, no gradient, no
fill colour difference between the card and the slide - only the thin border
separates them.
```

#### split-panel
```
Content slide on plain #FFFFFF with 68px margins. Top left: a small uppercase bold
23px gray #737373 label "{섹션라벨}"; 16px under it a bold 44px near-black #000000
title with the key phrase in green #2C846A: "{제목}". Below, a full-width white
rectangle 1144px wide with a 1px #A3A3A3 border inside and a 12px corner radius,
holding a simple table: a header row in bold 17px near-black, then {항목수} rows of
regular 17px gray #737373 text separated by 8px, each row ending with a bold 17px
green #2C846A score written as a fraction like "26 / 30". Row contents: {항목목록}.
No zebra striping, no cell borders, no shadow - one outer border only.
```

#### closing
```
Closing slide on plain #FFFFFF with 68px margins, everything left aligned. At the
top, a small uppercase bold 23px gray #737373 label "{섹션라벨}". 16px under it a
bold 44px near-black #000000 heading with the key phrase in green #2C846A:
"{감사문구}". Leave a 32px gap, then a single full-width white rectangle with a 1px
#A3A3A3 border inside and a 12px corner radius, 16px padding, containing a 28px
medium quote in darkest green #0E3327: "{안내문구}". Large empty space at the
bottom. No decoration, no shadow.
```

### 5-2. 이미지형 4종 — 사용자 첨부 이미지 필요

이 4종은 `references/image-slides.md`의 절차를 함께 따른다. 프롬프트 맨 뒤에
PLACEHOLDER BLOCK을 붙여 이미지 자리를 빈 회색 사각형으로 만들고, 실제 이미지는
3단계 pptx 조립에서 얹는다. **아래 블록의 이미지 묘사는 자리 크기와 방향을
정하기 위한 것이며, 글자는 이미지 영역 밖에만 둔다.**

이 테마에서는 **이미지 자리도 카드와 같은 규격**을 따른다: 라운드 12,
1px #A3A3A3 테두리.

#### photo-highlight
```
Statement slide on plain #FFFFFF with 68px margins. Right side: one image area
showing {사진묘사}, a plain rectangle 544px wide with a 12px corner radius and a 1px
#A3A3A3 border, vertically centered. Left side: a small uppercase bold 23px gray
#737373 label "{섹션라벨}"; 16px below it a bold 44px two-line heading where the
first line is near-black #000000 and "{강조단어}" is green #2C846A: "{헤드라인}".
After a 32px gap, a short bulleted list at 16px gray #737373 with line-height 1.5:
"{캡션}". All text stays in the left half and never overlaps the image area.
```

#### image-full
```
Content slide on plain #FFFFFF with 68px margins. The upper area is one wide image
area showing {사진묘사}, 1144px wide with a 12px corner radius and a 1px #A3A3A3
border. Below it, after a 32px gap, on the left a small uppercase bold 23px gray
#737373 label "{섹션라벨}" with a bold 44px heading under it in near-black #000000
and green #2C846A: "{헤드라인}", and on the right a 16px gray #737373 caption with
line-height 1.5 "{캡션}". No text appears over the image area.
```

#### image-compare
```
Comparison slide on plain #FFFFFF with 68px margins. Top left: a small uppercase
bold 23px gray #737373 label "{섹션라벨}"; 16px under it a bold 44px heading in
near-black #000000 with the key phrase in green #2C846A: "{제목}". Below, after a
32px gap, two equal image areas side by side with a 32px gutter, each 556px wide
with a 12px corner radius and a 1px #A3A3A3 border: the left shows {좌사진묘사}, the
right shows {우사진묘사}. Under each, a bold 20px green #2C846A caption: left
"{좌캡션}", right "{우캡션}". No text appears over the image areas.
```

#### logo-grid
```
Content slide on plain #FFFFFF with 68px margins. Top left: a small uppercase bold
23px gray #737373 label "{섹션라벨}"; 16px under it a bold 44px heading in near-black
#000000 with the key phrase in green #2C846A: "{제목}". Below, after a 32px gap, a
row of {항목수} equal white cards 360px wide with 32px gutters, each with a 12px
corner radius and a 1px #A3A3A3 border and 16px padding. Inside each card, stacked
with 8px gaps: a square image area at the top, then a bold 20px near-black name
line, then two lines of 16px gray #737373 description with line-height 1.5. Card
contents: {항목목록}. At the very bottom, a small uppercase medium 15px gray #737373
line "{마무리문구}". No text appears over the image areas.
```

## 6. DESIGN.md 본문

```markdown
# DESIGN.md — Kiwik Card Research Deck

## Colors
- primary: #2C846A        # figures, icon tiles, cover background, key phrases
- primaryLite: #2D9F7A    # lighter green accents
- primaryDark: #1E6B52    # mid green
- primaryDarkest: #0E3327 # quotes, darkest green
- neutral800: #000000     # titles, table headers, card titles
- neutral500: #737373     # body text, captions, labels
- neutral400: #A3A3A3     # borders only - never used for text
- background: #FFFFFF
- surface: #FFFFFF        # cards are the same white, separated by a border
- white: #FFFFFF
- placeholder: #E0E0E0

## Typography
- label: "Inter", "Noto Sans KR", sans-serif; weight 700; uppercase; letter-spacing: 0em; color #737373
- headings: "Inter", "Noto Sans KR", sans-serif; weight 700; letter-spacing: 0em; two-tone (near-black + green)
- body: "Inter", "Noto Sans KR", sans-serif; weight 400; line-height 1.5
- letter-spacing: 0em on every level, no exceptions
- scale (1280x720): cover headline 64px/900, divider headline 60px/700,
  slide title 44px/700, section number 34px/700, quote 28px/500,
  subject name 23px/700, top label 23px/700 uppercase, card title 20px/700,
  body and table 17px/400, wrapping body 16px/400, small body 15px/400,
  running head 15px/500 uppercase, source caption 13px/400
- line-height: 1.0 for single-line text only, 1.5 wherever text can wrap,
  1.2 on 60px+ display headlines, 1.4 on 13px captions
- four or five type levels on one slide is normal for this deck

## Spacing (1280x720, base unit 4px)
- slide margins: 68px top, bottom, left and right
- content area: 1144 x 584
- three columns of 360px with 32px gutters
- label to title: 16px; title to content: 32px
- card padding: 16px on all four sides; gap between elements inside a card: 8px
- gap between cards: 16px vertically; between groups: 32px
- table row gap: 8px; chip vertical padding: 12px
- spacing is tight throughout - the border, not the whitespace, marks the boundary

## Sizes
- icon tile 68px square, corner radius 12px, white glyph inside
- chip height 48px (12px padding + 20px content)
- small badge 85x22, corner radius 4px
- three-up card 360x320; full-width card 1144x81 or 1144x130
- side image area 544px wide; full-width image area 1144px; compare image 556px

## Components
- Section label: small uppercase bold 23px gray line above every title
- Title: bold 44px, split into a near-black part and a green key phrase
- Card: white rectangle, 1px #A3A3A3 border drawn inside, 12px corner radius,
  16px padding. Same fill as the slide - only the border separates it
- Icon tile: green rounded square 68px, corner radius 12px, white glyph
- Score: bold green numeral written as a fraction, e.g. "26 / 30"
- Table: one outer bordered card, bold header row, 8px row gaps, no cell borders
  and no zebra striping

## Decoration
- the thin border is the design. Depth comes from the border, never from shadow
- never add drop shadows, gradients, blurred glows, translucency, corner circles,
  dashed doodles or vertical rules
- borders are always 1px #A3A3A3 aligned INSIDE; 2px only for emphasis

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
- #A3A3A3 is a border colour only - never use it for text (contrast 2.52:1 fails)
```

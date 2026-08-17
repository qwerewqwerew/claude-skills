# Stitch 프롬프트 템플릿

모든 프롬프트는 [STYLE BLOCK] + [슬라이드 유형 블록] 순서로 조립한다.
`{중괄호}` 자리에 1단계 구성안의 실제 한국어 텍스트를 넣는다.
아래 블록들이 여러 줄로 적혀 있는 것은 이 문서에서 읽기 편하도록 나눈 것일 뿐이다.
**조립할 때는 모든 줄바꿈과 빈 줄을 공백 하나로 바꿔, 슬라이드 하나당 줄바꿈 없는
한 문단짜리 프롬프트로 완성한다.** 사용자가 한 번에 복사해 Stitch에 붙여넣기 위함이다.
완성된 프롬프트는 Stitch 도구에 직접 넘기거나(2-1), 권한이 막히면 md 문서에
슬라이드마다 코드 블록 하나로 담아 저장한다(2-2). 채팅창에는 나열하지 않는다.

## STYLE BLOCK (모든 프롬프트의 첫 단락)

```
Design a single 5:4 presentation slide, landscape 1280x1024, as one full-width
web page section with no browser chrome, no scrolling. This is a static
presentation slide, NOT an app screen or dashboard: absolutely no global
navigation bar (GNB), no top header bar, no menu bar, no sidebar, no left/right
navigation rail, no tab bar, no toolbar, and no footer of any kind (no footer
bar, no page-number strip, no logo/copyright line at the bottom). No interactive
UI controls at all: no buttons, no call-to-action buttons, no input fields, no
form elements. The slide content fills the entire 1280x1024 frame edge to edge.
Style: modern business pitch deck. Colors: primary orange #F48120, dark charcoal
#212121, body text gray #424242, light background #FAFAFA, card background #F5F5F5.
Typography: bold geometric sans-serif; use "Noto Sans KR" for Korean text and
Poppins for Latin text; headings bold with slightly tight letter-spacing.
Decorative language: soft blurred orange glow in one corner, large circles cropped
at the edges, thin 2px orange vertical rules, dashed orange doodle lines.
Keep the layout clean with generous whitespace.
```

## DESIGN.md (Stitch 프로젝트에 등록할 스타일 문서)

2단계 문서 앞부분에 아래 전문을 넣고, Stitch 프로젝트 설정에서 DESIGN.md로
등록하도록 안내한다. 등록 후에는 각 프롬프트의 STYLE BLOCK을 유지하되,
Stitch가 이미 스타일을 기억하므로 결과 편차가 줄어든다.

```markdown
# DESIGN.md — Orange Pitch Deck

## Colors
- primary: #F48120        # accent text, icons, highlight boxes, closing background
- primaryGradient: linear-gradient(180deg, #F5994C, #F48120)
- neutral900: #212121     # dark cover background
- neutral800: #424242     # headings and body on light backgrounds
- neutral100: #F5F5F5     # card background
- background: #FAFAFA
- white: #FFFFFF

## Typography
- headings: "Noto Sans KR", Poppins, sans-serif; weight 700; letter-spacing -0.02em
- body: "Noto Sans KR", Poppins, sans-serif; weight 400; line-height 1.5; text-align justify
- scale (1280x1024): cover title 64px, divider display 106px, section heading 43px,
  card title 24px, body 16px

## Components
- Card: background #F5F5F5, no border, inner padding 22px, orange line icon on top,
  bold title, justified body text
- Orange panel: rounded 16px, primaryGradient background, white bold titles,
  white body text, white line icons
- Highlight: orange box behind a keyword with white text, or thick orange underline
- Rule: 2px vertical orange line separating heading from description

## Decoration
- circles cropped at slide corners (gray or orange, 100-235px)
- soft blurred orange glow in one corner of light slides
- dashed orange doodle lines (e.g. flight path with paper plane)

## Rules
- every screen is a 5:4 landscape presentation slide, 1280x1024
- this is a static slide, NOT an app screen or dashboard
- no browser UI
- NEVER add buttons, call-to-action buttons, input fields, or any interactive form controls
- NEVER add a global navigation bar (GNB), top header bar, or menu bar
- NEVER add a sidebar, left/right navigation rail, tab bar, or toolbar
- NEVER add a footer of any kind: no footer bar, no page-number strip, no logo/copyright line at the bottom
- slide content fills the whole 1280x1024 frame edge to edge
- Korean text must render in "Noto Sans KR"
```

## 유형별 블록

### cover — 다크 표지

```
Dark cover slide. Background #212121 with a faint orange glow in the top-left
corner. Left-aligned two-line title block, vertically centered: first line in
white bold "{부제 또는 한 줄 소개}", second line in orange #F48120 bold
"{회사명 또는 발표 제목}". On the right half, a large abstract orange logo shape,
heavily blurred and cropped by the slide edge, as a background motif.
```

### divider — 섹션 디바이더

```
Section divider slide. Background #FAFAFA with soft gray and orange blurred
glows in opposite corners. In the center, a huge bold display heading in orange
#F48120 (or dark gray #424242), font size around 106px, one or two lines:
"{섹션 질문 문구}". No other content.
```

### card-grid — 카드 그리드

```
Content slide on #FAFAFA. Top area: on the left a large two-line bold heading in
#424242 "{슬라이드 제목}"; a thin 2px vertical orange rule; on the right a
justified paragraph in orange #F48120 "{리드 문단}". Below, a row of {N} equal
cards with background #F5F5F5: each card has an orange line icon on top, a bold
dark title, and a small justified body text. Card contents:
1. "{카드1 제목}" — "{카드1 본문}"
2. "{카드2 제목}" — "{카드2 본문}"
3. "{카드3 제목}" — "{카드3 본문}"
{4. ...}
A small orange circle cropped at one slide corner as decoration.
```

### split-panel — 좌우 분할 리스트

```
Content slide on #FAFAFA. Left half: large bold heading in #424242 with the key
word in orange "{슬라이드 제목}", below it a small italic subtitle
"{부제 한 줄}", and a dashed orange doodle line drawing (curved flight path with
a paper plane) as decoration. Right half: a rounded 16px panel with a vertical
orange gradient from #F5994C to #F48120, containing three stacked items; each
item has a white bold title, a small white line icon on the right, and white
body text. Items:
1. "{항목1 제목}" — "{항목1 본문}"
2. "{항목2 제목}" — "{항목2 본문}"
3. "{항목3 제목}" — "{항목3 본문}"
```

### photo-highlight — 사진 강조

```
Statement slide on #FAFAFA. Right side: a black-and-white photo of {사진 묘사}
inside a large light-gray circle, cropped by the slide edge. Left side: a large
bold multi-line headline in #424242 "{헤드라인}", with the key words
"{강조 단어}" highlighted by a solid orange box with white text and a hand-drawn
orange underline. A thin 2px vertical orange rule on the far left, and one small
italic caption line at the bottom: "{캡션}".
```

### logo-grid — 로고/항목 그리드

```
Content slide on #FAFAFA. Centered bold heading at the top in #424242
"{슬라이드 제목}". Below, a 3-column grid of {로고 개수} grayscale partner logos
(placeholder logos are fine), evenly spaced. At the bottom center a small gray
text "{마무리 문구}". Small orange circles cropped at two corners as decoration.
```

### closing — 마무리

```
Closing slide. Full background solid orange #F48120. Left-aligned white huge
bold heading "{감사 문구}", and below it two short white body lines:
"{질문 유도 문구}". Minimal, no decoration.
```

## 프롬프트 작성 요령

- 최종 프롬프트는 줄바꿈 없는 한 문단으로 출력한다. 이 문서 블록에 있는 줄바꿈은
  전부 공백으로 치환한다. 문단이 나뉘어 있으면 사용자가 여러 번 붙여넣어야 하므로 금지.
- 한 프롬프트 = 한 슬라이드. Stitch 한 프로젝트 안에서 화면을 추가해 나가야
  스타일이 유지된다.
- 한국어 문구는 반드시 큰따옴표 안에 원문 그대로 넣는다. 번역하지 않는다.
- 카드·항목 수가 템플릿과 다르면 {N}만 바꾸고 구조 설명은 유지한다.
- 도표·차트가 필요한 슬라이드는 card-grid를 변형해 "a simple bar chart in orange
  tones" 식으로 시각 요소만 추가한다. 복잡한 데이터는 Stitch보다 pptx에서 넣는 편이 정확하다.

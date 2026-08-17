# 전량 추출 — .fig / .deck에서 뽑을 수 있는 값을 하나도 빠뜨리지 않고 뽑는다

필드 목록 확인일 **2026-07-28** / 확인 대상 `fig-kiwi@0.0.1`, `kiwi-schema@0.5.0`.
실파일 검증: `fig-kiwi v106` 로컬 사본 1개(노드 312개, 스키마 정의 627개,
데이터 청크 zstd 압축). 항목표는 `fig-kiwi@0.0.1` 타입 정의 기준이라 v106보다
좁다 — 실제로 v106의 `NodeChange`에는 항목표에 없는 필드가 437개 더 있었다.
**항목표가 아니라 `schema.json` 덤프가 그 파일의 정답이다.**

이 문서는 전량 추출 경로의 작업 지시문이다. 용도에 맞춘 축약(PPT 테마 6색 등)은
`fig-extract.md`가 맡는다. **먼저 이 문서대로 전량을 뽑아 원본 대장을 만들고,
축약은 그 다음이다.**

## 0. 지켜야 할 원칙

1. **먼저 스키마를 본다.** 필드 목록을 외워서 쓰지 않는다. 그 파일에 실제로 존재하는
   필드를 덤프해 확인한 뒤 그 안에서만 값을 뽑는다.
2. **버리지 않는다.** "PPT에 필요한 색 6개"처럼 용도에 맞춰 미리 줄이지 않는다.
3. **근거를 같이 적는다.** 값마다 어디서 나왔는지를 함께 기록하고, 추정으로 잡힌
   값은 확인 대상으로 따로 표시한다.
4. **모르면 모른다고 쓴다.** 필드가 없으면 `null`이 아니라 `"미확인"`으로 적고,
   어떤 필드를 찾아봤는지 남긴다. 그럴듯한 기본값으로 메우지 않는다.

## 1. 작업 지시문

아래 블록을 그대로 따른다.

```
너는 Figma 로컬 사본(.fig / .deck)에서 디자인 토큰을 추출하는 작업을 한다.
목표는 "이 파일에서 뽑을 수 있는 값을 하나도 빠뜨리지 않고 뽑아 구조화하는 것"이다.
용도에 맞춰 미리 줄이지 마라. 축약은 사용자가 따로 요청할 때만 한다.

■ 절대 규칙
1. 파일에 없는 값을 지어내지 마라. 필드가 없으면 "미확인"으로 적는다.
2. 값마다 출처를 함께 적어라. 출처는 다음 4가지 중 하나다.
   variable(Figma 변수) / style(공유 스타일) / label(이름표가 붙은 견본) / infer(빈도 추정)
   infer로 잡힌 값은 결과 맨 뒤 "확인 필요" 목록에 다시 모아라.
3. .fig / .deck은 Figma 비공개 포맷이라 공식 지원 경로가 아니다. 디코딩이 실패하면
   파서를 억지로 고치지 말고, 실패한 지점과 증상을 그대로 보고하고 멈춰라.
4. 값을 단위 없이 적지 마라. px, %, 배수(ratio), 도(deg)를 항상 명시한다.
5. 색은 8자리 HEX(#RRGGBBAA)와 알파 분리값을 함께 적어라. 알파 1.0도 생략하지 않는다.

■ 1단계 — 열고 스키마부터 확인
1) .fig / .deck은 ZIP 컨테이너다. 다음을 먼저 나열해 보고한다.
   - canvas.fig 유무 (없으면 Figma 로컬 사본이 아니다. 여기서 중단하고 보고)
   - meta.json 내용 (파일 이름, 썸네일 크기 등)
   - images/ 안의 파일 개수와 총 용량
2) canvas.fig는 'fig-kiwi' 매직 + version + [길이][청크] × 2 구조다.
   청크0 = kiwi 스키마, 청크1 = 노드 데이터다.
   압축은 청크마다 다를 수 있으므로 zstd → deflateRaw → 원본 순으로 시도한다.
3) 청크0의 스키마를 디코드해 **이 파일에 실제로 존재하는 필드 이름 전체 목록**을
   먼저 출력한다. 이후 추출은 이 목록 안에서만 한다.
   목록에 있는데 아래 항목표에 없는 필드가 나오면 "미분류 필드"로 따로 모아 보고한다.
4) 노드 타입별 개수를 집계해 보고한다.
   (DOCUMENT / CANVAS / FRAME / GROUP / SECTION / RECTANGLE / ROUNDED_RECTANGLE /
    ELLIPSE / LINE / VECTOR / STAR / REGULAR_POLYGON / BOOLEAN_OPERATION / TEXT /
    SYMBOL / INSTANCE / SLICE / MEDIA / STAMP / WIDGET / VARIABLE 등)

■ 2단계 — 아래 A~N을 전부 추출한다 (하나도 건너뛰지 마라)

A. 파일·문서 메타
   파일명, 포맷 매직과 버전, 스키마/데이터 압축 방식, 노드 총 개수, 노드 타입별 개수,
   페이지(CANVAS) 목록과 각 페이지 배경색, 내장 이미지 목록(해시 파일명·바이트·개수),
   최상위 FRAME 목록(이름·크기·좌표).

B. 색 — 모든 페인트를 전부
   대상 필드: fillPaints, strokePaints, backgroundPaints, backgroundColor,
   prototypeBackgroundColor
   각 Paint에서 다음을 전부 적는다.
   - type: SOLID / GRADIENT_LINEAR / GRADIENT_RADIAL / GRADIENT_ANGULAR /
           GRADIENT_DIAMOND / IMAGE / EMOJI
   - color: r,g,b,a 원본 실수값 + 8자리 HEX
   - opacity, visible, blendMode
   - 그라디언트면 stops 배열 전부: 각 stop의 color(HEX+알파)와 position(0~1),
     그리고 transform 행렬에서 계산한 각도(deg)와 시작·끝 좌표
   - 이미지 채움이면 imageScaleMode(STRETCH/FIT/FILL/TILE), rotation, scale,
     originalImageWidth/Height, 이미지 해시
   - filterColorAdjust(노출·대비·채도 등 보정값)가 있으면 그대로
   숨김 페인트(visible=false)도 버리지 말고 hidden 표시를 달아 포함한다.

C. 타이포그래피 — 텍스트 관련 필드 전부
   fontName(family / style / postscript), fontSize,
   lineHeight(value + units: RAW|PIXELS|PERCENT, 그리고 fontSize로 나눈 배수),
   letterSpacing(value + units), textTracking,
   paragraphIndent, paragraphSpacing, listSpacing,
   textCase(ORIGINAL/UPPER/LOWER/TITLE/SMALL_CAPS/SMALL_CAPS_FORCED),
   textDecoration(NONE/UNDERLINE/STRIKETHROUGH),
   textAlignHorizontal(LEFT/CENTER/RIGHT/JUSTIFIED), textAlignVertical(TOP/CENTER/BOTTOM),
   textAutoResize(NONE/WIDTH_AND_HEIGHT/HEIGHT), textTruncation, hyperlink,
   fontVariations, detachOpticalSizeFromFontSize,
   OpenType 관련 전부: fontVariantCommonLigatures, fontVariantContextualLigatures,
   fontVariantDiscretionaryLigatures, fontVariantHistoricalLigatures, fontVariantOrdinal,
   fontVariantSlashedZero, fontVariantNumericFigure, fontVariantNumericSpacing,
   fontVariantNumericFraction, fontVariantCaps, fontVariantPosition,
   toggledOnOTFeatures, toggledOffOTFeatures,
   textData: characters(원문), fallbackFonts, styleOverrideTable(한 텍스트 안의 부분 서식),
   textListData(listID / bulletType / indentationLevel), directionality.
   ※ 텍스트 스타일이 이름(예: Type/Display/Hero)으로 정리돼 있으면 이름-값 쌍을 그대로 쓴다.
     이름표가 없을 때만 빈도 최빈값을 쓰고 출처를 infer로 적는다.

D. 모서리·형태
   cornerRadius, rectangleTopLeftCornerRadius, rectangleTopRightCornerRadius,
   rectangleBottomLeftCornerRadius, rectangleBottomRightCornerRadius,
   rectangleCornerRadiiIndependent, cornerSmoothing(스쿼클 정도),
   arcData(원호 시작·끝 각도와 안쪽 반지름), starInnerScale, count(별·다각형 꼭짓점 수).

E. 선(스트로크)·테두리
   strokeWeight, strokeAlign(CENTER/INSIDE/OUTSIDE),
   strokeCap(NONE/ROUND/SQUARE/ARROW_LINES/ARROW_EQUILATERAL 등),
   strokeJoin(MITER/BEVEL/ROUND), miterLimit, dashPattern(점선 배열), dashMode,
   borderTopWeight, borderBottomWeight, borderLeftWeight, borderRightWeight,
   borderStrokeWeightsIndependent, borderTopHidden, borderBottomHidden,
   borderLeftHidden, borderRightHidden, bordersTakeSpace.

F. 그림자·블러 (effects 배열 전부)
   각 effect의 type(DROP_SHADOW/INNER_SHADOW/FOREGROUND_BLUR/BACKGROUND_BLUR),
   color(HEX+알파), offset(x,y), radius, spread, visible, blendMode,
   showShadowBehindNode.

G. 레이아웃 — 오토레이아웃과 배치
   stackMode(NONE/HORIZONTAL/VERTICAL), stackSpacing,
   stackPadding, stackHorizontalPadding, stackVerticalPadding,
   stackPaddingRight, stackPaddingBottom,
   stackAlign, stackCounterAlign, stackJustify,
   stackPrimarySizing, stackCounterSizing, stackPrimaryAlignItems, stackCounterAlignItems,
   stackWidth, stackHeight, stackChildPrimaryGrow, stackChildAlignSelf,
   stackPositioning(AUTO/ABSOLUTE), stackReverseZIndex, fixedChildrenDivider,
   size(x,y), transform(위치·회전·스케일 행렬),
   horizontalConstraint / verticalConstraint(MIN/CENTER/MAX/STRETCH/SCALE/FIXED_MIN/FIXED_MAX),
   proportionsConstrained.
   ※ 간격(spacing)과 여백(padding)에 실제로 쓰인 숫자를 전부 모아 빈도순으로 정렬하라.
     4·8 배수 체계가 보이면 그 기준 단위를 함께 보고한다.

H. 레이아웃 그리드·가이드
   layoutGrids 배열 전부: type(MIN/CENTER/STRETCH/MAX), axis(X/Y), numSections,
   offset, sectionSize, gutterSize, color, pattern(STRIPES/GRID), visible.
   guides(자·가이드선) 좌표도 포함한다.

I. 표시 속성
   opacity, blendMode, visible, locked, mask, maskIsOutline, exportContentsOnly,
   backgroundEnabled, backgroundOpacity, frameMaskDisabled, resizeToFit,
   scrollDirection, scrollBehavior, scrollOffset, sectionContentsHidden.

J. Figma 변수(Variables) — 있으면 최우선 근거다
   type이 VARIABLE인 노드 전부에서:
   변수 이름(슬래시 경로 그대로), 설명, 데이터 타입(COLOR/FLOAT/STRING/BOOLEAN),
   변수 컬렉션 이름, **모드(Mode)별 값 전부**(예: Light / Dark / Compact),
   다른 변수를 가리키는 별칭(alias)이면 가리키는 대상 이름,
   기본값(initialValue), 정렬 위치, 삭제 여부(isDeleted), 사용 범위(scope).
   ※ 모드가 2개 이상이면 모드를 열로 하는 표로 만들어라. 라이트/다크 테마의 근거다.
   ※ 어떤 노드의 어떤 속성이 이 변수를 쓰고 있는지(variableData 연결)도 함께 적는다.

K. 공유 스타일(Styles)
   styleID, styleType, styleDescription, isFillStyle, isStrokeStyle, isPublishable,
   inheritFillStyleID, inheritStrokeStyleID, inheritTextStyleID, inheritEffectStyleID,
   inheritGridStyleID, inheritExportStyleID, inheritFillStyleIDForStroke,
   inheritFillStyleIDForBackground, sharedStyleReference, sharedStyleMasterData.
   ※ 스타일 이름과 그 스타일이 담고 있는 실제 값(색/텍스트/효과/그리드)을 짝지어 표로 만든다.

L. 컴포넌트·인스턴스
   SYMBOL(컴포넌트)과 INSTANCE 노드에서:
   컴포넌트 이름, symbolDescription, componentKey, originComponentKey,
   componentPropDefs(속성 id / 이름 / 타입 / 기본값 / preferredValues),
   componentPropRefs, componentPropAssignments,
   isStateGroup, stateGroupPropertyValueOrders(배리언트 조합),
   overriddenSymbolID, sharedSymbolReference, publishFile / publishID / publishedVersion,
   pluginRelaunchData.
   ※ 배리언트 축과 값 목록(예: size=sm|md|lg, state=default|hover)을 표로 정리한다.

M. 내보내기·프로토타입·모션
   exportSettings(suffix / imageType PNG|JPEG|SVG|PDF / constraint / contentsOnly 등),
   prototypeInteractions, interactionType, transitionType, transitionDuration,
   easingType, easingFunction, transitionShouldSmartAnimate, transitionTimeout,
   navigationType, overlayPositionType, overlayBackgroundAppearance,
   connectionType, connectionURL, prototypeDevice, prototypeStartingPoint.
   ※ duration과 easing은 모션 토큰이 되므로 값별 빈도까지 집계한다.

N. 이름·접근성·기타
   모든 노드의 name(레이어 이름) — 슬래시 경로는 토큰 이름의 1순위 근거다.
   htmlTag, ariaRole, accessibleLabel, pluginData, embedData, linkPreviewData,
   codeBlockLanguage, widgetMetadata.

■ 3단계 — 토큰 이름 붙이기
1) 이름 근거 우선순위: ① Figma 변수 이름 → ② 공유 스타일 이름 →
   ③ 이름표가 붙은 견본 프레임(라벨 텍스트 + 색 사각형이 한 칸에 있는 구조) →
   ④ 빈도 추정.
2) 슬래시 경로(color/bg/brand)는 그대로 계층으로 쓴다. 임의로 바꾸지 마라.
3) 이름이 전혀 없어 추정으로 잡은 항목은 전부 "확인 필요"로 분리한다.
4) 같은 값이 여러 이름으로 나오면 합치지 말고 둘 다 남기고, 별칭 관계로 표시한다.

■ 4단계 — 출력
아래 두 가지를 만든다.

(1) tokens.raw.json — 전량 원본 대장. 구조는 이렇게 한다.
{
  "source": { "file": "", "format": "", "version": "", "decodedAt": "" },
  "stats": { "nodeCount": 0, "byType": {}, "imageCount": 0 },
  "schemaFields": [],
  "variables": [ { "name":"", "collection":"", "type":"", "modes":{}, "alias":null,
                   "usedBy":[] } ],
  "styles":   [ { "name":"", "type":"", "value":{}, "description":"" } ],
  "color":    [ { "token":"", "hex8":"", "alpha":1, "paintType":"", "stops":[],
                  "source":"variable|style|label|infer", "count":0 } ],
  "typography":[ { "token":"", "family":"", "style":"", "size":0,
                   "lineHeight":{"value":0,"units":"","ratio":0},
                   "letterSpacing":{"value":0,"units":""},
                   "case":"", "decoration":"", "align":{}, "openType":{},
                   "source":"", "count":0 } ],
  "radius":   [], "stroke": [], "effect": [], "spacing": [], "grid": [],
  "layout":   [], "component": [], "export": [], "motion": [],
  "unclassifiedFields": [],
  "needsConfirmation": [ { "token":"", "value":"", "why":"빈도 추정" } ],
  "notFound": [ "찾아봤지만 이 파일에 없던 항목" ]
}

(2) 요약 보고 — 채팅에는 다음만 짧게 적는다.
   - 파일이 열렸는지, 노드·이미지 개수
   - 변수/스타일이 있었는지 (있으면 토큰 신뢰도가 높다는 뜻)
   - 뽑힌 항목 수: 색 n개, 텍스트 스타일 n개, 라운드 n개, 그림자 n개, 간격 n개 …
   - "확인 필요" 목록 (추정으로 잡은 것)
   - "찾았지만 없던 것" 목록
   JSON 전문을 채팅에 붙여넣지 마라. 파일로 저장해 전달한다.

■ 실패했을 때
- canvas.fig가 없다 → Figma 로컬 사본이 아니다. FigJam이나 다른 앱 파일일 수 있다.
- 청크가 2개가 아니다 → 컨테이너 구조가 바뀌었다. header.version을 보고한다.
- 스키마 디코드 실패 → 새 압축 방식일 수 있다. 청크 앞 4바이트를 16진수로 보고한다
  (zstd는 28 B5 2F FD).
- 노드는 읽히는데 토큰이 빈약하다 → 그 파일에 변수·스타일·이름표가 없는 것이다.
  추정으로 채우지 말고 "이 파일은 디자인 시스템 파일이 아니다"라고 보고한다.
어느 경우든 파서를 억지로 고치려 들지 말고, 증상을 그대로 알리고 사용자에게
Figma에서 값을 직접 확인하는 방법을 제안하라.
```

## 2. 이 스킬에서 1단계를 수행하는 방법

지시문 1단계는 손으로 하지 않는다. `fig_decode.mjs`가 전부 처리한다.

```bash
SKILL="${CLAUDE_PLUGIN_ROOT}/skills/extract-token"
node "$SKILL/scripts/fig_decode.mjs" <파일.fig|.deck> -o message.json --schema schema.json
```

- **1단계 1)** — ZIP 열기, `canvas.fig` 유무 확인, `meta.json` 파싱, `images/` 목록.
  `canvas.fig`가 없으면 스크립트가 안내 후 중단한다.
- **1단계 2)** — 컨테이너 파싱과 zstd → deflateRaw → 원본 순 압축 해제. 실제로 쓰인
  코덱은 콘솔의 `포맷` 줄에 `schema=… , data=…`로 찍힌다.
- **1단계 3)** — `--schema`가 만드는 `schema.json`이 이 항목이다. 반드시 붙인다.
  - `allFieldNames` — 이 파일에 실제로 존재하는 필드명. **추출은 이 목록 안에서만 한다.**
    ENUM 멤버는 필드가 아니므로 여기서 빠져 있다.
  - `enumValues` — 타입별 허용값. 값을 지어내지 않기 위한 근거다.
  - `definitions` — 정의별 필드와 타입, 배열 여부, deprecated 여부.
- **1단계 4)** — 노드 타입별 개수는 콘솔 `노드 타입` 줄에 찍히고, 원본은
  `message.json`의 `message.nodeChanges`에 있다.

A~N 값은 `message.json` 안에 **필드를 고르지 않고 전부** 들어 있다
(`fig_decode.mjs`는 디코드된 message를 통째로 쓴다).

## 3. 2~4단계를 수행하는 방법

집계는 `extract_all.py`가 한다. `message.json`을 손으로 훑지 않는다.

```bash
python "$SKILL/scripts/extract_all.py" message.json -o tokens.raw.json --schema schema.json
```

이 스크립트가 처리하는 것:

- **2단계 A~N 집계** — 같은 값을 합치며 `count`(등장 횟수)와 `nodes`(나온 노드 이름)를
  함께 남긴다. 숨김 페인트는 `hidden: true`로 포함한다.
- **출처 판정** — 노드에 공유 스타일이 붙어 있으면 `style`, 이름이 슬래시 경로면
  `label`, 둘 다 아니면 `infer`. VARIABLE 노드에서 나온 값은 `variable`.
  같은 값이 여러 번 나오면 더 믿을 만한 출처로 승격한다(infer < label < style < variable).
- **단위 부착** — px/%/배수/도/ms를 필드마다 붙인다. 색은 8자리 HEX + `alpha` +
  원본 `rgba` 실수값을 함께 적는다.
- **4단계 출력** — 위 4절 규격의 `tokens.raw.json`. 콘솔에는 요약만 찍는다.
- `needsConfirmation` — `infer`로 잡힌 값 전부.
- `notFound` — 항목표에 있는데 이 파일의 노드에 한 번도 안 나온 필드.
- `unclassifiedFields` — **`NodeChange`의 최상위 필드** 중 항목표에 없는 것.
  `allFieldNames`를 그대로 쓰지 않는 이유는 거기에 중첩 구조체 멤버(`Color.r`,
  `ColorStop.position` 등)가 섞여 있어 "새 필드가 생겼다"는 거짓 신호가 나기 때문이다.
  판정 근거는 `unclassifiedFields.basis`에 적힌다. 결과는 둘로 나뉜다.
  - `present` — 이 파일 노드에 **실제로 나타난** 미분류 필드. 확인해야 할 것.
  - `schemaOnly` — 스키마에만 있고 이 파일은 쓰지 않은 필드. 참고용.
  v106 실측에서 미분류 437개 중 실제 등장은 18개뿐이었다. 나누지 않으면 못 쓴다.
- `document.topLevelFrames` — 부모가 CANVAS인 프레임만 걸러낸 목록. `guid` /
  `parentIndex.guid` 대조로 판정하며 `aspect`(가로세로비)를 함께 적는다.
  16:9 발표 프레임인지 여기서 바로 보인다.

### 스크립트가 하지 않는 것 — 사람이 해야 한다

- **3단계 토큰 이름 붙이기.** 이름표 견본 프레임(라벨 텍스트 + 색 사각형이 한 칸에
  있는 구조) 판독은 구조를 눈으로 읽어야 한다. 스크립트는 노드 **이름이 토큰 경로
  꼴**일 때만 `label`로 본다(각 구간이 글자로 시작하고 점이 없을 것). `26 / 30`,
  `5 / 5`, `apple.com/kr/environment` 같은 본문 텍스트는 걸러진다 — 실제 파일에서
  이런 이름 39개가 잘못 승격돼 확인 목록을 빠져나간 적이 있다.
- **별칭 관계 정리.** 같은 값이 여러 이름으로 나올 때 둘 다 남기고 관계를 표시하는 일.
- **그라디언트 각도 검증.** `gradient.angleDeg`는 행렬 역변환으로 얻은 **유도값**이며
  `derived: true`로 표시된다. 행렬이 없거나 특이행렬이면 미확인이다.
- **행간 RAW 해석 검증.** `PIXELS`→`value/fontSize`, `PERCENT`→`value/100`,
  `RAW`→`value`를 그대로 배수로 읽는다. 환산 근거는 `lineHeight.ratioBasis`에 적힌다.
  RAW를 배수로 보는 것은 v106 실측(값이 1.2~1.5뿐, fontSize 13~64px)에 근거한
  **해석**이다. 다른 파일에서 값 범위가 다르면 이 해석부터 다시 본다.

### 큰 파일 주의

`message.json`은 노드 수에 비례해 커진다. 통째로 읽지 말고 `extract_all.py`에 맡기고,
결과인 `tokens.raw.json`만 읽는다.

## 4. 항목표의 근거

`fig-kiwi@0.0.1`의 타입 정의(`dist/index.d.ts`)에서 뽑은 실제 필드명 대조표다.

| 항목 | 대응하는 실제 필드(발췌) |
|---|---|
| B 색 | `fillPaints` `strokePaints` `backgroundPaints` `backgroundColor` `prototypeBackgroundColor` / Paint 내부: `type` `color(r,g,b,a)` `opacity` `visible` `blendMode` `stops` `transform` `image` `imageScaleMode` `rotation` `scale` `filterColorAdjust` |
| C 타이포 | `fontName` `fontSize` `lineHeight` `letterSpacing` `textTracking` `paragraphIndent` `paragraphSpacing` `listSpacing` `textCase` `textDecoration` `textAlignHorizontal` `textAlignVertical` `textAutoResize` `textTruncation` `hyperlink` `fontVariations` `fontVariant*`(11개) `toggledOn/OffOTFeatures` `textData` `textListData` |
| D 모서리 | `cornerRadius` `rectangle*CornerRadius`(4방향) `rectangleCornerRadiiIndependent` `cornerSmoothing` `arcData` `starInnerScale` `count` |
| E 선 | `strokeWeight` `strokeAlign` `strokeCap` `strokeJoin` `miterLimit` `dashPattern` `border*Weight`(4방향) `border*Hidden`(4방향) `borderStrokeWeightsIndependent` `bordersTakeSpace` |
| F 효과 | `effects` / Effect 내부: `type` `color` `offset` `radius` `spread` `visible` `blendMode` `showShadowBehindNode` |
| G 레이아웃 | `stackMode` `stackSpacing` `stackPadding` `stackHorizontal/VerticalPadding` `stackPaddingRight/Bottom` `stackAlign` `stackCounterAlign` `stackJustify` `stackPrimarySizing` `stackCounterSizing` `stackWidth` `stackHeight` `stackChildPrimaryGrow` `stackChildAlignSelf` `stackPositioning` `stackReverseZIndex` `size` `transform` `horizontal/verticalConstraint` |
| H 그리드 | `layoutGrids` / 내부: `type` `axis` `numSections` `offset` `sectionSize` `gutterSize` `color` `pattern` `visible` · `guides` |
| I 표시 | `opacity` `blendMode` `visible` `locked` `mask` `maskIsOutline` `backgroundEnabled` `backgroundOpacity` `frameMaskDisabled` `scrollDirection` `scrollBehavior` |
| J 변수 | 노드 타입 `VARIABLE` · `variableData` · (파일 내장 스키마의 `variableDataValues.entries`) |
| K 스타일 | `styleID` `styleType` `styleDescription` `isFillStyle` `isStrokeStyle` `inherit*StyleID`(6종+2) `sharedStyleReference` `sharedStyleMasterData` |
| L 컴포넌트 | 노드 타입 `SYMBOL` `INSTANCE` · `symbolData` `componentKey` `componentPropDefs` `componentPropRefs` `componentPropAssignments` `isStateGroup` `stateGroupPropertyValueOrders` `publishFile` `publishID` |
| M 내보내기·모션 | `exportSettings` `prototypeInteractions` `transitionType` `transitionDuration` `easingType` `easingFunction` `navigationType` `overlay*` `connectionType` |
| N 이름·접근성 | `name` `htmlTag` `ariaRole` `accessibleLabel` `pluginData` `embedData` |

### 확인 안 된 부분

- `variableDataValues`(모드별 변수값이 실제로 담기는 곳)는 `fig-kiwi@0.0.1`의 **정적
  타입 정의에는 없다.** 실제 디코딩은 파일 내장 스키마를 쓰므로 패키지 타입보다 필드가
  더 많을 수 있다. 그래서 1단계에서 **그 파일의 스키마를 먼저 덤프**한다.
  추측을 피하려고 넣은 안전장치다.
- 파일마다 Figma 버전이 다르므로 위 표의 필드가 모든 파일에 다 있다고 단정할 수 없다.
  없으면 `notFound`에 기록한다.

## 5. 자가 점검

- [ ] `schema.json`이 만들어졌고 `allFieldNames`가 비어 있지 않은가
- [ ] `variables`가 비어 있지 않은가 — 비었다면 그 파일에 Figma 변수가 없는 것이다
- [ ] 모드가 2개 이상인 변수의 **모든 모드 값**이 다 들어왔는가 (다크 테마 누락 여부)
- [ ] 색이 8자리 HEX로, 알파가 분리돼 적혔는가
- [ ] 그라디언트의 `stops`가 배열째로 들어왔는가 (첫 색만 뽑히지 않았는지)
- [ ] `lineHeight`가 원본 단위와 배수(ratio) 둘 다 적혔는가
- [ ] 4방향 라운드·4방향 테두리 두께가 각각 따로 들어왔는가
- [ ] `needsConfirmation`(추정으로 잡은 값) 목록이 별도로 나왔는가
- [ ] `notFound`(찾았지만 없던 항목) 목록이 나왔는가 — 빈 배열이면 오히려 의심한다
- [ ] JSON 전문을 채팅에 뿌리지 않고 파일로 저장했는가

## 6. 최신성 주의

`.fig` / `.deck`은 Figma 비공개 포맷이며 공식 문서화된 스펙이 없다. Figma가 형식을
바꾸면 위 필드명 일부가 맞지 않을 수 있다. 그때는 **1단계 스키마 덤프 결과를 기준으로
삼는다.** 억지로 파서를 고치지 않는다.

장기적으로 안정적인 경로가 필요하면 Figma REST API(파일 링크 + 액세스 토큰)가 공식
경로다. 다만 변수(Variables) 관련 엔드포인트는 플랜 제한이 있을 수 있어, 쓰기 전에
Figma 공식 문서에서 현재 조건을 확인해야 한다(이 문서에서는 확인하지 않았다).

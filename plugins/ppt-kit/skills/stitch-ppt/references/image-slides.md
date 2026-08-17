# 이미지 삽입형 슬라이드 — 사용자 첨부 이미지 넣기

`photo-highlight` · `image-full` · `image-compare` · `logo-grid` 네 원형은
**실제 이미지 소재가 필요하다.** 나머지 다섯 원형은 소재 없이 만들어진다.

## 전제: 이미지가 있을 때만 이 네 원형을 쓴다

**제공받은 콘텐츠에 이미지가 포함돼 있을 때만 이미지형 레이아웃을 쓴다.** 사용자가
사진·로고를 첨부했거나 가진 이미지를 명시한 경우가 그것이다. 이미지가 없으면 구성안
단계에서 텍스트형 5종만으로 짜고 이 문서는 아예 쓰지 않는다.

아래 "이미지 요청" 절차는 **이미 이미지가 있다고 확인된 뒤** 어떤 파일을 어느 슬라이드에
어떤 이름으로 넣을지 정리하는 용도다. 없는 이미지를 만들어 오라고 요구하는 절차가 아니다.

## 원칙: Stitch에게 사진을 그리게 하지 않는다

Stitch가 만들어 낸 사진·로고는 실제 대상과 무관한 합성 이미지다. 발표 자료에
그대로 쓰면 사실과 다른 장면이나 존재하지 않는 로고를 보여주게 된다.
그래서 이 스킬은 다음 순서로 처리한다.

1. **Stitch에는 빈 회색 사각형(플레이스홀더)만 그리게 한다.**
2. **사용자에게 실제 이미지를 첨부받는다.**
3. **3단계 pptx 조립에서 그 자리에 실제 이미지를 얹는다.**

플레이스홀더 영역 위에는 글자를 두지 않는다. Stitch가 그린 글자 위에 사진을
얹으면 글자가 가려지기 때문이다. 아래 PLACEHOLDER BLOCK이 이것을 강제한다.

## 1) 이미지 요청 — 언제, 어떻게

**1단계 구성안을 확정한 직후, 2단계 프롬프트를 만들기 전에** 요청한다.
구성안 표에서 이미지형 원형이 쓰인 슬라이드를 골라 아래 형식으로 묻는다.
필요한 장수와 파일명을 함께 알려 준다.

> 이미지가 필요한 슬라이드가 N장 있습니다. 아래 이름으로 파일을 첨부해 주세요.
>
> | 슬라이드 | 원형 | 필요한 이미지 | 파일 이름 |
> |---|---|---|---|
> | 4 | photo-highlight | 강의실 수업 장면 사진 1장 | `img-04.png` |
> | 6 | image-full | 행사 전경 사진 1장(가로) | `img-06.png` |
> | 7 | image-compare | 개선 전 / 개선 후 화면 2장 | `img-07-1.png`, `img-07-2.png` |
> | 9 | logo-grid | 협력사 로고 5장 | `logo-09-1.png` … `logo-09-5.png` |
>
> - 가로 1600px 이상을 권장합니다(작으면 pptx에서 흐리게 보입니다).
> - 사진은 jpg/png, 로고는 배경이 투명한 png가 가장 깔끔합니다.
> - 잘려도 괜찮은 여백이 있는 사진이 좋습니다. 인물 얼굴이 화면 가장자리에
>   있으면 잘릴 수 있습니다.
> - 저작권이 있는 사진·로고는 사용 권한이 있는 것만 보내 주세요.
>   인물 사진은 당사자 동의를 확인해 주세요.

파일명 규칙은 다음과 같다. 이 규칙을 지키면 3단계 배치표를 그대로 쓸 수 있다.

| 용도 | 이름 |
|---|---|
| 슬라이드당 이미지 1장 | `img-{슬라이드번호 2자리}.png` |
| 슬라이드당 여러 장 | `img-{번호}-{순번}.png` |
| 로고 | `logo-{번호}-{순번}.png` |

## 2) 이미지가 없을 때

사용자가 이미지를 줄 수 없다고 하면, 아래 중 하나를 **제안하고 선택을 받는다.**
임의로 정하지 않는다.

- **텍스트형으로 교체(권장)** — 해당 슬라이드를 `card-grid`나 `split-panel`로
  바꾼다. 구성안의 내용은 대부분 그대로 옮겨 쓸 수 있다.
- **플레이스홀더를 남긴 채 완성** — 회색 사각형이 있는 상태로 pptx를 만들고,
  나중에 파워포인트에서 사진을 끼워 넣게 한다. 발표 전 교체가 필요하다고 알린다.
- **Stitch 생성 이미지를 임시로 사용** — 분위기 이미지(추상적 배경 등)에만 쓴다.
  실제 인물·장소·제품·로고에는 쓰지 않는다. 임시본임을 문서에 명시한다.

## 3) 프롬프트에 붙이는 PLACEHOLDER BLOCK

이미지형 슬라이드의 프롬프트는 다음처럼 조립한다. 이 블록이 **맨 뒤**에 와야
앞의 이미지 묘사를 덮어쓴다.

```
[BASE BLOCK] + [STYLE BLOCK] + [원형 블록] + [PLACEHOLDER BLOCK]
```

```
IMPORTANT - image placeholder mode: render every photo, image or logo area as a
plain flat light-gray rectangle (#E0E0E0) with no rounded corners, no circular or
custom crop shape, no drop shadow, no border and no picture content inside,
overriding any image shape or crop described earlier. Do not draw any photograph,
illustration, icon or logo inside these rectangles. Do not place any text, label,
caption, number or watermark inside them or on top of them: every heading,
caption and body text must sit completely outside the placeholder rectangles and
must never overlap them. Keep the placeholder rectangles at exactly the positions
and sizes described above.
```

`{사진묘사}` 슬롯은 지운 채로 넣지 말고 그대로 둔다. Stitch가 자리 크기와
방향(가로/세로)을 정하는 데 쓰인다. 화면에 글자로 찍히지는 않는다.

Stitch 결과에 회색 사각형 대신 그림이 그려져 있으면, 해당 화면에만
"Replace the image area with a plain flat light-gray rectangle, no picture
inside." 라고 짧게 수정 지시를 보낸다.

## 4) 3단계 — 실제 이미지 얹기

`scripts/assemble_pptx.py`의 `--overlay` 옵션에 배치표(JSON)를 넘긴다.
배치표는 첨부 이미지와 같은 폴더에 두면 파일명만 적어도 된다(상대 경로 기준이
배치표 파일이 있는 폴더다).

```bash
python scripts/assemble_pptx.py <슬라이드이미지폴더> -o 발표자료.pptx \
       --overlay <첨부폴더>/overlay.json
```

### overlay.json 규격

배열이며, 항목 하나가 "어느 슬라이드의 어느 영역에 어떤 이미지를 얹을지"를 정한다.

```json
[
  { "slide": 4, "image": "img-04.png", "box": "right-half" },
  { "slide": 6, "image": "img-06.png", "box": "top-72" },
  { "slide": 7, "image": "img-07-1.png", "box": "left-panel" },
  { "slide": 7, "image": "img-07-2.png", "box": "right-panel" },
  { "slide": 9,
    "images": ["logo-09-1.png", "logo-09-2.png", "logo-09-3.png"],
    "box": "center", "cols": 3, "fit": "contain" }
]
```

| 키 | 필수 | 설명 |
|---|---|---|
| `slide` | ✅ | 슬라이드 번호(1부터). 범위를 벗어나면 오류로 멈춘다 |
| `image` | ✅* | 이미지 파일 하나 (`images`와 택일) |
| `images` | ✅* | 이미지 여러 개. `box` 영역을 그리드로 나눠 배치한다 |
| `box` | | 배치 영역. 프리셋 이름 또는 `[x, y, w, h]` 비율(0~1). 기본 `full` |
| `cols` | | `images`일 때 열 수. 기본 3 |
| `fit` | | `cover`(기본, 영역을 꽉 채우고 넘치면 자름) / `contain`(비율 유지, 안 잘림) |

- 사진은 `cover`, **로고는 `contain`** 을 쓴다. 로고를 `cover`로 두면 가장자리가 잘린다.
- 한 슬라이드에 여러 항목을 써도 된다(`slide` 값이 같은 항목을 여러 줄 적는다).

### box 프리셋

| 이름 | 영역 (x, y, w, h) | 주 용도 |
|---|---|---|
| `full` | 0, 0, 1, 1 | 전면 |
| `left-half` / `right-half` | 0/0.5, 0, 0.5, 1 | photo-highlight |
| `top-half` / `bottom-half` | 0, 0/0.5, 1, 0.5 | — |
| `top-72` | 0, 0, 1, 0.72 | image-full (하단 28%는 텍스트 밴드) |
| `left-third` / `right-third` | 0/0.66, 0, 0.34, 1 | 좁은 세로 사진 |
| `left-panel` | 0.06, 0.28, 0.42, 0.50 | image-compare 왼쪽 |
| `right-panel` | 0.52, 0.28, 0.42, 0.50 | image-compare 오른쪽 |
| `center` | 0.20, 0.28, 0.60, 0.52 | logo-grid 그리드 영역 |

프리셋이 실제 플레이스홀더와 어긋나면 `[x, y, w, h]`로 직접 적는다.
Stitch 결과 이미지를 열어 회색 사각형의 위치를 화면 비율로 읽으면 된다
(예: 가로 1280px 이미지에서 왼쪽 끝이 640px이면 x = 0.5).

### 원형별 기본값

| 원형 | box | fit | 비고 |
|---|---|---|---|
| photo-highlight | `right-half` | cover | 사진은 오른쪽 절반 |
| image-full | `top-72` | cover | 하단 텍스트 밴드를 덮지 않는다 |
| image-compare | `left-panel` / `right-panel` | cover | 항목 2줄 |
| logo-grid | `center` + `cols` | **contain** | 로고 장수에 맞춰 `cols` 조정 |

## 5) 마무리 확인

pptx를 만든 뒤 다음을 확인하고, 어긋나면 `box` 값을 조정해 다시 만든다.

- 회색 플레이스홀더가 첨부 이미지로 완전히 덮였는가(회색 테두리가 비치지 않는가)
- 글자가 이미지에 가려지지 않았는가
- 로고가 잘리거나 찌그러지지 않았는가(`fit: contain` 확인)
- 인물 얼굴이 잘리지 않았는가 — 잘렸다면 `box`를 넓히거나 이미지를 미리 크롭해 받는다

#!/usr/bin/env node
/**
 * Figma 로컬 사본(.fig / .deck)을 디코드해 노드 트리 JSON으로 뽑는다.
 *
 *   node fig_decode.mjs <파일.fig|파일.deck> [-o message.json]
 *
 * 구조(2026-07 확인): .fig/.deck 은 ZIP 컨테이너다.
 *   canvas.fig   'fig-kiwi' 매직 + version + [size][chunk] * 2
 *                chunk0 = kiwi 스키마(비압축 또는 deflate)
 *                chunk1 = 노드 데이터(zstd 또는 deflate)
 *   meta.json    파일 이름·썸네일 크기 등
 *   images/*     원본 이미지 (해시 파일명)
 *
 * ※ .fig 는 Figma 비공개 포맷이며 공개 스펙이 없다. Figma가 형식을 바꾸면
 *   이 스크립트는 깨진다. 그때는 압축 방식(zstd/deflate)과 청크 구성을 다시 확인한다.
 */
import fs from 'fs';
import path from 'path';
import AdmZip from 'adm-zip';
import { FigmaArchiveParser } from 'fig-kiwi/dist/index.esm.js';
import { decodeBinarySchema, compileSchema } from 'kiwi-schema';
import { decompress as zstdDecompress } from 'fzstd';
import { inflateRaw } from 'pako';

const args = process.argv.slice(2);
const flagVals = new Set();
for (const f of ['-o', '--schema']) {
  const i = args.indexOf(f);
  if (i >= 0 && args[i + 1]) flagVals.add(args[i + 1]);
}
const src = args.find((a) => !a.startsWith('-') && !flagVals.has(a));
const oi = args.indexOf('-o');
const out = oi >= 0 ? args[oi + 1] : 'message.json';
const si = args.indexOf('--schema');
const schemaOut = si >= 0 ? (args[si + 1] ?? 'schema.json') : null;

if (!src) {
  console.error('사용법: node fig_decode.mjs <파일.fig|파일.deck> [-o message.json] [--schema schema.json]');
  console.error('  --schema  이 파일에 실제로 존재하는 필드 목록을 덤프한다(전량 추출 1단계).');
  process.exit(1);
}

/** zstd → deflateRaw → 원본 순으로 시도한다. 청크마다 압축이 다를 수 있다. */
function unpack(chunk, label) {
  for (const [name, fn] of [['zstd', zstdDecompress], ['deflateRaw', inflateRaw]]) {
    try {
      const outBuf = fn(chunk);
      if (outBuf?.length) return { data: outBuf, codec: name };
    } catch { /* 다음 방식 시도 */ }
  }
  return { data: chunk, codec: 'raw' };
}

const zip = new AdmZip(src);
const entries = zip.getEntries();
const canvasEntry = entries.find((e) => e.entryName === 'canvas.fig');
if (!canvasEntry) {
  console.error(`${src} 안에 canvas.fig 가 없습니다. Figma 로컬 사본이 맞는지 확인하세요.`);
  console.error('들어 있는 항목:', entries.slice(0, 10).map((e) => e.entryName).join(', '));
  process.exit(1);
}

const meta = (() => {
  const e = entries.find((x) => x.entryName === 'meta.json');
  try { return e ? JSON.parse(zip.readAsText(e)) : {}; } catch { return {}; }
})();

const canvas = new Uint8Array(canvasEntry.getData());
const { header, files } = FigmaArchiveParser.parseArchive(canvas);
if (files.length < 2) {
  console.error(`청크가 ${files.length}개뿐입니다(2개 필요). 포맷이 바뀌었을 수 있습니다.`);
  process.exit(1);
}

const s = unpack(files[0], 'schema');
const d = unpack(files[1], 'data');
const schema = decodeBinarySchema(s.data);
const compiled = compileSchema(schema);
const message = compiled.decodeMessage(d.data);

// 이 파일에 실제로 존재하는 필드 목록. 외운 필드명이 아니라 이 목록 안에서만 값을 뽑는다.
// 패키지 타입 정의(fig-kiwi)보다 필드가 더 많을 수 있으므로 파일 쪽 스키마가 기준이다.
if (schemaOut) {
  const defs = (schema.definitions || []).map((def) => ({
    name: def.name,
    kind: def.kind,                                   // STRUCT / MESSAGE / ENUM
    fields: (def.fields || []).map((f) => ({
      name: f.name,
      type: f.type ?? null,                           // ENUM 값은 type이 없다
      isArray: !!f.isArray,
      isDeprecated: !!f.isDeprecated,
    })),
  }));
  const byKind = {};
  for (const def of defs) byKind[def.kind] = (byKind[def.kind] || 0) + 1;
  // ENUM의 "필드"는 열거 멤버지 필드가 아니다. 섞으면 필드 목록이 오염되므로 나눈다.
  const allFields = [...new Set(defs.filter((x) => x.kind !== 'ENUM')
    .flatMap((x) => x.fields.map((f) => f.name)))].sort();
  const enumValues = Object.fromEntries(defs.filter((x) => x.kind === 'ENUM')
    .map((x) => [x.name, x.fields.map((f) => f.name)]));
  fs.writeFileSync(schemaOut, JSON.stringify({
    package: schema.package ?? null,
    version: header.version,
    stats: {
      definitions: defs.length,
      byKind,
      uniqueFieldNames: allFields.length,
      enums: Object.keys(enumValues).length,
    },
    allFieldNames: allFields,   // STRUCT/MESSAGE의 필드명만. 추출은 이 목록 안에서만 한다.
    enumValues,                 // 타입별 허용값. "그럴듯한 값"을 지어내지 않기 위한 근거다.
    definitions: defs,
  }, null, 2));
}

const images = entries
  .filter((e) => e.entryName.startsWith('images/') && !e.isDirectory)
  .map((e) => ({ name: path.basename(e.entryName), bytes: e.header.size }));

fs.writeFileSync(out, JSON.stringify({ meta, header, images, message }));

const counts = {};
for (const n of message.nodeChanges || []) counts[n.type] = (counts[n.type] || 0) + 1;
console.log(`파일        : ${src}`);
console.log(`이름        : ${meta.file_name ?? '(없음)'}`);
console.log(`포맷        : ${header.prelude} v${header.version} / schema=${s.codec}, data=${d.codec}`);
console.log(`노드        : ${message.nodeChanges?.length ?? 0}개`);
console.log(`노드 타입   : ${Object.entries(counts).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k}=${v}`).join(' ')}`);
console.log(`이미지      : ${images.length}개`);
console.log(`저장        : ${out}`);
if (schemaOut) {
  const defs = schema.definitions || [];
  const fieldCount = new Set(defs.filter((x) => x.kind !== 'ENUM')
    .flatMap((x) => (x.fields || []).map((f) => f.name))).size;
  const enumCount = defs.filter((x) => x.kind === 'ENUM').length;
  console.log(`스키마      : 정의 ${defs.length}개 / 필드명 ${fieldCount}개 / ENUM ${enumCount}개 → ${schemaOut}`);
}

#!/usr/bin/env python3
"""Static quality contract for the six Hidemari Coffee flagship concepts."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "design-manifest.json"
FILES = [f"0{i}-{slug}.html" for i, slug in enumerate(("hikari-editorial","daily-utility","shiro-sumi","local-journal","roast-lab","afterglow"), 1)]
REQUIRED = ("ひだまり珈琲店", "みなと中央駅", "メニュー", "営業時間", "自家焙煎", "架空店舗の制作サンプル", "Wi-Fi", "電源8席")
MENU = ("ハウスブレンド", "シングルオリジン", "カフェラテ", "コールドブリュー", "自家製レモネード", "季節のドリンク", "厚切りトースト", "あんバタートースト", "季節のスープ", "たまごサンド", "固めプリン", "ベイクドチーズケーキ", "季節のタルト", "コーヒー豆200g", "ドリップバッグ", "ギフトボックス")

def load_manifest(): return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
def manifest_files(data): return [d["file"] for d in data["designs"]]

def check_page(path: Path):
    text = path.read_text(encoding="utf-8") + (ROOT / "flagship.css").read_text(encoding="utf-8"); errors=[]
    if not re.search(r"<meta[^>]+name=[\"']robots[\"'][^>]+noindex", text, re.I): errors.append("noindex missing")
    for token in REQUIRED:
        if token not in text: errors.append(f"missing content token: {token}")
    if sum(text.count(x) for x in MENU) < 16: errors.append("menu items missing")
    if len(re.findall(r"<section\b", text, re.I)) < 8: errors.append("at least 8 sections required")
    if not re.search(r"<dialog\b", text, re.I) or "実際の注文はできません" not in text: errors.append("takeout dialog missing")
    if not re.search(r"固定|mobile-bar|mobileBar", text, re.I): errors.append("mobile action bar missing")
    if re.search(r'href=["\'](?:#|\s*)["\']', text, re.I): errors.append("empty href")
    for src in re.findall(r'<img\b[^>]+src=["\']([^"\']+)', text, re.I):
        if src.startswith("http"): errors.append("external image")
    for tag in re.findall(r'<img\b[^>]*>', text, re.I):
        m=re.search(r'src=["\']([^"\']+)',tag,re.I)
        if not m or not (ROOT/m.group(1)).is_file(): errors.append("image file missing")
        if not all(re.search(rf'{attr}=["\'][^"\']+',tag,re.I) for attr in ("alt","width","height")): errors.append("image attributes missing")
    if re.search(r'href=["\']https?://|src=["\']https?://', text, re.I): errors.append("external URL not allowed")
    if re.search(r"word-break\s*:\s*keep-all", text, re.I): errors.append("keep-all must not apply globally")
    for rule in (r"word-break\s*:\s*normal", r"word-break\s*:\s*auto-phrase", r"line-break\s*:\s*strict", r"overflow-wrap\s*:\s*break-word", r"text-wrap\s*:\s*pretty", r"prefers-reduced-motion"):
        if not re.search(rule, text, re.I): errors.append(f"responsive/accessibility rule missing: {rule}")
    if not re.search(r"@media[^{}]+max-width", text, re.I): errors.append("mobile media rule missing")
    return errors

def run(selected=None):
    data=load_manifest(); files=manifest_files(data); errors=[]
    if data.get("version") != 2: errors.append("manifest version must be 2")
    if files != FILES: errors.append("manifest must contain exactly six flagship files")
    if len(data.get("designs", [])) != 6: errors.append("design count")
    if set(d.get("background") for d in data["designs"]) != {"white","cool-gray","dark"}: errors.append("background taxonomy")
    if sum(d.get("background")=="white" for d in data["designs"]) != 4: errors.append("four white designs required")
    selected=files if selected is None else selected
    for f in selected:
        if f not in files: errors.append(f"unknown filename: {f}"); continue
        p=ROOT/f
        if not p.is_file(): errors.append(f"{f}: file missing"); continue
        errors.extend(f"{f}: {e}" for e in check_page(p))
    if errors:
        for e in errors: print("FAIL:",e)
        return 1
    print(f"PASS: {len(selected)} flagship page(s) satisfy the contract"); return 0
if __name__ == "__main__": raise SystemExit(run(sys.argv[1:] or None))

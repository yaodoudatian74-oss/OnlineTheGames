# REALISTIC ISLAND SURVIVAL（無人島サバイバル）

three.js（r128）で作ったブラウザ用の3Dオープンワールド無人島サバイバル。PWA（ホーム画面に追加）とAndroid APKで遊べます。

- `index.html` … 遊べる本体（PWA。`manifest.webmanifest`・`sw.js`・アイコン同梱）
- `island-survival.apk` … Android用（WebViewラッパー、オフラインで起動）
- `src/` … ゲームのソース（`game.js`・`shell.html`・`build.py`）
- `android/` … APKのソースとビルドスクリプト（Android SDK build-tools 34 で直接ビルド）
- `tests/` … Playwright の自動テスト（操作・クラフト・建築・セーブ/ロード・潜水・洞窟・脱出・スマホ操作）

## 操作
PC：WASD移動・マウス視点・Shift走る・C しゃがむ/潜る・Space ジャンプ/浮上・左クリック 使う・E 拾う/調べる・G 石を投げる・Tab 持ち物・B 建築・M 地図・V 視点・1〜8 道具・R 回転・X 撤去
スマホ：左スティック移動・右側ドラッグで視点・右下ボタンで操作・上部バーでバッグ/建築/地図

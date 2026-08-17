# コーヒーショップ／高アクセス飲食店サイト調査（2026-08-15）

## 調査の見方

「デザインが受賞しているか」だけではなく、来店前の利用者がスマホで短時間に知りたいことを優先して比較した。2026年7月のSemrush Restaurants分類では、McDonald'sは月間3,439万訪問の87.28%がモバイル、Chipotleは1,488万訪問の82.58%がモバイル、日本マクドナルドは1,289万訪問の93.98%がモバイルと推計されている。よって追加10案では、PCの見栄えより先に「注文・メニュー・店舗・営業時間へすぐ到達できること」を共通条件にする。

## 参照したサイトと得た示唆

1. Starbucks Japan — https://www.starbucks.co.jp/
   - メニュー、店舗検索、モバイルオーダーを主要導線として常時見せる。
   - 季節商品は、一商品を大きく見せて短いコピーと行動ボタンへつなぐ。
2. Blue Bottle Coffee Japan — https://store.bluebottlecoffee.jp/pages/cafes
   - 店舗ページで住所、営業時間、席数、Wi-Fi、メニュー、アクセスを一画面で確認できる。
3. % Arabica — https://arabica.com/locations/
   - 強い記号と大きな余白を保ちつつ、世界の店舗一覧という実用情報を中心に据える。
4. Onyx Coffee Lab — https://onyxcoffeelab.com/
   - 商品販売だけでなく、店舗、コミュニティ、認証、透明性をブランド価値として見せる。
5. Stumptown Coffee Roasters — https://www.stumptowncoffee.com/
   - Shop / Subscribe / Locations / Brew Guidesを短い主ナビにまとめ、Coffee Quizで選択を助ける。
6. Kurasu — https://kurasu.kyoto/
   - 豆・器具・定期便・読み物を一つのブランド体験に統合し、味の発見を継続購入につなげる。
7. McDonald's — https://www.mcdonalds.com/us/en-us.html
   - Order Nowを最短導線にし、季節商品や特典ごとに同じ行動を繰り返し提示する。
8. sweetgreen — https://www.sweetgreen.com/
   - 商品名だけでなく材料・アレルゲンを一覧で見せ、各商品から直接注文できる。
9. Chipotle — https://www.chipotle.com/
   - 季節商品の短い訴求とORDER NOWを直結し、通常注文・ケータリング・グループ注文を利用場面で分ける。
10. HubSpot coffee-shop roundup — https://blog.hubspot.com/website/coffee-shops-websites
    - 優れたカフェサイトは、雰囲気だけでなく、住所・メニュー・注文への不確実さを数秒で取り除くという評価軸を採用している。

## 追加する10デザイン

| No. | ファイル | 役割 | 主な参照点 |
|---:|---|---|---|
| 31 | `31-order-first.html` | 注文・メニュー・アクセスをファーストビューに集約 | Starbucks / McDonald's |
| 32 | `32-seasonal-campaign.html` | 季節限定ドリンク一品を主役にした販促ページ | Starbucks / Chipotle |
| 33 | `33-menu-catalog.html` | 価格・説明を迷わず比較できる実用メニュー | sweetgreen |
| 34 | `34-cafe-location.html` | 営業時間・駅・席・設備・地図を中心にした店舗ページ | Blue Bottle |
| 35 | `35-roaster-shop.html` | 味の特徴から豆を選び、購入へ進むロースター型 | Stumptown / Kurasu |
| 36 | `36-coffee-finder.html` | 質問に答えておすすめの一杯を選ぶ診断型 | Stumptown Coffee Quiz |
| 37 | `37-origin-transparency.html` | 産地・焙煎・取引の透明性を見せる信頼訴求型 | Onyx |
| 38 | `38-neighborhood-community.html` | イベントと近所の居場所を伝える地域密着型 | Onyx / HubSpot調査例 |
| 39 | `39-global-locations.html` | 強いロゴと余白、店舗一覧で魅せるグローバル型 | % Arabica |
| 40 | `40-brew-journal.html` | 抽出ガイドと読み物から店・豆へ誘導する編集型 | Kurasu / Stumptown |

## 10案の共通合格条件

- 1ファイル完結、外部画像なし、装飾目的の絵文字なし。
- ひだまり珈琲店の共通メニュー、営業時間、最寄り駅を保持する。
- 全ページに「メニュー」「店舗情報」「営業時間」「次の行動」が視覚的に見つかる。
- 320pxと375pxで横スクロールを出さず、タップ対象はおおむね44px以上にする。
- 既存30案の表現実験とは異なり、実店舗の利用目的が一目で伝わる。

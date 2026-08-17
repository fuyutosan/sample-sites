import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import check_sample_sites  # noqa: E402

EXPECTED = {
    "01-hikari-editorial.html": {"h1": "朝の光を、一杯に。", "hero": "assets/images/interior-wide.webp", "body_class": "concept-hikari-editorial", "order": ["top", "today", "menu", "morning", "space", "story", "seasonal", "access", "faq", "final"]},
    "02-daily-utility.html": {"h1": "迷わず、今日の一杯へ。", "hero": "assets/images/house-coffee.webp", "body_class": "concept-daily-status", "order": ["top", "menu", "today", "morning", "access", "space", "seasonal", "story", "faq", "final"]},
    "03-shiro-sumi.html": {"h1": "白に、香りを置く。", "hero": "assets/images/handdrip-close.webp", "body_class": "concept-shiro-craft", "order": ["top", "story", "menu", "space", "morning", "seasonal", "access", "today", "faq", "final"]},
    "04-local-journal.html": {"h1": "街の朝を、ここから。", "hero": "assets/images/community-scene.webp", "body_class": "concept-local-journal", "order": ["top", "journal", "today", "community", "menu", "seasonal", "space", "story", "access", "faq", "morning", "final"]},
    "05-roast-lab.html": {"h1": "味を、選べる言葉に。", "hero": "assets/images/beans-package.webp", "body_class": "concept-roast-lab", "order": ["top", "bean-finder", "story", "menu", "space", "access", "today", "morning", "seasonal", "faq", "final"]},
    "06-afterglow.html": {"h1": "午後の余白に、深い一杯。", "hero": "assets/images/cheesecake-tart.webp", "body_class": "concept-afterglow", "order": ["top", "seasonal", "menu", "space", "today", "story", "access", "morning", "faq", "final"]},
}


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


class FlagshipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shop = json.loads(read("content/shop.json"))
        cls.manifest = check_sample_sites.load_manifest()

    def test_manifest_is_exactly_six(self):
        self.assertEqual(self.manifest["version"], 2)
        self.assertEqual(check_sample_sites.manifest_files(self.manifest), list(EXPECTED))
        expected_heroes = [v["hero"].split("/")[-1] for v in EXPECTED.values()]
        self.assertEqual([d["heroAsset"] for d in self.manifest["designs"]], expected_heroes)
        self.assertEqual(sum(d["background"] == "white" for d in self.manifest["designs"]), 4)

    def test_shop_has_sixteen_complete_menu_items(self):
        self.assertEqual(len(self.shop["menu"]), 16)
        self.assertTrue(all(item.get("name") and item.get("price") for item in self.shop["menu"]))

    def test_each_page_has_unique_strategy_and_section_order(self):
        orders = []
        for filename, expected in EXPECTED.items():
            html = read(filename)
            body = re.search(r"<body\b[^>]*class=[\"']([^\"']+)", html, re.I)
            self.assertIsNotNone(body, filename)
            self.assertIn(expected["body_class"], body.group(1), filename)
            h1 = re.search(r"<h1>(.*?)</h1>", html, re.I | re.S)
            self.assertIsNotNone(h1, filename)
            h1_text = re.sub(r"<[^>]+>|\s+", "", h1.group(1))
            self.assertEqual(h1_text, expected["h1"].replace(" ", ""), filename)
            hero = re.search(r'<section[^>]*class=["\'][^"\']*hero[^"\']*["\'][^>]*>.*?<img[^>]+src=["\']([^"\']+)', html, re.I | re.S)
            self.assertIsNotNone(hero, filename)
            self.assertEqual(hero.group(1), expected["hero"], filename)
            order = re.findall(r"<section\b[^>]*\bid=[\"']([^\"']+)", html, re.I)
            self.assertEqual(order, expected["order"], filename)
            orders.append(tuple(order))
        self.assertEqual(len(set(orders)), 6)

    def test_every_page_contains_canonical_shop_facts_and_menu(self):
        facts = [
            self.shop["station"], *self.shop["hours"].values(),
            "Wi-Fi", "電源8席", "ベビーカー", "キャッシュレス",
            "テイクアウト", "ペット",
        ]
        for filename in EXPECTED:
            html = read(filename)
            visible = re.sub(r"<style\b.*?</style>|<script\b.*?</script>|<[^>]+>", " ", html, flags=re.I | re.S)
            for fact in facts:
                self.assertIn(fact, visible, f"{filename}: {fact}")
            for item in self.shop["menu"]:
                self.assertIn(item["name"], visible, f"{filename}: {item['name']}")
                self.assertIn(item["price"], visible, f"{filename}: {item['price']}")
            self.assertGreater(len(re.sub(r"\s+", "", visible)), 900, filename)

    def test_images_are_local_complete_and_lazy_below_hero(self):
        for filename in EXPECTED:
            tags = re.findall(r"<img\b[^>]*>", read(filename), re.I)
            self.assertGreaterEqual(len(tags), 4, filename)
            for index, tag in enumerate(tags):
                src = re.search(r"src=[\"']([^\"']+)", tag, re.I)
                alt = re.search(r"alt=[\"']([^\"']+)", tag, re.I)
                self.assertIsNotNone(src, filename)
                self.assertFalse(src.group(1).startswith(("http://", "https://")), filename)
                self.assertTrue((ROOT / src.group(1)).is_file(), f"{filename}: {src.group(1)}")
                self.assertIsNotNone(alt, filename)
                self.assertTrue(alt.group(1).strip(), filename)
                self.assertRegex(tag, r'width=["\']\d+["\']', filename)
                self.assertRegex(tag, r'height=["\']\d+["\']', filename)
                if index == 0:
                    self.assertNotRegex(tag, r'loading=["\']lazy', filename)
                    self.assertRegex(tag, r'fetchpriority=["\']high', filename)
                else:
                    self.assertRegex(tag, r'loading=["\']lazy', filename)

    def test_safe_demo_interactions_and_no_external_routes(self):
        for filename in EXPECTED:
            html = read(filename)
            self.assertIn('<nav class="mobile-bar"', html, filename)
            self.assertIn("<dialog", html, filename)
            self.assertIn("実際の注文はできません", html, filename)
            self.assertNotRegex(html, r'(?:href|src)=["\']https?://', filename)
            self.assertNotRegex(html, r'href=["\'](?:#|\s*)["\']', filename)

    def test_checker_accepts_all(self):
        self.assertEqual(check_sample_sites.run(), 0)


if __name__ == "__main__":
    unittest.main()

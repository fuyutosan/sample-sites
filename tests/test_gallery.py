import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "design-manifest.json").read_text(encoding="utf-8"))
FILES = [item["file"] for item in MANIFEST["designs"]]
THUMBS = [f'thumbnails/{item["slug"]}.png' for item in MANIFEST["designs"]]
LEGACY = [
    "01-apothecary-editorial.html", "02-swiss-grid.html", "03-vertical-japan.html",
    "04-luxury-serif.html", "05-mono-editorial.html", "06-architectural-plan.html",
    "07-letterpress-ticket.html", "08-showa-signboard.html", "09-risograph-zine.html",
    "10-matchbox-label.html", "11-art-nouveau.html", "12-coffee-package.html",
    "13-neo-brutalist.html", "14-bauhaus.html", "15-constructivist.html",
    "16-maximalist.html", "17-dopamine-y2k.html", "18-checkerboard.html",
    "19-kinetic-type.html", "20-terminal-board.html", "21-retrofuture-manual.html",
    "22-radial-navigation.html", "23-css-3d-package.html", "24-split-scroll.html",
    "25-paper-collage.html", "26-handdrawn-chalk.html", "27-ink-organic.html",
    "28-horizontal-story.html", "29-sunlight-shadow.html", "30-low-impact-text.html",
    "31-order-first.html", "32-seasonal-campaign.html", "33-menu-catalog.html",
    "34-cafe-location.html", "35-roaster-shop.html", "36-coffee-finder.html",
    "37-origin-transparency.html", "38-neighborhood-community.html",
    "39-global-locations.html", "40-brew-journal.html",
]


class GalleryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_index_has_exactly_six_case_study_links_and_thumbnails(self):
        links = re.findall(r'href=["\']([^"\']+\.html)["\']', self.html, re.I)
        self.assertEqual([link for link in links if link in FILES], FILES)
        refs = re.findall(r'<img\b[^>]*src=["\'](thumbnails/[^"\']+)["\']', self.html, re.I)
        self.assertEqual(refs, THUMBS)
        for ref in THUMBS:
            self.assertTrue((ROOT / ref).is_file(), ref)
            self.assertGreater((ROOT / ref).stat().st_size, 20_000, ref)

    def test_index_sells_strategy_and_mobile_capability(self):
        for text in (
            "同じ一軒を", "6つの営業戦略", "想定客", "課題", "狙う行動",
            "スマホで検証", "クラウドワークスのメッセージからご相談ください",
        ):
            self.assertIn(text, self.html)
        self.assertNotIn("40 DESIGNS", self.html)
        self.assertRegex(self.html, r"background\s*:\s*#fff", re.I)

    def test_all_original_forty_routes_are_safe_redirects(self):
        for filename in LEGACY:
            text = (ROOT / filename).read_text(encoding="utf-8")
            self.assertRegex(text, r'name=["\']robots["\'][^>]*noindex', filename)
            self.assertRegex(text, r'http-equiv=["\']refresh["\'][^>]*index\.html#works', filename)
            self.assertRegex(text, r'href=["\']index\.html#works["\']', filename)
        archive = ROOT / "research" / "legacy-sites-2026-08.zip"
        self.assertTrue(archive.is_file())
        self.assertGreater(archive.stat().st_size, 30_000)


if __name__ == "__main__":
    unittest.main()

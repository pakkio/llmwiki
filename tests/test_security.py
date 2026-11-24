"""Security regressions: login, URL fetching (SSRF) and wiki page titles.

Run with:  python -m unittest discover -s tests
No network and no LLM calls: DNS and HTTP are faked.
"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import httpx

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import urlfetch  # noqa: E402
import wiki  # noqa: E402


def _addr(ip: str):
    family = 10 if ":" in ip else 2
    sockaddr = (ip, 0, 0, 0) if family == 10 else (ip, 0)
    return [(family, 1, 6, "", sockaddr)]


def _fake_dns(table=None):
    """getaddrinfo stand-in: names from `table`, IP literals resolve to themselves."""
    table = table or {}

    def fake(host, port, *args, **kwargs):
        return _addr(table.get(host, host))

    return fake


class WikiTitleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        patcher = mock.patch.object(wiki, "WIKI_DIR", Path(self.tmp.name))
        patcher.start()
        self.addCleanup(patcher.stop)
        self.dir = Path(self.tmp.name)

    def test_traversal_titles_stay_inside_the_wiki_dir(self):
        for title in ("../../evil", "..\\..\\evil2", "a/b/c", "/etc/passwd"):
            wiki.write_page(title, "x")
        written = list(self.dir.iterdir())
        self.assertEqual(len(written), 4)
        self.assertTrue(all(p.parent == self.dir for p in written))
        self.assertFalse((self.dir.parent / "evil.md").exists())

    def test_dot_titles_and_empty_titles_are_refused(self):
        for title in ("..", ".", "", "   ", "x" * 500):
            self.assertIn("Invalid page title", wiki.write_page(title, "x"))
        self.assertEqual(list(self.dir.iterdir()), [])

    def test_reserved_pages_cannot_be_written_or_appended(self):
        (self.dir / "index.md").write_text("original")
        (self.dir / "log.md").write_text("original")
        for title in ("index", "log", "Index", "LOG"):
            self.assertIn("system-managed", wiki.write_page(title, "pwned"))
            self.assertIn("system-managed", wiki.append_page(title, "pwned"))
            self.assertIn("system-managed", wiki.delete_page(title))
        self.assertEqual((self.dir / "index.md").read_text(), "original")
        self.assertEqual((self.dir / "log.md").read_text(), "original")

    def test_system_files_are_still_written_by_the_system(self):
        wiki.rebuild_index()
        wiki.append_log("test", "detail")
        self.assertTrue((self.dir / "index.md").exists())
        self.assertIn("detail", (self.dir / "log.md").read_text())

    def test_normal_pages_still_work(self):
        self.assertIn("written", wiki.write_page("Babilonia (città antica)", "# B"))
        self.assertEqual(wiki.read_page("Babilonia (città antica)"), "# B")
        self.assertIn("Appended", wiki.append_page("Babilonia (città antica)", "più"))
        self.assertIn("deleted", wiki.delete_page("Babilonia (città antica)"))

    def test_reading_reserved_pages_is_still_allowed(self):
        (self.dir / "index.md").write_text("# Wiki Index")
        self.assertEqual(wiki.read_page("index"), "# Wiki Index")


class UrlFetchTests(unittest.TestCase):
    def fetch(self, url, handler=None, dns=None):
        handler = handler or (lambda request: httpx.Response(200, text="ciao"))
        transport = httpx.MockTransport(handler)
        with mock.patch("urlfetch.socket.getaddrinfo", _fake_dns(dns)):
            return urlfetch.fetch_public_text(url, transport=transport)

    def test_non_public_addresses_are_refused(self):
        for ip in ("127.0.0.1", "10.1.2.3", "192.168.0.5", "172.16.0.1", "169.254.169.254",
                   "100.64.1.1", "0.0.0.0", "::1", "::ffff:127.0.0.1", "fe80::1", "fc00::1"):
            host = f"[{ip}]" if ":" in ip else ip
            with self.subTest(ip=ip), self.assertRaises(urlfetch.UnsafeURL):
                self.fetch(f"http://{host}/secret")

    def test_hostname_resolving_to_a_private_address_is_refused(self):
        with self.assertRaises(urlfetch.UnsafeURL):
            self.fetch("http://internal.example/", dns={"internal.example": "10.0.0.8"})

    def test_all_resolved_addresses_must_be_public(self):
        infos = _addr("8.8.8.8") + _addr("127.0.0.1")
        with mock.patch("urlfetch.socket.getaddrinfo", return_value=infos):
            with self.assertRaises(urlfetch.UnsafeURL):
                urlfetch.fetch_public_text("http://mixed.example/", transport=httpx.MockTransport(
                    lambda r: httpx.Response(200, text="x")))

    def test_only_http_and_https(self):
        for url in ("file:///etc/passwd", "ftp://example.com/x", "gopher://example.com/",
                    "javascript:alert(1)", "http:///nohost", "example.com/path"):
            with self.subTest(url=url), self.assertRaises(urlfetch.UnsafeURL):
                self.fetch(url, dns={"example.com": "8.8.8.8"})

    def test_credentials_in_url_are_refused(self):
        with self.assertRaises(urlfetch.UnsafeURL):
            self.fetch("http://user:pw@public.example/", dns={"public.example": "8.8.8.8"})

    def test_public_url_is_fetched(self):
        text = self.fetch("https://public.example/page", dns={"public.example": "8.8.8.8"})
        self.assertEqual(text, "ciao")

    def test_redirect_to_a_private_address_is_refused(self):
        def handler(request):
            if request.url.host == "public.example":
                return httpx.Response(302, headers={"location": "http://169.254.169.254/latest/meta-data/"})
            raise AssertionError("the private address must never be requested")

        with self.assertRaises(urlfetch.UnsafeURL):
            self.fetch("http://public.example/", handler, dns={"public.example": "8.8.8.8"})

    def test_relative_redirect_to_a_public_page_is_followed(self):
        def handler(request):
            if request.url.path == "/start":
                return httpx.Response(301, headers={"location": "/final"})
            return httpx.Response(200, text="arrivato")

        text = self.fetch("http://public.example/start", handler, dns={"public.example": "8.8.8.8"})
        self.assertEqual(text, "arrivato")

    def test_redirect_loop_is_cut(self):
        handler = lambda request: httpx.Response(302, headers={"location": "http://public.example/again"})
        with self.assertRaises(urlfetch.UnsafeURL):
            self.fetch("http://public.example/", handler, dns={"public.example": "8.8.8.8"})

    def test_oversized_body_is_refused(self):
        handler = lambda request: httpx.Response(200, content=b"x" * 100)
        with mock.patch.object(urlfetch, "MAX_BYTES", 10), self.assertRaises(urlfetch.UnsafeURL):
            self.fetch("http://public.example/", handler, dns={"public.example": "8.8.8.8"})

    def test_http_errors_still_surface(self):
        handler = lambda request: httpx.Response(404)
        with self.assertRaises(httpx.HTTPStatusError):
            self.fetch("http://public.example/", handler, dns={"public.example": "8.8.8.8"})


class StartupTests(unittest.TestCase):
    def test_refuses_to_start_without_a_password(self):
        # An empty value counts as set for python-dotenv, so a local .env cannot mask this test.
        env = {**os.environ, "DEEPSEEK_API_KEY": "test", "AUTH_PASSWORD": ""}
        result = subprocess.run(
            [sys.executable, "-c", "import api"],
            cwd=ROOT, env=env, capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AUTH_PASSWORD", result.stderr)


class LoginAndIngestTests(unittest.TestCase):
    PASSWORD = "correct-horse-battery"

    @classmethod
    def setUpClass(cls):
        cls._env = mock.patch.dict(os.environ, {
            "DEEPSEEK_API_KEY": "test", "AUTH_USERNAME": "tester", "AUTH_PASSWORD": cls.PASSWORD,
        })
        cls._env.start()
        from fastapi.testclient import TestClient
        import api
        cls.api = api
        cls.client = TestClient(api.app)

    @classmethod
    def tearDownClass(cls):
        cls._env.stop()

    def login(self, username="tester", password=PASSWORD):
        return self.client.post("/api/login", json={"username": username, "password": password})

    def test_login_rejects_wrong_empty_and_misspelled_credentials(self):
        self.assertEqual(self.login(password="").status_code, 401)
        self.assertEqual(self.login(password="wrong").status_code, 401)
        self.assertEqual(self.login(username="pakkio").status_code, 401)
        self.assertEqual(self.login(password=self.PASSWORD + "x").status_code, 401)

    def test_login_accepts_the_right_credentials_and_the_token_works(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        token = response.json()["token"]
        self.assertEqual(self.client.get("/api/pages").status_code, 401)
        ok = self.client.get("/api/pages", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(ok.status_code, 200)

    def test_ingest_of_an_internal_url_never_reaches_the_agent(self):
        token = self.login().json()["token"]
        with mock.patch.object(self.api, "ingest") as ingest, \
                mock.patch("urlfetch.socket.getaddrinfo", _fake_dns()):
            response = self.client.post(
                "/api/ingest", json={"url": "http://169.254.169.254/latest/meta-data/"},
                headers={"Authorization": f"Bearer {token}"},
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn('"type": "error"', response.text)
        self.assertIn("non-public address", response.text)
        ingest.assert_not_called()


if __name__ == "__main__":
    unittest.main()

# Run: python3 -I -m unittest discover -s tests
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from check_trending import problems  # noqa: E402


def repo(i, gain):
    return {"name": f"a/b{i}", "what": "x", "stars_week": f"+{gain}", "stars_week_n": gain,
            "stars": "5k", "url": f"https://github.com/a/b{i}", "early": False}


GOOD = {"updated": "2026-11-30", "week": "Week of November 30, 2026", "repos": [repo(1, 900), repo(2, 400)]}


class CheckTrending(unittest.TestCase):
    def test_good_and_empty_files_pass(self):
        self.assertEqual(problems(GOOD), [])
        self.assertEqual(problems(dict(GOOD, repos=[])), [])

    def test_links_must_go_to_the_repo_on_github(self):
        bad = dict(GOOD, repos=[dict(repo(1, 5), url="https://evil.example/a/b1")])
        self.assertTrue(any('"url"' in p for p in problems(bad)))
        bad = dict(GOOD, repos=[dict(repo(1, 5), name="javascript:alert(1)")])
        self.assertTrue(any('"name"' in p for p in problems(bad)))

    def test_ranked_by_weekly_gain_most_first(self):
        self.assertTrue(any("in order" in p for p in problems(dict(GOOD, repos=[repo(1, 1), repo(2, 9)]))))
        self.assertTrue(any("stars_week_n" in p for p in problems(dict(GOOD, repos=[dict(repo(1, 1), stars_week_n="9")]))))

    def test_limits(self):
        self.assertTrue(any("most is 10" in p for p in problems(dict(GOOD, repos=[repo(i, 100 - i) for i in range(11)]))))
        self.assertTrue(any("twice" in p for p in problems(dict(GOOD, repos=[repo(1, 9), repo(1, 8)]))))
        self.assertTrue(any('"what"' in p for p in problems(dict(GOOD, repos=[dict(repo(1, 1), what="w " * 21)]))))
        self.assertTrue(any('"stars"' in p for p in problems(dict(GOOD, repos=[{k: v for k, v in repo(1, 1).items() if k != "stars"}]))))
        self.assertTrue(problems([]))
        self.assertTrue(problems({"repos": []}))


if __name__ == "__main__":
    unittest.main()

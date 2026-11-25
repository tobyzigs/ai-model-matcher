# AI Model Matcher

Compare AI models by price per token, context size, parameters, and test scores, and find the cheapest model that does the job. Netlify serves the `app/` folder, and you can install it on a phone from the browser.

## How it updates

A weekly Claude scheduled task ("AI Model Matcher weekly update") refreshes the data:

1. It downloads prices from the OpenRouter model list and scores from Artificial Analysis into `data/or.json` and `data/aa.json`.
2. `python3 -I scripts/build.py` (run from the repo root) writes `models.json`, which is copied to `app/models.json`.
3. It rechecks subscription tool prices in `app/subs.json` and helper tool prices in `app/tools.json`, and picks up to 10 new tools for `app/notable.json` (New and notable money savers). It also fills `app/trending.json` (Trending on GitHub this week) and checks it with `python3 -I scripts/check_trending.py`; see below.
4. It saves the Artificial Analysis image leaderboard to `data/img.md` and runs `python3 -I scripts/build_images.py` to refresh `app/images.json`.
5. It commits and pushes. Netlify publishes each push.

## Files

- `app/`: the published site (page, data, icons, install files).
- `src/index.html`: the page source, also published as a Claude artifact.
- `scripts/make_app.py src/index.html app/index.html`: builds the installable page from the source.
- `scripts/check_trending.py`: checks `app/trending.json` (at most 10 repos, every field filled, links that go to github.com). The section stays hidden while the list is empty.
- `scripts/build.py`: builds the model data. Since November 2026 the Artificial Analysis feed sends only Intelligence Index v5 (and no per-test results), so the script keeps each model's last published per-test score from `app/models.json` and never carries Smarts forward.

## Trending on GitHub this week

The weekly task's step for `app/trending.json` (its prompt holds the same text):

> Trending on GitHub (app/trending.json): open https://github.com/trending?since=weekly (Firecrawl scrape, formats ["markdown"], maxAge 0). From the repos listed there, take the 10 with the most stars gained this week, on any topic, and skip any that is cracked, pirated, or patched paid software, a license or DRM bypass tool, a keygen, or leaked or decompiled code. Write each with: name (owner/repo), what (max 20 words, plain English), language, license (if shown on the repo), stars_week (as shown, e.g. "+3,214 stars"), stars_week_n (that number as a whole number), stars (total, e.g. "41k"), url ("https://github.com/" + name), early (true when under about 500 total stars or the project calls itself alpha or early stage). Order by stars_week_n, most first. Set "updated" to today and "week" to "Week of <Month D, YYYY>" (the Monday of this week). Run `python3 -I scripts/check_trending.py`; if it reports a problem, fix the file, or keep last week's file and say so in the final message.

Scope: the 10 biggest weekly gains among the repos on GitHub's weekly Trending page (GitHub picks that set of about 25), not every repo on GitHub. The page shows the list in that order, and drops any entry that fails its own checks, so a bad file never stops the rest of the page.

Checks: `python3 -I -m unittest discover -s tests` (the file checker) and `node --test tests/*.test.mjs` (the page code with bad feeds).

# AI Model Matcher

Compare AI models by price per token, context size, parameters, and test scores, and find the cheapest model that does the job. Netlify serves the `app/` folder, and you can install it on a phone from the browser.

## How it updates

A weekly Claude scheduled task ("AI Model Matcher weekly update") refreshes the data:

1. It downloads prices from the OpenRouter model list and scores from Artificial Analysis into `data/or.json` and `data/aa.json`.
2. `python3 -I scripts/build.py` (run from the repo root) writes `models.json`, which is copied to `app/models.json`.
3. It rechecks subscription tool prices in `app/subs.json` and helper tool prices in `app/tools.json`, and picks a new top 5 for `app/notable.json` (New and notable money savers).
4. It commits and pushes. Netlify publishes each push.

## Files

- `app/`: the published site (page, data, icons, install files).
- `src/index.html`: the page source, also published as a Claude artifact.
- `scripts/make_app.py src/index.html app/index.html`: builds the installable page from the source.
- `scripts/build.py`: builds the model data.

// The page's Trending code, run against bad feeds. Run: node --test tests/
// It takes trendRepos and renderTrending out of src/index.html and runs them with a stand-in page.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const html = fs.readFileSync(new URL('../src/index.html', import.meta.url), 'utf8');
const pick = (name, next) => html.slice(html.indexOf('function ' + name + '('), html.indexOf(next));
const escAt = html.indexOf('function esc(');
const src =
	html.slice(escAt, html.indexOf('\n', escAt)) +
	'\n' +
	pick('trendRepos', 'function renderTrending(') +
	pick('renderTrending', 'function renderHelpers(');
const page = (TREND) => {
	const els = { trendpanel: { hidden: true }, trendtitle: { textContent: '' }, trendgrid: { innerHTML: '' } };
	new Function('TREND', '$', src + '\nrenderTrending();')(TREND, (id) => els[id]);
	return els;
};
const repo = (i, n) => ({
	name: `a/b${i}`,
	what: 'Does a thing',
	stars_week: `+${n}`,
	stars_week_n: n,
	stars: '5k',
	url: `https://github.com/a/b${i}`,
});

test('good repos show, ranked by weekly gain, at most 10', () => {
	const repos = Array.from({ length: 12 }, (_, i) => repo(i, i * 10));
	const els = page({ week: 'Week of X', repos });
	assert.equal(els.trendpanel.hidden, false);
	const cards = els.trendgrid.innerHTML.match(/class="help"/g);
	assert.equal(cards.length, 10);
	assert.ok(els.trendgrid.innerHTML.indexOf('1. a/b11') < els.trendgrid.innerHTML.indexOf('2. a/b10'));
});

test('bad entries are dropped and links only ever go to github.com', () => {
	const els = page({
		repos: [
			repo(1, 5),
			{ ...repo(2, 9), url: 'javascript:alert(1)' },
			{ ...repo(3, 9), name: '<img src=x onerror=1>/x', url: 'https://github.com/<img src=x onerror=1>/x' },
			{ ...repo(4, 9), stars_week_n: '9' },
			null,
			'text',
		],
	});
	assert.equal(els.trendgrid.innerHTML.match(/class="help"/g).length, 1);
	assert.ok(!/javascript:|<img/.test(els.trendgrid.innerHTML));
	for (const m of els.trendgrid.innerHTML.matchAll(/href="([^"]+)"/g)) assert.match(m[1], /^https:\/\/github\.com\/a\/b1$/);
});

test('a missing or broken feed hides the section and never throws', () => {
	for (const feed of [null, undefined, {}, { repos: 'x' }, { repos: [] }, 42, { repos: [{ name: 'a/b' }] }]) {
		const els = page(feed);
		assert.equal(els.trendpanel.hidden, true);
	}
	// even a page error inside rendering only hides the section
	const els = { trendpanel: { hidden: false }, trendtitle: {}, trendgrid: null };
	new Function('TREND', '$', src + '\nrenderTrending();')({ repos: [repo(1, 1)] }, (id) => els[id]);
	assert.equal(els.trendpanel.hidden, true);
});

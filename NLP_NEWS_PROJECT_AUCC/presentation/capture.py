import sys, json, sqlite3, asyncio
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools'))
from playwright.async_api import async_playwright

async def main():
    assets = ROOT / 'assets'
    assets.mkdir(exist_ok=True)
    dbpath = ROOT.parent / 'backend' / 'sports_gemini.db'
    db = sqlite3.connect(dbpath.resolve().as_uri() + '?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    row = dict(db.execute('select * from analysis_snapshots where video_id not like "mock_%" order by id desc limit 1').fetchone())
    result = {'sentiment': json.loads(row['sentiment_json']), 'emotion': json.loads(row['emotion_json']),
              'categories': json.loads(row['category_json']), 'keywords': json.loads(row['keywords_json']),
              'summary': {'summary': row['summary_text'], 'based_on_comments': row['sample_size']}}
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 980}, device_scale_factor=1.5)
        await page.goto('http://127.0.0.1:5173', wait_until='networkidle', timeout=60000)
        await page.evaluate('document.fonts.ready')
        await page.screenshot(path=str(assets/'dashboard.png'), full_page=False)
        # Replay a real stored result so the screenshot does not rerun paid inference.
        async def snapshot(route):
            await route.fulfill(status=200, content_type='application/json', body=json.dumps(result, ensure_ascii=False))
        await page.route('**/api/analysis/*/run', snapshot)
        response = await page.request.get('http://127.0.0.1:5173/api/videos/' + row['video_id'], timeout=60000)
        video = await response.json()
        async def video_response(route):
            await route.fulfill(status=200, content_type='application/json', body=json.dumps(video, ensure_ascii=False))
        await page.route('**/api/videos/' + row['video_id'], video_response)
        await page.goto('http://127.0.0.1:5173/video/' + row['video_id'], wait_until='networkidle', timeout=60000)
        await page.get_by_text('ภาพรวมความรู้สึก', exact=True).wait_for(timeout=30000)
        await page.wait_for_timeout(1800)
        await page.screenshot(path=str(assets/'analysis.png'), full_page=False)
        await page.screenshot(path=str(assets/'analysis-full.png'), full_page=True)
        evidence = {'video': video, 'snapshot_at_utc': row['created_at'], 'result': result,
                    'capture_method': 'Actual UI displaying a real stored analysis snapshot; analysis POST replayed locally for capture.'}
        (ROOT/'evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
        await browser.close()
    print('Captured dashboard and real stored analysis; sample_size=', row['sample_size'])

asyncio.run(main())

"""Run against local backend :8000 and frontend :5173; synthetic alerts only.
Install playwright separately; uses installed Google Chrome, no downloaded browser.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('http://127.0.0.1:5173')
    expect(page.get_by_text('Connected', exact=True)).to_be_visible()
    expect(page.locator('.stock-card')).to_have_count(4)
    page.locator('.stock-card').filter(has_text='MSFT').click()
    expect(page.get_by_role('heading', name='MSFT — Live Price')).to_be_visible()
    expect(page.locator('.recharts-line-curve')).to_be_visible(timeout=10000)
    page.get_by_label('Stock symbol').select_option('AAPL')
    page.get_by_label('Target price').fill('1')
    with page.expect_response(lambda response: response.url.endswith('/alerts') and response.request.method == 'POST') as request:
        page.get_by_role('button', name='Create Alert').click()
    assert request.value.status == 201
    expect(page.locator('.alert-status').filter(has_text='Triggered').first).to_be_visible(timeout=10000)
    expect(page.locator('.notification-toast').first).to_be_visible()
    page.locator('.notification-toast').first.click()
    # Negative case: a deliberately injected FastAPI validation response (mocked only here).
    page.route('**/alerts', lambda route: route.fulfill(status=422, content_type='application/json', body=json.dumps({'detail': [{'msg': 'Input should be greater than 0'}]})) if route.request.method == 'POST' else route.continue_())
    count = page.locator('.alert-item').count()
    page.get_by_label('Target price').fill('10')
    page.get_by_role('button', name='Create Alert').click()
    expect(page.get_by_role('alert')).to_have_text('Input should be greater than 0')
    expect(page.locator('.alert-item')).to_have_count(count)
    page.set_viewport_size({'width': 390, 'height': 844})
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
    expect(page.get_by_role('button', name='Create Alert')).to_be_visible()
    assert not errors, errors
    browser.close()
    print('PASS: real UI -> HTTP create -> in-memory alert -> WebSocket -> visible trigger; selector/chart/toast; mocked 422 rollback; mobile width; no page errors')

"""Download daily KOSPI/KOSDAQ foreign net purchases (KRW) from KRX via pykrx."""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
from pykrx import stock

out = Path(__file__).with_name('data.json')
today = datetime.now(ZoneInfo('Asia/Seoul')).date()
start = today - timedelta(days=800)
markets = {}
for market in ('KOSPI', 'KOSDAQ'):
    # KRX can reject requests or change its site. Never replace prior data with empty results.
    df = stock.get_market_trading_value_by_date(start.strftime('%Y%m%d'), today.strftime('%Y%m%d'), market, etf=False, etn=False, elw=False)
    if df.empty or '외국인합계' not in df.columns:
        raise RuntimeError(f'{market}: KRX returned no usable foreign trading data')
    markets[market] = {idx.strftime('%Y-%m-%d'): int(v) for idx, v in df['외국인합계'].items()}
dates = sorted(set(markets['KOSPI']) & set(markets['KOSDAQ']))
if len(dates) < 30:
    raise RuntimeError('Too few matching trading days; refusing to overwrite data')
rows = [{'date': d, 'KOSPI': markets['KOSPI'][d], 'KOSDAQ': markets['KOSDAQ'][d]} for d in dates]
new_last = rows[-1]['date']
if out.exists():
    old = json.loads(out.read_text(encoding='utf-8'))
    old_rows = old if isinstance(old, list) else old.get('rows', [])
    if old_rows and old_rows[-1]['date'] > new_last:
        raise RuntimeError('Downloaded data is older than existing data')
    merged = {r['date']: r for r in old_rows}
    merged.update({r['date']: r for r in rows})
    rows = [merged[k] for k in sorted(merged)]
out.write_text(json.dumps({'updated_at': datetime.now(ZoneInfo('Asia/Seoul')).isoformat(), 'source': 'KRX via pykrx', 'rows': rows}, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print(f'Updated {len(rows)} days, latest {rows[-1]["date"]}')

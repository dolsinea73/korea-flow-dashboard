import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FILES = {
    "KOSPI": ROOT / "data_4903_20261108.csv",
    "KOSDAQ": ROOT / "data_4854_20261108.csv",
}

def read_csv(path):
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "cp949", "euc-kr"):
        try:
            content = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError(f"CSV 인코딩 확인 필요: {path.name}")

    reader = csv.DictReader(io.StringIO(content))
    if not reader.fieldnames:
        raise ValueError(f"CSV 헤더 없음: {path.name}")

    date_col = next((c for c in reader.fieldnames if "일자" in c or "날짜" in c), None)
    foreign_col = next((c for c in reader.fieldnames if "외국인" in c), None)
    if not date_col or not foreign_col:
        raise ValueError(f"날짜 또는 외국인 열 없음: {path.name}")

    result = {}
    for row in reader:
        date = (row[date_col] or "").strip().replace("/", "-").replace(".", "-")
        value = (row[foreign_col] or "").strip().replace(",", "")
        if not date or not value or value == "-":
            continue
        # KRX CSV 단위: 십억원 -> 원
        result[date] = round(float(value) * 1_000_000_000)
    return result

kospi = read_csv(FILES["KOSPI"])
kosdaq = read_csv(FILES["KOSDAQ"])
dates = sorted(set(kospi) & set(kosdaq))

if not dates:
    raise RuntimeError("두 시장의 공통 거래일이 없습니다.")

rows = [
    {"date": date, "KOSPI": kospi[date], "KOSDAQ": kosdaq[date]}
    for date in dates
]

output = ROOT / "data.json"
output.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"완료: {output.name}, {len(rows)}거래일, 마지막 날짜 {dates[-1]}")

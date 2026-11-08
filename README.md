# 한국 증시 외국인 수급 대시보드

## 맥북에서 웹사이트로 게시하기
1. GitHub에서 새 **공개(Public)** 저장소를 만듭니다.
2. 이 폴더의 `index.html`, `update_data.py`, `.github/workflows/update.yml`을 **경로 그대로** 저장소에 올립니다. (ZIP을 풀어 업로드)
3. 저장소의 **Actions** 탭에서 `Update KRX foreign flows` → **Run workflow**를 한 번 실행합니다. 정상 실행되면 `data.json`이 생성됩니다.
4. **Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save**를 선택합니다.
5. 표시되는 GitHub Pages 주소를 맥북 Safari와 아이폰 Safari에서 똑같이 엽니다.
6. 평일 한국시간 18:30에 업데이트를 시도합니다. GitHub 예약 실행이 지연될 수 있고 KRX 데이터 접속이 실패하면 마지막 성공 데이터가 유지됩니다.

## 데이터 범위
- KOSPI, KOSDAQ의 **외국인합계 순매수 거래대금(원)**
- ETF/ETN/ELW 제외
- 조회일 기준 최근 약 800일의 달력 기간(약 2년 거래일), 기존 데이터가 있으면 합쳐 보존
- 누적선은 선택 기간 첫 거래일부터 합산한 값, 4주 이동평균은 각 주의 마지막 거래일 누적 순매수액 4개를 단순평균하며, 진행 중인 주는 최신 거래일 기준 잠정값을 사용

## 수동 CSV
자동 수집이 막힐 때 `date,KOSPI,KOSDAQ` 헤더로 된 CSV(금액 단위 원)를 화면에서 가져올 수 있습니다. 브라우저에서만 읽고 외부 업로드는 하지 않습니다.

## 주의
이 패키지는 실제 KRX 연결과 GitHub Actions 실행을 확인하지 못한 **배포용 초안**입니다. `pykrx`가 KRX 사이트 변경·차단으로 작동하지 않을 수 있으며, GitHub Pages 공개 저장소에 게시되는 데이터는 공개됩니다. 데이터 수집 실패를 성공으로 표시하지 않습니다.

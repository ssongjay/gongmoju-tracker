import requests
from bs4 import BeautifulSoup


def fetch_ipo_list(page: int = 1) -> list[dict]:
    """38커뮤니케이션에서 최근 공모주 청약 일정을 크롤링"""
    url = f"http://www.38.co.kr/html/fund/index.htm?o=k&page={page}"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = "euc-kr"
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table", {"summary": "공모주 청약일정"})
    if not table:
        return []

    rows = table.find_all("tr")
    results = []

    for row in rows[1:]:  # skip header
        cells = row.find_all("td")
        if len(cells) < 6:
            continue

        stock_name = cells[0].get_text(strip=True)
        schedule = cells[1].get_text(strip=True)
        confirmed_price = cells[2].get_text(strip=True)
        hoped_price = cells[3].get_text(strip=True)
        competition_rate = cells[4].get_text(strip=True)
        brokers_text = cells[5].get_text(strip=True)

        if not stock_name:
            continue

        # Parse price
        ipo_price = 0
        if confirmed_price and confirmed_price != "-":
            ipo_price = int(confirmed_price.replace(",", ""))
        elif hoped_price and hoped_price != "-":
            # Use upper bound of range
            parts = hoped_price.replace(",", "").split("~")
            if parts:
                try:
                    ipo_price = int(parts[-1].strip())
                except ValueError:
                    pass

        # Parse brokers
        brokers = [b.strip() for b in brokers_text.split(",") if b.strip()]

        results.append({
            "stock_name": stock_name,
            "schedule": schedule,
            "ipo_price": ipo_price,
            "confirmed_price": confirmed_price,
            "hoped_price": hoped_price,
            "competition_rate": competition_rate,
            "brokers": brokers,
        })

    return results


if __name__ == "__main__":
    for item in fetch_ipo_list():
        print(item)

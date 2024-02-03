from base import SECFilingsLoader

if __name__ == '__main__':
    docs = SECFilingsLoader(ticker="AAPL",year=2023,filing_types=["10-K","10-Q"])
    d = docs.load_data()
    print(d)
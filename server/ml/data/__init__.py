from .create_dataset import create_datasets

from server.ml import TICKERS


def main():
    # print(TICKERS)
    create_datasets(tickers=list(TICKERS.keys()))


if __name__ == "__main__":
    main()
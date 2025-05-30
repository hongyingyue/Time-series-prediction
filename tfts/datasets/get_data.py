"""Generate the example data script
- https://github.com/keras-team/keras/blob/v3.3.3/keras/src/utils/file_utils.py#L130-L327
"""

import logging
import random
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from tfts.constants import TFTS_ASSETS_CACHE

logger = logging.getLogger(__name__)


air_passenger_url = (
    "https://raw.githubusercontent.com/AileenNielsen/TimeSeriesAnalysisWithPython/master/data/AirPassengers.csv"
)


def get_data(
    name: str = "sine",
    train_length: int = 24,
    predict_sequence_length: int = 8,
    test_size: float = 0.1,
) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[Tuple[np.ndarray, np.ndarray]], None]:
    assert (test_size >= 0) & (test_size <= 1), "test_size is the ratio of test dataset"
    if name == "sine":
        return get_sine(train_length, predict_sequence_length, test_size=test_size)

    elif name == "airpassengers":
        return get_air_passengers(train_length, predict_sequence_length, test_size=test_size)

    else:
        raise ValueError(f"unsupported data of {name} yet, try 'sine', 'airpassengers'")


def get_sine(
    train_sequence_length: int = 24, predict_sequence_length: int = 8, test_size: float = 0.2, n_examples: int = 100
) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[Tuple[np.ndarray, np.ndarray]]]:
    """
    Generate synthetic sine wave data.

    Parameters:
    train_sequence_length (int): Length of the training sequence.
    predict_sequence_length (int): Length of the prediction sequence.
    test_size (float): Fraction of the data to use for validation.
    n_examples (int): Number of examples to generate.

    Returns:
    (tuple): Two tuples of numpy arrays containing training and validation data.
    """
    x: List[np.ndarray] = []
    y: List[np.ndarray] = []
    for _ in range(n_examples):
        rand = random.random() * 2 * np.pi
        sig1 = np.sin(np.linspace(rand, 3.0 * np.pi + rand, train_sequence_length + predict_sequence_length))
        sig2 = np.cos(np.linspace(rand, 3.0 * np.pi + rand, train_sequence_length + predict_sequence_length))

        x1 = sig1[:train_sequence_length]
        y1 = sig1[train_sequence_length:]
        x2 = sig2[:train_sequence_length]
        y2 = sig2[train_sequence_length:]

        x_ = np.array([x1, x2])
        y_ = np.array([y1, y2])

        x.append(x_.T)
        y.append(y_.T)

    x_array = np.array(x)[:, :, 0:1]
    y_array = np.array(y)[:, :, 0:1]
    logging.info("Load sine data", x_array.shape, y_array.shape)

    if test_size > 0:
        slice = int(n_examples * (1 - test_size))
        x_train = x_array[:slice]
        y_train = y_array[:slice]
        x_valid = x_array[slice:]
        y_valid = y_array[slice:]
        return (x_train, y_train), (x_valid, y_valid)
    return x_array, y_array


def get_air_passengers(train_sequence_length: int = 24, predict_sequence_length: int = 8, test_size: float = 0.2):
    """
    A function that loads and preprocesses the air passenger data.

    Args:
        train_sequence_length (int): The length of each input sequence.
        predict_sequence_length (int): The length of each output sequence.
        test_size (float): The fraction of the data to use for validation.

    Returns:
        Tuple of training and validation data, each containing inputs and outputs.

    """
    # air_passenger_url = "../examples/data/international-airline-passengers.csv"
    df = pd.read_csv(air_passenger_url, parse_dates=None, date_parser=None, nrows=144)
    v = df.iloc[:, 1:2].values
    v = (v - np.max(v)) / (np.max(v) - np.min(v))  # MinMaxScaler

    x: List[np.ndarray] = []
    y: List[np.ndarray] = []
    for seq in range(1, train_sequence_length + 1):
        x_roll = np.roll(v, seq, axis=0)
        x.append(x_roll)
    x_array = np.stack(x, axis=1)
    x_array = x_array[train_sequence_length:-predict_sequence_length, ::-1, :]

    for seq in range(predict_sequence_length):
        y_roll = np.roll(v, -seq)
        y.append(y_roll)
    y_array = np.stack(y, axis=1)
    y_array = y_array[train_sequence_length:-predict_sequence_length]
    logging.info("Load air passenger data", x_array.shape, y_array.shape)

    if test_size > 0:
        slice = int(len(x_array) * (1 - test_size))
        x_train = x_array[:slice]
        y_train = y_array[:slice]
        x_valid = x_array[slice:]
        y_valid = y_array[slice:]
        return (x_train, y_train), (x_valid, y_valid)
    return x_array, y_array


def get_stock_data(ticker: str = "NVDA", start_date="2023-09-01", end_date="2024-03-15") -> pd.DataFrame:
    """
    Retrieve historical stock data for a given ticker symbol.
    """
    # Download data
    import yfinance as yf

    try:
        logger.info(f"Retrieving data for {ticker} from {start_date} to {end_date}")

        data = yf.download(ticker, start=start_date, end=end_date, progress=False)

        if data.empty:
            logger.warning(f"No data returned for ticker {ticker}")
            raise ValueError(f"No data available for ticker: {ticker}")

        logger.info(f"Successfully retrieved {len(data)} records for {ticker}")
        return data

    except Exception as e:
        raise ValueError(f"Error retrieving stock data: {str(e)}")

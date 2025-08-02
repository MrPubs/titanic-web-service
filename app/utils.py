from app.models import HistogramResponse, HistogramMetadata, Histogram, Bin
import numpy as np
import pandas as pd


def make_histogram(data: np.ndarray, bucket_count: int = 100) -> HistogramResponse:
    '''
    Structured Histogram making function, takes an ndarray representing a Numerical column and returns
    a Histogram JSON following the HistogramResponse model.
    :param data: Numerical column contents
    :param bucket_count: count of percentile buckets to divide
    :return: Histogram JSON following the HistogramResponse model
    '''

    # make histo and return
    groups = np.linspace(0, 100, num=bucket_count + 1)
    percentile_edges: np.ndarray = np.percentile(data, groups)
    hist: np.ndarray
    hist, _ = np.histogram(data, bins=percentile_edges)

    # JSONify
    bins: list[Bin] = []
    for i in range(bucket_count):
        if hist[i] != 0:
            bins.append(Bin(
                percentile_start=round(float(groups[i]), 4),
                percentile_end=round(float(groups[i + 1]), 4),
                bin_start=round(float(percentile_edges[i]), 4),
                bin_end=round(float(percentile_edges[i + 1]), 4),
                count=int(hist[i])
            ))

    metadata = HistogramMetadata(
        field="Fare",
        bucket_count=bucket_count,
        total_count=int(hist.sum())
    )

    histogram = Histogram(bins=bins)
    return HistogramResponse(metadata=metadata, histogram=histogram)


def steralize_df(df: pd.DataFrame) -> pd.DataFrame:
    '''
    remove bad data with fixed data
    :param df: input df to clean
    :return: cleaned data
    '''
    # return df.replace([np.nan], None)  # replace NaN's with None
    return df

if __name__ == '__main__':
    pass

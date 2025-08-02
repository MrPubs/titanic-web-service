import numpy as np
import pytest

from app.utils import make_histogram
from app.models import HistogramResponse

def test_make_histogram_with_array():

    data = np.array([5, 10, 15, 20, 25, 30])
    bucket_count = 3
    response: HistogramResponse = make_histogram(data, bucket_count=bucket_count)

    # Histogram Tests
    assert isinstance(response, HistogramResponse)  # Check return model is HistogramResponse
    assert response.metadata.bucket_count == bucket_count  # Check the bucket count is maintained
    assert response.metadata.total_count == 6  # check for total count of Datapoints
    assert len(response.histogram.bins) <= bucket_count  # check for no more bins than there are buckets

    # Bin Tests
    for i in range(len(response.histogram.bins) - 1):
        curr = response.histogram.bins[i]
        nxt = response.histogram.bins[i + 1]
        assert curr.percentile_end <= nxt.percentile_start  # check for non overlapping percentiles
        assert curr.bin_end <= nxt.bin_start  # check for non overlapping edges

def test_make_histogram_with_empty_array():

    # Empty data!
    data = np.array([])
    with pytest.raises(Exception):  # check for exception raised indeed
        make_histogram(data, bucket_count=3)

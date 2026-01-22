import pandas as pd
from src.etl_scripts.transform import validate_data_quality
import pytest

def test_data_quality_pass(tmp_path):
    file = tmp_path / "data.csv"

    df = pd.DataFrame({
        "InvoiceNo": ["A1"],
        "StockCode": ["S1"],
        "Quantity": [1],
        "UnitPrice": [10.0]
    })

    df.to_csv(file, index=False)

    # Should NOT raise error
    validate_data_quality(str(file), "test_stage")


def test_data_quality_fail_empty(tmp_path):
    file = tmp_path / "data.csv"
    pd.DataFrame().to_csv(file, index=False)

    with pytest.raises(ValueError):
        validate_data_quality(str(file), "test_stage")

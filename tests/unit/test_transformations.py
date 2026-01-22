import pandas as pd
from src.etl_scripts.transform import clean_and_enrich_data


def test_total_item_price_calculation(tmp_path):
    input_file = tmp_path / "raw.csv"
    output_file = tmp_path / "clean.csv"

    df = pd.DataFrame({
        "Quantity": [2, 3],
        "UnitPrice": [10.0, 5.0],
        "InvoiceNo": ["A1", "A2"],
        "StockCode": ["S1", "S2"]
    })

    df.to_csv(input_file, index=False)

    clean_and_enrich_data(str(input_file), str(output_file))

    result = pd.read_csv(output_file)
    assert "total_item_price" in result.columns
    assert result["total_item_price"].iloc[0] == 20.0


def test_no_empty_dataframe(tmp_path):
    input_file = tmp_path / "raw.csv"
    output_file = tmp_path / "clean.csv"

    df = pd.DataFrame({
        "Quantity": [1],
        "UnitPrice": [1.0],
        "InvoiceNo": ["A1"],
        "StockCode": ["S1"]
    })

    df.to_csv(input_file, index=False)

    clean_and_enrich_data(str(input_file), str(output_file))
    result = pd.read_csv(output_file)

    assert len(result) > 0


def test_quantity_positive(tmp_path):
    input_file = tmp_path / "raw.csv"
    output_file = tmp_path / "clean.csv"

    df = pd.DataFrame({
        "Quantity": [5],
        "UnitPrice": [2.0],
        "InvoiceNo": ["A1"],
        "StockCode": ["S1"]
    })

    df.to_csv(input_file, index=False)

    clean_and_enrich_data(str(input_file), str(output_file))
    result = pd.read_csv(output_file)

    assert result["Quantity"].iloc[0] > 0

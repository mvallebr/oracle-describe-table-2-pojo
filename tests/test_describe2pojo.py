from describe2pojo import main
import pytest
import os

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
TMP_FOLDER = os.path.join(os.path.dirname(__file__), "tmp")
os.makedirs(TMP_FOLDER)

test_data = [
    ("usage_writers.txt",   False, "UsageWriters.java"),
    ("usage_chain_steps.txt",  False, "UsageChainSteps.java"),
    ("usage_writer_chains.txt",  False, "UsageWriterChains.java"),
]


@pytest.mark.parametrize(argnames="input_file,overwrite,expected_output", argvalues=test_data)
def test_main(input_file, overwrite, expected_output):
    with open(os.path.join(DATA_FOLDER, expected_output), "r") as f:
        expected_output_text = f.read().strip()

    input_file_full_path = os.path.join(DATA_FOLDER, input_file)

    main(input_file_full_path, TMP_FOLDER, overwrite)

    actual_output_file_full_path = os.path.join(TMP_FOLDER, expected_output)
    with open(os.path.join(DATA_FOLDER, actual_output_file_full_path), "r") as f:
        actual_output_text = f.read().strip()

    assert actual_output_text == expected_output_text, f"\n`{actual_output_text}`\n\n!=\n\n`{expected_output_text}`"

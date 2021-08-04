from describe2pojo import main
import pytest
import os 

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
TMP_FOLDER = os.path.join(os.path.dirname(__file__), "tmp")

test_data = [
    ("usage_writers.txt", "UsageWriters.java", False, "UsageWritersExpected.java"),
    ("usage_chain_steps.txt", "UsageChainSteps.java", False, "UsageChainStepsExpected.java"),
    ("usage_writer_chains.txt", "UsageWriterChains.java", False, "UsageWriterChainsExpected.java"),
]


@pytest.mark.parametrize(argnames="input_file,output_file,overwrite,expected_output", argvalues=test_data)
def test_main(input_file,output_file,overwrite,expected_output):
    with open(os.path.join(DATA_FOLDER, expected_output), "r") as f:
        expected_output_text = f.read().strip()
         
    input_file_full_path = os.path.join(DATA_FOLDER, input_file)
    output_file_full_path = os.path.join(TMP_FOLDER, output_file)
    main(input_file_full_path, output_file_full_path, overwrite) 

    with open(os.path.join(DATA_FOLDER, output_file_full_path), "r") as f:
        actual_output_text = f.read().strip()
    
    assert actual_output_text == expected_output_text

 

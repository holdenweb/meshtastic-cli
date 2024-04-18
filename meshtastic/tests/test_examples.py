"""
Meshtastic test that the examples run as expected. We assume a suitable
python virtual environment is active, to allow the tester to create it by
whatever means is most convenient.
"""
import subprocess

import pytest


@pytest.mark.examples
def test_examples_hello_world_serial_no_arg():
    """Test hello_world_serial without any args"""
    return_value, _ = subprocess.getstatusoutput(
        "python3 examples/hello_world_serial.py"
    )
    assert return_value == 3


@pytest.mark.examples
def test_examples_hello_world_serial_with_arg(capsys):
    """Test hello_world_serial with arg"""
    return_value, _ = subprocess.getstatusoutput(
        "python3 examples/hello_world_serial.py hello"
    )
    assert return_value == 1
    out, err = capsys.readouterr()
    assert err == ""
    assert "If no connection arguments are specified," in out
    # TODO: Why does this not work?
    # assert out == 'Warning: No Meshtastic devices detected.'

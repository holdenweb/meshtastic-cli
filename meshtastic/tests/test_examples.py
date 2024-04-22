"""
Meshtastic test that the examples run as expected. We assume a suitable
python virtual environment is active, to allow the tester to create it by
whatever means is most convenient.
"""
import subprocess

import pytest


@pytest.mark.examples
def test_examples_hello_world_serial_no_arg():
    """Test hello_world_serial without any args.

    A valid test, but not a particularly valuable one."""
    print("test1")
    return_value, _ = subprocess.getstatusoutput(
        "python3 examples/hello_world_serial.py"
    )
    assert return_value == 3


@pytest.mark.examples
def test_examples_hello_world_serial_with_arg():
    """Test hello_world_serial with arg"""
    print("test2")
    result = subprocess.run(
        ["python3", "examples/hello_world_serial.py", "hello"],
        capture_output=True,
    )
    assert result.returncode == 2
    assert type(result.stderr) == bytes
    assert type("No serial Meshtastic device detected".encode('utf-8')) == bytes
    assert b"No serial Meshtastic device detected" in result.stderr


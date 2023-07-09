from unittest.mock import Mock, patch, call

from narpyn.ona.nar import (
    expect_output,
    get_output,
    get_raw_output,
    send_input,
    setup_nars,
    setup_nars_ops,
)


@patch("subprocess.Popen")
def test_send_input(mock_popen):
    mock_stdin = Mock()
    mock_stdout = Mock()
    mock_popen.return_value = Mock(stdin=mock_stdin, stdout=mock_stdout)
    send_input(mock_popen(), "test_input")
    mock_stdin.write.assert_called_once_with("test_input\n")
    mock_stdin.flush.assert_called_once()


@patch("subprocess.Popen")
def test_get_raw_output(mock_popen):
    mock_stdin = Mock()
    mock_stdout = Mock()
    mock_popen.return_value = Mock(stdin=mock_stdin, stdout=mock_stdout)
    mock_stdout.readline.side_effect = [
        "^op1 args [a b c]\n",
        "done with 0 additional inference steps.\n",
    ]
    output = get_raw_output(mock_popen())
    assert len(output) == 1
    assert output[0] == "^op1 args [a b c]"


@patch("subprocess.Popen")
def test_get_output(mock_popen):
    mock_stdin = Mock()
    mock_stdout = Mock()
    mock_popen.return_value = Mock(stdin=mock_stdin, stdout=mock_stdout)
    mock_stdout.readline.side_effect = [
        "Input: task1! :|: occurrenceTime=5\n",
        "Derived: task2! :|: occurrenceTime=5\n",
        "Revised: sent. :|: occurrenceTime=2\n",
        "Answer: ^op1 ({SELF} * arg)! :|: occurrenceTime=5\n",
        "^op1 executed with args ({SELF} * arg)\n",
        "done with 0 additional inference steps.\n",
    ]
    output = get_output(mock_popen())
    assert len(output["input"]) == 1
    assert output["input"][0] == {
        "occurrenceTime": "5",
        "punctuation": "!",
        "term": "task1",
    }
    assert len(output["derivations"]) == 2
    assert output["derivations"][0] == {
        "occurrenceTime": "5",
        "punctuation": "!",
        "term": "task2",
    }
    assert output["derivations"][1] == {
        "occurrenceTime": "2",
        "punctuation": ".",
        "term": "sent",
    }
    assert len(output["answers"]) == 1
    assert output["answers"][0] == {
        "occurrenceTime": "5",
        "punctuation": "!",
        "term": "^op1 ({SELF} * arg)",
    }
    assert len(output["executions"]) == 1
    assert output["executions"][0] == {"operator": "^op1", "arguments": ["{SELF}", "arg"]}
    assert (
        output["raw"]
        == "Input: task1! :|: occurrenceTime=5\nDerived: task2! :|: occurrenceTime=5\nRevised: sent. :|: occurrenceTime=2\nAnswer: ^op1 ({SELF} * arg)! :|: occurrenceTime=5\n^op1 executed with args ({SELF} * arg)"
    )


@patch("subprocess.Popen")
def test_expect_output(mock_popen):
    mock_stdin = Mock()
    mock_stdout = Mock()
    mock_popen.return_value = Mock(stdin=mock_stdin, stdout=mock_stdout)
    mock_stdout.readline.side_effect = [
        "Input: task1. :|: occurrenceTime=now\n",
        "Derived: task2. occurrenceTime=eternal\n",
        "Revised: task3. :|: occurrenceTime=now\n",
        "Answer: task4. :|: occurrenceTime=now\n",
        "^op1 executed with args arg\n",
        "done with 0 additional inference steps.\n",
    ]
    targets = ["^op1"]
    output = expect_output(mock_popen(), targets)
    assert len(output["input"]) == 1
    assert output["input"][0] == {
        "occurrenceTime": "now",
        "punctuation": ".",
        "term": "task1",
    }
    assert len(output["derivations"]) == 2
    assert output["derivations"][0] == {
        "occurrenceTime": "eternal",
        "punctuation": ".",
        "term": "task2",
    }
    assert output["derivations"][1] == {
        "occurrenceTime": "now",
        "punctuation": ".",
        "term": "task3",
    }
    assert len(output["answers"]) == 1
    assert output["answers"][0] == {
        "occurrenceTime": "now",
        "punctuation": ".",
        "term": "task4",
    }
    assert len(output["executions"]) == 1
    assert output["executions"][0] == {"operator": "^op1", "arguments": ["arg"]}
    assert (
        output["raw"]
        == "Input: task1. :|: occurrenceTime=now\nDerived: task2. occurrenceTime=eternal\nRevised: task3. :|: occurrenceTime=now\nAnswer: task4. :|: occurrenceTime=now\n^op1 executed with args arg"
    )


@patch("subprocess.Popen")
def test_setup_nars_ops(mock_popen):
    mock_stdin = Mock()
    mock_stdout = Mock()
    mock_popen.return_value = Mock(stdin=mock_stdin, stdout=mock_stdout)
    ops = ["op1", "op2"]
    setup_nars_ops(mock_popen(), ops)
    mock_stdin.write.assert_has_calls(
        [call("*setopname 1 op1\n"), call("*setopname 2 op2\n"), call(f"*babblingops={len(ops)}\n")]
    )
    mock_stdin.flush.assert_has_calls([call()] * 3)
    send_input_calls = [call(mock_popen(), f"*babblingops={len(ops)}")]
    setup_nars_ops(mock_popen(), ops, babblingops=5)
    send_input_calls.append(call(mock_popen(), "*babblingops=5"))
    mock_stdin.write.assert_has_calls(
        [call("*setopname 1 op1\n"), call("*setopname 2 op2\n"), call("*babblingops=5\n")]
    )
    mock_stdin.flush.assert_has_calls([call()] * 3)
    assert mock_stdin.write.call_count == 6


@patch("subprocess.Popen")
def test_setup_nars(mock_popen):
    mock_stdin = Mock()
    mock_stdout = Mock()
    mock_popen.return_value = Mock(stdin=mock_stdin, stdout=mock_stdout)
    setup_nars(
        mock_popen(),
        ["op1", "op2"],
        motor_babbling=0.5,
        babblingops=3,
        volume=100,
        decision_threshold=0.8,
    )
    mock_stdin.write.assert_has_calls(
        [
            call("*reset\n"),
            call("*setopname 1 op1\n"),
            call("*setopname 2 op2\n"),
            call("*babblingops=3\n"),
            call("*motorbabbling=0.5\n"),
            call("*volume=100\n"),
            call("*decisionthreshold=0.8\n"),
        ]
    )
    mock_stdin.flush.assert_has_calls([call()] * 7)
    assert mock_stdin.write.call_count == 7

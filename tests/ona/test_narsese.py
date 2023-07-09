from narpyn.ona.narsese import (
    Goal,
    ext,
    loc,
    nal_demand,
    nal_now,
    narsify,
    parse_execution,
    parse_reason,
    parse_task,
    parse_truth_value,
    pos,
)


# Test narsify function
def test_narsify():
    assert narsify([1, 2, 3]) == "1,2,3"
    assert narsify(["a", "b", "c"]) == "a,b,c"
    assert narsify([]) == ""


# Test loc function
def test_loc():
    assert loc((0, 0)) == "loc_x0_y0"
    assert loc((1, 2)) == "loc_x1_y2"
    assert loc((-1, -2)) == "loc_x-1_y-2"


# Test pos function
def test_pos():
    assert pos("loc_x0_y0") == (0, 0)
    assert pos("loc_x1_y2") == (1, 2)
    assert pos("loc_x-1_y-2") == (-1, -2)


# Test ext function
def test_ext():
    assert ext("abc") == "{abc}"
    assert ext("def") == "{def}"
    assert ext("") == "{}"


# Test nal_demand function
def test_nal_demand():
    assert nal_demand("demand") == "demand! :|:"
    assert nal_demand("request") == "request! :|:"
    assert nal_demand("order") == "order! :|:"


# Test nal_now function
def test_nal_now():
    assert nal_now("statement") == "statement. :|:"
    assert nal_now("fact") == "fact. :|:"
    assert nal_now("truth") == "truth. :|:"


# Test parse_truth_value function
def test_parse_truth_value():
    assert parse_truth_value("frequency=0.5 confidence=0.9") == {
        "frequency": 0.5,
        "confidence": 0.9,
    }
    assert parse_truth_value("frequency=0.3, confidence=0.8") == {
        "frequency": 0.3,
        "confidence": 0.8,
    }


# Test parse_task function
def test_parse_task():
    assert parse_task("task! :|: occurrenceTime=3 Truth: f=0.7 c=0.89") == {
        "occurrenceTime": "3",
        "punctuation": "!",
        "term": "task",
        'truth': {'frequency': 0.7, 'confidence': 0.89},
    }
    assert parse_task(
        "task! occurrenceTime=eternal Priority=1.0 Truth: f=0.5 c=0.9"
    ) == {
        "occurrenceTime": "eternal",
        "punctuation": "!",
        "term": "task",
        "truth": {"frequency": 0.5, "confidence": 0.9},
    }


# Test parse_reason function
def test_parse_reason():
    assert parse_reason(
        "implication: asdf. Truth: frequency=0.5 confidence=0.9 precondition: bls. :|: occurrenceTime=7 decision expectation=0.67"
    ) == {
        "desire": "0.67",
        "hypothesis": {
            "occurrenceTime": "eternal",
            "punctuation": ".",
            "term": "asdf",
            "truth": {"frequency": 0.5, "confidence": 0.9},
        },
        "precondition": {"occurrenceTime": "7", "punctuation": ".", "term": "bls"},
    }


# Test parse_execution function
def test_parse_execution():
    assert parse_execution("^op1 executed") == {"operator": "^op1", "arguments": []}
    assert parse_execution("^op2 executed with args ({SELF} * arg * x)") == {
        "operator": "^op2",
        "arguments": ["{SELF}", "arg", "x"],
    }


# Test Goal class
def test_goal():
    def is_satisfied():
        return True

    goal = Goal("symbol", is_satisfied, ["knowledge"])
    assert goal.symbol == "symbol"
    assert goal.satisfied() is True
    assert goal.knowledge == ["knowledge"]
    assert str(goal) == "Goal symbol; ['knowledge']"

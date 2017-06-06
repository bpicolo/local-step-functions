pass_state_cases = [
    {
        "state": {
            "Type": "Pass",
            "End": True
        },
        "input": {},
        "output": {}
    },
    {
        "state": {
            "Type": "Pass",
            "Result": "Hello",
            "ResultPath": "$.foo.bar",
            "End": True
        },
        "input": {
            "foo": {
                "boy": 1
            }
        },
        "output": {
            "foo": {
                "boy": 1,
                "bar": "Hello"
            }
        }
    },
    {
        "state": {
            "Type": "Pass",
            "Result": "Hello",
            "ResultPath": "$.foo.bar",
            "End": True
        },
        "input": {},
        "output": {
            "foo": {
                "bar": "Hello"
            }
        }
    },
    {
        "state": {
            "Type": "Pass",
            "Result": None,
            "End": True
        },
        "input": {'bar': 'baz'},
        "output": {'bar': 'baz'}
    },
    {
        "state": {
            "Type": "Pass",
            "Result": None,
            "ResultPath": "$.foo",
            "End": True
        },
        "input": {'bar': 'baz'},
        "output": {'bar': 'baz', 'foo': {'bar': 'baz'}}
    },
    {
        "state": {
            "Type": "Pass",
            "Result": "Hello",
            "End": True
        },
        "input": {},
        "output": "Hello"
    },
    {
        "state": {
            "Type": "Pass",
            "Result": "Hello",
            "ResultPath": "$.foo",
            "End": True
        },
        "input": {},
        "output": {
            "foo": "Hello"
        }
    }
]

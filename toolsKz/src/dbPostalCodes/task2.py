# ()
# []
# <>
# {}

# test_str_1 = input()
test_str_1 = "[qwerty;]"

# test_str_2 = input()
test_str_2 = "a[a(i]"

checker = {
    "(": {
        "num": 0,
        "first_index": -1,
        "mark": 1
    },
    ")": {
        "num": 0,
        "first_index": -1,
        "mark": 1
    },
    "{": {
        "num": 0,
        "first_index": -1,
        "mark": 2,
    },
    "}": {
        "num": 0,
        "first_index": -1,
        "mark": 2,
    },
    "<": {
        "num": 0,
        "first_index": -1,
        "mark": 3,
    },
    ">": {
        "num": 0,
        "first_index": -1,
        "mark": 3,
    },
    "[": {
        "num": 0,
        "first_index": -1,
        "mark": 4
    },
    "]": {
        "num": 0,
        "first_index": -1,
        "mark": 4
    }
}

for index, value in enumerate(test_str_2):
    if value in checker.keys():
        checker[value]["num"] += 1
        if checker[value]["first_index"] == -1:
            checker[value]["first_index"] = index

check_mark_struct = {
    "opened": 0,
    "closed": 0
}

check_mark_numbers = {}

for i in checker.keys():

    mark = checker[i]["mark"]

    if mark not in check_mark_numbers.keys():
        check_mark_numbers.update(
            {
                mark: {
                    "opened": checker[i]["num"],
                    "closed": 0
                }
            }
        )

    else:

        check_mark_numbers[mark]["closed"] = checker[i]["num"]

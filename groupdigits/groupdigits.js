'use strict';
// See the attached README file for what needs to be done.


// Formats an amount according to the grouping strategy in groupings. Groups
//    are separated with a `separator` string.
//
//    Args:
//        amount: Number - The amount to be formatted.
//        grouping: List[int] - Each element is the number of digits in a group;
//            elements with higher indices are further left. An element with value
//            -1 means that no further grouping is done. An element with value 0
//            means that the previous element is used for all groups further left.
//        separator: string - The string to use as a separator.
//
//    Returns: A string, consisting of the input amount grouped and with
//        separators inserted.
function group_digits(amount, grouping, separator) {
  throw "Please supply an implementation"
}

// Pad a string to at least 20 characters
function fmt20(s) {
  return ("                    " + s).slice(-20)
}


// Runs all the supplied test cases
function run_tests(testCases) {
  var failures = 0;
  testCases.forEach(function(testCase) {

    var amount = testCase[0];
    var groupings = testCase[1];
    var separator = testCase[2];
    var expected = testCase[3];

    var actual;

    var wasError = false;

    try {
       actual = group_digits(amount, groupings, separator)
    } catch (e) {
      console.log("ERR : expected", fmt20(expected), "got", e);
      failures++;
      wasError = true;
    }

    if (!wasError) {
      if (expected != actual) {
        console.log("FAIL: expected", fmt20(expected), "got", fmt20(actual));
        failures++;
      } else {
        console.log("OK  : correct ", fmt20(actual));
      }
    }
  })
  console.assert(!failures, "Unexpected failures were found.");
}

var BASIC_TESTS = [
    [0, [3, 0], ",", "0"],
    [100, [3, 0], ",", "100"],
    [1000, [3, 0], ",", "1,000"],
    [1000, [3, 3, 0], ",", "1,000"],
    [1000000, [3, 3, 0], ",", "1,000,000"],
    [1000000, [3, 0], ",", "1,000,000"],
    [1000000, [3, 0], " ", "1 000 000"],
    [1000000, [3, -1], ",", "1000,000"],
    [1000000, [3, 3, -1], ",", "1,000,000"],
    [70000000, [4, 0], " ", "7000 0000"],
    [4154041062, [4, 3, 0], "-", "415-404-1062"],
    [4154041062, [4, 3, -1], "-", "415-404-1062"],
    [10, [1, 1, 1, 1, -1], "! ", "1! 0"],
    [56781234, [1, 0], "", "56781234"],
    [56781234, [-1], ".", "56781234"],
    [19216801, [1, 1, 3, 0], ".", "192.168.0.1"],
]


run_tests(BASIC_TESTS)

# py-switch-case

py-switch-case allows Python to utilize switch and case statements found in other languages. Note: refrain from using anything besides strings, float, and integers as value unless absolutely necessary.

## Example
```python
from py-switch-case import switch

def found_a():
    print("Matched against 5")

def default_match():
    print("Didn't match against anything")

val = 7
with switch(val) as s:
    s.case(5, found_a)
    s.case(7, lambda: print("Matched against 7"))
    s.default(default_match)
```

## Installation

TBA

## Features
* Match against a regular expression
* Match against a function
* Match against a list or a range
* Default case
* Retrieve result if function returns a value
* Throws exception if:
	* A case is defined after the default case
	* No default case
	* Matching against an unknown type
	* Function is not callable
	* Duplicate cases, matches, and calls exist
	
## More examples

TBA
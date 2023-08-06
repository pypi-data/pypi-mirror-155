
# Text Cleaner

This module provides a simple class to remove special chars (ex. Ä -> A, ö -> o) from a string.





## Authors

- [@nerdlertech](https://github.com/nerdlertech)


## Usage

```python
from text_cleaner import cleaner

example = "\tHello   this\t  is   a test"
example = cleaner(example).text
```

## Output

```text
Hello this is a test
```
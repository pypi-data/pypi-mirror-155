Number to letters
=================

A python library to convert numbers to their catalan text representation. Decimals are managed as currency (1.5 is 'one and fifty') 

### Quick start 

Install it using [pip](https://pypi.python.org/pypi/pip):

    pip install nombrestolletres

### Usage

Import the library in your project and use it:

```python
from nombrestolletres import number_to_letters

number_to_letters(11452915)
> 'onze milions quatre-cents cinquanta-dos mil nou-cents quinze'
```


### Examples

* `1245`: 'mil dos-cents quaranta-cinc'
* `-30`: 'menys trenta'
* `0`: 'zero'
* `23.5`: 'vint-i-tres amb cinquanta'

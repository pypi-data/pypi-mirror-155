> # Calculator Module for Python
> By White Night
> 
> [![PYPI](https://img.shields.io/pypi/v/whiteCalculator?style=for-the-badge)](https://pypi.org/project/whiteCalculator/)
> [![PYPI](https://img.shields.io/pypi/pyversions/whiteCalculator?style=for-the-badge)](https://pypi.org/project/whiteCalculator/)
> [![PYPI](https://img.shields.io/pypi/wheel/whiteCalculator?style=for-the-badge)](https://pypi.org/project/whiteCalculator/)
> [![GITHUB](https://img.shields.io/github/contributors/WhiteNightAWA/whiteCalculator?style=for-the-badge)](https://github.com/WhiteNightAWA/whiteCalculator/)
> [![License](https://img.shields.io/github/license/WhiteNightAWA/whiteCalculator?style=for-the-badge)](https://github.com/WhiteNightAWA/whiteCalculator/)
> [![GITHUB](https://img.shields.io/github/languages/code-size/WhiteNightAWA/whiteCalculator?style=for-the-badge)](https://github.com/WhiteNightAWA/whiteCalculator/)
> [![GITHUB](https://img.shields.io/github/issues/WhiteNightAWA/whiteCalculator?style=for-the-badge)](https://github.com/WhiteNightAWA/whiteCalculator/)
> [![GITHUB](https://img.shields.io/github/issues-pr/WhiteNightAWA/whiteCalculator?style=for-the-badge)](https://github.com/WhiteNightAWA/whiteCalculator/)
> [![GITHUB](https://img.shields.io/github/commit-activity/y/WhiteNightAWA/whiteCalculator?style=for-the-badge)](https://github.com/WhiteNightAWA/whiteCalculator/)

***
## Install
```shell
# Linux/macOS
python3 -m pip install -U whiteCalculator

# Windows
py -3 -m pip install -U whiteCalculator
```
***
# [QuickStart](./INFO/QuickStart.md)
### Calculator
```python
from whiteCalculator import Calculator
c = Calculator()
print(c.run("1+8(5^2)"))
# Output: 201
print(c.run("9Ans"))
# Output: 1809
```
### Formula
```python
from whiteCalculator import Formula
Formula.PythagorasTheorem.getA(b=4, c=5)
# Output: 3
Formula.PythagorasTheorem.getA(b="2^2", c="√(25)")
# Output: 3
```
#### Formula List
```python
PythagorasTheorem, LensFormula, LinearMagnificationFormula
```
***
# [DOCS](https://whitenightawa.github.io/whiteCalculator/)
***
### TODO
- make Doc
- more Formula
- Calculate without eval
***
### Errors
```python
from whiteCalculator import Calculator

c1 = Calculator(skipError=True) # Default is True
c1.run("9/0")
# Output: Error: division by zero

c2 = Calculator(skipError=False)
c2.run("9/0")
# Outputs:
# Traceback (most recent call last):
#     ...
# ZeroDivisionError: division by zero
```
***
## You can use:
- `sin` / `asin` / `sinh`
- `cos` / `acos` / `cosh`
- `tan` / `atan` / `tanh`
- `ln` / `log`
- `×` / `•`
- `^` / `*` / `power`
- `√` / `sqrt`
- `π` / `pi`
- `%`
- `÷`
- `Ans`

# jdutable

Command line table data visualisation tool.

## Installation

```bash
> pip(3) install (-U) jdutable
```

and

```python
from jdutable import TableWriter
```

## Instantiation
```python
table = TableWriter()
```

## Methods

### Add data

```python
def set_header(self, header: list[str])
```
... to add a list of strings as the header of the table.


```python
def set_footer(self, footer: list[str])
```
... to add a list of strings as the footer of the table.

```python
def append(self, line:list[str])
```
... to add a line of strings to the content of the table.

```python
def append_bulk(self, data: list[list[str]])
```
... to add multiple lines to the content of the table.

```python
def from_csv(self, filename: Path, header: bool = False, footer: bool = False, sep: str = ",")
```
... to import a csv file. The parameter are:
- filename: path to the csv file to import
- header: boolean to tell if csv file contains a header
- footer: boolean to tell if csv file contains a footer
- sep: string defining what the csv delimiter is



### Parameters
```python
def set_uppercased(self, state: bool)
```
... to print the header and footer with uppercased letters.

```python
def set_border(self, state: bool)
```
... to show a border around the table.

```python
def set_alignment(self, alignment: str or list[str])
```
... to define alignment guide for each column. Alignement can be a single string defining alignment for all columns, or a list of strings specifying the alignment guide for each column. To align to the:
- left: either "<", "left" or "l"
- center: either "^", "center" or "c"
- right: either ">", "right" or "r"


```python
def set_center_separator(self, separator: str)
```
... to change the table lines intersection character.

```python
def set_column_separator(self, separator: str)
```
... to change the table vertical lines character.

### Display
```python
def render(self, file=sys.stdout)
```
... to render the table using previously specified content, header/footer and parameters. `file` parameter can be add to write the table to a file, or a different standard output.

### Reset
```python
def reset_header(self)
```
... to reset the header to an empty list.

```python
def reset_body(self)
```
... to reset the body to an empty list.

```python
def reset_footer(self)
```
... to reset the footer to an empty list.

```python
def reset_content(self)
```
... to reset header, body, and footer to an empty list.

### Example
Let's use the following content, that is in file `assets/example.csv`:
```csv
Date, Description, Amout
1/1/2014, Domain name, $10.98
1/1/2014, January Hosting, $54.95
1/4/2014, February Hosting, $51.00
1/4/2014, February Extra Bandwidth, $30.00
, Total, $146.93
```

Heres an example code to render this file:
```python
from pathlib import Path

from jdutable import TableWriter

table = TableWriter()

table.from_csv(Path("assets/example.csv"), header=True, footer=True)

table.set_uppercased(False)
table.set_border(True)
table.set_alignment(["left", "<", "r"])
table.set_center_separator("-")
table.set_column_separator("|")

table.render()
```

This shows the following result in the command line:
```console
---------------------------------------------------
! Date     ! Description               !    Amout !
---------------------------------------------------
! 1/1/2014 !  Domain name              !   $10.98 !
! 1/1/2014 !  January Hosting          !   $54.95 !
! 1/4/2014 !  February Hosting         !   $51.00 !
! 1/4/2014 !  February Extra Bandwidth !   $30.00 !
---------------------------------------------------
              Total                       $146.93
           ----------------------------------------
```

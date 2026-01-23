# MY_PACKAGE 
 
A Python package with Domain-Driven Design architecture. 
 
## Installation 
 
```bash 
pip install -e . 
``` 
 
## Usage 
 
```python 
from MY_PACKAGE import main 
main() 
``` 
 
## Project Structure 
 
```text 
MY_PACKAGE/ 
+¦¦ src/ 
-   L¦¦ MY_PACKAGE/ 
-       +¦¦ domain/          # Business logic 
-       +¦¦ application/     # Use cases 
-       L¦¦ interfaces/      # External interfaces 
+¦¦ tests/                   # Tests 
+¦¦ examples/                # Examples 
L¦¦ pyproject.toml          # Configuration 
``` 

# MY_PACKAGE

A Python package with Domain-Driven Design architecture.

## Installation

```bash
pip install -e .
```

## Usage

```python
from MY_PACKAGE.domain.value_objects.pilar_misto_circular import PilarCircularPreenchido

print(PilarCircularPreenchido)
```

## Project Structure

```text
MY_PACKAGE/
+-- src/
|   +-- MY_PACKAGE/
|       +-- domain/          # Business logic
|       +-- application/     # Use cases
|       +-- interfaces/      # External interfaces
+-- tests/                   # Tests
+-- examples/                # Examples
+-- pyproject.toml           # Configuration
```

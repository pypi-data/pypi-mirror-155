# DigiByte Scrypt (Python Bindings)

## Install

```bash
pip3 install digibyte_scrypt
```

## Usage

```python
import digibyte_scrypt

digibyte_scrypt.calcPoW(...)
```

## Changelog
`1.0.5`
- This version does not rely on `pypandoc` anymore as the new `setuptools` can handle markdown just well!
- Fixed a bunch of compilation issues

`1.0.0`
- Initial Development of scrypt (Integrated c module)

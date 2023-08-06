# ansiblevarchecker

[![codecov](https://codecov.io/gh/KlutzyBubbles/ansible-var-checker/branch/main/graph/badge.svg?token=NKQROPA7NT)](https://codecov.io/gh/KlutzyBubbles/ansible-var-checker)

CLI to check what vars are defined / used to find undefined or extra vars not documented.

Based on source for ansible 2.9 and striped down and modified version of jinja2schema.

## Known Issues

- Sub attributes of a dictionary are marked as defined if a different sub attribute is set e.g

```yaml
# Setting
dict:
  sub: yay

# Will cause the use of the following undefined var to be marked as defined
{{ dict.undefined }}
```

- Setting variables in jinja2 templates are seen as variable usage and will be marked as undefined if they have not been registered outside of the jinja2 template

- Because of the removed scalar typing (to fix issues with filter discovery and other edge cases), infer-ing assumes all if statements evaluate to a boolean which can fail when actually run. This is out of scope of what avc is meant to do and is expected behavior (aka, test your code before pushing)

- Python 3.6.x isn't tested and isn't 100% supported due to https://www.python.org/dev/peps/pep-0538/ being introduced min 3.7. 3.6 can still be configured to work with UTF-8 encoding but this package is not tested against 3.6

- Tests can fail with `ImportError: cannot import name 'soft_unicode' from 'markupsafe'`. To overcome this a downgraded version of markupsafe must be used `pip install MarkupSafe==2.0.1`

- On my local machine `python -m` needs to come before the `ansiblevarchecker` otherwise a `ImportError: cannot import name 'main' from 'ansiblevarchecker'` occurs

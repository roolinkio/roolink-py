# Contributing

This repository is a copy of a package that Roolink develops in a private
repository. Every commit here is exported from there, so nothing is pushed here
directly.

## Issues and pull requests

- Issues: open them here.
- Pull requests: welcome. Open one here as usual, and CI checks it. A
  maintainer imports it into the private repository, where it's reviewed and
  merged, and the next export brings the change back here. The pull request
  here is then closed.
- Dependency updates: these come from the private repository, so please
  don't open pull requests that only bump versions.

## Building and testing

Build and test it with Python's own tools:

```sh
pip install . pytest && pytest
```

## CI and releases

- [CI](.github/workflows/ci.yml) also tests the oldest Python that
  `pyproject.toml` allows, so code that needs a newer Python fails.
- PyPI trusts the [release workflow](.github/workflows/release.yml) by its file
  name, so renaming it stops releases.

# Replicated Means Data Provenance

The replicated experiment directories previously contained tracked absolute
symlinks named `data` pointing to:

```text
<repo-root>/autoresearch/data
```

Those symlinks were removed because they are machine-local and do not provide
portable repository content.

The canonical substrate is preserved at:

```text
autoresearch/
```

`autoresearch/prepare.py` owns CIFAR data download/loading behavior. Raw dataset
contents remain intentionally untracked and are ignored by `.gitignore`.


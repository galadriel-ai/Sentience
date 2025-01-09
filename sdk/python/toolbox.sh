function lint {
  pylint --rcfile=setup.cfg sentience/*
}

function format {
  black .
}

function type-check {
  mypy sentience
}

function unit-test {
  python -m pytest tests
}

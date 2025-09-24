# ChromaTerm

[![Build status](https://img.shields.io/github/workflow/status/hSaria/ChromaTerm/CI/main)](https://github.com/hSaria/ChromaTerm/actions?query=workflow%3ACI)
[![Coverage status](https://coveralls.io/repos/github/hSaria/ChromaTerm/badge.svg)](https://coveralls.io/github/hSaria/ChromaTerm)
[![Downloads](https://static.pepy.tech/personalized-badge/chromaterm?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=downloads)](https://pepy.tech/project/chromaterm)
[![Maintainability](https://img.shields.io/codeclimate/maintainability/hSaria/ChromaTerm)](https://codeclimate.com/github/hSaria/ChromaTerm)
[![PyPI version](https://badge.fury.io/py/chromaterm.svg)](https://badge.fury.io/py/chromaterm)

ChromaTerm (`ct`) is a Python script that colors your terminal's output using
regular expressions. It even works with interactive programs, like SSH.

![alt text](https://github.com/hSaria/ChromaTerm/raw/main/.github/junos-show-interface.png "Example output")

## Installation

```shell
# Recommended (isolated):
pipx install chromaterm

# Or with pip
pip install chromaterm

# Or using uv
uv tool install chromaterm
```

### From this fork (GitHub install)

If you want the version from this fork (`StewAlexander-com/ChromaTerm`), install directly from GitHub:

```shell
# pipx (recommended)
pipx install "git+https://github.com/StewAlexander-com/ChromaTerm.git@main#egg=chromaterm"

# pip
pip install "git+https://github.com/StewAlexander-com/ChromaTerm.git@main#egg=chromaterm"

# uv (as a tool)
uv tool install git+https://github.com/StewAlexander-com/ChromaTerm.git@main
```

### From source (clone this repo)

```shell
git clone https://github.com/StewAlexander-com/ChromaTerm.git
cd ChromaTerm

# Using pipx to install the local checkout
pipx install .

# Or create a virtual environment and install in editable mode
python -m venv .venv && . .venv/bin/activate
pip install -e .

# Run without installing (module mode)
python -m chromaterm --help
```

## Usage

Prefix your command with `ct`. It's that simple.

```shell
ct ssh somewhere
```

To run from a local clone without installing a console script, use:

```shell
python -m chromaterm ssh somewhere
```

You can also pipe data into `ct`, but some programs behave differently when piped,
like `less` would output the entire file.

```shell
echo "Jul 14 12:28:19  Message from 1.2.3.4: Completed successfully" | ct
```

### CLI reference

```text
ct [options] [program ...]
```

- `program ...`: When provided, `ct` spawns the program in a PTY and highlights its output while forwarding your input. When omitted, `ct` reads from stdin and writes highlighted output to stdout.

Options:

- `-b, --benchmark`: At exit, print rule usage statistics to stderr.
- `-c, --config FILE`: Override configuration file location (default resolution listed below).
- `-r, --reload`: Ask all running ChromaTerm instances to reload their configuration.
- `-R, --rgb`: Use truecolor output. By default `ct` auto-detects support and falls back to xterm-256.
- `--no-color`: Disable color output (equivalent to setting `NO_COLOR` or `CT_NO_COLOR=1`).
- `--force-color`: Force color output even if `NO_COLOR` is set.
- `--pcre`: Use PCRE2 instead of Python's `re` (visible only when PCRE2 is available on your system).
- `-v, --version`: Show version and exit.
- `-h, --help`: Show help message and exit.

Environment:

- `NO_COLOR` or `CT_NO_COLOR=1|true|yes|on`: Disable colors unless `--force-color` is used.

Exit status:

- When running a program, `ct` exits with the spawned program's status code.
- When reading from stdin, `ct` exits with status `0` on success.

### Persistence

To always highlight a program, set up an alias in your `.bash_profile`. For
instance, here's one for `ssh`.

```shell
alias ssh="ct ssh"
```

If you want to highlight your entire terminal, have ChromaTerm spawn your shell by
modifying the shell command in your terminal's settings to `/usr/local/bin/ct /bin/bash --login`.
Replace `/bin/bash` with your shell of choice.

### Color control

- To disable colors, pass `--no-color` or set the environment variable `NO_COLOR` (standard) or `CT_NO_COLOR=1`.
- To force colors even if `NO_COLOR` is set, pass `--force-color`.
- Truecolor is auto-detected and can be explicitly enabled with `--rgb`.

## Highlight Rules

ChromaTerm reads highlight rules from a YAML configuration file, formatted like so:

```yaml
rules:
- description: Obligatory "Hello, World"
  regex: Hello,?\s+World
  color: f#ff0000

- description: Spit some facts (emphasize "NOT" so they get it)
  regex: Pineapple does (NOT) belong on pizza
  color:
    0: bold
    1: blink italic underline
```

The configuration file can be placed in one of the locations below. The first one
found is used.

 * `$HOME/.chromaterm.yml`
 * `$XDG_CONFIG_HOME/chromaterm/chromaterm.yml` (`$XDG_CONFIG_HOME` defaults to
 `$HOME/.config`)
 * `/etc/chromaterm/chromaterm.yml`

If no file is found, a default one is created in your home directory.

> Check out [`contrib/rules`](https://github.com/hSaria/ChromaTerm/tree/main/contrib/rules);
> it has some topic-specific rules that are not included in the defaults.

### Description

Optional. It's purely for your sake.

### RegEx

The RegEx engine used is Python's [re](https://docs.python.org/3/library/re.html),
but it can be switched to PCRE2 (see relevant section below).

### Color

#### Background and Foreground

The color is a hex string prefixed by `b` for background (e.g. `b#123456`) and
`f` for foreground (e.g. `f#abcdef`).

#### Style

In addition to the background and foreground, you can also use `blink`, `bold`,
`invert`, `italic`, `strike`, and `underline`. Though, not all terminals support
those styles; you might not see their effects.

### Group

Colors can be applied per RegEx group (see the 2nd example rule). Any group in
the RegEx can be referenced, including group `0` (entire match) and
[named groups](https://docs.python.org/3/howto/regex.html#non-capturing-and-named-groups).

### Exclusive

When multiple rules match the same text, ChromaTerm highlights the text with all
of the colors of the matching rules. If you want the text to be highlighted only
by the first rule that matches it, use the `exclusive` flag.

```yaml
- regex: hello
  color: bold
  exclusive: true
```

In the code above, no other rule will highlight `hello`, unless it comes first
and has the `exclusive` flag set.

## Palette

You can define colors in a palette and reference them by name. For instance:

```yaml
palette:
  # Created from https://coolors.co/9140f5-bd5df6-e879f6
  purple-1: '#9140f5'
  purple-2: '#bd5df6'
  purple-3: '#e879f6'

rules:
- regex: hello
  color: f.purple-1

- regex: hi
  color: b.purple-3
```

When referencing a palette color, prefix it with `b.` for background and `f.` for
foreground.

## PCRE2

If the `PCRE2` library is present, you can use it instead of Python's `re`
engine. When present, an option in `ct -h` becomes available.

While the performance improvement is significant (~2x), the two RegEx engines
have a few differences; use this option only if you have a good understanding
of their unique features.

> The default rules work on both engines.

## Help

If you've got any questions or suggestions, please open up an
[issue](https://github.com/hSaria/ChromaTerm/issues/new/choose) (always
appreciated).

### Windows support

To use ChromaTerm on Windows, you will need to run it with the
[Windows Subsystem for Linux (`WSL`)](https://docs.microsoft.com/en-us/windows/wsl/about)

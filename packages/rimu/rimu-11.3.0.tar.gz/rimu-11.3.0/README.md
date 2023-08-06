A port of the [Rimu Markup language](https://srackham.github.io/rimu/) written
in the Python language.


## Features
Functionally identical to the [TypeScript
implementation](https://github.com/srackham/rimu) version 11.3.0.


## Usage
Install from [PyPI](https://pypi.org/project/rimu/) using the Python `pip` command:

    pip install rimu

Example usage:

``` python
import rimu

print(rimu.render('*Hello World*!'))
```

See also Rimu
[API documentation](https://srackham.github.io/rimu/reference.html#api).


## CLI command
The [Rimu CLI
command](https://srackham.github.io/rimu/reference.html#rimuc-command) installed
by Pip is named `rimupy`. CLI command example:

``` sh
echo 'Hello *Rimu*!' | rimupy
```

This will output:

``` html
<p>Hello <em>Rimu</em>!</p>
```


## Building
As of version 11.3.0 rimu-py is developed in a Docker container environment
using VSCode and the _Remote Containers_ extension.

1. Install the source repo from Github:

        git clone https://github.com/srackham/rimu-py.git

2. Build a development container image:

        cd rimu-py/
        docker build --tag rimu-py .

3. Create a container and run the bash shell:

        docker run -it rimu-py bash

4. Run tests and build rimu-py from the container bash prompt:

        make build


## Learn more
Read the [documentation](https://srackham.github.io/rimu/reference.html) and experiment
with Rimu in the [Rimu
Playground](http://srackham.github.io/rimu/rimuplayground.html).


## Implementation
- The largely one-to-one correspondence between the canonical
  [TypeScript code](https://github.com/srackham/rimu) and the Python code
  eased porting and debugging.  This will also make it easier to
  cross-port new features and bug-fixes.

- All Rimu implementations share the same JSON driven test suites
  comprising over 300 compatibility checks.
# Pumuckl
[![Build Status](https://travis-ci.org/Mayflower/pumuckl.svg?branch=master)](https://travis-ci.org/Mayflower/pumuckl)

**pumuckl** (Puppet Module Version Checker) is a simple script to check a Puppetfile if there are newer module versions on the forge.

## Requirements
 * Python >=3.3
 * pip(3)

## Installation
To install system-wide run:
```
sudo pip3 install .
```
Alternatively you may create a virtualenv and install it there.

## Usage
 * Either run `pumuckl` in a folder containing a `Puppetfile`.
 * Run `pumuckl path/to/Puppetfile`

## Contributing
 * If you find a bug or wish to have a new feature simply open an issue.
 * Otherwise if you are really motivated pull requests are always welcome, too.

## Credits
Created by [Robin Gloster](https://github.com/globin)

Named by [Tristan Helmich](https://github.com/fadenb)

## License
GPLv3, see [LICENSE](LICENSE) for details.

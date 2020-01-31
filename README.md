# Pointa! Project

![Pointa!](./Pointa_Scaled.png)

|   [Chinese](docs/README_ZH.md)    |

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [Contributing](#contributing)
- [License](#license)

## Background
"Pointa!" is a board game which is simple to learn & enjoy. Meanwhile you can also play the game with pen and paper, this repository is meant to implement the game in python.


### About Game Instruction ...
We suggest you that having at least a glancing is benefit for no matter playing or developing the game. It not only helps you to get familiar with the " Proper noun " we used in games, but also, is fun.

**Game Instructions**
- [English](docs/GameInstruction.md)
- [Chinese](docs/GameInstruction_ZH.md)

## Install

Get the latest version from this repository with(or better download [the latest release](https://github.com/KRedCell/Pointa/releases)):
```sh
$ git clone https://github.com/KRedCell/Pointa.git
```
Then
```sh
$ python setup.py install
```

## Usage

After the installation, you can use both client and dedicated server

As `Client`
```sh
$ python -m Pointa.Client -l [languageCode]
```
[Supported Language Codes](docs/SupportedLanguages.md)

As `Server`
```sh
$ python -m Pointa.Server -p
```
Start a `development` server by removing `-p`


## API
[API Refrences (to be done)](docs/Pointa_Web_API_Refrences.md)

## Contributing
Feel free! Sending PRs or [Open an issue](https://github.com/KRedCell/Pointa/issues/new) if you want!

The project follows the [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) Code of Conduct.

## License

[MIT © Red_Cell](./LICENSE)

**Special Thanks to [Standard Readme](https://github.com/RichardLitt/standard-readme)**
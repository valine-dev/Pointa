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


> ### About Game Instruction ...
> We suggest you that having at least a glancing is benefit for no matter playing or developing the game. It not only helps you to get familiar with the " Proper noun " we used in games, but also, is fun.

**Game Instructions**
- [English](docs/GameInstruction.md)
- [Chinese](docs/GameInstruction_ZH.md)

## Install

The project is based on `Python`, so make sure your python version is above `3.7`. 

Get the latest version from this repository with(or better download [the latest release](https://github.com/KRedCell/Pointa/releases)):
```sh
$ git clone https://github.com/KRedCell/Pointa.git
```
Then
```sh
$ python setup.py install
```

> ### Some of the known issues ...
> To host a server, we strongly suggest you that use the python whose version is above `3.6`, use `3.7` for the best. There are already some issues about `asyncio` had been discovered but the reason is still unknown. If you discover more issues like this, open a new issue please.

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

> ### About server configuring ...
> `flask` is what we used to build server, so most of the configurable options are the options available in original flask, go to `./Pointa/Server/configs/Config.py` to configure the server.

## API
[API Refrences (to be done)](docs/Pointa_Web_API_Refrences.md)

## Contributing
Feel free! Sending PRs or [Open an issue](https://github.com/KRedCell/Pointa/issues/new) if you want!

The project follows the [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) Code of Conduct.

## License

[MIT © Red_Cell](./LICENSE)

**Special Thanks to [Standard Readme](https://github.com/RichardLitt/standard-readme)**
# Pointa! Project

![Pointa!](./Pointa_Scaled.png)

## 目录

- [背景](#背景)
- [安装](#安装)
- [使用](#使用)
- [API](#api)
- [贡献](#贡献)
- [协议](#协议)

## 背景
"Pointa!" 是一个简单易懂的桌游（实际上你甚至可以用纸和笔来玩），这个repo是Pointa游戏机制在python里的一个实现。


### 关于游戏规则书 ...
我们建议你在游玩、参与开发之前，至少先浏览一遍游戏规则书，这不仅能让你理解游戏中许多专有名词的含义，还因为Pointa本身确实是有趣的。

**游戏规则书**
- [English](./GameInstruction.md)
- [中文](./GameInstruction_ZH.md)

## 安装

从该库中拉取最新版本（或者下载最新的[Release](https://github.com/KRedCell/Pointa/releases)）
```sh
$ git clone https://github.com/KRedCell/Pointa.git
```
接着安装
```sh
$ python setup.py install
```

## 使用

安装后，你可以使用Pointa的专用服务器或命令行客户端

如果是作为 `客户端`
```sh
$ python -m Pointa.Client -l [语言代码]
```
[支持的语言](./SupportedLanguages.md)

作为 `服务器`
```sh
$ python -m Pointa.Server -p
```
删除`-p`开启`开发`服务器 


## API
[API Refrences (未完成)](./Pointa_Web_API_Refrences.md)

## 贡献
无需感到拘束！发送PR或者[开个issue](https://github.com/KRedCell/Pointa/issues/new) 都可以！

另：本项目遵从 [贡献者公约](http://contributor-covenant.org/version/1/3/0/)的行为准则。

## 协议

[MIT © Red_Cell](../LICENSE)

**Special Thanks to [Standard Readme](https://github.com/RichardLitt/standard-readme)**
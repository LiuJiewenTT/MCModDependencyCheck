# 用户手册

**产品: MCMDC(Minecraft Mod Dependency Check)**

您好！感谢您使用我们的产品！<br/>
在本手册中，我们将会向您介绍有关本产品的相关信息。
（我们提供[更多语言版本](#语言选择区)）

![logo](../doc-res/MCMDC-2-GIF2.gif)

## 简介

我们为您提供此工具，适用于不启动游戏即完成模组相关依赖的检查的情景。这是相当有用的，因为启动游戏来完成依赖的检查是相当浪费时间的：所有信息其实都储存在了相应的模组当中，只需简单地读取便可以得知是否满足要求。因而我们设计了此产品，一次快速的运行即可得知结果。祝您游戏愉快！

此产品目前仅提供*缺失检查*，而期待中的*版本检查*已经在路上了，敬请期待！即便如此，这个初始发布版本也应该可以胜任大部分的情景。==有了它，您可以随意集结想要的模组而无需寻找其前置模组，只需一个检查即可发现相关前置模组==。如果您有兴趣加入我们、一起构建它，欢迎访问它的项目库(on *Github.com*)！

项目名称: *MCModDependencyCheck*<br/>
许可证: *GPL-3.0*<br/>
项目链接: *<https://github.com/LiuJiewenTT/MCModDependencyCheck>*<br/>
联系邮箱: *<liuljwtt@163.com>*

## 命令行选项

此处列出程序支持的选项:

1. `-dir [路径]`: 选择要检查的目录（接在后面）。如果程序只被传入一个额外参数，则它会被当做缺省此选项。（注意：某测试目录在无传入参数时会被启用。）
2. `-toIgnore [True/False]`: 此选项设置是否启用忽略功能。如果启用，指定列表中的模组会被默认为“准备好的”。此选项默认值为 `True`。 此选项数值对大小写不敏感。例如： `-toIgnore False` 或 `-toIgnore false`都是可以的。
3. `-IgnoreList "['some modId 1', 'some modId 2', ...]"`: 此选项配置哪些`modId`将被忽略。此选项默认值为：`['forge', 'minecraft']`。如果`-toIgnore` 被设置为`False`，此选项将不生效。 样例：`-IgnoreList "['create', 'minecraft']"`。
4. `-forceMandatory`: 为所有模组的*Mandatory*设置全局数值为`True`。 此选项将会参与相关判断，该判断将使用“或”操作。这意味着如果启用此选项，所有模组的`Mandatory`属性将会被认为是`True`值并进行后续检查。
5. `-license`: 展示产品的许可证内容。
6. `-onlyAbout`: 仅显示“关于”信息并退出。
7. `--version`: 仅告知版本并退出。
8. `-GiveDoc [某文档的路径]`: 打开产品携带的某个文档。此选项后接文档路径，默认值为："Manual"。
9. `-DocLang [语言代码]`: 选择文档的语言。此版本已预设一些语言，包括："en-us"（默认）和"zh-cn"。
10. `-GiveDoc_PauseExit`: 程序在给出文档后，将会暂停并等待键入，随后推出后。此高级选项应与`-GiveDoc`或`-ChooseDoc`一同使用。
11. `-GiveDoc_SleepExit [秒数]`: 程序在给出文档后，将会暂停一段时间，随后退出。`-GiveDoc_PauseExit`拥有比此选项更高的优先级。此高级选项应与`-GiveDoc`或`-ChooseDoc`一同使用。
12. `-ChooseDoc`: 手动选择和打开文档。

以下为调试相关选项:

1. `-enableGlobalDebug`
2. `-enableDebug`
3. `--devpause`

## 语言选择区

- [x] [en-us](../en-us/Manual.md)
- [x] [zh-cn]
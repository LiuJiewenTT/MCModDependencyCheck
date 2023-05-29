# Manual(English)

**Product: MCMDC(Minecraft Mod Dependency Check)**

Welcome! Thanks for choosing our product! In this manual, we will introduce all the things with *MCMDC(Minecraft Mod Dependency Check)* to you.
(More language versions are [provided](#Language Selection Section).)

![logo](../doc-res/MCMDC-2-GIF2.gif)

## Brief Introduction

We are offering you a tool that can verify whether all your mods or modpacks are ready to launch without starting a game. This means you will have a quick method to test the readiness and improve your working efficiency. And that is why we made this product for you. Wishing you have a good time!

The product is now able to check `modId`s and in the future `version`s based on datapack of the product as well. However, this initial release should be compatible for most scenarios you might encounter. If you are interested in the codes and wants to contribute on the project, please view the site on *Github.com*.

Project Name: *MCModDependencyCheck*<br/>
License: *GPL-3.0*<br/>
Project Link: *<https://github.com/LiuJiewenTT/MCModDependencyCheck>*<br/>
Email: *<liuljwtt@163.com>*

## Command Prompt Options

Here list out the options that supported:

1. `-dir [path]`: Select the directory to check. If there is only one argument except program itself, this switch can be left out as the argument will be suspected as a directory by default.
2. `-toIgnore [True/False]`: This indicates whether to ignore some *modId*s in the check and assume they are good. This is set to `True` by default. This option's value is not case-sensitive. E.g. `-toIgnore False` or `-toIgnore false`.
3. `-IgnoreList "['some modId 1', 'some modId 2', ...]"`: This option indicates what *modId*s to ignore in the check. This is set to `['forge', 'minecraft']` by default. If `-toIgnore` is set to `False`, this option will have no effect on the result. E.g. `-IgnoreList "['create', 'minecraft']"`.
4. `-forceMandatory`: Set global value of *Mandatory* for mods. The global value will be manufactured with every mods' corresponding value by an *OR* operation. That means if you starts it with this option, all mods will be considered to have `True` value on property `Mandatory` and thus check all of them. 
5. `-license`: This option will show you the license of the program.
6. `-onlyAbout`: This option will only print out the *About* information and exit.
7. `--version`: tell the version of program and exit.
8. `-GiveDoc [some doc path]`: To open some specific document provided along with the program. This option comes with a tailing doc path whose default value is "Manual".
9. `-DocLang [language code]`: To select the language of document. There are only a few presets allowed which includes "en-us"(by default) and "zh-cn".
10. `-GiveDoc_PauseExit`: The program would be paused before exit after it delivers the document. This is an advanced option when using with `-GiveDoc` and `-ChooseDoc`.
11. `-GiveDoc_SleepExit [seconds]`: The program would be paused for a period of time before exit after it delivers the document. `-GiveDoc_PauseExit` has higher priority than this option. This is an advanced option when using with `-GiveDoc` and `-ChooseDoc`.
12. `-ChooseDoc`: Choose what and how to open.

There is some options prepared for debugging:

1. `-enableGlobalDebug`
2. `-enableDebug`
3. `--devpause`

## Language Selection Section

- [x] [en-us]
- [x] [zh-cn](../zh-cn/Manual.md)


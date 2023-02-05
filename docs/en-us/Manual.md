# Manual(English)

**Product: MCMDC(Minecraft Mod Dependency Check)**

Welcome! Thanks for choosing our product! In this manual, we will introduce all the things with *MCMDC(Minecraft Mod Dependency Check)* to you.

![logo]()

## Brief Introduction

We are offering you a tool that can verify whether all your mods or modpacks are ready to launch without starting a game. This means you will have a quick method to test the readiness and improve your working efficiency. And that is why we made this product for you. Wishing you have a good time!

The product is now able to check `modId`s and in the future `version`s based on datapack of the product as well. However, this initial release should be compatible for most uses of yours. If you are interested in the codes and wants to contribute on the project, please view the site on *Github.com*.

Project Name: *MCModDependencyCheck*
License: *GPL-3.0*
Project Link: *<https://github.com/LiuJiewenTT/MCModDependencyCheck>*

## Command Prompt Options

Here list out the options that supported:

1. `-dir`: Select the directory to check. If there is only one argument except program itself, this switch can be left out as the argument is suspected as an directory by default.
2. `-toIgnore [True/False]`: This indicates whether to ignore some *modId*s in the check and assume they are good. This is set to `True` by default. This option's value is not case-sensitive. E.g. `-toIgnore False` or `-toIgnore false`.
3. `-IgnoreList "['some modId 1', 'some modId 2', ...]"`: This option indicates what *modId*s to ignore in the check. This is set to `['forge', 'minecraft']` by default. If `-toIgnore` is set to `False`, this option will have not effect on the result. E.g. `-IgnoreList "['create', 'minecraft']"`.
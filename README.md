# MCModDependencyCheck
Check if all dependencies are good to go before launching a game. (for forge)

![cover](./res/MCMDC-2-GIF2.gif)

## License

1. All the things under `./res/` have their own license. If not provided, they are reserved and you cannot use them or redistribute them without permission.
2. The program has its own License and the release versions will include that thing.

## Working Progress

See `working.md`.

<strong style="color:red">Asking for an icon design! Asking for donation with love!</strong>

**<mark>Will anybody help me design an icon?</mark>** **pls!**

## Words to say

2023-1-24:

Some mods are unbearable on version indications. They use `version="${file.jarVersion}"` sentence and the version is not simple format as we thought. Instead, the version string is consist of something else.

If some one can't wait and want to continue the project, here is a piece of advise for you:

1. For further processing of terrible versions, you may use class `Mod` and move `modinfo` and `dependenciesinfo` insides.
2. Or you might ignore the case and let user judge. In this solution, you may let the program remember user's judgement. This solution costs much lesser than the above.

Good luck!

2023-2-3:

I will go on my work.

2023-2-4:

I have prepared version-comparing method. The next work is to do with `modId` and then is to do with `versionRange`.

2023-2-5:

I make the first complete version. Only id check.
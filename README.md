# MCModDependencyCheck
Check if all dependencies are good to go before launching a game. (for forge)

## Working Progress

See `working.md`.

## Words to say

2023-1-24:

Some mods are unbearable on version indications. They use `version="${file.jarVersion}"` sentence and the version is not simple format as we thought. Instead, the version string is consist of something else.

If some one can't wait and want to continue the project, here is a piece of advise for you:

1. For further processing of terrible versions, you may use class `Mod` and move `modinfo` and `dependenciesinfo` insides.
2. Or you might ignore the case and let user judge. In this solution, you may let the program remember user's judgement. This solution costs much lesser than the above.

Good luck!

2023-2-3:

I will go on my work.


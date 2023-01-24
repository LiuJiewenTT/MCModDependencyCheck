# MCModDependencyCheck
Check if all dependencies are good to go before launching a game. (for forge)

## Working Progress

See `working.md`.

## Words to say

Some mods are unbearable on version indications. They use `version="${file.jarVersion}"` sentence and it confused me how to compare between versions. I don't know if they never want some else develop a mod based on theirs. It's a catastrophe!

Even I may ignore this or design more codes and structures, this awful case makes me very very uncomfortable. The workload will increase a big amount. OMG. I'm gonna rest for a while now.

If some one can't wait and want to continue the project, here is a piece of advise for you:

1. For further processing of terrible versions, you may use class `Mod` and move `modinfo` and `dependenciesinfo` insides.
2. Or you might ignore the case and let user judge. In this solution, you may let the program remember user's judgement. This solution costs much lesser than the above.

Good luck!
# Knowledge-Base-Agent
This is an implementation of a knowledge base  agent that takes in English sentences as input, extracts meaning/truth conditions from those sentences, and can answer questions based on its built up knowledge.
----
How it works:

This program uses the Cocke–Younger–Kasami algorithm (CYK) parsing algorithm (https://en.wikipedia.org/wiki/CYK_algorithm) to get phrase structures in input English sentences. The program uses this information to extract meaning, which is represented by sets that correspond to properties; in particular, for each property, there is a corresponding set made of the entities with that property (for instance, if given the input sentence "john runs", 'run' will map to a set containing 'john'--this is doen using dictionaries. It is also able to handle "If ..., then ..." sentences by maintaining a dictionary whose keys are antecedents that map to consequents that is checked whenever a new input sentence is entered.

For now, the program has a limited vocabulary and syntax (for instance, it cannot currently answer "wh-" questions where the "wh-" word is the object of the sentence, such as "Who does John like?"). I plan to expand the program's vocabulary with online resources, and I will add more rules to the grammar. I also hope to implement more sophisticated ways to deal with pronouns and references in general (for example, right now, the program just assumes "he" refers to the most recent male name used in an input sentence). I also plan to have the program be able to scan files rather than merely take in user input from the console.

------
While I originally presented a dumbed down version of this program to my computational linguistics class (one that basically only had the CYK parsing algorithm and the property-set dictionary), this is an ongoing personal project that I have expanded on quite a bit since then and will be periodically updating, as I've enjoyed working on this.

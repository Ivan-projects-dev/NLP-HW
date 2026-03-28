class FST:
    def __init__(self):
        self.rules = []

    def add_rule(self, name, category, func):
        self.rules.append((name, category, func))

    def apply(self, word, category):
        results = []
        for name, rule_category, rule in self.rules:
            if rule_category == category:
                res = rule(word)
                if res and res != word:
                    results.append((name, res))
        return results

fst = FST()

# Noun rules
def noun_a_to_y(word):
    if word.endswith("а"):
        return word[:-1] + "и"

def noun_o_to_a(word):
    if word.endswith("о"):
        return word[:-1] + "а"

def noun_ets_to_tsi(word):
    if word.endswith("ець"):
        return word[:-3] + "ці"

def noun_i_to_o_and_add_i(word):
    if word.endswith("і"):
        return word[:-1] + "о" + "и"

def noun_i_to_a(word):
    if word.endswith("і"):
        return word[:-1] + "а"

# Adjective rules
def adj_masc_to_fem(word):
    if word.endswith("ий"):
        return word[:-2] + "а"

def adj_fem_to_neut(word):
    if word.endswith("а"):
        return word[:-1] + "е"

# Verb rules
def verb_masc(word):
    if word.endswith("ти"):
        return word[:-2] + "в"

def verb_fem(word):
    if word.endswith("ти"):
        return word[:-2] + "ла"

def verb_removal(word):
    if word.endswith("ти"):
        return word[:-2]

# Add rules to FST
fst.add_rule("N1: а->и", "noun", noun_a_to_y)
fst.add_rule("N2: о->а", "noun", noun_o_to_a)
fst.add_rule("N3: ець->ці", "noun", noun_ets_to_tsi)
fst.add_rule("N4: i->о+и", "noun", noun_i_to_o_and_add_i)
fst.add_rule("N5: i->а", "noun", noun_i_to_a)
fst.add_rule("A1: masc->fem", "adj", adj_masc_to_fem)
fst.add_rule("A2: fem->neut", "adj", adj_fem_to_neut)
fst.add_rule("V1: past masc", "verb", verb_masc)
fst.add_rule("V2: past fem", "verb", verb_fem)
fst.add_rule("V3: infinitive->root", "verb", verb_removal)

def load_words(filename):
    words = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            word, category = line.strip().split()
            words.append((word, category))
    return words

# Example words and categories
words = load_words("Lexicon.txt")

# Apply FST to each word
for word, category in words:
    print(f"{word} ({category}):")
    results = fst.apply(word, category)
    if results:
        for rule, res in results:
            print(f"  {rule} -> {res}")
    else:
        print("  No transformation rules matched.")
    print()
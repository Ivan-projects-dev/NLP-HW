import os

class FST:
    def __init__(self, lexicon_path):
        self.lexicon = {}
        self.generate_map = {}
        self.analyze_map = {}
        self.rules = {
            "substitution": [],
            "insertion": [],
            "removal": []
        }
        self.states = ["q0", "qStem", "qPlural", "qf"]
        self.start_state = "q0"
        self.final_states = ["qf"]
        self.transitions = []
        self.load_lexicon(lexicon_path)

    def load_lexicon(self, path):
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                word, group = line.split()
                self.lexicon[word] = group

    def add_rule(self, rule_type, description):
        self.rules[rule_type].append(description)

    def add_transition(self, from_state, input_symbol, to_state, output_symbol):
        self.transitions.append({
            "from": from_state,
            "input": input_symbol,
            "to": to_state,
            "output": output_symbol
        })

    def generate(self, lexical_form):
        if "+N+PL" not in lexical_form:
            return "UNKNOWN"
        stem = lexical_form.replace("+N+PL", "")
        if stem not in self.lexicon:
            return "UNKNOWN"

        group = self.lexicon[stem]
        if group == "N1":
            base = stem[:-1]
            surface = base + "и"
        elif group == "N2":
            base = stem[:-1]
            surface = base + "а"
        elif group == "N3":
            base = stem[:-3]
            surface = base + "ці"
        else:
            return "UNKNOWN"

        self.generate_map[lexical_form] = surface
        self.analyze_map[surface] = lexical_form
        return surface

    def analyze(self, surface_form):
        if surface_form in self.analyze_map:
            return self.analyze_map[surface_form]

        if surface_form.endswith("и"):
            lexical = surface_form[:-1] + "а"
            if lexical in self.lexicon:
                if self.lexicon[lexical] == "N1":
                    result = lexical + "+N+PL"
                    self.analyze_map[surface_form] = result
                    return result

        if surface_form.endswith("а"):
            lexical = surface_form[:-1] + "о"
            if lexical in self.lexicon:
                if self.lexicon[lexical] == "N2":
                    result = lexical + "+N+PL"
                    self.analyze_map[surface_form] = result
                    return result

        if surface_form.endswith("ці"):
            lexical = surface_form[:-2] + "ець"
            if lexical in self.lexicon:
                if self.lexicon[lexical] == "N3":
                    result = lexical + "+N+PL"
                    self.analyze_map[surface_form] = result
                    return result

        return "UNKNOWN"

    def print_rules(self):
        print("\n========== RULES ==========")
        for rule_type, rules in self.rules.items():
            print(f"\n{rule_type.upper()} RULES:")
            for r in rules:
                print(" -", r)

    def print_transitions(self):
        print("\n========== TRANSITIONS ==========")
        for t in self.transitions:
            print(f"{t['from']} -- " f"{t['input']}:{t['output']} --> " f"{t['to']}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEXICON_PATH = os.path.join(BASE_DIR, "lexicon.txt")
fst = FST(LEXICON_PATH)
fst.add_rule("substitution", "а -> и in N1 plural formation")
fst.add_rule("substitution", "о -> а in N2 plural formation")
fst.add_rule("substitution", "ець -> ці in N3 plural formation")
fst.add_rule("insertion", "Insert і in N3 plural forms")
fst.add_rule("removal", "Remove final suffix before plural formation")
fst.add_transition("q0", "stem", "qStem", "stem")
fst.add_transition("qStem", "+N+PL", "qPlural", "plural_rule")
fst.add_transition("qPlural", "surface", "qf", "wordform")
print("========== GENERATION ==========\n")
for word in fst.lexicon:
    lexical = word + "+N+PL"
    surface = fst.generate(lexical)
    print(f"{lexical} -> {surface}")

print("\n========== ANALYSIS ==========\n")
for lexical, surface in fst.generate_map.items():
    print(f"{surface} -> {fst.analyze(surface)}")

fst.print_rules()
fst.print_transitions()
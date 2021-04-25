from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(And(AKnight,Not(AKnave)),And(Not(AKnight),AKnave)),
    Implication(And(AKnight,AKnave),AKnight),       
    Implication(Not(And(AKnight,AKnave)),AKnave)   
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(And(AKnight,Not(AKnave)),And(Not(AKnight),AKnave)),
    Or(And(BKnight,Not(BKnave)),And(Not(BKnight),BKnave)),
    Implication(And(AKnave,BKnave),AKnight),    
    Implication(Not(And(AKnave,BKnave)),AKnave) 
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(And(AKnight,Not(AKnave)),And(Not(AKnight),AKnave)),
    Or(And(BKnight,Not(BKnave)),And(Not(BKnight),BKnave)),
    Implication(Or(And(AKnight,BKnight),And(AKnave,BKnave)),AKnight),    
    Implication(Not(Or(And(AKnight,BKnight),And(AKnave,BKnave))),AKnave), 
    Implication(Or(And(AKnight,BKnave),And(AKnave,BKnight)),BKnight),    
    Implication(Not(Or(And(AKnight,BKnave),And(AKnave,BKnight))),BKnave) 
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(And(AKnight,Not(AKnave)),And(Not(AKnight),AKnave)),
    Or(And(BKnight,Not(BKnave)),And(Not(BKnight),BKnave)),
    Or(And(CKnight,Not(CKnave)),And(Not(CKnight),CKnave)),
    Implication(Or(AKnight,AKnave),AKnight),    
    Implication(Not(Or(AKnight,AKnave)),AKnave), 
    Implication(And(And(Implication(AKnave,AKnight),Implication(AKnight,AKnave)),CKnave),BKnight),    
    Implication(Not(And(And(Implication(AKnave,AKnight),Implication(AKnight,AKnave)),CKnave)),BKnave), 
    Implication(AKnight,CKnight),    
    Implication(Not(AKnight),CKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

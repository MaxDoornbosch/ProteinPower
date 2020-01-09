from code.classes import fold, placement, protein

if __name__ == "__main__":
    while True:
         protein = str(input("please enter your protein: "))
         # print(protein)
         fold = Fold()
         if fold.get_protein(protein) == True:
             # print(case.get_protein(protein))
             # print("error")
         placement = Placement(protein, fold.final_path)
         if placement == True:
             print("goed")

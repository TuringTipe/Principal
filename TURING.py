class Ruban:
    def __init__(self, values):
        self.values = values
        self.minIndex = 0
        self.maxIndex = len(values) - 1
        self.zeroIndex = 0

    def __getitem__(self, index):
        if index < self.minIndex:
            for k in range(self.minIndex - index):
                self.values.insert(0, " ")
            self.zeroIndex += (self.minIndex - index)
            self.minIndex = index
            return " "
        elif index > self.maxIndex:
            for k in range(index - self.maxIndex):
                self.values.append(" ")
            self.maxIndex = index
            return " " 
        else:
            return self.values[self.zeroIndex + index]

    def __setitem__(self, index, value):
        if index < self.minIndex:
            for k in range(self.minIndex - index):
                self.values.insert(0, " ")
            self.zeroIndex += (self.minIndex - index)
            self.minIndex = index
        elif index > self.maxIndex:
            for k in range(index - self.maxIndex):
                self.values.append(" ")
            self.maxIndex = index 
        self.values[self.zeroIndex + index] = value
        
class Machine:    
    def __init__(self, ruban, transitions, initState, initIndex):
        self.ruban = ruban
        self.transitions = transitions
        self.currentState = initState
        self.index = initIndex

    def oneStep(self):
        print("Current state : ( " + str(currentState) + " , " + str(self.ruban[self.index]) + " )")
        
        try:
            temp = self.transitions[(self.currentState, self.ruban[self.index])]
        except KeyError as ke:
            print("Transition for current state undefined, stopping.")
            return False

        nextState = temp[0]
        deplacement = temp[1]
        ecriture = temp[2]

        self.ruban[self.index] = ecriture
        self.index += deplacement
        self.currentState = nextState
                
        print("Transition : ( " + str(nextState) + " , " + str(deplacement) + " , " + str(ecriture) + " )")

        return True

    def allSteps(self):
        while oneStep():
            pass

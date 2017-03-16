import pickle

def pack(obj, fileName):
    f = open(fileName, 'wb')
    pickle.dump(obj, f)
    f.close()

def unpack(fileName):
    f = open(fileName, 'rb')
    temp = pickle.load(f)
    f.close()
    return temp

class Alphabet:
    def __init__(self, lettres, epsilon):
        self.lettres = lettres
        self.epsilon = epsilon

class Ruban:
    def __init__(self, values, alphabet):
        self.values = values
        self.minIndex = 0
        self.maxIndex = len(values) - 1
        self.zeroIndex = 0
        self.alphabet = alphabet

    def __getitem__(self, index):
        if index < self.minIndex:
            for k in range(self.minIndex - index):
                self.values.insert(0, self.alphabet.epsilon)
            self.zeroIndex += (self.minIndex - index)
            self.minIndex = index
            return self.alphabet.epsilon
        elif index > self.maxIndex:
            for k in range(index - self.maxIndex):
                self.values.append(self.alphabet.epsilon)
            self.maxIndex = index
            return self.alphabet.epsilon
        else:
            return self.values[self.zeroIndex + index]

    def __setitem__(self, index, value):
        if index < self.minIndex:
            for k in range(self.minIndex - index):
                self.values.insert(0, self.alphabet.epsilon)
            self.zeroIndex += (self.minIndex - index)
            self.minIndex = index
        elif index > self.maxIndex:
            for k in range(index - self.maxIndex):
                self.values.append(self.alphabet.epsilon)
            self.maxIndex = index 
        self.values[self.zeroIndex + index] = value

    def __repr__(self):
        return self.values.__repr__()
        
class Machine:    
    def __init__(self, ruban, transitions):
        self.ruban = ruban
        self.transitions = transitions
        self.currentState = 0
        self.index = 0

    def oneStep(self):
        print("Current state : ( " + str(self.currentState) + " , " + str(self.ruban[self.index]) + " )")
        
        try:
            temp = self.transitions[(self.currentState, self.ruban[self.index])]
        except KeyError as ke:
            print("Transition for " + str(self.ruban[self.index]) + " in state " + str(self.currentState) + " not defined, stopping.")
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
        while self.oneStep():
            pass
        self.currentState = 0

import pickle
import tkinter

def pack(obj, fileName):
    f = open(fileName, 'wb')
    pickle.dump(obj, f)
    f.close()

def unpack(fileName):
    f = open(fileName, 'rb')
    temp = pickle.load(f)
    f.close()
    return temp

def complement(tab):
    a = []
    for i in tab:
        a.append(1 - i)
    return a

def plussun(tab):
    for k in range(len(tab)):
        if tab[k] == 1:
            tab[k] = 0
        elif tab[k] == 0:
            r = 0
            tab[k] = 1
            return

def binToNint(tab, n = -1):
	nint = 0
	if n == -1:
		n = len(tab)
	for a in range(min(n, len(tab))): 
		nint += tab[a] * (2 ** a)
	return nint

def binToZint(tab, n = -1):
	h = 1
	if n == -1:
		n = len(tab)
	else:
		n -= 1 #Ca c est tres moche, mais ca marche. dont ask
	if tab[:n + 1][- 1] == 1:
		t = complement(tab[:n + 1])
		plussun(t)
		h = -1
	else:
		t = tab[:n + 1]
	if n != len(tab):
		n += 1 #Ca aussi
	return h * binToNint(t, n = n)

def nintToBin(nint, n = -1): #Cas nint = 0, n = -1 retourne [] Foireux... mais normalement sans importance
	a = []
	while nint != 0:
		a.append(nint % 2)
		nint = int((nint - nint % 2) / 2)
	if n != -1:
		if len(a) > n:
			a = a[:n]
		elif len(a) < n:
			for i in range(n - len(a)):
				a.append(0)
	return a

def zintToBin(zint, n = -1):
	if n == -1:
		n += 1 #pas ouf ca
	if zint >= 0:
		r = nintToBin(zint, n = n - 1)
		r.append(0)	
	else:
		a = -zint
		t = nintToBin(a, n = n - 1)
		t.append(0)
		r = complement(t)
		plussun(r)
	return r

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

	def getSpan(self, n, k):
		a = []
		for i in range(n, n + k):
			a.append(self.__getitem__(i))
		return a
        
	def __len__(self):
		return len(self.values)

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
		if type(value) == list:
			for k in range(len(value)):
				if index + k < self.minIndex:
					for i in range(self.minIndex - (index + k)):
						self.values.insert(0, self.alphabet.epsilon)
					self.zeroIndex += (self.minIndex - (index + k))
					self.minIndex = index + k
				elif index + k > self.maxIndex: #TODO A Améliorer de beauuuuuucouuuuup. Jle ferai demain, promis
					for i in range((index + k) - self.maxIndex):
						self.values.append(self.alphabet.epsilon)
					self.maxIndex = index + k
				self.values[self.zeroIndex + index + k] = value[k]
		else:
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
        self.currentState = "0"
        self.index = 0

    def oneStep(self):
        print("Current state : ( " + str(self.currentState) + " , " + str(self.ruban[self.index]) + " )" + "   " + str(self.index) )
        
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


##################################################
def generate_move(x):
	"""Génère un dictionnaire représentant la fonction de transition d'un déplacement
	de x à gauche ou à droite."""
	d = {}
	d[("0", 0)] = ("F", x, 0)
	d[("0", 1)] = ("F", x, 1)
	return d

def generate_copy(n, x):
	"""Génère un dictionnaire représentant la fonction de transition d'une copie
	de n bits vers l'emplacement x (relatif)."""
	d = {}
	for k in range(1, n + 1):
		K = str(k)
		d[("L" + K, 0)] = ("E0" + K, x, 0)
		d[("L" + K, 1)] = ("E1" + K, x, 1)
		d[("E0" + K, 0)] = ("L" + str(k + 1), -1 * (x - 1), 0)
		d[("E0" + K, 1)] = ("L" + str(k + 1), -1 * (x - 1), 0)
		d[("E1" + K, 0)] = ("L" + str(k + 1), -1 * (x - 1), 1)
		d[("E1" + K, 1)] = ("L" + str(k + 1), -1 * (x - 1), 1)	
	return d

def generate_add(n):
    """Génère un dictionnaire représentant la fonction de transition
    d'un aditionneur n bits."""
    d = {}
    d[("0", 1)] = ("E0P1", n, 1)
    d[("0", 0)] = ("E0P0", n, 0)
    d[("E0P0", 1)] = ("E1P", 1 - n, 1)
    d[("E0P0", 0)] = ("E1P", 1 - n, 0)
    d[("E0P1", 1)] = ("E1R", 1 - n, 0)
    d[("E0P1", 0)] = ("E1P", 1 - n, 1)
    for k in range(1, n + 1):
        K = str(k)
        L = str(k + 1)
        d[("E" + K + "P", 1)] = ("E" + K + "P1", n, 1)
        d[("E" + K + "P", 0)] = ("E" + K + "P0", n, 0)
        d[("E" + K + "R", 1)] = ("E" + K + "R1", n, 1)
        d[("E" + K + "R", 0)] = ("E" + K + "P1", n, 0)
        d[("E" + K + "P0", 1)] = ("E" + L + "P", 1 - n, 1)
        d[("E" + K + "P0", 0)] = ("E" + L + "P", 1 - n, 0)
        d[("E" + K + "P1", 1)] = ("E" + L + "R", 1 - n, 0)
        d[("E" + K + "P1", 0)] = ("E" + L + "P", 1 - n, 1)
        d[("E" + K + "R1", 1)] = ("E" + L + "R", 1 - n, 1)
        d[("E" + K + "R1", 0)] = ("E" + L + "R", 1 - n, 0)
    d[("E" + str(n + 1) + "P", 0)] = ("F", - n, 0)
    d[("E" + str(n + 1) + "P", 1)] = ("F", - n, 1)
    d[("E" + str(n + 1) + "R", 0)] = ("F", - n, 0)
    d[("E" + str(n + 1) + "R", 1)] = ("F", - n, 1)
    return d

def generate_mult():
	"""Génère un dictionnaire représentant la fonction de transition
	d'un multiplicateur 8 bits dans Z."""
	d = {}
	d[("L18", 0)] = ("F", 8, 0)
	d[("L18", 1)] = ("F", 8, 1)
	for i in range(0,8):
		I = str(i)
		d[("L1" + I, 0)] = ("L1" + str(i + 1), 1, 0)
		d[("L1" + I, 1)] = ("L2" + I + "(0)", 8 - i, 1)
		d[("L2" + I + "(8)", 0)] = ("L1" + str(i + 1), -15 + i, 0)
		d[("L2" + I + "(8)", 1)] = ("L1" + str(i + 1), -15 + i, 1)	
		for t in range(0,8):
			T = str(t)		
			for k in range(0,8):
				K = str(k)
				d[("E" + I + "(" + K + ")" + T, 0)] = ("L2" + I + "(" + str(t + 1) + ")", -7 - i - k, 1)
				d[("E" + I + "(" + K + ")" + T, 1)] = ("E" + I + "(" + str(k + 1) + ")" + T, 1, 0)		
			d[("L2" + I + "(" + T + ")", 0)] = ("L2" + I + "(" + str(t + 1) + ")", 1, 0)
			d[("L2" + I + "(" + T + ")", 1)] = ("E" + I + "(0)" + T, 8 + i, 1)
	return d

def generate_opposite(n):
	"""Genere une dictionnaire representant la fonction de transition
	permettant de determiner l'oppose d'un entier relatif."""
	d = {}
	d[("I" + str(n + 1), 0)] = ("P1", 0, 0)
	d[("I" + str(n + 1), 1)] = ("P1", 0, 0)
	d[("P" + str(n + 1), 0)] = ("F", -n, 0)
	d[("P" + str(n + 1), 1)] = ("F", -n, 1)
	for k in range(1, n + 1):
		K = str(k)
		d[("I" + K, 0)] = ("J0" + K, n, 0) 
		d[("I" + K, 1)] = ("J1" + K, n, 1)
		d[("J0" + K, 0)] = ("I" + str(k + 1), -n + 1, 1)
		d[("J0" + K, 1)] = ("I" + str(k + 1), -n + 1, 1)
		d[("J1" + K, 0)] = ("I" + str(k + 1), -n + 1, 0)
		d[("J1" + K, 1)] = ("I" + str(k + 1), -n + 1, 0)
		d[("P" + K, 0)] = ("F", -k + 1, 1)
		d[("P" + K, 1)] = ("P" + str(k + 1), 1, 0)
	return d
##################################################


class TuringWindow:

	def __init__(self, machine):
		self.machine = machine
		self.root = tkinter.Tk()
		self.root.minsize(width = 500, height = 500)
		self.root.maxsize(width = 500, height = 500)
		self.root.title("TIPE - Machine de Turing")
		#TODO
		#WIP En vrai je sais meme pas comment presenter la fenetre.... En discuter avec des designers ? Cest chiant les ihm

####################################################

class Generator:

	def __init__(self):
		self.V = []
		self.Vi = {}
		self.n = 0
		self.tr = {}
		self.constante = "0"
		self.ietat = "0"
		self.fetat = "1"
		self.currentIndex = 0
		self.ruban = None
		self.stack = []

	def generate(self, fileName, alphabet): ##TODO : Cleanup
		"""Genere une machine prete a partir."""
		f = open(fileName, "r")
		lines = f.readlines()
		f.close()
		self.ruban = Ruban([alphabet.epsilon], alphabet)
		for a in range(len(lines)):
			lines[a] = lines[a].replace("\n","")
		for line in lines: #TODO : Verifier la syntaxe + exceptions
			self.faidestrucs(line.split(" "))
		return Machine(self.ruban, self.tr)

	def faidestrucs(self, args):
		"""ATTTENTION FONCTION DIGOULASSE.
		Pirate, Ye be warned..."""
		a = args[0]
		if a == "DATA":
			pass #C'est juste là pour faire joli, en fait
		elif a == "BIT":
			self.n = int(args[1])
		elif a == "VAR" :
			self.V.append((args[1], args[2]))
		elif a == "CODE":
			c = 0
			for var in self.V:
				try:
					temp = [int(var[1][k]) for k in range(len(var[1]))]	#Check longueur TODO		
				except ValueError:
					temp = zintToBin(int(var[1][1:]), n = self.n)
				self._generate_write(temp) #Choix intéressant
				self._generate_move(self.n)
				self.Vi[var[0]] = c
				c += self.n
		elif a == "IF":
			self.faidestrucs(args[1:])
			self._generate_if()
		elif a == "ELSE":
			self._generate_else()
		elif a == "ENDIF":
			self._generate_endif()
		elif a == "WHILE":
			self._generate_while(args[1:])
		elif a == "ENDWHILE":
			self._generate_endwhile()
		elif a == "ADD":
			if len(args) == 3:
				self._get(args[1])
				self._generate_move(self.n)
				self._get(args[2])
				self._generate_move(-self.n)
			elif len(args) == 2:
				self._generate_move(self.n)
				self._get(args[1])
				self._generate_move(-self.n)
			self._generate_add(self.n)
		elif a == "SUB":
			if len(args) == 3:
				self._get(args[1])
				self._generate_move(self.n)
				self._get(args[2])
				self._generate_move(-self.n)
			elif len(args) == 2:
				self._generate_move(self.n)
				self._get(args[1])
				self._generate_move(-self.n)
			self._generate_move(self.n)
			self._generate_opposite(self.n)
			self._generate_copy(self.n, -self.n)
			self._generate_move(-2 * self.n)
			self._generate_add(self.n)
		elif a == "MULT":
			if len(args) == 3:
				self._get(args[1])
				self._generate_move(self.n)
				self._get(args[2])
				self._generate_move(-self.n)
			elif len(args) == 2:
				self._generate_move(self.n)
				self._get(args[1])
				self._generate_move(-self.n)	
			self._generate_mult()
		elif a == "COPY":
			self._generate_copy(self.n, int(args[1])) #TODO Avec get
		elif a == "OPP":
			if len(args) == 2:
				self._get(args[1])
			self._generate_opposite(self.n)
		elif a == "MV":
			self._generate_move(int(args[1])) #TODO Avec get
		elif a == "GET":
			self._get(args[1])
		elif a == "SET":
			self._generate_copy(self.n, self.Vi[args[1]] - self.currentIndex)
		elif a == "GT":
			if len(args) == 3:
				self._get(args[1])
				self._generate_move(self.n)
				self._get(args[2])
				self._generate_move(-self.n)
			elif len(args) == 2:
				self._generate_move(self.n)
				self._get(args[1])
				self._generate_move(-self.n)
			self._generate_greater_than(self.n)
		elif a == "EQU":
			if len(args) == 3:
				self._get(args[1])
				self._generate_move(self.n)
				self._get(args[2])
				self._generate_move(-self.n)
			elif len(args) == 2:
				self._generate_move(self.n)
				self._get(args[1])
				self._generate_move(-self.n)
			self._generate_equal(self.n)
						
	
	def getConstante(self):
		t = self.constante
		self.constante = str(int(self.constante) + 1)
		return t

	def getStates(self):
		t = (self.ietat, self.fetat)
		self.ietat = self.fetat
		self.fetat = str(int(self.fetat) + 1)
		return t

	
	def _get(self, a):
		try:
			b = int(a)
			temp = [int(a[k]) for k in range(len(a))] ##TODO Check la taille. Encore.
			self._generate_write(temp)
		except ValueError:
			if a.startswith('b'):##En supposant que a soit de la bonne taille TODO
				temp = zintToBin(int(a[1:]), self.n)
				self._generate_write(temp)
			else: #C'est une variable
				index = self.currentIndex
				self._generate_move(self.Vi[a] - index)
				self._generate_copy(self.n, index - self.Vi[a])
				self._generate_move(index - self.Vi[a])

	def _generate_move(self, x):
		"""Génère un dictionnaire représentant la fonction de transition d'un déplacement
		de x à gauche ou à droite."""
		d = self.tr
		startState, finalState = self.getStates()
		d[(startState, 0)] = (finalState, x, 0)
		d[(startState, 1)] = (finalState, x, 1)
		self.currentIndex += x

	def _generate_write(self, x):
		d = self.tr
		C = self.getConstante()
		startState, finalState = self.getStates()
		d[(startState, 0)] = (C + "E0", 0, 0)
		d[(startState, 1)] = (C + "E0", 0, 1)
		d[(C + "E" + str(len(x)), 0)] = (finalState, -len(x), 0)
		d[(C + "E" + str(len(x)), 1)] = (finalState, -len(x), 1)
		for k in range(len(x)):
			K = str(k)
			d[(C + "E" + K, 0)] = (C + "E" + str(k + 1), 1, x[k])
			d[(C + "E" + K, 1)] = (C + "E" + str(k + 1), 1, x[k])
	
	def _generate_copy(self, n, x):
		"""Génère un dictionnaire représentant la fonction de transition d'une copie
		de n bits vers l'emplacement x (relatif)."""
		d = self.tr
		C = self.getConstante()
		startState, finalState = self.getStates()
		d[(startState, 0)] = (C + "L1", 0, 0)
		d[(startState, 1)] = (C + "L1", 0, 1)
		d[(C + "L" + str(n + 1), 0)] = (finalState, -n, 0)
		d[(C + "L" + str(n + 1), 1)] = (finalState, -n, 1) 
		for k in range(1, n + 1):
			K = str(k)
			d[(C + "L" + K, 0)] = (C + "E0" + K, x, 0)
			d[(C + "L" + K, 1)] = (C + "E1" + K, x, 1)
			d[(C + "E0" + K, 0)] = (C + "L" + str(k + 1), -1 * (x - 1), 0)
			d[(C + "E0" + K, 1)] = (C + "L" + str(k + 1), -1 * (x - 1), 0)
			d[(C + "E1" + K, 0)] = (C + "L" + str(k + 1), -1 * (x - 1), 1)
			d[(C + "E1" + K, 1)] = (C + "L" + str(k + 1), -1 * (x - 1), 1)	

	def _generate_add(self, n):
		"""Génère un dictionnaire représentant la fonction de transition
		d'un aditionneur n bits."""
		d = self.tr
		C = self.getConstante()
		startState, finalState = self.getStates()
		d[(startState, 1)] = (C + "E1P1", n, 1)
		d[(startState, 0)] = (C + "E1P0", n, 0)
		#d[(C + "E0P0", 1)] = (C + "E1P", 1 - n, 1) Ces lignes sont louches et foutent le bronx ......?
		#d[(C + "E0P0", 0)] = (C + "E1P", 1 - n, 0)
		#d[(C + "E0P1", 1)] = (C + "E1R", 1 - n, 0)
		#d[(C + "E0P1", 0)] = (C + "E1P", 1 - n, 1)
		for k in range(1, n + 1):
			K = str(k)
			L = str(k + 1)
			d[(C + "E" + K + "P", 1)] = (C + "E" + K + "P1", n, 1)
			d[(C + "E" + K + "P", 0)] = (C + "E" + K + "P0", n, 0)
			d[(C + "E" + K + "R", 1)] = (C + "E" + K + "R1", n, 1)
			d[(C + "E" + K + "R", 0)] = (C + "E" + K + "P1", n, 0)
			d[(C + "E" + K + "P0", 1)] = (C + "E" + L + "P", 1 - n, 1)
			d[(C + "E" + K + "P0", 0)] = (C + "E" + L + "P", 1 - n, 0)
			d[(C + "E" + K + "P1", 1)] = (C + "E" + L + "R", 1 - n, 0)
			d[(C + "E" + K + "P1", 0)] = (C + "E" + L + "P", 1 - n, 1)
			d[(C + "E" + K + "R1", 1)] = (C + "E" + L + "R", 1 - n, 1)
			d[(C + "E" + K + "R1", 0)] = (C + "E" + L + "R", 1 - n, 0)
		d[(C + "E" + str(n + 1) + "P", 0)] = (finalState, 0, 0)
		d[(C + "E" + str(n + 1) + "P", 1)] = (finalState, 0, 1)
		d[(C + "E" + str(n + 1) + "R", 0)] = (finalState, 0, 0)
		d[(C + "E" + str(n + 1) + "R", 1)] = (finalState, 0, 1)
		self.currentIndex += n

	def _generate_mult(self):
		"""Génère un dictionnaire représentant la fonction de transition
		d'un multiplicateur 8 bits dans Z."""
		d = self.tr
		C = self.getConstante()
		startState, finalState = self.getStates()
		d[(startState, 0)] = (C + "L10", 0, 0)
		d[(startState, 1)] = (C + "L10", 0, 1)
		d[(C + "L18", 0)] = (finalState, 8, 0)
		d[(C + "L18", 1)] = (finalState, 8, 1)
		for i in range(0,8):
			I = str(i)
			d[(C + "L1" + I, 0)] = (C + "L1" + str(i + 1), 1, 0)
			d[(C + "L1" + I, 1)] = (C + "L2" + I + "(0)", 8 - i, 1)
			d[(C + "L2" + I + "(8)", 0)] = (C + "L1" + str(i + 1), -15 + i, 0)
			d[(C + "L2" + I + "(8)", 1)] = (C + "L1" + str(i + 1), -15 + i, 1)	
			for t in range(0,8):
				T = str(t)		
				for k in range(0,8):
					K = str(k)
					d[(C + "E" + I + "(" + K + ")" + T, 0)] = (C + "L2" + I + "(" + str(t + 1) + ")", -7 - i - k, 1)
					d[(C + "E" + I + "(" + K + ")" + T, 1)] = (C + "E" + I + "(" + str(k + 1) + ")" + T, 1, 0)		
				d[(C + "L2" + I + "(" + T + ")", 0)] = (C + "L2" + I + "(" + str(t + 1) + ")", 1, 0)
				d[(C + "L2" + I + "(" + T + ")", 1)] = (C + "E" + I + "(0)" + T, 8 + i, 1)
		self.currentIndex += 16 # 2*n 

	def _generate_opposite(self, n):
		"""Genere une dictionnaire representant la fonction de transition
		permettant de determiner l'oppose d'un entier relatif."""
		d = self.tr
		C = self.getConstante()
		startState, finalState = self.getStates()
		d[(startState, 0)] = (C + "I1", 0, 0)
		d[(startState, 1)] = (C + "I1", 0, 1)
		d[(C + "I" + str(n + 1), 0)] = (C + "P1", 0, 0)
		d[(C + "I" + str(n + 1), 1)] = (C + "P1", 0, 0)
		d[(C + "P" + str(n + 1), 0)] = (finalState, -n, 0)
		d[(C + "P" + str(n + 1), 1)] = (finalState, -n, 1)
		for k in range(1, n + 1):
			K = str(k)
			d[(C + "I" + K, 0)] = (C + "J0" + K, n, 0) 
			d[(C + "I" + K, 1)] = (C + "J1" + K, n, 1)
			d[(C + "J0" + K, 0)] = (C + "I" + str(k + 1), -n + 1, 1)
			d[(C + "J0" + K, 1)] = (C + "I" + str(k + 1), -n + 1, 1)
			d[(C + "J1" + K, 0)] = (C + "I" + str(k + 1), -n + 1, 0)
			d[(C + "J1" + K, 1)] = (C + "I" + str(k + 1), -n + 1, 0)
			d[(C + "P" + K, 0)] = (finalState, -k + 1, 1)
			d[(C + "P" + K, 1)] = (C + "P" + str(k + 1), 1, 0)
		self.currentIndex += n
			
	def _generate_greater_than(self, n):
		d = self.tr
		C = self.getConstante()
		startState, finalState = self.getStates()
		d[(startState, 0)] = (C + "L", n - 1, 0)
		d[(startState, 1)] = (C + "L", n - 1, 1)
		d[(C + "L", 0)] = (C + "M0", n, 0)
		d[(C + "L", 1)] = (C + "M1", n, 1)
		d[(C + "M0", 0)] = (C + "A0", -n - 1, 0)
		d[(C + "M0", 1)] = (C + "Y", 1, 1)
		d[(C + "M1", 0)] = (C + "N", 1, 0)
		d[(C + "M1", 1)] = (C + "A0", -n - 1, 1)
		d[(C + "A" + str(n - 1), 0)] = (C + "N", 2 * n + 1, 0)
		d[(C + "A" + str(n - 1), 1)] = (C + "N", 2 * n + 1, 1)
		d[(C + "Y", 0)] = (finalState, 0, 1)
		d[(C + "Y", 1)] = (finalState, 0, 1)
		d[(C + "N", 0)] = (finalState, 0, 0)
		d[(C + "N", 1)] = (finalState, 0, 0)
		for k in range(n - 1):
			K = str(k)
			d[(C + "A" + K, 0)] = (C + "B0(" + K + ")", n, 0)
			d[(C + "A" + K, 1)] = (C + "B1(" + K + ")", n, 1)
			d[(C + "B0(" + K + ")", 0)] = (C + "A" + str(k + 1), -n - 1, 0)
			d[(C + "B0(" + K + ")", 1)] = (C + "N", k + 2, 1)
			d[(C + "B1(" + K + ")", 0)] = (C + "Y", k + 2, 0)
			d[(C + "B1(" + K + ")", 1)] = (C + "A" + str(k + 1), -n - 1, 1)
		self.currentIndex += (2 * n)

	def _generate_equal(self, n):
		d = self.tr
		C = self.getConstante()
		startState, finalState = self.getStates()
		d[(startState, 0)] = (C + "A0", 0, 0)
		d[(startState, 1)] = (C + "A0", 0, 1)
		d[(C + "N", 0)] = (finalState, 0, 0)
		d[(C + "N", 1)] = (finalState, 0, 0)
		d[(C + "Y", 0)] = (finalState, 0, 1)
		d[(C + "Y", 1)] = (finalState, 0, 1) 
		d[(C + "A" + str(n), 0)] = (C + "Y", n, 0)
		d[(C + "A" + str(n), 1)] = (C + "Y", n, 1)
		for k in range(n):
			K = str(k)
			d[(C + "A" + K, 0)] = (C + "B0(" + K + ")", n, 0)
			d[(C + "A" + K, 1)] = (C + "B1(" + K + ")", n, 1)
			d[(C + "B0(" + K + ")", 0)] = (C + "A" + str(k + 1), -n + 1, 0)
			d[(C + "B0(" + K + ")", 1)] = (C + "N", n - k, 1)
			d[(C + "B1(" + K + ")", 0)] = (C + "N", n - k, 0)
			d[(C + "B1(" + K + ")", 1)] = (C + "A" + str(k + 1), -n + 1, 1)
		self.currentIndex += (2 * n)

	def _generate_if(self):
		d = self.tr
		startState, finalState = self.getStates()		
		d[(startState, 1)] = (finalState, 0, 1)
		self.stack.append(startState)

	def _generate_else(self):
		d = self.tr
		startState, finalState = self.getStates()
		a = self.stack.pop()
		d[(a, 0)] = (finalState, 0, 0)
		self.stack.append(startState)

	def _generate_endif(self):
		d = self.tr
		startState, finalState = self.getStates()
		a = self.stack.pop()
		d[(a, 0)] = (finalState, 0, 0)
		d[(a, 1)] = (finalState, 0, 1)
		d[(startState, 0)] = (finalState, 0, 0)
		d[(startState, 1)] = (finalState, 0, 1)

	def _generate_while(self, assertion):
		d = self.tr
		i = self.currentIndex
		s, f = self.getStates()
		self.ietat = s
		self.fetat = f
		self.faidestrucs(assertion)
		startState, finalState = self.getStates()		
		d[(startState, 1)] = (finalState, i - self.currentIndex, 1)
		self.currentIndex += (i - self.currentIndex)
		self.stack.append((s,startState, i))	

	def _generate_endwhile(self):
		d = self.tr
		s, ss, i = self.stack.pop()
		startState, finalState = self.getStates()
		d[(ss, 0)] = (finalState, i - self.currentIndex, 0)
		d[(startState, 0)] = (s, i - self.currentIndex, 0)
		d[(startState, 1)] = (s, i - self.currentIndex, 1)
		self.currentIndex += (i - self.currentIndex)

def test(f):
	g = Generator()
	m = g.generate(f,unpack("binaire.pickle"))
	m.allSteps()
	print(m.ruban)
	return m










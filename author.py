__author__ = 'Ryan Branch'
import random

#A link in the Markov chain
class Link:

	#Constructor for a link containing a word.
	#A posID of 0 indicates a normal link.
	#A negative posID indicates a link at the front
	#A positive posID indicates a link at the back
	def __init__(self, word_, choiceMade_):
		self.word = word_
		self.partOfSpeech = ""
		self.front = False
		self.back = False
		self.prevLink = None
		self.nextLink = None
		self.choiceMade = choiceMade_

	#Set function for word
	def setWord(self, wordIn):
		self.word = wordIn

	#Get function for word
	def getWord(self):
		return self.word

	#Set function for front
	def setFront(self, frontIn):
		self.front = frontIn

	#Get function for front
	def getFront(self):
		return self.front

    #Set function for back
	def setBack(self, backIn):
		self.back = backIn

	#Get function for back
	def getBack(self):
		return self.back

    #Set function for prevLink
	def setPrevLink(self, prevLinkIn):
		self.prevLink = prevLinkIn

	#Get function for prevLink
	def getPrevLink(self):
		return self.prevLink

    #Set function for nextLink
	def setNextLink(self, nextLinkIn):
		self.nextLink = nextLinkIn

	#Get function for nextLink
	def getNextLink(self):
		return self.nextLink

	#Set function for choiceMade
	def setChoiceMade(self, choiceMadeIn):
		self.choiceMade = choiceMadeIn

	#Get function for choiceMade
	def getChoiceMade(self):
		return self.choiceMade

#A Markov chain
class Chain:
	#Constructor for a piece based on input values
	def __init__(self, links_):
		self.links = links_

	#Gets the string represented by the chain, delimited by " "
	#NOTE: This currently makes the string end in a " ". Ideally I should get rid of this.
	def getString(self):
		outString = ""
		for link in self.links[:-1]:
			outString += link.getWord()
			outString += " "
		outString += self.links[-1].getWord()
		return outString

	#Set function for links
	def setLinks(self, linksIn):
		self.links = linksIn

	#Get function for links
	def getLinks(self):
		return self.links

	#Function to add a link to the end of chain
	def appendBack(self, linkIn):

		#If self.links is currently empty
		if (len(self.links) == 0):
			linkIn.setFront(True)
			linkIn.setBack(True)
			self.links.append(linkIn)

		#If self.links has an element
		elif (len(self.links) >= 1):
			linkIn.setBack(True)
			linkIn.setPrevLink(self.links[-1])
			self.links[-1].setBack(False)
			self.links[-1].setNextLink(linkIn)
			self.links.append(linkIn)

	    #Set function for numChoices
	def setNumChoices(self, numChoicesIn):
		self.numChoices = numChoicesIn

	#Get function for numChoices
	def getNumChoices(self):
		choices = 0
		for link in self.links:
			if link.getChoiceMade():
				choices += 1
		return choices

	#Get function for lenWords
	def getLenWords(self):
		return len(self.links)

	#Get function for lenChars
	def getLenChars(self):
		length = 0
		for link in self.links:
			length += len(link.getWord())
		return length

class Markov:
	#Constructor with corpus input
	def __init__(self, corpus_):
		self.bookshelf = {}
		self.corpus = corpus_
		self.chains = {}

	#REQUIRES: self.corpus is space-delimited
	#EFFECTS: Returns a list of Markov tuples of length self.length
	def buildTuples(self, length):
		tuples = []
		words = self.corpus.split()
		for i in range((len(words) - (length - 1))):
			tuple = ()
			for j in range(length):
				tuple += (words[i + j],)
			tuples.append(tuple)
		return tuples

	#REQUIRES: self.corpus is space-delimited
	#MODIFIES: self.dictionary
	#EFFECTS: Builds the dictionary
	def buildDictionary(self, tupleLength):
		#Ensures that a dictionary of that tupleLength doesn't already exist
		if tupleLength in self.bookshelf:

			#Returns False, signalling that no new dictionary has been added
			return False
		else:
			newDictionary = {}

			#Builds the dictionary from the tupleLength
			for tuple in self.buildTuples(tupleLength):
				#Initializes the "key" to be looked up
				key = ()
				#For all but the last word in the tuple, add to the key
				for word in tuple[:-1]:
					key += (word,)

				#If the key already exists in the dictionary, update the entry
				if key in newDictionary:
					(newDictionary[key]).append(tuple[-1])
				#If not, create a new entry
				else:
					newDictionary[key] = [tuple[-1]]

			#Adds the dictionary to the bookshelf
			(self.bookshelf)[tupleLength] = newDictionary

			#Returns True, signaling that a new dictionary has been built and added
			return True

	#Picks a random phrase of length lengthIn out of the corpus
	def getSeed(self, lengthIn):
		bodyWords = self.corpus.split()[:((lengthIn + 0) * -1)] #NOTE: Does this 0 need to be higher?
		outSeed = ""
		choiceIndex = random.randint(0,(len(bodyWords) - 1))
		for i in range(lengthIn - 1):
			outSeed += bodyWords[choiceIndex + i]
			outSeed += " "
		outSeed += bodyWords[choiceIndex + lengthIn - 1]
		return outSeed

	#EFFECTS: Returns a Piece where the length in characters is close to but not exceeding targetLength
	def write(self, seed, targetLength):
		seedTuple = ()
		words = seed.split()
		tupleSize = len(words) + 1

		#Generates the random seed using the system time
		random.seed()

		#Builds a new dictionary to fit the seed, if one doesn't already exist
		self.buildDictionary(tupleSize)
		theDictionary = self.bookshelf[tupleSize]

		#Creates the initial list of links
		initialLinks = []

		#Builds the first key to look up in the dictionary
		for i, word in enumerate(words):
			#I was doing something more advanced with "links" here but now I just want to go for basic functionality
			#So I'm saving this for later.
			#It will be used down the line for more complex algorithms involving things like parts of speech

			#The "False" represents the fact that no choice was made in building this part of the chain
			initialLinks.append(Link(word, False))
			seedTuple += (word,)

		#Initializes the Chain
		theChain = Chain(initialLinks)

		#Keep going as long as the length limit isn't reached
		while ((targetLength - theChain.getLenChars()) > 1):
			#Initializes madeChoice as false
			madeChoice = False

			#Writes the output
			try:
				matchLength = len(theDictionary[seedTuple])
			except:
				lastWord = self.corpus.split()[-1]
				if (seedTuple[-1] == lastWord):
					#At this point, the end of the corpus has been reached and there is no escape.
					return theChain
				else:
					print("Unable to locate key in theDictionary: " + str(seedTuple))

			#If there is only one word to choose from, picks that word
			if (matchLength == 1):
				nextWord = theDictionary[seedTuple][0]

			#If there are multiple words to choose from
			elif (matchLength > 1):
				randIndex = random.randint(0, (matchLength - 1))
				#Checks if all of the keys are the same
				checkWord = theDictionary[seedTuple][randIndex]
				#NOTE: Later on I need to make this more efficient so that we leave the for loop when allSame is found to be false
				allSame = True
				for word in theDictionary[seedTuple]:
					if (word != checkWord):
						#Boolean marked as false if not all words are the same
						allSame = False
				#If at least one word differed from checkWord, this should be counted as a choice
				if not allSame:
					madeChoice = True
				nextWord = checkWord

			#Some sort of error; the dictionary has no matching key
			#This can happen if the seed doesn't appear in the corpus
			else:
				print("Dictionary " + str(tupleSize) + " has no key matching " + str(seedTuple))
				#NOTE: Use exception here instead of returning false.

			#Creates the new seedTuple
			newTuple = ()
			for i in range(1, len(seedTuple)):
				newTuple += (seedTuple[i],)
			newTuple += (nextWord,)
			seedTuple = newTuple

			#If there is space, dds the new word to the text and performs other necessary operations
			if ((targetLength - theChain.getLenChars()) > len(nextWord)):
				theLink = Link(nextWord, madeChoice)
				theChain.appendBack(theLink)

			#If there isn't space, creates the Piece and returns it
			else:
				return theChain
		return theChain
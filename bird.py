import tweepy
from author import *

#GLOBAL CONSTANTS
CONSUMER_KEY = "Your Consumer Key goes in these quotes."
CONSUMER_SECRET = "Your Consumer Secret goes in these quotes."
ACCESS_KEY = "Your Access Key goes in these quotes."
ACCESS_SECRET = "Your Access Secret goes in these quotes."
CHARACTERS_PER_TWEET = 140
TUPLE_SIZE = 3

#NOTE: This should be the same as what is specified in split.py
FILENAMES_FILE = "corpus_filenames.txt"

#The program will attempt to generate a tweet in which the fraction of words generated
#by a choice is somewhere between TARGET_RATIO_MIN and TARGET_RATIO_MAX
#While attempting to find this tweet, it will start with the longest tuple size and
#move down towards the shortest, attempting ATTEMPTS times for each size until a
#suitable tweet is found.  If none are found, it will tweet the last attempt generated.
#This is my attempt at generating the most original tweet that maintains coherency.
TARGET_RATIO_MIN = 0.2
TARGET_RATIO_MAX = 0.4
ATTEMPTS = 30

#Defines punctuation marks which signal the end of a sentence
TERMINAL_PUNCTUATION = [".", "?", "!", "\""]

class Bird:
	def __init__(self):
		#Initializes the random seed
		random.seed()

		#Sets up Tweepy
		self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		self.api = tweepy.API(self.auth)

		#Sets up marks (markov chain instances)
		#A mark revolves around a single corpus and can contain multiple dictionaries
		#When generating content, a specific mark can be chosen and then from that the
		#specific dictionary to use can be built and selected, effectively allowing for
		#control over both the corpus and tuple size
		self.mark = None
		self.bodyText = ""
		self.corpusFilenames = []

	#Sets up the markov chain instances to use.
	#bodyTexts is a list of strings which are corpora from which texts are generated
	#sizes specifies which tuple sizes to generate dictionaries from for each string in bodyTexts
	#REQUIRES:
	#sizes should be a list of positive integers with a minimum of 2.
	#Theoretically its maximum should be the length, in words, of the shortest string in bodyTexts
	#But the actual upper limit should be much, much lower for functionality's sake.
	#EFFECTS:
	#The order in which each markov chain instance is stored in marks corresponds to the
	#order in which the string appears in bodyTexts.  This order should be preserved.
	def markovSetup(self):
		#Stored for later use
		self.dictSize = TUPLE_SIZE

		#Creates the Markov Chain Instance
		self.mark = Markov(self.bodyText)
		self.mark.buildDictionary(self.dictSize)

	def generateTweet(self):
		ready = False
		numAttempts = 0
		while ((not ready) and (numAttempts < ATTEMPTS)):
			theSeed = self.mark.getSeed(self.dictSize - 1)
			newChain = self.mark.write(theSeed, CHARACTERS_PER_TWEET)
			ratio = (float(newChain.getNumChoices()) / newChain.getLenWords())
			if ((ratio >= TARGET_RATIO_MIN) and (ratio <= TARGET_RATIO_MAX)):
				ready = True
			numAttempts += 1

		output = newChain.getString()
		return output

	def trimTweet(self, input):
		spaceFound = False
		punctFound = False
		foundIndex = -1

		#If the final character is already a punctuation mark, return the input string.
		if input[-1] in TERMINAL_PUNCTUATION:
			return input

		for i, char in enumerate(reversed(input)):

			#Continues until foundIndex has been updated, when a sentence end is found
			if (foundIndex == -1):
				#During the current iteration, if a blank space is found, remember that
				if (char == " "):
					spaceFound = True

				#If a blank space was found in the last iteration, check for punctuation
				#Elif is used to ensure that this doesn't run directly after last if
				elif spaceFound:
					if (char in TERMINAL_PUNCTUATION):
						punctFound = True
						foundIndex = i

					#Otherwise, reset spaceFound
					else:
						spaceFound = False

		#If foundIndex is unchanged, simply return the input string
		if foundIndex == -1:
			return input

		#Otherwise, return the input string less the trailing sentence fragment.
		else:
			return input[:(-1 * foundIndex)]

	#Posts a tweet
	def tweet(self, string):
		self.api.update_status(string)
		print("Tweet successful!")

	#Gets all of the corpus filenames and adds them to the corpusFilenames array
	def buildCorpusFilenames(self):
		with open(FILENAMES_FILE, 'rb') as file:
			for line in file:
				self.corpusFilenames.append(line)
		file.close()

	#Builds the body text to be used for tweet generation
	def buildBodyText(self, filename):
		with open(filename, 'rb') as file:
			for line in file:
				self.bodyText += (line.rstrip() + " ")
		file.close()

	#Set function for corpusFilenames
	def setCorpusFilenames(self, corpusFilenamesIn):
		self.corpusFilenames = corpusFilenamesIn

	#Get function for corpusFilenames
	def getCorpusFilenames(self):
		return self.corpusFilenames

	#returns the element of corpusFilenames at index
	def getCorpusFilename(self, index):
		return self.corpusFilenames[index]

def main():
	theBird = Bird()
	theBird.buildCorpusFilenames()
	corpusIndex = random.randint(0, (len(theBird.getCorpusFilenames()) - 1))
	corpusFilename = theBird.getCorpusFilename(corpusIndex).rstrip()
	theBird.buildBodyText(corpusFilename)
	theBird.markovSetup()
	tweetString = theBird.trimTweet(theBird.generateTweet())
	print(tweetString)
	theBird.tweet(tweetString)

main()
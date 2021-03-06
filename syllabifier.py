#
# See the original at: https://sourceforge.net/projects/p2tk/
#
# License: MIT
# 
#

# This is the P2TK automated syllabifier. Given a string of phonemes,
# it automatically divides the phonemes into syllables.
#
# By Joshua Tauberer, based on code originally written by Charles Yang.
#
# The syllabifier requires a language configuration which specifies
# the set of phonemes which are consonants and vowels (syllable nuclei),
# as well as the set of permissible onsets.
#
# Then call syllabify with a language configuration object and a word
# represented as a string (or list) of phonemes.
#
# Returned is a data structure representing the syllabification.
# What you get is a list of syllables. Each syllable is a tuple
# of (stress, onset, nucleus, coda). stress is None or an integer stress
# level attached to the nucleus phoneme on input. onset, nucleus,
# and coda are lists of phonemes.
#
# Example:
#
# import syllabifier
# language = syllabifier.English # or: syllabifier.loadLanguage("english.cfg")
# syllables = syllabifier.syllabify(language, "AO2 R G AH0 N AH0 Z EY1 SH AH0 N Z")
#
# The syllables variable then holds the following:
# [ (2, [],     ['AO'], ['R']),
#   (0, ['G'],  ['AH'], []),
#   (0, ['N'],  ['AH'], []),
#   (1, ['Z'],  ['EY'], []),
#   (0, ['SH'], ['AH'], ['N', 'Z'])]
#
# You could process that result with this type of loop:
#
# for stress, onset, nucleus, coda in syllables :
#   print " ".join(onset), " ".join(nucleus), " ".join(coda)
#
# You can also pass the result to stringify to get a nice printable
# representation of the syllables, with periods separating syllables:
#
# print syllabify.stringify(syllables)
#
#########################################################################

English = {
	'consonants': ['B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N',
	'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH'],
	'nuclei': [ 'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW'],
	'onsets': ['P', 'T', 'K', 'B', 'D', 'G', 'F', 'V', 'TH', 'DH', 'S', 'Z', 'SH', 'CH', 'JH', 'M',
	'N', 'R', 'L', 'HH', 'W', 'Y', 'P R', 'T R', 'K R', 'B R', 'D R', 'G R', 'F R',
	'TH R', 'SH R', 'P L', 'K L', 'B L', 'G L', 'F L', 'S L', 'T W', 'K W', 'D W',
	'S W', 'S P', 'S T', 'S K', 'S F', 'S M', 'S N', 'G W', 'SH W', 'S P R', 'S P L',
	'S T R', 'S K R', 'S K W', 'S K L', 'TH W', 'ZH', 'P Y', 'K Y', 'B Y', 'F Y',
	'HH Y', 'V Y', 'TH Y', 'M Y', 'S P Y', 'S K Y', 'G Y', 'HH W', '']
	}
Luxembourgish = {
	'consonants': ['ˈ', 'b', 'ɕ', 'd', 'd̥', 'ð', 'dʒ', 'f', 'ɡ', 'h', 'i̯', 'j', 'k', 'l', 'm', 'n', 
	'ɲ', 'ŋ', 'p', 'pf', 'ʀ', 'ʁ', 's', 'ʃ', 't', 'ts', 'tʃ', 'ɥ', 'v', 'w', 'z', 'ʑ', 'ʒ', 'θ', 'χ'],
	
	'nuclei': ['a', 'aː', 'ãː', 'aːɐ', 'æ', 'æː', 'æːɪ', 'æːʊ', 'ɐ', 'ɑ', 'ɑ̃ː', 'ɑɪ', 'ɑɪ', 
	'ɑʊ', 'e', 'eː', 'ə', 'əʊ', 'ɛ', 'ɛː', 'ɛ̃ː', 'ɛːɐ', 'ɜɪ', 'i', 'iː', 'iːɐ', 'iːə', 
	'iə', 'ɪ', 'o', 'ø', 'oː', 'øː', 'øːɐ', 'œ', 'œː', 'oɪ', 'ɔ', 'ɔː', 'ɔːɐ', 'ɔø', 'ɔʏ̯', 
	'u', 'uː', 'uːɐ', 'uːə', 'uə', 'ʊ', 'ʊɐ', 'y', 'yː'],
	
	'onsets': ['ˈ', 'b', 'b i̯', 'b l', 'b ʀ', 'ɕ', 'd', 'd̥', 'd i̯', 'ð', 'd ʀ', 'dʒ', 'dʒ w', 'f', 'f ɥ', 'f i̯', 'f l', 
	'f ʀ', 'ɡ', 'ɡ l', 'ɡ n', 'ɡ ʀ', 'g z', 'h', 'i̯', 'j', 'k', 'k ɥ', 'k i̯', 'k l', 'k n', 'k ʀ', 'k w', 'l', 'l i̯',
	'm', 'm i̯', 'n', 'n i̯', 'n w', 'ɲ', 'p', 'p ɥ', 'p i̯', 'p l', ' p l w', 'p ʀ', 'p s', 'p w', 'p f', 'p f l', 'ʀ', 
	'ʀ i̯', 'ʁ', 's', 's ɥ', 's i̯', 's w', 'ʃ', 'ʃ i̯', 'ʃ l', 'ʃ m', 'ʃ n', 'ʃ p', 'ʃ p l', 'ʃ p ʀ', 'ʃ ʀ', 
	'ʃ t', 'ʃ t ʀ', 'ʃ v', 'ʃ w', 't', 't i̯', 't ʀ', 't ʃ', 't w', 'ts', 'ts i̯', 'ts ʀ', 'ts w', 'v', 'v ʀ', 'w', 'z', 
	'z i̯', 'ʑ', 'ʒ', 'ʒ i̯', 'χ']
	}

def loadLanguage(filename) :
	'''This function loads up a language configuration file and returns
	the configuration to be passed to the syllabify function.'''

	L = { "consonants" : [], "nuclei" : [], "onsets" : [] }

	f = open(filename, "r")
	section = None
	for line in f :
		line = line.strip()
		if line in ("[consonants]", "[nuclei]", "[onsets]") :
			section = line[1:-1]
		elif section is None :
			raise ValueError("File must start with a section header such as [consonants].")
		elif not section in L :
			raise ValueError("Invalid section: " + section)
		else :
			L[section].append(line)

	for section in "consonants", "nuclei", "onsets" :
		if len(L[section]) == 0 :
			raise ValueError("File does not contain any consonants, nuclei, or onsets.")

	return L

def syllabify(language, word) :
	'''Syllabifies the word, given a language configuration loaded with loadLanguage.
	   word is either a string of phonemes from the CMU pronouncing dictionary set
	   (with optional stress numbers after vowels), or a Python list of phonemes,
	   e.g. "B AE1 T" or ["B", "AE1", "T"]'''

	if type(word) == str :
		word = word.split()

	syllables = [] # This is the returned data structure.

	internuclei = [] # This maintains a list of phonemes between nuclei.

	for phoneme in word :

		phoneme = phoneme.strip()
		if phoneme == "" :
			continue
		stress = None
		if phoneme[-1].isdigit() :
			stress = int(phoneme[-1])
			phoneme = phoneme[0:-1]

		if phoneme in language["nuclei"] :
			# Split the consonants seen since the last nucleus into coda and onset.

			coda = None
			onset = None

			# If there is a period in the input, split there.
			if "." in internuclei :
				period = internuclei.index(".")
				coda = internuclei[:period]
				onset = internuclei[period+1:]

			else :
				# Make the largest onset we can. The 'split' variable marks the break point.
				for split in range(0, len(internuclei)+1) :
					coda = internuclei[:split]
					onset = internuclei[split:]

					# If we are looking at a valid onset, or if we're at the start of the word
					# (in which case an invalid onset is better than a coda that doesn't follow
					# a nucleus), or if we've gone through all of the onsets and we didn't find
					# any that are valid, then split the nonvowels we've seen at this location.
					if " ".join(onset) in language["onsets"] \
					   or len(syllables) == 0 \
					   or len(onset) == 0 :
					   break

			# Tack the coda onto the coda of the last syllable. Can't do it if this
			# is the first syllable.
			if len(syllables) > 0 :
				syllables[-1][3].extend(coda)

			# Make a new syllable out of the onset and nucleus.
			syllables.append( (stress, onset, [phoneme], []) )

			# At this point we've processed the internuclei list.
			internuclei = []

		elif not phoneme in language["consonants"] and phoneme != "." :
			raise ValueError("Invalid phoneme: " + phoneme)

		else : # a consonant
			internuclei.append(phoneme)

	# Done looping through phonemes. We may have consonants left at the end.
	# We may have even not found a nucleus.
	if len(internuclei) > 0 :
		if len(syllables) == 0 :
			syllables.append( (None, internuclei, [], []) )
		else :
			syllables[-1][3].extend(internuclei)

	return syllables

def stringify(syllables) :
	'''This function takes a syllabification returned by syllabify and
	   turns it into a string, with phonemes spearated by spaces and
	   syllables spearated by periods.'''
	ret = []
	for syl in syllables :
		stress, onset, nucleus, coda = syl
		if stress != None and len(nucleus) != 0 :
			nucleus[0] += str(stress)
		ret.append(" ".join(onset + nucleus + coda))
	return " . ".join(ret)

# If this module was run directly, syllabify the words on standard input
# into standard output. Hashed lines are printed back untouched.
if __name__ == "__main__" :
	import sys
	if len(sys.argv) != 2 :
		print("Usage: python syllabifier.py english.cfg < textfile.txt > outfile.txt")
	else :
		L = loadLanguage(sys.argv[1])
		for line in sys.stdin :
			if line[0] == "#" :
				sys.stdout.write(line)
				continue
			line = line.strip()
			s = stringify(syllabify(L, line))
			sys.stdout.write(s + "\n")
			
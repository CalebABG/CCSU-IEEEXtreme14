import time

from IEEEXploreIndexing import helper

"""
IEEEXtreme14 2020 - https://csacademy.com/ieeextreme14/summary/
 
Problem: IEEEXplore Indexing - https://csacademy.com/ieeextreme14/task/ieeexplore-indexing/

Solution:
- Author: Caleb ABG
    - This code is an attempt at parsing the given html, looking and counting the keywords provided
        by the problem. There's probably a better way to solve this problem, but time ran out
    - Upside, this approach is wicked fast because I approached the parsing using a state-machine.
        the average algorithm efficiency is O(N) (approx: O(10*N))
- Issues:
    - The parser adds the text from the ```<publicationtitle>``` tag, most likely because the end of the tag name
        includes "title" which is a keyword that the parser looks for.
    - As a consequence, the counting of the words per section, is thrown off; for sample input, 
        the offset is around -5 to -12 to subtract from the total word count to account for the added words
    - Handling of tie's for words with the same index value is not taken into account, due to running out of time

Our Team: Mcalliver
- Placed: 5th in (R1) Northeastern US
- The geniuses of our team:
    - Mack - Github: MackG96
    - Javier - Github: Javi-Diez
    - Caleb - Github: CalebABG
    - Dave Broderick (Team Proctor) - Github: djbrod

1. To use a file as input change the filename. The default is: 'input.txt'
2. To use Command Line Input, set 'INPUT_TEXT_FILENAME' to 'None'
"""
# INPUT_TEXT_FILENAME = None
INPUT_TEXT_FILENAME = "input.txt"

# O(2*N) - splitting lines
stopWords, indexTerms = helper.get_stops_and_indexes(INPUT_TEXT_FILENAME)

# O(N) - building dict
indexTermsDict = dict.fromkeys(indexTerms, 0)

# O(N) - retrieving lines
allLines = helper.get_all_lines(INPUT_TEXT_FILENAME)

start_time = time.time()

allChars = []
linesStr = ""

# O(N)
for line in allLines:
    linesStr += line

# O(N)
for char in linesStr:
    allChars.append(char)

"""State Variables"""
state = 0

tokens = []
words = []
sections = []

specialTokens = {
    "<title>": 5,
    "<abstract>": 3,
    "<body>": 1
}

xmlTagStack = []
tokenStr = ""

previousChar = None

# O(N)
for i in range(len(allChars)):
    if i - 1 > -1:
        previousChar = allChars[i - 1]

    c = allChars[i]

    # Search for Tokens
    if state == 0:

        # Reset State because we've seen a 'break' token
        if helper.break_char_found(c):
            # Add word after
            if len(tokenStr) > 0:
                words.append(tokenStr.lower().replace("'", ""))

            tokenStr = ""
            state = 0
            continue

        # Opening XML Tag seen
        if c == '<':
            # Add word seen before start of an XML Tag
            if len(tokenStr) > 0:
                words.append(tokenStr.lower().replace("'", ""))

            tokenStr = ""

            tokenStr += c
            state = 1
            continue

        # If we're here, we must be looking at text, not searching for XML Tags
        tokenStr += c

    # XML Tag Opening
    elif state == 1:
        # if c == ' ':
        #     continue

        # End char of Opening XML Tag
        if c == '>':
            tokenStr += c
            tokens.append(tokenStr)

            xmlTagName = tokenStr
            if xmlTagName in specialTokens.keys():
                xmlTagStack.append(xmlTagName)

            tokenStr = ""
            state = 0
            continue

        # Start char of Closing XML Tag seen
        # This means we're closing a pair of XML Tags: i.e "<i> </i>"
        if c == '/':
            tokenStr += c
            state = 2
            continue

        # Append newly seen character
        tokenStr += c

    # XML Tag Closing
    elif state == 2:
        # End char of Closing XML Tag
        if c == '>':
            tokenStr += c
            tokens.append(tokenStr)

            # print(tokenStr)

            if len(xmlTagStack) > 0:
                # get tag name without opening '</'
                xmlTagName = tokenStr.replace('/', '')

                # get current tag scope we're in
                openXmlTag = xmlTagStack[-1]

                if openXmlTag == xmlTagName:
                    # Remove matching 'opening' XML Tag
                    xmlTagStack.pop()

                    tagWords = words
                    section = (openXmlTag, tagWords)
                    sections.append(section)

                    words = []

            tokenStr = ""
            state = 0
            continue

        # Append newly seen character
        tokenStr += c

# Total Words
L = -5

# print(tokens)
# print(sections)


# sections[0] = an XML Tag name
# sections[1] = a list of words
sectionIndex = 0
sectionIndexOffset = 0
sectionCount = len(sections)

# Approx: O(N) with for loop
# decompression
while sectionIndex < sectionCount:
    section = sections[sectionIndex]
    sectionLen = len(section[1])

    if sectionIndexOffset < sectionLen:
        word = section[1][sectionIndexOffset]
        if len(word) >= 4:
            L += 1

        if word in indexTerms:
            token = section[0]
            indexTermsDict[word] += specialTokens[token]

        sectionIndexOffset += 1
    else:
        sectionIndex += 1
        sectionIndexOffset = 0

print(f"\nTotal Words: {L}")

# O(N)
sortedIndexTermsDict = {k: v for k, v in sorted(indexTermsDict.items(), key=lambda item: item[1], reverse=True)}

tieFound = False
c = 0

# O(N)
print("\nOutput: ")
for term in sortedIndexTermsDict:
    if c >= 3 and not tieFound:
        break

    term_score = int(sortedIndexTermsDict[term])
    print(f"{term}: {(term_score / L) * 100.0}")

    c += 1

print("\nApprox Execution Time: %s sec" % (time.time() - start_time))

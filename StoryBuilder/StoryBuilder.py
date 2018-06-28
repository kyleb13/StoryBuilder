#Kyle Beveridge, TCSS 435 Spring 2018
#
#This program takes all of the words from multiple books,
#builds a trigram model (frequency in which sets of 3 words are found),
#and builds a new 1000 word story based on the trigram model.

import random

#calls all of the functions needed in required orded
def main(filelist = []):
    name = "story1.txt"
    if len(filelist)==6:
        name = "story2.txt"
    masterlist = readFiles(filelist) #get the data from the files
    trigram = processData(masterlist) #build the hash table from the data
    words = buildStory(trigram) #build a story from
    writeToFile(name, words)
    print(name + " created! " + str(len(filelist)) + " files used.")


# Read all of the files into an array of words and return that array
def readFiles(flist = []):
    results = []
    for f in flist:
        buffer = ""
        with open(f, 'r') as file:
            buffer = file.read()
            buffer = buffer.replace('\n', ' ').lower()
            results.append([x for x in buffer.split(" ") if x!=''])
    return results

#Take the array of words and build a trigram hash table out of that data
def processData(indata = []):
    result = {}
    for data in indata:
        idx = 0
        while idx + 2 < len(data):
            word1, word2, word3 = data[idx:idx + 3]
            if data[idx] not in result:#word not found, so make a new entry
                node = {word3:1}
                result[word1] = {word2:[node, 1]}
            else: #at least the first word has been encountered previously
                node1 = result[word1]
                if word2 in node1:#if second word has been encountered, increment counters
                    node2 = node1[word2]
                    node2[1] += 1
                    if word3 in node2[0]:#if third word has been encountered, increment counters
                        node2[0][word3] += 1
                    else: #else add new entry
                        node2[0][word3] = 1
                else: #else add new entry
                    node1[word2] = [{word3:1}, 1]
            idx +=1
    return result

def buildStory(tritable = {}):
    buffer = []
    recent = []
    word = random.choice(list(tritable))
    buffer.append(word)
    while len(buffer)<1020:#get 1000 words, with a little extra so final sentence can be finished
        if word in recent:#dont use word if used recently
            word = random.choice(list(tritable))#use random word instead
        recent.append(word)
        max = 0
        word2 = ""
        node2 = tritable[word]
        #pick second and third words based on frequency, or randomly if
        #chosen word was used recently
        for w in node2.keys():
            if node2[w][1]>max:
                word2 = w
                max = node2[w][1]
        if(word2 not in recent):
            recent.append(word2)
        else:
            word2 = random.choice(list(node2))
        buffer.append(word2)
        max = 0
        word3 = ""
        node3 = node2[word2][0]
        for t in node3.keys():
            if node3[t]>max:
                word3 = t
                max = node3[t]
        if(word3 not in recent):
            recent.append(word3)
        else:
            word3 = random.choice(list(node3))
        buffer.append(word3)
        word = word3
        while len(recent)>15:#only remember the last 15 used words
            recent.pop(0)
    return buffer


#write the story into the file in a more story-like format
def writeToFile(filename, words):
    cnt = 0
    linecnt = 0
    sentcnt = 0
    doNotEnd = ["and", "or", "for", "the", "if", "then", "a", "i", "we", "with", "no", "what", "now"]
    needPeriod = False
    nextCapital = True
    needIndent = True
    canIndent = True
    sentenceComplete = False
    with open(filename, 'w') as file:
        while (cnt<1000 or not(sentenceComplete)) and cnt != len(words):
            word = words[cnt]
            if needIndent and canIndent:#indent a new paragraph if current is past 200 words
                                        #and we are not currently in the middle of a sentence
                if cnt!=0:
                    file.write("\n")
                file.write("    ")
                needIndent = False
                canIndent = False
                linecnt = 0
                sentcnt = 0
            file.write(word.capitalize() if nextCapital or word == "i" else word)#write word, and capitalize if new sentence
            sentenceComplete = False
            if nextCapital:#if word was capitalized, set bool to false so next isnt
                nextCapital = False
            if sentcnt%15 == 0 and sentcnt != 0:#if we are over 16 words, we should end the sentence
                needPeriod = True
            else:#if sentence is ongoing, we cant indent for a new paragraph
                canIndent = False
            if cnt%200 == 0 and cnt != 0:#if we are over 200 words, we should start new paragraph
                needIndent = True
            if word not in doNotEnd and needPeriod:#if the word is not a poor word to end on and we need a period, put in a period
                file.write(".")
                sentcnt = 0
                sentenceComplete = True
                needPeriod = False
                nextCapital = True
                canIndent = True
            file.write(" ")
            if linecnt%25 == 0 and linecnt != 0:#if current line has more than 25 words, start new line
                file.write("\n")
                linecnt = 0
            cnt += 1
            linecnt += 1
            sentcnt += 1
        if sentenceComplete == False:
            file.write(".")
        file.write("\n---------THE END---------")


if __name__=="__main__":
    filelist = []
    filelist.append("doyle-27.txt")
    filelist.append("doyle-case-27.txt")
    main(filelist)
    filelist.append("alice-27.txt")
    filelist.append("london-call-27.txt")
    filelist.append("melville-billy-27.txt")
    filelist.append("twain-adventures-27.txt")
    main(filelist)
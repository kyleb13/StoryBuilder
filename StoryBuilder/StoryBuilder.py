import random

def main(filelist = []):
    name = "story1.txt"
    if len(filelist)==6:
        name = "story2.txt"
    masterlist = readFiles(filelist)
    trigram = processData(masterlist)
    words = buildStory(trigram)
    print()


def readFiles(flist = []):
    results = []
    for f in flist:
        buffer = ""
        with open(f, 'r') as file:
            buffer = file.read()
            buffer = buffer.replace('\n', ' ').lower()
            results.append([x for x in buffer.split(" ") if x!=''])
    return results

def processData(indata = []):
    result = {}
    for data in indata:
        idx = 0
        while idx + 2 < len(data):
            word1, word2, word3 = data[idx:idx + 3]
            if data[idx] not in result:
                node = {word3:1}
                result[word1] = {word2:[node, 1]}
            else:
                node1 = result[word1]
                if word2 in node1:
                    node2 = node1[word2]
                    node2[1] += 1
                    if word3 in node2[0]:
                        node2[0][word3] += 1
                    else:
                        node2[0][word3] = 1
                else:
                    node1[word2] = [{word3:1}, 1]
            idx +=1
    return result

def buildStory(tritable = {}):
    buffer = []
    recent = []
    word = random.choice(list(tritable))
    buffer.append(word)
    while len(buffer)<1000:
        if word in recent:
            word = random.choice(list(tritable))
        recent.append(word)
        max = 0
        word2 = ""
        node2 = tritable[word]
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
        while len(recent)>15:
            recent.pop(0)
    return buffer


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
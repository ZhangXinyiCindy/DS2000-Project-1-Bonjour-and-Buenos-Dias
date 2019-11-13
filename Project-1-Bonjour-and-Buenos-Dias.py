#read file as a single string
def readFileAsString(filename):
    file=open(filename)
    s=file.read()
    s=s.replace("\n"," ")
    return s

#clean the single string
#remove numbers and punctuation
#replace sequence of whitespace with a single space
#replace all uppercase letters with lowercase letters
def cleanString(s):
    e=""
    for i in range(len(s)-1):
        if (s[i].isalpha() or s[i]==" " and s[i+1]!=" "):
            e=e+s[i]
    if (s[len(s)-1].isalpha() or s[len(s)-2]!=" " and s[len(s)-1]==" "):
        e=e+s[len(s)-1]
    e=e.lower()
    return e

#taking a cleaned string as input
#make s dictionary with each trigram as keys and the times it appear as value
def countTri(e):
    Dict1={}
    for i in range(len(e)-3):
        if (e[i:i+3]  not in Dict1.keys()):
            Dict1[e[i:i+3]]=1
        if (e[i:i+3] in Dict1.keys()):
            Dict1[e[i:i+3]]=Dict1[e[i:i+3]]+1
    return Dict1

#take uncleaned single string
#make individual dictionary for each individual document
def individualDict(s):
    Dict=countTri(cleanString(s))
    return Dict

#loop each unknown documents with all languages
#call cosine function to calculate the similarity from them
#write it into a new file
def cosineLoop(languageDict,UnknownDict,Newfilename):
    file = open(Newfilename, 'w')
    for DictUnknown in UnknownDict.keys():
        file.write(str(DictUnknown)+'\n')
        for language in languageDict.keys():
            file.write(str(language)+" "+
                       str(cosine(languageDict[language],
                                  UnknownDict[DictUnknown]))+'\n')
    file.close()
    
#a is a language dictionary
#b is a individual unknown dictionary
#return cosine similarity of the unknown document with certain language
def cosine(a,b):
    numerator=0
    sumA=0
    sumB=0
    import math
    for key in b.keys():
        if key in a.keys():
            numerator=numerator+b[key]/sum(b.values())*a[key]/sum(a.values())
            sumB=sumB+b[key]/sum(b.values())*b[key]/sum(b.values())
            sumA=sumA+a[key]/sum(a.values())*a[key]/sum(a.values())
    denomenator=math.sqrt(sumA)*math.sqrt(sumB)                 
    return(numerator/denomenator)


#read the file of filenames
#build individual dictionary for each file
#combine individual dictionary from same language to make language dictionary
#build a big languageDict which is a dictionary of language dictionary
def getInput(filename):
    file= open(filename)
    languageDict={}
    for line in file:
        line=line.replace("\n","") 
        splitList=line.split()
        tri=individualDict(readFileAsString(line))
        if (splitList[0]!="Unknown" and splitList[0] not in languageDict.keys()):
            languageDict[splitList[0]]=tri
        if (splitList[0]!="Unknown" and splitList[0] in languageDict.keys()):
            languageDict[splitList[0]]=combineDict(tri,languageDict[splitList[0]])
    return languageDict

#read the file of filenames
#build individual dictionary for each unknown file
#build a big UnknownDict which is a dictionary of individual unknown dictionaries
def inputUnknown(filename):
    file= open(filename)
    UnknownDict={}
    for line in file:
        line=line.replace("\n","")
        splitList=line.split()
        if splitList[0]=="Unknown":
            tri=individualDict(readFileAsString(line))
            UnknownDict[splitList[1]]=tri
    return UnknownDict

#take in two dictionaries
#combine them into 1
def combineDict(Dict1, Dict2):
    for keys in Dict1.keys():
        if keys not in Dict2.keys():
            Dict2[keys]=Dict1[keys]
        if keys in Dict2.keys():
            Dict2[keys]=Dict1[keys]+Dict2[keys]
    return Dict2
            
#build languageDict which is a dictionary of dictionaries
#the key for languageDict is the name of different language
#the value of languageDict is the specific language dictionary 
#which is the combined the trigrams dictionary of all the source in that language
#build UnknownDict which is a dictionary of individual unknown dictionaries
#use cosine loop to anaylysis the similarity of 
#each individule unknown file with each language
#store the result in new file "similarity"
def main():
    Newfilename="similarity"
    languageDict=getInput("filename.txt")
    UnknownDict=inputUnknown("filename.txt")
    cosineLoop(languageDict,UnknownDict,Newfilename)
main()
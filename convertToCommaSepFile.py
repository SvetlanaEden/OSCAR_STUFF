
################################################################################
### Read file and create comma separated file, data.frame-like file for reading in R
################################################################################

#>>> l = ["0","1","9","A","B","Z","a","b","z"]
#>>> map(lambda x: ord(x), l)
#[48, 49, 57, 65, 66, 90, 97, 98, 122]

def getYearAndNumber(charStr):
  charSplt = charStr.split(" ")
  return (charSplt[0],charSplt[1][:-1])

def parceNominee(line, infoSep):
  songSep = " from "
  danceSep = [" number from ", " numbers from "]
  first = line.split(infoSep)[0]
  second = line.split(infoSep)[1]
  if second.find("{\"") != -1:
    name = first.strip()
    movie = second.split("{")[0].strip()
    roleOrSong = second[second.find("{\"")+2:second.find("\"}")]
  elif first[0] != "\"" and second[0] != "\"":
    name = second.strip()
    movie = first.strip()
    roleOrSong = ""
  elif first[0] == "\"":
    name = second.strip()
    indexOfSongSep = line.rfind(songSep)
    movie = first[indexOfSongSep+len(songSep):]
    roleOrSong = line[:indexOfSongSep].strip().replace("\"", "")
  elif second[0] == "\"":
    name = first.strip()
    indexOfDanceSep = max(second.rfind(danceSep[0]), second.rfind(danceSep[1]))
    length = (second.rfind(danceSep[0])>-1) * len(danceSep[0]) + (second.rfind(danceSep[1])>-1) * len(danceSep[1])
    movie = second[indexOfDanceSep+length:].strip()
    roleOrSong = second[:indexOfDanceSep].strip().replace("\"", "")
  return (name, movie, roleOrSong)
    

import os

#os.getcwd()
#os.system('mkdir today')

currFolderName = "/Users/svetlanaeden/Documents/GRADSCHOOL/2014_Fall/Robert/oscar/code"
dataInDirName = "../data/oscarByYear"
dataOutDirName = "../data"
#os.path.join(pathfile,"output","log.txt")
#os.remove(os.path.join(dataInDirName,".DS_Store"))

os.chdir(currFolderName)

fileList = os.listdir(dataInDirName)

categ = ""
winner = False
name = ""
movie = ""
roleOrSong = ""
note = ""
line=""
year=""
oscarNum=""
movieActSep = " -- "
cost = -1
rFileSep="\", \""

#fileList = ['oscar79.csv', 'oscar80.csv']
fileList = os.listdir(dataInDirName)
fw = open(os.path.join(dataOutDirName, "oscarDataInCommaSepForm.csv"), "w")
fw.write("\"movie\", \"categ\", \"winner\", \"name\", \"roleOrSong\", \"note\", \"year\", \"oscarNum\"\n")
for n in fileList:
  fr = open(os.path.join(dataInDirName, n), "r")
  line = fr.readline()
  while not line[0].isdigit():
    line = fr.readline()
  (year, oscarNum) = getYearAndNumber(line)
  #print lineCounter
  print "********************************* beginning of ", year, n
  readTheRest = True
  printYesNo = True
  lineCounter = 0
  while readTheRest and line:
    #print line[0:5], `winner`, movie, categ
    nextLine = fr.readline()
    if nextLine=="SPECIAL AWARD\n" or nextLine=="HONORARY AWARD\n":
      readTheRest=False
    ###----------------if the first word consists of capital letter with no " -- " it is a category
    if line.split(" ")[0].isupper() and (line[:-1]).split(" ")[0].isalpha() and line.find(movieActSep)==-1:
      categ = line[:-1]
    elif line.find(movieActSep)!=-1:
      (name, movie, roleOrSong) = parceNominee(line, movieActSep)
      #print line[0:5], `winner`, movie, categ
      #print (name, movie, roleOrSong)
      if nextLine[0:6] == "[NOTE:":
        note = nextLine[:-1]
      listToWrite = [movie, categ, `winner`, name, roleOrSong, note, year, oscarNum.strip()]
      listToWrite = map(lambda l, o=",", n=";": l.replace(o,n).strip(), listToWrite)
      lineToWrite = rFileSep.join(listToWrite)
      #print line[:-1]
      #print `winner`, "\t", movie, "\t", categ, "\t", name, "\t", roleOrSong
      lineToWrite = "\"" + lineToWrite + "\"\n"
      fw.write(lineToWrite)
      lineCounter += 1
      winner = False
      note = ""
    elif line=="*\t\n" and readTheRest:
      winner = True
    else:
      winner = False
    line = nextLine
  
  fr.close()

print lineCounter
fw.close()

################################################################################
### Replace all characters with code greater than nonASCII=128 with replStr="?"
################################################################################

nonASCII = 128
replStr = "?"
fileNameFrom = os.path.join(dataOutDirName, "oscarDataInCommaSepForm.csv")
fileNameTo = os.path.join(dataOutDirName, "oscarDataInCommaSepFormASCII.csv")
fr = open(fileNameFrom, "r")
fw = open(fileNameTo, "w")
line = fr.readline()
lineCount = 1
replStr = "?"
numOfReplChars = 0
badCharList = []
while line:
  # make a list of chars
  l = list(line)
  # convert char to int
  lo = map(lambda x: ord(x), l)
  # find all indices with value >=nonASCII
  loi = filter(lambda i, val=nonASCII, x=lo: x[i]>=val, range(len(lo)))
  for i in loi:
    numOfReplChars += 1
    badCharList.append(line[i])
    line = line.replace(line[i], replStr)
  fw.write(line)
  line = fr.readline()
  lineCount = lineCount+1

fr.close()
fw.close()

print numOfReplChars, " char. have been replaced\n"
print badCharList



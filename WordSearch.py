import re
In = input("Input file to read")
Out = input("File to output")
InFile = open("In", "r")
OutFile = open(Out, "w")
Text = InFile.read()
Text = Text.lower()
Text = re.sub(r'[^\w\s]', '', Text)
TextList = Text.split()
List = []
for i in TextList:
    if i not in List:
        List.append(i)
List.sort(key=str.lower)
Count = []
for i in List:
    Count.append(TextList.count(i))
for i, j in zip(List, Count):
    OutFile.write(i)
    OutFile.write(" ")
    OutFile.write(str(j))
    OutFile.write("\n")


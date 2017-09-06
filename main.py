#!/usr/bin/python3
import os
import copy

def snapList(bigString, n):
	return [bigString[i:min((i+n),(len(bigString)))] for i in range(0,len(bigString), n)];

def startsWith(line, char):
	if(len(line)==0):
		return False;
	if(line[0]==char):
		return True;
	else:
		return False;

def seqLineParse(line):
	both = line.split();
	return (both[0], both[-1]);

def extractAligned(filename):
	if(os.path.isfile(filename)==False):
		print("error: file not found");
		return([],[]);
	f = open(filename, "r");
	
	temp = "";
	seqNames = [];
	sequenceList = [];
	temp = f.readline();
	i = 0;
	#get past the initial text at the head of the .sto file
	while(startsWith(temp,'#') or temp.isspace()):
		temp = f.readline();
		if( (temp.isspace)==False and (temp=="" or temp[0]=='/')): 
			print("error: reached early end of file");
			return(seqNames, sequenceList);

	#this should be the first loop through all the sequence segments.
	while((temp.isspace())==False and startsWith(temp, '/')==False):
		seqNames.append(seqLineParse(temp)[0]);
		sequenceList.append(seqLineParse(temp)[1]);
		
		temp = f.readline();
	temp = f.readline(); #this should be at the section of sequence segments
	
	n= len(sequenceList);
	#this will loop through the rest of the file and build the full sequences together into the list.
	while((len(temp)>0) and startsWith(temp, '/')==False):
		while(temp.isspace()):
			temp = f.readline();
		
		for num in range(n):
			if(temp.isspace()):
				print("error: alignment traversal is off track at", num);
				return(seqNames, sequenceList);
			sequenceList[num] = sequenceList[num] + seqLineParse(temp)[1];
			temp = f.readline();
		temp = f.readline();
	f.close();
	return(seqNames, sequenceList);

def getEntropy(xList): #don't even that this the real version
	longness = len(xList[0]);
	return([12]*longness);

def findBlocks(scores, source):
	return[[200, 5],[213,6]];

def getBlocks(places, source):
	motList = [];
	currentMot = [];
	currentSeq = "";
	for mot in places:
		for sequence in source:
			currentSeq = sequence[mot[0]:(mot[0]+mot[1])];
			currentMot.append(currentSeq);
		motList.append(currentMot);
		currentMot = [];
		
	#return [["snake","shake","phake"],["killer","biller","tiller"]];
	return copy.deepcopy(motList);

def stoWriter(filename, coreList):
	#get the big header from the file
	header = ""; #does not include blank last line
	
	if(os.path.isfile(filename)==False):
		print("error: file not found");
		return([],[]);
	f = open(filename, "r");
	
	temp = "";
	temp = f.readline();
	header = header + temp;
	temp = f.readline();
	#get past the initial text at the head of the .sto file
	while(temp.isspace()):
		header = header + temp;
		if( (temp.isspace)==False and (temp=="" or temp[0]=='/')): 
			print("error: reached early end of file");
			return 0;
		temp = f.readline();
	while(startsWith(temp,'#')):
		header = header + temp;
		if( (temp.isspace)==False and (temp=="" or temp[0]=='/')): 
			print("error: reached early end of file");
			return 0;
		temp = f.readline();
	f.close();
	#we have the header now.
		
	#get the list of sequence names from the file
	seqNames = extractAligned(filename)[0];
	
	#declare blank name for our new file
	nextfile = "";
	curStep = 0; #this is literally just to make file names
	
	#declare blank list of other lines
	otherLines = [];
	
	#this number is how many chunks the sequences will have to be broken into
	#it will vary depending on the size of the sequences
	steps = 0;
	
	for motif in coreList:
		#generate a name for the file
		nextfile = filename[:len(filename)-4] + "_Mot" + str(curStep) + ".sto";
		#write new file
		fo = open(nextfile, "w")
		#add the header to the file
		fo.write(header);
		#generate list of other lines
		steps = len(snapList(motif[0], 50));
		for i in range(steps):
			otherLines.append("\n");
			for j in range(len(motif)):
				otherLines.append((seqNames[j].ljust(18, ' ')) + snapList(motif[j],50)[i]+"\n");
				#pull out the correct slice of our sequence and add it after the sequence name
		otherLines.append("//"+"\n");
		
		for line in otherLines:
			#append if to the file
			fo.write(line);
		otherLines = [];
		curStep=curStep+1;
		#clear filename
		nextfile = "";
		fo.close();
	



"""int main ( int argc, char *argv[] )
{
	std::vector<std::string> sequenceList;
	if(argc > 1)
		sequenceList = extractAligned(argv[1]);
	else
		sequenceList = extractAligned("PF06306_full_length_sequences.sto");
	//debug point. check the length of alignment. It should not be 0.

	std::cout << "We have this many seqNames: " << sequenceList.size() << std::endl;
	return 0;
}"""


def ourMain(originFile):
	sequenceList = extractAligned(originFile)[1];
	entScores = getEntropy(sequenceList);
	motLocs = findBlocks(entScores, sequenceList);
	cores = getBlocks(motLocs, sequenceList);
	stoWriter(originFile,cores);

ourMain("PF06306_full_length_sequences.sto");
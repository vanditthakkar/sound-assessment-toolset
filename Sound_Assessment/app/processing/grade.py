import process
import difflib
import pdb
import time
import json


indianNote = {'C#':'Sa','D#':'Re','F':'Ga','F#':'Ma','G#':'Pa','A#':'Dh','C':'Ni'}

def grade(filename1,filename2,id):
	file1 = filename1
	file2 = filename2



	fileObj1 = process.Process(file1)
	f1 = fileObj1.extractFeatures()
	fileObj2 = process.Process(file2)
	f2 = fileObj2.extractFeatures()
	diff = difflib.Differ()

	loudness1 = [loud for loud in fileObj1.getLoud()]
	loudness2 = [loud for loud in fileObj2.getLoud()]

	keys1 = [indianNote[i] for i in fileObj1.getKeys()]
	keys2 = [indianNote[i] for i in fileObj2.getKeys()]

	times1 = [float(time0) for time0 in fileObj1.getTime()]
	times2 = [float(time0) for time0 in fileObj1.getTime()]


	result = list(diff.compare(keys1,keys2))
	missed = []
	extra = []

	for i in result:
		if i.startswith('-'):
			missed.append(i[1:])	
		if i.startswith('+'):
			extra.append(i[1:])

	#print result
	#print "Missed : "+str(missed)
	#print "Extra : "+str(extra)


	results = {'loudness1':loudness1,'loudness2':loudness2,'keys1':keys1,'keys2':keys2,'times1':times1,'times2':times2}
	with open(str(id)+".json","w") as fp:
		json.dump(results,fp)


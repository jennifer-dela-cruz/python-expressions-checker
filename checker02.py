import subprocess
import glob
import sys

testCase = ['GIVEYOU! hello', 'GIVEYOU! "hello world"', 'GIVEYOU! "hello" #this prints hello', 'GIVEYOU! ", world."', 'GIVEYOU! "12.5"', 'GIVEYOU!       "yes       "', 'GIVEYOU! "NO!"           #"prints no"', 'GIVEYOU! "I am       very           sleepy"', 'GIVEYOU!! hello', 'GIVEYOU!! "hello world"', 'GIVEYOU!! "hello" #this prints hello', 'GIVEYOU!! ", world."', 'GIVEYOU!! "12.5"', 'GIVEYOU!!       "yes       "', 'GIVEYOU!! "NO!"           #"prints no"', 'GIVEYOU!! "I am       very           sleepy"', '#Heyow', 'PLUS 1 1','PLUS 4 5', 'PLUS 1.1 -1.1', 'PLUS 2 2 2', 'PLUS -10 +20', 'PLUS 0 0', 'PLUS -1 100000000000000000000000000000000000000', 'PLUS -100000000000000000000000000000000000000 1', 'MINUS 1 1', 'MINUS 4 5', 'MINUS 1.1 -1.1', 'MINUS 2 2 2', 'MINUS -10 +20', 'MINUS 0 0', 'MINUS -1 100000000000000000000000000000000000000', 'MINUS -100000000000000000000000000000000000000 1', 'TIMES 1 1', 'TIMES 4 5', 'TIMES 1.1 -1.1', 'TIMES 2 2 2', 'TIMES -10 +20', 'TIMES 0 0', 'TIMES -1 100000000000000000000000000000000000000', 'TIMES -100000000000000000000000000000000000000 1', 'DIVBY 1 1', 'DIVBY 4 5', 'DIVBY 1.1 -1.1', 'DIVBY 2 2 2', 'DIVBY -10 +20', 'DIVBY 0 0', 'DIVBY -1 100000000000000000000000000000000000000', 'DIVBY -100000000000000000000000000000000000000 1', 'MODU 1 1', 'MODU 4 5', 'MODU 1.1 -1.1', 'MODU 2 2 2', 'MODU -10 +20', 'MODU 0 0', 'MODU -1 100000000000000000000000000000000000000', 'MODU -100000000000000000000000000000000000000 1']

answerKey = ['Syntax is incorrect.\\n', 'hello world\\n', 'hello\\n', ', world.\\n', '12.5\\n', 'yes       \\n', 'NO!\\n', 'I am       very           sleepy\\n', 'Syntax is incorrect.\\n', 'hello world\\n\\n', 'hello\\n\\n', ', world.\\n\\n', '12.5\\n\\n', 'yes       \\n\\n', 'NO!\\n\\n', 'I am       very           sleepy\\n\\n', '\\n', '2\\n', '9\\n', 'Syntax is incorrect.\\n', 'Syntax is incorrect.\\n', '10\\n', '0\\n', '99999999999999999999999999999999999999\\n', '-99999999999999999999999999999999999999\\n', '0\\n', '-1\\n', 'Syntax is incorrect.\\n', 'Syntax is incorrect.\\n', '-30\\n', '0\\n', '-100000000000000000000000000000000000001\\n', '-100000000000000000000000000000000000001\\n', '1\\n', '20\\n', 'Syntax is incorrect.\\n', 'Syntax is incorrect.\\n', '-200\\n', '0\\n', '-100000000000000000000000000000000000000\\n', '-100000000000000000000000000000000000000\\n', '1\\n', '0\\n', 'Syntax is incorrect.\\n', 'Syntax is incorrect.\\n', '-1\\n', 'Error: Division by zero\\n', '-1\\n', '-100000000000000000000000000000000000000\\n', '0\\n', '4\\n', 'Syntax is incorrect.\\n', 'Syntax is incorrect.\\n', '10\\n', 'Error: Division by zero\\n', '99999999999999999999999999999999999999\\n', '0\\n']

noOfCases = len(testCase)

f = sys.argv[1]
i = 0
score = 0
outfile = f.replace(".py", ".txt")
out = open(outfile, "w")

for case in testCase:
	currCase = open("currCase", "w")
	currCase.write("CREATE\n" + case + "\nRUPTURE")
	currCase.close()

	try:
		command = 'python3 ' + f + '< currCase | grep -vi "Syntax correct\|INTERPOL\|CREATE\|RUPTURE\|Start\|Enter\|Exit\|Goodbye\|syntax checker\|BEGIN\|END"'
		output = subprocess.check_output(command, shell=True)


		#try to clean outputs
		strOutput = str(output).replace("b'$", "", 1)
		strOutput = strOutput.replace('b"$', "", 1)
		strOutput = strOutput.replace("b'", "", 1)
		strOutput = strOutput.replace('b"', "", 1)
		strOutput = strOutput.replace("$ \\n", "", 1)
		strOutput = strOutput.replace("\\n\\n\\n$  ", "", 1)
		strOutput = strOutput.replace("\\n'", "\\n").lstrip()
		if strOutput.find("\\n") == 0:
			strOutput = strOutput[2:]

		#print test cases and output
		outstr = "Test    Case: " + case + "\nYour  Answer: " + strOutput + "\nRight Answer: " + answerKey[i] + "\n\n"
		out.write(outstr)

		#if the your answer contains the correct answer, even though you have extra new lines, it is marked as correct
		#as long as you have the "incorrect" for the syntax is incorrect, it is marked as correct
		#as long as you have the "error" for the error, it is marked as correct
		#i even marked "none", "incorrect" "error" outputs for syntax errors and runtime errors. 
		ansKey = answerKey[i].lower()
		strOutput = strOutput.lower()

		if (strOutput.find(ansKey) > -1) or ( strOutput.find("none") > -1 and ansKey.find("incorrect") > -1 ) or (strOutput.find("incorrect") > -1 and ansKey.find("incorrect") > -1 ) or ( strOutput.find("error") > -1 and ansKey.find("error") > -1 ) or ( strOutput.find("error") > -1 and ansKey.find("incorrect") > -1 ) or ( strOutput.find("incorrect") > -1 and ansKey.find("error") > -1 ):
			score = score + 1

	except subprocess.CalledProcessError:
		strOutput = '\\n'
		if answerKey[i] == strOutput:
			score = score + 1
			outstr = "Test    Case: " + case + "\nYour  Answer: " + strOutput + "\nRight Answer: " + answerKey[i] + "\n\n"
			out.write(outstr)
			
	except:
		#this is when your program crashes
		out.write("Test    Case: " + case + "\n")
		out.write("Exception encountered.\n\n")

	
	print(case)
	print(outstr)
	i = i + 1

out.write("Score:\t" + str((score/(len(testCase))*100)))	
out.close()

'''
Ari, Aureliano, and Joe
2/10/22
Reflection: After we submitted the project plan and started working on making
a Braille dictionary for our project, we noticed the large amount of shorthand characters
in Braille, so we decided to use a library called pybrl. Pybrl can be found at https://github.com/ant0nisk/pybrl.
We changed this benchmark to be making a picture of the Braille, which can then be used to turn into
a 3d model. This part of the code went pretty smoothly, and we didn't have many issues.
Sources: Source #1: Pybrl library: https://github.com/ant0nisk/pybrl - Used to convert English to Braille
OMH
'''
import pybrl as brl  #Source #1
from PIL import Image
from dataclasses import dataclass
import os, sys

braillePoints = open("braillePoints.txt", 'w')


@dataclass
class Preferences:
    plateWidth : float
    plateLength : float
    plateHeight : float
    brailleScale : float

current_dir = os.path.dirname(os.path.abspath(__file__))  #This file path navigation is from ChatGPT

# Navigate up two levels to the parent directory
parent_dir = os.path.join(current_dir, "..", "..")  

# Path to the text file in the Website folder
text_file_path = os.path.join(parent_dir, "Website", "Preferences.txt")


with open(text_file_path, 'r') as prefs:
    for i, line in enumerate(prefs):
        try:
            line = int(line[:-1])
        except:
            line = 0

        if i == 0:
            firstPref = line * 10
        if i == 1:
            secPref = line * 10
        if i == 2:
            thrPref = line
    p = Preferences(firstPref, secPref, thrPref, 2)


def makeBrailleImage(string): # baseWidth, baseLength, baseHeight, brailleHeight
	current_dir = os.path.dirname(os.path.abspath(__file__))
	# print(current_dir)
	braillePoints = open("braillePoints.txt", 'w')
	
	current_dir = os.path.dirname(os.path.abspath(__file__))  #This file path navigation is from ChatGPT

	# Navigate up two levels to the parent directory
	parent_dir = os.path.join(current_dir, "..", "..")  

	# Path to the text file in the Website folder
	text_file_path = os.path.join(parent_dir, "Website", "Preferences.txt")
	
	
	with open(text_file_path, 'r') as prefs: #Gets preferences from user
		for i, line in enumerate(prefs):
			try:
				line = int(line[:-1])
			except:
				line = 0

			if i == 0:
				firstPref = line * 10
			if i == 1:
				secPref = line * 10
			if i == 2:
				thrPref = line
		p = Preferences(firstPref, secPref, thrPref, 2)

	current_dir = os.path.dirname(os.path.abspath(__file__))
	print(current_dir)
	braillePoints = open("braillePoints.txt", 'w')

	# plateWidth = 10
	dimx, dimy = (p.plateWidth * 10), 10000

	fontColor = (255, 255, 255)
	bgColor = (39, 42, 46)
	brailleImg = Image.new("RGB", (dimx, dimy), bgColor)  #Size of image
	# brailleImg.show()


	# string = "Braille Translator" #This will later be the users input from the app

	brailleNum = brl.translate(string)  #Source #1 - This converts the inputted string into a list of the Braille characters in 6 digit binary.
	finalBrailleNum = []

	for spot in brailleNum:  #This goes through all of the words and adds a space at the end so that it is easier to see/feel the division of words
		spot.append('000000')
		finalBrailleNum.append(spot)

	xstart, ystart = 30, 30  #This is just where we start to draw the Braille eon our image
	xline, yline = xstart, ystart
	longX, newLongX = xstart, False

	for spot in finalBrailleNum:  #Each word
			
		for letter in spot:  #Each letter
			index = 0
			addedHun = False
			
			for num in letter:  #Each binary
				
				index += 1
				num = int(num)  #The number is originally in a string, so we have to convert it to an int
				
				if num == 1:  #The number is one if it is a dot that must be printed
					
					for y in range(-3, 4):
						for x in range(-3, 4):  #This goes through a 3x3 square around a pixel
							
							if xline + 15 > dimx-20:
								ystart += 100  #Adds 100 pixels between each line
								addedHun = True
								yline = ystart
								if xline > longX:
									longX = xline
									
								xline = xstart
								
								try:
									brailleImg.putpixel((xline + x, yline + y), fontColor)

									# print(xline+x, yline+y)
									if y == 0 and x == 0: #These two if statements write the center points of the Braille to a file, so that these points can then be used to make the 3d model. For some reason, there needs to be both methods of putting the points in the file, but without both, it doesn't work
										with open("braillePoints.txt", 'w') as file:
											file.write(f"{xline + x} {yline+y} {index}\n")
									if y == 0 and x == 0:
										braillePoints.write(f"{xline + x} {yline + y} {index}\n")
										
								except IndexError:
									continue

							else:
								
								try:
									brailleImg.putpixel((xline + x, yline + y), fontColor)

									if y == 0 and x == 0:  #These two if statements write the center points of the Braille to a file, so that these points can then be used to make the 3d model. For some reason, there needs to be both methods of putting the points in the file, but without both, it doesn't work
										with open("braillePoints.txt", 'w') as file:
											file.write(f"{xline + x} {yline+y} {index}\n")
									if y == 0 and x == 0:
										braillePoints.write(f"{xline + x} {yline + y} {index}\n")

								except IndexError:
									continue
							# except:  #If we are trying to put a dot outside of the range of the image, it starts a new line
								

				if not addedHun:
					yline += 20  #This makes adds a 15 pixel margin between each dot or blank dot
				if yline - ystart >= 59:  #If the y has already been increased 3 times, it returns back to the top to start the next column of dots
					yline = ystart
					xline += 20  #Makes space for the next column in the letter
			xline += 20 #Adds space between each letter

		ystart = yline


	if longX < 200:
		longX = 200
	# print(ystart+100)
	dim = (0, 0, dimx, ystart + 100)

	FinalBrailleImage = brailleImg.crop(dim) #Crops the image to the right dimension to fit with the user's preferences
	# FinalBrailleImage.show()
	return FinalBrailleImage

makeBrailleImage("Hello")

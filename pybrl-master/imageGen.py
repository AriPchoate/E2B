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
import numpy as np
import matplotlib.pyplot as plt

def makeBrailleImage(string): # baseWidth, baseLength, baseHeight, brailleHeight
	dimx, dimy = 1000, 1000
	# dimx, dimy = int(baseLength) * 10, int(baseWidth) * 10

	fontColor = (255, 255, 255)
	bgColor = (39, 42, 46)
	brailleImg = Image.new("RGB", (dimx, dimy), bgColor)  #Size of image


	# string = "Braille Translator" #This will later be the users input from the app

	brailleNum = brl.translate(string)  #Source #1 - This converts the inputted string into a list of the Braille characters in 6 digit binary.
	finalBrailleNum = []

	for spot in brailleNum:  #This goes through all of the words and adds a space at the end so that it is easier to see/feel the division of words
		spot.append('000000')
		finalBrailleNum.append(spot)

	# print(finalBrailleNum)
	xstart, ystart = 30, 30  #This is just where we start to draw the Braille eon our image
	xline, yline = xstart, ystart
	longX, newLongX = xstart, False



	for spot in finalBrailleNum:  #Each word
		lengthWord = len(spot)	
		for letter in spot:  #Each letter
			for num in letter:  #Each binary
				num = int(num)  #The number is originally in a string, so we have to convert it to an int
				if num == 1:  #The number is one if it is a dot that must be printed
					for y in range(-3, 4):
						for x in range(-3, 4):  #This goes through a 3x3 square around a pixel
							if (lengthWord * 25) + xline + 3 > 1000:  #This checks to see if a new line has to be started. This if statement isn't perfect yet and has to be revised for the final image creation, but it is close to being good
								ystart += 100  #Adds 100 pixels between each line
								yline = ystart
								if xline > longX:
									longX = xline
									newLongX = True
									print(xline, longX)
								xline = xstart
								try:
									brailleImg.putpixel((xline + x, yline + y), fontColor)
								except IndexError:
									continue
							else:
								try:
									brailleImg.putpixel((xline + x, yline + y), fontColor)
								except IndexError:
									continue
							# except:  #If we are trying to put a dot outside of the range of the image, it starts a new line
								

				yline += 15  #This makes adds a 15 pixel margin between each dot or blank dot
				if yline - ystart >= 44:  #If the y has already been increased 3 times, it returns back to the top to start the next column of dots
					yline = ystart
					xline += 15  #Makes space for the next column in the letter
			xline += 10 #Adds space between each letter

		ystart = yline

	if newLongX == False:
		longX = xline
	if longX < 300:
		longX = 300

	dim = (0, 0, longX + 20, ystart + 100)

	FinalBrailleImage = brailleImg.crop(dim)	
	# FinalBrailleImage.show()
	# FinalBrailleImage.save("output.png", format="PNG")
	return FinalBrailleImage

# makeBrailleImage("Hello", 100, 100, 1, 1)

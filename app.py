'''
Ari, Aureliano, and Joe
This part of the website is the main section that controls the website and the backend code. This part was quite difficult to get up and running, but once we understood the basic principles of Flask, the coding went quite smoothly and efficiently.

Overall Project Reflection: This project went quite well. Throughout the entire process, the coding went smoothly and we did not have too many major bugs. Once we figured out how to implement Flask properly into the html, it was quite smooth to set up the website. Once we had the website working, we worked on making a Braille image. Making the image was not too complicated. We then worked on making a 3d model of the Braille. The model took a quite a bit to code and generally figure out how to make 3d models in python. Our first iteration of the 3d model had square Braille, but we later made the Braille semi-spheres like actual Braille. We wanted to make the 3d Braille according to standards, but the way that we were generating where to put the 3d spheres on the image was coded too early in the project and far too implemented to change the Braille to standardized sizing. This is one area that we can improve on if we were to continue working on this project. This project came out just as we originally invisioned it to do so. We worked very hard to meet the our original plan, and we think that this came out very well. It also fits well with social justice. From our calculations, if one make a 10cm x 10cm base plate with Braille, it would only cost 42 cents. After the inital cost of a 3d printer, it is very affordable for anyone to implement Braille into their office/company to increase accessibility.

Sources: https://flask.palletsprojects.com/en/3.0.x/ - This source was used to figure make html compatible with python through Flask. The coding principles from this source are scattered around the entirety of the code because of the specificity of important commands.
ChatGPT was used to go through the Flask documentation and pull out all of the major/important lines that are needed to make Flask work and communicate with the html.

Required imports across the entire project:

colorama
dataclasses
pillow
trimesh
pyrender

All other modules, such as pybrl, are downloaded through the GitHub repository.

'''


# ******* this is the link to be able to run the website: http://localhost:5000/translate *********
# app.py has to be run in terminal to build the site. Liveview doesn't work

from flask import Flask, render_template, request
print("1/4")
import sys, os
from colorama import Fore
print("2/4")
import modelGenerator
print("3/4")

directory = 'pybrl-master'
full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), directory))
sys.path.append(full_path)
import imageGen as picMaker
print("4/4")

isWindows = True

app = Flask(__name__,  subdomain_matching=True)  #Makes the website
# app.config['SCRIPT_NAME'] = '/translate'

print(Fore.GREEN + "Website Domain: http://localhost:5000/translate" + Fore.RESET)  #


print("Imports complete")

@app.route('/translate', methods=['GET', 'POST'])

def translate():  #This is the main website page
    text_from_form = request.form.get('userText')  #Gets the user's text
    if text_from_form == None:
        text_from_form = ""
    
    with open("userInputs.txt", 'a') as file:  #We append the user's input to a file to make sure that the user's input is properly received and read
        file.write(text_from_form + "\n")

    # print(text_from_form)
    if request.method == 'POST':  #This just means that the user did something on the page, which triggers 'POST'
        

        baseWidth, baseLength, baseHeight = request.form['baseWidth'], request.form['baseLength'], request.form['baseHeight']  #Gets preferences from the website

        try:  #Making sure the user put in integers and not too small of numbers
            i = int(baseWidth)
            j = int(baseLength)
            h = int(baseHeight)
            if i < 3 or j < 3 or h < 2:
                return render_template('translate.html')

        except:
            print(Fore.GREEN + "Please enter only integers into the preferences and greater than or equal to 3" + Fore.RESET)
            return render_template('translate.html')

        with open("Preferences.txt", 'w') as file:  #Writes the user's preferences to a file to be then extracted in other python
            file.write(f"{baseWidth}\n{baseLength}\n{baseHeight}\n")
        
        if request.form.get('Convert') == 'Convert':  #If the Convert button is pressed
            BrailleImage = picMaker.makeBrailleImage(text_from_form)  #Makes the braille image
            
            rootDirectory = os.getcwd()  #These next few lines makes the proper file path to save the Braille image

            # if isWindows == False:
            #     folderPath = os.path.join(rootDirectory, 'static', 'images', 'BrailleImage.png')  #This for Mac
            # else:
            #     folderPath = os.path.join(rootDirectory, 'Website', 'static', 'images', 'BrailleImage.png')  #This for Windows
            
            folderPath = os.path.join(rootDirectory, 'static', 'images', 'BrailleImage.png')

            BrailleImage.save(folderPath, format="PNG")
            modelGenerator.generateBraille()  #Creates the 3d model
            
    elif request.method == 'GET':
        print("No Post Back Call")

    return render_template('translate.html')  #Outputs the website

app.add_url_rule('/translate', 'translate', translate, methods=['GET', 'POST'])

@app.route('/about')
def about():  #About page - there is no logic, so it just returns the page
    return render_template('about.html')

@app.route('/directions')
def directions():  #Directions page - there is no logic, so it just returns the page
    return render_template('directions.html')

if __name__ == '__main__':  #Runs the website
    app.run(debug=True, host='0.0.0.0', port=5000)
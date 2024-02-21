# ******* this is the link to be able to run the website: http://localhost:5000/translate *********
# app.py has to be run in terminal to build the site. Liveview doesn't work unfortunately
from flask import Flask, render_template, request
print("1/4")
import sys, os
print("2/4")
import modelGenerator
print("3/4")
import modelImageGen  #If there is an error with importing this, just comment this line and line 39

directory = 'pybrl-master'
full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), directory))
sys.path.append(full_path)
# print(full_path)
import imageGen as picMaker
print("4/4")

app = Flask(__name__)

print("Imports complete")

@app.route('/translate', methods=['GET', 'POST'])

def translate():

    text_from_form = request.form.get('userText')
    # print(text_from_form)
    if request.method == 'POST':
        baseWidth, baseLength, baseHeight, brailleHeight = request.form['baseWidth'], request.form['baseLength'], request.form['baseHeight'], request.form['brailleHeight']
        with open("Preferences.txt", 'w') as file:
            file.write(f"{baseWidth}\n{baseLength}\n{baseHeight}\n{brailleHeight}\n")
        
        if request.form.get('Convert') == 'Convert':
            BrailleImage = picMaker.makeBrailleImage(text_from_form)
            #, baseWidth, baseLength, baseHeight, brailleHeight
            rootDirectory = os.getcwd()

            folderPath = os.path.join(rootDirectory, 'static', 'images', 'BrailleImage.png')  #This for Mac
            # folderPath = os.path.join(rootDirectory, 'Website', 'static', 'images', 'BrailleImage.png')  #This for Windows

            BrailleImage.save(folderPath, format="PNG")
            modelGenerator.generateBraille()
            
            modelImageGen.main()
            print("stuff")
    
        elif request.form.get('Download 3D Model') == 'Download 3D Model':
            print("hola")
        else:
            print("Other Actions")

    elif request.method == 'GET':
        print("No Post Back Call")

    return render_template('translate.html')

app.add_url_rule('/translate', 'translate', translate, methods=['GET', 'POST'])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/directions')
def directions():
    return render_template('directions.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
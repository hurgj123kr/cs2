from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import colorize



application = Flask(__name__)

@application.route('/')
def home():
        return render_template('home.html')

@application.route('/user_get')
def user_get():
        return render_template('user_get.html')

@application.route('/result', methods=['GET', 'POST'])
def upload_file():
        if request.method == 'POST':
                #User Image
                user_img = request.files['user_img']
                user_img.save('./static/images/'+str(user_img.filename))
                user_img_path = './static/images/'+str(user_img.filename)

                #result image
                black_image, colorize_image = colorize.main(user_img_path)
                black_image_path =  black_image
                colorize_image_path = colorize_image
                
        return render_template('result.html', user_img= user_img_path,black_image=black_image_path,colorize_image=colorize_image_path)

if __name__ == "__main__":
        application.run(debug=True)




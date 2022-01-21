from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import colorize



application = Flask(__name__)

@application.route('/')
def home():
        return render_template('home.html')

@application.route('/user_get')
def user_get():
        return render_template('user_get.html')

def allowed_file(filename):
        ALLOWED_EXTENSIONS = 'jpg'
        return '.' in filename and \
                filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/result', methods=['GET', 'POST'])
def upload_file():
        if request.method == 'POST':
                if 'file' not in request.files:
                        return redirect(request.url)
                #User Image
                user_img = request.files['user_img']
                if user_img and allowed_file(user_img.filename):  

                        user_img.save('./static/images/'+str(user_img.filename))
                        user_img_path = './static/images/'+str(user_img.filename)

                        #result image
                        black_image, colorize_image = colorize.main(user_img_path)
                        black_image_path =  black_image
                        colorize_image_path = colorize_image
                        return render_template('result.html', user_img= user_img_path,black_image=black_image_path,colorize_image=colorize_image_path)
        return render_template('user_get.html')


if __name__ == "__main__":
        application.run(debug=True,host='0.0.0.0')




from flask import Flask, request, render_template, send_file
from openssl import issue_cert


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
#app.config['ALLOWED_EXTENSIONS'] = set(['xml'])


@app.route('/register', methods=['get', 'post'])
def sign():
    if request.method == 'POST':

        req = request.files['req_file']

        f = open('req.pem', 'w+')
        f.write(req.read())
        f.flush()

        issue_cert('req.pem')

        response = send_file('cert.pem', attachment_filename='cert.pem')
        response.headers.add('filename', 'cert.pem')
        response.headers.add('Content-Disposition', 'attachment')
        return response
    else:
        return render_template('registration.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

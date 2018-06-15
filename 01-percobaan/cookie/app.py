from flask import Flask, render_template, make_response, request

app = Flask(__name__)

@app.route('/')
def index():
    nilaiCookie = 100
    respon = make_response(render_template('index.html'))
    respon.set_cookie('makecookie', str(nilaiCookie))
    return respon

@app.route('/halaman1')
def halaman1():
    var = request.cookies.get('makecookie')
    return render_template('halaman1.html', var=var)

@app.route('/halaman2')
def halaman2():
    var = request.cookies.get('makecookie')
    return render_template('halaman2.html', var=var)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

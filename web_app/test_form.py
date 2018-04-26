from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
      number_1 = request.form['ANGKA1']
      number_2= request.form['ANGKA2']
      hasil = int(number_1) * int(number_2)

      # hasil = '%d %d' % (number_1, number_2)
      return render_template('response.html', HASIL=hasil)
   return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)







from flask import Flask, render_template

app = Flask(__name__, 
           static_folder='app/static',
           template_folder='app/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/combos')
def combos():
    return render_template('combos.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(debug=True)
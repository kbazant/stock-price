import os
import yfinance as yf
from flask import Flask, redirect, render_template, request, send_from_directory, url_for

app = Flask(__name__)

@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/price', methods=['POST'])
def price():
    ticker = request.form.get('ticker')

    if ticker:
        print('Request for price page received with ticker=%s' % ticker)
        try:
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d")['Close'][0]
            price = round(price, 2)  # Round the price to two decimal places
            return render_template('price.html', ticker=ticker, price=price)
        except Exception as e:
            print(f"Error retrieving stock price: {e}")
            error_message = "There was an error retrieving the stock price. Please try again."
            return render_template('index.html', error_message=error_message)
    else:
        print('Request for price page received with no ticker or blank ticker -- redirecting')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
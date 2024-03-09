from flask import Flask, render_template, jsonify, request
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' before importing pyplot

app = Flask(__name__)

# Define a list of Nifty symbols (you might fetch this from Yahoo Finance)
nifty_symbols = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'HINDUNILVR.NS', 'INFY.NS',
    'ITC.NS', 'SBIN.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'LT.NS',
    'BAJAJFINSV.NS', 'BHARTIARTL.NS', 'ASIANPAINT.NS', 'MARUTI.NS',
    'HDFC.NS', 'WIPRO.NS', 'AXISBANK.NS', 'HCLTECH.NS', 'NESTLEIND.NS',
    'ONGC.NS', 'BAJAJ-AUTO.NS', 'SUNPHARMA.NS', 'COALINDIA.NS', 'M&M.NS',
    'INDUSINDBK.NS', 'ULTRACEMCO.NS', 'POWERGRID.NS', 'IOC.NS', 'TATAMOTORS.NS',
    'BAJFINANCE.NS', 'SHREECEM.NS', 'NTPC.NS', 'HEROMOTOCO.NS', 'CIPLA.NS',
    'TITAN.NS', 'DRREDDY.NS', 'SBILIFE.NS', 'DIVISLAB.NS', 'GRASIM.NS',
    'UBL.NS', 'BRITANNIA.NS', 'ADANIPORTS.NS', 'JSWSTEEL.NS', 'BAJAJHLDNG.NS',
    'TECHM.NS', 'HINDALCO.NS', 'UPL.NS', 'TATASTEEL.NS', 'IOC.NS',
    'PIDILITIND.NS', 'AUROPHARMA.NS', 'HDFCLIFE.NS', 'BPCL.NS', 'GAIL.NS',
    'NTPC.NS', 'ICICIGI.NS', 'DLF.NS', 'BIOCON.NS', 'PNB.NS',
    'NMDC.NS', 'TVSMOTOR.NS', 'ADANIGREEN.NS', 'BANDHANBNK.NS', 'INDIGO.NS',
    'IBULHSGFIN.NS', 'ADANITRANS.NS', 'GODREJCP.NS', 'LICHSGFIN.NS', 'INDIAMART.NS',
    'MOTHERSUMI.NS', 'GODREJPROP.NS', 'ICICIPRULI.NS', 'MRF.NS', 'SAIL.NS',
    'RAMCOCEM.NS', 'BHEL.NS', 'ACC.NS', 'AUROPHARMA.NS', 'BALKRISIND.NS',
    'GODREJIND.NS', 'LTI.NS', 'HINDZINC.NS', 'CADILAHC.NS', 'TORNTPOWER.NS',
    'HDFCAMC.NS', 'UBL.NS', 'UBL.NS', 'NMDC.NS', 'COLPAL.NS',
    'OFSS.NS', 'PAGEIND.NS', 'MUTHOOTFIN.NS', 'DABUR.NS', 'SIEMENS.NS',
    'CONCOR.NS', 'L&TFH.NS', 'APOLLOHOSP.NS', 'DLF.NS', 'RECLTD.NS',
    'SRTRANSFIN.NS', 'BANDHANBNK.NS', 'BIOCON.NS', 'IDFCFIRSTB.NS', 'BAJAJELEC.NS',
    'BHEL.NS', 'GLENMARK.NS', 'CUMMINSIND.NS', 'ADANIENT.NS', 'PNB.NS'
]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pairtrade')
def pairtrade():
    return render_template('pairtrade.html')

@app.route('/get_nifty_symbols')
def get_nifty_symbols():
    return jsonify({'symbols': nifty_symbols})
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Handle form submission from contact.html
@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    # Process the form submission (e.g., send email, save to database, etc.)
    # This is just a placeholder
    
    return render_template('contact_confirmation.html', name=name)

@app.route('/analyze', methods=['POST'])

def analyze():
    symbol1 = request.form['symbol1']
    symbol2 = request.form['symbol2']
    
    # Download historical data for the selected symbols
    stock1 = yf.Ticker(symbol1)
    stock2 = yf.Ticker(symbol2)
    data1 = stock1.history(period="1y")
    data2 = stock2.history(period="1y")
    
    # Plot individual stock prices
    plt.figure(figsize=(10, 6))
    plt.plot(data1['Close'], label=symbol1)
    plt.plot(data2['Close'], label=symbol2)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Prices')
    plt.legend()
    stock_prices_path = 'static/stock_prices.png'
    plt.savefig(stock_prices_path)
    plt.close()  # Close the plot to prevent memory leaks
    
    # Calculate spread difference
    spread_diff = data1['Close'] - data2['Close']
    
    # Plot spread difference
    plt.figure(figsize=(10, 6))
    plt.plot(spread_diff, label='Spread Difference')
    plt.xlabel('Date')
    plt.ylabel('Spread Difference')
    plt.title('Spread Difference')
    plt.legend()
    spread_diff_path = 'static/spread_difference.png'
    plt.savefig(spread_diff_path)
    plt.close()  # Close the plot to prevent memory leaks
    
    # Calculate z-score
    zscore = (spread_diff - np.mean(spread_diff)) / np.std(spread_diff)
    
    # Plot z-score
    plt.figure(figsize=(10, 6))
    plt.plot(zscore, label='Z-Score')
    plt.xlabel('Date')
    plt.ylabel('Z-Score')
    plt.title('Z-Score')
    plt.legend()
    zscore_path = 'static/zscore.png'
    plt.savefig(zscore_path)
    plt.close()  # Close the plot to prevent memory leaks
    
    return render_template('result.html', stock_prices_path=stock_prices_path,
                           spread_diff_path=spread_diff_path, zscore_path=zscore_path)

if __name__ == '__main__':
    app.run(debug=True)
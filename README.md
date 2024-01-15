# This is a dashboard that aggregates your trading data from BinanceUS using the BinanceUS API.

There are a few things you need to do to set up your environment to run this. It can be run from the terminal or on a web browser (preferred).

## Step 1: Download this repo
- Download this repository as a zip, extract it, and place it in a folder with the name of your choice (we'll call this myRepoDir for the sake of this tutorial).

## Step 2: Downloading Python, npm, and Installing pip
1. Download and install Python 3:

You will need to have a terminal open (these directions will only be described for Linux terminals (Mac)

Mac:
Download the latest Python 3 installer from https://www.python.org/downloads/macos/
Run the installer and follow the prompts.
Windows:
Download the latest Python 3 installer from https://www.python.org/downloads/windows/
Run the installer, choose "Add Python 3.x to PATH", and complete the installation.

2. Install npm:

Mac:
Check if npm is already installed: npm -v
If not, install Node.js (which includes npm): https://nodejs.org/en/download/
Windows:
Download and install Node.js from https://nodejs.org/en/download/

3. Install pip:

Python 3.4 and later: pip is usually included. Check with pip -V.

If pip is not installed:
Download get-pip.py from https://bootstrap.pypa.io/get-pip.py
Run python3 get-pip.py

## Step 3: Install Flask (Flask is a Python server)
- Install Flask through pip ```pip install Flask``` use ```pip3 install Flask``` if that doesn't work

## Step 4: Make changes to the source code to get your API information
- Change these lines in myRepoDir/binanceus/BinanceUSCostBasis.py (lines 13, 14, and 17) to match your public and private API keys, as well as set your starting date.

## Step 5: Start the Flask server
- Start the Flask server by running this command while you are in (myRepoDir) ```python3 CryptoCostBasisApp.py```
- You may need to install all of the imports in myRepoDir/binanceus/BinanceUSCostBasis.py before running; errors should tell you this.
- This will run your code in the terminal twice (yes, this can be run from the terminal), and it will start your server on your localhost (127.0.0.1) on port 5000.

## Step 6: Go to your browser to view the dashboard
- In your browser, type http://127.0.0.1:5000/
- This is where your dashboard is being hosted locally

## Notes:
The dashboard is meant to be able to allow you to make educated decisions in your crypto trading. It shows the amount of money that you personally have in the trade, as well as your profit/loss percentage.
The dashboard will show every crypto that you hold currently in your account. Depending on the date you select to start tracking from, the trades will be aggregated on those pairs (USDT pairs only).
Coins that were not traded since the start date, will only show the current price of those coins.
Pairs in green are in profit, pairs in red are at a loss. The number next to the crypto name is the percentage of profit (green) or loss (red).

## Troubleshooting:
If you get this error below when starting the server (i.e. when you type ```python3 CryptoCostBasisApp.py```)
```
Address already in use
Port 5000 is in use by another program. Either identify and stop that program, or start the server with a different port.
On macOS, try disabling the 'AirPlay Receiver' service from System Preferences -> General -> AirDrop & Handoff.
```
Do this:
First, type: ```lsof -i :5000``` then take all of the PID numbers that are listed (there should be 3 with 1 duplicate) and run this command: ```kill -9 <PID>``` do that until ```lsof -i :5000``` returns nothing.
Then run ```python3 CryptoCostBasisApp.py``` again and go to http://127.0.0.1:5000/ in your browser.

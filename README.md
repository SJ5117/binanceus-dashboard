**This is a dashboard that aggregates your trading data from BinanceUS using the BinanceUS API.**

There are a few things you need to do to set up your environment to run this. It can be run from the terminal or on a web browser (preferred).

Step 1:
- Download this repository as a zip, extract it, and place it in a folder with the name of your choice.

Step 2:
- You will need to have a terminal open (these directions will only be described for Linux terminals (Mac), I'm sure Windows terminals are possible.
- Download Python...
- Install npm
- Install pip In your new repo directory (repoDir), install pip by running '

Step 3:
- Install Flask through npm


The dashboard is meant to be able to allow you to make educated decisions in your crypto trading. It shows the amount of money that you personally have in the trade, as well as your profit/loss percentage.
The dashboard will show every crypto that you hold currently in your account. Depending on the date you select to start tracking from, the trades will be aggregated on those pairs (USDT pairs only).
Coins that were not traded since the start date, will only show the current price of those coins.
Pairs in green are in profit, pairs in red are at a loss. The number next to the crypto name is the percentage of profit (green) or loss (red).

Go to http://127.0.0.1:5000/ in your browser
Troubleshooting if you get an error that says a server is already running on port 5000
- lsof 5000
- kill -9 50690

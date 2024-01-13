function updateBinanceUSData(data) {
    for (let pair of data) {
        const pairDiv = document.createElement("div");
        
        let pctDiff = Math.abs((((pair.price - pair.average_buy_price) / pair.average_buy_price)) * 100);
        if (pctDiff == 'Infinity') { pctDiff = 'N/A' }
        
        pairDiv.classList.add("module");
        pairDiv.innerHTML = `<div class="module-header">
                            <h3>${pair.pair}</h3>
                            <p>${parseFloat(pctDiff).toFixed(2)}</p>
                            </div>
                            <p>Current Price: ${parseFloat(pair.price).toFixed(8)}</p>
                            <p>Average Buy Price: ${parseFloat(pair.average_buy_price).toFixed(8)}</p>
                            <p>Average Sell Price: ${parseFloat(pair.average_sell_price).toFixed(8)}</p>
                            <p>Total Amount Spent: ${parseFloat(pair.total_amount_spent).toFixed(2)}</p>
                            <p>Total Amount Sold: ${parseFloat(pair.total_amount_sold).toFixed(2)}</p>
                            <p>Personal Money Left: ${parseFloat(pair.personal_money_left).toFixed(2)}</p>`;

        if (pair.price < pair.average_buy_price) {
            pairDiv.classList.add("pairLoss");
        }
        else pairDiv.classList.add("pairProfit");

        document.getElementById("app").appendChild(pairDiv);
    }
}

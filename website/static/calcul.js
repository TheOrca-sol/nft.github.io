function deleteTrade(tradeId){
    fetch("/delete-trade",{
        method : 'POST',
        body: JSON.stringify({tradeId:tradeId})
    }).then((_res) =>{
        window.location.href="/";
    });
}
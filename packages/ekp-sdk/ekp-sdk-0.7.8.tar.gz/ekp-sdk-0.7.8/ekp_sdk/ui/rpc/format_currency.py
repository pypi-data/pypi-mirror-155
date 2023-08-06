def format_currency(rpc, symbol):
    return {
        "method": "formatCurrency",
        "params": [rpc, symbol]
    }

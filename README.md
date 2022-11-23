# ig API

[![PyPI](https://img.shields.io/pypi/v/igapi)](https://pypi.org/project/igapi/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/igapi)](https://pypistats.org/packages/igapi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/igapi)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/igapi)
![GitHub contributors](https://img.shields.io/github/contributors/Iceloof/IG-API)
![GitHub issues](https://img.shields.io/github/issues-raw/Iceloof/IG-API)
![GitHub Action](https://github.com/Iceloof/IG-API/workflows/GitHub%20Action/badge.svg)
![GitHub](https://img.shields.io/github/license/Iceloof/IG-API)

## Install
```
pip install igapi
```
or
```
pip install --upgrade igapi
```
## Usage
- Initializing
```
import igapi
ig = igapi.IG(apikey, username, password, account, acc_type)
```
- Check version
```
print(ig.getVersion())
```
- login
```
ig.login()
```
- Get account information
```
account = ig.account()
```
- Get account balance
```
ig.getBalance()
```
or
```
ig.getBalance(account)
```
- Get account available balance
```
ig.getAvailable()
```
or
```
ig.getAvailable(account)
```
- Get account deposit
```
ig.getDeposit()
```
or
```
ig.getDeposit(account)
```
- Get account getProfitLoss
```
ig.getProfitLoss()
```
or
```
ig.getProfitLoss(account)
```
- Get watchlists
```
watchlists = ig.watchlists()
```
- Get specific watchlist
```
watchlist = ig.watchlist(id)
```
- Get account transactions
```
transactions = ig.getAccountTransactions()
```
- Get account activities
```
activities = ig.getAccountActivities()
```
- Get price
```
price = ig.getPrice(epic, [resolution], [numPoints])
```
- Get prices
```
prices = ig.getPrices(epic, [resolution], [numPoints],[start],[end])
```
- Get open positions
```
positions = ig.getOpenPosition([dealId])
```
- Create position
```
dealReference = ig.createPosition(currency, direction, epic, expiry, orderType, size, [limitDistance], [stopDistance], [forceOpen], [guaranteedStop])
```
- Close position
```
dealReference = ig.closePosition(dealId, direction, epic, expiry, orderType, size)
```

Example
```
order = ig.createPosition('AUD', 'BUY', 'IX.D.NASDAQ.IFA.IP', '-', 'MARKET', 2, 20, 40)

dealReference = ig.closePosition([dealId],'SELL',  '-', 'MARKET', 2)

```
#!/usr/bin/env python3
# Script to read TradingView's CSV export of orders, and parse them to determine total filled contract count

import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Filename of CSV TradingView exported orders')
args = parser.parse_args()

f = open(args.filename, 'r')
raw = csv.DictReader(f)
trades = list()
skipped = 0
for row in raw:
    buf = {"SYMBOL": row['Symbol'], "SIDE": row['Side'], "QTY": row['Fill Qty'], "STATUS": row['Status']}
    if row['Status'] == 'Filled':
        trades.append(buf)
    else:
        skipped += 1
f.close()

print(f"Trades excluded(status != 'Filled')    : {skipped}")

symbols = set([row['SYMBOL'] for row in trades])

for symbol in symbols:
    symbol_trades = [row for row in trades if row['SYMBOL'] == symbol]
    trade_count = sum([int(trade['QTY']) for trade in symbol_trades])
    print(f"Total contracts traded for {symbol} : {trade_count}")

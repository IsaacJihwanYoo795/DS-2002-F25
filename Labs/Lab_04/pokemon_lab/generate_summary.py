#!/usr/bin/env python3
import os
import pandas as pd
import sys
def generate_summary(portfolio_file):
	if not os.path.exists(portfolio_file):
		print("Does not exist", file=sys.stderr)
		sys.exit(1)
	df = pd.read_csv(portfolio_file)
	if df.empty:
		print("empty")
		return
	total_portfolio_value = df['card_market_value'].sum()
	most_valuable_id = df['card_market_value'].idxmax()
	most_valuable_card = df.loc[most_valuable_id]
	print(f"Total Portfolio Value is: ${total_portfolio_value:,.2f}")
	print(f"Most Valauaable Card is: {most_valuable_card['card_name']} (ID: {most_valuable_card['card_id']}), Value: ${most_valuable_card['card_market_value']:,.2f}")
def main():
	generate_summary("card_portfolio.csv")
def test():
	generate_summary("test_card_portfolio.csv")

if __name__ == "__main__":
	print("Test", file=sys.stderr)
	test()

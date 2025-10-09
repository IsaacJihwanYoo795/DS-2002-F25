#!/usr/bin/env python3
import os
import pandas as pd
import json
import sys
def _load_lookup_data(lookup_dir):
	all_lookup_df = []
	for files in os.listdir(lookup_dir):
		if not files.endswith(".json"):
			continue
		filepath = os.path.join(lookup_dir, files)
		with open(filepath, 'r') as f:
			data = json.load(f)

		df = pd.json_normalize(data["data"])

		df['card_market_value'] = df.get('tcgplayer.prices.holofoil.market').fillna(df.get('tcgplayer.prices.normal.market')).fillna(0.0)

		df = df.rename(columns={"id":"card_id", "name":"card_name", "number":"card_number", "set.id":"set_id", "set.name":"set_name"})
		for column in ["card_id", "card_name", "card_number", "set_id", "set_name", "card_market_value"]:
			if column not in df.columns:
				df[column] = pd.NA
		required_cols = ["card_id", "card_name", "card_number", "set_id", "set_name", "card_market_value"]
		all_lookup_df.append(df[required_cols].copy())
	lookup_df = pd.concat(all_lookup_df, ignore_index=True)
	lookup_df = lookup_df.sort_values("card_market_value", ascending=False)
	lookup_df = lookup_df.drop_duplicates(subset=["card_id"], keep="first")
	return lookup_df

def _load_inventory_data(inventory_dir):
	inventory_data = []
	for files in os.listdir(inventory_dir):
		if not files.endswith(".csv"):
			continue
		path = os.path.join(inventory_dir, files)
		df = pd.read_csv(path)
		inventory_data.append(df)
	if not inventory_data:
		return pd.DataFrame()
	inventory_df = pd.concat(inventory_data, ignore_index=True)
	inventory_df['card_id'] = inventory_df['set_id'].astype(str) + '-' + inventory_df['card_number'].astype(str)
	return inventory_df

def update_portfolio(inventory_dir, lookup_dir, output_file):
	loadlookup = _load_lookup_data(lookup_dir)
	loadinventorydata = _load_inventory_data(inventory_dir)
	if loadinventorydata.empty:
		print("Error empty inventory")
		empty_p = pd.DataFrame(columns=["card_id", "card_name", "card_number", "set_id", "set_name", "card_market_value"])
		empty_p.to_csv(output_file, index=False)
		return
	for columns in ["card_name", "card_number", "set_id"]:
		if columns in loadinventorydata.columns:
			loadinventorydata = loadinventorydata.drop(columns=columns)
	merged = pd.merge(loadinventorydata, loadlookup[["card_id", "card_name", "card_number", "set_id", "set_name", "card_market_value"]], on="card_id", how="left")
	merged["card_market_value"] = merged["card_market_value"].fillna(0.0)
	merged["set_name"] = merged["set_name"].fillna("NOT_FOUND")
	merged["index"] = merged["binder_name"].astype(str) + "-" + merged["page_number"].astype(str) + "-" + merged["slot_number"].astype(str)
	final_cols = ["card_id", "card_name", "card_number", "set_id", "set_name", "card_market_value", "binder_name", "page_number", "slot_number", "index"]
	merged[final_cols].to_csv(output_file, index=False)
	print("Successful")

def main():
	update_portfolio("./card_inventory/", "./card_set_lookup/", "card_portfolio.csv")
def test():
	update_portfolio("./card_inventory_test/", "./card_set_lookup_test/", "test_card_portfolio.csv")

if __name__ == "__main__":
	print("Going into Test Mode", file=sys.stderr)
	test()


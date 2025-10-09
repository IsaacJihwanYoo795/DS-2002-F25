#!/usr/bin/env python3
import sys
import update_portfolio
import generate_summary

def run_production_pipeline():
	print("Starting now", file=sys.stderr)
	print("Running ETL", file=sys.stderr)
	update_portfolio.main()
	print("Reporting Step", file=sys.stderr)
	generate_summary.main()
	print("Done", file=sys.stderr)

if __name__ == "__main__":
	run_production_pipeline()

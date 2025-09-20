.PHONY: all fetch analyze clean
all: analyze

fetch:
	@echo "Fetching Data"
	bash ./fetch_metars.sh
	@echo "Complete"

analyze: fetch
	@echo "Analyzing Data"
	bash ./analyze_data.sh
	@echo "Complete"

clean:
	@echo "Cleaning Up"
	rm -rf weather_report.csv
	rm -rf raw_metars
	@echo "Complete"

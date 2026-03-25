# Makefile for the Pokemon White 2 Reverse Engineering Project

default: help

# Commands:

extract: extract_data extract_overlays	## Extract data and overlays from the rom file
	
extract_check:
	@if ! command -v ndstool &> /dev/null; then \
		echo "ERROR: ndstool not found!" >&2; \
		exit 1; \
	fi
	@if ! [ -f rom/*.nds ]; then \
		echo "ERROR: Rom file not found!" >&2; \
		exit 1; \
	fi

extract_data: extract_check
	@echo "Extracting data to 'data/'..."
	@mkdir -p data/
	@ndstool -d data/ -t data/banner.bin -o data/logo.bin -x rom/*.nds > /dev/null
	@echo "Finished extracting data"

extract_overlays: extract_check
	@echo "Extracting overlays to 'overlays/'..."
	@mkdir -p overlays/ARM9/
	@mkdir -p overlays/ARM7/
	@ndstool -y overlays/ -9 overlays/ARM9/ARM9.bin -y9 overlays/ARM9/overlay_table_ARM9.bin \
		-7 overlays/ARM7/ARM7.bin -y7 overlays/ARM7/overlay_table_ARM7.bin -x rom/*.nds > /dev/null
	@echo "Finished extracting overlays"

clean:	## Clean up any generated files
	rm -rf build/
	rm -rf assets/
	rm -rf data/
	rm -rf overlays/
	@echo "Finished cleaning"

help:	## Print this help dialogue 
	@echo ""
	@echo "Useage: make <command> [ARGUMENT=value]"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""

# Makefile for the Pokemon White 2 Reverse Engineering Project

default: help

# Commands:

ndstool_check:	
	@if ! command -v ndstool &> /dev/null; then \
		echo "ERROR: ndstool not found!" >&2; \
		exit 1; \
	fi

extract: extract_data extract_overlays	## Extract data and overlays from the rom file
	
extract_check: ndstool_check
	@if ! [ -f rom/*.nds ]; then \
		echo "ERROR: Rom file not found!" >&2; \
		exit 1; \
	fi

extract_data: extract_check
	@echo "Extracting data to 'data/'..."
	@mkdir -p data/
	@mkdir -p ex/
	@ndstool -d data/ -t ex/banner.bin -h ex/header.bin -o ex/logo.bin -x rom/*.nds > /dev/null
	@echo "Finished extracting data"

extract_overlays: extract_check
	@echo "Extracting overlays to 'overlays/'..."
	@mkdir -p overlays/
	@mkdir -p ex/ARM9/
	@mkdir -p ex/ARM7/
	@ndstool -y overlays/ -9 ex/ARM9/ARM9.bin -y9 ex/ARM9/overlay_table_ARM9.bin \
						  -7 ex/ARM7/ARM7.bin -y7 ex/ARM7/overlay_table_ARM7.bin \
						  -x rom/*.nds > /dev/null
	@echo "Finished extracting overlays"

repack: ndstool_check	## Repack files back into a game rom
	@echo "Repacking rom..."
	@rm -rf build/
	@mkdir build/
	@ndstool -9 ex/ARM9/ARM9.bin -y9 ex/ARM9/overlay_table_ARM9.bin \
			 -7 ex/ARM7/ARM7.bin -y7 ex/ARM7/overlay_table_ARM7.bin \
			 -t ex/banner.bin -h ex/header.bin -o ex/logo.bin \
			 -y overlays/ -d data -c build/pokemon_white_2.nds > /dev/null
	@echo "Rom created!"

clean:	## Clean up any generated files
	rm -rf build/
	rm -rf assets/
	rm -rf data/
	rm -rf overlays/
	rm -rf ex/
	@echo "Finished cleaning"

help:	## Print this help dialogue 
	@echo ""
	@echo "Useage: make <command> [ARGUMENT=value]"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""


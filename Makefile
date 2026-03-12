.PHONY: run-local clean

run-local:
	@echo "Starting API and Web locally..."
	@bash -lc 'make -C apps/api run-local & make -C apps/web dev & wait'

clean:
	@echo "Cleaning root and app artifacts..."
	@bash -lc 'make -C apps/api clean && make -C apps/web clean'

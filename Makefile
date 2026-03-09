.PHONY: run-local

run-local:
	@echo "Starting API and Web locally..."
	@bash -lc 'make -C apps/api run-local & make -C apps/web dev & wait'

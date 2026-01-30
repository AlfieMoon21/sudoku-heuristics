# Simple Makefile for Sudoku Project

.PHONY: test
test:
	python3 sudoku_solver.py

.PHONY: experiment
experiment:
	python3 experiments.py

.PHONY: clean
clean:
	rm -rf results/*
	rm -rf __pycache__

.PHONY: help
help:
	@echo "make test       - Run solver test"
	@echo "make experiment - Run full experiments"
	@echo "make clean      - Clean generated files"
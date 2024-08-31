#!/bin/bash

PYTHONPATH=/app/src uvicorn main:app --host 0.0.0.0

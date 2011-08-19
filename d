#!/bin/bash
./p 2>errors.err
if [ -s errors.err ]; then
	cat errors.err
fi

#!/bin/bash

while true; do
  echo "Stressing CPU..."
  stress-ng --cpu 2 --timeout 60

  echo "Stressing memory..."
  stress-ng --vm 1 --vm-bytes 512M --timeout 60

  echo "Stressing disk..."
  stress-ng --hdd 1 --timeout 60

  echo "Stressing I/O..."
  stress-ng --io 2 --timeout 60

  echo "Stressing matrix operations..."
  stress-ng --matrix 2 --timeout 60
done

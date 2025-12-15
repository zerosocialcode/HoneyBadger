#!/usr/bin/env python3
"""
HoneyBadger (AVS)
Enterprise Entry Point
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.app import main
except ImportError:
    sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

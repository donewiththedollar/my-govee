#!/usr/bin/env python3
"""Govee H6022 Quantum Desk Lamp display engine."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from govee.cli import main

if __name__ == "__main__":
    main()

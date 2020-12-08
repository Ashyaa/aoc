#!/usr/bin/env python

from datetime import datetime
from day8 import solution

if __name__ == "__main__":
    startTime = datetime.now()
    solution.run()
    print(datetime.now() - startTime)
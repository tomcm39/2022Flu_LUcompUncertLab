#mcandrew

import sys
import numpy as np
import pandas as pd


class epitime(object):
    def __init__(self):
        pass
    
    def thisweek(self):
        import datetime
        from epiweeks import Week

        from datetime import datetime as dt

        today = dt.today()
        dayofweek = today.weekday()

        thisWeek = Week.thisweek()
        lastWeek = Week.thisweek()-1
        
        self.thisWeek = thisWeek
        self.lastWeek = lastWeek
        return thisWeek, lastWeek

if __name__ == "__main__":


    pass

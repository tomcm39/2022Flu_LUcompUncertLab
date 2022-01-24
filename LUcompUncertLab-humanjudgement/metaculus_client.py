#mcandrew

class metaculus_client(object):
    def __init__(self,loginfile):
        self.importLoginInfo(loginfile)
        
    def importLoginInfo(self,loginfile):
        loginInfo = {}
        for line in open(loginfile):
            k,v = line.strip().split(",")
            loginInfo[k] = v
        self.username  = loginInfo['username']
        self.password  = loginInfo['password']
        self.csrftoken = loginInfo['csrftoken']

    def sendRequest2Server(self):
        import requests
        client = requests.session() # start session
    
        # add CSRF cookie
        cookie_obj = requests.cookies.create_cookie(name="csrftoken",value= self.csrftoken)
        client.cookies.set_cookie(cookie_obj)

        # add headers
        headers = { "referer":"https://covid.metaculus.com/questions/"
                    ,'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                    ,'accept': 'application/json; version=LATEST'
        }
        client.headers.update(headers)
        
        # post username and password to form to authenticate
        payload = {
	    "username": self.username, 
	    "password": self.password,
        }
        p = client.post("https://pandemic.metaculus.com/api2/accounts/login/", data = payload)
        self.client = client
        self.auth   = p

    def collectQdata(self,QN):
        root = "https://www.metaculus.com/api2/questions/{:d}"
        data = self.client.get(root.format(QN)).json()
        self.data = data

    def constructPDF(self):
        import numpy as np
        
        density = self.data['community_prediction']['unweighted']['y']
        numProbs = 200
        
        minvalue  = self.data['possibilities']['scale']['min']
        maxvalue  = self.data['possibilities']['scale']['max']

        deriv_ratio  = self.data['possibilities']['scale']['deriv_ratio']
        
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.deriv_ratio = deriv_ratio

        if type(minvalue) is int:
            minvalue = float(minvalue)
            maxvalue = float(maxvalue)
        elif type(minvalue) is str: #had to change this line because error if float
            minvalue = pd.to_datetime(minvalue)
            maxvalue = pd.to_datetime(maxvalue)

        exponent = np.log(deriv_ratio)
        b = (maxvalue-minvalue)/(deriv_ratio-1.)
        interval = 0 + b* np.exp( exponent*np.linspace(0,1,201))
            
        self.xs=interval
        self.dens=density
        self.exponent = exponent
        self.b = b

    def hasDist(self):
        try:
            density = self.data['community_prediction']['unweighted']['y']
            return 1
        except:
            return 0

    def extract_target_end_date(self):
        import re
        import pandas as pd
        desc = self.data["description"]
        laydate = re.findall("ending on (.*?)[?][*]",desc)[0]
        dow, month, day, yr = laydate.split(' ')

        dt = pd.to_datetime("{:s}-{:s}-{:s}".format(yr,month,day))
        self.dt = dt
        return dt

    def extract_location(self):
        import re
        import pandas as pd
        desc = self.data["description"]
        location = re.findall("due to influenza be in (.*?) for the week",desc)[0]
        self.location = location
        return location
        
def addInCDF(data):
    def cuumsum(x):
        x = x.sort_values('bin')
        x['cdf'] = np.cumsum(x.prob*x.interval)
        return x
    return data.groupby('qid').apply(cuumsum).drop(columns=['qid']).reset_index()

if __name__ == "__main__":
    pass



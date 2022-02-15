#mcandrew

class extractParams(object):
    def __init__(self):
        self.loadData()
        self.extractParams()
        self.write()

    def loadData(self):
        import pandas as pd
        community_preds = pd.read_csv("../communitypredictions.csv")
        self.community_preds = community_preds
        
    def extractParams(self):
        params = self.community_preds[["qid","b","exponent"]].drop_duplicates()
        self.params = params
        return params

    def write(self):
        self.params.to_csv("parametersPerQuestion.csv",index=False)

if __name__ == "__main__":

    EP = extractParams()

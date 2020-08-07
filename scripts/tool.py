import pandas as pd
import json
import os


class JsonFile:
    def __init__(self,filepath):
        self.filepath = filepath

    def read_file_by_json(self):
        if not os.path.exists(self.filepath):
            print(self.filepath,"不存在")
            return {}
        with open(self.filepath,"r",encoding="utf-8") as __f:
            filedata = json.load(__f)
        return filedata

    def write_file_by_json(self,filedata):
        with open(self.filepath,"w",encoding="utf-8") as __f:
            json.dump(filedata, __f,indent=1,sort_keys=False, ensure_ascii=False)

    def init_ipynbfile(self,lines):
        filedata = {"cells":[
                     {
                   "cell_type": "markdown",
                   "metadata": {},
                   "source": lines
                     }
                    ],
           "metadata":{
               "kernelspec": {
                   "display_name": "Python 3",
                   "language": "python",
                   "name": "python3"
                  },
                  "language_info": {
                   "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                   },
                   "file_extension": ".py",
                   "mimetype": "text/x-python",
                   "name": "python",
                   "nbconvert_exporter": "python",
                   "pygments_lexer": "ipython3",
                   "version": "3.7.4"
                  },
           },
            "nbformat": 4,
           "nbformat_minor": 2}
        
        self.write_file_by_json(filedata)

    def split_markdown_cells(self):
        __ipynb_data = self.read_file_by_json()
        __oldcells = __ipynb_data["cells"].copy()
        __newcells = []

        for __cell in __oldcells:
            if __cell["cell_type"] == "code":
                if len(__cell["source"]) > 0:
                    __newcells.append(__cell)
            else:
                __lines = __cell["source"]
                __start = __end = 0
                for __i in range(len(__lines)):
                    __line = __lines[__i]
                    if __line == "\n":
                        __end = __i
                        __icell = {"cell_type": "markdown","metadata": {},"source": __lines[__start:__end]}
                        if len(__icell["source"]) > 0:
                            __newcells.append(__icell)
                        __start = __i+1

                __icell = {"cell_type": "markdown","metadata": {},"source": __lines[__start:]}
                if len(__icell["source"]) > 0:
                    __newcells.append(__icell)
        
        __ipynb_data["cells"] = __newcells
        self.write_file_by_json(__ipynb_data)


def init_data(fromfile):
    """从数据库获取数据并初始化"""
    df = pd.read_csv(fromfile,sep=";",header=1)
    rlts = []
    #rlts = eval(df.T.to_json())
    for i in df.values:
        rlts = [{"id":i[0],"created_at":i[1],"updated_at":i[2],"title":i[3],"content":i[4],"sort_id":i[5],"alias":i[6],"relative":i[7],"type":i[8]}] + rlts

    JsonFile(dirpath+"\\data_dev\\help_docs.json").write_file_by_json(rlts)
    
    types = list(df["type"].unique())
    for itype in types:
        lines = [f"# XUE.cn 帮助手册之{itype}\n","\n"]
        for rlt in rlts:
            if rlt["type"] == itype:
                ilines = ["### " + rlt["title"] + "\n","\n"] \
                        + [i+"\n" for i in rlt["content"].replace("\n","\n\n").split("\n")] \
                        + ["\n"]
                lines.extend(ilines)

        ifile = JsonFile(dirpath+"\\data_dev\\"+itype+".ipynb")
        ifile.init_ipynbfile(lines)
        ifile.split_markdown_cells()


if __name__ == "__main__":
    dirpath = r"D:\Jupyter\xuecn_books\xuecn_help_docs"
    fromfile = dirpath + "\\data_dev\\grafana_data_export.csv"
    init_data(fromfile)
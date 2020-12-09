import pandas as pd
import json
import os
import re

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
                    if __icell["source"][-1][-1] == "\n":
                        __icell["source"][-1] = __icell["source"][-1][:-1]
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
                            if __icell["source"][-1][-1] == "\n":
                                __icell["source"][-1] = __icell["source"][-1][:-1]
                            __newcells.append(__icell)
                        __start = __i+1

                
                __icell = {"cell_type": "markdown","metadata": {},"source": __lines[__start:]}
                if len(__icell["source"]) > 0:
                    if __icell["source"][-1][-1] == "\n":
                        __icell["source"][-1] = __icell["source"][-1][:-1]
                    __newcells.append(__icell)
        
        __ipynb_data["cells"] = __newcells
        self.write_file_by_json(__ipynb_data)


def init_data(fromfile, jsonfile):
    """从数据库获取数据并初始化"""
    df = pd.read_csv(fromfile,sep=";",header=1)
    rlts = []
    #rlts = eval(df.T.to_json())
    for i in df.values:
        rlts = [{"id":i[0],"created_at":i[1],"updated_at":i[2],"title":i[3],"content":i[4],"sort_id":i[5],"alias":i[6],"relative":i[7],"type":i[8]}] + rlts

    JsonFile(jsonfile).write_file_by_json(rlts)
    


def json2ipynb(jsonfile,ipynbpath):

    jfile = JsonFile(jsonfile)
    filedata = jfile.read_file_by_json()

    types = list(set([x["type"] for x in filedata]))
    for itype in types:
        lines = [f"## {itype}\n","\n"]
        for i in filedata:
            if i["type"] == itype:
                ilines = ["### " + i["title"] + "\n","<a id='q"+str(i["id"])+"'></a>\n","\n"] \
                        + [j+"\n" for j in i["content"].replace("\n","\n\n").split("\n")] \
                        + ["\n"]
                
                if i["relative"] not in (0,"0") :
                    for j in filedata:
                        if str(j["id"]) == str(i["relative"]):
                            x = j["title"]
                            if j["type"] != i["type"]:
                                ilines.extend(["**相关问题**：["+ x +"]("+j["type"]+".ipynb?anchor=q"+str(i["relative"])+")\n","\n"])
                            elif j["type"] == i["type"]:
                                ilines.extend(["**相关问题**：["+ x +"](#q"+str(i["relative"])+")\n","\n"])
                            break
                lines.extend(ilines)


        ifile = JsonFile(ipynbpath+"\\"+itype+".ipynb")
        ifile.init_ipynbfile(lines)
        ifile.split_markdown_cells()

if __name__ == "__main__":
    dirpath = r"D:\Jupyter\xuecn_books\xuecn_help_docs"
    fromfile = dirpath+"\\data_dev\\grafana_data_export.csv"
    jsonfile = dirpath+"\\data_dev\\help_docs.json"
    ipynbpath = dirpath+"\\data_dev"

    # 首次初始化
    # init_data(fromfile,jsonfile)

    # 后续维护更新，规范写入
    # jfile = JsonFile(jsonfile)
    # filedata = jfile.read_file_by_json()
    # jfile.write_file_by_json(filedata)

    # 同步 json 数据生成 ipynb 文件。重复用的脚本。
    json2ipynb(jsonfile,ipynbpath)

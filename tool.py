import pandas as pd
import json
import os
import re


import sys
sys.path.append(r'..\xuecn_content_tool\scripts')
from _JsonFile import *


class xuecn_help:
    def __init__(self,filepath):
        self.devfilepath = r'..\data_dev\help_docs.json'
        self.livefilepath = r'..\data_live\help_docs.json'

    def init_ipynbfile(self,lines,filepath):
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
        
        JsonFile(filepath).write_file_by_json(filedata)



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

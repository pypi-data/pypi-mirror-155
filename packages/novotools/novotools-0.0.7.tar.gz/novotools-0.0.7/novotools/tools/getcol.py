#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = "cm.Rpy"

import sys
import re
import signal
import click
import colorama

#solve [Error 32] Broken pipe
signal.signal(signal.SIGPIPE,signal.SIG_DFL)


class DataExtracter:
    def __init__(self,**kwargs):
        self.indata = kwargs.get("filename")
        self.colnames = kwargs.get("column")
        self.allmark = kwargs.get("title")
        self.exceptmark = kwargs.get("except")
        self.ignoremark = kwargs.get("ignore")
        self.split = kwargs.get("split")
        
    def first5line_extract(self):
        first5line = []
        i = 0
        if self.ignoremark != None:
            for line in self.indata:
                if not line.strip().startswith(self.ignoremark) and i < 5:
                    if re.search("^$",line.strip()):
                        break
                    else:
                        first5line.append(line.strip())
                        i += 1
                elif i >= 5:
                    break
        else:
            while i < 5:
                line = self.indata.readline()
                if re.search("^$",line.strip()):
                    break
                else:
                    first5line.append(line.strip())
                    i += 1
        return(first5line)

    def show_summary(self,):
        first5line = self.first5line_extract()
        title = first5line.pop(0).split(self.split)
        colstrings = []
        #print(len(title))
        for i in range(len(title)):
            eachcol_list = []

            for ele in first5line:
                try:
                    eachcol_list.append(ele.split(self.split)[i])
                except:
                    eachcol_list.append("无对应值")
            
            eachstring = " ".join(eachcol_list)
            each_str_len = len(eachstring)
            if each_str_len > 50:
                eachstring = eachstring[0:51] + "..."
            else:
                eachstring = eachstring + "..."
            colstrings.append(eachstring)
        
        longest_value = max([len(i) for i in title])
        for j in range(len(title)):
            print("{bright}{color1}{order} {color2}{colname: >{value}}\t{color3}{content}{back}".format(
                color1 = colorama.Fore.YELLOW,color2 = colorama.Fore.RED,color3 = colorama.Fore.GREEN,
                bright=colorama.Style.BRIGHT,order = j+1, colname = title[j], content = colstrings[j],
                value = longest_value,back=colorama.Style.RESET_ALL
            )) 
    
    def extract_columns(self):
        
        seps=[re.split(":|-",i) if re.search(":|-",i) else [i] for i in self.colnames.split(",") ]
        #print(seps)
        first5line = self.first5line_extract()
        title = first5line[0].split(self.split)
        col_num_mark = [] #all column numbers colnames indicated
        for ele in seps:
            if len(ele) == 1 :
                if ele[0] not in title:
                    raise Exception(f"{ele[0]} not in title {title} or wrong split indicated, please check!")
                linenum = title.index(ele[0])
                col_num_mark.append(linenum)
            elif len(ele) == 2 :
                startnum = title.index(ele[0])
                endnum = title.index(ele[1])
                for num in range(startnum,endnum+1):
                    col_num_mark.append(num)
            assert len(ele) < 3, " May your colnames parameter was wrong, please check "
        if self.exceptmark:
            col_num_mark = [n for n in range(len(title)) if n not in col_num_mark ]
        return(col_num_mark)

    def column_print(self):
        col_num_mark = self.extract_columns()
        for line in self.indata:
            if self.ignoremark !=None:
                if line.strip().startswith(self.ignoremark):
                    pass
                else:
                    selected_cols = []
                    for i in col_num_mark:
                        selected_cols.append(line.strip().split(self.split)[i])
                    print(f"{self.split}".join([str(n) for n in selected_cols]))
                        
            else:
                selected_cols = []
                for i in col_num_mark:
                    selected_cols.append(line.strip().split(self.split)[i])
                print(f"{self.split}".join([str(n) for n in selected_cols])) 

@click.command()
@click.argument("filename",default=sys.stdin,type=click.File('r'))
@click.option("--title","-t",is_flag=True,help="list title information of input file")
@click.option("--split","-s",help="seperator to split each column default[\\t]",default="\t")
@click.option("--column","-c",help="columns to extract by their name,comma split")
@click.option("--except",'-e',is_flag=True,help="extract columns except indicated columns")
@click.option("--ignore",'-i',help="ignore lines start with indicated string")
def workflow(**kwargs):
    """\b
    Example:
        function1:show all colnames:
        getcol.py -t <Filename>
        cat file | getcol -t
        
        function2:select indicated colname:
        getcol.py -c colname1:colname2 <Filename>
        getcol.py -e -c colname1:colname2 <Filename>
        getcol.py -e -c colname1:colname2,colname3 --ignore "#" <Filename>
    """
    df = DataExtracter(**kwargs)
    #print(df.allmark)
    #print(df.exceptmark)
    #print(df.colnames)
    #df.show_summary()
    if df.allmark and df.exceptmark or df.allmark and df.colnames :
        raise SyntaxError("{}-a parameter will be not used with other parameters{}".format(
            colorama.Fore.RED,colorama.Style.RESET_ALL
        ))
    elif df.allmark:
        df.show_summary()
    elif df.colnames:
        df.column_print()


if __name__=="__main__":
    #print(__author__)
    colorama.init()
    #print(args)
    #print(df.first5line_extract()
    #df.column_print()
    workflow()
    

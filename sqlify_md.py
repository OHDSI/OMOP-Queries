import os
import re
import sys

def sql_chunks(filename):
    with(open(filename, "r")) as the_file: 
        the_md = the_file.readlines()
        in_chunk = False
        new_md = []

        def look_around(doc, regex, line_number, around = 1):
            def search(reg, ln):
                return(bool(re.search(pattern = reg, string = ln)))
            tr = []
            for k in range(around * 2 + 1):
                try:
                    tr.append(search(regex, doc[line_number - around + k]))
                except IndexError: 
                    tr.append(False)

            return(tr)

        for i in range(len(the_md)):
            preevl_code, prevl_code, currl_code, nxtl_code, nxxtl_code = look_around(the_md, r'^\ {4}', i, 2)
            _, _, _, nxtl_n, nxxtl_n = look_around(the_md, r'\n', i, 2)
            if (currl_code and nxtl_code) or (not in_chunk and currl_code and nxtl_n and nxxtl_code):
                #case: start of block
                #print "Match!"
                in_chunk = True
                new_md.append('```sql\n')
                new_md.append(the_md[i])
                #case: end of block
            elif currl_code and (not nxtl_code and not nxxtl_code):
                new_md.append(the_md[i])
                new_md.append('```\n')
                in_chunk = False
            elif in_chunk and not (nxtl_code or nxtl_n) and not (nxxtl_code or nxxtl_n):
                new_md.append(the_md[i])
                in_chunk = False
            elif currl_code and not in_chunk and not prevl_code and not preevl_code:
                new_md.append('```sql\n')
                new_md.append(the_md[i])
                new_md.append('```\n')
            else: 
                new_md.append(the_md[i])

    return(new_md)

def write_md(fl, flnm):
    with(open(flnm, 'w')) as new_fl:
        new_fl.writelines(fl)
    return(True)

if __name__ == '__main__':
    if len(sys.argv[1:]) != 1:
        stop('This script accepts one parameter: the path to a folder containing markdown files.')
    md_fldr = sys.argv[1]
    os.makedirs('sql_' + md_fldr)
    filenames = sorted(os.listdir("./md"))
    for flnm in filenames:
        write_md(sql_chunks("./md/" + flnm), "./sql_md/" + flnm) 


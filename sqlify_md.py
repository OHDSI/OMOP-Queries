import os
import re
import sys

def look_around(doc, regex, line_number, around = 1):
    def search(reg, ln):
        return(bool(re.search(pattern = reg, string = ln)))
    tr = []
    for k in range(around * 2 + 1):
        try:
            if search(regex, doc[line_number - around + k]):
                tr.append(True)
            else:
                tr.append(False)
        except IndexError: 
            tr.append(False)

    return(tr)


def write_md(fl, flnm):
    with(open(flnm, 'w')) as new_fl:
        new_fl.writelines(fl)
    return(True)

def read_md(flpath):
    with(open(flpath, 'r')) as new_fl:
        return(new_fl.readlines())

def sql_chunks(filename):

    the_md = read_md(filename)
    in_chunk = False
    new_md = []

    for i in range(len(the_md)):

        c_lp3, c_lp2, c_lp1, c_l, c_ln1, c_ln2, c_ln3 = look_around(the_md, r'^(\ {4}|\t)', i, 3)
        n_lp2, n_lp1, _, n_ln1, n_ln2 = look_around(the_md, r'\n', i, 2)

        #nextlines_code = (c_ln1 and c_ln2) or (n_ln1 and c_ln2) or (n_ln1 and n_ln2 and c_ln3)
        nextlines_code = c_ln1 or c_ln2 or c_ln3
        prevlines_code = c_lp1 or c_lp2 or c_lp3
        new_codeline = c_l and not prevlines_code
        any_code_nearby = nextlines_code or prevlines_code

        start_chunk = (not in_chunk) and ((c_l and nextlines_code) or new_codeline)
        end_chunk = c_l and in_chunk and not nextlines_code
        one_liner = c_l and not in_chunk and not any_code_nearby

        if start_chunk:
            #case: start of block
            #print "Match!"
            in_chunk = True
            new_md.append('```sql\n')
            new_md.append(the_md[i])
            #case: end of block
        elif end_chunk:
            new_md.append(the_md[i])
            new_md.append('```\n')
            in_chunk = False
        elif one_liner:
            new_md.append('```sql\n')
            new_md.append(the_md[i])
            new_md.append('```\n')
        else: 
            new_md.append(the_md[i])
        
    return(new_md)

if __name__ == '__main__':
    if len(sys.argv[1:]) != 1:
        raise ValueError('This script accepts one parameter: the path to a folder containing markdown files.')
    md_fldr = sys.argv[1] + '/'
    new_md_fldr = './sql_' + md_fldr
    os.makedirs(new_md_fldr)
    filenames = sorted(os.listdir(md_fldr))
    for flnm in filenames:
        write_md(sql_chunks(md_fldr + flnm), new_md_fldr + flnm) 

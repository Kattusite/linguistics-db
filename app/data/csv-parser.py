# Merge and anonymize the grammar/typology csv,
# Then convert it to a json file

import csv, json, hashlib, re

def main():
    grammarCSV = open("unanon-grammar.csv", "r", newline='')
    grammarReader = csv.reader(grammarCSV)

    typologyCSV = open("unanon-typology.csv", "r", newline='')
    typologyReader = csv.reader(typologyCSV)

    outputCSV = open("anon-combined.csv", "w", newline='')

    TIME  = 0
    NETID = 1
    NAME  = 2

    g_header = []
    g_data = {}
    g_netid = []
    for i, row in enumerate(grammarReader):
        if i == 0:
            g_header = row
            continue
        netid = asciify(row[NETID]).encode("ASCII")
        name  = asciify(row[NAME]).encode("ASCII")
        anon_netid = hashlib.sha3_256(netid).hexdigest()
        anon_name  = hashlib.sha3_256(name).hexdigest()
        row[NETID] = anon_netid
        row[NAME]  = anon_name
        g_data[anon_netid] = row
        g_netid.append(anon_netid)

    t_header = []
    t_data = {}
    t_netid = []
    for i, row in enumerate(typologyReader):
        if i == 0:
            t_header = row
            continue
        netid = asciify(row[NETID]).encode("ASCII")
        name  = asciify(row[NAME]).encode("ASCII")
        anon_netid = hashlib.sha3_256(netid).hexdigest()
        anon_name  = hashlib.sha3_256(name).hexdigest()
        row[NETID] = anon_netid
        row[NAME]  = anon_name
        t_data[anon_netid] = row
        t_netid.append(anon_netid)

    # Merge netid lists
    netidSet = set(g_netid).union(set(t_netid))
    print(len(netidSet))

def asciify(str):
    return re.sub(r'[^\x00-\x7F]',' ', str)


main()

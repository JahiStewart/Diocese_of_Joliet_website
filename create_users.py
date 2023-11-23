fvar = open('patron_report.txt','r')
from werkzeug.security import generate_password_hash
import random
from uuid import uuid4

def generate_password_symbols():
    symbols = []
    for i in range(33,127):
        if i not in [34,39]:
            symbols.append(chr(i))
    return symbols

def generate_password(symbols,length):
    result = ''
    for i in range(length):
        result = result + random.choice(symbols)
    return result

symbols = generate_password_symbols()
organizations = {}
org_queries = []
user_queries = []
user_org_queries = []
fvar = open('patron_report.txt','r')
for line in fvar:
    if line.strip() == '':
        continue
    parts = line.split('\t')
    first = parts[0]
    last = parts[1]
    email = parts[2]
    password = generate_password_hash(generate_password(symbols,10))
    orgs = parts[3].strip()
    org_list = []
    user_id = uuid4()
    if orgs != "":
        orgs = orgs.replace('"','').replace(',','\t')
        org_list = orgs.split('\t')
        for org in org_list:
            org = org.strip()
            if org not in organizations:
                organizations[org] = uuid4()
                org_queries.append('insert into organization values ("%s","%s","");' % (organizations[org],org))
            user_org_queries.append('insert into userorganization values ("%s","%s","%s");' % (uuid4(),organizations[org],user_id))
    user_queries.append('insert into user values ("%s","%s","%s","%s","%s","");' % (user_id,email,password,first,last))
fvar.close()
fvar = open('populate.sql','w')
for org_query in org_queries:
    fvar.write(org_query+'\n')
for user_query in user_queries:
    fvar.write(user_query+'\n')
for user_org_query in user_org_queries:
    fvar.write(user_org_query+'\n')
fvar.close()

    

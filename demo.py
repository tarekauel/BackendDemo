import sys
import graphlab as gl

from graphlab import SGraph
from graphlab import SArray
from graphlab import SFrame

from algorithm import initialize_graph
from algorithm import spreading_activation
from algorithm import shortest_path
from algorithm import distance_networks
from algorithm import distance_networks_wrapper

if sys.argv[1] != None:
	path = sys.argv[1]
else:		
	path = "./data/"

verbose=False
vertexFiles = ["City", "Country", "Region","Advisor", "Category", "Founder", "FundingRound", "HQ", "keywords", "Member", "Office", "organizations", "PrimaryImage", "TeamMember", "Website","companies_acquired_by_sap"]
edgesFiles = ["GeoInformation","acquisitions", "categories_keywords_edges", "investments", "keywords_descriptions_edges", "keywords_webpages_edges", "relationships", "companies_acquired_by_sap_edges"]
g = SGraph()

for f in vertexFiles:
    content = SFrame.read_csv(path + f + '.csv', na_values='null', verbose=verbose)
    if 'path' in content.column_names():
        g = g.add_vertices(content, vid_field='path')
    elif 'url' in content.column_names():
        g = g.add_vertices(content, vid_field='url')
    else:
        print "Unknown vid field: ", content.column_names()
        sys.exit()

for f in edgesFiles:
    content = SFrame.read_csv(path + f + '.csv', na_values='null', verbose=verbose)
    if 'src' in content.column_names() and 'dst' in content.column_names():
        g = g.add_edges(content, src_field='src', dst_field='dst')
    elif 'source' in content.column_names() and 'target' in content.column_names():
        g = g.add_edges(content, src_field='source', dst_field='target')
    else:
        print "Unknown src_id/dst_id field: ", content.column_names()
        sys.exit()

print g.summary();

def parseResult(row, columns):
    for c in columns:
        if isinstance(c, list):
            result = ''
            found = False
            for x in c:
                if row[x] != None and row[x] != '':
                    result += row[x] + ' '
                    found = True
            if found:
                return result
        else:
            if row[c] != None and row[c] != '':
                return row[c]
    return None

def select(graph, columns):
    columns.append('__id')
    columns.append('type')
    select_columns = []
    for c in columns:
        if isinstance(c, list):
            for x in c:
                select_columns.append(x)
        else:
            select_columns.append(c)
    return graph.get_vertices()[select_columns]

columns = ['name','label',['first_name','last_name']]
d = select(g,columns)
x = d[['__id','type']]
x = x.add_column(d.apply(lambda row: parseResult(row, columns)), 'name')
x = x[x['name'] != None]
x = x.filter_by(['Organization','City','Category','keyword','Region','Country','Person','TeamMember','Founder','Advisor'],'type')
x.save(path + "/auto.csv", format='csv')

print len(x), " items for auto suggestion"

print "START NOW INITIALIZING"

initialize_graph(g)

while True == True:
    print "Waiting for messages"
    sys.stdout.flush()
    data = raw_input('command: ');
    try:
        print eval(data)
    except Exception as details:
        print details
    sys.stdout.flush()
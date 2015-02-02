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

#,'City','Category','Keyword','Region','Country'
d = g.get_vertices()[['__id','name','type']]
d = d[d['name'] != None and d['name'] != 'null']
d = d.filter_by(['Organization','City','Category','Keyword','Region','Country'],'type')
d.save(path + "/auto.csv", format='csv')

print len(d), " items for auto suggestion"

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
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
	sys.exit(-1)

verbose=False
organizations = SFrame.read_csv(path + 'organizations.csv', na_values='null', verbose=verbose)
acquisitions_edges = SFrame.read_csv(path + 'acquisitions_edges.csv', na_values='null', verbose=verbose)
investments_investor_edges = SFrame.read_csv(path + 'investments_investors_edges.csv', na_values='null', verbose=verbose)
investments_companies_edges = SFrame.read_csv(path + 'investments_companies_edges.csv', na_values='null', verbose=verbose)
categories = SFrame.read_csv(path + 'categories.csv', na_values='null', verbose=verbose)
categories_edges = SFrame.read_csv(path + 'categories_edges.csv', na_values='null', verbose=verbose)
funding_rounds = SFrame.read_csv(path + 'fundingRounds.csv', na_values='null', verbose=verbose)
funding_rounds_edges = SFrame.read_csv(path + 'fundingRounds_edges.csv', na_values='null', verbose=verbose)
images = SFrame.read_csv(path + 'images.csv', na_values='null', verbose=verbose)
images_edges = SFrame.read_csv(path + 'images_edges.csv', na_values='null', verbose=verbose)
keywords = SFrame.read_csv(path + 'keywords.csv', na_values='null', verbose=verbose)
keywords_descriptions_edges = SFrame.read_csv(path + 'keywords_descriptions_edges.csv', na_values='null', verbose=verbose)
keywords_webpages_edges = SFrame.read_csv(path + 'keywords_webpages_edges.csv', na_values='null', verbose=verbose)
news = SFrame.read_csv(path + 'news.csv', na_values='null', verbose=verbose)
news_edges = SFrame.read_csv(path + 'news_edges.csv', na_values='null', verbose=verbose)
offices = SFrame.read_csv(path + 'offices.csv', na_values='null', verbose=verbose)
offices_edges = SFrame.read_csv(path + 'offices_edges.csv', na_values='null', verbose=verbose)
person = SFrame.read_csv(path + 'person.csv', na_values='null', verbose=verbose)
person_edges = SFrame.read_csv(path + 'person_edges.csv', na_values='null', verbose=verbose)
product = SFrame.read_csv(path + 'product.csv', na_values='null', verbose=verbose)
product_edges = SFrame.read_csv(path + 'product_edges.csv', na_values='null', verbose=verbose)
website = SFrame.read_csv(path + 'website.csv', na_values='null', verbose=verbose)
website_edges = SFrame.read_csv(path + 'websites_edges.csv', na_values='null', verbose=verbose)
categories_keywords_edges = SFrame.read_csv(path + 'categories_keywords_edges.csv', na_values='null', verbose=verbose)
categories_of_companies_acquired_by_sap__edges = SFrame.read_csv(path + 'categories_of_companies_acquired_by_sap__edges.csv', na_values='null', verbose=verbose)
companies_acquired_by_sap = SFrame.read_csv(path + 'companies_acquired_by_sap.csv', na_values='null', verbose=verbose)
companies_acquired_by_sap_edges = SFrame.read_csv(path + 'companies_acquired_by_sap_edges.csv', na_values='null', verbose=verbose, column_type_hints=[str,str,str,str,str,str,str,str,str,str])

g = SGraph()
g = g.add_vertices(organizations, vid_field='path')
g = g.add_edges(acquisitions_edges, src_field='src', dst_field='dst')
g = g.add_edges(investments_investor_edges, src_field='src', dst_field='dst')
g = g.add_edges(investments_companies_edges, src_field='src', dst_field='dst')
g = g.add_vertices(categories,vid_field='path')
g = g.add_edges( categories_edges,src_field='src',dst_field='dst')
g = g.add_vertices(funding_rounds,vid_field='path')
g = g.add_edges( funding_rounds_edges,src_field='src',dst_field='dst')
g = g.add_vertices(images,vid_field='path')
g = g.add_edges( images_edges,src_field='src',dst_field='dst')
g = g.add_vertices(keywords, vid_field='path')
g = g.add_edges(keywords_descriptions_edges, src_field='url', dst_field='keyword')
g = g.add_edges(keywords_webpages_edges, src_field='url', dst_field='keyword')
g = g.add_vertices(news,vid_field='url')
g = g.add_edges( news_edges,src_field='src',dst_field='dst')
g = g.add_vertices(offices,vid_field='path')
g = g.add_edges( offices_edges,src_field='src',dst_field='dst')
g = g.add_vertices(person,vid_field='path')
g = g.add_edges( person_edges,src_field='src',dst_field='dst')
g = g.add_vertices(product,vid_field='path')
g = g.add_edges( product_edges,src_field='src',dst_field='dst')
g = g.add_vertices(website,vid_field='url')
g = g.add_edges( website_edges,src_field='src',dst_field='dst')
g = g.add_vertices(website,vid_field='url')
g = g.add_vertices(companies_acquired_by_sap,vid_field='path')
g = g.add_edges( companies_acquired_by_sap_edges,src_field='src',dst_field='dst')
g = g.add_edges( categories_of_companies_acquired_by_sap__edges,src_field='src',dst_field='dst')
g = g.add_edges( categories_keywords_edges,src_field='src',dst_field='dst')
print g.summary();

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
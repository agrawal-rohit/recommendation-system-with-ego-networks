import string
import re
from nltk.corpus import stopwords
from stemming.porter2 import stem
import networkx
import nltk
nltk.download('stopwords')

# RECOMMENDATIONS
#-----------------
import networkx
from operator import itemgetter
import matplotlib.pyplot as plt
import matplotlib as mpl

# Read the data from the amazon-books.txt and populate amazonProducts nested dictionary
# key = ASIN; value = MetaData associated with ASIN
fhr = open('amazon-books.txt', 'r', encoding='utf-8', errors='ignore')
amazonBooks = {}
fhr.readline()
for line in fhr:
    cell = line.split('\t')
    MetaData = {}
    MetaData['Id'] = cell[0].strip()
    ASIN = cell[1].strip()
    MetaData['Title'] = cell[2].strip()
    MetaData['Categories'] = cell[3].strip()
    MetaData['Group'] = cell[4].strip()
    MetaData['Copurchased'] = cell[5].strip()
    MetaData['SalesRank'] = int(cell[6].strip())
    MetaData['TotalReviews'] = int(cell[7].strip())
    MetaData['AvgRating'] = float(cell[8].strip())
    MetaData['DegreeCentrality'] = int(cell[9].strip())
    MetaData['ClusteringCoeff'] = float(cell[10].strip())
    amazonBooks[ASIN] = MetaData
fhr.close()

# Read the data from amazon-books-copurchase.edgelist and assign it to copurchaseGraph weighted Graph;
# node = ASIN; edge = copurchase, edge weight = category similarity
fhr = open("amazon-books-copurchase.edgelist", "rb")
copurchaseGraph = networkx.read_weighted_edgelist(fhr)
fhr.close()

# Now let's assume a person is considering buying the following book;
print("Looking for Recommendations for Customer purchasing this Book:")
print("\n------------------------------------------------------------")
# purchasedAsin = '0805047905'
purchasedAsin = '0875421210'

# Let's first get some metadata associated with this book
print("ASIN = ", purchasedAsin)
print("Title = ", amazonBooks[purchasedAsin]['Title'])
print("SalesRank = ", amazonBooks[purchasedAsin]['SalesRank'])
print("TotalReviews = ", amazonBooks[purchasedAsin]['TotalReviews'])
print("AvgRating = ", amazonBooks[purchasedAsin]['AvgRating'])
print("DegreeCentrality = ", amazonBooks[purchasedAsin]['DegreeCentrality'])
print("ClusteringCoeff = ", amazonBooks[purchasedAsin]['ClusteringCoeff'])

# Get the depth-1 ego network of purchasedAsin from copurchaseGraph
n = purchasedAsin
ego = networkx.ego_graph(copurchaseGraph, n, radius=1)
purchasedAsinEgoGraph = networkx.Graph(ego)
pos = networkx.layout.spring_layout(purchasedAsinEgoGraph)
M = purchasedAsinEgoGraph.number_of_edges()
nodes = networkx.draw_networkx_nodes(purchasedAsinEgoGraph, pos, node_size=50, node_color='blue')
edges = networkx.draw_networkx_edges(purchasedAsinEgoGraph, pos, node_size=50, edge_cmap=plt.cm.Blues, width=2, alpha=0.1)
ax = plt.gca()
ax.set_axis_off()
plt.title('Degree-1 Ego Network')
plt.figure(0)
plt.show()

# Use the island method on purchasedAsinEgoGraph to only retain edges with Threshold >= 0.5
threshold = 0.5
purchasedAsinEgoTrimGraph = networkx.Graph()
for f,t,e in purchasedAsinEgoGraph.edges(data=True):
    if e['weight'] >= threshold:
        purchasedAsinEgoTrimGraph.add_edge(f,t, weight=e['weight'])
pos = networkx.layout.spring_layout(purchasedAsinEgoTrimGraph)
M = purchasedAsinEgoTrimGraph.number_of_edges()
nodes = networkx.draw_networkx_nodes(purchasedAsinEgoTrimGraph, pos, node_size=50, node_color='blue', label=True)
edges = networkx.draw_networkx_edges(purchasedAsinEgoTrimGraph, pos, node_size=50, edge_cmap=plt.cm.Blues, width=2, alpha=0.1)
ax = plt.gca()
ax.set_axis_off()
plt.title('Degree-1 Ego Network Trimmed using threshold of 0.5')
plt.figure(1)
plt.show()

# Get the list of nodes connected to the purchasedAsin
purchasedAsinNeighbours = purchasedAsinEgoTrimGraph.neighbors(purchasedAsin)

# Get Top Five book recommendations from among the purchasedAsinNeighbours based on one or more of the following data of the 
# neighbouring nodes: SalesRank, AvgRating, TotalReviews, DegreeCentrality, and ClusteringCoeff

# Accessing metadata with ASIN in purchasedAsinNeighbours
AsMeta = []
for asin in purchasedAsinNeighbours:
    ASIN = asin
    Title = amazonBooks[asin]['Title']
    SalesRank = amazonBooks[asin]['SalesRank']
    TotalReviews = amazonBooks[asin]['TotalReviews']
    AvgRating = amazonBooks[asin]['AvgRating']
    DegreeCentrality = amazonBooks[asin]['DegreeCentrality']
    ClusteringCoeff = amazonBooks[asin]['ClusteringCoeff']
    AsMeta.append((ASIN, Title, SalesRank, TotalReviews, AvgRating, DegreeCentrality, ClusteringCoeff))
    
# Sorting the top five nodes in purchasedAsinNeighbour by Average Rating then by TotalReviews
T5_byAvgRating_then_byTotalReviews = sorted(AsMeta, key=lambda x: (x[4], x[3]), reverse=True)[:5]

# Print Top 5 Recommendations
print('\nTop 5 Recommendations by AvgRating then by TotalReviews for Users Purchased the book:')
print('\n------------------------------------------------------------------------------------')
print('ASIN\t', 'Title\t', 'SalesRank\t', 'TotalReviews\t', 'AvgRating\t', 'DegreeCentrality\t', 'ClusteringCoeff')
for asin in T5_byAvgRating_then_byTotalReviews:
    print(asin)
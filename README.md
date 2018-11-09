# Graph based Recommendation System

## Objective
Amazon Book Recommendation with Social Network Analysis based on co-purchase data. This method would work equally well for other item groups in the dataset eg. DVDs, Music CDs, etc

## Dataset Information
Dataset used: [Amazon product co-purchasing network metadata](http://snap.stanford.edu/data/amazon-meta.html)

The dataset contains product metadata and review information about 548,552 different products. For each product the following information is available:
1. **Product ID:** numeric values (0,1,2….,548,551)
2. **ASIN:** Amazon Standard Identification Number is a 10-character alphanumeric
UID assigned by Amazon for product identification.
3. **Title:** Name of the Product.
4. **Group:** Product type, could be books, music CDs, DVDs and VHS video tapes.
5. **SalesRank:** Representation of the sales of that product compared to the others in
its category.
6. **Similar:** ASINs of co-purchased products i.e., people who buy A also buy B.
7. **Categories:** Gives the specification of the product’s category hierarchy, e.g., genre
etc. (separated by |, category id in [ ]).
8. **Reviews:** Product’s review information -
- Total Number of Reviews
- Average Rating
- Individual customer review with time, user id, rating, total number of votes on the review and the number of people who found the review helpful.

The data was collected by crawling the Amazon website. This was done in the summer of
2006.

## Preprocessing
The data on ASIN is used as the key and the other data as the metadata associated with that particular ASIN. Preprocessing was required to read the file as RDBMS:
- **ID:** the Product ID in the dataset.
-	**ASIN:** directly from the dataset.
-	**Title:** directly from the dataset.
-	**Categories:** Concatenation of all categories of that ASIN, then preprocessed as: conversion to lowercase, then stemmed, removal of: punctuation, digits, stop words, retention of unique words.
-	**Copurchased:** List of ASINs that were present in “similar” in the dataset and have metadata associated to them.
-	**SalesRank:** directly from the dataset.
-	**TotalReviews:** directly as the total number of reviews under “reviews” in the dataset.
-	**AvgRating:** directly as the average rating under “reviews” in the dataset.

The co-purchase data in this was used to create the copurchaseGraph Structure

## Graph structure
- **Nodes:** the ASINs
-	**Edges:** two ASINs had an edge if they were co-purchased.
-	**Edge weight:** This was determined on the basis of the category similarity of the products. This measure of similarity is generated using the “Category” data as:

<a href="https://www.codecogs.com/eqnedit.php?latex=Similarity&space;=&space;\frac{No.of&space;words&space;that&space;are&space;common&space;between&space;Categories&space;of&space;connected&space;nodes}{Total&space;no.of&space;words&space;in&space;both&space;Categories&space;of&space;connected&space;nodes}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Similarity&space;=&space;\frac{No.of&space;words&space;that&space;are&space;common&space;between&space;Categories&space;of&space;connected&space;nodes}{Total&space;no.of&space;words&space;in&space;both&space;Categories&space;of&space;connected&space;nodes}" title="Similarity = \frac{No.of words that are common between Categories of connected nodes}{Total no.of words in both Categories of connected nodes}" /></a>
where, 	 0 ≤Similarity≤1
such that:  0 is the least similar and 1 the most similar.

Following graph related measures were also added:
-	DegreeCentrality: This is the measure of centrality. As the graph is undirected, it is defined as count of the number of neighbors a node has. 
-	 ClusteringCoeff: By definition this is a measure of the degree to which nodes in a graph tend to cluster together.

In the analysis, concept of **EGO NETWORKS** is used. In such a network, we take a focal node call it the “ego”, and the nodes that have edges with the ego are termed as the “alters”. Each alter of an ego network forms their own ego network. The intertwining of all the ego networks forms the social network. 

![Ego Network](https://user-images.githubusercontent.com/29514438/48280888-fc030700-e47a-11e8-8d4a-b0c2c14bd1a3.PNG)

## Recommendations
Using the ASIN (0875421210), we can obtain the metadata associated with that book - 
![Test Item](https://user-images.githubusercontent.com/29514438/48280932-1a690280-e47b-11e8-85bb-07df96e3664c.jpg)

We get the degree-1 ego network by taking the books that have been co-purchased with this one previously. Then we proceed to narrow it further down to the most similar books. This is done by using the island method on the degree-1 graph. Only the edges with threshold>= 0.5 are retained. And hence we obtain the trimmed graph which contains neighbors of the node with ASIN (0875421210).
![Ego Graph](https://user-images.githubusercontent.com/29514438/48280947-2228a700-e47b-11e8-8f8f-80ae25991478.png)
![Ego Trim Graph](https://user-images.githubusercontent.com/29514438/48280945-2228a700-e47b-11e8-86d0-d357c6272b21.png)

Top Five Recommendations are then taken based on the similarity measures that are associated with the neighbors in this trimmed graph. In this example, The similarity metrics used are: first by AvgRating and then by TotalReviews.

## Result
![Output](https://user-images.githubusercontent.com/29514438/48280946-2228a700-e47b-11e8-91e7-6371ed960670.PNG)


# Recommendation System using Graph Network Analysis

![Output](https://user-images.githubusercontent.com/29514438/48280946-2228a700-e47b-11e8-91e7-6371ed960670.PNG)

## Objective
This project demonstrates the use of Social Network Analysis in building a recommendation system using Amazon's book co-purchase data. The methodology is adaptable to other product categories such as DVDs and Music CDs.

## Dataset Information
**Source:** [Amazon product co-purchasing network metadata](http://snap.stanford.edu/data/amazon-meta.html)

**Content:**
- **Product ID:** Numeric (0 to 548,551).
- **ASIN:** Amazon Standard Identification Number (10-character alphanumeric).
- **Title:** Product name.
- **Group:** Category (e.g., books, music CDs, DVDs, VHS).
- **SalesRank:** Sales ranking within its category.
- **Similar Products:** ASINs of co-purchased items.
- **Categories:** Product category hierarchy.
- **Reviews:** Number, average rating, and details of individual reviews.
- **Collection Period:** Summer of 2006.

## Data Preprocessing

Processed fields include:
- **ID, ASIN, Title, SalesRank, TotalReviews, AvgRating:** Extracted directly.
- **Categories:** Concatenated, converted to lowercase, stemmed and filtered (removing punctuation, digits, stop words) to retain unique words.
- **Copurchased:** Extracted from the **"Similar Products"** field, filtered to include only ASINs with associated metadata.


## Graph Structure
- **Nodes:** Represent ASINs.
-	**Edges:** Link co-purchased ASINs.
-	**Edge weight:** Calculated based on category similarity, ranging from 0 (least similar) to 1 (most similar).

<a href="https://www.codecogs.com/eqnedit.php?latex=Similarity&space;=&space;\frac{No.of&space;words&space;that&space;are&space;common&space;between&space;Categories&space;of&space;connected&space;nodes}{Total&space;no.of&space;words&space;in&space;both&space;Categories&space;of&space;connected&space;nodes}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Similarity&space;=&space;\frac{No.of&space;words&space;that&space;are&space;common&space;between&space;Categories&space;of&space;connected&space;nodes}{Total&space;no.of&space;words&space;in&space;both&space;Categories&space;of&space;connected&space;nodes}" title="Similarity = \frac{No.of words that are common between Categories of connected nodes}{Total no.of words in both Categories of connected nodes}" /></a>
where, 	 0 ≤Similarity≤1
such that:  0 is the least similar and 1 the most similar.

### Graph Measures:
- **DegreeCentrality:** Number of connections each node has.
- **ClusteringCoeff:** Indicates the extent to which nodes cluster together.

In the analysis, the concept of **Ego Networks** is used. In such a network, we take a focal node and call it the “ego”, and the nodes that have edges with the ego are termed the “alters”. Each alter of an ego network forms its own ego network. The intertwining of all the ego networks forms the social network. 

![Ego Network](https://user-images.githubusercontent.com/29514438/48280888-fc030700-e47a-11e8-8d4a-b0c2c14bd1a3.PNG)

## Recommendation Methodology
1. **Initial Step:** Select a product ASIN (e.g., 0875421210) and retrieve its metadata.
2. **Ego Network Creation:** Construct a degree-1 ego network based on co-purchased books.
   
   ![Ego Graph](https://user-images.githubusercontent.com/29514438/48280947-2228a700-e47b-11e8-8f8f-80ae25991478.png)
4. **Graph Trimming:** Apply the island method with a threshold ≥ 0.5 to narrow down similar books.
   
   ![Ego Trim Graph](https://user-images.githubusercontent.com/29514438/48280945-2228a700-e47b-11e8-86d0-d357c6272b21.png)
6. **Recommendations:** Select the top five similar books based on **"AvgRating"** and **"TotalReviews"**.

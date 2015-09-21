###nuclei-analysis
===================

a hadoop-gis project for data analytics.

#####Problem Statement:
Given set of Si of polygons (nuclei), compute feature vectors Fi from Pathology images.  Be creative about choice of features.  Examples:

* Mask area, perimeter,  shape
* Within-mask texture
* Padded region texture

Develop an interactive program that supports the following:

1. Select subset of features
2. Select number of clusters
3. Choose initial cluster centroids by random choice of data points 
4. Invoke  K-means clustering algorithm to cluster feature vectors 
5. Display clusters generated by clustering algorithm, cluster centroids along with within-cluster sum of squares 
6. Store clusters from Si : assignment of data points to clusters, initial cluster centroids, within-cluster sum of squares,  feature subset in database and all other metadata needed to re-run computation

#####TODO after Phase 1:
1. UI Features
  - [ ] Move to proper cluster section from nav menu
  - [x] Pick a single query dropodown and place it properly
  - [x] Remove dummy images from work and put workflow images
  - [x] Display polygons in a info section from cluster
  - [x] Custom query option redesign and work with actual data
2. Back-end
  - [x] Run whole slide images
  - [ ] Figure out how to use cluster power
  - [ ] Use mongo-db to prepopulate tables
  - [x] Fix bug to populate clusters from predefined queries

####Phase 2
#####Requirements
* Logon to eagle bmi cluster and add anaconda module.
* Clone this repository and set root path of dataNode.
* Feature Extraction: python analysis.py
* Run flask server: python hackrpi/run.py
* Access web interface from http://localhost:5000


## Unsupervised Crop-Classification using Multi-Spectral Satellite Imagery

This repo is used for crop classification using unsupervised Machine Leaning (K-Means clustering)

Installation
-----
For a manual installation get this package:

    wget https://github.com/sumit-maan/crop-classification
    cd crop-classification

Install the package (python 3.0 and above):

    python setup.py install

Example
--------
    from unsupcc import executer

    # getting indices layer stack for an AOI
        ie = executer.IndexExecuter()
        ie.get_layer_stack()
    #provide the asked input and it will return the path where layer stack is stored

    # get crop clusters from layer stack of multiple dates
        ce = executer.ClusterExecuter()
        ce.crop_classifier(indice_stack_path, date_bands, number_of_clusters)
    #It will return a raster containing clusters of multiple crops


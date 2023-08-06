from label.loader import *
import os
from operator import itemgetter
from fuzzycmeans import FCM
from detect.Detection import Detection
from label import model_construction
import pandas as pd
import numpy as np
import commons
import logging
from label import features
from commons.logger import set_config
logger = set_config(logging.getLogger(__name__))
np.set_printoptions(suppress=True)

TEST = False
TOP_K = 10  # return the top k properties in the classify function


def classify(kind, class_uri, columns):
    """
    :param kind:
    :param class_uri:
    :param columns: expecting a list of list
    :return: list of predictions
            each prediction is a pair of (membership_val, property_uri)
    """
    predictions = []
    model_fdir = model_construction.build_model(class_uri=class_uri)
    fcm, centroid_names, max_num_of_features = load_model(kind, model_fdir)
    if fcm is None:
        logger.debug("empty fcm model")
        return []
    for col in columns:
        logger.debug("detect column kind")
        d = Detection(col)
        nums = d.cleanValues
        # Not sure if it is needed here
        # detected_kind = d.getType()
        logger.debug("compute features")
        feats = features.compute_features(kind=kind, nums=nums)
        if feats is None:
            predictions.append([])
            continue
        # print("feats: "+str(feats))
        if kind == commons.CATEGORICAL:
            logger.debug("add trailing zeros to categorical features")
            if max_num_of_features > len(feats):
                feats += [0 for i in range((max_num_of_features)-len(feats))]
        data_array = np.array([feats])
        #data_array = data_array.transpose()
        # print(data_array)
        logger.debug("predict the cluster for the given column")
        pred = fcm.predict(data_array)
        pred_with_names = zip(pred[0], centroid_names)
        pred_with_names = sorted(pred_with_names, key=lambda x: x[0], reverse=True)
        # pred_with_names.sort(key=itemgetter(0), reverse=True)
        #logger.debug(str(pred_with_names))
        predictions.append(pred_with_names[:TOP_K])
    return predictions


def load_model(kind, model_fdir):
    """
    Get FCM model from the model file
    :param kind:
    :param model_fdir:
    :return:
    """
    df = pd.read_csv(model_fdir, delimiter='\t', names=['property_uri', 'kind', 'features'])
    dfkind = df[df.kind == kind]
    # print(dfkind.columns.values)
    centroids = []
    #centroids_names = list(df['property_uri'])
    centroids_names = []
    # centroids_names = [p for p in df['property_uri']]
    for idx, row in dfkind.iterrows():
    #for r in dfkind['features']:
        # print(r)
        # print(type(r))

        r = row['features']
        centroids_names.append(row['property_uri'])
        centroid = [float(num) for num in r.split(',')]
        centroids.append(centroid)

    # This is to fix for categorical
    max_num_features = 0
    if kind == commons.CATEGORICAL:  # has variant num of features
        for c in centroids:
            dim = len(c)
            if dim > max_num_features:
                max_num_features = dim

        for c in centroids:
            num_feats = len(c)
            if num_feats < max_num_features:
                additionals = max_num_features-num_feats
                for i in range(additionals):
                    c.append(0)
        logger.debug("for categorical max_num_features: "+str(max_num_features))
    if len(centroids) == 0:
        return None, None, None
    fcm = FCM(n_clusters=len(centroids))
    # print("centroids: "+str(centroids))
    # print("len: "+str(len(centroids)))
    fcm.fit(centroids, range(len(centroids)))
    logger.debug("centroids: "+str(centroids))
    logger.debug("fcm centroids: "+str(fcm.cluster_centers_))
    logger.debug("membership: ")
    logger.debug("\n"+str(fcm.u))
    return fcm, centroids_names, max_num_features


if __name__ == '__main__':
    # fname = "dbpedia.org__ontology__BadmintonPlayer.tsv.test"
    # model_fdir = os.path.join(commons.models_dir, fname)
    # load_model(commons.COUNTS, model_fdir)

    # print features.compute_features(kind=commons.OTHER, nums=[1,2,3,4,5,5,-20])

    class_uri = "http://dbpedia.org/ontology/BadmintonPlayer"
    data = [
        range(1, 100, 3)
    ]
    classify(kind=commons.OTHER, class_uri=class_uri, columns=data)


    # data = [
    #     [1,2,1,2,1,2,1,2,3,4]
    # ]
    # classify(kind=commons.CATEGORICAL, class_uri=class_uri, columns=data)
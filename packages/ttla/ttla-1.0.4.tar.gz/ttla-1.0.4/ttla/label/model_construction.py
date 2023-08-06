from label.loader import *
import commons
import detect
from label.features import compute_features
import os
import sys
from multiprocessing import Process, Pipe
from PPool.Pool import Pool
# from TPool.TPool import Pool
# from threading import Lock
from easysparql.easysparqlclass import EasySparql

import logging
from commons.logger import set_config
logger = set_config(logging.getLogger(__name__))

NUM_OF_PROCESSES = 20
ENDPOINT = commons.ENDPOINT
TEST = False


def features_gatherer(reciever_p, sender_p):
    """
    :param d:
    :param input_p:
    :param output_p:
    :return:
    """
    pairs = []
    while True:
        d = reciever_p.recv()
        if d is None:
            for pair in pairs:
                sender_p.send(pair)
            sender_p.send(None)
            logger.debug("gatherer sent all the pairs")
            return
        else:
            pairs.append(d)


def features_and_kinds_func(class_uri, property_uri, pipe):
    """
    :param property_uri:
    :return:
    """
    easysparql = EasySparql(endpoint=commons.ENDPOINT, cache_dir=commons.CACHE_DIR)
    values = easysparql.get_objects(class_uri=class_uri, property_uri=property_uri)
    logger.debug("got %d objects for property %s" % (len(values), property_uri))
    nums = commons.get_numerics_from_list(values)
    if nums and len(nums) > commons.MIN_NUM_NUMS:
        print("\n\n*********\n\nKEEPING: %s" % property_uri)
        logger.debug("%d of them are nums of property %s" % (len(nums), property_uri))
        kind, new_nums = detect.get_kind_and_nums(nums)
        logger.debug("detect kind: %s for property %s" % (kind, property_uri))
        features = compute_features(kind=kind, nums=new_nums)
        if features is None:
            logger.debug("No features for property %s" % property_uri)
            return

        logger.debug("property %s features: %s" % (property_uri, str(features)))
        pair = {
            'kind': kind,
            'features': features,
            'property_uri': property_uri,
        }
        print("Sending to pipe: %s" % str(pair))
        pipe.send(pair)
    else:
        print("skipping: %s\n\n" % property_uri)


def get_features_and_kinds_multi_thread(class_uri):
    """
    :param class_uri:
    :return:
    """
    logger.debug("ask for properties for %s" % class_uri)
    easysparql = EasySparql(endpoint=commons.ENDPOINT, cache_dir=commons.CACHE_DIR)
    properties = easysparql.get_class_properties(class_uri=class_uri, min_num=commons.MIN_NUM_NUMS)
    print("get_features_and_kinds_multi_thread> properties: ")
    print(properties)
    logger.debug("properties: "+str(len(properties)))
    features_send_pipe, features_recieve_pipe = Pipe()
    gatherer_send_pipe, gatherer_reciever_pipe = features_send_pipe, features_recieve_pipe
    gatherer = Process(target=features_gatherer, args=(gatherer_reciever_pipe, gatherer_send_pipe))
    gatherer.start()
    params = []
    for p in properties:
        params.append((class_uri, p, features_send_pipe))

    logger.debug("running the pool")
    pool = Pool(max_num_of_processes=NUM_OF_PROCESSES, func=features_and_kinds_func, params_list=params)
    pool.run()
    logger.debug("finished the pool")
    features_send_pipe.send(None)
    logger.debug("receiving the pairs from the gatherer")
    fk_pairs = []
    fk_pair = features_recieve_pipe.recv()
    while fk_pair is not None:
        fk_pairs.append(fk_pair)
        fk_pair = features_recieve_pipe.recv()
    logger.debug("waiting for the gathere")
    gatherer.join()
    logger.debug("gatherer finished")
    # print("fk pairs: "+str(fk_pairs))
    # fk_pairs = []
    # fk_pair = features_recieve_pipe.recv()
    # while fk_pair is not None:
    #     fk_pairs.append(fk_pair)
    #     fk_pair = features_recieve_pipe.recv()

    # fk_pairs = features_recieve_pipe.recv()
    return fk_pairs


# This is no longer in use, we replaced it with multi-threaded function
# def get_features_and_kinds(class_uri):
#     """
#     :param class_uri:
#     :return:
#     """
#     fk_pairs = []
#     logger.debug("ask for properties")
#     properties = commons.get_properties(class_uri=class_uri, endpoint=ENDPOINT)
#     logger.debug("properties: "+str(len(properties)))
#     for p in properties:
#         # if p != "http://dbpedia.org/property/beds":
#         #     continue
#         logger.debug("objects for property: "+p)
#         values = commons.get_objects(endpoint=ENDPOINT, class_uri=class_uri, property_uri=p)
#         logger.debug("got %d objects" % len(values))
#         nums = commons.get_numerics_from_list(values)
#         if nums and len(nums) > commons.MIN_NUM_NUMS:
#             logger.debug("%d of them are nums" % len(nums))
#             kind, new_nums = detect.get_kind_and_nums(nums)
#             logger.debug("detect kind: "+kind)
#             features = compute_features(kind=kind, nums=new_nums)
#             if features is None:
#                 logger.debug("No features")
#                 continue
#             logger.debug("computed features: "+str(features))
#             pair = {
#                 'kind': kind,
#                 'features': features,
#                 'property_uri': p,
#             }
#             fk_pairs.append(pair)
#     return fk_pairs


def build_model(class_uri):
    """
    :param class_uri:
    :return: the directory of the model
    """
    logger.debug("class uri: "+class_uri)
    fname = commons.class_uri_to_fname(class_uri=class_uri)
    logger.debug("fname: "+fname)
    model_fdir = os.path.join(commons.models_dir, fname)+'.tsv'
    if TEST:
        model_fdir += '.test'
        f = open(model_fdir, 'w')
        f.close()
        os.remove(model_fdir)

    logger.debug("model_fdir: "+model_fdir)
    if os.path.isfile(model_fdir):
        logger.debug("Model already exists")
        return model_fdir

    # if multi_threading:
    #     print("multi threading")
    #     features_and_kinds = get_features_and_kinds_multi_thread(class_uri=class_uri)
    # else:
    #     print("single thread")
    #     features_and_kinds = get_features_and_kinds(class_uri=class_uri)

    features_and_kinds = get_features_and_kinds_multi_thread(class_uri=class_uri)

    print("features and kinds: ")
    print(features_and_kinds)

    model_txt = ""
    logger.debug("num of features and kinds: %d" % (len(features_and_kinds)))
    for fk in features_and_kinds:
        features_txt = ",".join([str(f) for f in fk['features']])
        line = "%s\t%s\t%s\n" % (fk['property_uri'], fk['kind'], features_txt)
        model_txt += line
    f = open(model_fdir, 'w')
    # f.write(model_txt.encode('utf-8'))
    f.write(model_txt)
    f.close()
    return model_fdir


if __name__ == '__main__':
    if len(sys.argv) == 2:
        build_model(sys.argv[1])
import logging
import os
import shutil

from offline_model_builder.common.read_write_s3 import ConnectS3
from offline_model_builder.user_profile.clustering.centroids_generator import CentroidGenerator
from offline_model_builder.user_profile.clustering.cluster_generator import ClusterGenerator
from offline_model_builder.user_profile.clustering.evaluation.constants import NON_FEATURES
from offline_model_builder.user_profile.constants import CUSTOMER_ID, CSV_EXTENSION, ENSEMBLE_IR1_PATH, \
    ENSEMBLE_IR2_PATH, ENSEMBLE_IR3_PATH, ENSEMBLE_IR4_PATH, \
    INTERMEDIATE_RESULTS_DIRECTORY, PAYTVPROVIDER_ID, S3_PAYTV_PREFIX, S3_NONPAYTV_PREFIX

logging.basicConfig(level=logging.INFO)


class ClusterFeaturesGenerator:

    @staticmethod
    def release_intermediate_resources():
        directories = [
            ENSEMBLE_IR1_PATH,
            ENSEMBLE_IR2_PATH,
            ENSEMBLE_IR3_PATH,
            ENSEMBLE_IR4_PATH
        ]
        for directory in directories:
            location = INTERMEDIATE_RESULTS_DIRECTORY + "/"
            path = os.path.join(location, directory)
            try:
                shutil.rmtree(path)
            except Exception:
                logging.error("Error in removing directory subtree")

    @staticmethod
    def create_cluster_features(
            resource,
            s3_bucket_name,
            s3_object_name,
            user_profile,
            paytv: bool,
            connection_object=None
    ):
        user_profile[PAYTVPROVIDER_ID] = \
            user_profile[PAYTVPROVIDER_ID].fillna("").apply(list)
        for index in range(len(user_profile)):
            if len(user_profile.loc[index, PAYTVPROVIDER_ID]) == 0:
                user_profile.loc[index, PAYTVPROVIDER_ID] = -1
                continue
            paytvprovider_id = user_profile.loc[index, PAYTVPROVIDER_ID]
            user_profile.loc[index, PAYTVPROVIDER_ID] = \
                (paytvprovider_id[0])[PAYTVPROVIDER_ID]

        cluster_generator = ClusterGenerator(
            data=user_profile
        )
        cluster_generator.controller(paytv)

        cg = CentroidGenerator(
            user_features=user_profile,
            user_clusters=cluster_generator.clusters,
            connection_object=connection_object
        )
        cg.compute_centroids(
            s3_bucket_name=s3_bucket_name,
            s3_object_name=s3_object_name,
            resource=resource,
            paytv=paytv
        )
        print("Successfully dumped all the centroids data into S3...")

        for feature in NON_FEATURES:
            if feature == CUSTOMER_ID:
                continue
            rel = cluster_generator.clusters[[CUSTOMER_ID, feature]]

            feature = S3_PAYTV_PREFIX + feature if paytv \
                else S3_NONPAYTV_PREFIX + feature

            ConnectS3().write_csv_to_s3(
                bucket_name=s3_bucket_name,
                object_name=s3_object_name + feature + CSV_EXTENSION,
                df_to_upload=rel,
                resource=resource
            )
        # ClusterFeaturesGenerator.release_intermediate_resources()

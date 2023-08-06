from pandas import DataFrame, Series, get_dummies
from sklearn.cluster import MiniBatchKMeans

from offline_model_builder.user_profile.clustering.clustering_utils import ClusteringUtils
from offline_model_builder.user_profile.clustering.config import K_PAYTV, K_NO_PAYTV, MINIBATCH_SIZE
from offline_model_builder.user_profile.constants import CUSTOMER_ID, MINIBATCH_KMEANS_FEATURE, BIRTHDAY, \
    CUSTOMER_CREATED_ON, \
    CUSTOMER_MODIFIED_ON, PAYTVPROVIDER_ID, GENDER, UD_KEY, IS_PAY_TV, GENDER_NAN


class ClusterGenerator(ClusteringUtils):

    def __init__(
            self,
            data=DataFrame
    ):
        data[CUSTOMER_ID] = data[CUSTOMER_ID].astype(str)
        ClusteringUtils.__init__(self, data=data)
        self.clusters = DataFrame()

    def get_minibatch_kmeans(
            self,
            features: DataFrame,
            paytv: bool
    ) -> Series:
        """
        Generate MiniBatch-KMeans clusters
        :param features: user features
        :return: list of assigned cluster values
        """
        if paytv:
            k = K_PAYTV
        else:
            k = K_NO_PAYTV
        model = MiniBatchKMeans(n_clusters=k, random_state=0,
                                batch_size=MINIBATCH_SIZE)
        return model.fit_predict(features)

    def controller(
            self,
            paytv: bool
    ):
        """
        Driver function for Cluster based feature
        processing and results generation
        :return: None
        """
        import time

        start = time.time()
        features = self.drop_sparse_features()
        end = time.time()
        print(end - start)
        self.clusters[CUSTOMER_ID] = features[CUSTOMER_ID]

        features = get_dummies(
            features,
            columns=[GENDER, PAYTVPROVIDER_ID]
        )

        # since we do not want to pass an identifier as a clustering feature
        if paytv:
            features = self.remove_attributes(attributes=features,
                                              to_drop=[CUSTOMER_ID,
                                                       BIRTHDAY,
                                                       CUSTOMER_CREATED_ON,
                                                       CUSTOMER_MODIFIED_ON,
                                                       IS_PAY_TV,
                                                       UD_KEY,
                                                       GENDER_NAN])
        else:
            features = self.remove_attributes(attributes=features,
                                              to_drop=[CUSTOMER_ID,
                                                       BIRTHDAY,
                                                       CUSTOMER_CREATED_ON,
                                                       CUSTOMER_MODIFIED_ON,
                                                       UD_KEY,
                                                       GENDER_NAN])

        self.clusters[MINIBATCH_KMEANS_FEATURE] = self.get_minibatch_kmeans(features=features, paytv=paytv)

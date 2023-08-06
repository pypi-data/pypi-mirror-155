import pickle
import time
from sklearn.decomposition import PCA


class FeaturesReduction:

    @staticmethod
    def pca_reduction(input_file, pca_factor, output_file):
        pkl_file = open(input_file, 'rb')
        data = pickle.load(pkl_file)
        pkl_file.close()

        print("Starting reduction phase......")
        print("")
        start_time = time.time()

        # The real magic happens here
        n_features = 50
        num_components = n_features * pca_factor
        pca = PCA(n_components=num_components)
        result = pca.fit_transform(data)

        output = open(output_file, "wb")
        pickle.dump(pca, output)
        pickle.dump(data, output)
        output.close()

        print("DATA Saved")

        end_time = time.time()
        print(f"Runtime of the program is {end_time - start_time} seconds")
        pass

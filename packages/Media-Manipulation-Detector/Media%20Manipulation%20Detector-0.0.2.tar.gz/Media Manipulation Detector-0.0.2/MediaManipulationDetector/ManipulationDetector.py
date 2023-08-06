import os

from MediaManipulationDetector.ModelCreation import ModelCreation
from MediaManipulationDetector.FeaturesExtraction import FeaturesExtraction
from MediaManipulationDetector.FeaturesReduction import FeaturesReduction


class ManipulationDetector:

    @staticmethod
    def create_file(mode="train", src_dir="/", number_features=50, max_files=1000, pre_processing="dft", pca_reduction=0, out_file="output"):
        if os.path.isdir(src_dir) is False:
            print("Invalid source directory!")
            exit(0)

        output_file = out_file+".pkl"

        if pca_reduction != 0:
            temp_file = "temp"+output_file+".pkl"
            FeaturesExtraction.extract_features(src_dir,number_features,max_files,pre_processing,temp_file)
            FeaturesReduction.pca_reduction(temp_file, pca_reduction, output_file)
        else:
            FeaturesExtraction.extract_features(src_dir,number_features,max_files,pre_processing,output_file)
        pass

    @staticmethod
    def create_model(algo="svm", k_fold=0, src_file="input.pkl", testfile="none"):
        if k_fold == -1 and testfile == "none":
            print("For this k-fold please add a test file")
            exit(0)

        ModelCreation.create_model(algo, k_fold, src_file, testfile)
        pass

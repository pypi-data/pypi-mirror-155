from scipy.interpolate import griddata

from .RadialProfile import radialProfile
import pickle
import os
import cv2
import numpy as np
import time


class FeaturesExtraction:

    @staticmethod
    def extract_features(src_dir, features, max_files, pre_processing, output_filename):
        N = features
        number_iter = max_files

        data = {}

        print("Starting pre-processing phase......")
        print("")
        start_time = time.time()
        dir_folders = ["/fake", "/real"]
        dir_count = 0

        psd1D_total = np.zeros([number_iter, N])
        label_total = np.zeros([number_iter])
        psd1D_org_mean = np.zeros(N)
        psd1D_org_std = np.zeros(N)

        for cur_dir in dir_folders:
            count = 0
            full_dir = src_dir + cur_dir

            for subdir, dirs, files in os.walk(full_dir):
                for file in files:

                    filename = os.path.join(subdir, file)
                    if filename == src_dir + dir_folders[dir_count] + "\desktop.ini":
                        continue

                    img = cv2.imread(filename, 0)

                    if pre_processing == "fft":
                        f = np.fft.rfft2(img)
                    else:
                        f = np.fft.fft2(img)

                    fshift = np.fft.fftshift(f)

                    magnitude_spectrum = 20 * np.log(np.abs(fshift))
                    psd1D = radialProfile.azimuthalAverage(magnitude_spectrum)

                    # Calculate the azimuthally averaged 1D power spectrum
                    points = np.linspace(0, N, num=psd1D.size)  # coordinates of a
                    xi = np.linspace(0, N, num=N)  # coordinates for interpolation

                    interpolated = griddata(points, psd1D, xi, method='cubic')
                    interpolated /= interpolated[0]

                    psd1D_total[count, :] = interpolated
                    if cur_dir == dir_folders[0]:
                        label_total[count] = 0
                    else:
                        label_total[count] = 1
                    count += 1

                    if count == number_iter:
                        break
                if count == number_iter:
                    break

            for x in range(N):
                psd1D_org_mean[x] = np.mean(psd1D_total[:, x])
                psd1D_org_std[x] = np.std(psd1D_total[:, x])

            if dir_count == 0:
                psd1D_total_1 = psd1D_total
                label_total_1 = label_total
                psd1D_org_mean_1 = psd1D_org_mean
                psd1D_org_std_1 = psd1D_org_std
            elif dir_count == 1:
                psd1D_total_2 = psd1D_total
                label_total_2 = label_total
                psd1D_org_mean_2 = psd1D_org_mean
                psd1D_org_std_2 = psd1D_org_std

            dir_count += 1

        y = [psd1D_org_mean_1, psd1D_org_mean_2]
        error = [psd1D_org_std_1, psd1D_org_std_2]

        psd1D_total_final = np.concatenate((psd1D_total_1, psd1D_total_2), axis=0)
        label_total_final = np.concatenate((label_total_1, label_total_2), axis=0)

        data["data"] = psd1D_total_final
        data["label"] = label_total_final

        print("Number of items checked")
        print(len(label_total_final))

        output = open(output_filename, 'wb')
        pickle.dump(data, output)
        output.close()

        print("DATA Saved")

        end_time = time.time()
        print(f"Runtime of the program is {end_time - start_time} seconds")

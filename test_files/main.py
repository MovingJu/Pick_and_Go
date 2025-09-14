# calendar data flow test

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import math, json

async def main(date: int = 3):

    with open("./test_files/result_sample.json", "r") as file:
        data = json.load(file)

    data_full = data["food"]

    # with open("./test_files/sample.json", "w") as file:
    #     file.write(
    #         json.dumps(data_full, indent=4, ensure_ascii=False)
    #     )

    gps = []
    for i in data_full:
        if float(i["mapx"]) < 120 or float(i["mapx"]) > 130:
            continue
        if float(i["mapy"]) < 30 or float(i["mapy"]) > 40:
            continue

        gps.append(
            (
                float(i["mapx"]), float(i["mapy"])
            )
        )

    gps = np.array(gps)

    print(gps)

    xlim = (max(gps[:, 0]), min(gps[:, 0]))
    ylim = (max(gps[:, 1]), min(gps[:, 1]))

    # plt.scatter(gps[:, 0], gps[:, 1])
    # plt.xlabel("gpsx")
    # plt.ylabel("gpsy")
    # plt.savefig("./test_files/figs/scatter_gps1.png")

    kmean = KMeans(
        n_clusters=date, 
        random_state=42
    ).fit(gps)

    print(kmean.labels_)

    center = (sum(kmean.cluster_centers_[:, 0]) / date, sum(kmean.cluster_centers_[:, 1]) / date)

    print(center)

    labeled_gps = [[] for _ in range(3)]
    for idx, label in enumerate(kmean.labels_):
        labeled_gps[label].append(gps[idx])

    labeled_gps = [
        np.array(labeled_gps[i])
        for i in range(3)
    ]

    # for i in range(3):
    #     plt.scatter(labeled_gps[i][:, 0], labeled_gps[i][:, 1])
    # plt.scatter(center[0], center[1], marker="^")
    # plt.xlim(xlim)
    # plt.ylim(ylim)
    # plt.xlabel("gpsx")
    # plt.ylabel("gpsy")
    # plt.savefig("./test_files/figs/labeled1.png")

    def distance(center: tuple[float, float], arr: np.ndarray):
        return np.sqrt((arr[:, 0] - center[0])**2 + (arr[:, 1] - center[1])**2)

    # centerized_labeled_gps = []
    # for elem in labeled_gps:
    #     temp = elem[np.argsort(distance(center, elem))][:3]
    #     centerized_labeled_gps.append(temp)

    centerized_labeled_gps = []
    for idx, elem in enumerate(labeled_gps):
        temp = elem[np.argsort(distance(kmean.cluster_centers_[idx], elem))][:3]
        centerized_labeled_gps.append(temp)

    for i in range(3):
        plt.scatter(centerized_labeled_gps[i][:, 0], centerized_labeled_gps[i][:, 1])
    plt.scatter(center[0], center[1], marker="^")
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel("gpsx")
    plt.ylabel("gpsy")
    plt.savefig("./test_files/figs/labeled3.png")


    return
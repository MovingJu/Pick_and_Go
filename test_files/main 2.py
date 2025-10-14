# calendar data flow test

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import json

async def main():

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

    plt.scatter(gps[:, 0], gps[:, 1])
    plt.xlabel("gpsx")
    plt.ylabel("gpsy")
    plt.savefig("./test_files/figs/scatter_gps1.png")

    kmean = KMeans(
        n_clusters=3, 
        random_state=42
    ).fit(gps)

    print(kmean.labels_)

    labeled_gps = [[] for _ in range(3)]
    for idx, label in enumerate(kmean.labels_):
        labeled_gps[label].append(gps[idx])

    labeled_gps = [
        np.array(labeled_gps[i])
        for i in range(3)
    ]

    for i in range(3):
        plt.scatter(labeled_gps[i][:, 0], labeled_gps[i][:, 1])
    plt.xlabel("gpsx")
    plt.ylabel("gpsy")
    plt.savefig("./test_files/figs/labeled1.png")

    return
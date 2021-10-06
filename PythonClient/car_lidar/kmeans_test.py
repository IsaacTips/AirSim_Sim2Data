import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import airsim
import numpy
from sklearn.cluster import KMeans


def parse_lidarData(data):
    points = numpy.array(data.point_cloud, dtype=numpy.dtype('f4'))
    points = numpy.reshape(points, (int(points.shape[0]/3), 3))
    return points


# It uses the same point cloud as the lidar sensor
def animate(i, client):
    lidarData = client.getLidarData(lidar_name="LidarSensor")
    longrange1 = client.getLidarData(lidar_name='LongRangeRadar1')
    longrange2 = client.getLidarData(lidar_name='LongRangeRadar2')
    shortrange1 = client.getLidarData(lidar_name='ShortRangeRadar1')
    shortrange2 = client.getLidarData(lidar_name='ShortRangeRadar2')
    shortrange3 = client.getLidarData(lidar_name='ShortRangeRadar3')
    shortrange4 = client.getLidarData(lidar_name='ShortRangeRadar4')

    ax.clear()

    if(len(lidarData.point_cloud) >= 3):
        lidarPoints = parse_lidarData(lidarData)
        x, y, z = lidarPoints.T

        ax.scatter(y, x, s=10, color="black")

    # # In the case of radar, instead of mapping the whole point cloud, we just use one point
    if(len(longrange1.point_cloud) >= 3):
        longRangePoints1 = parse_lidarData(longrange1)
        lx1, ly1, lz1 = longRangePoints1.T
        df = pd.DataFrame({
            'x': lx1,
            'y': ly1
        })
        k = 3
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(df)
        labels = kmeans.predict(df)
        centroids = kmeans.cluster_centers_
        x, y = centroids.T
        print(x, y)
        # ax.scatter(df['y'], df['x'], c=labels.astype(float), edgecolor='k')
        ax.plot(y, x, 'ro-', color='green')

    # if(len(longrange2.point_cloud) >= 3):
    #     longRangePoints2 = parse_lidarData(longrange2)
    #     lx2, ly2, lz2 = longRangePoints2.T
    #     ax.plot([mean(ly2), 0], [mean(lx2), 0], 'ro-', color='green')

    # if(len(shortrange1.point_cloud) >= 3):
    #     shortRangePoints1 = parse_lidarData(shortrange1)
    #     sx1, sy1, sz1 = shortRangePoints1.T
    #     ax.plot([mean(sy1), 0], [mean(sx1), 0], 'ro-', color='red')

    # if(len(shortrange2.point_cloud) >= 3):
    #     shortRangePoints2 = parse_lidarData(shortrange2)
    #     sx2, sy2, sz2 = shortRangePoints2.T
    #     ax.plot([mean(sy2), 0], [mean(sx2), 0], 'ro-', color='red')

    # if(len(shortrange3.point_cloud) >= 3):
    #     shortRangePoints3 = parse_lidarData(shortrange3)
    #     sx3, sy3, sz3 = shortRangePoints3.T
    #     ax.plot([mean(sy3), 0], [mean(sx3), 0], 'ro-', color='red')

    # if(len(shortrange4.point_cloud) >= 3):
    #     shortRangePoints4 = parse_lidarData(shortrange4)
    #     sx4, sy4, sz4 = shortRangePoints4.T
    #     ax.plot([mean(sy4), 0], [mean(sx4), 0], 'ro-', color='red')

    ax.scatter(0, 0, s=400, marker="^")
    ax.set_xlim([-70, 70])
    ax.set_ylim([-70, 70])
    ax.axis('off')
    ax.grid(b=None)


plt.style.use('seaborn')  # Pre defined plot style template
fig = plt.figure()
ax = plt.subplot(1, 1, 1)
client = airsim.CarClient()  # Create an airsim client
client.confirmConnection()  # Confirm that the connection was successful

# This calls animate function every 5 ms
animation = FuncAnimation(fig, animate, fargs=(client,), interval=1)
plt.show()  # Show the plot

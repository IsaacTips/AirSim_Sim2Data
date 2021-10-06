
class DetectionInfo(MsgpackMixin):
    name = ''
    geo_point = GeoPoint()
    box2D = Box2D()
    box3D = Box3D()
    relative_pose = Pose()


class GeoPoint(MsgpackMixin):
    latitude = 0.0
    longitude = 0.0
    altitude = 0.0

class Box2D(MsgpackMixin):
    min = Vector2r()
    max = Vector2r()

class Box3D(MsgpackMixin):
    min = Vector3r()
    max = Vector3r()

class Pose(MsgpackMixin):
    position = Vector3r()
    orientation = Quaternionr()


class Vector2r(MsgpackMixin):
    x_val = 0.0
    y_val = 0.0

    def __init__(self, x_val = 0.0, y_val = 0.0):
        self.x_val = x_val
        self.y_val = y_val

class Vector3r(MsgpackMixin):
    x_val = 0.0
    y_val = 0.0
    z_val = 0.0

    def __init__(self, x_val = 0.0, y_val = 0.0, z_val = 0.0):
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val

class Quaternionr(MsgpackMixin):
    w_val = 0.0
    x_val = 0.0
    y_val = 0.0
    z_val = 0.0

    def __init__(self, x_val = 0.0, y_val = 0.0, z_val = 0.0, w_val = 1.0):
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val
        self.w_val = w_val
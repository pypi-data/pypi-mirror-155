from .fuelmap import Fuelmap
from .ignitionmap import Ignitionmap
from scipy.interpolate import interp2d


class FLS:
    def __init__(self, load, rpm) -> None:
        self.load = load
        self.rpm = rpm

    def lambdavalue(load=None, rpm=None):
        a_f_r = interp2d(Fuelmap.load, Fuelmap.rpm, Fuelmap.afr,
                         kind='linear', fill_value='-1')
        lambdavalue = (float(round(a_f_r(load, rpm)[0], 4))) / 14.7
        return lambdavalue

    def airfuelratio(load=None, rpm=None):
        a_f_r = interp2d(Fuelmap.load, Fuelmap.rpm, Fuelmap.afr,
                         kind='linear', fill_value='-1')
        airistofuelratio = float(round(a_f_r(load, rpm)[0], 4))
        return airistofuelratio

    def sparkangle(load=None, rpm=None):
        spang = interp2d(Ignitionmap.load, Ignitionmap.rpm, Ignitionmap.spark_angle,
                         kind='linear', fill_value='-1')
        sparkangle = float(round(spang(load, rpm)[0], 4))
        return sparkangle

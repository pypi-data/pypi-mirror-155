import matplotlib.pyplot as plt

from RWTHColors.colors import *
from cycler import cycler


class ColorManager:
    def __init__(self, frmt: str = "HEX"):
        if frmt not in ["HEX", "RGB"]:
            raise ValueError("frmt must be HEX or RGB not %s" % frmt)

        self.RWTHBlau = RWTHBlau()
        self.RWTHSchwarz = RWTHSchwarz()
        self.RWTHMagenta = RWTHMagenta()
        self.RWTHGelb = RWTHGelb()
        self.RWTHPetrol = RWTHPetrol()
        self.RWTHTuerkis = RWTHTuerkis()
        self.RWTHGruen = RWTHGruen()
        self.RWTHMaiGruen = RWTHMaiGruen()
        self.RWTHOrange = RWTHOrange()
        self.RWTHRot = RWTHRot()
        self.RWTHBordeaux = RWTHBordeaux()
        self.RWTHViolett = RWTHViolett()
        self.RWTHLila = RWTHLila()

        self.rwth_color_cycle = cycler(color=[self.RWTHBlau.p(100),
                                              self.RWTHOrange.p(100),
                                              self.RWTHGruen.p(100),
                                              self.RWTHRot.p(100),
                                              self.RWTHViolett.p(100),
                                              self.RWTHBordeaux.p(100),
                                              self.RWTHLila.p(100),
                                              self.RWTHPetrol.p(100),
                                              self.RWTHMaiGruen.p(100),
                                              self.RWTHTuerkis.p(100),
                                              ])

        plt.rcParams["axes.prop_cycle"] = self.rwth_color_cycle

        self.frmt = frmt

    @property
    def frmt(self):
        return self._frmt

    @frmt.setter
    def frmt(self, frmt: str = "HEX"):
        if frmt not in ["HEX", "RGB"]:
            raise ValueError("frmt must be HEX or RGB not %s" % frmt)

        self._frmt = frmt

        RWTHBlau.frmt = frmt
        RWTHSchwarz.frmt = frmt
        RWTHMagenta.frmt = frmt
        RWTHGelb.frmt = frmt
        RWTHPetrol.frmt = frmt
        RWTHTuerkis.frmt = frmt
        RWTHGruen.frmt = frmt
        RWTHMaiGruen.frmt = frmt
        RWTHOrange.frmt = frmt
        RWTHRot.frmt = frmt
        RWTHBordeaux.frmt = frmt
        RWTHViolett.frmt = frmt
        RWTHLila.frmt = frmt

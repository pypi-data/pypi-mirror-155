from ..sessioncontroll import (
    baseobj,
    strobj,
    txtobj,
    baseobj,
    intobj,
    colobj,
)


class SeisekiRaceData(baseobj):
    __tablename__ = "seisekirace"
    racekey = colobj(strobj, primary_key=True)
    furlongtime1 = colobj(intobj)
    furlongtime2 = colobj(intobj)
    furlongtime3 = colobj(intobj)
    furlongtime4 = colobj(intobj)
    furlongtime5 = colobj(intobj)
    furlongtime6 = colobj(intobj)
    furlongtime7 = colobj(intobj)
    furlongtime8 = colobj(intobj)
    furlongtime9 = colobj(intobj)
    furlongtime10 = colobj(intobj)
    furlongtime11 = colobj(intobj)
    furlongtime12 = colobj(intobj)
    furlongtime13 = colobj(intobj)
    furlongtime14 = colobj(intobj)
    furlongtime15 = colobj(intobj)
    furlongtime16 = colobj(intobj)
    furlongtime17 = colobj(intobj)
    furlongtime18 = colobj(intobj)
    corner1 = colobj(strobj)
    corner2 = colobj(strobj)
    corner3 = colobj(strobj)
    corner4 = colobj(strobj)
    paceupposition = colobj(intobj)
    truckbias1_in = colobj(strobj)
    truckbias1_center = colobj(strobj)
    truckbias1_out = colobj(strobj)
    truckbias2_in = colobj(strobj)
    truckbias2_center = colobj(strobj)
    truckbias2_out = colobj(strobj)
    truckbias_muko_in = colobj(strobj)
    truckbias_muko_center = colobj(strobj)
    truckbias_muko_out = colobj(strobj)
    truckbias3_in = colobj(strobj)
    truckbias3_center = colobj(strobj)
    truckbias3_out = colobj(strobj)
    truckbias4_saiuchi = colobj(strobj)
    truckbias4_in = colobj(strobj)
    truckbias4_center = colobj(strobj)
    truckbias4_out = colobj(strobj)
    truckbias4_oosoto = colobj(strobj)
    truckbias_straight_saiuchi = colobj(strobj)
    truckbias_straight_in = colobj(strobj)
    truckbias_straight_center = colobj(strobj)
    truckbias_straight_out = colobj(strobj)
    truckbias_straight_oosoto = colobj(strobj)
    comment = colobj(txtobj)

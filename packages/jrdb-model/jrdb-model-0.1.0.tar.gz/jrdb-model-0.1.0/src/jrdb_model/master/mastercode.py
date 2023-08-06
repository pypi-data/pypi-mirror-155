from ..sessioncontroll import (
    baseobj,
    strobj,
    baseobj,
    intobj,
    colobj,
)


class BacodeMaster(baseobj):
    __tablename__ = "bacodemaster"
    bacode = colobj(intobj, primary_key=True)
    baname = colobj(strobj)


class JuryoMaster(baseobj):
    __tablename__ = "juryomaster"
    juryo = colobj(intobj, primary_key=True)
    juryo_name = colobj(strobj)


class JokenMaster(baseobj):
    __tablename__ = "jokenmaster"
    joken = colobj(strobj, primary_key=True)
    joken_group = colobj(intobj)
    joken_name = colobj(strobj)


class JokenGroupMaster(baseobj):
    __tablename__ = "jokengroupmaster"
    joken_group = colobj(intobj, primary_key=True)
    joken_group_name = colobj(strobj)


class ShubetsuMaster(baseobj):
    __tablename__ = "shubetsumaster"
    shubetsu = colobj(intobj, primary_key=True)
    shubetsu_name = colobj(strobj)


class IjokbnMaster(baseobj):
    __tablename__ = "ijokbnmaster"
    ijo_kbn = colobj(intobj, primary_key=True)
    ijo_kbn_name = colobj(strobj)


class TenkoMaster(baseobj):
    __tablename__ = "tenkomaster"
    tenko = colobj(intobj, primary_key=True)
    tenko_name = colobj(strobj)


class RestreasoncodeMaster(baseobj):
    __tablename__ = "restreasoncodemaster"
    rest_reason_code = colobj(intobj, primary_key=True)
    rest_reason_name = colobj(strobj)


class LegtypeMaster(baseobj):
    __tablename__ = "legtypemaster"
    leg_type = colobj(intobj, primary_key=True)
    race_leg_type = colobj(strobj)
    leg_type_name = colobj(strobj)


class DistanceadjustMaster(baseobj):
    __tablename__ = "distanceadjustmaster"
    distance_adjust = colobj(intobj, primary_key=True)
    distance_name = colobj(strobj)

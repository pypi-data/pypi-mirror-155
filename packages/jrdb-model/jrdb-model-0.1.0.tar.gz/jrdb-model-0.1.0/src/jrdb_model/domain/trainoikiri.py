from ..sessioncontroll import (
    baseobj,
    strobj,
    baseobj,
    intobj,
    colobj,
    fkyobj,
)


class TrainOikiriData(baseobj):
    __tablename__ = "train_oikiri"
    racehorsekey = colobj(strobj, fkyobj("racehorse.racehorsekey"), primary_key=True)
    racekey = colobj(strobj)
    num = colobj(intobj)
    day_of_week = colobj(strobj)
    train_date = colobj(strobj)
    kaisu = colobj(intobj)
    train_course_code = colobj(strobj)
    oikiri_kind = colobj(intobj)
    oikiri_state = colobj(intobj)
    rider = colobj(intobj)
    train_f = colobj(intobj)
    ten_f = colobj(intobj)
    mid_f = colobj(intobj)
    end_f = colobj(intobj)
    ten_f_score = colobj(intobj)
    mid_f_score = colobj(intobj)
    end_f_score = colobj(intobj)
    oikiri_score = colobj(intobj)
    awase_result = colobj(strobj)
    aite_oikiri_kind = colobj(intobj)
    aite_age = colobj(intobj)
    aite_class = colobj(strobj)

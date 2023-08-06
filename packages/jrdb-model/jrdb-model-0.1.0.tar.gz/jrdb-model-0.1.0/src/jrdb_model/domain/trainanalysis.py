from ..sessioncontroll import (
    baseobj,
    strobj,
    baseobj,
    intobj,
    colobj,
    fkyobj,
)


class TrainAnalysisData(baseobj):
    __tablename__ = "train_analysis"
    racehorsekey = colobj(strobj, fkyobj("racehorse.racehorsekey"), primary_key=True)
    racekey = colobj(strobj)
    num = colobj(intobj)
    train_type = colobj(strobj)
    train_course_kind = colobj(strobj)
    saka = colobj(intobj)
    wood = colobj(intobj)
    dart = colobj(intobj)
    turf = colobj(intobj)
    pool = colobj(intobj)
    steeple = colobj(intobj)
    politruck = colobj(intobj)
    train_distance = colobj(intobj)
    train_juten = colobj(intobj)
    oikiri_score = colobj(intobj)
    shiage_score = colobj(intobj)
    train_vol_hyoka = colobj(strobj)
    shiage_score_change = colobj(intobj)
    train_comment = colobj(strobj)
    comment_date = colobj(strobj)
    train_hyoka = colobj(intobj)

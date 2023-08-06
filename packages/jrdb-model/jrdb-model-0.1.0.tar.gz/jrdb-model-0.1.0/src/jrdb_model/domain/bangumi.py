from ..sessioncontroll import (
    baseobj,
    strobj,
    baseobj,
    intobj,
    colobj,
    relobj,
    fkyobj,
    bkrobj,
)


class BangumiData(baseobj):
    __tablename__ = "bangumi"
    racekey = colobj(strobj, primary_key=True)
    # 親に対して
    kaisaikey = colobj(strobj, fkyobj("kaisai.kaisaikey"))
    # 子に対して
    racehorses = relobj("RacehorseData", backref=bkrobj("bangumi"), innerjoin=True)

    # 1:1
    returninfo = relobj("ReturninfoData", uselist=False, backref=bkrobj("bangumi"))
    umaren_odds = relobj("UmarenOddsData", uselist=False, backref=bkrobj("bangumi"))
    wide_odds = relobj("WideOddsData", uselist=False, backref=bkrobj("bangumi"))
    wakuren_odds = relobj("WakurenOddsData", uselist=False, backref=bkrobj("bangumi"))
    predict_race = relobj("PredictRaceData", uselist=False, backref=bkrobj("bangumi"))
    ymd = colobj(strobj)
    start_time = colobj(strobj)
    distance = colobj(intobj)
    tdscode = colobj(intobj)
    right_left = colobj(intobj)
    in_out = colobj(intobj)
    shubetsu = colobj(intobj)
    joken = colobj(strobj)
    kigo = colobj(intobj)
    horse_kind_joken = colobj(intobj)
    horse_sex_joken = colobj(intobj)
    inter_race_joken = colobj(intobj)
    juryo = colobj(intobj)
    grade = colobj(intobj)
    race_name = colobj(strobj)
    kai = colobj(strobj)
    num_of_all_horse = colobj(intobj)
    course = colobj(intobj)
    kaisai_kbn = colobj(intobj)
    race_name_short = colobj(strobj)
    race_name_9char = colobj(strobj)
    data_kbn = colobj(intobj)
    money1st = colobj(intobj)
    money2nd = colobj(intobj)
    money3rd = colobj(intobj)
    money4th = colobj(intobj)
    money5th = colobj(intobj)
    sannyu_money1st = colobj(intobj)
    sannyu_money2nd = colobj(intobj)
    sellflg_tansho = colobj(intobj)
    sellflg_fukusho = colobj(intobj)
    sellflg_wakuren = colobj(intobj)
    sellflg_umaren = colobj(intobj)
    sellflg_umatan = colobj(intobj)
    sellflg_wide = colobj(intobj)
    sellflg_sanrenpuku = colobj(intobj)
    sellflg_sanrentan = colobj(intobj)
    yobi = colobj(intobj)
    win5flg = colobj(intobj)

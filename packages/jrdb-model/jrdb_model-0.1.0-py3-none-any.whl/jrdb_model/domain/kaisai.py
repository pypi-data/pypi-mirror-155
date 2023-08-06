from ..sessioncontroll import (
    baseobj,
    strobj,
    baseobj,
    intobj,
    colobj,
    relobj,
    bkrobj,
)


class KaisaiData(baseobj):
    __tablename__ = "kaisai"
    kaisaikey = colobj(strobj, primary_key=True)
    # 子に対して
    races = relobj("BangumiData", backref=bkrobj("kaisai"), innerjoin=True)
    ymd = colobj(intobj)
    kaisai_kbn = colobj(intobj)
    day_of_week = colobj(strobj)
    course_name = colobj(strobj)
    tenko = colobj(intobj)
    turf_baba = colobj(intobj)
    turf_baba_abst = colobj(intobj)
    turf_baba_detail = colobj(intobj)
    turf_baba_in = colobj(intobj)
    turf_baba_center = colobj(intobj)
    turf_baba_out = colobj(intobj)
    turf_baba_sa = colobj(intobj)
    turf_baba_straight_saiuchi = colobj(intobj)
    turf_baba_straight_in = colobj(intobj)
    turf_baba_straight_center = colobj(intobj)
    turf_baba_straight_out = colobj(intobj)
    turf_baba_straight_oosoto = colobj(intobj)
    dart_baba = colobj(intobj)
    dart_baba_abst = colobj(intobj)
    dart_baba_detail = colobj(intobj)
    dart_baba_in = colobj(intobj)
    dart_baba_center = colobj(intobj)
    dart_baba_out = colobj(intobj)
    dart_baba_sa = colobj(intobj)
    data_kbn = colobj(intobj)
    renzoku_day = colobj(intobj)
    turf_kind = colobj(intobj)
    turf_length = colobj(intobj)
    tennatsu = colobj(intobj)
    stopfreeze = colobj(intobj)
    precipitation = colobj(intobj)

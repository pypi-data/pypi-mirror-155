from ..sessioncontroll import (
    baseobj,
    strobj,
    baseobj,
    intobj,
    colobj,
)


class TrainerData(baseobj):
    __tablename__ = "trainer"
    trainer_code = colobj(intobj, primary_key=True)
    delete_flg = colobj(intobj)
    delete_ymd = colobj(intobj)
    trainer_name = colobj(strobj)
    trainer_kana = colobj(strobj)
    trainer_name_short = colobj(strobj)
    shozoku_code = colobj(intobj)
    shozoku_region = colobj(strobj)
    birthday = colobj(intobj)
    get_licence_year = colobj(intobj)
    trainer_comment = colobj(strobj)
    comment_ymd = colobj(intobj)
    this_leading = colobj(intobj)
    this_seiseki_flat_1st = colobj(intobj)
    this_seiseki_flat_2nd = colobj(intobj)
    this_seiseki_flat_3rd = colobj(intobj)
    this_seiseki_flat_out = colobj(intobj)
    this_seiseki_steeple_1st = colobj(intobj)
    this_seiseki_steeple_2nd = colobj(intobj)
    this_seiseki_steeple_3rd = colobj(intobj)
    this_seiseki_steeple_out = colobj(intobj)
    this_tokubetsu_win = colobj(intobj)
    this_jusho_win = colobj(intobj)
    last_leading = colobj(intobj)
    last_seiseki_flat_1st = colobj(intobj)
    last_seiseki_flat_2nd = colobj(intobj)
    last_seiseki_flat_3rd = colobj(intobj)
    last_seiseki_flat_out = colobj(intobj)
    last_seiseki_steeple_1st = colobj(intobj)
    last_seiseki_steeple_2nd = colobj(intobj)
    last_seiseki_steeple_3rd = colobj(intobj)
    last_seiseki_steeple_out = colobj(intobj)
    last_tokubetsu_win = colobj(intobj)
    last_jusho_win = colobj(intobj)
    total_seiseki_flat_1st = colobj(intobj)
    total_seiseki_flat_2nd = colobj(intobj)
    total_seiseki_flat_3rd = colobj(intobj)
    total_seiseki_flat_out = colobj(intobj)
    total_seiseki_steeple_1st = colobj(intobj)
    total_seiseki_steeple_2nd = colobj(intobj)
    total_seiseki_steeple_3rd = colobj(intobj)
    total_seiseki_steeple_out = colobj(intobj)
    data_ymd = colobj(intobj)

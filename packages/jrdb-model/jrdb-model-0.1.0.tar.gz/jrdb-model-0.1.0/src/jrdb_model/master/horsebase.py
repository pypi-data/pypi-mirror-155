from ..sessioncontroll import (
    baseobj,
    strobj,
    baseobj,
    intobj,
    colobj,
)


class HorsebaseData(baseobj):
    __tablename__ = "horsebase"
    blood = colobj(intobj, primary_key=True)
    horse = colobj(strobj)
    sex = colobj(intobj)
    hair = colobj(intobj)
    umakigo = colobj(intobj)
    father = colobj(strobj)
    mother = colobj(strobj)
    mother_father = colobj(strobj)
    birthday = colobj(intobj)
    father_birthyear = colobj(intobj)
    mother_birthyear = colobj(intobj)
    mother_father_birthyear = colobj(intobj)
    owner = colobj(strobj)
    owner_kai_code = colobj(intobj)
    producer = colobj(strobj)
    locality = colobj(strobj)
    delete_flg = colobj(intobj)
    data_ymd = colobj(intobj)
    father_phylogeny = colobj(intobj)
    mother_phylogeny = colobj(intobj)


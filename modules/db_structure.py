from sqlalchemy import Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), nullable=False)
    location = mapped_column(String(500))

    tour_favs = relationship("Tour_place", back_populates="owner", cascade="all, delete")


class Tour_place(Base):
    __tablename__ = "tour_places"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="tour_favs")

    addr1 = mapped_column(String(255), nullable=False)
    areacode = mapped_column(Integer, nullable=True)

    contentid = mapped_column(Integer, nullable=False)
    contenttypeid = mapped_column(Integer, nullable=False)

    firstimage = mapped_column(String(500), nullable=True)
    firstimage2 = mapped_column(String(500), nullable=True)

    lDongRegnCd = mapped_column(Integer, nullable=False)
    lDongSignguCd = mapped_column(Integer, nullable=False)

    lclsSystm1 = mapped_column(String(20), nullable=False)
    lclsSystm2 = mapped_column(String(20), nullable=False)
    lclsSystm3 = mapped_column(String(20), nullable=False)


class Sigungu_sido(Base):
    __tablename__ = "sigungu_sido"

    city_id = mapped_column(Integer, primary_key=True)
    city_name = mapped_column(String(100), nullable=False)

    sigungus = relationship("SigunguSigungu", back_populates="parent_city")


class Sigungu_sigungu(Base):
    __tablename__ = "sigungu_sigungu"

    city_id = mapped_column(Integer, primary_key=True)
    city_name = mapped_column(String(100), nullable=False)
    parent_city_id = mapped_column(Integer, ForeignKey("sigungu_sido.city_id"), nullable=False)

    parent_city = relationship("SigunguSido", back_populates="sigungus")


class LclsSystmCode1(Base):
    __tablename__ = "lclsSystmCode1"

    lclsSystm1Cd = mapped_column(String(50), primary_key=True)
    lclsSystm1Nm = mapped_column(String(100), nullable=False)

    children = relationship("LclsSystmCode2", back_populates="parent")


class LclsSystmCode2(Base):
    __tablename__ = "lclsSystmCode2"

    lclsSystm2Cd = mapped_column(String(100), primary_key=True)
    lclsSystm2Nm = mapped_column(String(100), nullable=False)
    parent_lclsSystm1Cd = mapped_column(String(50), ForeignKey("lclsSystmCode1.lclsSystm1Cd"), nullable=False)

    parent = relationship("LclsSystmCode1", back_populates="children")
    children = relationship("LclsSystmCode3", back_populates="parent")


class LclsSystmCode3(Base):
    __tablename__ = "lclsSystmCode3"

    lclsSystm3Cd = mapped_column(String(100), primary_key=True)
    lclsSystm3Nm = mapped_column(String(100), nullable=False)
    parent_lclsSystm2Cd = mapped_column(String(100), ForeignKey("lclsSystmCode2.lclsSystm2Cd"), nullable=False)

    parent = relationship("LclsSystmCode2", back_populates="children")

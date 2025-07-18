from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from modules.db_load import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), nullable=False)
    email = mapped_column(String(255), unique=True, nullable=False)
    is_active = mapped_column(Boolean, default=False)

    posts = relationship("Post", back_populates="owner", cascade="all, delete")


class Post(Base):
    __tablename__ = "posts"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(255), nullable=False)
    description = mapped_column(String(1000))
    owner_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="posts")


class SigunguSido(Base):
    __tablename__ = "sigungu_sido"

    city_id = mapped_column(Integer, primary_key=True)
    city_name = mapped_column(String(100), nullable=False)

    sigungus = relationship("SigunguSigungu", back_populates="parent_city")


class SigunguSigungu(Base):
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

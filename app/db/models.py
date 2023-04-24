import sqlalchemy as sa
import re

from sqlalchemy.ext.declarative import declarative_base, declared_attr

metadata = sa.MetaData()

PlainBase = declarative_base(metadata=metadata)


class Base(PlainBase):
    __name__: str
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True, index=True)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        return pattern.sub('_', cls.__name__).lower()


class BtcUsdPrice(Base):
    __tablename__ = 'btc_usd_price'
    value = sa.Column(sa.DECIMAL(asdecimal=True, precision=12, scale=2, ), nullable=False)


class Leads(Base):
    phone_work = sa.Column(sa.String(255), nullable=True)
    first_name = sa.Column(sa.String(255), nullable=True)
    last_name = sa.Column(sa.String(255), nullable=True)

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
    amount = sa.Column(sa.DECIMAL(asdecimal=True, precision=12, scale=2, ), nullable=False)

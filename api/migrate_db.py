from sqlalchemy import create_engine
from api.models.goods import Base as Goods_Base
from api.models.user import Base as User_Base
from api.models.goods_user import Base as GU_Base

DB_URL = "mysql+pymysql://root@db:3306/degicali_data?charset=utf8"
engine = create_engine(DB_URL, echo=True)

def reset_database():
    Goods_Base.metadata.drop_all(bind=engine)
    User_Base.metadata.drop_all(bind=engine)
    GU_Base.metadata.drop_all(bind=engine)
    Goods_Base.metadata.create_all(bind=engine)
    User_Base.metadata.create_all(bind=engine)
    GU_Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    reset_database()
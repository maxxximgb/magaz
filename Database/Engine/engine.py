import sqlalchemy.orm as orm
import sqlalchemy

__factory = None
SqlAlchemyBase = sqlalchemy.orm.declarative_base()


def global_init():
    global __factory

    if __factory:
        return

    conn_str = f'sqlite:///Database/database.sqlite?check_same_thread=False'

    engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> orm.Session:
    global __factory
    return __factory()
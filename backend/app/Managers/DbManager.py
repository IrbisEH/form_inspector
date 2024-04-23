import datetime

from sqlalchemy import text
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

TEST_TABLE = "test_table"


class TaskDbModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)
    enable = Column(Integer, nullable=False)
    schedule_config = Column(Text, nullable=False)
    test_config = Column(Text, nullable=False)
    created = Column(TIMESTAMP, default=datetime.datetime.now)
    modified = Column(TIMESTAMP, default=datetime.datetime.now)

class DbManager:
    def __init__(self, config_manager=None, log_manager=None):
        self.config_manager = config_manager
        self.log_manager = log_manager
        self.session = None

        self.connect()

    def connect(self):
        try:
            user = self.config_manager.db_user
            password = self.config_manager.db_pass
            host = self.config_manager.db_host
            port = self.config_manager.db_port
            database = self.config_manager.db_name

            engine = create_engine(
                f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
                isolation_level="READ COMMITTED"
            )

            self.session = Session(bind=engine)
            self.session.execute(text(f"SELECT * FROM {database}.{TEST_TABLE}")).fetchall()

            self.log_manager.info('Connect to DB successfully done.')
        except Exception as e:
            print(e)
            self.log_manager.error('Connect to DB failed.')

    def get_list(self, model):
        return self.session.query(model).all()

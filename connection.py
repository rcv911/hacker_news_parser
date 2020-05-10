from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class Connection:
    """ Класс поделючение к БД postgresql """
    def __init__(self, **kwargs):
        """
        Инициализация подключения к БД

        :param kwargs:
            * *dsn* (``str``) -- URL БД
            * *pool_size* (``int``) -- число сессий в пуле
        """
        self.engine = create_engine(kwargs.get('dsn'),
                                    pool_size=kwargs.get('pool_size', 1))

        session = sessionmaker(autocommit=False, autoflush=False,
                               bind=self.engine)
        self.session = session()

    def close(self):
        self.session.close()

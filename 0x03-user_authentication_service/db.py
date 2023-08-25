#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        `add_user` saves given user with email and password to the database.

        Args:
            email(str): email of user.
            hashed_password(str): hashed password of user.

        Returns:
            User: The newly added user.
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            return

        return user

    def find_user_by(self, **kwargs) -> User:
        """
        `find_user_by` gets a user from the database with using the arguments
        supplied by `kwargs` as filter.

        Returns:
            User: The user, or None if no user is found.

        Raises:
            InvalidRequestError: If any of the arguments is not a valid
                attribute of User.
            NoResultFound: If no user is found with given characteristics.
        """

        keys, values = [], []
        for k, v in kwargs.items():
            if not hasattr(User, k):
                raise InvalidRequestError()
            keys.append(getattr(User, k))
            values.append(v)
        user = self._session.query(User).filter(
            tuple_(*keys).in_([tuple(values)])).first()
        if not user:
            raise NoResultFound()

        return user

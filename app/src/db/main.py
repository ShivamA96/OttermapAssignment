from sqlmodel import SQLModel, create_engine, Session
from models.user_model import User
from models.shop_model import Shop
from app.src.config import DB_URL, DB_ECHO, DB_CONNECT_ARGS, TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD

engine = create_engine(DB_URL, echo=DB_ECHO, connect_args=DB_CONNECT_ARGS)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("Tables Created Successfully!!")


def init_test_data():
    with Session(engine) as session:
        existing_user = session.exec(User).first()

        if existing_user is None:
            from services.user_service import create_user
            test_user = create_user(
                name=TEST_USER_NAME,
                email=TEST_USER_EMAIL,
                password=TEST_USER_PASSWORD
            )
            session.add(test_user)
            session.commit()

            test_shop = Shop(
                name="Test Shop",
                business_type="Retail",
                latitude=37.7749,
                longitude=-122.4194,
                vendor_id=test_user.id
            )
            session.add(test_shop)
            session.commit()

from sqlmodel import SQLModel, create_engine, Session
from models.user_model import User
from models.shop_model import Shop
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("Tables Created Successfully!!")


def init_test_data():
    with Session(engine) as session:
        existing_user = session.exec(User).first()

        if existing_user is None:
            from services.user_service import create_user
            test_user = create_user(
                name="Test Vendor",
                email="test@example.com",
                password="securepassword123"
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

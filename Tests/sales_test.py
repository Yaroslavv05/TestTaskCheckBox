import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from models.user_models import User
from models.sales_models import SalesCheck, Product, SalesCheckProduct
from schemas.sales_schemas import CreateSalesCheck
from datetime import datetime
from fastapi.responses import PlainTextResponse

@pytest.fixture(scope="module")
def test_app():
    app = app()
    yield TestClient(app)


@pytest.fixture
def mock_db():
    yield MagicMock(spec=Session)


@pytest.fixture
def mock_current_user():
    return User(id=1, username="test_user")

@pytest.mark.asyncio
async def test_create_sales_check(mock_db, mock_current_user):
    from main import create_sales_check

    sales_check_data = CreateSalesCheck(
        payment_type="cash",
        payment_amount=100,
        products=[
            {"name": "Product 1", "price": 10, "quantity": 2},
            {"name": "Product 2", "price": 15, "quantity": 1},
        ],
    )

    created_sales_check = await create_sales_check(
        sales_check_data, current_user=mock_current_user, db=mock_db
    )

    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_get_sales_checks(mock_db, mock_current_user):
    from main import get_sales_checks

    mock_db.query.return_value.filter.return_value.count.return_value = 1
    mock_db.query.return_value.filter.return_value.limit.return_value.offset.return_value.all.return_value = [
        SalesCheck(
            id=1,
            user_id=mock_current_user.id,
            created_at=datetime.now(),
            payment_type="cash",
            payment_amount=100,
            products=[
                SalesCheckProduct(
                    product=Product(name="Product 1", price=10), quantity=2, total=20
                ),
                SalesCheckProduct(
                    product=Product(name="Product 2", price=15), quantity=1, total=15
                ),
            ],
        )
    ]

    sales_checks_response = await get_sales_checks(
        current_user=mock_current_user, db=mock_db
    )

    assert isinstance(sales_checks_response, dict)
    # Add more assertions as needed


@pytest.mark.asyncio
async def test_get_sales_check_by_id(mock_db, mock_current_user):
    from main import get_sales_check_by_id

    mock_db.query.return_value.all.return_value = [
        SalesCheck(
            id=1,
            user_id=mock_current_user.id,
            created_at=datetime.now(),
            payment_type="cash",
            payment_amount=100,
            products=[
                SalesCheckProduct(
                    product=Product(name="Product 1", price=10), quantity=2, total=20
                ),
                SalesCheckProduct(
                    product=Product(name="Product 2", price=15), quantity=1, total=15
                ),
            ],
        )
    ]

    sales_check_response = await get_sales_check_by_id(
        sales_check_id=1, current_user=mock_current_user, db=mock_db
    )

    assert isinstance(sales_check_response, dict)

@pytest.mark.asyncio
async def test_view_sales_check(mock_db):
    from main import view_sales_check

    mock_db.query.return_value.filter.return_value.first.return_value = SalesCheck(
        id=1,
        created_at=datetime.now(),
        payment_type="cash",
        payment_amount=100,
        products=[
            SalesCheckProduct(
                product=Product(name="Product 1", price=10), quantity=2, total=20
            ),
            SalesCheckProduct(
                product=Product(name="Product 2", price=15), quantity=1, total=15
            ),
        ],
    )

    sales_check_text_response = await view_sales_check(sales_check_id=1, db=mock_db)

    assert isinstance(sales_check_text_response, PlainTextResponse)
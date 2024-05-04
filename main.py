from fastapi import FastAPI
from schemas.user_shemas import Token
from schemas.sales_schemas import SalesCheckListResponse, SalesCheckResponse
from services.authentication_services import login_for_access_token, register_user
from services.sales_services import create_sales_check, get_sales_checks, get_sales_check_by_id, view_sales_check

app = FastAPI()

'''
Routes definition for handling various endpoints in the application.

POST endpoint "/register": Registers a new user using the register_user function.
POST endpoint "/token": Generates an access token for authentication using login_for_access_token function.
POST endpoint "/sales-check": Creates a new sales check using create_sales_check function.
GET endpoint "/sales-checks": Retrieves a list of sales checks using get_sales_checks function.
GET endpoint "/sales-checks/{sales_check_id}": Retrieves details of a specific sales check by ID using get_sales_check_by_id function.
GET endpoint "/sales-checks/{sales_check_id}/view": Generates a text representation of a sales check using view_sales_check function.
'''

app.post("/register")(register_user)

app.post("/token", response_model=Token)(login_for_access_token)

app.post("/sales-check")(create_sales_check)

app.get("/sales-checks", response_model=SalesCheckListResponse)(get_sales_checks)

app.get("/sales-checks/{sales_check_id}", response_model=SalesCheckResponse)(get_sales_check_by_id)

app.get("/sales-checks/{sales_check_id}/view")(view_sales_check)
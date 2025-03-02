from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, field_validator


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.USER


class UserCreate(User):
    password: str


class BusinessCategory(BaseModel):
    name: str


class Business(BaseModel):
    business_tax_id: str
    business_name: str
    zip_code: Optional[str] = None
    street_address: Optional[str] = None
    street_number: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    business_category_id: Optional[int] = None


class ExpenseCategory(BaseModel):
    name: str


class IncomeCategory(BaseModel):
    name: str


class BankAccount(BaseModel):
    user_id: Optional[int] = None
    bank_name: str
    account_name: str
    account_number: str
    account_type: str


class CreditCard(BaseModel):
    card_name: str
    bank_account_id: int
    credit_amount: int
    billing_period_end_date: date
    payment_due_date: date


class PurchasedItem(BaseModel):
    expense_id: Optional[int] = None
    name: str
    code: str
    quantity: Decimal
    unit_type: str
    unit_price: Decimal
    total_price: Decimal
    main_category_id: Optional[int] = None

    @field_validator("total_price")
    def validate_total_price(cls, v, values):
        if "quantity" in values.data and "unit_price" in values.data:
            calculated = values.data["quantity"] * values.data["unit_price"]
            if abs(v - calculated) > Decimal(
                "0.01"
            ):  # Allow for small rounding differences
                raise ValueError("Total price must equal quantity * unit_price")
        return v

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = str(value)
        return data


class PurchasedItemSubcategory(BaseModel):
    purchased_item_id: UUID4
    subcategory_id: int

    class Config:
        from_attributes = True


class Expense(BaseModel):
    user_id: Optional[int] = None
    bank_account_id: Optional[int] = None
    business_id: Optional[int] = None
    total: Optional[Decimal] = None
    total_due: Decimal = Decimal("0")
    cashback: Decimal = Decimal("0")
    qrcode_scanned: bool = False
    discounts: Optional[Decimal] = Decimal("0")
    taxes: Optional[Decimal] = Decimal("0")
    payment_method: str = "Débito"
    installments: Optional[int] = 1
    additional_info: Optional[str] = None
    items_count: int = 0
    nfce_bpe_link: Optional[str] = None
    currency: str = "BRL"
    purchase_timestamp: Optional[datetime] = None

    @field_validator("purchase_timestamp", mode="before")
    def parse_purchase_timestamp(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")
        return value

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = str(value)
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
        return data

    class Config:
        from_attributes = True


class Installment(BaseModel):
    expense_id: int
    installment_number: int
    value: Decimal
    due_date: Optional[date] = None
    paid: bool = False


class TransactionType(int, Enum):
    DEBIT = 0
    CREDIT = 1


class Transaction(BaseModel):
    transaction_id: Optional[int] = None
    type: TransactionType


class CreditCardBillHistory(BaseModel):
    credit_card_id: int
    expense_id: int
    installment_id: Optional[int] = None
    total_installments: int
    bill_date: date


class Income(BaseModel):
    user_id: Optional[int] = None
    name: str
    total: Decimal
    income_category_id: Optional[int] = None


class Budget(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date

    @field_validator("end_date")
    def validate_dates(cls, v, values):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("End date must be after start date")
        return v


class BudgetItem(BaseModel):
    budget_id: int
    expense_category_id: int
    planned_amount: Decimal


class BudgetVsActual(BaseModel):
    budget_id: int
    budget_name: str
    expense_category_id: int
    category_name: str
    planned_amount: Decimal
    actual_amount: Decimal
    remaining_amount: Decimal
    percentage_used: Optional[float] = None

    class Config:
        from_attributes = True


class MonthlyExpenseSummary(BaseModel):
    user_id: int
    username: str
    month: str
    category_id: int
    category_name: str
    total_amount: Decimal
    transaction_count: int

    class Config:
        from_attributes = True

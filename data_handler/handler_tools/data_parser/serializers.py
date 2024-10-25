from decimal import Decimal
from pydantic import BaseModel, ValidationInfo, field_validator
from typing import Any
from shared.helpers import add_leading_zeros


class DataAccumulatorsSyncEvent(BaseModel):
    """
    Model to parse and validate data for AccumulatorsSync event.

    This model validates and converts the lending and debt accumulators from hexadecimal
    strings to `Decimal` format, scaled by `1e27`.

    Attributes:
        token (str): The token address as a hexadecimal string.
        lending_accumulator (Decimal): The lending accumulator value, converted from hex to Decimal.
        debt_accumulator (Decimal): The debt accumulator value, converted from hex to Decimal.
    """

    token: str
    lending_accumulator: Decimal
    debt_accumulator: Decimal

    @field_validator("lending_accumulator", "debt_accumulator", mode="before")
    def hex_to_decimal(cls, v: str) -> Decimal:
        """
        Converts a hexadecimal string to a Decimal value, scaled by 1e27.

        Args:
            v (str): The hexadecimal string to be converted.

        Returns:
            Decimal: The converted decimal value scaled by 1e27.
        """
        return Decimal(int(v, 16)) / Decimal("1e27")


class LiquidationEventData(BaseModel):
    """
    Class for converting liquidation event to an object model.

    Attributes:
        liquidator: The address of the liquidator.
        user: The address of the user.
        debt_token: The address of the debt token.
        debt_raw_amount: A numeric string of the debt_raw_amount converted to decimal.
        debt_face_amount: A numeric string of the debt_face_amount converted to decimal.
        collateral_token: The address of collateral token.
        collateral_amount: A numeric string of the collateral_amount converted to decimal.
    """

    liquidator: str
    user: str
    debt_token: str
    debt_raw_amount: str
    debt_face_amount: str
    collateral_token: str
    collateral_amount: str

    @field_validator("liquidator", "user", "debt_token", "collateral_token")
    def validate_valid_addresses(cls, value: str, info: ValidationInfo) -> str:
        """
        Check if the value is an address and format it to having leading zeros.

        Raises:
            ValueError

        Returns:
            str
        """
        if not value.startswith("0x"):
            raise ValueError("Invalid address provided for %s" % info.field_name)
        return add_leading_zeros(value)

    @field_validator("debt_raw_amount", "debt_face_amount", "collateral_amount")
    def validate_valid_numbers(cls, value: str, info: ValidationInfo) -> Decimal:
        """
        Convert the hexadecimal string value to a decimal.

        Raises:
            ValueError: If value is not a valid hexadecimal.

        Returns:
            Decimal: Converted decimal value.
        """

        if not value.isdigit():
            raise ValueError("%s field is not numeric" % info.field_name)
        return Decimal(str(int(value, base=16)))

class RepaymentEventSerializer(BaseModel):
    """
    Data model representing a repayment event in the system.

    Attributes:
        repayer (str): The address or identifier of the individual or entity making the repayment.
        beneficiary (str): The address or identifier of the individual or entity receiving the repayment.
        token (str): The type or symbol of the token being used for the repayment.
        raw_amount (str): The raw amount of the repayment as provided, before any conversions or calculations.
        face_amount (str): The face amount of the repayment, representing the value after necessary conversions.
    """
    repayer: str
    beneficiary: str
    token: str
    raw_amount: str
    face_amount: str

    @field_validator("beneficiary", "token", pre=True, always=True)
    def add_leading_zeros(cls, value: str) -> str:
        """
        Ensures the `beneficiary` and `token` fields contain leading zeros if required.

        Args:
            value (str): The value of the field to validate, typically an address or identifier.

        Returns:
            str: The value with added leading zeros if necessary, maintaining a consistent format.
        """
        return add_leading_zeros(value)

    @classmethod
    def parse_event(cls, event: pd.Series) -> "RepaymentEventSerializer":
        """
        Parses the repayment event data into a `RepaymentEventSerializer` instance.

        Args:
            event (pd.Series): A pandas Series containing repayment event data, 
                               with keys "data", "block_number", and "timestamp".

        Returns:
            RepaymentEventSerializer: An instance with parsed and validated repayment event data.
        """
        return cls(
            repayer=event["data"][0],
            beneficiary=event["data"][1],
            token=event["data"][2],
            raw_amount=event["data"][3],
            face_amount=event["data"][4],
            block_number=event["block_number"],
            timestamp=event["timestamp"]
        )
    
    class Config:
        """
        Configuration for the RepaymentEventSerializer model.

        Attributes:
            arbitrary_types_allowed (bool): If set to True, allows fields to accept non-standard or arbitrary types
                                            that are not strictly validated, adding flexibility for custom data types.
        """
        arbitrary_types_allowed = True


    @staticmethod
    def convert_hex_to_decimal(value: str) -> Decimal:
        """
        Converts a hexadecimal string to a Decimal, or raises an error if invalid.

        Args:
            value (str): The hexadecimal string to convert.

        Returns:
            Decimal: The converted decimal value.
        """
        try:
            return Decimal(int(value, 16))
        except ValueError:
            raise ValueError(f"{value} is not a valid hexadecimal number")

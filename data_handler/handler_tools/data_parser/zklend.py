from decimal import Decimal
from typing import List, Any


from serializers import DataAccumulatorsSyncEvent, LiquidationEventData, RepaymentEventData


class ZklendDataParser:
    """
    Parses the zkLend data to human-readable format.
    """

    @classmethod
    def parse_accumulators_sync_event(
        cls, event_data: list[Any]
    ) -> DataAccumulatorsSyncEvent:
        """
        Parses the AccumulatorsSync event data into a human-readable format using the AccumulatorsSyncEvent serializer.

        The event data is fetched from on-chain logs and is structured in the following way:
        - event_data[0]: The token address (as a hexadecimal string).
        - event_data[1]: Lending accumulator value (as a hexadecimal string).
        - event_data[2]: Debt accumulator value (as a hexadecimal string).

        Example of raw event data can be found on Starkscan:
        https://starkscan.co/event/0x029628b89875a98c1c64ae206e7eb65669cb478a24449f3485f5e98aba6204dc_0

        Args:
            event_data (list[Any]): A list containing the raw event data, typically with 3 elements:
                token, lending accumulator (hexadecimal string), and debt accumulator (hexadecimal string).

        Returns:
            AccumulatorsSyncEvent: A Pydantic model with the parsed and validated event data in a human-readable format.
        """
        parsed_event = DataAccumulatorsSyncEvent(
            token=event_data[0],
            lending_accumulator=event_data[1],
            debt_accumulator=event_data[2],
        )
        return parsed_event

    @classmethod
    def parse_deposit_event(cls, event_data):
        # TODO: Implement parsing logic for Deposit event
        pass

    @classmethod
    def parse_collateral_enabled_disabled_event(cls, event_data):
        # TODO: Implement parsing logic for CollateralEnabled event
        # TODO put it together with disabled event
        pass

    @classmethod
    def parse_withdrawal_event(cls, event_data):
        # TODO: Implement parsing logic for Withdrawal event
        pass

    @classmethod
    def parse_borrowing_event(cls, event_data):
        # TODO: Implement parsing logic for Borrowing event
        pass

    @classmethod
    def parse_repayment_event(cls, event_data: List[Any]) -> RepaymentEventData:
        """
        Parses the Repayment event data into a human-readable format using the RepaymentEventData serializer.

        Args:
            event_data (List[Any]): A list containing the raw repayment event data, typically with 5 elements:
                repayer, beneficiary, token, raw_amount, and face_amount.

        Returns:
            RepaymentEventData: A Pydantic model with the parsed and validated repayment event data in a human-readable format.
        """
        parsed_event = RepaymentEventData(
            repayer=event_data[0],
            beneficiary=event_data[1],
            token=event_data[2],
            raw_amount=event_data[3],
            face_amount=event_data[4],
        )
        return parsed_event

    @classmethod
    def parse_liquidation_event(cls, event_data):
        """
        Convert the event list to a Liquidation event data object

        :event_data - List of length 7 of the event data

        Returns
        LiquidationEventData
        """
        event_data = LiquidationEventData(
            liquidator=event_data[0],
            user=event_data[1],
            debt_token=event_data[2],
            debt_raw_amount=event_data[3],
            debt_face_amount=event_data[4],
            collateral_token=event_data[5],
            collateral_amount=event_data[6],
        )
        return event_data
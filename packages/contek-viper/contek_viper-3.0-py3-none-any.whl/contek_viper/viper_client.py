from __future__ import annotations

from typing import Iterable

import grpc

from contek_viper.execution.execution_service_pb2 import SubmitMarketSignalsRequest
from contek_viper.execution.execution_service_pb2_grpc import ExecutionServiceStub
from contek_viper.execution.market_signal_pb2 import MarketSignal


class ViperClient:

    def __init__(self, stub: ExecutionServiceStub) -> None:
        self._stub = stub

    @classmethod
    def create(cls, server_address: str) -> ViperClient:
        channel = grpc.insecure_channel(server_address)
        stub = ExecutionServiceStub(channel)
        return cls(stub)

    def submit(
        self,
        trigger_name: str,
        market_signals: Iterable[MarketSignal],
    ) -> None:
        self._stub.SubmitMarketSignals(
            SubmitMarketSignalsRequest(
                trigger_name=trigger_name,
                market_signal=list(market_signals),
            ))

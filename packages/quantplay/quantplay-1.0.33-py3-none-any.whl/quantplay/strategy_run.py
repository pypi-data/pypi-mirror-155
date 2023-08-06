from quantplay.strategies.options.intraday.musk import Musk
from quantplay.strategies.futures.overnight.nexon import Nexon
from quantplay.strategies.equity.overnight.shifu import Shifu
from quantplay.executor.strategy_executor import UserStrategiesExecutor

strategies = [Musk(), Nexon()]

UserStrategiesExecutor("Zerodha", strategies).start_execution()
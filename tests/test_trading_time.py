import pytest
import os
from datetime import datetime, timedelta
from china_stock_data import PersistentDict, TradingTimeChecker
import tempfile
import shutil

@pytest.fixture
def setup_persistent_dict():
    # 创建临时目录和文件
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, 'test_dict.json')
    
    # 创建 PersistentDict 实例
    pdict = PersistentDict(temp_file)
    
    yield pdict
    
    # 清理
    shutil.rmtree(temp_dir)

def test_persistent_dict(setup_persistent_dict):
    pdict = setup_persistent_dict
    pdict.set('key1', 'value1')
    assert pdict.get('key1') == 'value1'
    pdict.set('key2', 'value2')
    assert pdict.get('key2') == 'value2'
    pdict.delete('key1')
    assert pdict.get('key1') is None
    assert pdict.get('key2') == 'value2'

@pytest.fixture
def setup_trading_time_checker():
    # 创建临时目录和文件
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, 'test_trade_dates_cache.json')

    # 使用临时缓存文件进行测试
    TradingTimeChecker.appDict = PersistentDict(temp_file)
    yield
    # 清理测试缓存文件
    shutil.rmtree(temp_dir)

def test_is_trading_time(setup_trading_time_checker):
    # 假设今天是交易日，并在交易时间内
    assert TradingTimeChecker.is_trading_time('2023-10-23 10:00:00') is True
    # 假设今天是交易日，但不在交易时间内
    assert TradingTimeChecker.is_trading_time('2023-10-23 16:00:00') is False
    # 假设今天不是交易日
    assert TradingTimeChecker.is_trading_time('2023-10-22 10:00:00') is False

def test_get_nearest_trade_date(setup_trading_time_checker):
    nearest_trade_date = TradingTimeChecker.get_nearest_trade_date('2023-10-23')
    assert nearest_trade_date <= '2023-10-23'

def test_compare_with_nearest_trade_date(setup_trading_time_checker):
    assert TradingTimeChecker.compare_with_nearest_trade_date('2023-10-23', '2023-10-23') is True
    assert TradingTimeChecker.compare_with_nearest_trade_date('2023-10-22', '2023-10-23') is False

# 确保替换 'your_module' 为包含 PersistentDict 和 TradingTimeChecker 类的实际模块名。

from unittest.mock import patch
from app.contract import register_content_on_chain, verify_content_on_chain


@patch("app.contract.w3.eth.get_transaction_count")
@patch("app.contract.w3.eth.gas_price")
@patch("app.contract.w3.eth.send_raw_transaction")
@patch("app.contract.w3.eth.wait_for_transaction_receipt")
def test_register_content_on_chain(mock_wait, mock_send, mock_gas, mock_nonce):
    mock_nonce.return_value = 0
    mock_gas.return_value = 1000000000
    mock_send.return_value = b"txhash"
    mock_wait.return_value = {"blockNumber": 12345}

    result = register_content_on_chain("testhash")
    assert "tx_hash" in result
    assert result["block_number"] == 12345


@patch("app.contract.contract.functions.verify")
def test_verify_content_on_chain_exists(mock_verify):
    mock_verify.return_value.call.return_value = ("0x123", 123456)
    result = verify_content_on_chain("testhash")
    assert result["exists"] is True
    assert result["owner"] == "0x123"
    assert result["timestamp"] == 123456


@patch("app.contract.contract.functions.verify")
def test_verify_content_on_chain_not_exists(mock_verify):
    mock_verify.return_value.call.side_effect = Exception("Not found")
    result = verify_content_on_chain("testhash")
    assert result["exists"] is False

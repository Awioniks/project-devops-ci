import pytest
import requests
from pytest_mock import MockerFixture

from http_checker.checker import check_urls

def test_check_urls_success(mocker):
    mock_requests_get = mocker.patch("http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.ok = True
    mock_requests_get.return_value = mock_response

    urls = ["https://www.example.com"]
    results = check_urls(urls, timeout=5)

    mock_requests_get.asser_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == "200 OK"

def test_check_urls_client_error(mocker: MockerFixture):
    mock_requests_get = mocker.patch(
        "http_checker.checker.requests.get"
    )

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    mock_response.ok = False
    mock_requests_get.return_value = mock_response

    urls = ["https://www.example.com"]
    results = check_urls(urls, timeout=5)

    mock_requests_get.assert_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == "404 Not Found"

@pytest.mark.parametrize(
        "error_exception, expected_status",
        [
            (requests.exceptions.Timeout, "TIMEOUT"),
            (requests.exceptions.ConnectionError, "CONNECTION_ERROR"),
            (requests.exceptions.RequestException, "REQUEST_ERROR: RequestException"),
        ],
)
def test_check_urls_exceptions(
    mocker: MockerFixture,
    error_exception: type[requests.exceptions.RequestException],
    expected_status: str,
):
    mock_requests_get = mocker.patch(
        "http_checker.checker.requests.get"
    )

    mock_requests_get.side_effect = error_exception(
        f"Simulated {expected_status}"
    )

    urls = ["https://www.problem.com"]
    results = check_urls(urls, timeout=5)

    mock_requests_get.asser_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == expected_status

def test_check_urls_with_multiple_urls(mocker: MockerFixture):

    mock_requests_get = mocker.patch("http_checker.checker.requests.get")

    #First call
    mock_response_ok = mocker.MagicMock(spec=requests.Response)
    mock_response_ok.status_code = 200
    mock_response_ok.reason = "OK"
    mock_response_ok.ok = True

    #Second call
    timeout_exception = requests.exceptions.Timeout("Simulated timeout")

    #Third call
    mock_response_fail = mocker.MagicMock(spec=requests.Response)
    mock_response_fail.status_code = 500
    mock_response_fail.reason = "Server Error"
    mock_response_fail.ok = False

    mock_requests_get.side_effect = [
        mock_response_ok,
        timeout_exception,
        mock_response_fail
    ]

    urls = ["https://www.success.com", "https://timeout.com", "https://servererror.com"]
    results = check_urls(urls, timeout=5)

    assert len(results) == 3
    assert mock_requests_get.call_count == 3
    assert results["https://www.success.com"] == "200 OK"
    assert results["https://timeout.com"] == "TIMEOUT"
    assert results["https://servererror.com"] == "500 Server Error"


def test_check_urls_empty():

    result = check_urls([])
    assert result == {}


def test_check_urls_custom_timeout(mocker):
    mock_requests_get = mocker.patch("http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.ok = True
    mock_requests_get.return_value = mock_response

    urls = ["https://www.example.com"]
    results = check_urls(urls, timeout=10)

    mock_requests_get.asser_called_once_with(urls[0], timeout=10)
    assert results[urls[0]] == "200 OK"

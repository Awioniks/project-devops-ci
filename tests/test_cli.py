from click.testing import CliRunner
from pytest_mock import MockerFixture

from http_checker.cli import main


def test_no_urls():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.exit_code == 0
    assert "Usage: check-urls" in result.output

def test_main_single_url_success(mocker: MockerFixture):
    url = "https://www.example.com"
    mock_check = mocker.patch("http_checker.cli.check_urls")
    mock_check.return_value = {url: "200 OK"}

    runner = CliRunner()
    result = runner.invoke(main, [url])

    assert result.exit_code == 0
    mock_check.assert_called_once_with((url, ), 5)

    assert "--- Results ---" in result.output
    assert url in result.output
    assert "--- Results ---" in result.output

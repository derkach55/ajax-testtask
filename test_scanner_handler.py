import pytest

from scanner_handler import CheckQr


@pytest.fixture(scope='module')
def check_qr():
    return CheckQr()


@pytest.mark.parametrize(
    'qr, color',
    [
        ('123', 'Red'),
        ('12345', 'Green'),
        ('1234567', 'Fuzzy Wuzzy')
    ]
)
def test_qr_color_when_device_exist_in_db(mocker, check_qr, qr, color):
    mocker.patch('scanner_handler.CheckQr.check_in_db', return_value=True)
    check_len_color_spy = mocker.spy(check_qr, 'check_len_color')
    can_add_device_spy = mocker.spy(check_qr, 'can_add_device')
    check_qr.check_scanned_device(qr)

    check_len_color_spy.assert_called_once_with(qr)
    assert check_len_color_spy.spy_return == color

    can_add_device_spy.assert_called_once_with(f'hallelujah {qr}')
    assert can_add_device_spy.spy_return == f'hallelujah {qr}'


@pytest.mark.parametrize(
    'qr',
    [
        '1',
        '12',
        '1234',
        '123456',
    ]
)
def test_incorrect_qr_length(mocker, check_qr, qr):
    mocker.patch('scanner_handler.CheckQr.check_in_db', return_value=True)
    check_len_color_spy = mocker.spy(check_qr, 'check_len_color')
    send_error_spy = mocker.spy(check_qr, 'send_error')
    check_qr.check_scanned_device(qr)

    check_len_color_spy.assert_called_once_with(qr)
    assert check_len_color_spy.spy_return is None

    send_error_spy.assert_called_once_with(f'Error: Wrong qr length {len(qr)}')


def test_device_do_not_exist_in_db(mocker, check_qr):
    mocker.patch('scanner_handler.CheckQr.check_in_db', return_value=None)
    send_error_spy = mocker.spy(check_qr, 'send_error')
    check_qr.check_scanned_device('123')

    send_error_spy.assert_called_once_with('Not in DB')


if __name__ == '__main__':
    pytest.main()

from hmpy.util import Timer


def test_timer_recurring(qtbot, mock):
    # Test that a recurring timer executes the action at the expected interval
    timer = Timer(10, mock)
    timer.start()
    qtbot.wait(105)
    mock.assert_called_around(10)


def test_timer_non_recurring(qtbot, mock):
    # Test that a non-recurring timer only executes the action once
    timer = Timer(10, mock, False)
    timer.start()
    qtbot.wait(105)
    mock.assert_called_once()


def test_timer_stop(qtbot, mocker):
    # Test that the timer can be stopped
    mock = mocker.stub()
    timer = Timer(10, mock)
    timer.start()
    timer.stop()
    qtbot.wait(25)
    mock.assert_not_called()


def test_timer_stop_start(qtbot, mock):
    # Test that the timer can be started again after being stopped
    timer = Timer(10, mock)
    timer.start()
    timer.stop()
    timer.start()
    qtbot.wait(105)
    mock.assert_called_around(10)


def test_timer_interval_change(qtbot, mock):
    # Test that the timer behaves as expected when the interval is changed
    timer = Timer(100, mock)
    timer.start()
    timer.interval = 10
    qtbot.wait(100)
    mock.assert_called_around(10)


def test_timer_set_action(qtbot, mocker, mock):
    # Test that the set_action method changes the action being invoked
    initial_action = mocker.stub()
    timer = Timer(10, initial_action)
    timer.start()
    qtbot.wait(50)

    initial_action.reset_mock()
    timer.set_action(mock)
    qtbot.wait(100)

    initial_action.assert_not_called()
    # Increased acceptable range since setting action does not reset current tick
    mock.assert_called_around(10, 2)

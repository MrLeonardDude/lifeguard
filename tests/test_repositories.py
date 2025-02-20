import unittest
from unittest.mock import MagicMock, patch
import sys

from lifeguard.repositories import (
    IMPLEMENTATIONS,
    HistoryRepository,
    NotificationRepository,
    ValidationRepository,
    declare_implementation,
)

sys.path.append("tests/fixtures")

NAMES = ["history", "notification", "validation"]


class TestNotificationRepository(unittest.TestCase):
    def setUp(self):
        for name in NAMES:
            if name in IMPLEMENTATIONS:
                IMPLEMENTATIONS.pop(name)

        self.implementation = MagicMock(name="implementation")

        with patch("lifeguard.repositories.logger"):
            implementation_class = MagicMock(name="implementation_class")
            implementation_class.__name__ = "mocked_implementation"
            implementation_class.return_value = self.implementation

            declare_implementation("notification", implementation_class)

        self.notification_repository = NotificationRepository()

    def test_save_last_notification_for_a_validation(self):
        result = MagicMock(name="result")
        self.notification_repository.save_last_notification_for_a_validation(result)
        self.implementation.save_last_notification_for_a_validation.assert_called_with(
            result
        )

    def test_validation_repository_fetch_last_validation_result(self):
        validation_name = MagicMock(name="validation_name")
        self.notification_repository.fetch_last_notification_for_a_validation(
            validation_name
        )
        self.implementation.fetch_last_notification_for_a_validation.assert_called_with(
            validation_name
        )


class TestHistoryRepository(unittest.TestCase):
    def setUp(self):
        for name in NAMES:
            if name in IMPLEMENTATIONS:
                IMPLEMENTATIONS.pop(name)

        self.implementation = MagicMock(name="implementation")

        with patch("lifeguard.repositories.logger"):
            implementation_class = MagicMock(name="implementation_class")
            implementation_class.__name__ = "mocked_implementation"
            implementation_class.return_value = self.implementation

            declare_implementation("history", implementation_class)

        self.history_repository = HistoryRepository()

    def test_append_notification(self):
        notification_occurrence = MagicMock(name="notification_occurrence")
        self.history_repository.append_notification(notification_occurrence)
        self.implementation.append_notification.assert_called_with(
            notification_occurrence
        )

    def test_count_notifications(self):
        result = self.history_repository.count_notifications()

        self.implementation.count_notifications.assert_called_with(None, None, {})
        self.assertIsNotNone(result)

    def test_fetch_notifications(self):
        start_interval = MagicMock(name="start_interval")
        end_interval = MagicMock(name="end_interval")
        filters = MagicMock(name="filters")

        result = self.history_repository.fetch_notifications(
            start_interval, end_interval, filters
        )

        self.implementation.fetch_notifications.assert_called_with(
            start_interval, end_interval, filters, None, None
        )
        self.assertIsNotNone(result)


class TestValidationRepositories(unittest.TestCase):
    def setUp(self):
        for name in NAMES:
            if name in IMPLEMENTATIONS:
                IMPLEMENTATIONS.pop(name)

        self.implementation = MagicMock(name="implementation")
        self.implementation.__name__ = "mocked_implementation"

        with patch("lifeguard.repositories.logger"):
            implementation_class = MagicMock(name="implementation_class")
            implementation_class.__name__ = "mocked_implementation"
            implementation_class.return_value = self.implementation

            declare_implementation("validation", implementation_class)

        self.validation_repository = ValidationRepository()

    def test_validation_repository_save_validation_result(self):
        result = MagicMock(name="result")
        self.validation_repository.save_validation_result(result)
        self.implementation.save_validation_result.assert_called_with(result)

    def test_validation_repository_fetch_last_validation_result(self):
        validation_name = MagicMock(name="validation_name")
        self.validation_repository.fetch_last_validation_result(validation_name)
        self.implementation.fetch_last_validation_result.assert_called_with(
            validation_name
        )

    def test_validation_repository_fetch_all_validation_results(self):
        self.validation_repository.fetch_all_validation_results()
        self.implementation.fetch_all_validation_results.assert_called()


class TestRepositoriesFunctions(unittest.TestCase):
    def setUp(self):
        if "test" in IMPLEMENTATIONS:
            IMPLEMENTATIONS.pop("test")
        self.implementation = MagicMock(name="implementation")
        self.implementation.__name__ = "test"

    @patch("lifeguard.repositories.logger")
    def test_warning_when_an_implementation_is_overwrited(self, mock_logger):
        declare_implementation("test", self.implementation)
        declare_implementation("test", self.implementation)
        mock_logger.warning.assert_called_with(
            "overwriting implementation for respository %s", "test"
        )

    @patch("lifeguard.repositories.logger")
    def test_info_when_an_implementation_is_declared(self, mock_logger):
        declare_implementation("test", self.implementation)
        mock_logger.info.assert_called_with(
            "loading implementation %s for repository %s",
            "test",
            "test",
        )

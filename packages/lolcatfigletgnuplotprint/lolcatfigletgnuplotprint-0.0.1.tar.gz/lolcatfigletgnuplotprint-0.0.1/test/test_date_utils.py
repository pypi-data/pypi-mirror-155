import unittest
from dateutil.relativedelta import relativedelta
from printers.utils.dates import format_datetime, parse_past_date_text


class TestDateUtils(unittest.TestCase):
    def test_past_dates_parsing(self):
        import datetime

        today = datetime.datetime.now()
        self.assertEqual(parse_past_date_text("1 hour"), format_datetime((today - datetime.timedelta(hours=1))))
        self.assertEqual(parse_past_date_text("last week"), format_datetime((today - datetime.timedelta(weeks=1))))
        self.assertEqual(parse_past_date_text("2 days ago"), format_datetime((today - datetime.timedelta(days=2))))
        self.assertEqual(parse_past_date_text("2 months ago"), format_datetime((today - relativedelta(months=2))))
        self.assertEqual(parse_past_date_text("2 years ago"), format_datetime((today - relativedelta(years=2))))


if __name__ == "__main__":
    unittest.main()

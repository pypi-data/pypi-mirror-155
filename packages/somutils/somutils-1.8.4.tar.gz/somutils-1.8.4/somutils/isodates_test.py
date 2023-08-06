#!/usr/bin/env python

from .isodates import (
    asUtc,
    toLocal,
    parseLocalTime,
    assertLocalDateTime,
    daterange,
    isodate,
    naiveisodate,
    localisodate,
    utcisodate,
    isodatetime,
    utcisodatetime,
    localisodatetime,
    addHours,
    addDays,
    tz,
    )

import datetime
import dateutil
import unittest

def localTime(string):
    isSummer = string.endswith("S")
    if isSummer: string=string[:-1]
    return parseLocalTime(string, isSummer)

class LocalTime_Test(unittest.TestCase):

    def test_localTime_fullySummer(self):
        self.assertEqual(
            str(localTime("2016-08-15 02:00:00")),
            "2016-08-15 02:00:00+02:00")

    def test_localTime_fullyWinter(self):
        self.assertEqual(
            str(localTime("2016-01-01 02:10:00")),
            "2016-01-01 02:10:00+01:00")

    def test_localTime_badTz_ignored(self):
        self.assertEqual(
            str(localTime("2016-01-01 02:00:00S")),
            "2016-01-01 02:00:00+01:00")

    def test_localTime_badSummerTz_ignored(self):
        self.assertEqual(
            str(localTime("2016-08-15 02:00:00")),
            "2016-08-15 02:00:00+02:00")

    def test_localTime_beforeOctoberChange(self):
        self.assertEqual(
            str(localTime("2016-10-30 02:00:00S")),
            "2016-10-30 02:00:00+02:00")

    def test_localTime_afterOctoberChange(self):
        self.assertEqual(
            str(localTime("2016-10-30 02:00:00")),
            "2016-10-30 02:00:00+01:00")

    def test_localTime_SIgnored(self):
        self.assertEqual(
            str(localTime("2016-10-30 03:00:00S")),
            "2016-10-30 03:00:00+01:00")

    @unittest.skip('toreview: it should fail')
    def test_localTime_unexistingHour(self):
        self.assertEqual(
            str(localTime("2016-03-27 02:00:00")),
            "2016-03-27 02:00:00+01:00")

    def test_localTime_atWinterMidnight(self):
        self.assertEqual(
            str(localTime("2016-01-01 00:00:00")),
            "2016-01-01 00:00:00+01:00")

class Assertions_Test(unittest.TestCase):

    def test_assertLocalDateTime_withDate(self):
        with self.assertRaises(AssertionError) as ctx:
            assertLocalDateTime('myname', datetime.date(2016,1,1))
        self.assertEqual(ctx.exception.args[0],
            "myname should be a datetime")

    def test_assertLocalDateTime_withNaive(self):
        with self.assertRaises(AssertionError) as ctx:
            assertLocalDateTime('myname', datetime.datetime(2016,1,1))
        self.assertEqual(ctx.exception.args[0],
            "myname should have timezone")

    def test_assertLocalDateTime_withUTC(self):
        with self.assertRaises(AssertionError) as ctx:
            assertLocalDateTime('myname', asUtc(datetime.datetime(2016,1,1)))
        self.assertEqual(ctx.exception.args[0],
            "myname has UTC timezone")

    def test_assertLocalDateTime_withLocal(self):
        assertLocalDateTime('myname', toLocal(datetime.datetime(2016,1,1)))
        # No assert


class DatetimeParsers_Test(unittest.TestCase):

    def test_isodatetime_naive(self):
        self.assertEqual(
            isodatetime("2020-01-02 10:20:30"),
            datetime.datetime(
                2020,1,2,10,20,30
            )
        )

    def test_isodatetime_zulu(self):
        self.assertEqual(
            isodatetime("2020-01-02 10:20:30Z"),
            datetime.datetime(
                2020,1,2,10,20,30,
                tzinfo=dateutil.tz.tzutc()
            )
        )

    def test_isodatetime_zero(self):
        self.assertEqual(
            isodatetime("2020-01-02 10:20:30+00"),
            datetime.datetime(
                2020,1,2,10,20,30,
                tzinfo=dateutil.tz.tzutc()
            )
        )

    def test_isodatetime_tz(self):
        self.assertEqual(
            isodatetime("2020-01-02 10:20:30+04"),
            datetime.datetime(
                2020,1,2,10,20,30,
                tzinfo=dateutil.tz.tzoffset(None,4*60*60)
            )
        )

    def test_isodatetime_notime_returnsNaiveNoon(self):
        self.assertEqual(
            isodatetime("2020-01-02"),
            datetime.datetime(
                2020,1,2,0,0,0
            )
        )

    def test_utcisodatetime_naive_reinterprests(self):
        self.assertEqual(
            utcisodatetime("2020-01-02 10:20:30"),
            datetime.datetime(
                2020,1,2,10,20,30,
                tzinfo=dateutil.tz.tzutc()
            )
        )

    def test_localisodatetime_naive_reinterprets(self):
        date = localisodatetime("2020-01-02 10:20:30")
        self.assertEqual(date,
            tz.localize(datetime.datetime(
                2020,1,2,10,20,30,
            ))
        )
        self.assertEqual(str(date), "2020-01-02 10:20:30+01:00")

    def test_localisodatetime_naive_reinterprets_ambiguous(self):
        # Folded because daylight, could be two different times
        date = localisodatetime("2022-10-30 02:30:40")
        self.assertEqual(str(date), "2022-10-30 02:30:40+01:00")
        # Could have been also:
        #self.assertEqual(str(date), "2022-10-30 02:30:40+02:00")

    def test_localisodatetime_naive_reinterprets_missing(self):
        # Missing because daylight, skip from 2am to 3am
        date = localisodatetime("2022-03-27 02:30:40")
        # But this local time does not exist!
        self.assertEqual(str(date), "2022-03-27 02:30:40+01:00")

    def test_utcisodatetime_tz_reinterprets(self):
        self.assertEqual(
            utcisodatetime("2020-01-02 10:20:30+02"),
            datetime.datetime(
                2020,1,2, 8 ,20,30,
                tzinfo=dateutil.tz.tzutc()
            )
        )

    def test_localisodatetime_tz_reinterprets(self):
        date = localisodatetime("2020-01-02 10:20:30+05")
        self.assertEqual(str(date), "2020-01-02 06:20:30+01:00")

    def test_localisodatetime_utc_reinterprets(self):
        date = localisodatetime("2020-01-02 10:20:30z")
        self.assertEqual(str(date), "2020-01-02 11:20:30+01:00")

    def test_isodate(self):
        self.assertEqual(
            isodate("2020-01-02"),
            datetime.date(2020,1,2),
        )

    def test_naiveisodate(self):
        self.assertEqual(
            naiveisodate("2020-01-02"),
            datetime.datetime(2020,1,2,0,0,0),
        )

    def test_utcisodate(self):
        self.assertEqual(
            str(utcisodate("2020-01-02")),
            "2020-01-02 00:00:00+00:00"
        )

    def test_localisodate(self):
        self.assertEqual(
            str(localisodate("2020-01-02")),
            "2020-01-02 00:00:00+01:00"
        )

    def test_localisodate_summer(self):
        self.assertEqual(
            str(localisodate("2020-08-02")),
            "2020-08-02 00:00:00+02:00" # Now, +02:00
        )

    def test_naiveisodate(self):
        date = naiveisodate("2020-01-02")
        self.assertEqual(str(date), "2020-01-02 00:00:00")

    def test_daterange(self):
        days = daterange(
            isodate('2020-01-02'),
            isodate('2020-01-04'),
        )
        self.assertEqual(list(days), [
            isodate('2020-01-02'),
            isodate('2020-01-03'),
            isodate('2020-01-04'),
        ])

    def test_daterange_invertedRange(self):
        days = daterange(
            isodate('2020-01-04'),
            isodate('2020-01-02'),
        )
        self.assertEqual(list(days), [
        ])

    def test_daterange_times(self):
        days = daterange(
            isodatetime('2020-01-02 01:00:00'),
            isodatetime('2020-01-04 01:00:00'),
        )
        self.assertEqual(list(days), [
            isodatetime('2020-01-02 01:00:00'),
            isodatetime('2020-01-03 01:00:00'),
            isodatetime('2020-01-04 01:00:00'),
        ])

# vim: et ts=4 sw=4

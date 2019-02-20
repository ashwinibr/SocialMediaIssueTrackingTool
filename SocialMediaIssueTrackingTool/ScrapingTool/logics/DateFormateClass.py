import datetime


def dateListFunction(formdate, todate):
    date_list = []

    from_dt, to_dt = dateFormate(formdate, todate)

    for dt in daterange(from_dt, to_dt):
        date_list.append(dt.strftime("%m/%d/%Y"))
    return date_list


# Fetch date ranges between from and to date.
def daterange(fromdate, todate):
    for n in range(int((todate - fromdate).days) + 1):
        yield fromdate + datetime.timedelta(n)


# Converting From and To date in date formate from string formate.
def dateFormate(from_date, to_date):
    todate = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    fromdate = datetime.datetime.strptime(from_date, "%Y-%m-%d")

    from_dt = datetime.date(fromdate.year, fromdate.month, fromdate.day)
    to_dt = datetime.date(todate.year, todate.month, todate.day)

    return from_dt, to_dt
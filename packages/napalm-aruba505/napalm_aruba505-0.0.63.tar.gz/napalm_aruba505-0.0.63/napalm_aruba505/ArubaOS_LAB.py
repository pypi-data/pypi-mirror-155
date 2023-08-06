SECONDS = 1
MINUTE_SECONDS = 60
HOUR_SECONDS = 3600
DAY_SECONDS = 24 * HOUR_SECONDS
WEEK_SECONDS = 7 * DAY_SECONDS
YEAR_SECONDS = 365 * DAY_SECONDS
(years, weeks, days, hours, minutes, seconds) = (0, 0, 0, 0, 0, 0)


def show_version_sanitizer(data):
    """ Collects the vendor, model, os version and uptime from the 'show version'
    :returns a tuple with two values (vendor, model, os version, uptime)
    """
    if data:
        vendor = "Hewlett Packard"
        model = ""
        os_version = ""
        uptime = ""

        for line in data.splitlines():
            #print(f"{line}\n")
            if "MODEL:" in line:
                model, os_version = line.split(',')
            if "AP uptime is" in line:
                print(line)
                uptimes_records = [int(i) for i in line.split() if i.isnumeric()]
                print(uptimes_records)
                if uptimes_records and len(uptimes_records) == 5:
                    weeks, days, hours, minutes, seconds = uptimes_records
                    uptime = sum([
                        (years * YEAR_SECONDS),
                        (weeks * WEEK_SECONDS),
                        (days * DAY_SECONDS),
                        (hours * HOUR_SECONDS),
                        (minutes * MINUTE_SECONDS),
                        (seconds * SECONDS), ])

        return vendor, model, os_version, uptime


























    #
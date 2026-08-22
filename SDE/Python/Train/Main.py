import requests
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

SEARCH_URL = (
    "https://www.irctc.co.in/"
    "eticketing/protected/mapps1/altAvlEnq/TC"
)

AVAILABILITY_BASE_URL = (
    "https://www.irctc.co.in/"
    "eticketing/protected/mapps1/avlFarenquiry"
)


# ============================================================
# CREATE SESSION
# ============================================================

def create_session():

    session = requests.Session()

    headers = {
        "Accept": "application/json, text/plain, */*",

        "Accept-Language": "en-US,en;q=0.0",

        "Content-Language": "en",

        "Content-Type": "application/json; charset=UTF-8",

        "Referer": (
            "https://www.irctc.co.in/"
            "nget/train-search"
        ),

        "Origin": "https://www.irctc.co.in",

        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),

        "sec-ch-ua": (
            '"Not=A?Brand";v="99", '
            '"Google Chrome";v="151", '
            '"Chromium";v="151"'
        ),

        "sec-ch-ua-mobile": "?0",

        "sec-ch-ua-platform": '"Windows"',

        "bmirak": "webbm",

        # These values came from your working Postman request.
        "greq": (
            "1787248453075:"
            "4ce11695-e455-4fc7-9491-43e4a33594eb"
        ),

        "bmiyek": (
            "43366DDFA7C0617D2C08AF67F45AB6DD"
        )
    }

    session.headers.update(headers)

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # These cookies are from your working Postman request.
    # They can expire/change. If IRCTC stops accepting them,
    # copy fresh values from the working Postman request.
    # --------------------------------------------------------

    cookies = {

        "TS01aeac8e": (
            "01d83d9ce7989bfbb75ea87c03746648c49b06ef13aab8c2cb4b44cdbb5b6de"
            "0741bf2874e5af76989274a38c367a581566c0aae49"
        ),

        "ngetAppId": (
            "QiYpt6e-hH_fO6yp1vHXzpr6KTnH_Xi5fmT1lF4gEJni8k3p4-sF!977690173"
        ),

        "TS018d84e5": (
            "01d83d9ce7989bfbb75ea87c03746648c49b06ef13aab8c2cb4b44cdbb5b6de"
            "0741bf2874e5af76989274a38c367a581566c0aae49"
        ),

        "_abck": (
            "2AB767764FB7815AF51CBAC78B56CEBF~-1~"
            "YAAQdwosFz2qBuufAQAA1ae3KRASmG/W9W7Ivnu/2YEFC6qQzwlFcxVipgjm8yh"
            "R2e1HrZeGZMxFBCYKWcNO4FiZWs7231HOMBrq0ZjrFtPNmNmK1acXzJED7Nsw6"
            "IHoeesxoFMB7vtij10F+RgxVDxHzsdgS5bhAl4grGgAPLiqrToaNzVLnHdAm"
            "/S4wBxhxuNFrDzS4GDzP6CIkpadrtrJyt3NqVyVdw6HxCcB4fKt0IQuaRoHh"
            "0JfX8halaUUf/IGmuUwh5fjiY7dZbe7RGIcMWAyLAGDMsdSG2REm2tFAc1Np"
            "THOSNARw+pfv3fw9W88/rU5sHMOuWHdkX3uCX4ojNe28Rvuwj5s33pGF9kR39"
            "GjFFNBJa2vk3uVV78iYSu0wwAHCKgRXKd7fnNY4qPGK19h5T1Ct7KbF+e07OG"
            "MkM8Hy42PlPKLKlHZMBkA60EJp84OSYx5OVJIfXNOyEW+jZ01CE2dC8Q"
            "l2L2FlMOOqkJAAk642zK/ri5/89vnmXY0VPppCExXF/er8MO8j5aTS1gtMNyGq"
            "GaAX4VK1WUJEslbQqeNF765G4Bhojt7UQIGh1Ke1COJ6ZusuLU+fYXvurwOYBF"
            "5IA=="
        ),

        "bm_s": (
            "YAAQdwosFz6qBuufAQAA1ae3KQXtJSa+h/PUb4TYfQiPLUgCtVOKXC83EjQws3b"
            "SROyVXLHOWhw4ahw9lVpTrm87iWxe69CGrhC/7zS2ZxtGMr3BGBPErqEaQVZoPc"
            "BHRgw6QUxm8eXymlik0bY+meBib/ki0PnblQYHPa0Fxcuc+Y0VEo3FuGOHBEkn"
            "3fvYwx6eVTuTciLoGprKI10tYhY9jVq5wPDlcI5k/SapVBFJgTH59zzZ80IZm8j"
            "MPTlLOSFLWIIBVgYtvH3AFiimEAgBfHUrH+B1NpWHZC9m2C8mUd0F9BhxaXj"
            "+A/NgLx7QFaxEppXTDUJ8ooz3OKXNH+DmbW0uaSfdVCCFwNPZzsO0DhrJLv4"
            "/ZrCMkr79iEuFGC"
        ),

        "bm_sz": (
            "D46186FB06B4C7087E7D60898D7E7ABA~"
            "YAAQdwosFz+qBuufAQAA1ae3KQBywCubaE6sBrKfVd0YgZ7nyjv5TTIb/"
            "wKwURDTbosaVm4YtN8tkVq0VGifNVnEotz2NeZw3U66Hx9geYIRY9SKowxkw"
            "ZezGC4UTdMk11URhq+ogO7Fgbc9WS/S7yzAfE0+mdS3s0WxESQv6MZ+e+Eg9/"
            "hnZADNVV1hNywa7MLObEYbGcvyF8R2ZY1pyVPTTS4kc0DjMOF5TS6wj+Di309"
            "cZ30YnqrsnTOOJKzYnCTsxKpkI2LX+BFyermaocUvJNPfHjfDKiUSMjuc8E+"
            "1xQqKyMSowwXLfm34Zt5T5QUCJqYiRoU3OfmPfbW0uaSfdVCCFwNPZzsO0Dhr"
            "JLv4/ZrCMkr79iEuFGc=~4474160~3618872"
        ),

        "et_appVIP1": "1160269322.19743.0000"
    }

    session.cookies.update(cookies)

    return session


# ============================================================
# USER INPUT
# ============================================================

def get_search_input():

    print("\n" + "=" * 60)
    print("IRCTC TRAIN SEARCH")
    print("=" * 60)

    from_station = input(
        "From station code : "
    ).strip().upper()

    to_station = input(
        "To station code   : "
    ).strip().upper()

    journey_date = input(
        "Journey date (DDMMYYYY) : "
    ).strip()

    try:

        date_obj = datetime.strptime(
            journey_date,
            "%d%m%Y"
        )

        irctc_date = date_obj.strftime(
            "%Y%m%d"
        )

    except ValueError:

        print(
            "\nInvalid date."
            "\nPlease use DDMMYYYY format."
        )

        return None

    return (
        from_station,
        to_station,
        irctc_date
    )


# ============================================================
# SEARCH TRAINS
# ============================================================

def search_trains(
    session,
    from_station,
    to_station,
    journey_date
):

    payload = {

        "srcStn": from_station,

        "destStn": to_station,

        "jrnyClass": "",

        "jrnyDate": journey_date,

        "quotaCode": "GN",

        "currentBooking": "false",

        "flexiFlag": False,

        "handicapFlag": False,

        "ticketType": "E",

        "loyaltyRedemptionBooking": False,

        "ftBooking": False
    }

    # Search request uses train-search referer.
    session.headers.update({
        "Referer": (
            "https://www.irctc.co.in/"
            "nget/train-search"
        )
    })

    print("\nSearching trains...")

    print(
        f"{from_station} -> "
        f"{to_station} "
        f"on {journey_date}"
    )

    try:

        response = session.post(
            SEARCH_URL,
            json=payload,
            timeout=30
        )

        # print(
        #     "\nHTTP Status:",
        #     response.status_code
        # )

        print(
            "Content-Type:",
            response.headers.get(
                "Content-Type"
            )
        )

        if not response.text.strip():

            print(
                "\nIRCTC returned an empty response."
            )

            return None

        try:

            data = response.json()

        except ValueError:

            print(
                "\nIRCTC returned a non-JSON response."
            )

            print(
                response.text[:1000]
            )

            return None

        return data

    except requests.exceptions.RequestException as e:

        print(
            "\nSearch request failed:"
        )

        print(e)

        return None


# ============================================================
# DISPLAY TRAIN LIST
# ============================================================

def display_train_list(data):

    trains = data.get(
        "trainBtwnStnsList",
        []
    )
    # Sort trains by departure time (earliest first)
    trains.sort(
    key=lambda train: datetime.strptime(
        train.get("departureTime", "23:59"),
        "%H:%M"
    )
)

    if not trains:

        print(
            "\nNo trains found."
        )

        return []

    print("\n")
    print("=" * 95)
    print("AVAILABLE TRAINS")
    print("=" * 95)

    for index, train in enumerate(
        trains,
        start=1
    ):

        train_number = train.get(
            "trainNumber",
            ""
        )

        train_name = train.get(
            "trainName",
            ""
        )

        departure = train.get(
            "departureTime",
            ""
        )

        arrival = train.get(
            "arrivalTime",
            ""
        )

        duration = train.get(
            "duration",
            ""
        )

        distance = train.get(
            "distance",
            ""
        )

        classes = train.get(
            "avlClasses",
            []
        )

        print(
            f"{index}. "
            f"{train_name} "
            f"({train_number})"
        )

        print(
            f"   {departure} -> {arrival}"
        )

        print(
            f"   Duration : {duration}"
        )

        print(
            f"   Distance : {distance} km"
        )

        print(
            f"   Classes  : "
            f"{', '.join(classes)}"
        )

        print("-" * 95)

    print("0. Back / New Search")

    return trains


# ============================================================
# SELECT TRAIN
# ============================================================

def select_train(trains):

    while True:

        try:

            choice = int(
                input(
                    "\nSelect train number "
                    "(0 = New Search): "
                )
            )

        except ValueError:

            print(
                "Please enter a number."
            )

            continue

        if choice == 0:

            return None

        if choice < 1 or choice > len(trains):

            print(
                "Invalid train selection."
            )

            continue

        return trains[choice - 1]


# ============================================================
# DISPLAY CLASS LIST
# ============================================================

def display_class_list(selected_train):

    classes = selected_train.get(
        "avlClasses",
        []
    )

    if not classes:

        print(
            "\nNo classes available."
        )

        return []

    print("\n")
    print("=" * 60)
    print("AVAILABLE CLASSES")
    print("=" * 60)

    for index, class_code in enumerate(
        classes,
        start=1
    ):

        class_name = get_class_name(
            class_code
        )

        print(
            f"{index}. "
            f"{class_code} - "
            f"{class_name}"
        )

    print(
        "0. Back to Train List"
    )

    return classes


# ============================================================
# CLASS NAME
# ============================================================

def get_class_name(class_code):

    class_names = {

        "1A": "AC First Class",

        "2A": "AC 2 Tier",

        "3A": "AC 3 Tier",

        "3E": "AC 3 Economy",

        "SL": "Sleeper",

        "CC": "AC Chair Car",

        "EC": "Executive Chair Car",

        "2S": "Second Sitting"
    }

    return class_names.get(
        class_code,
        class_code
    )


# ============================================================
# SELECT CLASS
# ============================================================

def select_class(classes):

    while True:

        try:

            choice = int(
                input(
                    "\nSelect class "
                    "(0 = Back): "
                )
            )

        except ValueError:

            print(
                "Please enter a number."
            )

            continue

        if choice == 0:

            return None

        if choice < 1 or choice > len(classes):

            print(
                "Invalid class selection."
            )

            continue

        return classes[choice - 1]


# ============================================================
# GET QUOTA
# ============================================================

def get_quota():

    # For the availability API we use GN by default,
    # matching your supplied working cURL.
    #
    # You can expand this later if you want
    # quota selection as another menu.

    print("\n")
    print("=" * 60)
    print("QUOTA")
    print("=" * 60)

    print("1. GN - General")

    print("0. Back")

    while True:

        try:

            choice = int(
                input(
                    "\nSelect quota: "
                )
            )

        except ValueError:

            print(
                "Please enter a number."
            )

            continue

        if choice == 0:

            return None

        if choice == 1:

            return "GN"

        print(
            "Invalid quota selection."
        )


# ============================================================
# AVAILABILITY API
# ============================================================

def get_availability(
    session,
    selected_train,
    from_station,
    to_station,
    journey_date,
    class_code,
    quota_code
):

    train_number = selected_train.get(
        "trainNumber"
    )

    # --------------------------------------------------------
    # URL
    #
    # Example:
    #
    # /avlFarenquiry/
    # 22639/
    # 20260825/
    # MAS/
    # CBE/
    # SL/
    # GN/
    # N
    # --------------------------------------------------------

    url = (
        f"{AVAILABILITY_BASE_URL}/"
        f"{train_number}/"
        f"{journey_date}/"
        f"{from_station}/"
        f"{to_station}/"
        f"{class_code}/"
        f"{quota_code}/"
        f"N"
    )

    payload = {

        "paymentFlag": "N",

        "concessionBooking": False,

        "ftBooking": False,

        "loyaltyRedemptionBooking": False,

        "ticketType": "E",

        "quotaCode": quota_code,

        "moreThanOneDay": True,

        "returnJourney": False,

        "trainNumber": train_number,

        "fromStnCode": from_station,

        "toStnCode": to_station,

        "isLogedinReq": False,

        "journeyDate": journey_date,

        "classCode": class_code
    }

    # These headers match the availability request
    # you supplied.

    session.headers.update({

        "Accept": (
            "application/json, text/plain, */*"
        ),

        "Accept-Language": (
            "en-US,en;q=0.0"
        ),

        "Content-Language": "en",

        "Content-Type": (
            "application/json; charset=UTF-8"
        ),

        "Origin": (
            "https://www.irctc.co.in"
        ),

        "Referer": (
            "https://www.irctc.co.in/"
            "nget/booking/train-list"
        ),

        "bmirak": "webbm",

        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),

        "sec-ch-ua": (
            '"Not=A?Brand";v="99", '
            '"Google Chrome";v="151", '
            '"Chromium";v="151"'
        ),

        "sec-ch-ua-mobile": "?0",

        "sec-ch-ua-platform": '"Windows"'
    })

    print("\n")
    print("=" * 70)
    print("CHECKING AVAILABILITY")
    print("=" * 70)

    print(
        f"Train : {train_number} - "
        f"{selected_train.get('trainName')}"
    )

    print(
        f"Route : {from_station} -> "
        f"{to_station}"
    )

    print(
        f"Class : {class_code} - "
        f"{get_class_name(class_code)}"
    )

    print(
        f"Quota : {quota_code}"
    )

    print(
        f"Date  : {journey_date}"
    )

    try:

        response = session.post(
            url,
            json=payload,
            timeout=30
        )

        # print(
        #     "\nHTTP Status:",
        #     response.status_code
        # )

        if not response.text.strip():

            print(
                "\nEmpty response received."
            )

            return None

        try:

            data = response.json()

        except ValueError:

            print(
                "\nIRCTC returned a non-JSON response."
            )

            print(
                response.text[:2000]
            )

            return None

        return data

    except requests.exceptions.RequestException as e:

        print(
            "\nAvailability request failed:"
        )

        print(e)

        return None


# ============================================================
# DISPLAY AVAILABILITY
# ============================================================

def display_availability(data):

    if not data:

        return

    print("\n")
    print("=" * 80)
    print("AVAILABILITY RESULT")
    print("=" * 80)

    train_name = data.get(
        "trainName",
        ""
    )

    train_number = data.get(
        "trainNo",
        ""
    )

    from_station = data.get(
        "from",
        ""
    )

    to_station = data.get(
        "to",
        ""
    )

    quota = data.get(
        "quota",
        ""
    )

    enq_class = data.get(
        "enqClass",
        ""
    )

    print(
        f"Train       : "
        f"{train_number} - {train_name}"
    )

    print(
        f"Route       : "
        f"{from_station} -> {to_station}"
    )

    print(
        f"Class       : "
        f"{enq_class} - "
        f"{get_class_name(enq_class)}"
    )

    print(
        f"Quota       : {quota}"
    )

    print(
        f"Base Fare   : ₹{data.get('baseFare', '0')}"
    )

    print(
        f"Total Fare  : ₹{data.get('totalFare', '0')}"
    )

    print("\n" + "-" * 80)

    availability_days = data.get(
        "avlDayList",
        []
    )

    if not availability_days:

        print(
            "No availability information returned."
        )

    else:

        print(
            "DATE-WISE AVAILABILITY"
        )

        print("-" * 80)

        for day in availability_days:

            date = day.get(
                "availablityDate",
                ""
            )

            status = day.get(
                "availablityStatus",
                ""
            )

            current_booking = day.get(
                "currentBkgFlag",
                ""
            )

            print(
                f"{date:<15} "
                f"{status:<25} "
                f"Current Booking: "
                f"{current_booking}"
            )

    print("-" * 80)

    # --------------------------------------------------------
    # Interpret availability
    # --------------------------------------------------------

    print("\nSTATUS SUMMARY")

    if availability_days:

        for day in availability_days:

            status = day.get(
                "availablityStatus",
                ""
            )

            date = day.get(
                "availablityDate",
                ""
            )

            if "AVAILABLE" in status.upper():

                print(
                    f"✓ {date}: "
                    f"{status}"
                )

            elif "WL" in status.upper():

                print(
                    f"⚠ {date}: "
                    f"{status} "
                    f"(Waiting List)"
                )

            elif "RAC" in status.upper():

                print(
                    f"⚠ {date}: "
                    f"{status} "
                    f"(RAC)"
                )

            else:

                print(
                    f"• {date}: "
                    f"{status}"
                )

    print("\n" + "=" * 80)


# ============================================================
# AVAILABILITY MENU
# ============================================================

def availability_menu(
    session,
    selected_train,
    from_station,
    to_station,
    journey_date
):

    while True:

        classes = display_class_list(
            selected_train
        )

        if not classes:

            input(
                "\nPress ENTER to go back..."
            )

            return

        selected_class = select_class(
            classes
        )

        # 0 -> Back to train list
        if selected_class is None:

            return

        quota_code = get_quota()

        # 0 -> Back to class menu
        if quota_code is None:

            continue

        data = get_availability(
            session=session,
            selected_train=selected_train,
            from_station=from_station,
            to_station=to_station,
            journey_date=journey_date,
            class_code=selected_class,
            quota_code=quota_code
        )

        if data:

            display_availability(data)

        print("\n")
        print("=" * 60)
        print("OPTIONS")
        print("=" * 60)
        print("0. Back to Main Search")

        while True:

            try:

                choice = int(
                    input(
                        "\nEnter 0 to go back: "
                    )
                )

                if choice == 0:

                    return

                print(
                    "Please enter 0."
                )

            except ValueError:

                print(
                    "Please enter 0."
                )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    # Create ONE session.
    #
    # This same session is reused for:
    #
    # 1. Train search
    # 2. Availability enquiry
    #
    # This is important for cookies/session state.

    session = create_session()

    while True:

        # ----------------------------------------------------
        # SEARCH SCREEN
        # ----------------------------------------------------

        search_input = get_search_input()

        if not search_input:

            continue

        (
            from_station,
            to_station,
            journey_date
        ) = search_input

        # ----------------------------------------------------
        # TRAIN SEARCH
        # ----------------------------------------------------

        data = search_trains(
            session=session,
            from_station=from_station,
            to_station=to_station,
            journey_date=journey_date
        )

        if not data:

            print(
                "\nSearch failed."
            )

            input(
                "\nPress ENTER to try again..."
            )

            continue

        # ----------------------------------------------------
        # TRAIN LIST
        # ----------------------------------------------------

        while True:

            trains = display_train_list(
                data
            )

            if not trains:

                break

            # ------------------------------------------------
            # TRAIN SELECTION
            # ------------------------------------------------

            selected_train = select_train(
                trains
            )

            # 0 -> New Search
            if selected_train is None:

                break

            print("\n")
            print("=" * 60)
            print("SELECTED TRAIN")
            print("=" * 60)

            print(
                f"Train Number : "
                f"{selected_train.get('trainNumber')}"
            )

            print(
                f"Train Name   : "
                f"{selected_train.get('trainName')}"
            )

            print(
                f"Route        : "
                f"{selected_train.get('fromStnCode')} "
                f"-> "
                f"{selected_train.get('toStnCode')}"
            )

            print(
                f"Departure    : "
                f"{selected_train.get('departureTime')}"
            )

            print(
                f"Arrival      : "
                f"{selected_train.get('arrivalTime')}"
            )

            # ------------------------------------------------
            # AVAILABILITY MENU
            # ------------------------------------------------

            availability_menu(
                session=session,
                selected_train=selected_train,
                from_station=from_station,
                to_station=to_station,
                journey_date=journey_date
            )

            # After availability -> go back to main search
            break


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()
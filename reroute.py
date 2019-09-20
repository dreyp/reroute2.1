import info_sql

while True:
    barcode_scan = input('Please scan Barcode: ')
    barcode = info_sql.find_asin(barcode_scan)
    info_sql.copy_to_clipboard(barcode)
    info_from_scan = info_sql.check_item(barcode)
    if info_from_scan.text == "[]":
        info_from_scan = info_sql.check_data_15(barcode)
        if info_from_scan is False:
            text = ("Please enter ASIN For Item " + barcode_scan + " or press enter to skip: ")
            ASIN = input(text)
            if ASIN == "":
                print("This item was skipped")
            else:
                info_from_scan = info_sql.check_item(ASIN)
                Data = barcode_scan, ASIN, info_sql.timestamp()
                add = info_sql.add_asin(Data)
                if add == "Added":
                    print("ASIN Was added to Database")
                    info_from_scan = info_sql.check_data_15(ASIN)
                    if info_from_scan is False:
                        print("There was trouble finding the item please try again later")
                    else:
                        Result = info_sql.sort_data_from_web(info_from_scan)
                        print(Result)

                else:
                    print("There was a problem inputting the ASIN please try again")

    else:
        Result = info_sql.sort_data_from_web(info_from_scan)
        print(Result)

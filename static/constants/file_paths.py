class WebAppConstants:
    try:
        HOUSEHOLD_UPLOAD_FILE_PATH = '/tmp/static/UploadFiles/Households'
        TRANSACTIONS_UPLOAD_FILE_PATH = '/tmp/static/UploadFiles/Transactions'
        PRODUCTS_UPLOAD_FILE_PATH = '/tmp/static/UploadFiles/Products'
    except Exception as e:
        print("Upload Paths are not found")
        raise e


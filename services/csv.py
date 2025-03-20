import pandas as pd


class CSVService:
    def __init__(self):
        pass

    def write_to_database(self, file, process_row_callback, valid_rows):
        """

        :param file: csv file to be processed.
        :param process_row_callback: The callback function which is called with single row each time.
        :param valid_rows: valid_rows are again passed to callback to maintain the valid rows after doing
        custom validation
        :return: response = {
            "success": True,
            "errors": errors,
            "created_rows": created_rows,
            "message": message
        }
        """
        errors = []
        created_rows = []
        message = ""
        response = {
            "success": True,
            "errors": errors,
            "created_rows": created_rows,
            "message": message
        }
        try:
            df = pd.read_csv(file)
        except Exception as e:
            message = f"Failed to read CSV: {str(e)}"
            response["success"] = False
            response["message"] = message
            return response

        for index, row in df.iterrows():
            try:
                process_row_callback(row, valid_rows)
            except Exception as e:
                errors.append({"row": index + 1, "error": str(e)})
                response["success"] = False

        return response

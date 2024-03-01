from returnReportData import returnReportData
from locateReports import locateReports
from returnSettingsData import returnSettingsData
from saveDataToTable import fillSQL
from init import file_root, file_extension, standard_path, settings_path
import argparse
import logger

#MAIN
def main(init_run):
    # Locate report files and settings files
    logger.logger.info("Start........................................................")
    ReportLocations, SettingsLocations = locateReports(file_extension, file_root, standard_path, settings_path)

    #Retrieve connection information from settings files
    logger.logger.info("Retrieving settings data...")
    print("Retrieving settings data...")
    ConnectionInfo = returnSettingsData(SettingsLocations)

    # Retrieve report data from located files
    print("\nRetrieving report data...")
    logger.logger.info("\n\nRetrieving report data...")
    ReportData = returnReportData(ReportLocations, ConnectionInfo)

    # Save report data to SQL table
    logger.logger.info("Saving report data to SQL table...")
    fillSQL(ReportData, init_run)
    print("Success")
    logger.logger.info("End..........................................................")

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true")
    args = parser.parse_args()

    init = False
    if args.init:
        init = True
        logger.logger.info("___Initial Run___")

    # Call the main function with the initialization flag
    main(init)

"""
The main function is the main logic of the program. It takes an init_run parameter indicating whether it's an initialization run or not. Inside the function, it performs the following steps:

locateReports: It calls the locateReports function to locate report files based on the provided file_extension, file_root, and standard_path parameters. The result is stored in the ReportLocations variable.

returnReportData: It calls the returnReportData function and passes the ReportLocations to retrieve the report data from the located files. The result is stored in the ReportData variable.

fillSQL: It calls the fillSQL function and passes the ReportData along with the init_run flag to save the report data to an SQL table.

Finally, it prints "Success" to indicate that the program has finished successfully.

The code also includes a section that checks if the script is being run as the main module (if __name__ == '__main__':). It utilizes the argparse module to parse command-line arguments. If the --init flag is provided, the init variable is set to True, indicating an initialization run. Then, it calls the main function with the init flag passed as an argument.

The code uses logging to log messages to a log file specified by log_loc. The log file captures information about the program's execution.
"""
import os
import configparser

from src.postalCodes.ParsingPostalCodes import ParsingPostalCodes
from src.licenseMinCulture.ParsingMinCultLicenses import ParsingMinCultLicenses


if __name__ == "__main__":

    # a = ParsingMinCultLicenses()
    # a.runDataParsing()

    a = ParsingPostalCodes()
    a.processRun()

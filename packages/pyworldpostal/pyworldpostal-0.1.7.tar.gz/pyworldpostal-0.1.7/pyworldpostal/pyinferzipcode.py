#!/usr/bin/env python
# -*- coding: utf-8 -*-
# git filter-branch --tree-filter "rm -rf pyzipcode/allCountries.txt" HEAD
# git filter-branch -f  --index-filter "git rm --cached --ignore-unmatch pyzipcode/allCountries.txt"
# git filter-branch -f --index-filter "git rm --cached --ignore-unmatch fixtures/11_user_answer.json"
# GB is delivery is pending
import pandas as pd
from typing import Union

__version__ = "0.1.0"
__author__ = "Dalwinder singh"

val_countries = ["AD", "AR", "AS", "AT", "AU", "AX", "AZ", "BD", "BE", "BG", "BM", "BR", "BY", "CA", "CH", "CL", "CO",
                "CR", "CY", "CZ", "DE", "DK", "DO", "DZ", "EE", "ES", "FI", "FM", "FO", "FR", "GB", "GF", "GG", "GL",
                "GP", "GT", "GU", "HR", "HU", "IE", "IM", "IN", "IS", "IT", "JE", "JP", "KR", "LI", "LK", "LT", "LU",
                "LV", "MC", "MD", "MH", "MK", "MP", "MQ", "MT", "MW", "MX", "MY", "NC", "NL", "NO", "NZ", "PE", "PH",
                "PK", "PL", "PM", "postal_data", "PR", "PT", "PW", "RE", "RO", "RS", "RU", "SE", "SG",
                "SI", "SJ", "SK", "SM", "TH", "TR", "UA", "US", "UY", "VA", "VI", "WF", "YT", "ZA"]


class WorldPostalSearch(object):
    def valid_countries(self):
        return val_countries

    def bulkget(self, pin_contry: list):
        res = []
        for i in pin_contry:
            pincode, country_code = i[0], i[1]
            out = self._get(pincode, country_code)
            if len(res) == 0:
                res.extend(out)
            if bool(out[0]):
                res.extend(out)
        return res

    def return_df(self, pincode, df):
        if isinstance(pincode, list):
            df = df[df["postal_code"].isin(pincode)]
        if isinstance(pincode, str):
            df = df[df["postal_code"].isin([pincode])]
        if df.empty:
            return [{}]
        else:
            df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2", "admin_name3",
                          "place_name"]
            return df.to_dict("records")

    def _get(self, pincode: Union[list, str], country: str):
        if country in val_countries:
            if country == "AD":
                from pyworldpostal.country_files import AD
                df = pd.DataFrame(AD.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "AR":
                from pyworldpostal.country_files import AR
                df = pd.DataFrame(AR.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "AS":
                from pyworldpostal.country_files import AS
                df = pd.DataFrame(AS.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "AT":
                from pyworldpostal.country_files import AT
                df = pd.DataFrame(AT.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "AU":
                from pyworldpostal.country_files import AU
                df = pd.DataFrame(AU.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "AX":
                from pyworldpostal.country_files import AX
                df = pd.DataFrame(AX.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "AZ":
                from pyworldpostal.country_files import AZ
                df = pd.DataFrame(AZ.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "BD":
                from pyworldpostal.country_files import BD
                df = pd.DataFrame(BD.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "BE":
                from pyworldpostal.country_files import BE
                df = pd.DataFrame(BE.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "BG":
                from pyworldpostal.country_files import BG
                df = pd.DataFrame(BG.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "BM":
                from pyworldpostal.country_files import BM
                df = pd.DataFrame(BM.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "BR":
                from pyworldpostal.country_files import BR
                df = pd.DataFrame(BR.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "BY":
                from pyworldpostal.country_files import BY
                df = pd.DataFrame(BY.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "CA":
                from pyworldpostal.country_files import CA
                df = pd.DataFrame(CA.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "CH":
                from pyworldpostal.country_files import CH
                df = pd.DataFrame(CH.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "CL":
                from pyworldpostal.country_files import CL
                df = pd.DataFrame(CL.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "CO":
                from pyworldpostal.country_files import CO
                df = pd.DataFrame(CO.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "CR":
                from pyworldpostal.country_files import CR
                df = pd.DataFrame(CR.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "CY":
                from pyworldpostal.country_files import CY
                df = pd.DataFrame(CY.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "CZ":
                from pyworldpostal.country_files import CZ
                df = pd.DataFrame(CZ.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "DE":
                from pyworldpostal.country_files import DE
                df = pd.DataFrame(DE.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "DK":
                from pyworldpostal.country_files import DK
                df = pd.DataFrame(DK.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "DO":
                from pyworldpostal.country_files import DO
                df = pd.DataFrame(DO.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "DZ":
                from pyworldpostal.country_files import DZ
                df = pd.DataFrame(DZ.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "EE":
                from pyworldpostal.country_files import EE
                df = pd.DataFrame(EE.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "ES":
                from pyworldpostal.country_files import ES
                df = pd.DataFrame(ES.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "FI":
                from pyworldpostal.country_files import FI
                df = pd.DataFrame(FI.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "FM":
                from pyworldpostal.country_files import FM
                df = pd.DataFrame(FM.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "FO":
                from pyworldpostal.country_files import FO
                df = pd.DataFrame(FO.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "FR":
                from pyworldpostal.country_files import FR
                df = pd.DataFrame(FR.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            # elif country == "GB":
            #     from pyworldpostal.country_files import GB
            #     df = pd.DataFrame(GB.PostalData().data())
            #     if isinstance(pincode, list):
            #         df = df[df["postal_code"].isin(pincode)]
            #     if isinstance(pincode, str):
            #         df = df[df["postal_code"].isin([pincode])]
            #     if df.empty:
            #         return [{}]
            #     else:
            #         df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
            #                       "admin_name3", "place_name"]
            #         return df.to_dict("records")
            elif country == "GF":
                from pyworldpostal.country_files import GF
                df = pd.DataFrame(GF.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "GG":
                from pyworldpostal.country_files import GG
                df = pd.DataFrame(GG.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "GL":
                from pyworldpostal.country_files import GL
                df = pd.DataFrame(GL.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "GP":
                from pyworldpostal.country_files import GP
                df = pd.DataFrame(GP.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "GT":
                from pyworldpostal.country_files import GT
                df = pd.DataFrame(GT.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "GU":
                from pyworldpostal.country_files import GU
                df = pd.DataFrame(GU.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "HR":
                from pyworldpostal.country_files import HR
                df = pd.DataFrame(HR.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "HU":
                from pyworldpostal.country_files import HU
                df = pd.DataFrame(HU.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "IE":
                from pyworldpostal.country_files import IE
                df = pd.DataFrame(IE.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "IM":
                from pyworldpostal.country_files import IM
                df = pd.DataFrame(IM.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "IN":
                from pyworldpostal.country_files import IN
                df = pd.DataFrame(IN.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "IS":
                from pyworldpostal.country_files import IS
                df = pd.DataFrame(IS.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "IT":
                from pyworldpostal.country_files import IT
                df = pd.DataFrame(IT.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "JE":
                df = pd.DataFrame(JE.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "JP":
                from pyworldpostal.country_files import JP
                df = pd.DataFrame(JP.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "KR":
                from pyworldpostal.country_files import KR
                df = pd.DataFrame(KR.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "LI":
                from pyworldpostal.country_files import LI
                df = pd.DataFrame(LI.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "LK":
                from pyworldpostal.country_files import LK
                df = pd.DataFrame(LK.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "LT":
                from pyworldpostal.country_files import LT
                df = pd.DataFrame(LT.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "LU":
                from pyworldpostal.country_files import LU
                df = pd.DataFrame(LU.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "LV":
                from pyworldpostal.country_files import LV
                df = pd.DataFrame(LV.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "MC":
                from pyworldpostal.country_files import MC
                df = pd.DataFrame(MC.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "MD":
                from pyworldpostal.country_files import MD
                df = pd.DataFrame(MD.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "MH":
                from pyworldpostal.country_files import MH
                df = pd.DataFrame(MH.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "MK":
                from pyworldpostal.country_files import MK
                df = pd.DataFrame(MK.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "MP":
                from pyworldpostal.country_files import MP
                df = pd.DataFrame(MP.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "MQ":
                from pyworldpostal.country_files import MQ
                df = pd.DataFrame(MQ.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "MT":
                from pyworldpostal.country_files import MT
                df = pd.DataFrame(MT.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "MW":
                from pyworldpostal.country_files import MW
                df = pd.DataFrame(MW.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "MX":
                from pyworldpostal.country_files import MX
                df = pd.DataFrame(MX.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "MY":
                from pyworldpostal.country_files import MY
                df = pd.DataFrame(MY.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "NC":
                from pyworldpostal.country_files import NC
                df = pd.DataFrame(NC.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "NL":
                from pyworldpostal.country_files import NL
                df = pd.DataFrame(NL.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "NO":
                from pyworldpostal.country_files import NO
                df = pd.DataFrame(NO.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "NZ":
                from pyworldpostal.country_files import NZ
                df = pd.DataFrame(NZ.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "PE":
                from pyworldpostal.country_files import PE
                df = pd.DataFrame(PE.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "PH":
                from pyworldpostal.country_files import PH
                df = pd.DataFrame(PH.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "PK":
                from pyworldpostal.country_files import PK
                df = pd.DataFrame(PK.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "PL":
                from pyworldpostal.country_files import PL
                df = pd.DataFrame(PL.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "PM":
                from pyworldpostal.country_files import PM
                df = pd.DataFrame(PM.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "PR":
                from pyworldpostal.country_files import PR
                df = pd.DataFrame(PR.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "PT":
                from pyworldpostal.country_files import PT
                df = pd.DataFrame(PT.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "PW":
                from pyworldpostal.country_files import PW
                df = pd.DataFrame(PW.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "RE":
                from pyworldpostal.country_files import RE
                df = pd.DataFrame(RE.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "RO":
                from pyworldpostal.country_files import RO
                df = pd.DataFrame(RO.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "RS":
                from pyworldpostal.country_files import RS
                df = pd.DataFrame(RS.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "RU":
                from pyworldpostal.country_files import RU
                df = pd.DataFrame(RU.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "SE":
                from pyworldpostal.country_files import SE
                df = pd.DataFrame(SE.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "SG":
                from pyworldpostal.country_files import SG
                df = pd.DataFrame(SG.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "SI":
                from pyworldpostal.country_files import SI
                df = pd.DataFrame(SI.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "SJ":
                from pyworldpostal.country_files import SJ
                df = pd.DataFrame(SJ.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "SK":
                from pyworldpostal.country_files import SK
                df = pd.DataFrame(SK.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "SM":
                from pyworldpostal.country_files import SM
                df = pd.DataFrame(SM.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "TH":
                from pyworldpostal.country_files import TH
                df = pd.DataFrame(TH.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "TR":
                from pyworldpostal.country_files import TR
                df = pd.DataFrame(TR.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "UA":
                from pyworldpostal.country_files import UA
                df = pd.DataFrame(UA.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "US":
                from pyworldpostal.country_files import US
                df = pd.DataFrame(US.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "UY":
                from pyworldpostal.country_files import UY
                df = pd.DataFrame(UY.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "VA":
                from pyworldpostal.country_files import VA
                df = pd.DataFrame(VA.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "VI":
                from pyworldpostal.country_files import VI
                df = pd.DataFrame(VI.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "WF":
                from pyworldpostal.country_files import WF
                df = pd.DataFrame(WF.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "YT":
                from pyworldpostal.country_files import YT
                df = pd.DataFrame(YT.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            elif country == "ZA":
                from pyworldpostal.country_files import ZA
                df = pd.DataFrame(ZA.PostalData().data())
                if isinstance(pincode, list):
                    df = df[df["postal_code"].isin(pincode)]
                if isinstance(pincode, str):
                    df = df[df["postal_code"].isin([pincode])]
                if df.empty:
                    return [{}]
                else:
                    df.columns = ["postal_code", "country_code", "state_code", "state_name", "admin_name2",
                                  "admin_name3", "place_name"]
                    return df.to_dict("records")
            else:
                return [{}]
        else:
            return [{}]

#print(WorldPostalSearch().bulkget([("AD100", "AD"), ("AD1000", "AD"), ("AD100", "AD"), ("AD200", "AD")]))


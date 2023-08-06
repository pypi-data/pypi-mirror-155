#!/usr/bin/env python
# -*- coding: utf-8 -*-
# git filter-branch --tree-filter "rm -rf pyzipcode/allCountries.txt" HEAD
# git filter-branch -f  --index-filter "git rm --cached --ignore-unmatch pyzipcode/allCountries.txt"
# git filter-branch -f --index-filter "git rm --cached --ignore-unmatch fixtures/11_user_answer.json"
# GB is delivery is pending
import pandas as pd
from typing import Union
from pyworldpostal.country_files import (AD, AR, AS, AT, AU, AX, AZ, BD, BE, BG, BM, BR, BY, CA, CH, CL, CO, CR, CY, CZ, DE, DK, DO,
                           DZ, EE, ES, FI, FM, FO, FR, GF, GG, GL, GP, GT, GU, HR, HU, IE, IM, IN, IS, IT, JE, JP,
                           KR, LI, LK, LT, LU, LV, MC, MD, MH, MK, MP, MQ, MT, MW, MX, MY, NC, NL, NO, NZ, PE, PH, PK,
                           PL, PM, PR, PT, PW, RE, RO, RS, RU, SE, SG, SI, SJ, SK, SM, TH, TR, UA, US, UY,
                           VA, VI, WF, YT, ZA)

__version__ = "0.1.0"
__author__ = "Dalwinder singh"

val_counties = ["AD", "AR", "AS", "AT", "AU", "AX", "AZ", "BD", "BE", "BG", "BM", "BR", "BY", "CA", "CH", "CL", "CO",
                "CR", "CY", "CZ", "DE", "DK", "DO", "DZ", "EE", "ES", "FI", "FM", "FO", "FR", "GB", "GF", "GG", "GL",
                "GP", "GT", "GU", "HR", "HU", "IE", "IM", "IN", "IS", "IT", "JE", "JP", "KR", "LI", "LK", "LT", "LU",
                "LV", "MC", "MD", "MH", "MK", "MP", "MQ", "MT", "MW", "MX", "MY", "NC", "NL", "NO", "NZ", "PE", "PH",
                "PK", "PL", "PM", "postal_data", "PR", "PT", "PW", "RE", "RO", "RS", "RU", "SE", "SG",
                "SI", "SJ", "SK", "SM", "TH", "TR", "UA", "US", "UY", "VA", "VI", "WF", "YT", "ZA"]


class WorldPostalSearch(object):
    def valid_countries(self):
        return val_counties

    def bulkget(self, pin_contry: list):
        res = []
        for i in pin_contry:
            pincode, country_code = i[0], i[1]
            out = self._get(pincode, country_code)
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
        if country in val_counties:
            if country == "AD":
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
                [{}]

#print(WorldPostalSearch().bulkget([("AD100", "AD"), ("AD1000", "AD"), ("AD100", "AD"), ("AD200", "AD")]))


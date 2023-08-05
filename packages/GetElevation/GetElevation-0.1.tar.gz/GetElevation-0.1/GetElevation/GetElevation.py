import time
import requests
import pandas as pd
from pandas import DataFrame


class _ElevationRequest(object):

    def __init__(self, latlong: str, mode):
        self.latlong = latlong
        self.mode = mode
        if self.mode not in ("nearest", "bilinear", "cubic"):
            raise ValueError("插值方式错误，请在nearest, bilinear, cubic中选择！")

    def get_elevation(self) -> list:
        query = ('https://api.opentopodata.org/v1/mapzen'
                 f'?locations={self.latlong}&interpolation={self.mode}')

        # nearest, bilinear, cubic. Default: bilinear
        res = requests.get(query).json()
        if res["status"] == "INVALID_REQUEST":
            return [-99999]
        elevation = [res["results"][i]["elevation"] for i in range(len(res["results"]))]
        return elevation


class GetSingleElevation(object):

    def __init__(self, lat, long, mode = "bilinear") -> None:
        """
        :param lat: 纬度：double/int
        :param long: 经度：double/int
        :param mode: 插值方式：str
        """
        self.lat = lat
        self.long = long
        self.mode = mode
        if self.lat > 90 or self.lat < -90:
            raise Exception("纬度应该在-90~90之间")
        if self.long > 180 or self.long < -180:
            raise Exception("经度应该在-180~180之间")

    def __repr__(self) -> str:
        return "纬度:{},经度:{},插值方式:{}".format(self.lat, self.long, self.mode)

    def merge(self):
        return '{},{}'.format(self.lat, self.long)

    def get_elevation(self):
        lat_long = self.merge()
        elevation = _ElevationRequest(lat_long, self.mode)
        elevation = elevation.get_elevation()[0]
        return elevation


class GetMutilElevation(object):
    suffix = ("txt", "TXT", "xlsx", "xls", "XLSX", "XLS", "csv", "CSV")
    df = None
    result = []
    start, end = 0, 100

    def __init__(self, path: str, mode="bilinear", sheetname="Sheet1", ):
        self.path = path
        self.sheetname = sheetname
        self.mode = mode

    def get_suffix(self):
        suffix = self.path.split(".")
        if len(suffix) == 1:
            raise ValueError("文件路径必须包括后缀！")
        else:
            if suffix[-1] not in self.suffix:
                raise ValueError("文件必须为txt格式或excel格式！")
            else:
                return suffix[-1]

    def get_df(self):
        suffix = self.get_suffix()
        if suffix in ("csv", "CSV", "txt", "TXT"):
            self.df = pd.read_csv(self.path)
        elif suffix in ("xlsx", "xls", "XLSX", "XLS"):
            try:
                self.df = pd.read_excel(self.path, sheet_name=self.sheetname)
            except:
                raise ValueError("请检查Sheetname!")
        return self.df

    def check_columnname(self):
        self.df = self.get_df()
        column_list = list(self.df.columns)
        if len(column_list) == 2 and "X" in column_list and "Y" in column_list:
            pass
        else:
            raise ValueError("该Sheet中应当有且只有X和Y两列！")

    def check_lat_long(self):
        check_lat_list = list(filter(lambda x: x > 90 or x < -90, list(self.df["X"])))
        if check_lat_list:
            raise ValueError("纬度(X)中含有不合法数据！请检查")
        check_long_list = list(filter(lambda x: x > 180 or x < -180, list(self.df["Y"])))
        if check_long_list:
            raise ValueError("经度(Y)中含有不合法数据！请检查")

    def query_whole_hundred(self):
        for i in range(self.df.shape[0] // 100):
            latlong = ""
            for j in range(self.start, self.end):
                latlong += (self.df.iloc[j]["latlong"] + "|")
            latlong = latlong[:-1]
            elevation = _ElevationRequest(latlong, self.mode)
            elevation = elevation.get_elevation()
            if len(elevation) == 1 and elevation[0] == -99999:
                # 为了不让出错的部分影响别的数据，对没查询到的数据以默认值替换
                elevation.extend([-99999 for _ in range(100)])
                print("error in {} -- {}".format(self.start, self.end))
            else:
                self.result.extend(elevation)
            self.start += 100
            self.end += 100
            time.sleep(1)

    def query_less_hunder(self):
        latlong = ""
        for i in range(self.start, self.df.shape[0]):
            latlong += (self.df.iloc[i]["latlong"] + "|")
        latlong = latlong[:-1]
        elevation = _ElevationRequest(latlong, self.mode)
        elevation = elevation.get_elevation()
        if len(elevation) == 1 and elevation[0] == -99999:
            self.result.extend([-99999 for _ in range(self.df.shape[0] % 100)])
            print("error in {} -- {}".format(self.start, self.df.shape[0]))
        else:
            self.result.extend(elevation)

    def query_elevation(self) -> DataFrame:
        self.check_columnname()
        self.check_lat_long()
        self.df["latlong"] = self.df["X"].map(str) + "," + self.df["Y"].map(str)
        count = self.df.shape[0]
        if count < 100:
            self.query_less_hunder()
        else:
            self.query_whole_hundred()
            self.query_less_hunder()
        self.df["ELEVATION"] = self.result
        return self.df

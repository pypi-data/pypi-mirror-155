import copy
import traceback

import numpy as np

from yangke.sis.dll_file import init_dbp_api
from yangke.sis.sis_io import get_tag_value
from yangke.web.flaskserver import start_server_app, logger
from yangke.performance.tools.natural_gas import NaturalGas


def deal(args):
    action = args.get("Action").lower()
    result = eval("{}(args)".format(action))
    return result


def naturalgas(args):
    try:
        # 获取前端传入的数据
        compositions = NaturalGas.get_components_name()
        comp = {name: float(args.get(name) or 0) for name in compositions}
        ng = NaturalGas(comp)
        p = float(args.get("P") or 0.101325)
        t = float(args.get("T") or 20)
        t0 = float(args.get("T0") or 20)
        res = {
            "M": ng.mole_weight,
            "Hmg": ng.get_gcv_mass(t0) / 1000,
            "Hvg": ng.get_gcv_voln(20, 20) / 1000,
            "Hcg": ng.get_gcv_mole() / 1000,
            "Hmn": ng.get_ncv_mass(t0) / 1000,
            "Hvn": ng.get_ncv_voln(20, 20) / 1000,
            "Hcn": ng.get_ncv_mole() / 1000,
            "Z": ng.get_z_gas(p, t),
            "D": ng.density
        }
        return res
    except:
        traceback.print_exc()
        logger.debug("error")
        return {"Success": True,
                "Info": "服务正常，请使用Action传入指定的操作！",
                "Example": example}


class PolyCurve:
    def __init__(self, x_list, y_list, deg=1):
        """
        多项式拟合曲线，根据x_list和y_list拟合多项式曲线

        :param x_list: 已知的x点列表
        :param y_list: 一致的y点列表
        :param deg: 多项式阶次
        """
        self.x = np.array(x_list)
        self.y = np.array(y_list)
        self.z = np.polyfit(self.x, self.y, deg)
        self.func = np.poly1d(self.z)

    def get_value(self, x):
        """
        获取曲线上x点上对应的y值

        :param x:
        :return:
        """
        return self.func(x)

    def plot(self, xlim=None, ylim=None):
        import matplotlib.pyplot as plt
        xp = np.linspace(min(self.x), max(self.x))
        _ = plt.plot(self.x, self.y, '.', xp, self.func(xp), '-')
        if xlim is not None:
            plt.xlim()
        if ylim is not None:
            plt.ylim()
        plt.show()


def fit_curve(type="", power=None, flow_gas=None, a=-0.0693, b=1.3388, c=0.4832, d=3.7897):
    if type == "燃气流量vs纯凝功率":
        f_gas = [9.31, 7.5, 5.92, 4.54]
        power = [68.443, 53.504, 39.202, 27.098]
        _ = PolyCurve(x_list=power, y_list=f_gas, deg=3)
        _.plot()
        return _.func
    elif type == "纯凝功率vs燃气流量":
        f_gas = [9.31, 7.5, 5.92, 4.54]
        power = [68.443, 53.504, 39.202, 27.098]
        _ = PolyCurve(x_list=f_gas, y_list=power, deg=3)
        _.plot()


def get_history():
    from datetime import datetime, timedelta
    tags1 = {  # 可读参数，部分也可以写入，但不建议从该程序中写入
        "N1DCS.TCS110RCAOG_B120_01": "调压站天然气流量1",
        "N1DCS.TCS110RCAOG_B120_02": "调压站天然气流量2",
        "N1DCS.TCS110RCAOG_B116_01": "#1电功率",
        "N1DCS.TCS110RCAOG_B116_02": "#2电功率",
        "N1DCS.TCS110RCAOG_B116_03": "#3电功率",

    }
    now = datetime.now()
    p_list1 = []
    p_list2 = []
    p_list3 = []
    p_list4 = []
    api = init_dbp_api()
    his_value = api.get_his_value(tags=list(tags1.keys()), tags_description=list(tags1.values()),
                                  start_time=now - timedelta(days=0, hours=1),
                                  end_time=now - timedelta(days=0, hours=0), time_interval=60)
    his_value = his_value[his_value["#1电功率"] < 1]  # 剔除1号机运行时的数据
    his_value = his_value[his_value["#2电功率"] < 1]  # 剔除2号机运行时的数据
    his_value = his_value[his_value["#3电功率"] > 20]  # 剔除3号机停机时的数据
    his_value = his_value.set_index("DateTime").mean()

    his_value["天然气流量"] = (his_value["调压站天然气流量1"] + his_value["调压站天然气流量2"]) / 2

    data_file2 = []
    for i in range(12):
        api = init_dbp_api()
        his_value = api.get_his_value(tags=list(tags1.keys()), tags_description=list(tags1.values()),
                                      start_time=now - timedelta(days=30 * (i + 1), hours=0),
                                      end_time=now - timedelta(days=30 * i, hours=0), time_interval=60)
        his_value = his_value.set_index("DateTime").rolling(window=10).mean()
        his_value.dropna(how="any", inplace=True)
        # his_value_bak = copy.deepcopy(his_value)
        his_value.drop(his_value.tail(10).index, inplace=True)  # 删掉最后十行数据
        his_value = drop_revulsion(his_value, "#1电功率", 10, 10)  # 删除10分钟功率变化超过10MW的数据行
        his_value["大气压力"] = his_value["大气压力"] / 10  # 单位转换
        his_value["环境湿度"] = his_value["环境湿度"] / 100  # 单位转换

        his_value.to_csv(f"origin_{i}.csv")  # his_value为原始数据，不删除任何时间的数据


def start_server():
    # run()  # 启动定时执行
    heat_supply({})
    start_server_app(deal=deal, port=5000,
                     example_url=example)


if __name__ == "__main__":
    example = "http://127.0.0.1:5000/?Action=NaturalGas&CH4=0.98&N2=0.02&T=15&P=3.8&T0=20"
    start_server()

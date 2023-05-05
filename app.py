from flask import Flask, render_template
# 这些代码导入用于数据分析、可视化和图像编码/解码的必要模块。
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
from flask import Flask, render_template, jsonify

# 这一行创建了一个名为 app 的 Flask 实例。
app = Flask(__name__)
# 这段代码创建了一个新的路由 /reload_charts，它以 JSON 格式返回图表数据。它使用 generate_charts() 函数生成图表数据。
@app.route('/reload_charts', methods=['GET'])
def reload_charts():
    # 这段代码是 Flask 应用程序中的一个路由，它是一个 GET 请求，接受并返回 JSON 数据。在请求 "/reload_charts" 路由时，
    # 会调用 generate_charts() 函数，生成一系列图表，并将它们存储在一个名为 charts_data 的列表中。
    # 最后，将 charts_data 列表作为 JSON 对象返回给客户端。
    charts_data = generate_charts()
    # 具体而言，jsonify() 函数将 Python 对象转换为 JSON 对象。
    # 在这个例子中，{"charts": charts_data} 是一个包含一个名为 charts 的列表的字典，它将在浏览器中作为 JSON 格式返回。
    # 由于浏览器不支持 Python 对象，因此需要将它们转换为 JSON 对象，这样浏览器才能正确地显示它们。
    return jsonify({"charts": charts_data})
# 这一行代码定义了一个名为 generate_charts() 的函数。该函数生成图表并将其作为列表返回。
def generate_charts():
    # 读取数据
    # 这一行代码将自行车共享数据从 hour.csv 文件读取到 pandas DataFrame 中。
    data = pd.read_csv('hour.csv')
    # 这一行代码初始化了一个名为 charts 的空列表，以及一个名为 chart_names 的列表，其中包含要生成的图表名称。
    charts = []
    chart_names = [
        'hourly_usage_frequency', 'usage_by_season', 'usage_by_weather', 'usage_vs_temperature', 'usage_vs_humidity',
        'usage_workingday_vs_holiday', 'usage_by_year', 'user_type_usage'
    ]

    # 这一行代码创建一个新的 matplotlib 图形，大小为 12 英寸宽，6 英寸高。
    for chart_name in chart_names:
        plt.figure(figsize=(12, 6))
        # 这一行代码生成了小时单车使用频率的计数图，并设置了标题、x轴标签和y轴标签。
        if chart_name == 'hourly_usage_frequency':
            # 这两行代码的格式和用法都是Seaborn库提供的图表绘制函数，可以用于在数据可视化中生成各种类型的图表。
            # 需要导入Seaborn库并对数据进行处理，然后使用各种绘图函数来创建和自定义图表，最后可以使用matplotlib库保存图表并显示。

            # 绘制的是自行车使用次数的条形计数图，其中data参数是要用于绘图的数据集，x参数是指定数据中哪一列作为横坐标，这里是小时数（hr）。
            # sns.countplot(data=data, x='hr')
            # 绘制的是自行车使用次数随时间（小时）的变化曲线，其中data参数和x参数与第一行相同，y参数指定数据中哪一列作为纵坐标，
            # 这里是自行车使用的总数（cnt）。ci参数是控制置信区间的范围，这里设置为None表示不显示置信区间。
            sns.lineplot(data=data, x='hr', y='cnt', ci=None)
            plt.title('Hourly Usage Frequency')
            plt.xlabel('Hour of Day')
            plt.ylabel('Usage Count')
        #     这一行代码生成了按季节分类的单车使用量箱形图，并设置了标题、x轴标签和y轴标签
        elif chart_name == 'usage_by_season':
            # sns.boxplot(data=data, x='season', y='cnt')
            sns.barplot(data=data, x='season', y='cnt')
            plt.title('Bike Usage by Season')
            plt.xlabel('Season')
            plt.ylabel('Bike Usage')
        # 这一行代码生成了按天气状况分类的单车使用量箱形图，并设置了标题、x轴标签和y轴标签。
        elif chart_name == 'usage_by_weather':
            # sns.boxplot(data=data, x='weathersit', y='cnt')
            sns.countplot(data=data, x='weathersit')
            plt.title('Bike Usage by Weather Condition')
            plt.xlabel('Weather Condition')
            plt.ylabel('Bike Usage')
        # 这一行代码生成了温度和单车使用量之间的散点图，并设置了标题、x轴标签和y轴标签。
        elif chart_name == 'usage_vs_temperature':
            sns.scatterplot(data=data, x='temp', y='cnt')
            plt.title('Bike Usage vs Temperature')
            plt.xlabel('Temperature')
            plt.ylabel('Bike Usage')
        #     这一行代码生成了湿度和单车使用量之间的散点图，并设置了标题、x轴标签和y轴标签。
        elif chart_name == 'usage_vs_humidity':
            sns.scatterplot(data=data, x='hum', y='cnt')
            plt.title('Bike Usage vs Humidity')
            plt.xlabel('Humidity')
            plt.ylabel('Bike Usage')
        #这一行代码生成了工作日和假日单车使用情况的箱形图，并设置了标题、x轴标签和y轴标签
        elif chart_name == 'usage_workingday_vs_holiday':
            sns.boxplot(data=data, x='workingday', y='cnt')
            # sns.barplot(data=data, x='workingday', y='cnt')
            plt.title('Bike Usage on Working Days vs Holidays')
            plt.xlabel('Working Day (1) / Holiday (0)')
            plt.ylabel('Bike Usage')
        #     这一行代码生成了按年份分类的单车使用量箱形图，并设置了标题、x轴标签和y轴标签。
        elif chart_name == 'usage_by_year':
            # sns.boxplot(data=data, x='yr', y='cnt')
            sns.lineplot(data=data, x='dteday', y='cnt', ci=None)
            plt.title('Bike Usage by Year')
            plt.xlabel('Year')
            plt.ylabel('Bike Usage')
        # 这一行代码生成了按用户类型分类的单车使用量条形图，并设置了标题、x轴标签和y轴标签。
        elif chart_name == 'user_type_usage':
            sns.barplot(data=data, x=['Casual', 'Registered'], y=[data['casual'].sum(), data['registered'].sum()])
            plt.title('Bike Usage by User Type')
            plt.xlabel('User Type')
            plt.ylabel('Bike Usage')
        #     #     这些代码将生成的图形编码为 PNG 格式，存储在内存中，并将其添加到 charts 列表中。
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        base64_image = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        charts.append({'name': chart_name, 'data': base64_image})
    #     这一行代码返回生成的图表列表。
    return charts
# 这些代码定义了 / 路由，它将渲染名为 index.html 的模板，该模板将显示生成的图表。
@app.route('/')
def index():
    charts = generate_charts()
    return render_template('index.html', charts=charts)
# 这一行代码在运行该脚本时启动应用程序。 debug = True 表示启用调试模式。
if __name__ == '__main__':
    app.run(debug=True)

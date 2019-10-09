#import sqlite3
from string import Template
import ScrapingTool.Models.mongo_read_write as mongo

class CreateChart:
    def __init__(self, req_id, Product):
        self.template=''
        self.results = []
        ##SQLite DB Option
        #self.conn = sqlite3.connect('db.sqlite3')
        #self.cursor = ''


    def Create_Column_Chart(self, req_id, Product):
        print('running GChart Col ' + Product)

        ##SQLite DB Option
        # query = "SELECT Date, sum(NrOfIssues) from Issues_Count_By_Keyword WHERE Product='{}' GROUP By Date ORDER BY Date ASC".format(Product)
        
        # self.cursor = self.conn.execute(query)

        # for row in self.cursor:
        #     self.results.append({'Date': row[0], 'NrOfIssues': row[1]})

        ##MongoDB Option
        collection_name = 'Exported_Data' + str(req_id)
        self.results = mongo.Get_Chart_Data(collection_name,'Date')
        print(self.results)

        ##Common For Both SQLite and Mongo
        self.template = '''
        {% extends 'base.html' %}

        {% block content %}

        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
                var data = google.visualization.arrayToDataTable([
                    ["Date", "Comments"],
                    $res
                ]);
                
                var options = {
                    title: "Number of Issues By Date",
                    legend: { position: "right" },
                    bar: {groupWidth: "75%"},
                    hAxis: {title: "Date", groupByRowLabel: true, slantedText:true, slantedTextAngle:90 },
                    vAxis: {title: "Nr of Issues"}
                };

                var chart = new google.visualization.ColumnChart(document.getElementById("columnchart_values"));
                chart.draw(data, options);
            }
        </script>'''

        with open('ScrapingTool\\templates\\dashboard.html', 'w') as html:
            data = ','.join(['["{Date}", {NrOfIssues}]'.format(**r) for r in self.results])
            #html.write(Template(self.template).substitute(res=data))
            self.template = Template(self.template).substitute(res=data)

    def Create_Pie_Chart(self, req_id, Product):
        print('running GChart Pie ' + Product)

        ##SQLite DB Option
        # self.results=[]
        # query = "SELECT Category, sum(NrOfIssues) from Issues_Count_By_Keyword WHERE Product='{}' GROUP By Category ORDER BY sum(NrOfIssues) DESC".format(Product)
        
        # self.cursor = self.conn.execute(query)
        
        # for row in self.cursor:
        #     self.results.append({'Category': row[0], 'NrOfIssues': row[1]})

        ##MongoDB Option
        collection_name = 'Exported_Data' + str(req_id)
        self.results = mongo.Get_Chart_Data(collection_name,'Category')
        print(self.results)
        
        ##Common For Both SQLite and Mongo
        self.template = self.template + '''
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
                var data = google.visualization.arrayToDataTable([
                    ["Category", "Comments"],
                    $res
                ]);
                
                var options = {
                    title: "Number of Issues By Category",
                    legend: { position: "right" },
                };

                var chart = new google.visualization.PieChart(document.getElementById("piechart_values"));
                chart.draw(data, options);
            }
        </script>'''
        html_template = '''
        <body class="dashboard-contents">
            <div id="content-container" class="container-fluid dashboard-card">
                <div class="card text-center">
                    <form id="dashboard-form" method="POST">
                        <div class="card-header text-white">
                            <h2 align="center"> Dashboard </h2>
                        </div>
                        <div id="wrapper">
                            <h3 align="center"><b>Product: $prod </b></h3>
                            <div  id="prod-dropdown" align="right">
                                <label align="right">Select Product:</label>
                                <select name="product" id="product-dropdown" class="product-dropdown">
                                    {% for product in product_list %}
                                    <option type = "option" name="product" value="{{product}}">{{product}}</option><br>
                                    {%endfor %}
                                </select>
                                <button type="submit" id="product-button" name="gen_graph" value='submit'>Generate Graph</button>
                            </div>                                
                            <div id="columnchart_values" align="center" style="width: 48%; height: 600px"></div>
                            <div id="piechart_values" align="center" style="width: 48%; height: 600px"></div>
                        </div>
                    </form>
                </div>
            </div>
        </body>
        {% endblock content %}'''
        
        with open('ScrapingTool\\templates\\dashboard.html', 'w') as html:
            data = ','.join(['["{Category}", {NrOfIssues}]'.format(**r) for r in self.results])
            #html.write(Template(self.template).substitute(res=data))
            self.template = Template(self.template).substitute(res=data)
            html_template = Template(html_template).substitute(prod=Product)
            self.template = self.template + html_template 
            html.write(self.template)
            

import sqlite3
from string import Template

class CreateChart:
    def __init__(self):
        self.template=''
        self.conn = sqlite3.connect('db.sqlite3')
        self.cursor = ''
        self.results = []


    def Create_Column_Chart(self):
        self.cursor = self.conn.execute("SELECT Date, sum(NrOfIssues) from Issues_Count_By_Keyword GROUP By Date ORDER BY Date ASC")

        for row in self.cursor:
            self.results.append({'Date': row[0], 'NrOfIssues': row[1]})
        
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
                    hAxis: {title: "Date" , direction:-1, slantedText:true, slantedTextAngle:90 },
                    vAxis: {title: "Nr of Issues"}
                };

                var chart = new google.visualization.ColumnChart(document.getElementById("columnchart_values"));
                chart.draw(data, options);
        }
        </script>'''

        with open('chart.html', 'w') as html:
            data = ','.join(['["{Date}", {NrOfIssues}]'.format(**r) for r in self.results])
            #html.write(Template(self.template).substitute(res=data))
            self.template = Template(self.template).substitute(res=data)

    def Create_Pie_Chart(self):
        self.results=[]
        self.cursor = self.conn.execute("SELECT Category, sum(NrOfIssues) from Issues_Count_By_Keyword GROUP By Category ORDER BY sum(NrOfIssues) DESC")
        
        for row in self.cursor:
            self.results.append({'Category': row[0], 'NrOfIssues': row[1]})
        print(self.results)
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
            <div id="content-container" class="container">
                <form id="dashboard-form" method="POST">
                    <div class="content-container">
                        <div name="dashboard-container" class="dashboard-container">
                          <div id="wrapper">
                                <h1 align="center">Dashboard</h1>
                                <div id="columnchart_values" align="center" style="width: 900px; height: 600px"></div>
                                <div id="piechart_values" align="center" style="width: 900px; height: 600px"></div>
                          </div>
                        </div>
                    </div>
                </form>
            </div>
        </body>
        {% endblock content %}'''
        
        with open('chart.html', 'w') as html:
            data = ','.join(['["{Category}", {NrOfIssues}]'.format(**r) for r in self.results])
            #html.write(Template(self.template).substitute(res=data))
            self.template = Template(self.template).substitute(res=data)
            self.template = self.template + html_template 
            html.write(self.template)
            
x = CreateChart()
x.Create_Column_Chart()
x.Create_Pie_Chart()

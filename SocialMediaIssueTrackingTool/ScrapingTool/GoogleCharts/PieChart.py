import sqlite3
from string import Template

def Create_Pie_Chart():
  conn = sqlite3.connect('db.sqlite3')
  cursor = conn.execute("SELECT Category, sum(NrOfIssues) from Issues_Count_By_Keyword GROUP By Category ORDER BY sum(NrOfIssues) DESC")

  results = []

  for row in cursor:
      results.append({'Category': row[0], 'NrOfIssues': row[1]})

  template = '''
  <html>
  <head>
  <script type="text/javascript"
  src=\'https://www.google.com/jsapi?autoload={
      "modules":[{
        "name":"visualization",
        "version":"1",
        "packages":["corechart"]
      }]
    }\'></script>

  <script type="text/javascript">
  google.setOnLoadCallback(drawPieChart);

  function drawPieChart() {
      var PieData = google.visualization.arrayToDataTable([
        ["Category", "NrOfIssues"],
      $res
      ]);

      var options = {
        title: "Number of Comments By Tags",
        curveType: "function",
        legend: { position: "right" }
      };

      var chart = new google.visualization.PieChart(document.getElementById('Pie_chart'));

      chart.draw(PieData, options);

  }

  </script>
  </head>
  <body>

  <div id="Pie_chart" style="width: 450px; height: 250px"></div>

  </body>
  </html>'''

  with open('ScrapingTool\\templates\\piechart.html', 'w') as html:
      PieData = ','.join(['["{Category}", {NrOfIssues}]'.format(**r) for r in results])
      html.write(Template(template).substitute(res=PieData))

def Create_Column_Chart():
  conn = sqlite3.connect('db.sqlite3')
  cursor = conn.execute("SELECT Date, sum(NrOfIssues) from Issues_Count_By_Keyword GROUP By Date ORDER BY sum(NrOfIssues) DESC")

  results = []

  for row in cursor:
      results.append({'Date': row[0], 'NrOfIssues': row[1]})

  template = '''
  <html>
  <head>
  <script type="text/javascript"
  src=\'https://www.google.com/jsapi?autoload={
      "modules":[{
        "name":"visualization",
        "version":"1",
        "packages":["corechart"]
      }]
    }\'></script>

  <script type="text/javascript">
  google.setOnLoadCallback(drawPieChart);

  function drawPieChart() {
      var ColData = google.visualization.arrayToDataTable([
        ["Date", "NrOfIssues"],
      $res
      ]);

      var options = {
        title: "Number of Comments By Tags",
        curveType: "function",
        legend: { position: "right" }
      };

      var chart = new google.visualization.ColumnChart(document.getElementById('Col_chart'));

      chart.draw(ColData, options);

  }

  </script>
  </head>
  <body>

  <div id="Col_chart" style="width: 450px; height: 250px"></div>

  </body>
  </html>'''

  with open('ScrapingTool\\templates\\colchart.html', 'w') as html:
      ColData = ','.join(['["{Date}", {NrOfIssues}]'.format(**r) for r in results])
      html.write(Template(template).substitute(res=ColData))

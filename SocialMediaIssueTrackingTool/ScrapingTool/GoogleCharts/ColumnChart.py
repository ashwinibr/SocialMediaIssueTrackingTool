import sqlite3
from string import Template

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

      var chart = new google.visualization.PieChart(document.getElementById('Col_chart'));

      chart.draw(ColData, options);

  }

  </script>
  </head>
  <body>

  <div id="Col_chart" style="width: 450px; height: 250px"></div>

  </body>
  </html>'''

  with open('chart.html', 'w') as html:
      ColData = ','.join(['["{Date}", {NrOfIssues}]'.format(**r) for r in results])
      html.write(Template(template).substitute(res=ColData))

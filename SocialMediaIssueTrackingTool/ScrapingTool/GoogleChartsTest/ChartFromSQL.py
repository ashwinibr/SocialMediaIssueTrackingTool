

import sqlite3
from string import Template

conn = sqlite3.connect('Charts.sqlite3')
cursor = conn.execute("SELECT IssueTags, NrComments from Issues")

results = []

for row in cursor:
    results.append({'IssueTags': row[0], 'NrComments': row[1]})
    print("IssueTags :", row[0])
    print("NrComments :", row[1])

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
google.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable([
      ["IssueTags", "NrComments"],
     $res
    ]);

    var options = {
      title: "Number of Comments by Users By Tags",
      curveType: "function",
      legend: { position: "right" }
    };

    var chart = new google.visualization.PieChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}
</script>
</head>
<body>

<div id="curve_chart" style="width: 900px; height: 500px"></div>
</body>
</html>'''

with open('chart.html', 'w') as html:
    data = ','.join(['["{IssueTags}", {NrComments}]'.format(**r) for r in results])
    html.write(Template(template).substitute(res=data))


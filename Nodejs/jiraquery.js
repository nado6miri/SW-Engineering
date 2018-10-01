var request = require("request");

function jquery_jira(res){
    var options = { method: 'POST',
    url: 'http://hlm.lge.com/issue/rest/api/2/search/',
    headers:
     { 'Postman-Token': '5bf2adbb-3708-4304-8710-bfc82a6de5d9',
       'Cache-Control': 'no-cache',
       Authorization: 'Basic c3VuZ2Jpbi5uYTpTdW5nYmluQDE4MDg=',
       Accept: 'application/json, text/javascript, */*;q=0.01',
       'content-Type': 'application/json' },
    body: '{\r\n\t "jql" : "filter=Initiative_webOS4.5_Initial_Dev" \r\n\t,"maxResults" : 1000\r\n    , "startAt": 0\r\n    ,"fields" : ["summary", "key", "assignee", "due", "status", "labels"]\r\n};' };

    request(options, function (error, response, body) {
      if (error) throw new Error(error);
      //console.log(body);
      res.header("Access-Control-Allow-Origin", "*");
      res.header("Access-Control-Allow-Headers", "X-Requested-With");
      res.send(body);
    });
}

const express = require('express');
const app = express();

app.get('/', (req, res) => {
  jquery_jira(res);
});

app.get('/initiative', (req, res) => {
  jquery_jira(res);
});

app.listen(3000, '127.0.0.1', () => {
  console.log('Example app listening on port 3000!');
});

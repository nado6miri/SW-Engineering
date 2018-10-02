var request = require("request");
var http = require('http');
var path = require('path');
var fs = require('fs');
var url = require('url');
const express = require('express');
const app = express();

var mime = {
  html: 'text/html',
  txt: 'text/plain',
  css: 'text/css',
  gif: 'image/gif',
  jpg: 'image/jpeg',
  png: 'image/png',
  svg: 'image/svg+xml',
  js: 'application/javascript'
};

function jquery_jira(res){
    var options = { method: 'POST',
    url: 'http://hlm.lge.com/issue/rest/api/2/search/',
    headers:{ 
      'Postman-Token': '5bf2adbb-3708-4304-8710-bfc82a6de5d9',
       'Cache-Control': 'no-cache',
       Authorization: 'Basic c3VuZ2Jpbi5uYTpTdW5nYmluQDE4MDg=',
       Accept: 'application/json, text/javascript, */*;q=0.01',
       'content-Type': 'application/json' },
       body: '{\r\n\t "jql" : "filter=Initiative_webOS4.5_Initial_Dev" \r\n\t,"maxResults" : 1000\r\n    , "startAt": 0\r\n    ,"fields" : ["summary", "key", "assignee", "due", "status", "labels"]\r\n};' 
      };

    request(options, function (error, response, body) {
      if (error) throw new Error(error);
      //console.log(body);
      res.header("Access-Control-Allow-Origin", "*");
      res.header("Access-Control-Allow-Headers", "X-Requested-With");
      //transfer text msg to browser
      res.send(body);
    });
}

app.get('/', (req, res) => {
  jquery_jira(res);
});

app.get('/initiative', (req, res) => {
  jquery_jira(res);
});

app.get('/socketchat', (req, res) => {
  res.writeHead(200,{'Content-Type':'text/html'}); // header 설정
  fs.readFile(__dirname+'/template/'+ 'chat.html', (err, data) => { // 파일 읽는 메소드
    if (err) {
      return console.error(err); // 에러 발생시 에러 기록하고 종료
    }
    res.end(data, 'utf-8'); // 브라우저로 전송  
  });

  jquery_jira(res);
});

app.get('/img', (req, res) => {
    //use the url to parse the requested url and get the image name
    var query = url.parse(req.url,true).query;
    var pic = query.image;
 
    //var query = "/home/sdet/sdetshare/workspace/SW-Engineering/Nodejs/img/"; //url.parse(req.url,true).query;
    //var pic = "a.jpg"; //query.image;
    console.log("pic=", pic);
    console.log("query=", query);

    //read the image using fs and send the image content back in the response
    fs.readFile(__dirname + '/img/' + pic, function (err, content) {
        if (err) {
            res.writeHead(400, {'Content-type':'text/html'})
            console.log(err);
            res.end("No such image");    
        } else {
            //specify the content type in the response will be an image
            res.writeHead(200,{'Content-type':'image/jpg'});
            res.end(content);
        }
    });
});


/*
app.listen(3000, '127.0.0.1', () => {
  console.log('Example app listening on port 3000!');
});
*/

app.use(express.static(path.join(__dirname, 'public')));

var httpServer = http.createServer(app).listen(3000, function(req,res){
  console.log('Socket IO server has been started');
});

// upgrade http server to socket.io server
var io = require('socket.io').listen(httpServer);

// http://bcho.tistory.com/899 
io.sockets.on('connection',function(socket)
{
   socket.emit('toclient',{msg:'Welcome !'});
   socket.on('fromclient',function(data){
       socket.broadcast.emit('toclient',data); // 자신을 제외하고 다른 클라이언트에게 보냄
       socket.emit('toclient',data); // 해당 클라이언트에게만 보냄. 
       console.log('Message from client :'+data.msg);
   });
});







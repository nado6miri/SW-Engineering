var request = require("request");
var http = require('http');
var path = require('path');
var fs = require('fs');
var url = require('url');
const express = require('express');
const app = express();

var XMLHttpRequest = require('xmlhttprequest-ssl').XMLHttpRequest;

// Express에서 정적 파일 제공 방법
// http://expressjs.com/ko/starter/static-files.html
// app.use(express.static('public')); // public folder의 file 제공
// http://localhost:3000/images/kitten.jpg
// http://localhost:3000/css/style.css

// app.use('/static', express.static('public')); // 가상의 /static url로 제공
// http://localhost:3000/static/images/kitten.jpg
// http://localhost:3000/static/css/style.css

// important : express.static 함수에 제공되는 경로는 node 프로세스가 실행되는 디렉토리에 대해 상대적입니다. 
// Express 앱을 다른 디렉토리에서 실행하는 경우에는 다음과 같이 제공하기 원하는 디렉토리의 절대 경로를 사용하는 것이 더 안전합니다.
// app.use('/static', express.static(__dirname + '/public'));

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
            res.writeHead(400, {'Content-type':'text/html; charset=utf-8'})
            console.log(err);
            res.end("No such image");    
        } else {
            //specify the content type in the response will be an image
            res.writeHead(200,{'Content-type':'image/jpg; charset=utf-8'});
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
io.sockets.on('connection',function(socket){
   socket.emit('toclient',{msg:'Welcome !'});
   socket.on('fromclient',function(data){
       socket.broadcast.emit('toclient',data); // 자신을 제외하고 다른 클라이언트에게 보냄
       socket.emit('toclient',data); // 해당 클라이언트에게만 보냄. 
       console.log('Message from client :'+data.msg);
   });
});



/*


//===========================================================================================

function Check_Session_Login()
{
	var searchURL = "http://10.164.2.76/rest/auth/1/session";

	var xhttp = new XMLHttpRequest();
	
	xhttp.onreadystatechange = function()
	{
		if (xhttp.readyState === 4)
		{
			if (xhttp.status === 200)
			{
				var resultJSON = JSON.parse(xhttp.responseText);
                console.log("====> Found SVLJIRA log-in id : "+resultJSON.name);
				//CCC_Gathering_Status_Init();
				setTimeout(CCC_Gathering, 1000);
			}
            else
            {
                console.log("Not log-in at SVLJIRA --> Need log-in !");
                setTimeout(Post_Login_Session,1000);
            }			
		}
        else
        {
            console.log("Check_Session_Login --> readyState : "+xhttp.readyState);
        }
	};
	xhttp.open("GET", searchURL, true, id, pwd);	
	xhttp.withCredentials = true;
	xhttp.setRequestHeader("Content-Type","application/json; charset=utf-8");
	xhttp.send();
}
 
function Post_Login_Session()
{
	var url = "http://10.164.2.76/rest/auth/1/session";
	
	var xhttp = new XMLHttpRequest();
	
	xhttp.onreadystatechange = function()
	{
		if (xhttp.readyState === 4)
		{
			if (xhttp.status === 200)
			{
				var resultJSON = JSON.parse(xhttp.responseText);
                console.log("====> login success at Jira2 !!");
			    console.log("====> Found SVLJIRA log-in id : "+resultJSON.name);
           
				setTimeout(Check_Session_Login, 1000);
            }
            else
            {
				setTimeout(Post_Login_Session,1000);
      }  
            console.log("Post_Login_Session failed -->status : "+xhttp.status);
      }  
        }
	  }  
	}
	  }  
	else
	  }  
	{
	  }  
		console.log("Post_Login_Session --> readyState : "+xhttp.readyState)
	  }  
	}
	  }  
};
	  }  
xhttp.open("POST", url, true, id, pwd);
	xhttp.withCredentials = true;
	xhttp.setRequestHeader("Content-Type", "application/json; charset=utf-8");
	xhttp.send(JSON.stringify(authObj));
}


function postJSONResult_InstallMONTHCCCReview(param,searchURL,index)
{
	var xhttp = new XMLHttpRequest();
	
    xhttp.onreadystatechange = function()
    {
         if (xhttp.readyState === 4)
         {
            if (xhttp.status === 200)
            {
				var resultJSON = JSON.parse(xhttp.responseText);
				console.log(resultJSON.total);
				var json = JSON.stringify(resultJSON);
				fse.outputFileSync("./"+MONTH_CCC_FILE_ARRAY[index],json, 'utf-8', function(e){
					if(e){
						console.log(e);
					}else{
						console.log("Download is done!");	
					}
				});
				MONTH_CCC_GATHERING_STATUS[index] = 1;
                console.log("MONTH CCC gathering ok ("+index+")");
            }
            else
            {
                (function f(x){
                setTimeout(function (){postJSONResult_InstallMONTHCCCReview(param,searchURL,index);},1000);
                }(index));
            }
        }
    };
	xhttp.open("POST", searchURL, true, id, pwd);
    xhttp.withCredentials = true;
    xhttp.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    xhttp.send(JSON.stringify(param));
} 


function Request_MonthCCCData_toSVL()
{
	var param_MonthCCC = new Array();
	console.log("Month CCC Request Number = %d", MONTH_CCC_QUERY.length);
	for(var i=0;i<MONTH_CCC_QUERY.length;i++)
	{
		param_MonthCCC[i] = {"jql": MONTH_CCC_QUERY[i],"maxResults":1000,"startAt":0, "fields":["status"]};
		(function f(x){
			setTimeout(function (){postJSONResult_InstallMONTHCCCReview(param_MonthCCC[x],CCCSearchURL,x);},x*1000);
		}(i));
	}
}



function Timer_Setting()
{
		var x = {
					hours: 0,
					minutes: 0,
					seconds: 0
				};

		var dtAlarm = new Date();
		dtAlarm.setHours(x.hours);
		dtAlarm.setMinutes(x.minutes);
		dtAlarm.setSeconds(x.seconds);
		var dtNow = new Date();

		if (dtAlarm - dtNow > 0) {
			console.log('Later today, no changes needed!');
		}
		else {
			console.log('Tomorrow, changing date to tomorrow');
			dtAlarm.setDate(dtAlarm.getDate() + 1);
		}

		var diff = dtAlarm - new Date();
	
		setTimeout(Request_DataAcq_Trigger, diff);
}

function Request_DataAcq_Trigger()
{
		console.log("Request Data#1!!");
		Check_Session_Login();
		setInterval(Check_Session_Login, 86400000); //24 hour 마다 Data Gathering
}

function CCC_Gathering()
{
	
	CCCSearchURL = "http://10.164.2.76/rest/api/2/search";
	
	console.log("CCC_Gathering~Start");
	
	CCC_Gathering_Status_Init();
	RequesttoSVL_Trigger_Int();
	
	Generate_Query();
	CCC_Gathering_Status_Check();
}

var port = 27024;

var id = "Hongcheol Eom";
var pwd = "!Min0712486!";
   authObj = {
	"password" : pwd,
	"username" : id
};


function Request_MonthlyDPTERR_toSVL(startIndex, endIndex)
{
	var param_DPTERR = new Array(DPT_MONTHLY_ERR_ARRAY.length);
	console.log("Department ERR Request Number[%d] = %d", startIndex,(endIndex-startIndex)*DPT_MONTHLY_ERR_ARRAY[0].length);
	for(var i=startIndex; i<endIndex; i++)
	{
		param_DPTERR[i] = new Array(DPT_MONTHLY_ERR_ARRAY[i].length);
		
		for(var j=0; j<DPT_MONTHLY_ERR_ARRAY[i].length; j++)
		{
			param_DPTERR[i][j] =  {"jql": MonthlyDPTERRQueryArray[i][j],"maxResults":1000,"startAt":0, "fields":["status"]};
			(function f(x,y){
					setTimeout(function (){postJSONResult_InstallDPTMonthlyERRReview(param_DPTERR[x][y],CCCSearchURL,x, y);},y*1000);
			}(i,j));
		}
	}	
}



function postJSONResult_InstallDPTMonthlyERRReview(param, searchURL, index1, index2)
{
	var xhttp = new XMLHttpRequest();
	
    xhttp.onreadystatechange = function()
    {
        if (xhttp.readyState === 4)
        {
          if (xhttp.status === 200)
            {
                var resultJSON = JSON.parse(xhttp.responseText);
				console.log(resultJSON.total);
				var json = JSON.stringify(resultJSON);
				fse.outputFileSync("./"+DPT_MONTHLY_ERR_ARRAY[index1][index2],json, 'utf-8', function(e){
					if(e){
						console.log(e);
					}else{
						console.log("Download is done!");
					}
				});
				DPT_MONTHLY_ERR_GATHERING_STATUS[index1][index2]=1;
				console.log("Monthly DPT ERR gathering ok (["+index1+"]["+index2+"])");
			}
			else
            {
                (function f(x, y){
                    setTimeout(function (){postJSONResult_InstallDPTMonthlyERRReview(param,searchURL,index1,index2);},1000);
                }(index1, index2));
            }
        }
    };
    xhttp.open("POST", searchURL, true, id, pwd);
    xhttp.withCredentials = true;
    xhttp.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    xhttp.send(JSON.stringify(param));
} 
*/
var http = require('http'),
  request = require('request');

var opts = {
  url: 'https://api.producthunt.com/v1/posts',
  auth: {
    bearer: process.env.PH_API_ACCESS_TOKEN
  },
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Accept-Encoding': ''
  }
};

http.createServer(function (req, res) {

  if (req.url === '/v1/posts') {
    request.get(opts)
      .pipe(res);
  } else {
    res.writeHead(501);
    res.end('Not Implemented');
  }
}).listen(process.env.PORT || 3000);

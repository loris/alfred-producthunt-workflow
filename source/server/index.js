/* global process */
var http = require('http'),
  request = require('request');

var cachedPosts;

var fetchPosts = function (callback) {
  var opts = {
    url: 'https://api.producthunt.com/v1/posts',
    auth: {
      bearer: process.env.PH_API_ACCESS_TOKEN
    },
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  };

  request.get(opts, function (err, resp, body) {
    callback(err, body);
  });
};

(function loop() {
  fetchPosts(function (err, posts) {
    cachedPosts = posts;
    setTimeout(function () {
      loop();
    }, 60*1000);
  });
})();

http.createServer(function (req, res) {
  if (req.url === '/v1/posts') {
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(cachedPosts);
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
}).listen(process.env.PORT || 3000);


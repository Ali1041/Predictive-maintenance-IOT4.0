var http = require('http');
const axios = require('axios');


http.createServer(function(req,res) {
    res.writeHead(200,{'Content-Type': 'text/plain'});
    console.log('Running Zetta server')
    let data = ''
    req.on('data', chunk => {
        data = JSON.parse(chunk)
        console.log(data)
        axios
        .post('http://localhost:3000', {
          data: data,
        })
        .then(res => {
          console.log(`statusCode: ${res.status}`);
          console.log(res);
        })
        .catch(error => {
          console.error(error);
        });
      });
      req.on('end', () => {
        // end of data
        
        res.end('Data Sent Successfully!!!');
      });
    
}).listen(3000);
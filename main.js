var express = require('express');
var bodyParser = require("body-parser");
var app = express();


app.set('view engine', 'ejs');

app.get('/', function(req, res) {
    res.render('coordinates');
});

app.use(express.static('public'));

app.listen(8080);
console.log('Lets get rollin!');


var dataPath = undefined;
var location = "";

var auto_suggest = undefined;

if (process.argv[2]) {
    dataPath = process.argv[2].trim();
    console.log("Data location: " + dataPath);
    if (dataPath.charAt(0) != '/') {
        console.error("Only absolute path for data path allowed!");
        process.exit(1);
    }
} else {
    console.error("Please provide a data path as first argument!");
    process.exit(1);
}

if (process.argv[3]) {
    location = process.argv[3].trim();
    console.log("Script location: " + location + "demo.py");
    if (location.charAt(0) != '/') {
        console.error("Only absolute path for script path allowed!");
        process.exit(1);
    }
}

var spawn = require('child_process').spawn,
    python    = spawn('/usr/bin/python2.7', [location + 'demo.py', dataPath]);
var fs = require('fs');
var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

fs.unlink(__dirname + '/public/spreading_activation_result.json', function(err) {
    if (err && err.errno != 34) console.log(err);
});

fs.unlink(__dirname + '/public/network_distance.json', function(err) {
    if (err && err.errno != 34) console.log(err);
});

app.get('/data.json', function(req, res){
    res.send(auto_suggest);
});

app.use('/', express.static(__dirname + '/public'));
var status = false;
var requestedSA = false;

io.on('connection', function(socket){
    socket.on('start spreading activation', function(company){
        console.log("request for spreading activation: " + company);
        requestedSA = true;
        status = false;
        io.emit("status", status);
        python.stdin.write("spreading_activation('" + company +"',8, 0.0001,True)" + "\n");
    });
    socket.on('start network distance', function(companies){
        companies = companies.split("\n");
        console.log("request for network distance: " + companies);
        status = false;
        io.emit("status", status);
        python.stdin.write("distance_networks_wrapper('" + companies[0] +"', '" + companies[1] +"', 8, 0.0001,3,10)" + "\n");
    });
    socket.on('disconnect', function () {
        oldFileND = "";
        oldFileSA = "";

        fs.unlink(__dirname + '/public/spreading_activation_result.json', function(err) {
            if (err && err.errno != 34) console.log(err);
        });

        fs.unlink(__dirname + '/public/network_distance.json', function(err) {
            if (err && err.errno != 34) console.log(err);
        });
    });
    io.emit("status", status);
});

http.listen(3000, function(){
    console.log('listening on *:3000');
});

var oldFileSA = "";
var oldFileND = "";

python.stdout.on('readable', function() {
    var chunk;
    while (null !== (chunk = python.stdout.read())) {
        var message = String(chunk);
        console.log("OUTPUT:\n" + message);
        io.emit("chat message", message);
        if (message.indexOf("Waiting for messages") != -1) {
            prepareAuto();
            status = true;
            io.emit("status", status);
        }
    }
    fs.readFile('public/spreading_activation_result.json', function (err, data) {
        if (!requestedSA) {
            return;
        }
        if (err) {
            if (err.errno != 34) console.log(err); // ignore if file not found
            return;
        }
        if (data.toString() != oldFileSA.toString()) {
            try {
                array = JSON.parse(data);
                oldFileSA = data;
            } catch (e) {
                return;
            }
            io.emit("data spreading activation", JSON.stringify(array));
            requestedSA = false;
            fs.unlink(__dirname + '/public/spreading_activation_result.json', function(err) {
                if (err && err.errno != 34) console.log(err);
            });
        }
    });
    fs.readFile('public/network_distance.json', function (err, data) {
        if (err) {
            if (err.errno != 34) console.log(err); // ignore if file not found
            return;
        }
        if (data != oldFileND) {
            try {
                object = JSON.parse(data);
                oldFileND = data;
            } catch (e) {
                return;
            }
            io.emit("data network distance", JSON.stringify(object));
            fs.unlink(__dirname + '/public/spreading_activation_result.json', function(err) {
                if (err && err.errno != 34) console.log(err);
            });

            fs.unlink(__dirname + '/public/network_distance.json', function(err) {
                if (err && err.errno != 34) console.log(err);
            });
        }
    });
});

python.stderr.on('readable', function () {
    var chunk;
    while (null !== (chunk = python.stdout.read())) {
        var message = String(chunk);
        console.log("OUTPUT:\n" + message);
        io.emit("chat message", message);
    }
});

preparedAuto = false;

prepareAuto = function() {
    if (preparedAuto) {
        return;
    }
    preparedAuto = true;
    /* Provide autosuggest json */
    //Converter Class
    var Converter = require("csvtojson").core.Converter;
    var fs = require("fs");

    var csvFileName = dataPath + "auto.csv";
    var fileStream = fs.createReadStream(csvFileName);
    //new converter instance
    var csvConverter = new Converter({constructResult: true});

    //end_parsed will be emitted once parsing finished
    csvConverter.on("end_parsed", function (jsonObj) {
        auto_suggest = jsonObj;
    });

    //read from file
    fileStream.pipe(csvConverter);
};

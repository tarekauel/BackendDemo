var spawn = require('child_process').spawn,
    ls    = spawn('/usr/bin/python', ['/Users/tarek/gl_extensions/test.py']);

ls.stdout.on('data', function (data) {
    console.log('OUTPUT:' + data);
});

ls.stderr.on('data', function (data) {
    console.log('OUTPUT: ' + data);
});

ls.on('close', function (code) {
    if (code !== 0) {
        console.log('grep process exited with code ' + code);
    }
});

ls.stdin.write("exit()\n");
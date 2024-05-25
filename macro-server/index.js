const os = require("node:os");
const express = require("express");
const fs = require("fs");
const { exec } = require("node:child_process");
const ip = require("ip");
const app = express();
const port = 4321;

let commands = {};

switch (process.platform) {
  case "win32": // Windows
    commands = JSON.parse(fs.readFileSync("./commands/windows.json", "utf8"));
    break;
  case "linux": // Linux
    commands = JSON.parse(fs.readFileSync("./commands/linux.json", "utf8"));
    break;
  case "darwin": // Mac
    commands = JSON.parse(fs.readFileSync("./commands/mac.json", "utf8"));
    break;
  default:
    console.error("OS not supported");
    process.exit(1);
}

function response(message = "done") {
  return `<!DOCTYPE html>
    <html lang='en'>
      <head>
        <title>Macro Server</title>
        <meta charset='utf-8'>
      </head>
      <body>
        <p>${message}</p>
      </body>
    </html>`;
}

function execute(cmd) {
  console.log();
  if(!cmd || cmd === "") {
	console.log("Command not assigned.");
    return;
  }

  console.log(`Command: ${cmd}`);
  const process = exec(cmd, (err) => {
    if (err) {
      console.error("could not execute command: ", err);
      return;
    }
  });
  process.stdout.on('data', function(data) {
    console.log(data);
  });
}

app.get("/ping", (req, res) => {
  console.log("pinged");
  res.send(response("OK"));
});

app.get("/volume_mute", (req, res) => {
  execute(commands["volume_mute"]);
  res.send(response());
});

app.get("/volume?:level", (req, res) => {
  if (req.url.includes("=up")) {
    execute(commands["volume_up"]);
  } else {
    execute(commands["volume_down"]);
  }
  res.send(response());
});

// play previous media
app.get("/b/:key", (req, res) => {
  const key = req.params.key;
  if (key == 1) {
    res.send(response("OK"));
  } else {
    console.log("Key: " + key);
    execute(commands["b" + req.params.key]);
    res.send(response());
  }
});

app.listen(port, () => {
  console.log(`Server started. Open http://${ip.address()}:${port}/ping in a web browser.`);
}).on('error', function (err) {
  if(err.code === 'EADDRINUSE') {
      console.log(`The port ${port} is already in use, may be the macro server is already running.`);
  } else {
      console.log(err);
  }
  process.exit(1);
});

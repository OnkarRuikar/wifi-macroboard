# Macro server setup and hosting

To execute macro commands on your PC you need to host an HTTP server on your PC. Let us call it macro server. The macro server receives HTTP requests from Pico W or any web browser. A request looks like any URL that you use in web browsers, e.g. `http://192.168.0.55:4321/volume_mute`.

## Prerequisites

1. Node.js: [LTS version of Node.js](https://nodejs.org/en/download).
2. Your PC needs to have a constant(static) IP in your network. In other words your PC should get same IP address every power off and on everyday. You can achieve this using one of the following methods:
  a. On your router, assign an IP address to your PC's MAC address. This is the most stable way.
  b. In your OS [manually set IP address](https://youtu.be/_QnqFsWJV58?si=2GlFyc4yrwGr704Y).

## Setup macro server

Execute following steps to build and host the server:

1. Copy [macro-server](./../macro-server) directory to any suitable location where you want to keep the server code forever. Let's say `~/scripts/` on Linux.
2. Open terminal/command-prompt.
3. In terminal, switch to the server directory/folder.
4. Execute following command to setup the server:

   ```bash
   npm install
   ```

5. The default server port is `4321` which mostly won't create any problems. In case if the port is not available for any reasons, then you can change it in `index.js` file.
6. Execute following command to start the server:

    ```bash
    node index.js
    ```

7. Open a web browser and use following URL. Use your PC's IP address.

   ```text
   http://192.168.0.55:4321/ping
   ```

   It should display `OK` in the browser.

8. Close the server by pressing `ctrl + c` keys.

## Add or update macro commands

Open `macro-server/commands` directory and open a `.json` file that has the same name as your operating system. Open terminal/command prompt and switch to the `macro-server/commands` directory. Try all the existing commands in the terminal to make sure they work. If required, then update the commands to make them work on your operating system. You may need to install the commands if not available in your Linux instance.

You can add new commands, edit exiting ones, or remap them to rearrange button functions.

Start the macro server and try all the macro URLs in a web browser. Make sure the macro commands actually work.

```plain
http://192.168.0.55:4321/volume_up
http://192.168.0.55:4321/volume_down
http://192.168.0.55:4321/volume_mute
http://192.168.0.55:4321/b1
http://192.168.0.55:4321/b2
...
```

### Execute script

Entire script file can also be executed using the macro server. For example:

- Bash script `.sh` file
- Batch file `.bat` file
- Python`.py` file
- Node.js JavaScript `.js` file

To execute a script file set one of the following in command files:

```json
{
  "b5": "bash ./scripts/sample.sh",
  "b6": "./scripts/sample.bat",
  "b7": "python3 ./scripts/sample.py",
  "b8": "node ./scripts/sample.js"
}
```

## Run macro server on computer startup

The macro server can be run more easily on user log on. Following steps ensures that the macros are run on behalf of the user and at the user's authorization level.

### Linux

Edit `./scripts/start-macro-server.sh` file and update the drive and path.

To run the bash script easily add following to your shell config file.

#### Bash shell

Add following code at the end of `~/.bashrc` file:

```bash
macro-server() {
  bash /home/username/scripts/macro-server/scripts/start-macro-server.sh 
}
```

#### Fish shell

Add following code at the end of `~/.config/fish/config.fish` file:

```plain
function macro-server
  bash /home/username/scripts/macro-server/scripts/start-macro-server.sh
end
```

Once you login you need to open a terminal and run `macro-server` command and tuck the terminal window away.

### Windows

Edit `./scripts/start-macro-server.bat` file and update the drive and path.

To run the batch file when you log in, create a scheduled task using Windows' Task Scheduler utility refer [this video guide](https://youtu.be/lzy8KNnqV0I?si=g8EgwUc6-RrhjSEU&t=65). Note, make sure on 'Triggers' tab set `Begin the task: At log on`. Select the `start-macro-server.bat` as the program/script to run.

You can improve automatically running the server as per your need.

## Next

[Program Pico W](./3_program_pico_w.md)

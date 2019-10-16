# MuddySwamp

Multi-user dungeons, or "MUDs" are text-based role-playing games, that naturally evolved from the text-based rpg and adventure games of the 1970s.
This project aims to introduce a new generation—one that never experienced a world without broadband internet—to this classic game genre.
While this code can be adapted for any setting, we intend to render our university in beautiful ASCII. 

Note: this repo has the internal (less stable) branch `develop` set to default.
For a more stable version, please look at the `master` branch.

## Requirements

### Hosting
For **hosting** a server, Python 3 must be installed on the system (along with an appropriate internet connection.) For help with Python installation, visit <https://www.python.org>

### Connecting
For **connecting** to an existing server, a simple telnet client is required. However, we recommend using a dedicated MUD client to avoid ugliness like this:

![raw_telnet.png](images/raw_telnet.png)

There are many solid MUD clients available. 
We have been using [Mudlet](https://github.com/Mudlet/Mudlet), a completely free and open source MUD client.
Here's the same scenario, in Mudlet:

![mudlet_client.png](images/mudlet_client.png)

## Getting Started
### Hosting

Download this repository, or one of the releases. In a terminal, navigate to the repository and run

```
./MuddySwamp.py
```

By default, the server uses port 1234. If you want to specify a different port, you can run

```
./MuddySwamp.py [port]
```

If you are hosting a server for other people to connect, you will need to port foward your router. When you port forward, select the TCP protocol and direct traffic towards whatever port the server is listening on. 

Once the server begins running, you will see an administrator prompt:

```
2019-02-24 14:49:09,497 [MudServerThread] [INFO] Starting server.
2019-02-24 14:49:09,497 [MudServerThread] [INFO] Server started successfully.
```

You can type "help" to get a list of administrator commands.

```
help
2019-02-24 14:50:01,441 [MainThread] [INFO] Server commands are:
 broadcast [message] - Broadcasts a message to the entire server
 players - Prints a list of all players
 stop - Stops the server
 list [locations|items|chars] - list all available loaded locations/items/chars
```

### Connecting

#### with a Raw Telnet Client

If you want to use an ugly, raw telent client, you can use the following terminal command on *nix systems:

```
telnet <ip address> 1234
```

On Windows, a telnet client is not provided by default. One option is to follow [this guide](http://technet.microsoft.com/en-us/library/cc771275%28v=ws.10%29.aspx)
to enable the Windows telnet client.

Alternatively, you can install [PuTTY](https://putty.org/), a **free and open source** telnet and ssh client. 

#### with Mudlet
1. Run Mudlet. You will be prompted to "Select a profile to connect with". 
2. You must enter a set of required fields:
    - For "Profile name", put whatever you prefer.
    - For "Server address", put the address of the server.
    - For "Port", put the port of the server.
3. Once all the fields are entered, simply press "connect". 
4. Have fun!
5. When you exit Mudlet, you will be asked if you want to save the profile. Select "Yes", and simply load the profile next time you play.

## Contributing

Please read **[CONTRIBUTING.md](CONTRIBUTING.md)** for how to work on the project.

## License

This project is licensed under the **MIT** License - see the [LICENSE.md](LICENSE.md) file for details.

test

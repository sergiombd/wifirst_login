# Wifirst CLI portal login tool

`wifirst_login` is a very simple CLI tool to login into the public wifirst 
network that is widely found in student dorms.

Several tools already exist but none are up to date with the new Wifirst portal that has the following link https://portal-front.wifirst.net/.

The CLI is based on [tiangolo's typer](https://typer.tiangolo.com/) which is an increadible CLI builder tool.
You'll need to run the following line to run the tool as is:

```bash
pip install "typer[all]"
```

If you want a minimalist way to run it, you can remove typer to only use builtin python libraries. You can check [the following repo](https://github.com/MarcVillain/wifirst-connect) which demonstrates how to have a service that automatically starts on startup. If you do the following, you should choose where to store your credentials and add a while loop to login whenever the connection is lost.
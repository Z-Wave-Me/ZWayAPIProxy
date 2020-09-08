# Proxy tool to run UI from local folder and Z-Way API from remote server

## Usage

```
./ZWayAPIProxy.py [URL to API server] [local port]
```

Default URL to API server is http://localhost:8889  
Default local port is 8888

# Forward ports for a remote API server

ssh my-server.com -L 8889:127.0.0.1:8083

## Preparing the UI

```
mkdir htdocs
cd htdocs
git clone https://github.com/Z-Wave-Me/zwave-smarthome.git smarthome
(cd smarthome && git checkout stage)
git clone https://github.com/Z-Wave-Me/ExpertUI.git expert
(cd expert && git checkout stage)
cd ..
```

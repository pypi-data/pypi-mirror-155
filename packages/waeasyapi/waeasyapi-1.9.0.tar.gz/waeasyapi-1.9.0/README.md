# WA Easy API Python Client

[![PyPI](https://img.shields.io/pypi/pyversions/waeasyapi.svg)]() [![License](https://img.shields.io/:license-mit-blue.svg)](https://opensource.org/licenses/MIT)

Python bindings for interacting with the WA Easy API

This is primarily meant for developers who wish to perform interactions with the WA Easy API programatically.

## Installation

```sh
$ pip install waeasyapi
```

## Usage

You need to setup your key and secret using the following:
You can find your keys at <https://app.waeasyapi.com/>.

```py
import waeasyapi
client = waeasyapi.Client(auth=("<YOUR_ACC_ID>", "<YOUR_ACC_SECRET>"))
```

## Usage

```py
// number must start with the country's dialing code

// example - For USA: 158883993
// example - For India: 919876543210

client.message.sendMessage({
  "number" : "188377783",
  "message" : "Hello world!"
})

// example - send a text message
client.message.sendMessage({
  "number" : "188377783",
  "message" : "Hello world!"
})

// example - send an approved WhatsApp template
client.message.sendTemplate({
  "number" : "188377783",
  "template" : "template-name",
  "params" : { 
    "key1" : "value1",
    "key2" : "value2"
  }
})

// example - send an approved WhatsApp media template

// media = media-url-or-media-blob
client.message.sendMedia({
  "number" : "188377783",
  "template" : "template-name",
  "media" : "media-url-or-media-blob",
  "params" : { 
    "key1" : "value1",
    "key2" : "value2"
  }
})

```

## App Details

After setting up client, you can set your app details before making any request
to WA Easy API using the following:

```py
client.set_app_details({"title" : "<YOUR_APP_TITLE>", "version" : "<YOUR_APP_VERSION>"})
```

For example, you can set the title to `Django` and version to `1.8.17`. Please ensure
that both app title and version are strings.

## Bugs? Feature requests? Pull requests?

All of those are welcome. You can [file issues][issues] or [submit pull requests][pulls] in this repository.

[issues]: https://github.com/waeasyapi/waeasyapi-python/issues
[pulls]: https://github.com/waeasyapi/waeasyapi-python/pulls

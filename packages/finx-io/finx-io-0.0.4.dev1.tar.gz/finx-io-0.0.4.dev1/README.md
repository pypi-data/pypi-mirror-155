---
title: APIs
tags: technology, documentation
---

### FinX Capital Markets LLC

Please see LICENSE and SECURITY for terms of use.

# Software Development Kit (SDK)

#### FinX SDK version 0.0.2

The FinX SDK is a collection of code that has interfaces to the FinX Capital Markets
Analytics Platform ('FinX CMAP'). The code in the SDK makes calls to REST APIs 
& WebSocket endpoints. A FinX API Key is required for the SDK to return results.

## Introduction

This document is the definitive source of information for using the FinX SDK for
the following version:

For questions or comments please contact us [via email](mailto:info@finx.io).

## FinX SDK - Python

The FinX SDK is currently available as a python package and contains 2 clients 
that have separate functions and connect to dedicated computing resources on 
the FinX CMAP. Depending on your use case, you may use one or both clients.

- TickPlant
- FinXClient

### TickPlant

The *finx tick_client* package contains TickPlant which is a websocket client that 
may be run synchronously ('sync' mode) or asynchronously ('async' mode).

Sync mode is a single call to the platform over websocket, including a connect, 
function call, and disconnect. This mode should only be used for one-time calls or 
for testing individual methods. For production purposes, use the Async mode.

Async mode is used in a check_event loop with a connection established, followed 
by streaming data and/or multiple message requests over the same connection. An 
example of how to use Async mode is documented below in the Jump Right In section 
where the run_tests method is included for reference.

#### TickPlant Websocket Endpoints

The websocket endpoints for FinX TickPlant are:


- TEST ENDPOINT: wss://beta.finx.io/ws/
- PROD ENDPOINT: wss://ws.finx.io/ws/

***

#### Install finx-io

BETA MODE ANNOUNCEMENT: the TestPyPi package directory is the Beta Version of the FinX SDK.

linux
```bash
#! bash
## linux
pip install -i https://test.pypi.org/simple/ finx-io
```
mac-os
```bash
#! bash
## mac-os assuming you use python3
python3 -m pip install -i https://test.pypi.org/simple/ finx-io
```


***

#### Import finx into python

You must set your environment variable 'FINX_API_KEY' to your assigned FinX API Key.

```bash
#! bash
export FINX_API_KEY=my_api_key
export FINX_API_ENDPOINT=my_api_endpoint
```

or, you may set up your environment variable 'FINX_API_KEY' in python directly:

```python
#! python
import os
from src import finx
from finx import tick_client

os.environ['FINX_API_KEY'] = input('---> ENTER FINX API KEY ---> ') 
```

then call the tick_client using your api key:

```python
my_api_key = os.environ['FINX_API_KEY']
my_tick_client = tick_client.TickPlant(api_key=my_api_key, environment='dev')
```

***

#### Tick Plant Methods 0.0.2

The Tick Plant in finx-io=0.0.2 includes the following methods.

##### TICKER REFERENCE DATA

TickPlant.get_reference_data(ticker)

```python
my_ticker = 'BTC'
my_ref_data = my_tick_client.get_reference_data(my_ticker)
```

Example return dict:

```python
return_dict: {
    "function-call":"secdb",
    "request-datestamp":"2022-06-19T17:21:22.380Z",
    "request-security-id":"BTC",
    "ref-data":{
        "ticker":"BTC",
        "security-name":"Bitcoin",
        "finx-sec-id":"fc22a61c-3bcc-4885-a73d-f493a10e05de"
    }
}
```

TickPlant.tick_snap(pair, date, time)

```python
my_pair = 'BTC:USD'
my_date = '2022-06-15'
my_time = '00:00'
my_ref_data = my_tick_client.tick_snap(my_pair, my_date, my_time)
```

Example return dict:

```python
{
    "pair":"BTC:USD",
    "date":"2022-06-15",
    "time":"21:27:40.453Z",
    "exchange":"COINBASE",
    "price":"21865.010000000002"
}
```

TickPlant.tick_history(pair, date, time)

```python
my_pair = 'BTC:USD'
my_date = '2022-06-01'
my_time = '00:00'
my_ref_data = my_tick_client.tick_history(my_pair, my_date, my_time)
```

This method currently returns 100 rows at a time. You may specify a single pair. The "date" entered 
is the *start date* for the return series. Items are not sorted by date, you will have to order the 
result set when you receive it.

In a future release, we will include the following parameters:

- number of observations (future, up to a max of 1000)
- frequency of ticks across time window (future)
- my_date is starting time (0.0.2 included)
- my_end_date is ending window (future)

Example return dict:

```python
{
    "0":{
        "pair":"BTC:USD",
        "date":"2022-06-15",
        "time":"21:27:40.453Z",
        "exchange":"COINBASE",
        "price":"21865.010000000002"},
    "1":{
        "pair":"BTC:USD","date":"2022-06-15",
        "time":"18:07:17.110Z",
        "exchange":"COINBASE",
        "price":"20871.54"},
    "2":{
        "pair":"BTC:USD",
        "date":"2022-06-15",
        "time":"11:57:01.842Z",
        "exchange":"GEMINI",
        "price":"21100.50"},
    "3":{
        "pair":"BTC:USD",
        "date":"2022-06-15",
        "time":"08:47:43.619Z",
        "exchange":"FTX",
        "price":"20209.32"},#...
}
```

***

## Jump Right In

### Following is the code from the run_tests.py script, also found in github

```python
#! python
# run tests for tick_client and client
import nest_asyncio
import os

from tick_client import asyncio, Hybrid, TickPlant


@Hybrid
async def main(environment: str = "dev"):
    print('main routine kicked off using api_key:', os.getenv('FINX_API_KEY'))
    api_key = os.getenv('FINX_API_KEY')
    tick_plant = TickPlant(api_key, environment)
    tick_plant.api_key = api_key
    await tick_plant.connect()
    ref_data: dict = await tick_plant.get_reference_data("BTC")
    snap_data: dict = await tick_plant.tick_snap("BTC:USD", "2022-06-15", "00:00")
    history: dict = await tick_plant.tick_history("BTC:USD", "2022-06-15", "00:00")
    print(f'**********************\nBTC REFERENCE DATA: {ref_data}\n\n')
    print(f'**********************\nBTC SNAP DATA: {snap_data}\n\n')
    print(f'**********************\nBTC HISTORY DATA: {history}\n\n')


def main_synchronous(environment: str = "dev"):
    print('main_synchronous routine kicked off using api_key:', os.getenv('FINX_API_KEY'))
    api_key = os.getenv('FINX_API_KEY')
    tick_plant = TickPlant(api_key, environment)
    tick_plant.connect()
    ref_data: dict = tick_plant.get_reference_data("BTC")
    snap_data: dict = tick_plant.tick_snap("BTC:USD", "2022-06-15",  "00:00")
    history: dict = tick_plant.tick_history("BTC:USD", "2022-06-15", "00:00")
    print(f'**********************\nBTC REFERENCE DATA: {ref_data}\n\n')
    print(f'**********************\nBTC SNAP DATA: {snap_data}\n\n')
    print(f'**********************\nBTC HISTORY DATA: {history}\n\n')


if __name__ == '__main__':
    print('-----> FinX Test Runner ----->')
    print(' ')
    finx_api_key = input("Please enter your FinX API Key --> ")
    os.environ['FINX_API_KEY'] = finx_api_key
    """
    There are 2 ways to use the sdk client
    (1) Synchronous
    (2) Async
    """
    # RUN SYNC
    main_synchronous()
    # RUN ASYNC
    check_event_loop = asyncio.get_event_loop()
    # Hybrid decorated methods can be called like synchronous methods
    print(f'{check_event_loop}')
    if check_event_loop.is_running():
        nest_asyncio.apply()
        # * The only caveat is if Hybrid method is called from within a running event loop *
        check_event_loop.run_until_complete(main())
    else:
        main()


```

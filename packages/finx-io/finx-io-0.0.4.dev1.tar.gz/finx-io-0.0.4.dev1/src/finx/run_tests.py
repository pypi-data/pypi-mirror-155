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


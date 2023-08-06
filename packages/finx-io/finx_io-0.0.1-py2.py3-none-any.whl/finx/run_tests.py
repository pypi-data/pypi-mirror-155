#! python
# run tests for tick_client and client
import nest_asyncio

from tick_client import asyncio, Hybrid, TickPlant


@Hybrid
async def main(api_key: str = '8e22344d-94b0-4579-bee8-bbbf2838f36f', environment: str = "dev"):
    tick_plant = TickPlant(api_key, environment)
    await tick_plant.connect()
    ref_data: dict = await tick_plant.get_reference_data("BTC")
    snap_data: dict = await tick_plant.tick_snap("BTC:USD", "2022-06-15")
    history: dict = await tick_plant.tick_history("BTC:USD", "2022-06-15")
    print(f'**********************\nBTC REFERENCE DATA: {ref_data}\n\n')
    print(f'**********************\nBTC SNAP DATA: {snap_data}\n\n')
    print(f'**********************\nBTC HISTORY DATA: {history}\n\n')


def main_synchronous(api_key: str = '8e22344d-94b0-4579-bee8-bbbf2838f36f', environment: str = "dev"):
    tick_plant = TickPlant(api_key, environment)
    tick_plant.connect()
    ref_data: dict = tick_plant.get_reference_data("BTC")
    snap_data: dict = tick_plant.tick_snap("BTC:USD", "2022-06-15")
    history: dict = tick_plant.tick_history("BTC:USD", "2022-06-15")
    print(f'**********************\nBTC REFERENCE DATA: {ref_data}\n\n')
    print(f'**********************\nBTC SNAP DATA: {snap_data}\n\n')
    print(f'**********************\nBTC HISTORY DATA: {history}\n\n')


if __name__ == '__main__':
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


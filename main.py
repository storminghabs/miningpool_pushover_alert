import crypto_pools


def main_loop():
    hive_pool = crypto_pools.pool_ethermine(
        "https://hiveon.net/api/v1/stats/miner/",
        "ETH_ADDRESS",
        "PUSHOVER_APP_TOKEN",
        "PUSHOVER_USER_TOKEN"
    )
    eth_pool = crypto_pools.pool_hiveon(

        "https://api.ethermine.org/miner/",
        "ETH_ADDRESS",
        "PUSHOVER_APP_TOKEN",
        "PUSHOVER_USER_TOKEN"
    )

    pools = [eth_pool,hive_pool]

    #If wanted you could add an outer loop with timers
    for pool in pools:
        if pool.pull_data():
            pool.calculate_has_rate()
            pool.print_hash_rate()
            pool.alert()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_loop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

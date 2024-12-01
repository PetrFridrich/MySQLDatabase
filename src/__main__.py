import setup_database.db_setup as db_setup


def main():

    db_setup.INIT_DB()

    return None


if __name__ == '__main__':

    print('Hello, home!')

    main()
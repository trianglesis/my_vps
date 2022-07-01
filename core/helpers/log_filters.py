import logging


class DebugDjangoFilters(logging.Filter):
    def filter(self, record):
        """
        Two lists of allowed and diasllowed django internal debug func levels: record.funcName
        :param record:
        :return:
        """
        # 'debug_sql' - shows all sql queries and even cache load
        # 'log_message' - base http message, useful to get page load confirm
        allowed = ['log_message']
        disallowed = ['watch_dir', 'tick', '_resolve_lookup', 'debug_sql']

        if record.funcName in allowed:
            return True
        elif record.funcName in disallowed:
            return False
        else:
            print(
                f"record.filename: {record.filename}; record.funcName: {record.funcName}; record.module: {record.module}")
        return True

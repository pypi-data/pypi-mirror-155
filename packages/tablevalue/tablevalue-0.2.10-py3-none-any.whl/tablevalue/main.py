import sqlite3


class TableValue(object):
    class Types:
        INTEGER = 'INTEGER'
        REAL = 'REAL'
        TEXT = 'TEXT'
        BLOB = 'BLOB'

    @staticmethod
    def _get_where_string_value(filter_query: dict):
        if len(filter_query) > 0:
            where_section = list()
            where_string = 'where '
            values_query = list()
            for key, value in filter_query.items():
                string_filter = f'{key}=?'
                values_query.append(value)
                where_section.append(string_filter)

            where_string += ' and '.join(where_section)
        else:
            values_query = None
            where_string = ''
        return where_string, values_query

    def __init__(self, path=None, manager=None, table_name='Table1', new_table=True):
        if not manager is None:
            self.manager = manager
            self.conn = self.manager.conn
        elif path is None:
            self.manager = Manager(':memory:')
            self.conn = self.manager.conn
        else:
            self.manager = Manager(path)
            self.conn = self.manager.conn
        if self.manager.exists(table_name) and new_table:
            raise NameError(f'Table with name [{table_name}] already exist.')
        self._transaction_active = False
        self.cur = self.conn.cursor()
        if new_table:
            self.manager.tables[table_name] = table_name
            self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
                           id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL);""")
            self.conn.commit()
        self.table_name = table_name
        self.columns = Columns(self, new_table)

    def begin_transaction(self):
        self._transaction_active = True

    def transaction_is_active(self) -> bool:
        return self._transaction_active

    def finish_transaction(self):
        self.conn.commit()

    def cancel_transaction(self):
        if self.transaction_is_active():
            self.conn.rollback()

    def new_row(self):
        return Row(self)

    def new_bulk_insert(self, *values_to_bulk):
        self.cur.executemany(
            f'INSERT INTO {self.table_name}({self.columns.get_all_at_string()}) VALUES({self.columns.get_question_for_query()});',
            tuple(values_to_bulk[0]))
        if not self.transaction_is_active():
            self.conn.commit()

    def get_data(self, filter_query=None, sort='', limit=100000000):
        """
        Fast get method from table
        :param limit: limit for select
        :param filter_query: dict
        :param sort: str
        :return:
        """

        if filter_query is None:
            filter_query = {}

        sort_string = ''
        if bool(sort):
            sort_string = f'order by {sort}'

        where_string, values_query = self._get_where_string_value(filter_query)

        if values_query is None:
            self.cur.execute(
                f'SELECT {self.columns.get_all_at_string()} FROM {self.table_name} {where_string} {sort_string} Limit {limit};')
        else:
            self.cur.execute(
                f'SELECT {self.columns.get_all_at_string()} FROM {self.table_name} {where_string} {sort_string} Limit {limit};',
                values_query)

        all_data = self.cur.fetchall()
        return all_data

    def get_rows(self, filter_query=None, sort='', limit=100000000):

        """
        Slow formatted get method from table
        :param limit: limit for select
        :param filter_query: dict
        :param sort: str
        :return: list of Row classes
        """

        if filter_query is None:
            filter_query = {}

        all_pre_data = self.get_data(filter_query, sort, limit)
        all_data = list()
        for data in all_pre_data:
            all_data.append(Row(self, data))

        return all_data

    def get_grouped_data(self, columns_to_group, columns_to_sum='', filter_query=None, sort='',
                         number_of_rows=100000000, row_mode=True):

        if filter_query is None:
            filter_query = {}

        if type(columns_to_group) == str:
            columns_to_group = [i.strip() for i in columns_to_group.split(',')]

        if type(columns_to_sum) == str:
            columns_to_sum = [i.strip() for i in columns_to_sum.split(',')]

        sort_string = ''
        if bool(sort):
            sort_string = f'order by {sort}'

        where_string, values_query = self._get_where_string_value(filter_query)

        text_grouped = ','.join(columns_to_group)
        text_sum = []
        for to_group in columns_to_sum:
            text_sum.append(f'sum({to_group})')

        if len(text_sum):
            text_sum = ',' + ','.join(text_sum)
        else:
            text_sum = ''

        executed_text = f'select {text_grouped}{text_sum} from {self.table_name} {where_string} group by {text_grouped} {sort_string} Limit {number_of_rows}'

        if values_query is None:
            self.cur.execute(executed_text)
        else:
            self.cur.execute(executed_text, values_query)

        result = self.cur.fetchall()

        if row_mode:
            all_data = list()
            for data in result:
                all_data.append(Row(self, data, columns_to_group + columns_to_sum))
            return all_data
        else:
            return result

    def count(self):
        self.cur.execute(f'select count(*) from {self.table_name}')
        return self.cur.fetchone()[0]

    def update(self, filter_query, values_query):
        update_string = []
        arguments = []
        for key, value in values_query.items():
            update_string.append(f'{key} = ?')
            arguments.append(value)

        where_string, values_for_query = self._get_where_string_value(filter_query)
        for value_query in values_for_query:
            arguments.append(value_query)

        update_string = ','.join(update_string)
        executed_text = f'''Update {self.table_name} set {update_string} {where_string}'''
        self.cur.execute(executed_text, arguments)
        if not self.transaction_is_active():
            self.conn.commit()

    def special_query(self, query, need_commit=False):
        self.cur.execute(query)
        if need_commit:
            self.conn.commit()
        else:
            return self.cur.fetchall()

    def clear(self):
        sql = f'delete from {self.table_name}'
        self.cur.execute(sql)
        if not self.transaction_is_active():
            self.conn.commit()

    def delete(self, filter_query):
        where_string, values_query = self._get_where_string_value(filter_query)
        sql = f'delete from {self.table_name} {where_string}'
        self.cur.execute(sql, values_query)
        if not self.transaction_is_active():
            self.conn.commit()

    def drop(self):
        sql = f'drop table {self.table_name}'
        self.cur.execute(sql)
        if not self.transaction_is_active():
            self.conn.commit()


class DictOnes(dict):
    def __init__(self, keys=None, *values, type_return=None):
        if keys is None:
            return
        index = 0
        for key in [i.strip() for i in keys.split(',')]:
            if len(values) and len(values) >= index + 1:
                value = values[index]
            else:
                value = None
            self[key] = value
            index += 1

    def __getattr__(self, attrname):
        if attrname not in self:
            raise KeyError(attrname)
        return self[attrname]

    def __setattr__(self, attrname, value):
        self[attrname] = value

    def __delattr__(self, attrname):
        del self[attrname]

    def copy(self):
        return DictOnes(super(DictOnes, self).copy())


class Manager(object):
    def __init__(self, path=':memory:', connection=None):
        if not connection is None:
            self.conn = connection
        else:
            self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self.tables = dict()
        if path != ':memory:':
            sql = "SELECT name FROM sqlite_master WHERE type='table'"
            self.cur.execute(sql)
            all_tables = self.cur.fetchall()
            for table_name in all_tables:
                self.tables[table_name[0]] = self.get(table_name[0], True)

    def update_list_tables(self):
        for table_name in list(self.tables):
            self.__dict__[table_name[0]] = self.get(table_name[0])

    def get(self, table_name, initial=False) -> TableValue:
        if not initial and not self.exists(table_name):
            return None
        tablevalue = TableValue(manager=self, table_name=table_name, new_table=False)
        return tablevalue

    def drop_table(self, name):
        if not name in self.tables:
            raise NameError(f'Table [{name}] is not exists.')
        sql = f'drop table {name}'
        self.cur.execute(sql)
        del self.tables[name]

    def exists(self, name):
        return name in list(self.tables.values())

    def close(self):
        for table in list(self.tables):
            self.drop_table(table)


class Columns(list):

    def __init__(self, parent, new_table):
        self._parent = parent
        if not new_table:
            columns_info = parent.cur.execute(f'pragma table_info({parent.table_name})').fetchall()
            for column_info in columns_info:
                column = DictOnes('name, type', column_info[1], column_info[2])
                self.append(column)

    def add(self, name_column, type_column='TEXT') -> None:
        """
        Add column in the table
        :param name_column:
        :param type_column: INTEGER, REAL, TEXT, BLOB
        :return:
        """
        column = DictOnes('name, type', name_column, type_column)
        self.append(column)
        self._parent.cur.execute(f'ALTER TABLE {self._parent.table_name} ADD COLUMN {name_column} {type_column}')
        self._parent.conn.commit()

    def get_all(self) -> list:
        result = list()
        for column in self:
            result.append(column['name'])

        return result

    def get_all_at_string(self):
        all_columns = self.get_all()
        return ','.join(all_columns)

    def get_question_for_query(self) -> str:
        pre_result = list()
        for column in self.get_all():
            pre_result.append('?')
        return ','.join(pre_result)


class Row(object):

    def __init__(self, parent: TableValue, filled_values=None, name_fields=None):
        self._parent = parent
        self._all_columns_string = parent.columns.get_all_at_string()
        self._all_columns = parent.columns.get_all()
        if filled_values is None:
            self._new_string = True
        else:
            self._new_string = False

        index = 0

        if name_fields is None:
            columns = self._parent.columns.get_all()
        else:
            columns = name_fields

        for column in columns:
            if filled_values is None:
                value = None
            else:
                value = filled_values[index]
            self.__dict__[column] = value
            index += 1

    def __str__(self):
        result = list()
        for i in self._all_columns:
            result.append(f'[{i}:{self.__dict__[i]}]')
        return ', '.join(result)

    def apply_add(self):
        if not self._new_string:
            return

        values_for_query = list()
        for column in self._all_columns:
            values_for_query.append(self.__dict__[column])

        self._parent.cur.execute(
            f'INSERT INTO {self._parent.table_name}({self._all_columns_string}) VALUES({self._parent.columns.get_question_for_query()});',
            list(values_for_query))
        if not self._parent.transaction_is_active():
            self._parent.finish_transaction()
#!/usr/bin/env python

# original code: http://code.activestate.com/recipes/577599-nagios-plugin-for-monitoring-database-servers/
# Nagios_sql.py - Matt Keranen 2011 (mksql@yahoo.com)
# Pablo Estigarribia 201705 (pablodav at gmail)
#
# changes:
# * use pymssql instead of pyodbc to have simple setup
# * refactor compatible to python3
# * code inspect and fixes to pep8 compliant
# * Added possibility to use user and password from cmd
# * Added better output on CRITICAL and WARNING in replication_status

import sys
import pymssql
import argparse
from . import __version__


nagios_codes = dict(OK=0, WARNING=1, CRITICAL=2, UNKNOWN=3, DEPENDENT=4)


def parse_args(args):
    """
    Information extracted from: https://mkaz.com/2014/07/26/python-argparse-cookbook/
    :return:
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-H', '--host', dest='host',
                        help='SQL Backup HOST to connect')

    # Adding test choices
    parser.add_argument("--test", '-t', dest='test',
                        choices=test_pylist(),
                        help=test_list()
                        )

    parser.add_argument("-U", "--user", dest='user', help="User to auth to DB")
    parser.add_argument("-P", "--password", dest='password', help="Password to auth to DB")
    parser.add_argument("-S", "--server_primary", dest='server_primary', help="Specify primary availability group server")
    parser.add_argument("-N", "--publisher_name", dest='publisher_name', 
                        help='used to monitor replication_status in diffent publisher',
                        default=None)
	
    parser.add_argument("-v", "--version", dest='version', nargs='?', default=None, const=True,
                        help="Gets version number")

    if not args:
        raise SystemExit(parser.print_help())

    return parser.parse_args(args)


def nagios_return(code, response):
    print((code + ": " + response))
    sys.exit(nagios_codes[code])


def execute_sql(host, sql, database='master', user="user", password="password", return_dict=True):
    """Execute SQL against specified database"""

    user = user
    password = password
    server = host

    try:
        conn = pymssql.connect(server=server,
                               user=user,
                               password=password,
                               database=database)
    except pymssql.Error as e:
        return {'code': 'CRITICAL', 'msg': "Unable to connect to SQL host %s\n%s" % (host, e)}

    if return_dict:
        cursor = conn.cursor(as_dict=True)
    else:
        cursor = conn.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def get_func(test):
    """Determine if function name is valid and defined as a Nagios test"""

    try:
        func = getattr(sys.modules[__name__], test)
    except AttributeError as e:
        nagios_return('UNKNOWN', 'Invalid test name %s' % test)

    try:
        test = func.is_test
    except:
        nagios_return('UNKNOWN', '%s not defined as test' % test)

    if test:
        return func
    else:
        nagios_return('UNKNOWN', '%s not defined as test' % test)


def test_pylist():
    """Python List of valid test names"""
    tests = []
    for func in dir(sys.modules[__name__]):
        test = getattr(sys.modules[__name__], func)
        try:
            test.is_test
        except:
            pass
        else:
            tests.append(func)

    return tests


def test_list():
    """List of valid test names"""
    tests = 'tests:\n'
    for func in dir(sys.modules[__name__]):
        test = getattr(sys.modules[__name__], func)
        try:
            test.is_test
        except:
            pass
        else:
            tests += '  %s\n' % func

    return tests


def nagios_test(func):
    func.is_test = True
    return func


@nagios_test
def sql_ping(host, user, password):
    """Connect to SQL Server instance and return version string"""

    sql = 'SELECT @@VERSION'
    rows = execute_sql(host, sql, user=user, password=password, return_dict=False)
    if type(rows) is dict:
        return rows

    message = rows[0][0]

    return {'code': 'OK', 'msg': message}


@nagios_test
def db_state(host, user, password):
    """Check state of each database"""
    crit = warn = 0
    msg = ''

    sql = 'SELECT [name] db, user_access, user_access_desc, state, state_desc FROM sys.databases ' \
          'WHERE user_access > 0 OR state > 0'
    rows = execute_sql(host, sql, user=user, password=password)
    if type(rows) is dict:
        return rows

    for row in rows:
        if row.get("state") == 6:
            warn += 1
            msg += 'Database %s is %s\n' % (row.get("db"), row.get("state_desc"))
        elif row.get("state") > 3:
            crit += 1
            msg += 'Database %s is %s\n' % (row.get("d"), row.get("state_desc"))

        if row.get("user_access") > 0:
            # warn += 1
            msg += 'Database %s in mode %s\n' % (row.get("db"), row.get("user_access_desc"))

    if crit > 0:
        code = 'CRITICAL'
        msg = 'Database state CRITICAL\n' + msg
    elif warn > 0:
        code = 'WARNING'
        msg = 'Database state warning\n' + msg
    else:
        code = 'OK'
        msg = 'Databases OK\n' + msg

    return {'code': code, 'msg': msg}


@nagios_test
def replication_status(host, user, password, publisher_name='@@SERVERNAME'):
    """Report transactional replication status"""
    # 0 = error ('Unknown')
    # mstat: status of check publication or subscription
    # mwarn: warning status received from check of publication or subscription
    # Default 0 for both
    mstat = mwarn = 0
    msg = ''
    status_critical_list = [5, 6]
    status_ok_list = [0, 1, 2, 3, 4]

    # Status dictionaries 
    status = {0: 'Unknown', 1: 'Started', 2: 'Succeeded', 3: 'Active', 4: 'Idle', 5: 'Retrying', 6: 'Failed'}
    warning = {0: '', 1: '-Expiration ', 2: '-Latency '}

    def __get_publications_status():
        """
        Check if publication status is not critical and returns status number.
        Check if publication warning is not critical and returns mwarn number.
        Adds msg and publication status vars.

        return: mstat, mwarn, msg
        """
        _mstat = _mwarn = 0
        _msg = ''
        

        # Transactional replication - publications
        # Get data
        sql = 'EXEC dbo.sp_replmonitorhelppublication @publisher = {}'.format(publisher_name)
        rows = execute_sql(host, sql, 'distribution', user=user, password=password)
        if type(rows) is dict:
            return rows

        # Check publications
        for row in rows:

            publication_status = 'OK'

            if row.get("status") in status_critical_list:
                publication_status = "CRITICAL"
                _mstat = row["status"]
                
            elif row.get("warning") > 0:
                publication_status = "WARNING"
                _mwarn = row["warning"]

            if row.get("worst_latency") is None:
                row["worst_latency"] = 0

            _msg += '%s Pub:%s DB:%s Status:%s%s MaxLatency:%ss\n' % (
                publication_status,
                row["publication"],
                row["publisher_db"],
                status.get(row["status"]),
                warning.get(row["warning"]),
                row["worst_latency"])
            
        return _mstat, _mwarn, _msg

    def __get_subscription_status():
        """
        return: mstat, mwarn, msg
        """
        _mstat = _mwarn = 0
        _msg = ''
        # Get data
        sql = 'EXEC dbo.sp_replmonitorhelpsubscription @publisher = {}'.format(publisher_name) + ', @publication_type = 0'
        rows = execute_sql(host, sql, 'distribution', user=user, password=password)
        if type(rows) is dict:
            return rows

        # Check suscriptions
        # will set _mstat or _mwarn to CRITICAL or WARNING number value if any error found
        for row in rows:

            subscription_status = "OK"

            if row.get("status") in status_critical_list:
                subscription_status = "CRITICAL"
                _mstat = row["status"]
            elif row.get("warning") > 0:
                subscription_status = "WARNING"
                _mwarn = row["warning"]

            if row.get("latency") is None:
                row["latency"] = '?'

            _msg += '%s Sub:%s DB:%s Status:%s%s Latency:%ss\n' % (
                subscription_status,
                row.get("subscriber"),
                row.get("subscriber_db"),
                status.get(row["status"]),
                warning.get(row["warning"]),
                row.get("latency"))
        
        return _mstat, _mwarn, _msg

    # Check publications status
    # change variables received from the check.
    mstat, mwarn, msg = __get_publications_status()

    # Transactional replication - suscriptions
    # Do not check subscription_status if publication is CRITICAL.    
    if mstat not in status_critical_list:
        mstat, mwarn, _msg_subscription = __get_subscription_status()
        msg += _msg_subscription

    if mstat in status_critical_list:
        code = 'CRITICAL'
        msg = 'Replication CRITICAL\n' + msg
    elif mwarn > 0:
        code = 'WARNING'
        msg = 'Replication WARNING\n' + msg
    elif mstat in status_ok_list:
        code = 'OK'
        msg = 'Replication OK\n' + msg
    else:
        code = 'CRITICAL'
        msg = 'Replication CRITICAL\n' + msg

    return {'code': code, 'msg': msg}


@nagios_test
def mirror_status(host, user, password):
    """Report mirror status"""
    crit = warn = 0
    msg = ''

    sql = """SELECT d.name dbname, m.mirroring_partner_instance partner, m.mirroring_state, m.mirroring_state_desc state
        FROM sys.databases d
        INNER JOIN sys.database_mirroring m ON m.database_id = d.database_id
        WHERE m.mirroring_state IS NOT NULL"""
    rows = execute_sql(host, sql, user=user, password=password)
    if type(rows) is dict:
        return rows

    # state = {0:'Suspended', 1:'Disconnected', 2:'Synchronizing', 3:'PendingFailover', 4:'Synchronized'}
    # sql = "EXEC sp_dbmmonitorresults '%s'" % dbname

    for row in rows:
        if row.get("mirroring_state") < 2:
            crit += 1
        if row.get("mirroring_state") == 3:
            warn += 1

        msg += "DB:%s Partner:%s State:%s\n" % (
            row.get("dbname"),
            row.get("partner"),
            row.get("state"))

    if crit > 0:
        code = 'CRITICAL'
        msg = 'Mirroring CRITICAL\n' + msg
    elif warn > 0:
        code = 'WARNING'
        msg = 'Mirroring warning\n' + msg
    else:
        code = 'OK'
        msg = 'Mirroring OK\n' + msg

    return {'code': code, 'msg': msg}


@nagios_test
def logship_status(host, user, password):
    """Report log shipping retstore delta and latency"""
    crit = warn = 0
    msg = ''

    sql = """SELECT secondary_server, secondary_database, primary_server, primary_database,
        last_restored_date, DATEDIFF(mi, last_restored_date, GETDATE()) last_restored_delta,
        last_restored_latency, restore_threshold
        FROM msdb..log_shipping_monitor_secondary"""
    rows = execute_sql(host, sql, user=user, password=password)
    if type(rows) is dict:
        return rows

    for row in rows:
        if row.get("last_restored_delta") >= row.get("restore_threshold"):
            warn += 1
            msg += "Srv:%s DB:%s Restore delta %s exceeds threshold of %s\n" % (
                row.get("primary_server"),
                row.get("primary_database"),
                row.get("last_restored_delta"),
                row.get("restore_threshold"))
        if row.get("last_restored_latency") >= row.get("restore_threshold"):
            crit += 1
            msg += "Srv:%s DB:%s Latency of %s exceeds threshold of %s\n" % (
                row.get("primary_server"),
                row.get("primary_database"),
                row.get("last_restored_latency"),
                row.get("restore_threshold"))
        if row.get("last_restored_delta") < row.get("restore_threshold") and \
           row.get("last_restored_latency") < row.get("restore_threshold"):
            msg += "Srv:%s DB:%s Latency:%s Restore delta:%s\n" % (
                row.get("primary_server"),
                row.get("primary_database"),
                row.get("last_restored_latency"),
                row.get("last_restored_delta"))

    if crit > 0:
        code = 'CRITICAL'
        msg = 'Log shipping CRITICAL\n' + msg
    elif warn > 0:
        code = 'WARNING'
        msg = 'Log shipping warning\n' + msg
    else:
        code = 'OK'
        msg = 'Log shipping OK\n' + msg

    return {'code': code, 'msg': msg}
    
@nagios_test
def availability_group_status(host, user, password):
    """availability group status"""
    crit = warn = 0
    msg = ''

    sql = """SELECT ag.name agname, ags.* FROM sys.dm_hadr_availability_group_states ags INNER JOIN sys.availability_groups ag ON ag.group_id = ags.group_id"""
    rows = execute_sql(host, sql, user=user, password=password)
    if type(rows) is dict:
        return rows
    
    #https://docs.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-hadr-availability-replica-states-transact-sql?view=sql-server-2017
    # state = {0:'Not healthy', 1:'Partially healthy', 2:'Healthy'}

    for row in rows:
        if row.get("synchronization_health") == 0:
            crit += 1
        if row.get("synchronization_health") == 1:
            warn += 1

        msg += "Group:{} Primary Replica:{} State:{}\n".format(
            row.get("agname"),
            row.get("primary_replica"),
            row.get("synchronization_health_desc"))

    if crit > 0:
        code = 'CRITICAL'
        msg = 'Availability Group CRITICAL\n' + msg
    elif warn > 0:
        code = 'WARNING'
        msg = 'Availability Group warning\n' + msg
    else:
        code = 'OK'
        msg = 'Availability Group OK\n' + msg

    return {'code': code, 'msg': msg}

@nagios_test
def synchronization_databases_ag(host, user, password, server_primary):
    """Databases Availability group Status"""
	
    msg = ''
    primary = False
    synchronized = 'OK'
	
    #status = {0: 'Unknown', 1: 'Started', 2: 'Succeeded', 3: 'Active', 4: 'Idle', 5: 'Retrying', 6: 'Failed'}
    #warning = {0: '', 1: '-Expiration ', 2: '-Latency '}

    sql = """select * FROM sys.dm_hadr_availability_group_states"""
    rows = execute_sql(host, sql, user=user, password=password)
	
    for row in rows:
        if row.get("primary_replica") == server_primary:
            primary = True

    sql = """SELECT db.name,repstat.synchronization_state_desc,repstat.synchronization_health_desc FROM sys.databases db INNER JOIN sys.dm_hadr_database_replica_states repstat ON db.database_id = repstat.database_id WHERE is_local = 1"""
    rows = execute_sql(host, sql, user=user, password=password)

    if type(rows) is dict:
        return rows
	
    if primary:

        for row in rows:
        
            if row.get("synchronization_state_desc") != "SYNCHRONIZED":
                synchronized = "CRITICAL"
            
            msg += "Name:{} State:{} Health:{}\n".format(
                row.get("name"),
                row.get("synchronization_state_desc"),
                row.get("synchronization_health_desc"))

    else:
        
        for row in rows:
            
            if row.get("synchronization_state_desc") != "SYNCHRONIZING":
                synchronized = "CRITICAL"
            
            msg += "Name:{} State:{} Health:{}\n".format(
                row.get("name"),
                row.get("synchronization_state_desc"),
                row.get("synchronization_health_desc"))
    
    msg = 'Database synchronization\n' + msg
    	
    return {'code': synchronized, 'msg': msg}


def main():

    options = parse_args(sys.argv[1:])

    if options.version:
        raise SystemExit('{}'.format(__version__))

    host = options.host
    test = options.test
    user = options.user
    password = options.password
    publisher_name = options.publisher_name
    server_primary = options.server_primary

    func = get_func(test)
    if publisher_name:
        result = func(host, user=user, password=password, publisher_name=publisher_name)
    elif server_primary:
        result = func(host, user=user, password=password, server_primary=server_primary)
    else:
        result = func(host, user=user, password=password)

    nagios_return(result['code'], result['msg'])
    

if __name__ == "__main__":
    main()
    

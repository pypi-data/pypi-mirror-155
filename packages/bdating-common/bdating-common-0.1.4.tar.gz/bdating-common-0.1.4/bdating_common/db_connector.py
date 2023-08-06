#!/usr/bin/env python3
import pymysql
import boto3
import dns.resolver
import os

os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

def _find_cname_target(domain_name, logger):
    try:
        while True:  # keep digging down until nothing to search
            result = dns.resolver.resolve(domain_name, 'CNAME')
            domain_name = str(list(result)[0].target)
    except Exception as e:
        pass
    return domain_name


def analyse_sonder_rds_host(domain_name, logger):
    # dig down dname until it is not CNAME
    domain_name = _find_cname_target(domain_name, logger)
    if domain_name[-1] == '.':
        domain_name = domain_name[:-1]
    if domain_name.endswith('.rds.amazonaws.com'):
        return domain_name
    else:
        raise ValueError(
            f"Analysed domain name does not look like a rds host: {domain_name}")


def build_sonder_rds_conector(sonder_domain_name, username, password, db_name, logger, connect_timeout=2):
    return pymysql.connect(host=analyse_sonder_rds_host(sonder_domain_name, logger), user=username,
                           passwd=password, db=db_name, connect_timeout=connect_timeout)


def build_sonder_rds_connector_by_role(sonder_domain_name, db_user_on_role, db_name, logger, connect_timeout=2, profile=None, ):
    session = boto3.Session(profile_name=profile)
    host = analyse_sonder_rds_host(sonder_domain_name, logger)
    region = host.split('.')[-4]
    client = session.client('rds')
    token = client.generate_db_auth_token(
        DBHostname=host, Port=3306, DBUsername=db_user_on_role, Region=region)
    certificate_path=os.path.join(os.path.dirname(__file__), 'global-bundle.cer')
    with open(certificate_path) as f:
        cert_string = f.read() # reading this is really necessary, however if the file is not accessible then the exception will clearly show it
    return pymysql.connect(host=host, user=db_user_on_role, passwd=token, port=3306, database=db_name, ssl_ca=certificate_path, connect_timeout=connect_timeout)


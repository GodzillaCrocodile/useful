from collections import OrderedDict
import time
import xml.etree.ElementTree as et
import requests
from bs4 import BeautifulSoup
import csv
import os
import argparse
import re
from ipaddress import summarize_address_range
from ipaddress import IPv4Address


__author__ = "EStroev <jenya.stroev(at)gmail.com>"
__email__ = "jenya.stroev@gmail.com"

COOKIE = {
    'cookies-accepted': 'accepted',
    'crowd.ripe.hint': 'true',
    '_ga': 'GA1.2.1726447427.1511198866',
    '_gid': 'GA1.2.255152598.1511198866'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Host': 'rest.db.ripe.net',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

KEY_WORDS = ['First', 'Second', 'Third']


def summarize(line):
    if line:
        firstAddr, lastAddr = line.split('-')
        firstAddr = firstAddr.strip()
        lastAddr = lastAddr.strip()
        nets = [ipaddr for ipaddr in summarize_address_range(IPv4Address(firstAddr), IPv4Address(lastAddr))]
        if len(nets) == 1:
            return str(nets[0])
        else:
            return ';'.join(str(net) for net in nets)
    else:
        return None


def ripe_search(query, proxies, headers=HEADERS, cookies=COOKIE):
    url = 'http://rest.db.ripe.net/search.xml?query-string=' + query + '&flags=no-filtering'

    r = requests.get(url, headers=headers, cookies=cookies, timeout=15, proxies=proxies)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "xml")
        return soup
    elif r.status_code == 403:
        print('Access denied: ' + url)
        return None
    elif r.status_code == 404:
        print('404 manage Not Found ' + url)
        return None
    else:
        print(str(r.status_code) + ' ' + url)
        return None


def response_parser(response):
    if response is None:
        print('Response is None')
        return None

    root = et.fromstring(str(response))
    attributes = root.findall('objects/object/attributes/attribute')

    attributes_dict = {
        'inetnum': '',
        'country': '',
        'netname': '',
        'descriptions': list()
    }

    for attribute_iter in attributes:
        if attribute_iter.get('name') == 'inetnum':
            attributes_dict['inetnum'] = attribute_iter.get('value')
        if attribute_iter.get('name') == 'country':
            attributes_dict['country'] = attribute_iter.get('value')
        if attribute_iter.get('name') == 'netname':
            attributes_dict['netname'] = attribute_iter.get('value')
        if attribute_iter.get('name') == 'descr':
            attributes_dict['descriptions'].append(attribute_iter.get('value'))
    return attributes_dict


def csv_writer(out_file, data, ip_list):
    with open(out_file, 'w', newline='') as csv_out:
        csv_out_writer = csv.writer(csv_out, delimiter=';')
        csv_out_writer.writerow(
            [
                'IP',
                'Inetnum',
                'Network',
                'Country',
                'Netname',
                'Descriptions'
            ]
        )
        for ip in ip_list:
            csv_out_writer.writerow(
                [
                    ip,
                    data[ip]['inetnum'],
                    data[ip]['network'],
                    data[ip]['country'],
                    data[ip]['netname'],
                    data[ip]['descriptions']
                ]
            )
    print('\n[+] Write %s IP to %s' % (len(ip_list), out_file))


def analyzed_csv_writer(out_file, data):
    with open(out_file, 'a', newline='') as csv_out:
        csv_out_writer = csv.writer(csv_out, delimiter=';')
        csv_out_writer.writerow(
            [
                'IP', 'Country', 'City'
            ]
        )
        for ip in data:
            csv_out_writer.writerow(
                [
                    ip,
                    data[ip]['country'],
                    data[ip]['city']
                ]
            )
    print('\n[+] Write %s IP to %s' % (len(data), out_file))


def country_analyze(countries, ip, attributes):
    if attributes['country'] in countries:
        countries[attributes['country']].append(ip)
    else:
        countries[attributes['country']] = [ip]


def org_analyze(organizations, ip, attributes):
    if re.search('first', attributes['netname'], re.IGNORECASE):
        organizations['first'].append(ip)
        return 'First'
    elif re.search('second', '; '.join(attributes['descriptions']), re.IGNORECASE):
        organizations['second'].append(ip)
        return 'Second'
    else:
        organizations['other'].append(ip)
        return 'Other'


def city_analyze(cities, ip, attributes):
    if re.search('moscow', attributes['netname'], re.IGNORECASE):
        cities['moscow'].append(ip)
        return 'Moscow'
    elif re.search('moscow', '; '.join(attributes['descriptions']), re.IGNORECASE):
        cities['moscow'].append(ip)
        return 'Moscow'
    else:
        cities['other'].append(ip)
        return 'Other'


def analyze(countries, cities, organizations):
    # 1. Ru, First, Moscow
    first_list = list(set(countries['RU']) & set(cities['moscow']) & set(organizations['first']))
    # 2. Ru, First, Regions
    second_list = list(set(countries['RU']) & set(cities['other']) & set(organizations['first']))
    # 3. Ru, First
    third_list = list(set(countries['RU']) & set(organizations['first']))
    # 4. Ru, Not First
    fourth_list = list(set(countries['RU']) - set(organizations['first']))
    # 1. Ru, Second
    fifth_list = list(set(countries['RU']) & set(organizations['second']))

    return first_list, second_list, third_list, fourth_list, fifth_list


def main():
    parser = argparse.ArgumentParser(description='IP search in the RIPE.net database')
    parser.add_argument('-v', dest='terminal_print', action='store_true', help='Print to console')
    parser.add_argument('-o', dest='output_folder', action='store', help='Output folder for results')
    parser.add_argument('-q', dest='query', action='store', help='Search query for single IP')
    parser.add_argument('-Q', dest='list_query', action='store_true', help='Search query for IP list')
    parser.add_argument('-f', dest='input_file', action='store', help='Input file with IP list for searching')
    parser.add_argument('-a', dest='analyse', action='store_true', help='IP analysis')
    parser.add_argument('-u', dest='unique', action='store_true', help='Only unique IP')
    parser.add_argument('-p', dest='proxy', action='store', help='Proxy')

    args = parser.parse_args()

    PROXY = {
        'http': args.proxy,
        'https': args.proxy
    }

    if not args.output_folder and not args.terminal_print:
        print('[-] You must specify an existing path to the output folder or flag \'-p\' for print to console!')
        exit(-1)
    if args.analyse and not args.output_folder:
        print('[-] You must specify an existing path to the output folder!')
        exit(-1)
    if args.output_folder:
        if not os.path.exists(args.output_folder):
            print('[-] Output folder %s does not exist!' % os.path.abspath(args.output_folder))
            create_out_folder = input('[*] Create output folder? [y/n]: ')
            if create_out_folder in ['Y', 'y']:
                os.makedirs(args.output_folder)
                print('[+] Create output folder %s' % args.output_folder)
            else:
                print('[-] You must specify an existing path to the output folder!')
                exit(-1)
    if args.list_query and not args.input_file:
        print('[-] You must specify an existing path to the input file!')
        exit(-1)
    if not args.list_query and not args.query:
        print('[-] Search query is not specified!')
        exit(-1)

    if args.list_query:
        with open(args.input_file, 'r') as file_in:
            if args.unique:
                ip_list = list(set(file_in.read().split('\n')))  # Only unique
            else:
                ip_list = file_in.read().split('\n')
            if '' in ip_list:
                ip_list.remove('')  # Delete empty line
        print('[+] Open %s and read %d IP (%d unique)\n' % (args.input_file, len(ip_list), len(set(ip_list))))
    else:
        ip_list = [args.query]
        print('[+] Search query for single IP: %s\n' % args.query)

    all_data = dict()
    all_data_for_save = list()
    all_analyzed_data_for_save = list()
    len_ip_list = len(ip_list)

    countries_dict = dict()
    organizations_dict = {
        'first': list(),
        'second': list(),
        'other': list()
    }
    cities_dict = {
        'moscow': list(),
        'other': list()
    }

    start_time = time.time()
    for index, ip in enumerate(ip_list, 1):
        ip = ip.strip()
        if ip not in all_data:
            ripe_response = ripe_search(query=ip, proxies=PROXY)
            ip_attributes_dict = response_parser(response=ripe_response)
            if ip_attributes_dict is None:
                print('[-] %s/%s %s' % (index, len(ip_list), ip))
                continue
            else:
                all_data[ip] = {
                    'inetnum': ip_attributes_dict['inetnum'],
                    'network': summarize(ip_attributes_dict['inetnum']),
                    'country': ip_attributes_dict['country'],
                    'netname': ip_attributes_dict['netname'],
                    'descriptions': '; '.join(ip_attributes_dict['descriptions']),
                    'city': ''
                }
        else:
            ip_attributes_dict = {
                'inetnum': all_data[ip]['inetnum'],
                'network': all_data[ip]['network'],
                'country': all_data[ip]['country'],
                'netname': all_data[ip]['netname'],
                'descriptions': all_data[ip]['descriptions']
            }

        if args.analyse:
            country = country_analyze(countries=countries_dict, ip=ip, attributes=ip_attributes_dict)
            organiation = org_analyze(organizations=organizations_dict, ip=ip, attributes=ip_attributes_dict)
            city = city_analyze(cities=cities_dict, ip=ip, attributes=ip_attributes_dict)
            all_data[ip]['city'] = city

        print('[+] %s/%s %s' % (index, len_ip_list, ip))

        if args.terminal_print:
            print('Inetnum: %s\nCountry: %s\nNetName: %s\nDescriptions: %s\n\n' % (ip_attributes_dict['inetnum'], ip_attributes_dict['country'], ip_attributes_dict['netname'], '; '.join(ip_attributes_dict['descriptions'])))

    if args.output_folder:
        csv_writer(out_file=os.path.join(args.output_folder, 'all.csv'), data=all_data, ip_list=ip_list)

    if args.analyse:
        first_list, second_list, third_list, fourth_list, fifth_list = analyze(countries=countries_dict, cities=cities_dict, organizations=organizations_dict)
        with open(os.path.join(args.output_folder, 'first.csv'), 'w') as outF:
            outF.writelines('\n'.join(sorted(first_list)))
        with open(os.path.join(args.output_folder, 'second.csv'), 'w') as outF:
            outF.writelines('\n'.join(sorted(second_list)))
        with open(os.path.join(args.output_folder, 'third.csv'), 'w') as outF:
            outF.writelines('\n'.join(sorted(third_list)))
        with open(os.path.join(args.output_folder, 'fourth.csv'), 'w') as outF:
            outF.writelines('\n'.join(sorted(fourth_list)))
        with open(os.path.join(args.output_folder, 'fourth.csv'), 'w') as outF:
            outF.writelines('\n'.join(sorted(fifth_list)))
        analyzed_csv_writer(out_file=os.path.join(args.output_folder, 'all_analyzed.csv'), data=all_data)

        print('[+] Write analyzed data to %s' % args.output_folder)

    print("\n--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()

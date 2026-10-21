import sys
import geoip2.database
from geoip2.errors import AddressNotFoundError


def analyze_logs(input_file, db_path):
    country_ips = {}
    with geoip2.database.Reader(db_path) as reader, \
         open(input_file, 'r', encoding='utf-8', errors='ignore') as in_file:
        for line in in_file:
            clean_line = line.strip()
            if not clean_line:
                continue
            line_parts = clean_line.split()
            if not line_parts:
                continue
            ip = line_parts[0]
            try:
                response = reader.country(ip)
                country_name = response.country.name
                if not country_name:
                    country_name = 'Unknown'
            except (AddressNotFoundError, ValueError):
                country_name = 'Unknown'
            if country_name not in country_ips:
                country_ips[country_name] = set()
            country_ips[country_name].add(ip)
    sorted_countries = sorted(
        country_ips.items(),
        key=lambda item: len(item[1]),
        reverse=True
    )
    for country, ips in sorted_countries:
        print(f'{country}: {len(ips)}')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('ERROR: Insufficient arguments', file=sys.stderr)
        print('Usage: python geoip-log-analyzer.py <input_file> <db_path>', file=sys.stderr)
        sys.exit(1)
    try:
        analyze_logs(
            input_file=sys.argv[1],
            db_path=sys.argv[2],
        )
    except FileNotFoundError as e:
        print(f'ERROR: File not found - {e.filename}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'ERROR: An unexpected error occurred: {e}', file=sys.stderr)
        sys.exit(1)

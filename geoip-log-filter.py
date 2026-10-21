import sys
import geoip2.database
from geoip2.errors import AddressNotFoundError


def filter_logs(input_file, db_path, target_country, output_file=None):
    total_lines = 0
    target_lines = 0
    out_stream = open(output_file, 'w', encoding='utf-8') if output_file else sys.stdout
    try:
        with geoip2.database.Reader(db_path) as reader, \
             open(input_file, 'r', encoding='utf-8', errors='ignore') as in_file:
            for line in in_file:
                total_lines += 1
                clean_line = line.strip()
                if not clean_line:
                    continue
                line_parts = clean_line.split()
                if not line_parts:
                    continue
                ip = line_parts[0]
                try:
                    response = reader.country(ip)
                    country_code = response.country.iso_code
                    if country_code == target_country.upper():
                        out_stream.write(line)
                        target_lines += 1
                except (AddressNotFoundError, ValueError):
                    continue
    finally:
        if output_file:
            out_stream.close()
    print(f'\n{target_lines} out of {total_lines} requests are from {target_country}', file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('ERROR: Insufficient arguments', file=sys.stderr)
        print('Usage: geoip-log-filter.py <input_file> <db_path> <country_code> [output_file]', file=sys.stderr)
        sys.exit(1)
    out_file = sys.argv[4] if len(sys.argv) > 4 else None
    try:
        filter_logs(
            input_file=sys.argv[1],
            db_path=sys.argv[2],
            target_country=sys.argv[3],
            output_file=out_file,
        )
    except FileNotFoundError as e:
        print(f'ERROR: File not found: {e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'ERROR: An unexpected error occurred: {e}', file=sys.stderr)
        sys.exit(1)

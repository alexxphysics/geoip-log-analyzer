# GeoIP Log Analyzer

A lightweight Python script that parses server log files, extracts IP addresses, and aggregates them by country using the MaxMind GeoIP2 database. 

Results are automatically sorted from the country with the most unique IP addresses to the least.

## Important: Log Format Limitation

This script uses a simple space-separation logic and expects the **IP address to be the very first element in each log line**. 

It works out-of-the-box with standard **Nginx** access logs (Combined/Main format). If your server log format (e.g., custom Apache or JSON logs) places the IP address in a different column, you will need to modify the `ip = line_parts[0]` line in the code.

## Features

- **Unique IP Counting:** Uses Python sets to count only unique hosts per country, avoiding inflation from repetitive log lines.
- **Memory Efficient:** Processes large log files line-by-line using buffered I/O, keeping RAM usage minimal and flat regardless of file size.
- **Flexible Stream Redirection:** Works flawlessly with standard OS piping (`>`) to export data into external files.
- **Robust Parsing:** Safe file reading with encoding error handling (`errors='ignore'`).

## Requirements

- Python 3.9 or higher
- External packages listed in `requirements.txt` (contains `geoip2` and its sub-dependencies)
- MaxMind GeoIP2 Country database (e.g., the free GeoLite2 Country `.mmdb` file)

To install the dependencies, run:
```bash
pip install -r requirements.txt
```

## Usage

The script requires two arguments: the path to your log file and the path to your GeoIP `.mmdb` database.

### 1. Print output to console:
```bash
python geoip-log-analyzer.py access.log GeoLite2-Country.mmdb
```

### 2. Save output to a file:
To avoid potential encoding issues when redirecting stdout to a file on certain operating systems (like Windows), use the `-X utf8` flag:
```bash
python -X utf8 geoip-log-analyzer.py access.log GeoLite2-Country.mmdb > report.txt
```

## Example Output

```text
United States: 18
Germany: 4
Singapore: 3
China: 3
Sweden: 2
Belgium: 2
Argentina: 1
France: 1
South Korea: 1
```

## License

This project is open-source and available under the MIT License.

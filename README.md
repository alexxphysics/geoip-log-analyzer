# GeoIP Log Analyzer

A collection of lightweight Python scripts that parse server log files and extract geographical data using the MaxMind GeoIP2 database.

## Important: Log Format Limitation

These scripts use a simple space-separation logic and expect the **IP address to be the very first element in each log line**. 

It works out-of-the-box with standard **Nginx** access logs (Combined/Main format). If your server log format (e.g., custom Apache or JSON logs) places the IP address in a different column, you will need to modify the `ip = line_parts[0]` line in the code.

## Features

- **Unique IP Counting:** Uses Python sets to count only unique hosts per country, avoiding inflation from repetitive log lines.
- **Log Filtering:** Extracts complete log lines matching a specific target country code.
- **Memory Efficient:** Processes large log files line-by-line using buffered I/O, keeping RAM usage minimal and flat regardless of file size.
- **Flexible Stream Redirection:** Works flawlessly with standard OS piping (>) or built-in file writing to export data into external files.
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

### Analyzing Logs (geoip-log-analyzer.py)

Aggregates statistics and lists countries sorted from most unique IP addresses to least.

The script requires two positional arguments: the path to your log file and the path to your GeoIP .mmdb database.

#### Print output to console:
```bash
python geoip-log-analyzer.py access.log GeoLite2-Country.mmdb
```

#### Save output to a file:
To avoid potential encoding issues when redirecting stdout to a file on certain operating systems (like Windows), use the `-X utf8` flag:
```bash
python -X utf8 geoip-log-analyzer.py access.log GeoLite2-Country.mmdb > report.txt
```

#### Example Output

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

### Filtering Logs by Country (geoip-log-filter.py)

Extracts and outputs only the log lines that originated from a specific country (using two-letter ISO codes).

The script requires three positional arguments: the path to your log file, the path to your GeoIP database, and the target country code. You can optionally provide a fourth argument to save results directly to a file.

#### Print output to console:
```bash
python geoip-log-filter.py access.log GeoLite2-Country.mmdb FR
```

#### Save output to a file:
```bash
python geoip-log-filter.py access.log GeoLite2-Country.mmdb FR filtered_access.log
```

## License

This project is open-source and available under the MIT License.

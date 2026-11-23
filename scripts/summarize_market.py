"""Recompute quarterly indicators from the published daily/monthly subsets."""
import calendar
import collections
import csv
import datetime as dt
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'research' / 'market'


def quarter(date):
    return date[:4] + 'Q' + str((int(date[5:7]) - 1) // 3 + 1)


def write(name, rows):
    with (ROOT / name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def aggregate_daily(rows):
    groups = collections.defaultdict(list)
    for row in rows:
        groups[(row['metric'], row['country'], quarter(row['date']))].append(row)
    out = []
    for (metric, country, period), group in sorted(groups.items()):
        dates = sorted(row['date'] for row in group)
        last = dt.date.fromisoformat(dates[-1])
        first = dt.date(last.year, (last.month - 1) // 3 * 3 + 1, 1)
        end_month = first.month + 2
        end = dt.date(last.year, end_month, calendar.monthrange(last.year, end_month)[1])
        complete = dates[0] == first.isoformat() and last == end
        out.append({
            'metric': metric, 'country': country, 'quarter': period,
            'value': statistics.mean(float(row['value']) for row in group),
            'n_observations': len(group), 'first_date': dates[0], 'last_date': dates[-1],
            'partial_quarter': not complete,
            'aggregation': 'Arithmetic mean of published daily 7-day-trailing observations',
            'source': 'Indeed Hiring Lab',
        })
    return out


def aggregate_monthly(rows):
    groups = collections.defaultdict(list)
    for row in rows:
        groups[(row['metric'], row['country'], row['group'], quarter(row['date']))].append(row)
    out = []
    for (metric, country, size, period), group in sorted(groups.items()):
        dates = sorted(row['date'] for row in group)
        out.append({
            'metric': metric, 'country': country, 'group': size, 'quarter': period,
            'value_pct': statistics.mean(float(row['value_pct']) for row in group),
            'n_months': len(group), 'last_date': dates[-1],
            'partial_quarter': len(set(dates)) < 3,
            'aggregation': 'Unweighted mean of published monthly YoY rates; not quarter-on-quarter growth',
            'source': 'LinkedIn Economic Graph',
        })
    return out


def main():
    with (ROOT / 'indeed-daily-subset.csv').open() as f:
        daily = aggregate_daily(list(csv.DictReader(f)))
    with (ROOT / 'linkedin-monthly-subset.csv').open() as f:
        monthly = aggregate_monthly(list(csv.DictReader(f)))
    write('indeed-quarterly.csv', daily)
    write('linkedin-quarterly.csv', monthly)
    print(f'Aggregated {len(daily)} Indeed and {len(monthly)} LinkedIn quarterly observations.')


if __name__ == '__main__':
    main()

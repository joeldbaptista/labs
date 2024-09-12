"""
This script creates a theoretical demand curve
"""
import json
import yaml
import argparse
import logging
import numpy as np
import scipy.stats as stats
import typing as t
import datetime as dt
import matplotlib.pyplot as plt


GAP = 10

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%y-%m-%d %H:%M:%S", 
    level=logging.INFO,
)


def error(msg: str, exit_code: int=1):
    """
    Logs an error with message `msg`, and exits the script with code `exit_code`
    """
    logging.error(msg)
    exit(exit_code)


def info(msg: str):
    """
    Logs an info with message `msg`
    """
    logging.info(msg)


def read_yaml(fname: str) -> t.Dict:
    """
    Reads the yaml in `fname` and returns its content in a dictionary
    """
    try:
        with open(fname, mode="r", encoding="UTF-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError as err:
        raise Exception(err) from err
    except yaml.YAMLError as err:
        raise Exception(err) from err


def write_json(data: t.Dict|t.List, fname: str, indent:int=4):
    """
    Writes data to a json
    """
    try:
        with open(fname, mode="w", encoding="UTF-8") as f:
            return json.dump(data, f, indent=indent)
    except Exception as err:
        raise Exception(err) from err


def get_argsparser() -> argparse.ArgumentParser:
    """
    Returns the CLI arguments

    Returns:
        argparse.ArgumentParser object
    """
    parser = argparse.ArgumentParser(
        description="Parses arguments for the demand curves simulator"
    )
    parser.add_argument(
        "--config", type=str, required=True, help="The mandatory configuration YAML file"
    )
    parser.add_argument(
        "--bsize", type=int, required=False, default=1, help="The size of the time bucket in minutes; default, 1 min"
    )
    parser.add_argument(
        "--create_plot", action="store_true", help="Create or not a plot"
    )
    parser.add_argument(
        "--outfile", type=str, required=True, help="The mandatory output file"
    )
    return parser


def probability_in_normal(
    loc: float, scale: float, t0: float, t1: float,
) -> float:
    """
    Returns the dP (probability) of an event in the interval [t0, t1[ assuming
    a normal distribution N(loc, scale).

    Args:
        loc (float): the location of the center of mass, aka the mean
        scale (float): the scale of the Normal distribution, aka standard-deviation
        t0 (float): the lower bound 
        t1 (float): the upper bound

    Returns:
        the probability of an event in the interval [t0, t1[
    """
    if t0 > t1:
        t0, t1 = t1, t0
    # Calculate the accumulative probability for each point
    cdf_t0 = stats.norm.cdf(x=t0, loc=loc, scale=scale)
    cdf_t1 = stats.norm.cdf(x=t1, loc=loc, scale=scale)
    return cdf_t1 - cdf_t0 # dP


def divide_time_axis(bsize:int=1) -> t.List[t.Tuple[dt.timedelta, dt.timedelta]]:
    """
    Generates a list of time buckets of size `bsize` minutes.
    """
    hour_0 = dt.timedelta(days=0, hours=0)
    hour_24 = dt.timedelta(days=1, hours=0)
    time_step = dt.timedelta(minutes=bsize)
    current_hour = hour_0
    time_buckets = []
    while current_hour < hour_24:
        next_hour = current_hour + time_step
        # To guarantee high bound of the last bucket 
        # does not exceeds the 24h.
        if next_hour > hour_24:
            next_hour = hour_24
        time_buckets.append((current_hour, next_hour)) 
        current_hour = next_hour
    return time_buckets


def format_timedelta(t0: dt.timedelta) -> str:
    """
    Returns the formated string for timedelta
    """
    total_seconds = int(t0.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60) 
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def convert_timedelta_to_decimal(t0: dt.timedelta) -> float:
    """
    Converts the timedelta object `t0` to decimal
    """
    total_seconds = int(t0.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    return hours + remainder/3600.0


def validate_args(parser: argparse.ArgumentParser) -> t.Tuple:
    """
    Validates the arguments
    """
    args = parser.parse_args()
    config = args.config
    bsize = args.bsize
    create_plot = args.create_plot
    outfile = args.outfile
    if bsize <= 0:
        error("bsize cannot be <= 0")
    return config, bsize, create_plot, outfile


def plot_demand_curve(
    timedeltas: t.List[dt.timedelta], counts: t.List[int], plot_file: str,
):
    """
    Plots the demand curve
    """
    seconds = [td.total_seconds() for td in timedeltas]
    plt.figure(figsize=(15, 11))
    plt.plot(seconds, counts,linestyle='-', color='b')
    two_hour_intervals = [
        td 
        for td in seconds 
        if dt.timedelta(seconds=td).seconds % (2 * 3600) == 0
    ]
    tick_labels = [
        str(dt.timedelta(seconds=int(sec))) 
        for sec in two_hour_intervals
    ]
    plt.xticks(two_hour_intervals, tick_labels, rotation=45)
    plt.xlabel("time")
    plt.ylabel("N. of events")
    plt.title("Demand curve")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plot_file, format="png")
    plt.close()
   

def main(config: str, bsize: int, outfile: str, create_plot: bool):
    """ Entry point """
    try:
        config = read_yaml(config)
        peaks = config.get("peaks")
        if peaks:
            out = []
            total = 0
            info(f"Start - Simulate events")
            for t0, t1 in divide_time_axis(bsize=bsize):
                dt0 = convert_timedelta_to_decimal(t0)
                dt1 = convert_timedelta_to_decimal(t1)
                exp_nevents = 0 # expected number of events
                for peak in peaks:
                    prob = probability_in_normal(
                        loc=peak["location"], scale=peak["scale"], t0=dt0, t1=dt1
                    )
                    nevents = int(peak["nevents"]*prob)
                    total += nevents
                    if nevents > 0:
                        low = nevents if nevents-GAP < 0 else nevents-GAP
                        high = nevents + GAP
                        exp_nevents += np.random.randint(low=low, high=high)
                out.append((t0, t1, exp_nevents))
            if create_plot:
                info("Creating plot as requested")
                plot_file = outfile.split(".")[0] + ".png"
                t0s, counts = [], []
                for t0, _, count in out:
                    t0s.append(t0)
                    counts.append(count)
                plot_demand_curve(t0s, counts, plot_file)
            write_json(
                fname=outfile,
                data=[
                    {
                        "t0": format_timedelta(t0), 
                        "t1": format_timedelta(t1), 
                        "nevents": counts,
                    }
                    for t0, t1, counts in out
                ], 
            )            
            info(f"Done - Total number of events: {total}")
        else:
            error("Configuration file without peaks")
    except Exception as err:
        error(err)


if __name__ == "__main__":
    """
    Example of usage:
    $ python3 demand_curves.py --bsize=5 --config=./examples/pizzaria.yml --outfile=theoretical-demand-curve.json
    """
    parser = get_argsparser()
    config, bsize, create_plot, outfile = validate_args(parser)
    main(config=config, bsize=bsize, create_plot=create_plot, outfile=outfile)



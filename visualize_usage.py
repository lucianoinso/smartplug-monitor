import sys

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def preprocess(df):
    # Fill the seconds which couldn't be measured, with the last measured value
    df = df.resample("1s").ffill()

    # Compute energy per second (Wh = W * sec / 3600, then / 1000 for kWh)
    df["energy_kWh"] = df["power"] / 3600000

    # Total consumption
    total_kWh = df["energy_kWh"].sum()

    print(f"Total energy consumed: {total_kWh:.6f} kWh")
    df["cumulative_kWh"] = df["energy_kWh"].cumsum()
    df["status"] = df["power"] != 0

    # Group consecutive ON/OFF segments
    df["group"] = (df["status"] != df["status"].shift()).cumsum()

    return df


def visualize(df, tick_range_minutes):
    fig, (ax2, ax3, ax4, ax1) = plt.subplots(
        nrows=4, ncols=1, sharex=True, figsize=(15, 9)
    )

    ax1.set_ylabel("Cumulative (kWh)")
    ax1.plot(df.index, df["cumulative_kWh"],
             color="green", linewidth=0, marker='.', markersize=1,
             label="Cumulative (kWh)")

    ax3.set_ylabel("Power (W)")
    ax3.step(df.index, df["power"],
             color="yellowgreen", linewidth=1, marker='.', markersize=0,
             label="Power (W)")

    ax2.set_ylabel("Voltage (V)")

    ax2.plot(df.index, df["voltage"],
             color="lightblue", linewidth=1, marker='.', markersize=1,
             label="Voltage (V)")

    ax4.set_ylabel("Status (ON/OFF)")
    ax4.tick_params(axis='y')
    ax4.set_yticks([0, 1])
    ax4.set_yticklabels(["OFF", "ON"])
    ax4.set_ylim(-0.2, 1.3)

    df_on = df[df["status"] == 1]
    df_off = df[df["status"] == 0]

    ax4.plot(df_on.index, df_on["status"],
             color="red", linewidth=0, marker='.', markersize=4,
             label="ON")

    ax4.plot(df_off.index, df_off["status"],
             color="blue", linewidth=0, marker='.', markersize=4,
             label="OFF")

    grouped = df.groupby("group").agg({
        "status": "first",
    })

    # Calculate the full duration of each segment
    grouped["duration"] = df.groupby("group").apply(
        lambda g: (g.index[-1] - g.index[0]).seconds / 60,
        include_groups=False)

    # Calculate the middle time of each segment to add labels to the plot later
    grouped["mid_time"] = df.groupby("group").apply(
        lambda g: g.index[len(g) // 2],
        include_groups=False)

    # Add confidence and duration labels
    for _, row in grouped.iterrows():
        x = row["mid_time"]
        y = row["status"]
        duration = row["duration"]
        # label = f'{duration:.1f} min'
        label = f'{duration:.1f}\nmin'
        ax4.text(x, y + 0.05, label, ha="center", va="bottom", fontsize=8)

    start_time = df.index.min() + pd.Timedelta(minutes=-5)
    end_time = df.index.max() + pd.Timedelta(minutes=5)

    for ax in (ax1, ax3, ax2, ax4):
        ax.set_xlim(start_time, end_time)
        ax.set_xlabel("Time")
        ax.legend()
        ax.xaxis.set_major_locator(mdates.MinuteLocator(
                                    byminute=range(0, 60, tick_range_minutes)))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.grid(True, linestyle="--", alpha=0.4)
        for label in ax.get_xticklabels():
            label.set_rotation(80)
            label.set_fontsize(8)

    current_date = df.index.min().strftime("%Y-%m-%d")
    plt.suptitle(f"Device Energy Profile ({current_date})")
    plt.tight_layout()
    plt.show()


def main():
    if len(sys.argv) < 2:
        print("Usage: python visualize_usage.py <filename>")
        sys.exit(1)

    filename = f"logs/{sys.argv[1]}"

    df = pd.read_csv(filename, parse_dates=["timestamp"], index_col="timestamp")
    df = preprocess(df)
    visualize(df, tick_range_minutes=15)


if __name__ == '__main__':
    main()

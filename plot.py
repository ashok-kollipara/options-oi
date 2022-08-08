#!/usr/bin/env python

import tkinter as tk
import matplotlib.pyplot as plt
import json

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

filename = "option_chain.json"
atm = 0


def plot_open_interest_data(
    spot, strikes, expiry_list, expiry, index, container_window
):

    global atm
    content = {}

    with open(filename, "r") as json_file:

        content = json.load(json_file)

    index_dict = {
        "NIFTY": {"slicer": 25, "lot_size": 50},
        "BANKNIFTY": {"slicer": 100, "lot_size": 25},
        "USDINR": {
            "slicer": 0.1250,
            "lot_size": 1,
        },  #  USDINR is leveraged for 1000 USD for 1 Qty
    }

    atm_slicer = index_dict[index]["slicer"]
    lot_size = index_dict[index]["lot_size"]

    f_strikes = []
    call_oi = []
    put_oi = []
    call_change_oi = []
    put_change_oi = []

    for item in strikes:
        if abs(item - spot) < atm_slicer:
            atm = item

    # os.system("cls")
    print(f"{index} Spot is : {spot}")
    print(f"{index} ATM strike is : {atm}")
    # print(strikes)

    for item in content["records"]["data"]:

        if item["strikePrice"] in strikes:

            if item["expiryDate"] == expiry:

                # check for strikes
                f_strikes.append(item["strikePrice"])

                # Check and add Call OI, Call OI change
                if "CE" in item.keys():
                    call_oi.append(item["CE"]["openInterest"])
                    call_change_oi.append(item["CE"]["changeinOpenInterest"])
                else:
                    call_oi.append(0)
                    call_change_oi.append(0)

                # Check and add Put OI
                if "PE" in item.keys():
                    put_oi.append(item["PE"]["openInterest"])
                    put_change_oi.append(item["PE"]["changeinOpenInterest"])
                else:
                    put_oi.append(0)
                    put_change_oi.append(0)

            else:
                pass

        else:
            print("fail")

    atm_oi_yval = max(max(call_oi), max(put_oi))
    atm_change_oi_yval = max(max(call_change_oi), max(put_change_oi))

    # Contract values calculation in million
    calls = round(lot_size * sum(call_oi) / 1000000, 2)
    puts = round(lot_size * sum(put_oi) / 1000000, 2)
    calls_change = round(lot_size * sum(call_change_oi) / 1000000, 2)
    puts_change = round(lot_size * sum(put_change_oi) / 1000000, 2)

    # Plotting Begins here
    # splitting into subplots with shared strike price x-axis
    fig, axs = plt.subplots(2, 1, sharex=True)

    canvas = FigureCanvasTkAgg(fig, master=container_window)
    canvas.draw()

    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, container_window)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # plotting OI and atm strike as a subplot
    axs[0].bar(
        f_strikes,
        call_oi,
        color="green",
        width=45,
        edgecolor="black",
        linewidth=1,
        label=f"CALL OI : {calls}M",
    )
    axs[0].bar(
        f_strikes,
        put_oi,
        color="red",
        width=30,
        edgecolor="black",
        linewidth=1,
        label=f"PUT OI : {puts}M",
    )
    axs[0].bar(
        atm,
        (atm_oi_yval + 10000),
        color="blue",
        label=f"ATM Strike {atm}",
        linestyle="dashed",
        linewidth=1,
        width=7,
    )
    axs[0].annotate(f"ATM Strike {atm}", xy=(atm + 50, atm_oi_yval), xycoords="data")
    axs[0].set_title(f"{index} Open Interest")

    # plotting change in OI and atm strike as another sub plot
    axs[1].bar(
        f_strikes,
        call_change_oi,
        color="green",
        width=45,
        edgecolor="black",
        linewidth=1,
        label=f"CALL OI change : {calls_change}M",
    )
    axs[1].bar(
        f_strikes,
        put_change_oi,
        color="red",
        width=30,
        edgecolor="black",
        linewidth=1,
        label=f"PUT OI change : {puts_change}M",
    )
    axs[1].bar(
        atm,
        (atm_change_oi_yval + 2000),
        color="blue",
        label=f"ATM Strike {atm}",
        linestyle="dashed",
        linewidth=1,
        width=7,
    )
    axs[1].annotate(
        f"ATM Strike {atm}", xy=(atm + 50, atm_change_oi_yval), xycoords="data"
    )
    # axs[1].annotate(f'Calls : {(lot_size*sum(call_change_oi)/1000000)}M \n Puts : {(lot_size*sum(put_change_oi)/1000000)}M',xy=(atm+100, atm_change_oi_yval-10000),xycoords='data')
    axs[1].set_title(f"{index} Change in Open Interest")

    # show legends for the plot
    axs[0].legend()
    axs[1].legend()

    # Define the size of window or frame
    container_window.geometry("1200x800")

    def destroyer():
        container_window.quit()
        container_window.destroy()
    
    # Destroy windows on main window close detection and exit python
    container_window.wm_protocol ("WM_DELETE_WINDOW",destroyer)
    
    # function to show the plot
    # plt.show()

    return

import requests
import json
import matplotlib.pyplot as plt
import time
import tkinter as tk
import os

#  Check for the Operating system type and clear the stdout/terminal screen
#  and issue corresponding command for the Operating system
if os.name == "posix":
    os.system("clear")
else:
    os.system("cls")

#  Get the data from NSE website in JSON and dump it to readable json file


def get_OC_json(url, filename):

    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)

    content = r.json()

    with open(filename, "w") as f:

        json.dump(content, f, indent=4)

    time.sleep(5)


def filter_chain(filename, atm_slicer, ind):

    # Create an instance of tkinter frame
    win = tk.Tk()

    # Define the size of window or frame
    win.geometry("715x250")

    win.eval("tk::PlaceWindow . center")

    w = tk.Label(
        win, text="Open interest analysis from Option chain API", font="50", fg="blue"
    )
    w.pack()

    expiry_list = []
    strikes = []

    with open(filename, "r") as f:

        content = json.load(f)

    # get strikes, Spot and ATM strike
    # underlying value is given as float in NIFTY,BANKNIFTY api and as text in USDINR api
    spot = float(content["records"]["underlyingValue"])
    strikes = content["records"]["strikePrices"]
    expiry_list = content["records"]["expiryDates"]

    s = tk.Label(win, text=f"{ind} Spot : {spot}", font="50", fg="brown")
    s.pack()

    def selected():

        f_strikes = []
        call_oi = []
        put_oi = []
        call_change_oi = []
        put_change_oi = []

        expiry = menu.get()

        for item in strikes:
            if abs(item - spot) < atm_slicer:
                atm = item

        os.system("cls")
        print(f"{ind} Spot is : {spot}")
        print(f"{ind} ATM strike is : {atm}")
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
        calls = round(50 * sum(call_oi) / 1000000, 2)
        puts = round(50 * sum(put_oi) / 1000000, 2)
        calls_change = round(50 * sum(call_change_oi) / 1000000, 2)
        puts_change = round(50 * sum(put_change_oi) / 1000000, 2)

        # splitting into subplots with shared strike price x-axis
        fig, axs = plt.subplots(2, 1, sharex=True)

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
        axs[0].annotate(
            f"ATM Strike {atm}", xy=(atm + 50, atm_oi_yval), xycoords="data"
        )
        axs[0].set_title(f"{ind} Open Interest")

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
        # axs[1].annotate(f'Calls : {(50*sum(call_change_oi)/1000000)}M \n Puts : {(50*sum(put_change_oi)/1000000)}M',xy=(atm+100, atm_change_oi_yval-10000),xycoords='data')
        axs[1].set_title(f"{ind} Change in Open Interest")

        # show legends for the plot
        axs[0].legend()
        axs[1].legend()

        # function to show the plot
        plt.show()

    # Set the Menu initially
    menu = tk.StringVar()
    menu.set("Select Expiry Date")

    # Create a dropdown Menu
    drop = tk.OptionMenu(win, menu, *expiry_list)
    drop.config(bg="lightblue")
    drop.pack()

    load_button = tk.Button(win, text="Load", command=selected)
    load_button.pack()

    win.mainloop()

    return


if __name__ == "__main__":

    print("Enter : 1 for NIFTY")
    print("Enter : 2 for BANKNIFTY")
    # print("Enter : 3 for USDINR")

    atm_slicer = 0
    ind, ind_type = "", ""

    p = int(input("Choose the index for option chain : ").strip())

    if p == 1:
        ind = "NIFTY"
        atm_slicer = 25
        ind_type = "indices"
    elif p == 2:
        ind = "BANKNIFTY"
        atm_slicer = 100
        ind_type = "indices"
    elif p == 3:
        ind = "USDINR"
        atm_slicer = 0.1250
        ind_type = "currency"

    # paste api url
    url = f"https://www.nseindia.com/api/option-chain-{ind_type}?symbol={ind}"

    # working with stored file
    filename = "option_chain.json"

    get_OC_json(url, filename)

    filter_chain(filename, atm_slicer, ind)

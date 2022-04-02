# NSE Options Open Interest Analysis using Python
The aim of this project is to able to fetch the Option chain data available from NSE API and use it to plot open interest data for analysis.

**Why do this when there are so many alternatives ?**

1. Showcase my python skills learnt during sabbatical
2. Opstra free account OI data is 15 mins delayed
3. Didnot want to pay :) for this service
4. Work with slowest internet connection
5. Provides ability to use and make data as per my usage

## Getting Started

**Step 1: Clone** 

Clone the project/repository into desired folder

```
git clone https://github.com/ashok-kollipara/options-oi.git

```

**Step 2. Get Python**

> Python 3.10.x (Tested) 

```
https://www.python.org/downloads/
```

Setup help for windows ( environment variables and MAX PATH limitations)

```
https://docs.python.org/3/using/windows.html
```
Most Linux distributions have python installed by default

**Step 3. Install required Python packages**
 
```
pip install -r requirements.txt
```

## Usage

**Step A : Launch program**

In case python is added to environment variables it can be directly used in command line at any folder level. 

Navigate into the folder in which the repo is cloned

```
python main.py
```

![Step A](/docs/1_start.PNG)

**Step B : Main Window**

If everything is done perfectly so far there will be a window that appears as below

![Step B](/docs/2_main_window.PNG)

**Step C : Choose Index**

Choose the index by clicking and selecting from available dropdown

![Step C](/docs/3_Indexchoice.png)

**Step D : Load Index**

Press Load Button Below as indicated in image

![Step D](/docs/4_LoadIndex.png)

**Step E : Auto Download Index Option Chain**

In background program fetches the optiona data from API

![Step E](/docs/5_Loadingdata.png)

**Step F : Expiry Screen**

Window will update to show the spot value of selected index in previous steps and present dropdown to select the expiry date to load 

![Step F](/docs/6_Expiryscreen.PNG)

**Step G : Choose Expiry Data**

Choose the expiry date by clicking and selecting from available dropdown

![Step G](/docs/7_ChooseExpiry.png)

**Step H : Load Expiry Data**

Press Load Button Below as indicated in image

![Step H](/docs/8_LoadExpirydata.PNG)

**Final Step : Open Interest data is plotted**

Open Interest data for selected Index and Expiry date is presented with resized screen for study

![OI_Plot](/docs/9_FinalPlotOI.png)

## Whats Next ?

1. Add functionality to change indexes and expiry dates without relaunching program
2. Add time and date
3. Ability to refresh by click / (Auto refresh every 5 mins)

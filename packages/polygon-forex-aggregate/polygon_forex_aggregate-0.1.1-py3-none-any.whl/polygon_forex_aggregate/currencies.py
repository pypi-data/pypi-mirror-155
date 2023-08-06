# The following 10 blocks of code define the classes for storing the the return data, for each
# currency pair.
from math import isnan
from math import sqrt
from math import floor
# from sqlalchemy import create_engine
from sqlalchemy import text
import datetime

# Define the USDINR_return class - each instance will store one row from the dataframe
class currency_return(object):
    """
    Define the generic class - each instance will store one row from the dataframe
    :param curr_from: currency conversion from
    :param curr_to: currency conversion to
    :param tick_time: time for the average price
    :param avg_price: average price for this currency pair
    :type   avg_price: float
    :type   curr_from: string
    :type   curr_to: string
    :type tick_time: int
    """
    curr_from = ""
    curr_to = ""
    # Variable to store the total number of instantiated objects in this class
    num = 0
    # Variable to store the running sum of the return
    run_sum = 0
    run_squared_sum = 0
    run_sum_of_std = 0
    last_price = -1

    # Init all the necessary variables when instantiating the class
    def __init__(self, curr_from, curr_to, tick_time, avg_price):
        self.curr_from = curr_from
        self.curr_to = curr_to
        # Store each column value into a variable in the class instance
        self.tick_time = tick_time
        # self.price = avg_price

        if currency_return.last_price == -1:
            hist_return = float('NaN')
        else:
            hist_return = (avg_price - currency_return.last_price) / currency_return.last_price

        self.hist_return = hist_return
        if isnan(hist_return):
            currency_return.run_sum = 0
        else:
            # Increment the counter
            if currency_return.num < 5:
                currency_return.num += 1
            currency_return.run_sum += hist_return
        currency_return.last_price = avg_price

    def add_to_running_squared_sum(self, avg):
        if isnan(self.hist_return) == False:
            currency_return.run_squared_sum += (self.hist_return - avg) ** 2

    def get_avg(self, pop_value):
        if isnan(self.hist_return) == False:
            currency_return.run_sum -= pop_value
            avg = currency_return.run_sum / (currency_return.num)
            self.avg_return = avg
            return avg

    def get_std(self):
        if isnan(self.hist_return) == False:
            std = sqrt(currency_return.run_squared_sum / (currency_return.num))
            self.std_return = std
            currency_return.run_sum_of_std += std
            currency_return.run_squared_sum = 0
            return std

    def get_avg_std(self, pop_value):
        if isnan(self.hist_return) == False:
            currency_return.run_sum_of_std -= pop_value
            avg_std = currency_return.run_sum_of_std / (currency_return.num)
            self.avg_of_std_return = avg_std
            return avg_std

# We can buy, sell, or do nothing each time we make a decision.
# This class defies a nobject for keeping track of our current investments/profits for each currency pair
class portfolio(object):
    """
    A portfolio object that can take a currency pair and store them

    :param from_: currency in three letter format. like USD or INR
    :param    to: currency in three letter format. like USD or INR
    :type from_: string
    :type   to: string
    """
    def __init__(self, from_, to):
        # Initialize the 'From' currency amont to 1
        self.amount = 1
        self.curr2 = 0
        self.from_ = from_
        self.to = to
        # We want to keep track of state, to see what our next trade should be
        self.Prev_Action_was_Buy = False

    # This defines a function to buy the 'To' currency. It will always buy the max amount, in whole number
    # increments
    def buy_curr(self, price):
        if self.amount >= 1:
            num_to_buy = floor(self.amount)
            self.amount -= num_to_buy
            self.Prev_Action_was_Buy = True
            self.curr2 += num_to_buy * price
            print(
                "Bought %d worth of the target currency (%s). Our current profits and losses in the original currency (%s) are: %f." % (
                num_to_buy, self.to, self.from_, (self.amount - 1)))
        else:
            print("There was not enough of the original currency (%s) to make another buy." % self.from_)

    # This defines a function to sell the 'To' currency. It will always sell the max amount, in a whole number
    # increments
    def sell_curr(self, price):
        if self.curr2 >= 1:
            num_to_sell = floor(self.curr2)
            self.amount += num_to_sell * (1 / price)
            self.Prev_Action_was_Buy = False
            self.curr2 -= num_to_sell
            print(
                "Sold %d worth of the target currency (%s). Our current profits and losses in the original currency (%s) are: %f." % (
                num_to_sell, self.to, self.from_, (self.amount - 1)))
        else:
            print("There was not enough of the target currency (%s) to make another sell." % self.to)

# Function slightly modified from polygon sample code to format the date string
def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M:%S')


# Function which clears the raw data tables once we have aggregated the data in a 6 minute interval
def reset_raw_data_tables(engine, currency_pairs):
    with engine.begin() as conn:
        for curr in currency_pairs:
            conn.execute(text("DROP TABLE " + curr[0] + curr[1] + "_raw;"))
            conn.execute(
                text("CREATE TABLE " + curr[0] + curr[1] + "_raw(ticktime text, fxrate  numeric, inserttime text);"))


# This creates a table for storing the raw, unaggregated price data for each currency pair in the SQLite database
def initialize_raw_data_tables(engine, currency_pairs):
    with engine.begin() as conn:
        for curr in currency_pairs:
            conn.execute(
                text("CREATE TABLE " + curr[0] + curr[1] + "_raw(ticktime text, fxrate  numeric, inserttime text);"))


# This creates a table for storing the (6 min interval) aggregated price data for each currency pair in the SQLite database
def initialize_aggregated_tables(engine, currency_pairs):
    with engine.begin() as conn:
        for curr in currency_pairs:
            conn.execute(text(
                "CREATE TABLE " + curr[0] + curr[1] + "_agg(inserttime text, avgfxrate  numeric, stdfxrate numeric, maxfxrate numeric, minfxrate numeric, volfxrate numeric, fdfxrate numeric);"))


# This function is called every 6 minutes to aggregate the data, store it in the aggregate table,
# and then delete the raw data
def aggregate_raw_data_tables(engine, currency_pairs):
    with engine.begin() as conn:
        for curr in currency_pairs:
            result = conn.execute(
                text("SELECT AVG(fxrate) as avg_price, COUNT(fxrate) as tot_count FROM " + curr[0] + curr[1] + "_raw;"))
            for row in result:
                avg_price = row.avg_price
                tot_count = row.tot_count

            result = conn.execute(
                text("SELECT MAX(fxrate) as max_price, COUNT(fxrate) as tot_count FROM " + curr[0] + curr[1] + "_raw;"))
            for row in result:
                max_price = row.max_price

            result = conn.execute(
                text("SELECT MIN(fxrate) as min_price, COUNT(fxrate) as tot_count FROM " + curr[0] + curr[1] + "_raw;"))
            for row in result:
                min_price = row.min_price

            vol_price = max_price - min_price

            result = conn.execute(
                text("SELECT COUNT(avgfxrate) as agg_count FROM " + curr[0] + curr[1] + "_agg;"))
            for row in result:
                agg_count = row.agg_count

            FD = 0
            if agg_count > 20:
                result = conn.execute(
                    text("SELECT avgfxrate as EMA, volfxrate as VOL FROM " + curr[0] + curr[1] + "_agg;"))
                results_ema = []
                results_vol = []
                for row in result:
                    results_ema.append(row.EMA)
                    results_vol.append(row.VOL)
                EMA = results_ema[-1]
                VOL = results_vol[-1]
                KCUB_list = []
                KCLB_list = []
                for i in range(1, 101):
                    KCUB = EMA + i*0.025*VOL
                    KCLB = EMA - i*0.025*VOL
                    KCUB_list.append(KCUB)
                    KCLB_list.append(KCLB)

                result = conn.execute(
                    text("SELECT fxrate as rate FROM " + curr[0] + curr[1] + "_raw;"))
                for row in result:
                    price = row.rate
                    if price > KCUB_list[0] or price < KCLB_list[0]:
                        FD += 1



            std_res = conn.execute(text(
                "SELECT SUM((fxrate - " + str(avg_price) + ")*(fxrate - " + str(avg_price) + "))/(" + str(
                    tot_count) + "-1) as std_price FROM " + curr[0] + curr[1] + "_raw;"))
            for row in std_res:
                std_price = sqrt(row.std_price)
            date_res = conn.execute(text("SELECT MAX(ticktime) as last_date FROM " + curr[0] + curr[1] + "_raw;"))
            for row in date_res:
                last_date = row.last_date



            conn.execute(text("INSERT INTO " + curr[0] + curr[
                1] + "_agg (inserttime, avgfxrate, stdfxrate, minfxrate, maxfxrate, volfxrate, fdfxrate) VALUES (:inserttime, :avgfxrate, :stdfxrate, :minfxrate, :maxfxrate, :volfxrate, :fdfxrate);"),
                         [{"inserttime": last_date, "avgfxrate": avg_price, "stdfxrate": std_price, "minfxrate":min_price, "maxfxrate":max_price, "volfxrate":vol_price, "fdfxrate":FD}])

            # This calculates and stores the return values
            # exec("curr[2].append(" + curr[0] + curr[1] + "_return(last_date,avg_price))")
            curr[2].append(currency_return(curr[0], curr[1], last_date, avg_price))
            # exec("print(\"The return for "+curr[0]+curr[1]+" is:"+str(curr[2][-1].hist_return)+" \")")

            if len(curr[2]) > 5:
                try:
                    avg_pop_value = curr[2][-6].hist_return
                except:
                    avg_pop_value = 0
                if isnan(avg_pop_value) == True:
                    avg_pop_value = 0
            else:
                avg_pop_value = 0
            # Calculate the average return value and print it/store it
            curr_avg = curr[2][-1].get_avg(avg_pop_value)
            # exec("print(\"The average return for "+curr[0]+curr[1]+" is:"+str(curr_avg)+" \")")

            # Now that we have the average return, loop through the last 5 rows in the list to start compiling the
            # data needed to calculate the standard deviation
            for row in curr[2][-5:]:
                row.add_to_running_squared_sum(curr_avg)

            # Calculate the standard dev using the avg
            curr_std = curr[2][-1].get_std()
            # exec("print(\"The standard deviation of the return for "+curr[0]+curr[1]+" is:"+str(curr_std)+" \")")

            # Calculate the average standard dev
            if len(curr[2]) > 5:
                try:
                    pop_value = curr[2][-6].std_return
                except:
                    pop_value = 0
            else:
                pop_value = 0
            curr_avg_std = curr[2][-1].get_avg_std(pop_value)
            # exec("print(\"The average standard deviation of the return for "+curr[0]+curr[1]+" is:"+str(curr_avg_std)+" \")")

            # -------------------Investment Strategy-----------------------------------------------
            try:
                return_value = curr[2][-1].hist_return
            except:
                return_value = 0
            if isnan(return_value) == True:
                return_value = 0

            try:
                return_value_1 = curr[2][-2].hist_return
            except:
                return_value_1 = 0
            if isnan(return_value_1) == True:
                return_value_1 = 0

            try:
                return_value_2 = curr[2][-3].hist_return
            except:
                return_value_2 = 0
            if isnan(return_value_2) == True:
                return_value_2 = 0

            try:
                upp_band = curr[2][-1].avg_return + (1.5 * curr[2][-1].std_return)
                if return_value >= upp_band and curr[
                    3].Prev_Action_was_Buy == True and return_value != 0:  # (return_value > 0) and (return_value_1 > 0) and
                    curr[3].sell_curr(avg_price)
            except:
                pass

            try:
                loww_band = curr[2][-1].avg_return - (1.5 * curr[2][-1].std_return)
                if return_value <= loww_band and curr[
                    3].Prev_Action_was_Buy == False and return_value != 0:  # and  (return_value < 0) and (return_value_1 < 0)
                    curr[3].buy_curr(avg_price)
            except:
                pass





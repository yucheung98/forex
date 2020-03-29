import MetaTrader5 as mt5

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# get all symbols
symbols = mt5.symbols_get()
print('Symbols: ', len(symbols))
count = 0
# display the first five ones
for s in symbols:
    count += 1
    print("{}. {}".format(count, s.name))
    if count == 5: break
print()

# # get symbols containing RU in their names
# ru_symbols = mt5.symbols_get("*RU*")
# print('len(*RU*): ', len(ru_symbols))
# for s in ru_symbols:
#     print(s.name)
# print()

# get the number of financial instruments
symbols = mt5.symbols_total()
if symbols > 0:
    print("Total symbols =", symbols)
else:
    print("symbols not found")

# attempt to enable the display of the EURJPY symbol in MarketWatch
selected = mt5.symbol_select("EURJPY", True)
if not selected:
    print("Failed to select EURJPY")
    mt5.shutdown()
    quit()

# display EURJPY symbol properties
symbol_info = mt5.symbol_info("EURJPY")
if symbol_info != None:
    # display the terminal data 'as is'
    print(symbol_info)
    print("EURJPY: spread =", symbol_info.spread, "  digits =", symbol_info.digits)
    # display symbol properties as a list
    print("Show symbol_info(\"EURJPY\")._asdict():")
    symbol_info_dict = mt5.symbol_info("EURJPY")._asdict()
    for prop in symbol_info_dict:
        print("  {}={}".format(prop, symbol_info_dict[prop]))



# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
from statsmodels.tsa.stattools import adfuller

class Data_Evaluator:

    def print_adfuller_stats(self, col):
        test_results = adfuller(col)

        print(f"ADF test statistic: {test_results[0]}")
        print(f"p-value: {test_results[1]}")
        print("Critical thresholds:")

        for key, value in test_results[4].items():
            print(f"\t{key}: {value}")

        print("")



"""Forecasting utilities (ARIMA-based trend prediction)."""

from ._deps import ARIMA, adfuller, np, pd, require_analysis_deps


class TrendPredictor:
    def __init__(
        self,
        market_trend_df,
        date_col,
        smoothed_avg_col,
        rise_label="上升",
        fall_label="下滑",
        flat_label="横盘",
        freq="B",
        order=None,
        steps=7,
        sortdata="逆序",
    ):
        require_analysis_deps("numpy", "pandas", "statsmodels")
        self.market_trend_df = market_trend_df.copy()
        self.date_col = date_col
        self.smoothed_avg_col = smoothed_avg_col
        self.rise_label = rise_label
        self.fall_label = fall_label
        self.flat_label = flat_label
        self.freq = freq
        self.order = order if order else (5, 1, 0)
        self.steps = steps
        self.sortdata = sortdata
        self._prepare_data()

    def _prepare_data(self):
        if self.sortdata == "逆序":
            self.reversed_market_trend_df = self.market_trend_df[self.smoothed_avg_col][::-1].reset_index(drop=True)
        else:
            self.reversed_market_trend_df = self.market_trend_df[self.smoothed_avg_col].reset_index(drop=True)

        self.market_trend_df["趋势"] = self.market_trend_df[self.smoothed_avg_col].diff().apply(
            lambda x: self.rise_label if x > 0 else (self.fall_label if x < 0 else self.flat_label)
        )
        self.is_stationary = self._check_stationarity(self.reversed_market_trend_df)

    def _check_stationarity(self, series):
        result = adfuller(series.dropna())
        return result[1] <= 0.05

    def original_data(self):
        return self.market_trend_df

    def _highlight_color(self, val):
        if val == self.rise_label:
            color = "crimson"
        elif val == self.fall_label:
            color = "forestGreen"
        else:
            color = "black"
        return f"color: {color}"

    def _predict(self):
        model = ARIMA(self.reversed_market_trend_df, order=self.order)
        model_fit = model.fit()

        forecast_result = model_fit.forecast(steps=self.steps, alpha=0.05)
        forecast = forecast_result.tolist() if isinstance(forecast_result, np.ndarray) else forecast_result
        forecast = [round(x, 4) for x in forecast]

        last_value = self.market_trend_df[self.smoothed_avg_col][
            self.market_trend_df[self.date_col] == self.market_trend_df[self.date_col].max()
        ].tolist()[0]
        forecast.insert(0, last_value)

        future_dates = pd.date_range(start=self.market_trend_df[self.date_col].max(), periods=len(forecast), freq=self.freq)
        date_values = future_dates.strftime("%Y-%m-%d").tolist()
        future_forecast_df = pd.DataFrame({self.date_col: date_values, "预测值": forecast})
        future_forecast_df["趋势"] = future_forecast_df["预测值"].diff().apply(
            lambda x: self.rise_label if x > 0 else (self.fall_label if x < 0 else self.flat_label)
        )

        if len(self.reversed_market_trend_df) > 10:
            self.model_metrics = {
                "AIC": round(model_fit.aic, 2),
                "BIC": round(model_fit.bic, 2),
                "RMSE": round(np.sqrt(model_fit.mse), 4),
            }
        else:
            self.model_metrics = {"注意": "数据量不足，无法计算可靠的模型评估指标"}

        future_forecast_df = future_forecast_df.loc[
            future_forecast_df[self.date_col] > self.market_trend_df[self.date_col].max(),
            [self.date_col, "预测值", "趋势"],
        ]

        return future_forecast_df, forecast, list(map(str, forecast)), future_dates

    def forecast_data(self):
        return self._predict()

    def styled_forecast_data(self):
        future_forecast_df, forecast, str_forecast, future_dates = self._predict()
        future_forecast_df["预测值"] = future_forecast_df["预测值"].astype(str)
        future_forecast_df = future_forecast_df.set_index(self.date_col).T
        future7_df = future_forecast_df.style.map(
            lambda val: self._highlight_color(val), subset=pd.IndexSlice["趋势", :]
        )
        return future7_df, forecast, str_forecast, future_dates

    def get_model_info(self):
        info = {
            "模型参数": f"ARIMA{self.order}",
            "数据是否平稳": "是" if self.is_stationary else "否",
            "预测步数": self.steps,
        }
        if hasattr(self, "model_metrics"):
            info.update(self.model_metrics)
        return info

    def cross_validate(self, test_size=0.2):
        if len(self.reversed_market_trend_df) < 10:
            return {"错误": "数据量不足，无法进行交叉验证"}

        train_size = int(len(self.reversed_market_trend_df) * (1 - test_size))
        train, test = self.reversed_market_trend_df[:train_size], self.reversed_market_trend_df[train_size:]

        model = ARIMA(train, order=self.order)
        model_fit = model.fit()
        predictions = model_fit.forecast(steps=len(test))

        mse = np.mean((predictions - test) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(predictions - test))
        mape = np.mean(np.abs((test - predictions) / test)) * 100

        return {
            "均方误差(MSE)": round(mse, 4),
            "均方根误差(RMSE)": round(rmse, 4),
            "平均绝对误差(MAE)": round(mae, 4),
            "平均绝对百分比误差(MAPE)": round(mape, 2),
        }


class MultipleTrendPredictor:
    def __init__(self, market_trend_df, freq="B", order=(5, 1, 0), steps=7):
        require_analysis_deps("pandas", "statsmodels")
        self.market_trend_df = market_trend_df.copy()
        self.freq = freq
        self.order = order
        self.steps = steps

    def predict(self):
        self.market_trend_df = self.market_trend_df.sort_index(ascending=True)

        def predict_next_days(series, days):
            model = ARIMA(series, order=self.order)
            model_fit = model.fit()
            return model_fit.forecast(steps=days)

        predictions = pd.DataFrame()
        for column in self.market_trend_df.columns:
            predictions[column] = predict_next_days(self.market_trend_df[column].reset_index(drop=True), self.steps)

        last_date = self.market_trend_df.index.max() + pd.Timedelta(days=1)
        future_dates = pd.date_range(start=last_date, freq=self.freq, periods=self.steps)
        predictions.index = future_dates
        return predictions


__all__ = ["TrendPredictor", "MultipleTrendPredictor"]

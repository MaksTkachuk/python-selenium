metrics = {
"Price": ("Financial", "historyPrice"),
"Volume": ("Financial", "volume"),
"Development Activity": ("Development", "devActivity"),
"Twitter": ("Social", "historyTwitterData"),
"Social Volume": ("Social", "socialVolume"),
"Social Dominance": ("Social", "socialDominance"),
"Daily Active Deposits": ("On-chain",),
"Exchange Flow Balance": ("On-chain", "exchangeFundsFlow"),
"Eth Spent Over Time": ("On-chain", "ethSpentOverTime"),
"In Top Holders Total": ("On-chain", "topHoldersPercentOfTotalSupply"),
"Percent of Token Supply on Exchanges": ("On-chain", "percentOfTokenSupplyOnExchanges"),
"Realized Value": ("On-chain", "realizedValue"),
"Market Value To Realized Value": ("On-chain", "mvrvRatio"),
"NVT Ratio Circulation": ("On-chain", "nvtRatioCirculation"),
"NVT Ratio Transaction Volume": ("On-chain", "nvtRatioTxVolume"),
"Network Growth": ("On-chain", "networkGrowth"),
"Daily Active Addresses": ("On-chain", "dailyActiveAddresses"),
"Token Age Consumed": ("On-chain", "tokenAgeConsumed"),
"Token Velocity": ("On-chain", "tokenVelocity"),
"Transaction Volume": ("On-chain", "transactionVolume"),
"Token Circulation": ("On-chain", "tokenCirculation")
}

xpaths = {
"close_cookies_button": "//button[text()='Accept']",
"close_assets_button": "//button[text()='Dismiss']",
"page_element": """//div[@class="ChartPage_wrapper__805jp"]""",
"search_result": "//button[contains(@class, SearchWithSuggestions_suggestion__AqZNi)]//span[contains(text(), '{0}')]/././.",
"period_selector": "//div[contains(@class, 'ChartPage_ranges__3h7wX')]//div[text()='{0}']",
"period_selector_active": "//div[contains(@class, 'Selector_selected__2rsUx') and text()='{0}']",
"metrics_category": "//button[contains(text(), '{0}') and contains(@class, 'ChartMetricSelector_btn__1PClN')]",
"metrics_category_active": "//button[contains(text(), '{0}') and contains(@class, 'Button_active__3FPKU')]",
"metric": "//button[contains(text(), '{0}') and contains(@class, 'ChartMetricSelector_btn__1PClN')]",
"active_metric": "//button[contains(text(), '{0}') and contains(@class, 'ChartActiveMetrics_btn__3bHzp')]",
"inactive_metric": "//span[text()='no data']"
}

selectors = {
"search_wrapper": 'div.SearchWithSuggestions_wrapper__3BM6h',
"search_input": 'input.Input_input__1XjEb',
"metrics_container": 'div.ChartPage_container__2avm9.ChartPage_container_bottom__3Cwyv',
"metrics_categories": 'div.ChartMetricSelector_column__2SqCU.ChartMetricSelector_categories__uBPiA',
"metrics_list": 'div.ChartMetricSelector_group__FhAJt',
"active_metrics_panel": 'section.ChartActiveMetrics_wrapper__3Z0I8',
"share_dialog": 'div.Dialog_modal__1QXQD.Panel_panel__280Ap',
"share_link": 'input.Input_input__1XjEb.SharePanel_link__input__2bRzG',
"close_share_dialog": 'svg.Dialog_close__wPN0y',
"graph_title": 'div.ChartPage_title__fLVYV',
"calendar_dates": 'button.CalendarBtn_btn__2WS5X',
"interval": 'div.Dropdown_wrapper__2SIQh.IntervalSelector_wrapper__3_304'
}

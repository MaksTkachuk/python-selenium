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

chart_settings_options = {
"share": "Share",
"download": "Download as PNG"
}

xpaths = {
"close_cookies_button": "//button[text()='Accept']",
"close_assets_button": "//button[text()='Dismiss']",
"chart_page_element": """//div[@class="ChartPage_wrapper__805jp"]""",
"period_selector": "//div[contains(@class, 'ChartPage_ranges__3h7wX')]//div[text()='{0}']",
"period_selector_active": "//div[contains(@class, 'Selector_selected__2rsUx') and text()='{0}']",
"metrics_category": "//button[contains(text(), '{0}') and contains(@class, 'ChartMetricSelector_btn__1PClN')]",
"metrics_category_active": "//button[contains(text(), '{0}') and contains(@class, 'Button_active__3FPKU')]",
"metric": "//button[contains(@class, 'ChartMetricSelector_btn__1PClN')]//div[text()='{0}']/./.",
"active_metric": "//button[contains(text(), '{0}') and contains(@class, 'ChartActiveMetrics_btn__3bHzp')]",
"inactive_metric": "//span[text()='no data']",
"search_result": """//button[contains(@class, SearchWithSuggestions_suggestion__AqZNi)]//span[@class="SearchContainer_name__3fYwt"]""",
"chart_settings_menu_item": "//button[text()='{0}']",

}

selectors = {
"chart_header_element": "div.Header_wrapper__fXGgW",
"search_dialog": 'div.Dialog_modal__1QXQD.Panel_panel__280Ap',
"search_input": 'input.Input_input__1XjEb',
"search_result_list": "div.SearchWithSuggestions_suggestions__3z1wA",
"close_search_dialog": "svg.Dialog_close__wPN0y",
"token_selector_element": "div.Header_selector__3x1uF",
"token_selector_image": 'div.Header_selector__3x1uF img[alt="Bitcoin"]',
"metrics_menu": "div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n",
"modal_overlay": "div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO",
"metrics_categories": 'div.ChartMetricSelector_column__2SqCU.ChartMetricSelector_categories__uBPiA',
"metrics_list": 'div.ChartMetricSelector_group__FhAJt',
"active_metrics_panel": 'section.ChartActiveMetrics_wrapper__3Z0I8',
"close_active_metric": 'svg.ChartActiveMetrics_icon__17g9k',
"share_dialog": 'div.Dialog_modal__1QXQD.Panel_panel__280Ap',
"share_link": 'input.Input_input__1XjEb.SharePanel_link__input__2bRzG',
"close_share_dialog": 'svg.Dialog_close__wPN0y',
"graph_title": 'div.ChartPage_title__fLVYV',
"calendar_dates": 'button.CalendarBtn_btn__2WS5X',
"interval": 'div.Dropdown_wrapper__2SIQh.IntervalSelector_wrapper__3_304',
"metrics_menu_button": "button.ChartMetricsTool_trigger__3DzJE",
"chart_settings_button": "div.ChartPage_settings__group__p-3hT button.Button_button__16STw.Button_flat__2o9Q6",
"chart_settings_menu": "div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n",
"token_title": "h1.Header_project__name__2-7uj",

}

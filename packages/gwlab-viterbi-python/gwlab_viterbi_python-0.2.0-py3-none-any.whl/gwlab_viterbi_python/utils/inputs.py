from dataclasses import dataclass


@dataclass
class DataInput:
    """Data input class
    """
    data_choice: str = 'real'
    source_dataset: str = 'o3'


@dataclass
class DataParametersInput:
    """Data parameters input class
    """
    start_frequency_band: str = "188.0"
    min_start_time: str = "1238166483"
    max_start_time: str = "1254582483"
    asini: str = "0.01844"
    freq_band: str = "1.2136296"
    alpha: str = "4.974817413935078"
    delta: str = "-0.4349442914295658"
    orbit_tp: str = "1238161512.786"
    orbit_period: str = "4995.263"
    drift_time: str = "864000"
    d_freq: str = "5.78703704e-07"


@dataclass
class SearchParametersInput:
    """Search parameters input class
    """
    search_start_time: str = "1238166483"
    search_t_block: str = "864000"
    search_central_a0: str = "0.01844"
    search_a0_band: str = "0.00012"
    search_a0_bins: str = "1"
    search_central_p: str = "4995.263"
    search_p_band: str = "0.003"
    search_p_bins: str = "1"
    search_central_orbit_tp: str = "1238160263.9702501"
    search_orbit_tp_band: str = "260.8101737969591"
    search_orbit_tp_bins: str = "9"
    search_l_l_threshold: str = "296.27423"

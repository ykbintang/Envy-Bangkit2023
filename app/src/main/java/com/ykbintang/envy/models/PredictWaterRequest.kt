package com.ykbintang.envy.models

data class PredictWaterRequest(
    val fc: Int,
    val oxy: Int,
    val ph: Int,
    val tss: Int,
    val temp: Int,
    val tpn: Int,
    val tp: Int,
    val turb: Int
)

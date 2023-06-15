package com.ykbintang.envy.models

data class PredictAirRequest(
    val co: Int,
    val ozon: Int,
    val no2: Int,
    val pm25: Int
)

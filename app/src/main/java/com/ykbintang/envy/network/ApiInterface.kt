package com.ykbintang.envy.network

import com.ykbintang.envy.models.PredictWaterRequest
import com.ykbintang.envy.models.ApiResponse
import com.ykbintang.envy.models.PredictAirRequest
import com.ykbintang.envy.models.PredictSoilRequest
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST


interface ApiInterface {
    @POST("water?api_key=super")
    fun predictWater(@Body requestBody: PredictWaterRequest): Call<ApiResponse>
    @POST("soil?api_key=super")
    fun predictSoil(@Body requestBody: PredictSoilRequest): Call<ApiResponse>
    @POST("air?api_key=super")
    fun predictAir(@Body requestBody: PredictAirRequest): Call<ApiResponse>
}
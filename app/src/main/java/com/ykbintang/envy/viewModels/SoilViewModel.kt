package com.ykbintang.envy.viewModels

import androidx.lifecycle.MutableLiveData
import com.ykbintang.envy.models.ApiResponse
import com.ykbintang.envy.models.PredictSoilRequest
import com.ykbintang.envy.models.PredictWaterRequest
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class SoilViewModel: BaseViewModel() {
    val result = MutableLiveData<String>()

    fun detect(predictSoilRequest: PredictSoilRequest) {
        isLoading.postValue(true)
        api.predictSoil(predictSoilRequest).enqueue(object: Callback<ApiResponse> {
            override fun onResponse(
                call: Call<ApiResponse>,
                response: Response<ApiResponse>
            ) {
                isLoading.postValue(false)
                result.postValue(response.body()?.result)
            }

            override fun onFailure(call: Call<ApiResponse>, t: Throwable) {
                isLoading.postValue(false)
                onError.postValue(t.message)
            }
        })
    }
}
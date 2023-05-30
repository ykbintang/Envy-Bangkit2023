package com.ykbintang.envy.viewModels

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.ykbintang.envy.network.ApiInterface
import com.ykbintang.envy.network.RetrofitClient

open class BaseViewModel : ViewModel() {
    var isLoading = MutableLiveData(false)
    var onError = MutableLiveData("")
    var onSuccess = MutableLiveData<Boolean>()

    private val retrofit = RetrofitClient.getClient()
    val api = retrofit.create(ApiInterface::class.java)
}
package com.ykbintang.envy.network

import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient {
    private const val BASE_URL = "https://pentidur-mbd2rndo6a-et.a.run.app/"

    private val loggingInterceptor = HttpLoggingInterceptor().also {
        it.level = HttpLoggingInterceptor.Level.BODY
    }

    private val okHttpClient = OkHttpClient()
        .newBuilder()
        .addInterceptor(Interceptor { chain ->
            val request: Request =
                chain.request().newBuilder().addHeader("Authorization", "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").build()
            chain.proceed(request)
        })
        .build()

    fun getClient(): Retrofit =
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
}
package com.ykbintang.envy.views.air

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View.VISIBLE
import androidx.activity.viewModels
import com.google.android.material.snackbar.Snackbar
import com.ykbintang.envy.R
import com.ykbintang.envy.databinding.ActivityAirBinding
import com.ykbintang.envy.models.PredictAirRequest
import com.ykbintang.envy.models.PredictSoilRequest
import com.ykbintang.envy.viewModels.AirViewModel

class AirActivity : AppCompatActivity() {
    private lateinit var binding: ActivityAirBinding
    private val viewModel by viewModels<AirViewModel>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityAirBinding.inflate(layoutInflater)
        setContentView(binding.root)
        setSupportActionBar(binding.materialToolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = getString(R.string.deteksi_udara)

        binding.btnDetect.setOnClickListener { detect() }
        viewModel.result.observe(this) {
            if (it.isNotEmpty()) {
                binding.llResult.visibility = VISIBLE
                binding.tvResult.text = getString(
                    R.string.sistem_kami_memprediksi_bahwa_kualitas_udara_di_tempat_kamu,
                    it
                )
            }
        }
        viewModel.onError.observe(this) {
            if (it.isNotEmpty()) Snackbar.make(binding.root, it, Snackbar.LENGTH_SHORT).show()
        }
        viewModel.isLoading.observe(this) {
            binding.btnDetect.isEnabled = !it
        }
    }

    private fun detect() {
        val co = binding.etCo.text.toString()
        val o3 = binding.etO3.text.toString()
        val no2 = binding.etNo2.text.toString()
        val pm25 = binding.etPm25.text.toString()

        if (co.isEmpty() || o3.isEmpty() || no2.isEmpty() || pm25.isEmpty())
            Snackbar.make(binding.root, "Silahkan isi semua field!", Snackbar.LENGTH_SHORT).show()
        else {
            val predictAirRequest = PredictAirRequest(co.toInt(), o3.toInt(), no2.toInt(), pm25.toInt())
            viewModel.detect(predictAirRequest)
        }
    }
}